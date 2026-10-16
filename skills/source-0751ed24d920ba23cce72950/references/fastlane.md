---
name: paypal-fastlane-v5
description: PayPal Fastlane accelerated guest checkout for JS SDK v5 - FastlanePaymentComponent, identity lookup, and single-use payment tokens (US-only).
---

# Fastlane (v5 SDK)

> **This file describes Fastlane on JS SDK v5 only.** For v6, see [js-sdk-v6.md](js-sdk-v6.md) and stop reading here — the script-load and init pattern differ. Mixing the two will produce broken code.

**When to Use:** Developer is on JS SDK v5 and asks about accelerated guest checkout, auto-fill for returning shoppers, or Fastlane integration.
**When NOT to Use:** Standard checkout for new buyers (see [checkout.md](checkout.md)). Non-US merchants (Fastlane is US-only). Any v6 integration — go to [js-sdk-v6.md](js-sdk-v6.md).

## Overview

[Fastlane](https://developer.paypal.com/studio/checkout/fastlane) is PayPal's accelerated guest checkout that auto-fills returning shoppers' payment and shipping details using their PayPal profile. US-only, available through the PayPal JS SDK.

## v5 → v6: what changed (do not confuse)

| Concern | v5 (this file) | v6 ([js-sdk-v6.md](js-sdk-v6.md)) |
|---|---|---|
| Init | `paypal.Fastlane({})` (**arg required, even if empty**) | `sdkInstance.createFastlane()` |
| Auth | **Client ID + `data-sdk-client-token` script attribute** (both required) | Client token passed to `createInstance({ clientToken })` |
| Default component | **`FastlanePaymentComponent`** (member + guest) | **`FastlanePaymentComponent`** (same name, different init) |
| Low-level card-only component | `FastlaneCardComponent` (rarely needed) | n/a |
| Script load | URL params: `components=buttons,fastlane` | `<script src=".../web-sdk/v6/core">` |

> Generating v6 code? Stop here and use [js-sdk-v6.md](js-sdk-v6.md) — auth, init, and script-loading model all differ.

## Common mistakes

These are failure modes that have shipped broken Fastlane integrations. Verify each against the [PayPal sample integration](https://github.com/paypaldev/fastlane_paypal_video_project/blob/main/netlify/functions/api.js).

| Mistake | Why it's wrong | Correct |
|---|---|---|
| `POST /v1/identity/generate-token` for the client token | That endpoint generates a buyer-vault client token, not the SDK-init token Fastlane needs. | `POST /v1/oauth2/token` with body `grant_type=client_credentials&response_type=client_token&intent=sdk_init` (see [§1](#1-client-token-server-side)) |
| `"domains[]": "localhost"` (or any non-hostname value) in the client-token body | PayPal rejects `localhost`, `127.0.0.1`, raw IPs, and unregistered hostnames with `invalid_domain`. The parameter is for *registered* origins only. | **Omit `domains[]` entirely for sandbox/local dev.** For production, list every registered origin (e.g. `"domains[]": "shop.example.com"`) — repeat the key for multiple. |
| Renaming the JSON response field from `access_token` to `client_token` | When `response_type=client_token` is set, PayPal still returns the client-safe JWT in the `access_token` field. The field name does not change to match the request type. Renaming reads `undefined` and the SDK then throws `"missing/invalid authorization token"`. | `const { access_token: clientToken } = await response.json();` |
| `data-client-token="…"` on the script tag | That attribute belongs to Braintree, not the PayPal JS SDK. | `data-sdk-client-token="…"` |
| `await paypal.Fastlane()` (no argument) | The SDK requires a config object, even if empty. Throws a `TypeError` otherwise. | `await paypal.Fastlane({})` |
| `payment_source: { token: { id, type: "SINGLE_USE" } }` in the order create | That shape is for vaulted tokens. Fastlane single-use tokens go under `payment_source.card`. | `payment_source: { card: { single_use_token: "<token>" } }` |
| Using `@paypal/paypal-server-sdk` camelCase fields in a raw REST `fetch` body | The REST API only accepts snake_case. CamelCase only applies inside the server SDK's typed methods. | Pick one: raw REST with `single_use_token`, or `ordersController.createOrder()` with `singleUseToken` — never both shapes in the same payload |
| Concluding "merchant account not provisioned for Fastlane" from a decoded `idToken: null` | The token was just a `client_credentials` access token — it can't carry Fastlane claims because the `response_type=client_token&intent=sdk_init` params weren't sent. | Fix the client-token request body first. Don't escalate to PayPal support based on JWT decoding alone. |

## v5 Integration

### 1. Client token (server-side)

Fastlane requires a **client token** (NOT a plain access token) loaded into the SDK via `data-sdk-client-token`. Generate it with `POST /v1/oauth2/token` using these extra form params:

```javascript
// Node — verified against paypaldev/fastlane_paypal_video_project
const auth = Buffer.from(`${PAYPAL_CLIENT}:${PAYPAL_SECRET}`).toString("base64");

const params = new URLSearchParams({
  grant_type: "client_credentials",
  response_type: "client_token",
  intent: "sdk_init",
});

// PRODUCTION ONLY: list every registered origin. OMIT entirely for sandbox/localhost.
// PayPal rejects "localhost", "127.0.0.1", raw IPs, and unregistered hostnames with invalid_domain.
if (process.env.NODE_ENV === "production") {
  params.append("domains[]", "shop.example.com");
  // params.append("domains[]", "checkout.example.com"); // repeat for multiple
}

const response = await fetch("https://api-m.sandbox.paypal.com/v1/oauth2/token", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": `Basic ${auth}`,
  },
  body: params,
});

// The field is `access_token`, not `client_token` — even though response_type=client_token.
// Reading data.client_token returns undefined and the SDK throws "invalid authorization token".
const { access_token: clientToken } = await response.json();
// Return clientToken to the browser — safe to expose, scoped to the listed domains (if any).
```

Sandbox and production share the same endpoint path (only the host differs: `api-m.sandbox.paypal.com` vs `api-m.paypal.com`).

> **About `intent=sdk_init`:** strictly required when you use Fastlane's identity lookup (`lookupCustomerByEmail` → `triggerAuthenticationFlow`). Without it, PayPal returns a plain `client_credentials` token whose decoded JWT has `idToken: null`, and authentication silently fails. The v6 official sample omits the param because its flow only renders the payment component without identity lookup — don't use that omission as a model. If your integration calls `identity.*`, send `intent=sdk_init`.

### 2. Script tag (client-side)

```html
<script
  src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&components=buttons,fastlane"
  data-sdk-client-token="CLIENT_TOKEN_FROM_STEP_1"
  data-sdk-integration-source="developer-studio"
  defer
></script>
```

The attribute name is `data-sdk-client-token` — not `data-client-token`. `defer` matters because the init code runs after DOM ready.

### 3. Initialization

Single-use tokens are generated client-side and valid for 3 hours — always call `triggerAuthenticationFlow()` on page reload. Fastlane does not support creating customers or payment methods before a transaction.

#### Quick Start vs Flexible for Fastlane's card collection UI

| | Quick Start | Flexible |
|---|---|---|
| **What it is** | A pre-built PayPal form that handles card collection end-to-end | Uses `FastlaneCardComponent` for card input, but you control the layout and styling of the billing address fields |
| **Choose this when** | You want minimal integration effort | You need to own the billing address form, or the pre-built UI doesn’t match your page design |
| **You are responsible for** | Rendering `FastlanePaymentComponent` | For Fastlane members with a stored card: the selected card from the profile object, Fastlane watermark, and a "Change card" button that invokes `showCardSelector()`. For members with no card and guest payers: `FastlaneCardComponent` for card input + your own form fields to collect the billing address |

> The code sample below uses **Quick Start** (`FastlanePaymentComponent` handles everything). If you choose Flexible, replace the `FastlanePaymentComponent` blocks with `FastlaneCardComponent` and add your own billing address form fields — see the [PayPal Fastlane integrate guide](https://developer.paypal.com/studio/checkout/fastlane/integrate) for the per-persona rendering requirements.

```javascript
// Either destructure or attach properties — but ALWAYS pass {}.
const { identity, profile, FastlanePaymentComponent, FastlaneWatermarkComponent } =
  await window.paypal.Fastlane({});

// Optional but recommended: render the "secured by Fastlane" watermark near the email/payment fields
const watermark = await FastlaneWatermarkComponent({ includeAdditionalInfo: true });
watermark.render("#watermark-container");

// Email lookup → authentication
const { customerContextId } = await identity.lookupCustomerByEmail(email);
const { authenticationState, profileData } =
  await identity.triggerAuthenticationFlow(customerContextId);

if (authenticationState === "succeeded") {
  // Member: optionally let the buyer pick a saved shipping address or saved card
  const { selectedAddress } = await profile.showShippingAddressSelector();
  // Also available: await profile.showCardSelector() — opens UI to switch the saved card

  // FastlanePaymentComponent handles BOTH member (saved card) and guest UI
  const paymentComponent = await FastlanePaymentComponent({
    shippingAddress: profileData.shippingAddress,
  });
  paymentComponent.render("#payment-container");

  // No args — component collects what it needs internally
  const { id: singleUseToken } = await paymentComponent.getPaymentToken();
  // POST singleUseToken to your server, then create the order (step 4).
} else {
  // Guest: same component, no shipping address yet
  const paymentComponent = await FastlanePaymentComponent({});
  paymentComponent.render("#payment-container");
  const { id: singleUseToken } = await paymentComponent.getPaymentToken();
}
```

> `FastlaneCardComponent` exists as a lower-level option for cases where you want only the card-entry form and will supply billing address yourself — **prefer `FastlanePaymentComponent`** unless you specifically need that.

### 4. Create the order (server-side, REST)

The single-use token goes under `payment_source.card.single_use_token` — NOT under `payment_source.token`, and NOT under any vault token shape.

```javascript
const payload = {
  intent: "CAPTURE",
  purchase_units: [{
    amount: {
      currency_code: "USD",
      value: "10.00",
      breakdown: {
        item_total: { currency_code: "USD", value: "10.00" },
      },
    },
    items: [{
      name: "Sample item",
      quantity: "1",
      category: "PHYSICAL_GOODS",
      unit_amount: { currency_code: "USD", value: "10.00" },
    }],
    soft_descriptor: "MYBIZ",
  }],
  payment_source: {
    card: {
      single_use_token: singleUseToken,             // from FastlanePaymentComponent.getPaymentToken()
      experience_context: {
        brand_name: "My Store",
        shipping_preference: "GET_FROM_FILE",
        user_action: "PAY_NOW",
        payment_method_preference: "IMMEDIATE_PAYMENT_REQUIRED",
      },
    },
  },
};

const orderResponse = await fetch(`${PAYPAL_API_BASE_URL}/v2/checkout/orders`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${accessToken}`,        // standard OAuth access token, NOT the client token
    "PayPal-Request-Id": crypto.randomUUID(),         // idempotency key
  },
  body: JSON.stringify(payload),
});
```

> Using `@paypal/paypal-server-sdk` instead of raw REST? The field becomes `paymentSource.card.singleUseToken` (camelCase). **Don't mix shapes in a single payload.**

### 5. Capture

Standard `POST /v2/checkout/orders/{id}/capture` — no Fastlane-specific quirks.

### 6. Optional - 3D Secure (3DS)

> **Only implement this section if the developer explicitly requests 3DS, SCA, PSD2, or liability shift. If not mentioned, skip this section entirely.**

Add 3DS to reduce fraud and shift chargeback liability to the issuer. Required for EU/UK merchants under PSD2/SCA. See [3D Secure for Fastlane](https://developer.paypal.com/docs/checkout/fastlane/3d-secure/) for the full guide.

Two integration paths:

**JavaScript SDK 3DS Component** — check eligibility client-side, trigger challenge if needed. Supports retry. Returns `liabilityShift` and `authenticationState` only (no `enrollmentStatus`).

Add `three-domain-secure` to the components param in your script tag:

```html
<script
  src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&components=buttons,fastlane,three-domain-secure"
  data-sdk-client-token="CLIENT_TOKEN_FROM_STEP_1"
  defer
></script>
```

```javascript
const threeDomainSecureComponent = window.paypal.ThreeDomainSecureClient;

const threeDomainSecureParameters = {
  amount: "12.00",
  currency: "USD",
  nonce: singleUseToken,                  // from FastlanePaymentComponent.getPaymentToken()
  threeDSRequested: "SCA_WHEN_REQUIRED",  // or "SCA_ALWAYS" to force 3DS
  transactionContext: {
    experience_context: {
      brand_name: "YourBrandName",
      locale: "en-US",
      return_url: "https://example.com/returnUrl",
      cancel_url: "https://example.com/cancelUrl",
    },
    transaction_context: {                // optional
      soft_descriptor: "Card verification hold",
    },
  },
};

const isThreeDomainSecureEligible = await threeDomainSecureComponent.isEligible(
  threeDomainSecureParameters,
);

// Call on submit — await 3DS completion before creating the order
if (isThreeDomainSecureEligible) {
  const { liabilityShift, authenticationState, nonce } =
    await threeDomainSecureComponent.show();
  // liabilityShift: "possible" | "no" | "unknown"
  // authenticationState: "success" | "cancelled" | "errored"
  // nonce: enriched token — use this instead of singleUseToken when creating the order
  if (authenticationState === "success") {
    // Check liabilityShift and proceed with order creation
  } else {
    // Cancelled or errored — retry 3DS or proceed without it
  }
}
```

**Orders v2 API** — embed 3DS in order creation server-side. Returns all three params (`liability_shift`, `enrollment_status`, `authentication_status`). Does not support retry after failure.

Add `attributes.verification` to the order create payload from Step 4:

```javascript
payment_source: {
  card: {
    single_use_token: singleUseToken,
    attributes: {
      verification: {
        method: "SCA_WHEN_REQUIRED", // or "SCA_ALWAYS"
      },
    },
  },
},
```

After order creation, redirect the buyer to the `rel: payer-action` HATEOAS link in the response. Once they return, call `GET /v2/checkout/orders/{id}` to read `authentication_result` before capturing.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `"Missing/invalid authorization token"` from the SDK | One of: (1) `data-sdk-client-token` attribute missing/misspelled (e.g. `data-client-token`); (2) you read `data.client_token` from the OAuth response — it's `data.access_token`; (3) token wasn't loaded into the script tag at render time. |
| `invalid_domain` error from `POST /v1/oauth2/token` | You passed `"domains[]": "localhost"` (or `127.0.0.1`, an IP, or an unregistered hostname). **Omit `domains[]` entirely for sandbox/local dev**; for production, list only registered origins. |
| Decoded client token has `idToken: null` | The server-side request was missing `response_type=client_token&intent=sdk_init` — you got a plain `client_credentials` access token, not a Fastlane-capable client token. **Don't conclude the merchant account is unprovisioned without first fixing the token request.** |
| `paypal.Fastlane is not a function` | `components=fastlane` missing from the script URL, or `paypal.Fastlane` called before the deferred script loaded. |
| `TypeError` on `await paypal.Fastlane()` | Argument missing — must be `paypal.Fastlane({})` even when no options. |
| Order create returns `UNPROCESSABLE_ENTITY` / `INVALID_PARAMETER_VALUE` on `payment_source` | Wrong shape — verify `payment_source.card.single_use_token` (REST) or `paymentSource.card.singleUseToken` (server SDK), not `payment_source.token.id`. |
| Fastlane component never renders, origin error in console | The browser origin isn't in the `domains[]` list passed during client-token generation. |

## Performance

PayPal reports that Fastlane-enabled checkouts see significantly higher conversion rates and faster completion times than non-accelerated guest checkout. Check [PayPal's Fastlane page](https://developer.paypal.com/studio/checkout/fastlane) for the latest performance data.

Non-US developers must use a VPN to test Fastlane in sandbox.

## Live Documentation
- [Fastlane integration guide](https://developer.paypal.com/studio/checkout/fastlane)
- [Fastlane integration steps (data-sdk-client-token, components)](https://developer.paypal.com/studio/checkout/fastlane/integrate)
- [3D Secure for Fastlane](https://developer.paypal.com/docs/checkout/fastlane/3d-secure/)
- Verified working sample (backend + frontend): [paypaldev/fastlane_paypal_video_project](https://github.com/paypaldev/fastlane_paypal_video_project)
- v5↔v6 mapping: `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-to-v6/v5-to-v6-upgrade/mappings/fastlane.json`
- v6 working snippet: `https://raw.githubusercontent.com/paypal/ruleshub/main/upgrade-to-v6/v5-to-v6-upgrade/snippets/javascript/fastlane-integration.md`
