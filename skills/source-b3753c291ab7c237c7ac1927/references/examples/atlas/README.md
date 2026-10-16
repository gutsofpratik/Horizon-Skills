# Atlas

The product backend: a single Django codebase in `fieldkit/atlas`, deployed as three ECS
services — `web` (API and server-rendered app), `worker` (Celery consumers), and `beat`
(the scheduler, always exactly one task). The boundary: atlas is everything that deploys
from the `atlas` repo; the storefront calls atlas's public API but is its own system,
and the data warehouse consumes atlas's events but is not atlas.

Key identifiers, verbatim:

| Thing | Name |
|---|---|
| ECS clusters | `atlas-prod`, `atlas-staging` |
| Postgres | RDS `atlas-prod-db` (+ replica) and `atlas-prod-timeseries` ([database](./database.md)) |
| Cache | ElastiCache Redis `atlas-prod-cache` |
| Queues | SQS, `atlas-prod-*` per queue family ([events](./events.md)) |
| Object storage | S3 `fieldkit-prod-exports`, `fieldkit-prod-uploads` |
| Public hostnames | `app.fieldkit.com`, `api.fieldkit.com` (both land on `web`) |

Scaling shape: `web` autoscales on ALB request count, `worker` autoscales on queue
depth, `beat` never scales. Desired counts and limits live in
`fieldkit/infra/ecs/atlas.tf` — read them there, not here.

## Concerns

| Concern | File |
|---|---|
| How a merge reaches production, rollback, hotfixes | [deployment.md](./deployment.md) |
| Postgres: instances, pooling, replicas, migrations | [database.md](./database.md) |
| Async work: queues, retries, backlogs, deploy effects | [events.md](./events.md) |
| How atlas ships its signals, correlation keys, dashboards | [observability.md](./observability.md) |

Caching hasn't earned its own file: Redis holds sessions, rate-limit counters, and the
feature-flag snapshot, refreshed every 30s from the flags service (the interval lives in
`atlas/core/cache.py` — trust it over this number). Stale flags after a flags outage is
the known trap, owned by the runbook "Feature flag snapshot staleness".
All access goes through `atlas/core/cache.py`, which enforces the `atlas:<domain>:` key
convention and default TTLs — code talking to Redis directly is a bug, and an
unrecognized key prefix means exactly that. Losing Redis logs everyone out and briefly
removes rate limiting; nothing durable lives there.
