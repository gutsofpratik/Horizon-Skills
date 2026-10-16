---
name: import
description: Use when the user wants to import bulk data into a Milvus collection via Zilliz Cloud import jobs, or manage import stages (pre-uploaded file holders that import jobs reference).
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. Target collection must exist on the target cluster.

## Commands Reference

### Import Jobs

#### Start an Import Job

```bash
zilliz import start --collection <target-collection-name>
# Optional:
#   --cluster-id <target-cluster-id>
#   --project-id <project-id>
#   --region-id <region-id>
# Or use raw JSON: --body '{"files": [["s3://bucket/path/data.parquet"]]}'
```

#### List Imports

```bash
zilliz import list
# Optional:
#   --cluster-id <cluster-id>
#   --project-id <project-id>
#   --region-id <region-id>
#   --database <database-name>
```

#### Check Import Status

```bash
zilliz import status --job-id <import-job-id>
# Optional:
#   --cluster-id <cluster-id>
#   --project-id <project-id>
#   --region-id <region-id>
```

### Import Stages

#### List Stages

```bash
zilliz stage list
# Optional: --project-id <filter-by-project-id>
# Pagination: --page-size <n> --page <n>
# Fetch all pages: --all
```

#### Create a Stage

```bash
zilliz stage create \
  --project-id <owning-project-id> \
  --region-id <cloud-region> \
  --stage-name <stage-name>
```

#### Delete a Stage

```bash
zilliz stage delete --stage-name <stage-name>
```

#### Apply

```bash
zilliz stage apply --stage-name <stage-name>
# Optional:
#   --project-id <project-id>
#   --region-id <region-id>
#   --cluster-id <target-cluster-id>
#   --path <stage-subpath>
```

## Integration Setup

Import requires a cloud storage integration to access data files. The `integration-id` is configured in the Zilliz Cloud console under **Project Settings > Integrations**. Ensure the integration has read access to the source bucket and path.

Supported file formats: Parquet, JSON, CSV.

## Stages vs. Direct Integrations

A **stage** is a named, project-scoped handle to a pre-uploaded set of files in
managed cloud storage. Import jobs reference either:

- a customer-owned bucket via an integration (the original flow above), or
- a stage (`zilliz stage create --project-id <id> --region-id <region> --stage-name <name>`), which is preferable when the user wants Zilliz Cloud to host the staging bucket.

`stage apply` updates an existing stage in place; `stage delete` removes it
(confirm with the user first -- pending import jobs referencing the stage
will fail).

## Import Targets

`import start`, `import list`, and `import status` accept either:

- `--cluster-id <id>` (legacy form, still supported), or
- `--project-id <id>` together with `--region-id <region>` (the server then
  resolves the target instance from the project + region pair).

You must supply exactly one of those two grouping forms -- the CLI rejects
an import command that provides neither, or that provides `--project-id`
without `--region-id`.

## Guidance

- Import jobs run asynchronously. After starting a job, use `import status` to track progress.
- The data files must be accessible from Zilliz Cloud (either via a configured integration or via a stage).
- The collection schema must match the data file structure.
- When importing into a Vector Lake / on-demand-cluster setup, prefer the `--project-id` + `--region-id` form -- on-demand clusters do not have a stable single cluster ID to point at.
