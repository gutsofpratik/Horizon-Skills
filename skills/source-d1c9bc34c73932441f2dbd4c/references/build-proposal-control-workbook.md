# Build Proposal Control Workbook

## Overview
- Use this workflow for a proposal control workbook, requirement matrix, compliance matrix, proposal cross-reference matrix, or Section L / Section M crosswalk tied to a federal, state, local, or grant solicitation.
- Prefer this workflow when the output should guide a proposal team, not just summarize the solicitation.
- Goal: produce a working GovTribe proposal workbook that traces the solicitation to the proposal and keeps evaluator priorities, submission controls, and change control visible.
- If the real request is a writer-facing annotated outline, storyboard starter, or section-by-section drafting package, switch to [Build Annotated Proposal Outline](build-annotated-proposal-outline.md) instead of forcing workbook output.

## Default output
- For a new curated workbook, use `govtribe-file-templates` to resolve catalog ID `proposal-control-workbook`. Its approved blank master is the canonical master; the populated example is a reference, not a source of solicitation facts.
- Use the bundled `govtribe-document-editing` skill and the host's file capabilities for adaptation and revision handling. For an existing workbook, continue from the selected working revision rather than resetting it to the master.
- If the user selected a specific catalog revision and resolution fails, obtain that verified revision before adaptation; do not silently substitute a schema-built workbook.
- The portable distribution includes a generated `assets/proposal-control-workbook.xlsx` copy of the same canonical master; use that copy when available. Without a packaged or supplied workbook, create one with the tabs and key fields in [Workbook Schema](workbook-schema.md), using host spreadsheet capabilities. Identify schema-built output as such; it is not the approved master. Keep the source-traceability, validation and partial-output rules below. The generated portable copy is never an independently maintained source master.
- Also deliver a concise narrative summary with:
  - coverage status,
  - highest-risk gaps,
  - open questions and assumptions,
  - critical dates and submission controls,
  - next actions for the proposal team.

## Inputs to resolve
Resolve as many of these inputs as are available from the request, opportunity context, and source files. Do not block if some are missing.
- Solicitation number and opportunity name
- RFP, notice, or task-order request
- Section L instructions
- Section M evaluation factors
- PWS, SOW, SOO, and attachments, exhibits, or forms
- Pricing sheets, CLIN structure, and deliverable attachments
- Amendments, conformed RFP, and Q&A
- Proposal schedule, owners, and review milestones if available
- Existing proposal control workbook, compliance matrix, account template, or prior generated workbook if the user asks to reuse, update, or match one

If critical source documents are missing, build a partial workbook, mark it clearly as partial, and list the missing documents needed to complete it.

If vector-store retrieval skips pricing schedules, workbook attachments, CSV/TSV files, CLIN tables, budget templates, or staffing matrices, use the external host's attachment or spreadsheet capability. If none is available, mark the source register partial, deliver supported Markdown or CSV control tables, and request a supported export only when the missing content materially changes the result.

## Read-on-demand references
- Read [Workbook Schema](workbook-schema.md) before creating a workbook from scratch or modifying the tab structure.
- Read [Requirement Extraction Rules](extraction-rules.md) before populating the Requirement Matrix.
- Read [Quality Checks](quality-checks.md) before finalizing.
- Read [Final Proposal Artifact Quality Checks](./final-artifact-quality-checks.md) before delivering the workbook or any companion narrative.
- Read [Prior User File Context](prior-user-file-context.md) before searching for a prior workbook, proposal template, approved boilerplate, or reusable matrix structure.
- On an authorized working copy, when execution and `openpyxl` are available, before PDF rendering or visual delivery run `python3 scripts/prepare_proposal_workbook_render.py path/to/workbook.xlsx --in-place` so print areas, fit-to-width settings, and wrapped row heights reflect the populated workbook.
- For generic workbook-derived PDF QA, use the external host's spreadsheet render and visual-inspection capability.
- When execution and `openpyxl` are available, before final delivery run `python3 scripts/validate_proposal_workbook.py path/to/workbook.xlsx` and correct any reported errors.

## Procedure

### 1) Build the source register first
1. Create or update the `Sources` tab with every source file used.
2. Prefer the latest conformed or amended solicitation text.
3. If an amendment changes prior language, treat the latest amendment as controlling and log the change in `Amendment Log`.
4. Use the host's attachment or spreadsheet capability for spreadsheet-like pricing, CLIN, budget, and staffing files skipped by vector-store retrieval; otherwise record the coverage gap and continue with a labeled partial workbook or CSV controls.
5. Preserve exact citations so every row can be traced back to the source.

### 2) Reconstruct the proposal model
Identify:
- proposal volumes or files the offeror must submit,
- evaluation factors and subfactors,
- due date, time, time zone, portal or delivery method, and file packaging rules,
- page limits, font, spacing, naming rules, and required forms or attachments,
- CLINs, pricing instructions, and required deliverables,
- any explicit risk, staffing, security, small business, OCI, transition, past performance, or management response instructions.

### 3) Populate the workbook
Populate a working copy of the resolved master or selected workbook. Map columns by header names, not legacy column letters. Update these tabs in this order:

1. `Opportunity Setup`
   - Fill opportunity metadata, major dates, and review schedule.
2. `Requirement Matrix`
   - Use one row per discrete requirement or response instruction.
   - Split each separate shall, must, will, submit, provide, describe, explain, identify, discuss, complete, acknowledge, include, or demonstrate instruction into its own row.
   - Keep the exact source citation and verbatim requirement.
   - Translate the requirement into a proposal-writing task in `Proposal Action / Interpretation`.
   - Assign proposal volume, outline reference, owner, evidence needed, and compliance posture.
   - If the requirement is changed by an amendment or Q&A, note that in `Amendment / Q&A Impact` and update the row rather than duplicating stale guidance.
3. `Evaluation Crosswalk`
   - Use one row per factor or subfactor from Section M or equivalent.
   - Preserve the exact evaluation language, relative importance, evaluator focus, and related requirement IDs.
   - Link each factor to the proposal volume and section where the team intends to win.
4. `Submission Checklist`
   - Capture deadline, submission method, file naming, formatting, signatures, amendment acknowledgement, reps and certs, and all packaging controls that can cause a preventable compliance failure.
5. `Pricing & Deliverables`
   - Capture CLINs, optional CLINs, price narratives, deliverables, attachments, and any support files that must accompany the price volume.
6. `Questions-Risks`
   - Log ambiguities, internal assumptions, missing information, and items needing customer Q&A or leadership decisions.
7. `Amendment Log`
   - Record every amendment, conformed update, and relevant Q&A answer that changes requirements, instructions, schedule, pricing, or evaluation logic.
8. `Dashboard`
   - Preserve formulas if already present. Otherwise summarize counts of total requirements, mandatory rows, evaluated rows, missing owners, open checklist items, open questions, and changed items.
9. `Start Here`
   - Keep the workbook purpose and usage notes intact unless a customized intro is explicitly requested.

### 4) Handle requirement rows carefully
For row-splitting, categorization, and field conventions, follow [Requirement Extraction Rules](extraction-rules.md).

Core rules:
- Do not merge separate instructions just because they appear in the same paragraph.
- Do not paraphrase the citation or the verbatim requirement.
- Put informative background that does not create a proposal action into `Notes / Assumptions`, not the requirement text.
- If the solicitation gives an evaluation discriminator but not a direct command, still capture it as an evaluated row or in `Evaluation Crosswalk`.
- If a control is administrative or packaging-only, make sure it appears in `Submission Checklist` even if it is also represented in the matrix.
- If a pricing instruction or deliverable affects completeness, make sure it appears in `Pricing & Deliverables` even if it is also represented in the matrix.

### 5) Maintain Section L / Section M traceability
- Keep proposal instructions traceable to evaluation factors wherever the solicitation makes the linkage explicit.
- Make it easy for the writing team to see both:
  - what must be included, and
  - what evaluators are likely to reward or penalize.
- When Section M factors map to multiple requirements, link all relevant requirement IDs rather than collapsing them into one generic note.

### 6) Use a validation loop before finalizing
Run the checklist in [Quality Checks](quality-checks.md).
Run `scripts/prepare_proposal_workbook_render.py` before rendering and `scripts/validate_proposal_workbook.py` before delivery when execution is available.
If `openpyxl` or script execution is unavailable, use the host's spreadsheet capability, inspect every sheet against [Workbook Schema](workbook-schema.md) and [Quality Checks](quality-checks.md), and deliver Markdown or CSV control views alongside the workbook when visual verification remains unavailable. If validation fails, correct the workbook and re-check before delivering.

### 7) Deliver the result
Return:
- the populated workbook file,
- a concise summary of major requirement counts, open gaps, open questions, amendment impacts, and submission controls,
- a clear statement if the workbook is partial because source documents were missing.

## Output rules
- Be recommendation-first and control-focused.
- Prefer exact solicitation language for requirement and evaluation fields.
- Make synthesis explicit in interpretation, notes, risks, and summary fields.
- Flag uncertainty instead of guessing when the source is ambiguous.
- Keep the workbook operational for proposal managers, writers, reviewers, and pricing.

## Common failure modes to avoid
- Treating one paragraph with multiple commands as one requirement row
- Missing page-limit, file-format, or amendment-acknowledgement controls
- Capturing Section L instructions without connecting Section M evaluator priorities
- Letting stale pre-amendment language survive in the matrix
- Mixing pricing detail into technical locations or vice versa
- Producing a narrative summary without a usable workbook
- Using the workbook workflow when the proposal team actually needs a writer-facing outline or storyboard package
