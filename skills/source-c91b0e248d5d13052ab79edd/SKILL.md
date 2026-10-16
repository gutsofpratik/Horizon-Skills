---
name: collection
description: Use when the user wants to create, list, describe, drop, rename, load, release, or manage collections and collection aliases in Milvus.
---

## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).

## Commands Reference

All collection commands accept an optional `--database <db-name>` flag to target a non-default database. If omitted, the database from the current context is used.

## Collection metrics

Query per-collection metrics against `POST /v2/clusters/{clusterId}/metrics/query` with `collectionName` set in the request body. Mirrors the web console's Collection Detail > Metrics page.

```bash
zilliz collection metrics --collection-name <collection-name> --metric <metric-name>
# Optional:
#   --cluster-id <cluster-id>         Override cluster context
#   --period <duration>               e.g. 1h, 24h, 7d (mutually exclusive with --start/--end)
#   --start <iso-8601> --end <iso-8601>
#   --granularity <duration> / -g     e.g. 30s, 5m, 1h (auto-selected if omitted)
#   -o table                          Render pivot table instead of the default inline chart
```

The default output is an inline text chart: one block per metric with a summary line (`min / max / avg / last`) and a Braille-rendered line chart. Pass an explicit `-o table` (or `--output table`) to render the pivot-table layout — useful for terminals without good Braille font support. `-o json`, `-o yaml`, `-o csv`, and `--query` always bypass both renderers and return the raw response.

Examples:

```bash
# Period shorthand: last hour of SEARCH_QPS for a collection
zilliz collection metrics -c my_coll -m SEARCH_QPS --period 1h

# Explicit range with 1h granularity
zilliz collection metrics -c my_coll -m ENTITIES_LOADED \
  --start 2026-04-13T00:00:00Z --end 2026-04-14T00:00:00Z -g 1h

# Multiple metrics in a single call
zilliz collection metrics -c my_coll -m SEARCH_QPS -m SEARCH_LATENCY_P99 --period 6h
```

### Metric scope

Each metric is tagged with a scope. `zilliz collection metrics` only accepts metrics whose scope is `Collection` or `Both`. Using a Cluster-only metric emits:

```
Metric '<NAME>' is cluster-scope only and cannot be used with --collection-name.
```

| Scope | Metrics |
|-------|---------|
| Cluster only (rejected here) | `CU_COMPUTATION`, `CU_CAPACITY`, `CU_SIZE`, `REPLICA_COUNT`, `STORAGE`, `COLLECTIONS`, `SLOW_QUERIES`, `READ_VCU`, `WRITE_VCU` |
| Collection / Both (allowed) | `SEARCH_QPS`, `QUERY_QPS`, `INSERT_QPS`, `UPSERT_QPS`, `DELETE_QPS`, `BULK_INSERT_QPS`, `SEARCH_LATENCY_AVG/P99`, `QUERY_LATENCY_AVG/P99`, `INSERT_LATENCY_AVG/P99`, `UPSERT_LATENCY_AVG/P99`, `DELETE_LATENCY_AVG/P99`, VPS counters, failure-rate counters, `ENTITIES`, `ENTITIES_LOADED`, `ENTITIES_INDEXED`, plus the hybrid-search aliases below |

### Hybrid-search aliases

| CLI name | Backend name |
|----------|--------------|
| `HYBRID_SEARCH_QPS` | `REQ_HYBRID_SEARCH_COUNT` |
| `HYBRID_SEARCH_LATENCY_AVG` | `REQ_HYBRID_SEARCH_LATENCY_AVG` |
| `HYBRID_SEARCH_LATENCY_P99` | `REQ_HYBRID_SEARCH_LATENCY_P99` |
| `HYBRID_SEARCH_FAIL_RATE` | `REQ_FAIL_RATE_HYBRID_SEARCH` |

For cluster-wide metrics (CU sizing, storage, serverless VCU, slow queries) use `zilliz cluster metrics` instead -- see the monitoring skill.

### Create a Collection

```bash
zilliz collection create --name <collection-name> --dimension <vector-dimension>
# Optional:
#   --metric-type <COSINE|L2|IP>
#   --id-type <Int64|VarChar>
#   --auto-id <true|false>
#   --primary-field <primary-key-field-name>
#   --vector-field <vector-field-name>
#   --database <database-name>
# Or use raw JSON: --body '{"schema": {"fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": "768"}}]}}'
```

### List Collections

```bash
zilliz collection list
# Optional: --database <database-name>
```

### Describe a Collection

```bash
zilliz collection describe --name <collection-name>
# Optional: --database <database-name>
```

### Drop a Collection

```bash
zilliz collection drop --name <collection-name-to-drop>
# Optional: --database <database-name>
```

### Rename a Collection

```bash
zilliz collection rename --name <current-collection-name> --new-name <new-collection-name>
# Optional: --database <current-database-name>, --new-database <target-database-name>
```

### Load a Collection

```bash
zilliz collection load --name <collection-name>
# Optional: --database <database-name>
```

### Release a Collection

```bash
zilliz collection release --name <collection-name>
# Optional: --database <database-name>
```

### Get Load State

```bash
zilliz collection get-load-state --name <collection-name>
# Optional: --database <database-name>
```

### Get Statistics

```bash
zilliz collection get-stats --name <collection-name>
# Optional: --database <database-name>
```

### Check if a Collection Exists

```bash
zilliz collection has --name <collection-name>
# Optional: --database <database-name>
```

### Flush a Collection

```bash
zilliz collection flush --name <collection-name>
# Optional: --database <database-name>
```

### Compact a Collection

```bash
zilliz collection compact --name <collection-name>
# Optional: --database <database-name>
```

### Collection Aliases

#### Create an Alias

```bash
zilliz alias create --collection <target-collection-name> --alias <alias-name>
# Optional: --database <database-name>
```

#### List Aliases

```bash
zilliz alias list --database <database-name>
# Optional: --collection <filter-by-collection-name>
```

#### Describe an Alias

```bash
zilliz alias describe --alias <alias-name>
# Optional: --database <database-name>
```

#### Alter an Alias

```bash
zilliz alias alter --collection <new-target-collection> --alias <alias-name-to-reassign>
# Optional: --database <database-name>
```

#### Drop an Alias

```bash
zilliz alias drop --alias <alias-name-to-drop>
# Optional: --database <database-name>
```

## Guidance

- When the user wants to create a collection, ask about their use case to recommend appropriate dimension, metric type, and schema.
- Before dropping a collection, always confirm with the user -- this deletes all data.
- A collection must be loaded before it can be searched or queried.
- After creating a collection, suggest loading it if the user plans to query immediately.
- Use `describe` to inspect schema before performing vector operations.
