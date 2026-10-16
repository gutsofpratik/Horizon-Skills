# Workbook schema

For the curated workbook, resolve `proposal-control-workbook` through `govtribe-file-templates`; that skill owns the approved master. This schema remains the standalone construction contract for portable hosts or a user-authorized new design. Column lists describe logical fields; locate actual columns by header name rather than ordinal position.

## Sheet order
1. `Start Here`
2. `Opportunity Setup`
3. `Dashboard`
4. `Requirement Matrix`
5. `Evaluation Crosswalk`
6. `Submission Checklist`
7. `Pricing & Deliverables`
8. `Questions-Risks`
9. `Amendment Log`
10. `Sources`
11. `Lists`

## Keep these design rules
- Preserve the overall structure unless a different workbook design is explicitly requested.
- Keep one filterable header row per working sheet.
- Do not remove the `Lists` tab if data validation depends on it.
- Preserve formulas on `Dashboard` when working from the resolved master or an existing working workbook.
- Freeze the working header row and keep columns wide enough for citations and notes.
- Prefer plain, operational labels over decorative formatting.

## Required tabs and key fields

### `Start Here`
Purpose: orient the proposal team and explain the workbook.
Include:
- workbook purpose,
- how to use it,
- reminder that the matrix is traceability and control support.

### `Opportunity Setup`
Purpose: set the pursuit profile and review schedule.
Key fields:
- opportunity name,
- solicitation or notice number,
- agency or buying office,
- NAICS, PSC, set-aside, contract type,
- due date and time zone,
- submission method,
- proposal volumes,
- internal review milestones.

### `Dashboard`
Purpose: management roll-up.
Track at minimum:
- total requirements,
- mandatory rows,
- evaluated rows,
- missing owners,
- open checklist items,
- open questions,
- amendment-driven changes.

### `Requirement Matrix`
Purpose: one-row-per-requirement control sheet.
Columns:
1. `Req ID`
2. `Source Area`
3. `Requirement Category`
4. `Requirement Level`
5. `Source Citation`
6. `Verbatim Requirement`
7. `Proposal Action / Interpretation`
8. `Proposal Volume`
9. `Proposal Outline Ref`
10. `Owner`
11. `Support Owner(s)`
12. `Compliance Posture`
13. `Draft Status`
14. `Evidence / Artifact Needed`
15. `Evaluator Focus / Discriminator`
16. `Final Proposal Location`
17. `Final Page / File`
18. `Amendment / Q&A Impact`
19. `Notes / Assumptions`
20. `Source URL`
21. `Control Flag`

### `Evaluation Crosswalk`
Purpose: keep evaluator priorities visible.
Columns:
1. `Eval ID`
2. `Source Citation`
3. `Factor / Subfactor`
4. `Relative Importance`
5. `Evaluator Focus`
6. `Related Req IDs`
7. `Proposal Volume`
8. `Proposal Section`
9. `Lead Owner`
10. `Evidence / Discriminators`
11. `Review Status`
12. `Source URL`

### `Submission Checklist`
Purpose: track preventable compliance failures.
Columns:
1. `Check ID`
2. `Category`
3. `Control Item`
4. `Why it matters`
5. `Owner`
6. `Due / Verify By`
7. `Status`
8. `Evidence / Location`
9. `Source Citation`
10. `Notes`
11. `Control Flag`

### `Pricing & Deliverables`
Purpose: map CLINs, deliverables, attachments, and pricing support files.
Columns:
1. `Item ID`
2. `Item Type`
3. `Source Citation`
4. `Description`
5. `Related Requirement IDs`
6. `Price / Proposal Location`
7. `Owner`
8. `Status`
9. `Notes`
10. `Source URL`

### `Questions-Risks`
Purpose: capture unresolved issues and decisions.
Columns:
1. `Item ID`
2. `Type`
3. `Priority`
4. `Issue / Decision`
5. `Impacted Req IDs`
6. `Owner`
7. `Resolution Path`
8. `Need Customer Q&A?`
9. `Status`
10. `Resolution / Notes`
11. `Due Date`

### `Amendment Log`
Purpose: manage solicitation change control.
Columns:
1. `Amendment ID`
2. `Date`
3. `Change Type`
4. `Summary of Change / Clarification`
5. `Impacted Sections`
6. `Impacted Req IDs`
7. `Owner`
8. `Action Needed`
9. `Status`
10. `Source URL`

### `Sources`
Purpose: preserve both design rationale and pursuit-specific source register.
Columns:
1. `Source Type`
2. `Short Name`
3. `What it supports`
4. `Key Takeaway / Notes`
5. `Source URL`

### `Lists`
Purpose: helper values for validation and consistency.
Recommended value groups:
- source area,
- requirement category,
- requirement level,
- compliance posture,
- draft status,
- evaluation importance,
- review status.
