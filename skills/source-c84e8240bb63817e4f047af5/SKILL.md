---
name: diagnose
description: Use when the user reports that a Zilliz Cloud cluster or Milvus collection is unhealthy, slow, stuck, returning errors, hitting quotas, or otherwise misbehaving — or when they ask "what's wrong with...", "why is ... slow", "diagnose ...", "troubleshoot ...".
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. For cluster diagnosis: a cluster context, or pass `--cluster-id` explicitly.
3. For collection diagnosis: the cluster context must point at the cluster that owns the collection (see setup skill).

## Scope

This skill performs **read-only diagnosis** using existing `zilliz` commands. It does NOT mutate clusters, collections, indexes, or data. Every recommendation is presented as a suggestion plus the exact next command the user can run themselves.

Two entry points:

| User says | Use section |
|---|---|
| "diagnose my cluster", "cluster is slow / stuck / unhealthy" | [Cluster Diagnosis](#cluster-diagnosis) |
| "diagnose this collection", "search is slow on X", "X won't load" | [Collection Diagnosis](#collection-diagnosis) |

When the user's intent spans both (e.g. "everything is slow"), run cluster diagnosis first — a collection-level symptom often has a cluster-level cause.

## Cluster Diagnosis

Follow this checklist in order. Stop early only if you find a P0 problem (cluster not RUNNING, quota hard-stop) — surface it before running the rest.

### 1. Collect

Run these in parallel where possible and prefer `-o json` for machine parsing:

```bash
zilliz context current
zilliz cluster describe --cluster-id <id> -o json
zilliz cluster list --all -o json                       # peer clusters for context
zilliz billing usage -o json                            # quota / spend headroom
```

Then pull time-series metrics covering the last hour and last 24h. Use the chart output for human review and `-o json` if you need to compute thresholds:

```bash
zilliz cluster metrics --cluster-id <id> \
  -m CU_COMPUTATION -m CU_CAPACITY -m CU_SIZE -m REPLICA_COUNT \
  -m STORAGE -m SLOW_QUERIES \
  -m SEARCH_QPS -m SEARCH_LATENCY_P99 \
  -m SEARCH_FAIL_RATE -m INSERT_FAIL_RATE \
  --period 1h
```

Repeat with `--period 24h` for trend context.

### 2. Analyze

Walk each rule. Each finding must cite the evidence (command + observed value).

| Check | Evidence | If true, suggest |
|---|---|---|
| Cluster status ≠ RUNNING | `cluster describe` `.status` | Pause diagnosis; explain status; if SUSPENDED suggest `cluster resume` |
| Plan vs. observed QPS mismatch (e.g. Serverless under sustained high QPS) | plan + `SEARCH_QPS` | Discuss plan upgrade tradeoff |
| `CU_COMPUTATION` p95 > 80% of `CU_CAPACITY` for sustained windows | metric series | Recommend scaling CU or adding replicas |
| `SEARCH_LATENCY_P99` rising while QPS flat | latency vs qps | Likely index/CU pressure; drill into top collections |
| Non-zero `*_FAIL_RATE` | fail-rate series | Cross-check with recent user-reported errors |
| `SLOW_QUERIES` non-zero | metric | Drill into per-collection diagnosis for the offenders |
| Storage trending toward quota | `STORAGE` + billing | Suggest cleanup / plan change before hard cap |
| Region likely far from client | endpoint + user-reported RTT | Note possible region mismatch — cannot measure RTT from CLI |

### 3. Present

Render a single report with three sections, in this order:

1. **Summary** — one-line health verdict (healthy / degraded / critical) + 1-3 sentence rationale.
2. **Findings** — table with columns `Severity | Finding | Evidence | Suggested Next Step`.
3. **Suggested commands** — copy-pasteable `zilliz ...` commands matching each suggestion. Never run mutating commands yourself — let the user run them.

## Collection Diagnosis

### 1. Collect

```bash
zilliz collection describe --name <coll> -o json
zilliz collection get-stats --name <coll> -o json
zilliz collection get-load-state --name <coll> -o json
zilliz index list --collection-name <coll> -o json
# For each vector index reported above:
zilliz index describe --collection-name <coll> --field-name <field> -o json
zilliz partition list --collection-name <coll> -o json
```

Pull per-collection metrics for the last hour and 24h:

```bash
zilliz collection metrics -c <coll> \
  -m SEARCH_QPS -m SEARCH_LATENCY_P99 -m SEARCH_FAIL_RATE \
  -m QUERY_QPS -m QUERY_LATENCY_P99 \
  -m INSERT_QPS -m INSERT_LATENCY_P99 \
  -m ENTITIES -m ENTITIES_LOADED -m ENTITIES_INDEXED \
  --period 1h
```

If the cluster context is wrong or the collection lives in a non-default database, pass `--database <db>` on every command.

### 2. Analyze

| Check | Evidence | If true, suggest |
|---|---|---|
| Load state ≠ Loaded (or partially loaded) | `get-load-state` | `collection load --name <coll>`; explain that unloaded collections cannot serve search |
| `ENTITIES_LOADED` ≪ `ENTITIES` | metrics | Load incomplete or recently grew; wait or reload |
| `ENTITIES_INDEXED` ≪ `ENTITIES` | metrics | Indexing lag; investigate before tuning |
| Vector field present but no vector index, or FLAT on large row count | `index list` + `get-stats` | Recommend HNSW / IVF_* with a parameter range appropriate for row count; mark as recommendation, not absolute |
| Index params clearly off (e.g. `nlist` ≪ √N for IVF) | `index describe` + row count | Suggest revised values; note that benchmarking is needed for the final number |
| Replica count = 1 with sustained high QPS | `collection describe` replicas + `SEARCH_QPS` | Suggest more replicas, conditioned on CU headroom from cluster diagnosis |
| Schema reasons: very wide varchar, many un-indexed scalar fields used in filters | `collection describe` schema | Note impact; suggest scalar indexes where applicable |
| No partition key but row count is large and queries are naturally partitionable | schema | Mention partition-key option (cannot be added in place — design-time decision) |
| Non-zero `SEARCH_FAIL_RATE` | metric | Cross-check with cluster-level fail-rate metrics |
| Latency rising while QPS flat | latency vs qps | Index pressure or growing segment count; consider compaction; note that segment-level state is not exposed via CLI |

### 3. Present

Same three-section format as cluster diagnosis. When a collection finding's true root cause is at the cluster level (e.g. CU saturation), say so explicitly and reference the cluster report.

## Guidance

- **Read-only.** Never run `delete`, `drop`, `release`, `resume`, `suspend`, `create`, `update`, index create/drop, or any mutating data-plane command as part of diagnosis. Present them as suggestions only.
- **Cite evidence.** Every finding must reference the command that produced it and the observed value. No unsourced claims.
- **Mark uncertainty.** Index parameter recommendations, replica counts, and CU sizing depend on workload specifics the CLI cannot observe. Phrase as "starting point, benchmark to confirm."
- **Know the limits.** The CLI cannot see per-query plans, segment-level state, compaction backlog, GC, server-internal queues, or alert-rule state. If a question requires those, say so plainly rather than guessing.
- **Prefer parallel collection.** When multiple read-only commands are independent, run them in parallel to keep the diagnosis fast.
- **JSON for parsing, charts for humans.** Use `-o json` (optionally with `--query`) when comparing values against thresholds; use the default chart output when surfacing trends back to the user.
- **Honor context.** If the user has multiple clusters, confirm which one before collecting. If the collection is in a non-default database, thread `--database` through every command.
