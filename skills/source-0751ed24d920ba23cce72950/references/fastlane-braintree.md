---
name: paypal-fastlane-braintree
description: Braintree Fastlane accelerated guest checkout via the Braintree gateway - gateway.clientToken.generate, braintree-web fastlane sub-module, and payment-method nonces.
---

# Fastlane (Braintree variant)

> **This file describes Fastlane when integrated through the Braintree gateway.** If the merchant uses the PayPal JS SDK directly (no Braintree gateway), see [fastlane.md](fastlane.md) and stop reading here — the SDK package, client-token flow, script tags, and charge path all differ. Mixing the two will produce broken code.

**When to Use:** Developer is on the Braintree gateway (uses `braintree-web` on the client and the `braintree` Node SDK / equivalent on the server) and asks about Fastlane, accelerated guest checkout, or auto-fill for returning shoppers.
**When NOT to Use:** Developer integrates Fastlane directly through `https://www.paypal.com/sdk/js?...&components=fastlane` (no Braintree gateway) — go to [fastlane.md](fastlane.md). Native mobile apps (web-only, including mobile web).

## Overview

[Braintree Fastlane](https://developer.paypal.com/braintree/docs/guides/fastlane/overview/) is the same accelerated guest checkout product as PayPal-direct Fastlane, delivered through the Braintree gateway. The API surface (`identity.lookupCustomerByEmail`, `triggerAuthenticationFlow`, `FastlanePaymentComponent`, `profile.showShippingAddressSelector`) is intentionally identical — only the bootstrap, the client-token source, and the charge path differ.

Fastlane must be **enabled in the Braintree control panel** before it works in sandbox or production: *Account Settings → Customer Checkout → Turn On*. ([Setup and Integration](https://developer.paypal.com/braintree/docs/guides/fastlane/setup-integration/))

## PayPal-direct → Braintree: what changed (do not confuse)

| Concern | PayPal-direct ([fastlane.md](fastlane.md)) | Braintree (this file) |
|---|---|---|
| Server SDK | `@paypal/paypal-server-sdk` or raw REST | `braintree` (Node) — requires **≥ 3.25.0**. No Fastlane-specific server changes |
| Client token | `POST /v1/oauth2/token` with `response_type=client_token&intent=sdk_init` | `gateway.clientToken.generate({ domains: [...] })` — Braintree SDK call |
| Client token field on the wire | `access_token` (despite `response_type=client_token`) | `response.clientToken` (camelCase, on the gateway response) |
| Script load | One tag: `paypal.com/sdk/js?...&components=fastlane` + `data-sdk-client-token` attr | **Three** tags from `js.braintreegateway.com`: `client.min.js`, `fastlane.js`, `data-collector.min.js` — all the same version, **≥ 3.120.0** |
| `data-*` script attrs | `data-sdk-client-token` (REQUIRED) | **None.** Token is passed in JS to `braintree.client.create({ authorization })` |
| Init | `await paypal.Fastlane({})` (arg required) | `braintree.client.create` → `braintree.dataCollector.create` → `braintree.fastlane.create({ client, deviceData, authorization })` |
| Payment token field | `payment_source.card.single_use_token` (or `paymentSource.card.singleUseToken`) | `paymentMethodNonce` — Braintree returns a standard nonce via `PaymentToken.id` |
| Charge | `POST /v2/checkout/orders` then `/capture` | `gateway.transaction.sale({ amount, paymentMethodNonce, options: { submitForSettlement: true } })` |
| CSP additions | `*.paypal.com`, `*.paypalobjects.com` | `*.paypal.com`, `*.paypalobjects.com`, `*.braintreegateway.com`, `*.braintree-api.com` |

> Generating PayPal-direct code? Stop here and use [fastlane.md](fastlane.md) — auth, init, script-loading, and charge path all differ.

## Common mistakes

These are failure modes that have shipped broken Braintree-Fastlane integrations.

| Mistake | Why it's wrong | Correct |
|---|---|---|
| `import braintreeFastlane from '@braintree/fastlane'` | That package doesn't exist. Fastlane ships as a sub-module of `braintree-web`. | CDN: load `https://js.braintreegateway.com/web/<ver>/js/fastlane.js`. NPM: `import fastlane from 'braintree-web/fastlane'` (with matching `braintree-web/client` and `braintree-web/data-collector`). |
| Calling `POST /v1/oauth2/token` to get the client token | That endpoint produces a PayPal-direct Fastlane client token, which the Braintree SDK won't accept. | Server: `gateway.clientToken.generate({ domains: ['example.com'] })` (see [§1](#1-client-token-server-side)). |
| Omitting `domains` from `clientToken.generate` on a deployed site | Fastlane silently fails to recognise returning customers. The docs warn: *"Omitting the root domain will cause Fastlane to malfunction and will prevent it from working entirely."* | Always pass `domains: ['<root-domain>']` for any non-localhost environment. Root domain only — no subdomains, no wildcards, no `https://` prefix. **Exception: when running on `localhost`, omit `domains` entirely** — `localhost` is not a registrable root domain and Braintree will reject it. ([Server-side / Node](https://developer.paypal.com/braintree/docs/guides/fastlane/server-side/node/)) |
| `domains: ['sub.example.com']`, `domains: ['*.example.com']`, `domains: ['https://example.com']` | All three are rejected. The field is the **root domain only**. | `domains: ['example.com']` — repeat in the array for multiple roots. |
| Loading scripts at mixed versions (e.g. `client@3.116`, `fastlane@3.120`, `data-collector@3.110`) | The three modules share internal contracts; mismatched versions throw at runtime. | Pin all three to the same version, **≥ 3.120.0**. ([Client-side, Step 1](https://developer.paypal.com/braintree/docs/guides/fastlane/client-side/)) |
| Adding `data-sdk-client-token="…"` (or `data-client-token="…"`) to the Braintree script tags | Those attributes belong to PayPal-direct Fastlane / Braintree Drop-in respectively. Braintree Fastlane reads the token from JS. | No script attributes. Pass the token as `braintree.client.create({ authorization: clientToken })`. |
| Skipping `data-collector` / `deviceData` | The SDK initialises without it, but risk decisioning and Premium Fraud Protection are degraded. | Always create `dataCollectorInstance`, then pass `deviceData` to both `fastlane.create` and `transaction.sale`. |
| Sending the token as `payment_source.card.single_use_token` on a `/v2/checkout/orders` call | That's the PayPal-direct shape on a PayPal-direct endpoint. Braintree Fastlane returns a Braintree nonce; the charge runs through Braintree. | `gateway.transaction.sale({ paymentMethodNonce: paymentToken.id, ... })`. |
| Forgetting to enable Fastlane in the Braintree control panel | Even the sandbox is gated. SDK init succeeds but identity lookup never finds returning shoppers. | *Sandbox / Production control panel → Account Settings → Customer Checkout → Turn On*. ([Setup and Integration](https://developer.paypal.com/braintree/docs/guides/fastlane/setup-integration/)) |
| Missing CSP entries for `*.paypalobjects.com` | The `fastlane.js` loader fetches the AXO runtime from `paypalobjects.com`. CSP without it silently blocks initialisation. | See the CSP block in [Performance & availability](#performance--availability). |
| `region: "California"` in a shipping/billing address | Braintree requires the 2-letter region code; the long form is rejected. | `region: "CA"`. |

## Braintree Integration

### 1. Client token (server-side)

Generate the client token via the Braintree Node SDK. The Fastlane-specific knob is `domains`. There is **no** OAuth dance — Braintree's gateway credentials are used directly.

```js
// Node — verified against braintree/fastlane-sample-application-sdk (server/node/src/server.js)
import braintree from "braintree";

const gateway = new braintree.BraintreeGateway({
  environment: braintree.Environment.Sandbox,    // braintree.Environment.Production for prod
  merchantId:  process.env.BRAINTREE_MERCHANT_ID,
  publicKey:   process.env.BRAINTREE_PUBLIC_KEY,
  privateKey:  process.env.BRAINTREE_PRIVATE_KEY,
});

app.get("/api/client-token", async (_req, res) => {
  // REQUIRED on any deployed host. Root domains only — no subdomains, no wildcards,
  // no protocols. Multiple roots: ["example.com", "example2.com"].
  // On localhost, omit `domains` entirely — Braintree rejects "localhost" as a root.
  const rootDomain = process.env.FASTLANE_ROOT_DOMAIN;   // e.g. "example.com"
  const response = await gateway.clientToken.generate(
    rootDomain ? { domains: [rootDomain] } : {}
  );
  // Field is `clientToken` (camelCase) on the gateway response.
  res.json({ clientToken: response.clientToken });
});
```

The same `BraintreeGateway` instance is reused for the later `transaction.sale` call — there is no separate access token to manage.

> **Why `domains` matters.** Quote from the official guide: *"You must include your root domain in the client token request. Omitting the root domain will cause Fastlane to malfunction and will prevent it from working entirely."* ([Server-side / Node](https://developer.paypal.com/braintree/docs/guides/fastlane/server-side/node/)). The PayPal-direct equivalent (`domains[]` on `POST /v1/oauth2/token`) is optional in sandbox; the Braintree equivalent is **required on every deployed host**. The one exception is local development on `localhost` — there is no registrable root domain to declare, and Braintree rejects `"localhost"` as a value, so the field must be **omitted entirely** in that case.

GraphQL equivalent:

```graphql
mutation ($input: CreateClientTokenInput) {
  createClientToken(input: $input) { clientToken }
}
# variables: { "input": { "clientToken": { "domains": ["example.com"] } } }
```

### 2. Script tags (client-side)

**Three** script tags are required, all pinned to the same version, **≥ 3.120.0**. Unlike PayPal-direct Fastlane, no `data-*` attributes are needed.

```html
<script src="https://js.braintreegateway.com/web/3.141.0/js/client.min.js"></script>
<script src="https://js.braintreegateway.com/web/3.141.0/js/fastlane.js"></script>
<script src="https://js.braintreegateway.com/web/3.141.0/js/data-collector.min.js"></script>
```

NPM/ESM equivalent (samples use CDN, but the per-module ESM imports work):

```js
import client        from "braintree-web/client";
import fastlane      from "braintree-web/fastlane";
import dataCollector from "braintree-web/data-collector";
```

> The CDN's `fastlane.js` is a ~40 KB loader that fetches the real Fastlane runtime ("AXO") from `https://www.paypalobjects.com/connect-boba/axo.min.js`. CSP must allow `*.paypalobjects.com` (see [§6](#performance--availability)).

### 3. Initialization

Three SDK calls in order: client → data collector → Fastlane. Single-use payment tokens are valid only for the current session; always run identity lookup again on page reload.

```js
// Verified against braintree/fastlane-sample-application-sdk (client/html/src/init-fastlane.js)

// 3a. Braintree client — wraps the client token for all downstream modules.
const clientInstance = await braintree.client.create({
  authorization: clientToken,                  // from /api/client-token
});

// 3b. Data collector — produces deviceData for fraud/risk decisioning.
const dataCollectorInstance = await braintree.dataCollector.create({
  client: clientInstance,
});
const deviceData = dataCollectorInstance.deviceData;

// 3c. Fastlane — pass the token AGAIN here, plus the client and deviceData.
const fastlaneInstance = await braintree.fastlane.create({
  authorization: clientToken,
  client:        clientInstance,
  deviceData,                                  // recommended, not strictly required
  styles: { root: { backgroundColorPrimary: "#ffffff" } },   // optional
  // shippingAddressOptions: { allowedLocations: ["US:CA"], noShipping: false },  // optional
  // cardOptions: { allowedBrands: ["VISA", "MASTERCARD"] },                       // optional
});

const {
  identity,
  profile,
  FastlanePaymentComponent,
  FastlaneCardComponent,        // lower-level: card-only, you supply billing address
  FastlaneWatermarkComponent,   // "secured by Fastlane" mark
} = fastlaneInstance;

// fastlaneInstance.setLocale("en_us")  // en_us | es_us | fr_us | zh_us
// fastlaneInstance.events.{ checkoutPageLoaded | apmSelected | emailSubmitted |
//                           orderPlaced | checkoutEnd | storeAccountCreated }
```

### 4. Identity lookup + payment component

The shopper-facing API matches PayPal-direct Fastlane exactly — only the payment-token return shape differs (Braintree returns a `PaymentToken` whose `.id` is a standard payment-method nonce).

```js
// Email lookup → authentication
const { customerContextId } = await identity.lookupCustomerByEmail(email);

const { authenticationState, profileData } =
  await identity.triggerAuthenticationFlow(customerContextId);
// authenticationState: "succeeded" | "failed" | "canceled" | "not_found"

let shippingAddress;
if (authenticationState === "succeeded") {
  // Optional: let the buyer pick from saved addresses / cards.
  ({ selectedAddress: shippingAddress } = await profile.showShippingAddressSelector());
  // Also available: await profile.showCardSelector();
  shippingAddress = shippingAddress ?? profileData.shippingAddress;
}

// FastlanePaymentComponent handles BOTH member (saved card) and guest UI.
const paymentComponent = await fastlaneInstance.FastlanePaymentComponent({
  shippingAddress,                              // optional pre-fill
  // options: { fields: { phoneNumber: { prefill: "5551234567" } } },
});
await paymentComponent.render("#payment-container");

// Later (after buyer clicks Pay):
const paymentToken = await paymentComponent.getPaymentToken();
// paymentToken.id                                     ← Braintree paymentMethodNonce
// paymentToken.paymentSource.card.billingAddress      ← collected billing address
// POST { nonce: paymentToken.id, deviceData, billing: paymentToken.paymentSource.card.billingAddress,
//        shipping: shippingAddress, customer, amount } to your server.
```

> `FastlaneCardComponent` is the lower-level card-only variant — use it only if you intend to supply the billing address from your own form. **Prefer `FastlanePaymentComponent`** otherwise.

### 5. Transaction (server-side)

The Fastlane payment token IS a Braintree payment-method nonce. Charge it with the standard `transaction.sale` call — there's no Fastlane-specific endpoint, and no field renamed for Fastlane.

```js
// Verified against fastlane-sample-application-sdk (server/node/src/server.js)
app.post("/api/transaction", async (req, res) => {
  const { nonce, deviceData, billing, shipping, customer, amount } = req.body;

  gateway.transaction.sale(
    {
      amount,                                            // string, e.g. "10.00"
      paymentMethodNonce: nonce,                         // paymentToken.id from the client
      deviceData,                                        // from data-collector
      customer,                                          // { firstName, lastName, email }
      billing,                                           // from paymentToken.paymentSource.card.billingAddress
      // REQUIRED IF you want the shipping address saved back to the Fastlane profile:
      ...(shipping && {
        shipping: { ...shipping, shippingMethod: "ground" },
      }),
      options: { submitForSettlement: true },            // auth + capture in one call
    },
    (error, result) => {
      if (error)        return res.status(500).json({ error: error.message });
      if (!result.success) return res.status(400).json({ error: result.message, errors: result.errors });
      res.json({ transactionId: result.transaction.id });
    }
  );
});
```

> **Including `shipping` saves the address back to the buyer's Fastlane profile** for next time — the docs call this out explicitly ([Server-side / Node](https://developer.paypal.com/braintree/docs/guides/fastlane/server-side/node/)). Omit it only if you genuinely don't ship physical goods.

GraphQL equivalent uses `chargeCreditCard` with `paymentMethodId: paymentToken.id` and `transaction.riskData.deviceData`. ([Server-side](https://developer.paypal.com/braintree/docs/guides/fastlane/server-side/))

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Fastlane initialises but `lookupCustomerByEmail` never recognises returning shoppers | (1) `domains` missing from `gateway.clientToken.generate` on a deployed host (omit `domains` only on `localhost`); (2) Fastlane not enabled in the Braintree control panel (Account Settings → Customer Checkout → Turn On); (3) browser origin's root domain doesn't match the registered `domains`. |
| `Invalid authorization` from `braintree.client.create` | Client token was generated against a different gateway (sandbox vs production mismatch), or the token has been reused past its lifetime. Generate a fresh one per session. |
| `fastlane.js` throws / network errors before init | CSP missing `*.paypalobjects.com`. Fastlane's CDN loader fetches the AXO runtime from there; without it, init aborts silently. |
| Version mismatch errors at runtime | The three script tags (`client`, `fastlane`, `data-collector`) are on different `braintree-web` versions. Pin all three to the same version, ≥ 3.120.0. |
| `transaction.sale` returns `validation error` on `region` | Address `region` is the long form (e.g. `"California"`). Use the 2-letter code (`"CA"`). |
| Saved shipping address isn't appearing for the same buyer on a later visit | The previous `transaction.sale` omitted the `shipping` block. Re-include it on every Fastlane transaction. |
| `paymentMethodNonce` not found / consumed | Nonces are single-use. If `transaction.sale` failed, request a new nonce by calling `paymentComponent.getPaymentToken()` again — don't retry with the same nonce. |
| Fastlane works in production but not sandbox | Fastlane must be turned on **separately** in the sandbox control panel — it's not enabled by default. |
| `@braintree/fastlane` not found on `npm install` | That package doesn't exist. Use `braintree-web` and import the `fastlane` sub-module. |

## Performance & availability

- **Availability:** Web only (desktop + mobile responsive); no native mobile apps. For supported regions and currencies, see the [Overview](https://developer.paypal.com/braintree/docs/guides/fastlane/overview/) or check the merchant's Braintree control panel.
- **PayPal must be presented** as a payment option alongside the Fastlane email field — this is a requirement of the program, not just a recommendation.
- **Billing address collection is mandatory** on the checkout page.

**Required CSP** ([Advanced Options](https://developer.paypal.com/braintree/docs/guides/fastlane/advanced-option/)):

```http
Content-Security-Policy:
  connect-src https://*.paypal.com https://*.paypalobjects.com
              https://*.braintreegateway.com https://*.braintree-api.com;
  font-src    https://*.paypalobjects.com;
  frame-src   https://*.paypal.com https://*.braintreegateway.com;
  img-src     https://*.paypal.com https://*.paypalobjects.com;
  script-src  https://*.paypal.com https://*.paypalobjects.com https://*.braintreegateway.com;
  style-src   'unsafe-inline';
```

**Versioning:**
- `braintree-web` added Fastlane in **3.103.0** (2024-07-11). The current minimum supported version is **3.120.0**.
- `braintree` (Node) requires **≥ 3.25.0**. No Fastlane-specific server-SDK changes — the server just charges a nonce.

## Live Documentation
- [Overview](https://developer.paypal.com/braintree/docs/guides/fastlane/overview/)
- [Setup and Integration (enable Fastlane in the control panel)](https://developer.paypal.com/braintree/docs/guides/fastlane/setup-integration/)
- [Client-side Integration](https://developer.paypal.com/braintree/docs/guides/fastlane/client-side/)
- [Server-side (overview)](https://developer.paypal.com/braintree/docs/guides/fastlane/server-side/)
- [Server-side (Node)](https://developer.paypal.com/braintree/docs/guides/fastlane/server-side/node/)
- [Reference Types (TypeScript interfaces for the Fastlane instance, identity, profile, components)](https://developer.paypal.com/braintree/docs/guides/fastlane/reference/)
- [Advanced Options (CSP, locale, watermark)](https://developer.paypal.com/braintree/docs/guides/fastlane/advanced-option/)
- [Testing and Go-Live](https://developer.paypal.com/braintree/docs/guides/fastlane/testing-go-live/)
- Verified working sample (SDK): [braintree/fastlane-sample-application-sdk](https://github.com/braintree/fastlane-sample-application-sdk) — Node + Java + Python + PHP + Ruby + .NET servers; HTML + Vue + Angular clients
- Verified working sample (GraphQL): [braintree/fastlane-sample-application-graphql](https://github.com/braintree/fastlane-sample-application-graphql)
