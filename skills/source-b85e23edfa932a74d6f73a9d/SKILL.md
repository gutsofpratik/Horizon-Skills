---
name: external-collection
description: Use when the user wants to trigger, describe, or list refresh jobs for an external collection (a collection backed by an external data source such as Vector Lake). Note this is the data-plane refresh workflow, not collection CRUD -- for create/drop/load see the collection skill.
---

## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).
2. The target collection must already exist as an **external collection**
   (created with an `externalSource` / `externalSpec` schema in the
   collection skill). Plain in-place collections do not have refresh jobs.
3. The cluster must be running a `kite-coordinator` build that exposes
   `/v2/vectordb/jobs/external_collection/*` (PR #5735 or later). On older
   data planes the API returns 404 -- in that case ask the user to upgrade
   the cluster.

## Commands Reference

The `external-collection` resource has a single operation, `refresh`, with
three actions: `trigger`, `describe`, and `list`. All three are data-plane
calls and inherit the database from the current context unless overridden
with `--database`.

### Trigger a refresh job

```bash
zilliz external-collection refresh trigger --name <collection-name>
# Optional:
#   --database <db-name>          Override the context database
#   --external-source <src>       Override the external source registered on the collection
#   --external-spec <spec>        Override the external spec registered on the collection
```

`trigger` returns the new `jobId`. Use it with `refresh describe` to poll
status. The override flags are intentionally rare -- normally the source
and spec are pinned at collection-create time, and a plain
`refresh trigger --name <name>` is enough.

### Describe a refresh job

```bash
zilliz external-collection refresh describe --job-id <id>
```

Returns the job's state, progress, and (on failure) the error message.

### List refresh jobs

```bash
zilliz external-collection refresh list
# Optional:
#   --name <collection-name>      Filter to one external collection
#   --database <db-name>          Override the context database
```

Without filters, `list` returns recent refresh jobs scoped to the current
database. Pair with `--query` to extract a single field, e.g.:

```bash
zilliz external-collection refresh list --name my_external_coll \
  --query 'data[?state==`Pending` || state==`Running`].jobId'
```

## Guidance

- An external collection is a collection whose rows live in an external
  source (e.g. a Vector Lake table). The collection's metadata, indexes,
  and schema are in Milvus, but the data is pulled in on demand. The
  `refresh` job is what synchronises that external data into the
  collection so subsequent queries see fresh rows.
- Refresh jobs are asynchronous. After `trigger`, poll with `describe`
  until the job reaches a terminal state. Do not assume completion just
  because `trigger` returned successfully -- that only means the job was
  accepted.
- If `trigger` fails with "collection not found" or "not an external
  collection", verify with `zilliz collection describe --name <name>`
  that the collection actually has an `externalSource` field. If it
  does not, this is a normal in-place collection and refresh does not
  apply -- nothing needs to be done.
- When `describe` reports a failed job, surface the error message to the
  user verbatim. It usually points at a credentials, network, or schema
  mismatch in the external source rather than a Milvus bug.
- Avoid scheduling overlapping refresh jobs against the same collection
  -- check `list --name <name>` for an already-running job before
  triggering a new one.
- A `trigger` on a large external table can run for minutes. Do not
  hold a chat session open polling every few seconds -- give the user
  the `jobId` and explain how to come back and check `describe` later.
- For related operations on the same collection (create, drop, load,
  query) defer to the `collection` skill. This skill only covers the
  refresh lifecycle.
