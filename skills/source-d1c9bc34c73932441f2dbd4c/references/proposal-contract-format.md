# Proposal contract format (schema version 1)

The contract is an independent declaration of expected source coverage, not an export of whatever the current workbook happens to contain. Preserve it beside the final QA receipt. `--profile eleven-sheet` remains the default, with unchanged legacy sheet names and CLI output fields.

A contract uses `schema_version: 1`, a delivery `state`, `requirement_ids` from the source inventory, the controlling timezone-aware `deadline`, and `tables`. Each table maps a semantic `role`, actual `sheet`, one-based `header_row`, and semantic `columns` to one-based column numbers. Several roles may share a sheet. The supported columns are:

| Role | Required semantic columns |
|---|---|
| requirements | id, source_id, citation, classification, mandatory, response, owner |
| sources | id, classification, citation |
| deadlines | deadline |
| gaps | id, status |
| amendments | id, requirement_id |

Requirement classifications are `source-requirement` or `internal-control`. Default source classifications: solicitation, amendment, official-qa, customer-input, internal-control. List additional allowed classifications in `source_classifications` only when grounded in the source inventory. Citations must be portable HTTP(S) URLs; use stable official source links including page/section fragments. `amendment_impacts` maps amendment IDs to the complete impacted requirement-ID arrays. `mandatory_inputs` lists missing task-level inputs. A gap row is open unless its status is resolved/closed.

The delivered amendment IDs must exactly match `amendment_impacts`; missing or additional IDs fail. Each array contains unique IDs from `requirement_ids`. For an amendment with no requirement impacts, declare an empty array and retain an amendment row with a blank `requirement_id`. Omitting the inventory means no mapped amendment rows are expected.

Active deadlines must match both the controlling instant and its source-local UTC offset. Equivalent formatting (a space instead of `T`, or `Z` instead of `+00:00`) is accepted. Converting `17:00-04:00` to `21:00Z` preserves the instant but loses the required local representation and fails that separate check. Preserve a named source zone in the source notes when supplied; the helper checks the offset encoded in the deadline, not a zone name inferred from it.

```json
{"schema_version":1,"state":"review-draft","requirement_ids":["R1"],"deadline":"2030-05-10T17:00:00-04:00","tables":[{"role":"requirements","sheet":"Matrix","header_row":1,"columns":{"id":1,"source_id":2,"citation":3,"classification":4,"mandatory":5,"response":6,"owner":7}},{"role":"sources","sheet":"Sources","header_row":1,"columns":{"id":1,"classification":2,"citation":3}},{"role":"deadlines","sheet":"Deadlines","header_row":1,"columns":{"deadline":1}},{"role":"gaps","sheet":"Gaps","header_row":1,"columns":{"id":1,"status":2}}]}
```

The proposal validator proves source/control checks, not spreadsheet calculation or page layout. Use the host's spreadsheet recalculation, behavioral checks, render and visual inspection for those separate checks. When unavailable, preserve the workbook and validated Markdown or CSV controls, explicitly state the unexecuted checks, and leave readiness unresolved. Retain both receipts for the same artifact SHA256. After any workbook save, invalidate both receipts and rerun final checks.
