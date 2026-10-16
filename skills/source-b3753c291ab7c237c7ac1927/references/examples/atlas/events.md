# Atlas events

How asynchronous work moves: Celery over SQS. Producers enqueue from web requests and
from `beat` schedules; `worker` consumes. Every task is declared through the decorator
in `atlas/tasks/registry.py`, which assigns its queue and retry policy — so "which queue
does this task use, and how often does it retry" is always a one-file lookup, and a task
defined outside the registry is a bug. Delivery is at-least-once and handlers are
expected to be idempotent — duplicate side effects from a redelivered task are a handler
bug, not an infrastructure mystery.

Queue families, verbatim (all prefixed `atlas-prod-`; a queue outside these families is
a finding):

| Queue | Carries | Sensitivity |
|---|---|---|
| `atlas-prod-default` | Most application tasks | Backlog degrades features quietly |
| `atlas-prod-notify` | Email, SMS, push | Backlog is customer-visible fast |
| `atlas-prod-export` | Report and data exports | Slow by design; big messages |

Each queue has a DLQ (`-dlq` suffix, 14-day retention) and messages land there after
five failed receives — the redrive policy in `fieldkit/infra/sqs/atlas.tf` owns both
numbers. A non-empty DLQ is always worth explaining, and draining one is owned by the
runbook "Draining an SQS dead-letter queue".

## How backlogs surface

`worker` autoscales on queue depth, so a backlog first shows as scaling to max rather
than as customer impact. Depth and age-of-oldest per queue are on the Datadog dashboard
`atlas-queues`; age is the honest signal (depth alone hides one stuck message). Backlog
triage is owned by the runbook "SQS queue backlog".

## Deploy effects

ECS drains workers on deploy: in-flight tasks get 30 seconds before SIGKILL (the stop
timeout in `fieldkit/infra/ecs/atlas.tf`), so tasks longer than that re-deliver after
every deploy — the visible symptom is a small DLQ
blip and duplicate-task warnings just after rollouts. Long tasks are supposed to
checkpoint; the list of known offenders lives in the atlas repo's
`docs/long-tasks.md`.
