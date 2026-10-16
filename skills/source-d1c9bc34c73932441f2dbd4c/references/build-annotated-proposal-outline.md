# Build Annotated Proposal Outline

## Overview
- Use this workflow for an annotated proposal outline, proposal skeleton, storyboard starter, writer work package, or compliance-to-outline mapping package tied to a solicitation.
- Prefer this workflow when the output should help proposal managers and writers start drafting, not just control compliance in a spreadsheet.
- Goal: produce a writer-facing outline that maps instructions, evaluation factors, work requirements, and evidence needs into a usable proposal structure.

## Default output
- Prefer a Markdown deliverable based on Annotated Proposal Outline Template (`assets/annotated-proposal-outline-template.md`, from the skill root).
- If requested, also provide:
  - a CSV companion based on Annotated Proposal Compliance Matrix Template (`assets/annotated-proposal-compliance-matrix-template.csv`, from the skill root),
  - or an intermediate JSON representation that validates against Annotated Proposal Outline Schema (`assets/annotated-proposal-outline-schema.json`, from the skill root).
- Include a concise summary of:
  - source coverage,
  - highest-risk requirements,
  - major assumptions,
  - open questions,
  - and recommended next steps.
- Keep the Markdown document readable: include a compact compliance matrix summary, not a full row-level matrix, unless the user explicitly asks for the full matrix inside the document.
- Put the complete requirement-by-requirement compliance matrix in the CSV and/or JSON companion artifact.

If the request is primarily for spreadsheet controls, dashboarding, or submission tracking, use [Build Proposal Control Workbook](build-proposal-control-workbook.md) instead or as a companion artifact.

If a proposal control workbook already exists, treat it as the control baseline for the outline. Reuse its requirement IDs, source citations, amendment notes, and unresolved-gap list rather than re-shredding from scratch, unless the workbook is clearly incomplete, stale, or missing needed source coverage.

## Inputs to resolve
Resolve as many of these as are available from the request, opportunity context, and source files. Do not block if some are missing.
- Solicitation number and opportunity name
- RFP, RFQ, task-order request, notice, or grant package
- Section L instructions or equivalent submission guidance
- Section M evaluation factors or equivalent award criteria
- PWS, SOW, SOO, CDRLs, attachments, forms, and pricing templates
- Amendments, conformed solicitation text, and Q&A
- Company context, win themes, past performance, vehicles, and differentiators if available
- Any requested page budgets, outline conventions, or owner assignments
- Prior annotated outlines, proposal templates, capability statements, approved boilerplate, or reusable past performance language when the user asks to reuse or match earlier work

If critical source files are missing, build a partial outline and state exactly what is missing.

If vector-store retrieval skips pricing schedules, workbook attachments, CSV/TSV files, CLIN tables, budget templates, or staffing matrices, use the external host's attachment or spreadsheet capability. If none is available, label the gap, deliver the supported Markdown or CSV result, and request a supported export only when the missing content materially changes package coverage.

## Read-on-demand references
- Read [Annotated Proposal Outline Method](annotated-outline-method.md) before shredding requirements or building the hierarchy.
- Read [Annotated Outline Source Priority](annotated-outline-source-priority.md) when amendments, metadata, attachments, or company context conflict.
- Read [Annotated Outline Quality Checks](annotated-outline-quality-checks.md) before finalizing.
- Read [Final Proposal Artifact Quality Checks](./final-artifact-quality-checks.md) before delivering a customer-facing outline, storyboard package, DOCX, or PDF.
- Read [Prior User File Context](prior-user-file-context.md) before searching for prior proposal outlines, templates, boilerplate, or reusable company evidence.

## Procedure

### 1) Build the source inventory first
- Record every solicitation file, amendment, Q&A set, attachment, and relevant GovTribe context source used.
- Prefer the latest conformed or amended solicitation package.
- Preserve stable source IDs so every requirement and section annotation can be traced later.

### 2) Shred the solicitation into requirements
Use [Annotated Proposal Outline Method](annotated-outline-method.md).
If a current proposal control workbook exists, start from its requirement map first and only extract net-new or corrected items needed to support the outline.
Capture:
- instructions,
- evaluation factors,
- work or PWS tasks,
- deliverables,
- formatting and submission controls,
- pricing dependencies,
- forms and certifications,
- and gaps or ambiguities.

If exact wording matters, call `Add_To_Vector_Store`, wait for readiness, and use focused `Search_Vector_Store` queries instead of relying on loose summaries. Use [Vector-Store Content Retrieval](govtribe-docs-vector-store-content-retrieval.md) for stable guidance and `Documentation` for current schemas.
If an important spreadsheet-like file was skipped by vector retrieval, use the host attachment or spreadsheet capability; otherwise disclose the gap and deliver the supported partial result before finalizing source coverage or proposal annotations.

### 3) Build the outline hierarchy
- Follow the required volume and section structure when the solicitation gives one.
- If the solicitation is structurally weak, infer a defensible outline from the evaluation model and work breakdown, and label it as inferred.
- Preserve Section L submission logic while keeping Section M scoring logic visible.

### 4) Annotate each section for the writing team
For each major section and meaningful subsection, include:
- purpose or evaluator question,
- source mapping,
- mandatory response content,
- evaluation mapping,
- work or PWS mapping,
- GovTribe and company intelligence hooks,
- win-theme placeholders,
- evidence needed,
- graphics or tables,
- suggested owner,
- page budget,
- open questions or risks.

Use Annotated Proposal Requirement Types (`assets/annotated-proposal-requirement-types.yaml`, from the skill root) when a consistent requirement taxonomy is needed.

### 5) Create writer work packages and unresolved-item lists
- Group sections into practical writing packages with owners, inputs, and review focus.
- Keep ambiguous, conflicting, or unmapped requirements visible instead of burying them in notes.
- If pricing is a separate volume, capture dependencies without inventing a pricing strategy.

### 6) Keep the document matrix compact
- In the Markdown outline, summarize compliance coverage with counts by requirement type, priority, mapping status, volume, and highest-risk gap.
- Use a narrow risk/coverage table in the Markdown document. Prefer columns like `Req ID`, `Why it matters`, `Status`, `Outline location`, and `Next action` instead of the full compliance-matrix column set.
- Include only representative or high-risk rows in the Markdown compliance matrix summary, such as mandatory submission controls, evaluated criteria, gaps, partial mappings, or newly amended requirements.
- Keep the Markdown summary table to 8 rows or fewer by default.
- If the full matrix has more than 12 rows, do not include every row in the Markdown/PDF. State that the full row-level matrix is delivered in the CSV or JSON companion.
- If the user explicitly requests a full matrix inside a rendered document, split it by volume or requirement family and use landscape-friendly formatting.

### 7) Validate before finalizing
- Run the checklist in [Annotated Outline Quality Checks](annotated-outline-quality-checks.md).
- If you created an intermediate JSON outline, validate it against Annotated Proposal Outline Schema (`assets/annotated-proposal-outline-schema.json`, from the skill root).
- If script execution is available in the external host, run from the skill root:

```bash
python3 scripts/validate_annotated_outline.py path/to/outline.json
```

- If execution is not available, perform the same checks manually before delivery.

### 8) Deliver the result
Return:
- the annotated outline,
- any requested CSV or JSON companion,
- a concise summary of risks, assumptions, unmapped requirements, and next steps,
- and a clear note if the result is partial because source files were missing.

## Output rules
- Keep the deliverable writer-facing and proposal-operational.
- Prefer exact solicitation language for instruction and evaluation fields.
- Make all inferred structure, win themes, and assumptions explicit.
- Do not invent capabilities, pricing, staffing, or past performance proof.
- Keep evaluator priorities and work requirements visible at the same time.
- Flag conflicts and missing files directly.

## Common failure modes to avoid
- Building an outline from Section L only
- Losing Section M scoring logic inside a generic section list
- Hiding submission controls, attachments, or forms outside the outline package
- Turning the result into one giant matrix without a readable section structure
- Inventing proof points or win themes that the company has not supported
- Ignoring amendments, Q&A, or conflicting source files
- Recreating a second, incompatible requirement map when a usable proposal control workbook already exists
