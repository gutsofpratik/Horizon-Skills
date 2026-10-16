# Proposal Compliance & Control

Read only after resolving `proposal-control-workbook`.

- Use this catalog’s master as the canonical workbook. Use `govtribe-proposal-workflows` from its own installed root. Read its build-proposal-control-workbook.md procedure from that skill's references directory and its conditional extraction, schema and quality guidance; use host discovery or an explicit host-supplied location, never ancestor searching.
- Preserve the eleven-sheet structure, header-based mappings, formulas, validations, helper lists and print panels. Columns may differ from the legacy seed: bind by header names, not remembered column letters.
- Populate Sources first; keep requirement IDs, verbatim text, citations, evaluation links, submission controls and amendment impacts traceable. Run the domain’s prepare_proposal_workbook_render.py and validate_proposal_workbook.py on the working output, using host-authorized input/output locations, plus the host's spreadsheet recalculation, rendering and validation. Follow the domain workflow's Markdown/CSV degradation if its optional Office dependencies are unavailable; do not install packages or claim unperformed validation. A blank master is not a completed or submission-ready matrix.
