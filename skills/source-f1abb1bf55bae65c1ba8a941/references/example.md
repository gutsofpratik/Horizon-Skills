# Worked example

One complete skill for an invented company, at the depth a real one deserves. Acme
runs an order-fulfillment pipeline; this is the utility skill their on-call agents
load for any question about it. The margin notes in brackets name the pattern each
part carries — don't copy those.

---

````markdown
---
name: fulfillment
description: >
  Inspect and unstick Acme's order-fulfillment pipeline. Use whenever you're working
  with fulfillment in any way — delayed orders, the fulfillment-lag alert, "stuck in
  fulfillment" reports, requeueing or dropping a batch. Not for payment failures —
  payments fail before this pipeline sees them.
metadata:
  incident-io-plugin-version: "0.19.0"
---

# Order fulfillment

Every accepted order is written to the pipeline in exactly one of two regional
queues, split by warehouse. The consequence that shapes everything below: a
merchant's backlog lives in **whichever region their warehouse is in**, and a
count from the wrong region reads as "no backlog" while orders sit stuck.
[model with consequence]

This skill covers operating the pipeline. Why it's regional, the reconciliation
job, and the merchant-notification flow are owned by the architecture doc
`architecture/fulfillment.md`; the recovery procedure for a dead region is the
"Region failover" runbook. Read those there — ask the architecture and runbooks
skills.                                              [scope with owners]

## Vocabulary

- A **batch** is the pipeline's unit: orders for one warehouse, up to a
  per-warehouse cap the pipeline config owns.
- The tools say `station`; the dashboard says "warehouse". Same thing — station
  IDs are the dashboard name lowercased with `wh-` prefixed (`wh-leeds`). Each
  station belongs to one region; `pipeline_show` lists each region's stations.
- `state: parked` is not an error: reconciliation parks batches it will retry.
                                                     [vocabulary + traps]

## Where things are

| Need | Where |
|---|---|
| What's queued, per region | the Fulfillment Ops connection's `pipeline_show` |
| One batch's history | `batch_show`, by batch ID |
| Requeue or drop a batch | `batch_requeue` / `batch_drop` — write tools, gated below |
| Lag over time | the **production metrics** datasource (Prometheus), below |
| Why a batch parked | [parked states](references/parked-states.md) |
                                    [need-keyed table; connection named once]

## Reading results

- **`orders_pending: null` means the region didn't answer, never zero.** Each
  region reports independently; when `regions[].error` is set, report that
  region unreadable — never as healthy or empty.
- **`found: false` is confirmed absence** — normal for a batch already shipped.
  `found: null` means the lookup failed, which is evidence of nothing. A batch
  neither lookup finds is reported as not found, and you stop — never invent a
  batch ID.                        [null/absent/zero semantics; abstention]

## Common flows

**"Merchant says orders are stuck"** — get their warehouse from the order, map it
to the station (vocabulary above), find the station's region in `pipeline_show`,
and work in that region only. Healthy pipelines hold under a minute of work;
anything older than the region's `sla_seconds` is the finding. Quote the batch
IDs you read.

**"Is fulfillment lagging?"** — lag history lives on the **production metrics**
datasource:

```promql
# Datasource: production metrics
max by (region) (fulfillment_oldest_order_age_seconds)
```

Falling means it's draining; don't act on a single sample. Where the session has no
metrics surface, say lag history is unchecked and judge from `pipeline_show`'s order
ages alone.                    [pinned query, datasource annotation,
                                              conditional capability]

## Output

End every answer with, whatever else it says:      [output contract]

- **State:** draining | stuck | region unreadable | batch not found
- **Evidence:** the batch IDs and ages you read — or what you couldn't read
- **Next action:** one line

All three survive skipped steps: an unreadable region is Evidence, not silence. The
block goes in the reply itself — never only in a file the asker can't open.

## Dropping a batch

`batch_drop` abandons every order in the batch: **merchants are not notified and
the orders never ship.** Before it, in order:            [gates before the act]

1. **Will it drain by itself?** Watch the lag metric for two samples first.
2. **What exactly is lost?** `batch_show` the batch; if it shows refunds in
   progress, stop and hand the drop to a human (that was Acme's INC-1204).
3. **Requeue beats drop** whenever the failure was transient: `batch_requeue`
   loses nothing and is idempotent.

Both write tools take `dry_run: true` — always run it first and read `warnings`.

## What this skill doesn't do

- **Pause a region without dropping anything** — that's the pipeline's own
  throttle, in the dashboard's fulfillment settings.
- **Cross-region order search** — the **order history** datasource (Acme's data
  warehouse) holds every order; ask it, don't page through regions.
                                   [negative space, with routes; the off-ramp rule]
````

---

What to notice, beyond the bracketed notes: the description leads with the subject
stated broadly, keeps only the signals nothing else matches, and carries one negative
trigger; the
connection is named once and every later mention is a bare tool; the two datasources
are named in bold with their types and the pinned query carries its annotation; the
batch cap names its owner instead of a number; the one incident reference does a
gate's worth of persuading in a parenthesis; and the output contract survives every
way a run can fall short. At about ninety lines it's near the small end — a system
with more failure shapes earns more — but nothing here is padding, and that's the
calibration to copy.
