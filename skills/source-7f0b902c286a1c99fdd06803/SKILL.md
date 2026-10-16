---
name: understand-project-yylo
description: Inspect the current product architecture, dependencies, and validation loops before planning or implementing a requested change.
argument-hint: "[Main Task] [Constraints] [Ultimate Goal]"
enable-shell-directives: true
---

# Understand the project

1. Read `AGENTS.md`/`CLAUDE.md`, repository status, relevant source, tests, and existing product documentation in the integration or assigned feature worktree.
2. Read related Kanban tasks and durable specs through the canonical metadata controller. Do not assume `.juno_task/plan.md` exists and do not materialize controller-private metadata in a product worktree.
3. Trace only the dependencies and runtime paths needed for the requested goal. Use bounded parallel investigation when independent questions justify it.
4. Report current behavior, sources of truth, affected components, risks, unknowns, and the smallest useful validation loop.
5. If the user requested planning, hand the findings to `plan-ledger-tasks-yylo`. If implementation was requested, work only in the task worktree returned by `yy task start TASK_ID`.
6. Write a durable operational spec only when requested or materially useful. Draft it externally, preflight the installed `yy ledger artifact` API, capture it as an immutable `report` Artifact Record with provenance/retention, and verify retrieval, digest, and history. If that API is unavailable, stop with the external draft intact; never fall back to product `docs/`, task bodies/responses, new `.juno_task/specs`, or direct controller-store edits. Product `docs/` remains reserved for documentation shipped with the product. Do not update root instructions with transient status.

## Retrieve context without guessing types

Preflight `yy ledger get --help`; prefer `yy ledger get RECORD_ID -f json` for
known task, document, PDR or artifact IDs. If installed get is task-only, use
`yy ledger record get RECORD_ID -f json` after checking native help; stop for an
upgrade if unavailable. New generated IDs use `task_`, `doc_`, or `artifact_` for
storage kind; existing IDs remain unchanged. New PDRs are artifact/report;
historical document/pdr Records remain readable without reclassification.

When no ID is known, use `yy ledger record search --projection summary --limit 20 -f json`.
Exact reads include hot and archived Records in the selected project; discovery
is hot-only unless archive scope is explicit. Preserve missing/ambiguous/corrupt
record diagnostics rather than trying other kinds or projects. Universal get
includes small readable UTF-8 content up to 64 KiB; metadata with omitted content
is not payload evidence. Use explicit bounded `--content` for local/inline bytes
(maximum 16 MiB), check exit status, and never implicitly fetch external URLs.

## User-facing Record results

After creation, update, discovery, or handoff, report the Record kind/profile,
actual immutable Record ID, and actual Ledger slug from the returned Record or a
native get readback. Never invent a slug from the title or confuse it with the ID.
If the selected API omits a field, say it is unavailable rather than fabricate it.
IDs remain authoritative for relations and lifecycle operations; slugs aid discovery.

## Invocation contract

The structured views below intentionally alias parts of the complete request; they are not additional user arguments.

### Main task

$1

### Constraints and context

$2

### Complete raw request

$ARGUMENTS
