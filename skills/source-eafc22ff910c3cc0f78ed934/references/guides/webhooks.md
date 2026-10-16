# Guide: Webhooks
# Updated: 2026-06-22 | Source: Mercado Pago MCP (search_documentation)
#
# TRAP TO AVOID FIRST:
#   Validate x-signature BEFORE doing anything with the payload.
#   Respond 200 IMMEDIATELY — process asynchronously after.

---

## Complete working webhook receiver (Node.js / Express)

### Install

```bash
npm install express dotenv
```

### webhook-server.js

```js
import 'dotenv/config';
import express from 'express';
import crypto from 'node:crypto';

const app = express();
app.use(express.json());

const SECRET = process.env.MP_WEBHOOK_SECRET;

// ─── POST /webhooks/mp ────────────────────────────────────────────────────────
app.post('/webhooks/mp', async (req, res) => {
  // Step 1: Validate signature FIRST
  const signature = req.headers['x-signature'] ?? '';
  const requestId = req.headers['x-request-id'] ?? '';
  const parts = Object.fromEntries(
    signature.split(',').map(p => p.split('=').map(s => s.trim()))
  );
  const { ts, v1 } = parts;
  const dataId = req.body?.data?.id;

  if (!ts || !v1 || !dataId || !requestId) {
    return res.status(400).end();
  }

  const canonical = `id:${dataId};request-id:${requestId};ts:${ts};`;
  const expected = crypto.createHmac('sha256', SECRET).update(canonical).digest('hex');
  const valid = expected.length === v1.length &&
                crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(v1));

  if (!valid) return res.status(401).end();

  // Step 2: Respond 200 IMMEDIATELY
  res.status(200).end();

  // Step 3: Process asynchronously
  queueMicrotask(async () => {
    const { type, data } = req.body;
    console.log(`[webhook] type=${type} id=${data?.id}`);

    if (type === 'payment') {
      // Fetch payment to confirm status
      const r = await fetch(`https://api.mercadopago.com/v1/payments/${data.id}`, {
        headers: { Authorization: `Bearer ${process.env.MP_ACCESS_TOKEN}` },
      });
      const payment = await r.json();
      console.log(`[webhook] payment status=${payment.status} ref=${payment.external_reference}`);
      // → update your database here
    }

    if (type === 'merchant_order') {
      console.log(`[webhook] merchant_order id=${data?.id}`);
    }
  });
});

// ─── GET / — health check ─────────────────────────────────────────────────────
app.get('/', (req, res) => res.send('Webhook server running'));

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => console.log(`\n🔔 Webhook server at http://localhost:${PORT}/webhooks/mp\n`));
```

### .env

```
MP_WEBHOOK_SECRET=...          # from DevPanel → Webhooks → Signature secret
MP_ACCESS_TOKEN=APP_USR-...
PORT=3002
```

### package.json

```json
{ "type": "module", "scripts": { "start": "node webhook-server.js" } }
```

### Run & test locally

```bash
# Start server
node webhook-server.js

# Expose locally with ngrok (to receive real webhook events)
ngrok http 3002
# → gives you: https://xxxx.ngrok.io

# Register webhook URL (requires MCP auth)
# mcp__plugin_mercadopago_mcp__save_webhook(
#   callback="https://xxxx.ngrok.io/webhooks/mp",
#   topics=["payment", "merchant_order"]
# )

# Simulate a notification
# Trigger a real test payment instead:
# /mp-integrate test-setup → create test user
# make a payment → webhook fires → check delivery with notifications_history
```

---

## Notification topics

| Topic | When | Fetch |
|---|---|---|
| `payment` | Payments API status change | `GET /v1/payments/{id}` |
| `merchant_order` | Checkout Pro order update | `GET /merchant_orders/{id}` |
| `orders` | Orders API / QR / Point | `GET /v1/orders/{id}` |
| `subscription_preapproval` | Subscription status | `GET /preapproval/{id}` |
| `subscription_authorized_payment` | Recurring charge | `GET /authorized_payments/{id}` |

---

## Critical rules

| Rule | Why |
|---|---|
| Respond `200` before processing | MP retries on non-200 up to 24h |
| Validate `x-signature` first | Never process unsigned notifications |
| Use `timingSafeEqual` | Prevents timing attacks |
| Dedup on `data.id + type` | Same notification can arrive multiple times |

---

## Pre-production checklist

- [ ] Webhook URL registered via MCP `save_webhook` or DevPanel
- [ ] `MP_WEBHOOK_SECRET` in `.env`
- [ ] `x-signature` validated with HMAC-SHA256
- [ ] Responds `200` before processing
- [ ] Idempotent handler (dedup on `data.id + type`)
- [ ] Tested by triggering a real test payment and confirming delivery via `notifications_history`
