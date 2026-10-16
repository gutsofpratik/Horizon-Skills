# Architecture

*A worked example for an invented company (Fieldkit), showing the calibrated depth these
docs aim for — see [concerns.md](../concerns.md). Everything below is fictional.*

How we build, deploy, and run our software. These docs describe what each system *is* —
where it runs, what it depends on, and the real names of things — so that a responder or
an agent working an incident can ground themselves before reaching for a fix. Runbooks
own *procedures* (how to diagnose and fix); these docs own *facts*.

## The estate

The directory reflects how people reason about things when they break, not how the code
is organized: atlas and the storefront share nothing but an API, the storefront is
deliberately not on our AWS estate, and observability is an estate service — a family
of tools, not a deployment.

| Entry | What it is |
|---|---|
| [atlas](./atlas/README.md) | The product backend: a Django monolith run as web and worker services on ECS. Almost everything Fieldkit does happens here. |
| [storefront](./storefront/README.md) | The marketing site and checkout at fieldkit.com. A Next.js app on Vercel — deliberately not on our infrastructure, so marketing stays up when atlas is down. |
| [observability](./observability/README.md) | Where our signals go: Datadog for logs, metrics, and traces, Sentry for errors. An estate service — the tools every system reports into, not a deployment of ours. |

## The views

- [Environments](./environments.md) — the production/staging model, the AWS account
  directory, and where authoritative infrastructure config lives.
- [Routing](./routing.md) — every public hostname and what serves it, one request walked
  end-to-end, and the deliberately unauthenticated paths.

## Where do I look?

| You want to know | Open |
|---|---|
| What AWS accounts exist and what each is for | [Environments](./environments.md) |
| How a merged PR reaches production, or how to roll back | [Atlas deployment](./atlas/deployment.md) |
| How Postgres is set up: instances, poolers, migrations | [Atlas database](./atlas/database.md) |
| How async work moves: queues, retries, backlogs | [Atlas events](./atlas/events.md) |
| What's behind a URL, or whether a path should be public | [Routing](./routing.md) |
| Which observability tool answers which question, and where alert rules live | [Observability](./observability/README.md) |
| How atlas ships its signals, and the correlation keys to pivot on | [Atlas observability](./atlas/observability.md) |
| What Redis holds and what breaks without it | [Atlas](./atlas/README.md) |
| Why marketing stays up when the product is down | [Storefront](./storefront/README.md) |
