# Requirement extraction rules

## Primary rule
Create one row for each discrete proposal action, compliance obligation, evaluation discriminator, submission control, pricing item, or amendment-driven change that the team could miss.

## What becomes a row
Create a row when the solicitation tells the offeror to do, include, submit, address, or acknowledge something, or when Section M reveals something evaluators will explicitly assess.

Common trigger verbs:
- shall
- must
- will
- submit
- provide
- include
- address
- describe
- explain
- identify
- discuss
- demonstrate
- propose
- complete
- acknowledge
- certify
- upload
- label
- format

Also create rows for:
- due date and submission instructions,
- file naming, page limits, font, spacing, and packaging rules,
- required forms, resumes, attachments, and representations,
- CLIN-specific pricing and deliverables,
- evaluation factors and subfactors,
- amendment and Q&A answers that change prior instructions.

## What usually does not become a row
Do not create a row for every clause or background paragraph unless it creates a real proposal action, evaluation implication, or compliance control.

Examples that are often notes rather than rows:
- general acquisition background,
- mission context without an offeror action,
- duplicated restatements of a requirement already captured elsewhere,
- boilerplate clauses with no proposal submission impact.

## Row-splitting rules
Split into separate rows when any of these are true:
- numbered or lettered elements each require a distinct response,
- one paragraph mixes technical, management, staffing, and pricing directions,
- a single citation contains multiple mandatory artifacts,
- omission of one element would create a compliance miss even if the rest were covered,
- a Section M sentence contains separate discriminators that different writers must address.

Default to finer granularity when in doubt.

## Citation rule
- Keep the exact section, page, paragraph, table, attachment, or amendment citation.
- If the source is a PDF, include page number when available.
- If the source is an amendment or Q&A, cite that source directly and note the superseded section if known.

## Verbatim requirement rule
- Preserve the exact requirement text or the minimally necessary excerpt.
- Do not rewrite the source language in the `Verbatim Requirement` field.
- Put interpretation and tasking in `Proposal Action / Interpretation`.

## Proposal action / interpretation rule
Write this field as a clear writer task, not a restatement.

Good examples:
- `Describe the transition governance model, milestones, and staffing ramp for day-one continuity.`
- `Provide resumes for each proposed key person using the required resume elements.`
- `Acknowledge Amendment 0003 and update the due date on all control sheets.`

Avoid vague entries like:
- `Respond to this requirement`
- `Address technical approach`

## Field conventions

### `Req ID`
Use sequential IDs such as `RM-001`, `RM-002`, `RM-003`.

### `Source Area`
Use these values when possible:
- `C / PWS / SOW`
- `L - Instructions`
- `M - Evaluation`
- `B - CLIN / Pricing`
- `J - Attachment / Exhibit`
- `H / Special Terms`
- `Amendment`
- `Q&A`
- `Other`

### `Requirement Category`
Choose the best fit:
- `Submission`
- `Format / Packaging`
- `Technical`
- `Management`
- `Staffing`
- `Past Performance`
- `Pricing`
- `Security`
- `Transition`
- `Deliverable / Report`
- `Small Business`
- `OCI / Legal`
- `Attachment / Form`
- `Schedule`
- `Other`

### `Requirement Level`
Use these meanings:
- `Mandatory`: explicit proposal content, submission, formatting, pricing, attachment, or acknowledgement requirement.
- `Evaluated`: factor, subfactor, discriminator, or emphasis that will affect assessment.
- `Clarification`: ambiguous or not fully controlling without more context.
- `Informational`: useful context that does not by itself require a response.
- `Risk Item`: internal control row created to prevent a likely miss.

### `Compliance Posture`
Use:
- `Comply` when the requirement is understood and the plan is complete enough to respond.
- `Partial` when a response path exists but is incomplete.
- `Gap` when the team has no adequate answer, owner, or evidence yet.
- `Question` when the source is ambiguous or needs leadership or customer clarification.
- `N/A` only when the requirement is truly not applicable.

### `Draft Status`
Use:
- `Not Started`
- `In Progress`
- `In Review`
- `Final`

## Section L versus Section M handling
- Section L rows tell the team what to submit and how.
- Section M rows tell the team what evaluators care about.
- Preserve both views.
- When Section L and Section M clearly map to one another, connect them through `Related Req IDs`, `Evaluator Focus / Discriminator`, and the `Evaluation Crosswalk`.

## Submission and pricing overlap rules
- If a requirement affects technical content and final packaging, represent it in the matrix and the checklist.
- If a requirement affects technical content and pricing completeness, represent it in the matrix and the pricing map.

## Amendments and Q&A
- Do not leave the original row untouched if later guidance changes it.
- Update the affected requirement row and note the impact.
- Log the change in `Amendment Log`.
- If the amendment creates a new requirement, add a new row.
- If the amendment removes a requirement, keep traceability but mark the row clearly as changed or superseded.

## Ambiguity rule
If the source is unclear:
1. capture the row anyway,
2. mark `Compliance Posture` as `Question` or `Partial`,
3. log the issue in `Questions-Risks`,
4. avoid inventing a definitive interpretation.

## Common edge cases
- Resume templates: separate the resume package requirement from the individual resume elements if the team needs detailed control.
- Past performance: separate submission quantity rules, recency rules, similarity rules, and questionnaire or CPARS support rules if each can be missed independently.
- Oral presentations or demonstrations: create dedicated rows for content, time limits, attendees, format, and logistics.
- Security or OCI representations: treat required attestations and mitigation plans as distinct rows.
- Attachment-driven requirements: cite the attachment directly, not only the main RFP section.
