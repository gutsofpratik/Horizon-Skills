---
name: on-demand-cluster
description: Use when the user wants to create, list, describe, or delete an on-demand (Vector Lake / VectorLake) cluster. On-demand clusters auto-suspend after an idle TTL and are intended for ad-hoc query workloads against a Vector Lake.
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. A Vector Lake instance in the target project/region (see cluster
   skill -- `cluster create-vectorlake`).

## Commands Reference

### Create an On-Demand Cluster

`create` is hand-written and not generated from the JSON model. It calls
`POST /v2/clusters/createOnDemandCluster` and accepts:

```bash
zilliz on-demand-cluster create \
  --project-id <project-id> \
  --region-id <region-id> \
  --cu-size <integer>            # required, >= 8
  --cluster-name <string> \      # required, max 64 chars, letters/digits/space/_/-/CJK
  [--session-ttl <duration>] \   # auto-suspend TTL: 30m, 1h, 90s (min 60s, default 60s)
  [--max-query-node-cu <n>] \
  [--max-query-node-replicas <n>]
```

Session TTL controls how long an idle on-demand cluster stays running before
it is automatically suspended. Format is `<number><s|m|h>`, with a floor of
60 seconds. Resuming a suspended on-demand cluster happens transparently on
the next query.

Examples:

```bash
# Create an 8-CU on-demand cluster with the default 60s idle TTL
zilliz on-demand-cluster create \
  --project-id proj-xxxx \
  --region-id aws-us-east-1 \
  --cu-size 8 \
  --cluster-name "qc-prod-1"

# Keep alive 30 minutes between queries, cap query node CU and replicas
zilliz on-demand-cluster create \
  --project-id proj-xxxx \
  --region-id aws-us-east-1 \
  --cu-size 16 \
  --cluster-name "qc-batch-1" \
  --session-ttl 30m \
  --max-query-node-cu 16 \
  --max-query-node-replicas 4
```

### List On Demand Clusters

```bash
zilliz on-demand-cluster list --project-id <project-id> --region-id <cloud-region>
```

### Describe an On Demand Cluster

```bash
zilliz on-demand-cluster describe --cluster-id <on-demand-cluster-id>
```

### Delete an On Demand Cluster

```bash
zilliz on-demand-cluster delete --cluster-id <on-demand-cluster-id-to-delete>
```

## Guidance

- On-demand clusters belong to a Vector Lake instance and only exist inside a `<projectId>` + `<regionId>` pair. If neither `list` nor `describe` returns anything, first confirm that the project has a Vector Lake (`zilliz cluster create-vectorlake`).
- `list` requires both `--project-id` and `--region-id` -- there is no all-projects listing.
- Status flows through `CREATING` -> `RUNNING` -> `SUSPENDING` -> `SUSPENDED` and back to `RESUMING` -> `RUNNING` on the next query. Treat `SUSPENDING`/`SUSPENDED` as healthy idle state, not an error.
- `--session-ttl` is the idle auto-suspend timer. The minimum is `60s`; values smaller than that are rejected client-side before the API call. The current default is `60s`, so on-demand clusters are aggressive about suspending -- raise it (e.g. `30m`) when running interactive workloads.
- `--cu-size` must be >= 8 and `--cluster-name` is at most 64 characters, allowing letters, digits, space, `_`, `-`, and Chinese characters.
- `delete` is irreversible and asynchronous -- always confirm with the user before invoking. The cluster row moves to `DELETING` and disappears once cleanup finishes.
- These commands are distinct from the regular `cluster` skill: a regular cluster owns its own compute, while on-demand clusters share storage with their parent Vector Lake. Do not confuse `zilliz on-demand-cluster delete` with `zilliz cluster delete`.
