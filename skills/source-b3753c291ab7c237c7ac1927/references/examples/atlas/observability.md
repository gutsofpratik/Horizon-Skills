# Atlas observability

How atlas ships its signals and how to pivot between them. The tools themselves —
accounts, Sentry projects, and where monitors are defined — are the estate service's:
[observability](../observability/README.md).

Everything lands in Datadog: logs ship via the ECS FireLens sidecar, metrics via
DogStatsD from the app, traces via `dd-trace` auto-instrumentation under the service
names `atlas-web` and `atlas-worker`. Errors additionally go to Sentry, project `atlas`.

## Correlation keys

The fields that join signals together — what you pivot on:

| Field | Logs | Traces | Metrics | Deploy events |
|---|---|---|---|---|
| `request_id` | yes | yes (as a span tag) | — | — |
| `trace_id` | yes | yes | — | — |
| `git_sha` | yes | yes | — | yes |
| `env` | yes | yes | yes (tag) | yes |
| `account_id` (the tenant) | yes | yes | never — unbounded cardinality | — |

The one to remember: `account_id` is never a metric tag, so "is this one customer or
everyone?" is a logs question, not a metrics question.

## Dashboards

The dashboards that matter, by name:

- `atlas-overview` — request rates, error rates, and latency for `web` (each Datadog
  account carries its own copy).
- `atlas-queues` — depth and age-of-oldest per queue ([events](./events.md)).

Runbooks name these two rather than re-explaining them; a diagnostic that needs more
than these starts from the monitor that fired ([alert rules](../observability/README.md)).
