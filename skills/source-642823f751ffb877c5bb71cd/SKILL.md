---
name: cluster
description: Use when the user wants to create, list, describe, delete, suspend, resume, or modify Zilliz Cloud clusters.
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. No cluster context required -- these are control-plane operations.

## Commands Reference

### Create a Cluster

```bash
# Serverless cluster
zilliz cluster create \
  --name <cluster-name> \
  --type serverless \
  --project-id <project-id> \
  --region <region-id>

# Free-tier cluster
zilliz cluster create \
  --name <cluster-name> \
  --type free \
  --project-id <project-id> \
  --region <region-id>

# Dedicated cluster
zilliz cluster create \
  --name <cluster-name> \
  --type dedicated \
  --project-id <project-id> \
  --region <region-id> \
  --cu-type <Performance-optimized|Capacity-optimized> \
  --cu-size <cu-size>
```

To find available project IDs, cloud providers, and regions:

```bash
zilliz project list
zilliz cluster providers
zilliz cluster regions --cloud-id <aws|gcp|azure>
```

### Create a Vector Lake instance

A Vector Lake (sometimes called a "VectorLake" cluster) is the storage layer
that on-demand clusters attach to (see the `on-demand-cluster` skill). It is
created via a hand-written subcommand calling
`POST /v2/clusters/createVectorLake`:

```bash
zilliz cluster create-vectorlake \
  --project-id <project-id> \
  --region-id <region-id> \
  [--session-ttl <duration>] \      # idle auto-suspend TTL, min 60s
  [--max-query-node-cu <integer>] \
  [--max-query-node-replicas <integer>]
```

After the Vector Lake is `RUNNING`, attach a query workload with
`zilliz on-demand-cluster create --project-id <id> --region-id <region> --cu-size <n> --cluster-name <name>`.

### List Clusters

```bash
zilliz cluster list
# Optional: --region-id <filter-by-region-id>
# Pagination: --page-size <n> --page <n>
# Fetch all pages: --all
```

### Describe a Cluster

```bash
zilliz cluster describe --cluster-id <cluster-id>
```

### Modify a Cluster

```bash
zilliz cluster modify --cluster-id <cluster-id-to-modify>
# Optional: --cu-size <number-of-compute-units>, --replica <number-of-replicas>
# Or use raw JSON: --body '{"cuSize": 2, "replica": 2}'
```

### Suspend a Cluster

```bash
zilliz cluster suspend --cluster-id <cluster-id-to-suspend>
```

### Resume a Cluster

```bash
zilliz cluster resume --cluster-id <cluster-id-to-resume>
```

### Delete a Cluster

```bash
zilliz cluster delete --cluster-id <cluster-id-to-delete>
```

### List Cloud Providers

```bash
zilliz cluster providers
```

### List Regions

```bash
zilliz cluster regions
# Optional: --cloud-id <aws|gcp|azure>
```

## Guidance

- Before creating a cluster, help the user choose a region by running `zilliz cluster providers` and `zilliz cluster regions`.
- Cluster creation is **asynchronous**. After `cluster create`, the cluster status will be `CREATING`. Poll with `zilliz cluster describe --cluster-id <id>` until the status becomes `RUNNING` before proceeding with data-plane operations.
- Before deleting a cluster, always confirm with the user -- this is irreversible.
- After creating a cluster, suggest setting it as the active context with `zilliz context set --cluster-id <id>`.
- When a cluster is suspended, remind the user it must be resumed before data-plane operations.
- Different cluster types have different capabilities. See the "Cluster Type Differences" table in the setup skill for details.
- `cluster create-vectorlake` creates a Vector Lake storage instance, not a regular cluster. Query workloads against it run on on-demand clusters (see the `on-demand-cluster` skill). Do not pass `--type` to this subcommand; it has its own dedicated parameter set.
- `cluster list` supports a `--region-id <region>` filter for scoping to a single region.
