---
name: workflow-yylo
description: Create and maintain validated YYLO Ledger workflow Records while keeping storage, execution, and run evidence as separate explicit boundaries.
argument-hint: "[workflow to find/create/update or execution question]"
enable-shell-directives: true
---

# Use YYLO workflow Records

Treat Ledger as the source of truth for workflow identity, validated definition,
and revision history. Use `yy ledger` in a YYLO controller or `yylo-ledger`
standalone. Inspect `COMMAND workflow --help`; if the namespace is absent, do not
invent it or edit Ledger storage directly.

## Keep three boundaries distinct

1. **Ledger stores and validates workflow data.** It does not execute workflows.
2. **A separately selected YYLO runner executes reviewed workflow data.** Storage
   does not grant execution, network, mutation, release, or deployment authority.
3. **Artifact Records retain run evidence.** Do not overwrite the workflow
   definition with stdout, logs, model output, reports, or receipts.

The read-only Ledger host also has no workflow execution endpoint.

## Discover and inspect

Preflight `yy ledger get --help`; prefer `yy ledger get RECORD_ID -f json` for
known IDs without needing the type. If installed get is task-only, use
`yy ledger record get RECORD_ID -f json` after checking native help; stop for an
upgrade if unavailable. New generated workflow IDs use `doc_`, not a workflow
prefix; existing IDs remain unchanged. Exact reads include hot and archived
Records in the selected project. Unknown kinds can be discovered with bounded
`record search`; do not try each kind or project after a miss or ambiguity.
Universal get includes readable UTF-8 text up to 64 KiB by default; omission
reasons are not empty workflow definitions. Request explicit bounded `--content`
when needed (maximum 16 MiB). Typed get remains for source and schema validation.

```bash
yy ledger workflow search --text "release verification" --projection summary --limit 20 -f json
yy ledger get RECORD_ID -f json
yy ledger workflow get RECORD_ID --raw
yy ledger workflow get RECORD_ID --validated
```

Prefer immutable IDs after discovery. Use bounded projections and explicit archive
scope. `--validated` emits normalized YAML only after schema validation.

## Author safe workflow data

A workflow v1 document requires a mapping with `schema_version: v1`, a non-empty
`workflow_id`, and a `steps` list whose step IDs are non-empty and unique.

```yaml
schema_version: v1
workflow_id: focused-validation
steps:
  - id: test
    command: ["npm", "test"]
```

Create through file/stdin transport:

```bash
yy ledger workflow create --title "Focused validation" --file workflow.yaml
```

Ledger rejects unsafe or non-portable YAML, including duplicate keys, aliases,
anchors, explicit tags, recursive structures, non-string mapping keys, implicit
date/time values, non-finite numbers, CRLF input, and unsupported values. Never
weaken validation by storing executable shell as an unvalidated substitute.

## Revise safely

Read the current revision and history, then follow the installed
`workflow update --help` compare-and-replace contract. Bind updates to the
expected revision and preimage/digests, validate the result, and read it back.
On drift, stop and reconcile instead of forcing. Archive is non-destructive.

Before execution, freeze the exact workflow Record ID, revision, payload digest,
runner identity, inputs, and granted authorities. After execution, store bounded
outputs under `artifact-yylo` with workflow/run provenance. An execution request
never implies merge, release, publication, deployment, or production authority.

## Complete request

## User-facing Record results

After creation, update, discovery, or handoff, report the Record kind/profile,
actual immutable Record ID, and actual Ledger slug from the returned Record or a
native get readback. Never invent a slug from the title or confuse it with the ID.
If the selected API omits a field, say it is unavailable rather than fabricate it.
IDs remain authoritative for relations and lifecycle operations; slugs aid discovery.

$ARGUMENTS
