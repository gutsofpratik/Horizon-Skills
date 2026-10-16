# Routing

Every public hostname and what serves it. Two worlds: Vercel serves the storefront
hostnames, and the `atlas-prod` ALB serves everything else. We deliberately run no CDN
or gateway layer of our own — Vercel and the ALB are the front doors.

| Hostname | Serves | TLS |
|---|---|---|
| `fieldkit.com` | Storefront (Vercel) — marketing pages | Vercel-managed |
| `checkout.fieldkit.com` | Storefront (Vercel) — checkout flow | Vercel-managed |
| `app.fieldkit.com` | Atlas `web` (the product) via the `atlas-prod` ALB | ACM cert on the ALB |
| `api.fieldkit.com` | Atlas `web` (the public API) via the same ALB | ACM cert on the ALB |

A hostname answering that isn't listed here means this doc has drifted — flag it. DNS
for all four is Route 53 in `fieldkit-prod`; the ALB and listener rules are Terraform in
`fieldkit/infra/alb/`.

## One request, walked

A login at `app.fieldkit.com`: Route 53 resolves to the `atlas-prod` ALB; the ALB
terminates TLS (ACM) and forwards to the `atlas-prod-web` target group; an ECS `web`
task's Django app handles it, reading the session from Redis and the user row through
PgBouncer into `atlas-prod-db`. Every hop after the ALB is visible in Datadog APM under
the `atlas-web` service ([observability](./atlas/observability.md)). API traffic differs
only in the listener rule: `api.fieldkit.com` matches a separate rule on the same ALB
but lands on the same `web` tasks.

## Deliberately unauthenticated

Paths that answer without a session or API key, on purpose:

- `api.fieldkit.com/healthz` — the ALB health check.
- `api.fieldkit.com/webhooks/stripe` — Stripe events; authenticated by signature
  verification in the handler, not by a session.
- Everything on `fieldkit.com` — public marketing pages.

Anything else answering unauthenticated is a finding: either this list has drifted or
something is misconfigured — check which before assuming either.
