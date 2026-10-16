# Storefront

The marketing site and checkout at `fieldkit.com` and `checkout.fieldkit.com`: a Next.js
app in `fieldkit/storefront`, deployed on Vercel — deliberately not on our AWS estate,
so a full atlas outage leaves marketing up (checkout pages render, but session creation
needs atlas). The boundary: everything Vercel serves is storefront; the moment a request
hits `api.fieldkit.com`, it's [atlas](../atlas/README.md).

- **Deploys**: Vercel from the `main` branch, previews per PR. No staging account —
  previews are staging. Rollback is Vercel's instant rollback to a previous deployment
  (a console lever).
- **Data**: none of its own. Checkout is Stripe Checkout sessions created via atlas's
  public API; content is MDX in the repo. If checkout fails while pages render fine,
  look at atlas or Stripe, not here.
- **Runtime dependencies, in order of blast radius**: atlas's public API (checkout,
  signup), Stripe, Vercel itself. Cached marketing pages survive all three; the runbook
  "Checkout failures" owns the triage order.
- **Observability**: Vercel's own logs plus Sentry project `storefront`. There is no
  Datadog here — a gap we accept, noted so nobody hunts for dashboards that don't
  exist.
