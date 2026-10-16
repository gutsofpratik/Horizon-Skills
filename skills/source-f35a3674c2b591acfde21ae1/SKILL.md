---
name: status
description: Use when the user wants a comprehensive overview of their current Zilliz Cloud environment — context, cluster details, databases, and collections with stats.
---

Gather and display a status overview of the user's current Zilliz Cloud environment. Run commands with `--output json` for structured data, then present a formatted summary.

## Step 1: Check Prerequisites

Verify CLI is installed and user is logged in:

```bash
zilliz auth status
```

If not set up, use the quickstart skill first.

## Step 2: Show Current Context

```bash
zilliz context current --output json
```

If no context is set, suggest running `zilliz context set --cluster-id <id>`.

## Step 3: Cluster Details

Using the cluster ID from context:

```bash
zilliz cluster describe --cluster-id <cluster-id> --output json
```

Present: cluster name, status, plan, region.

## Step 4: Database List

```bash
zilliz database list --output json
```

## Step 5: Collections Summary

For each database returned in Step 4, gather collection information:

```bash
zilliz collection list --database <db-name> --output json
```

For each collection, gather stats and index info:

```bash
zilliz collection get-stats --name <name> --database <db-name> --output json
zilliz collection get-load-state --name <name> --database <db-name> --output json
zilliz index list --collection <name> --database <db-name> --output json
```

## Step 6: Present Summary

Format the results as a readable summary:

**Cluster:** <name> (<cluster-id>)
**Status:** RUNNING | **Region:** <region> | **Plan:** <plan>

For each database, show its collections:

**Database:** <db-name>

| Collection | Rows | Load State | Indexes |
|---|---|---|---|
| my_collection | 10,000 | Loaded | vector_idx (AUTOINDEX) |
| ... | ... | ... | ... |

If the cluster is suspended, show a warning that data operations are unavailable.
