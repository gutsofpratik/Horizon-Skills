---
title: Draft Response and Fill Template
description: Draft source-grounded RFI, RFQ, capability, project-plan, and other proposal responses, then populate user-provided templates without losing structure or prior edits.
---

# Draft Response and Fill Template

Use this reference for asks such as "create an RFI response based on the attached," "how do I respond to this," "draft a project plan," "use this template," or "fill this out too."

## Goal

- Recover the active solicitation, RFI, RFQ, request, or pursuit from the current thread and attached files.
- Determine the exact response package the buyer expects.
- Draft a persuasive but source-grounded response using known company context.
- Populate the requested Word, spreadsheet, PDF, survey, or other template while preserving its required structure.
- Support iterative follow-ups without restarting the analysis or discarding accepted user edits.

## Context recovery

Before asking the user to repeat information, inspect:

- the active GovTribe record or pursuit in the conversation
- attached solicitation, PWS/SOW, survey, instructions, amendments, and Q&A files
- company context already provided in the thread or available from permitted user context
- prior draft artifacts and templates in the same workflow
- requested delivery format and any previous formatting decisions

A terse prompt is sufficient when "this," the target record, and the source files resolve cleanly. Ask one bounded clarification only when multiple possible targets or output formats remain.

Preserve the resolved target, provided source files and requested source scope. For needed record lookup or refresh, select the tool by established target type: `Search_Federal_Contract_Opportunities` for federal contract opportunities, `Search_State_And_Local_Contract_Opportunities` for state/local contract opportunities, `Search_Federal_Grant_Opportunities` for federal grant opportunities, or `Search_Pursuits` for pursuits. Use `Search_GovTribe` when the type remains unresolved; a solicitation number, notice ID, title or URL alone does not establish a federal-contract type. Use `Search_Government_Files` and `Search_User_Files` for source and reusable files. When exact file text controls the response, call `Add_To_Vector_Store`, wait for readiness, and use focused `Search_Vector_Store` queries. Cite returned source metadata through the external host's native citation format.

## Source priority

Use this order when sources conflict:

1. current controlling solicitation or notice and formally incorporated amendments; apply Q&A according to its stated authority and incorporation status
2. buyer-provided response form, survey, workbook, or template
3. PWS, SOW, SOO, attachments, exhibits, and submission instructions
4. verified GovTribe opportunity, pursuit, agency, vehicle, and vendor context
5. company-provided facts, approved boilerplate, capability statements, and past performance
6. clearly labeled assumptions or drafting recommendations

Do not invent company capabilities, past performance, certifications, staffing, pricing, or commitments to complete a template.

Use the source package's explicit order of precedence. Informal Q&A does not automatically override an issued requirement. Company evidence establishes what the company can substantiate; it does not change the buyer's requirements. Surface unresolved conflicts before representing the response as compliant.

## Workflow

### 1. Resolve the artifact intent

Classify the request as one or more of:

- response strategy or "how should we respond"
- RFI or sources-sought response
- RFQ or capability response
- cover letter or submission email
- project or management plan
- questionnaire, survey, information sheet, or form completion
- buyer-provided template population
- revision of an existing draft

Identify the intended reader and decision as part of artifact intent. External responses and capability statements normally serve the relevant government program, technical and acquisition reviewers; use the source requirement and evaluation criteria to establish their priorities. Writer-facing outlines and internal control packages serve the proposal team. An explicitly requested partner or internal audience takes precedence. Reuse resolved context and ask only when competing audiences would materially change the response.

### 2. Build the response requirement map

Extract:

- questions and requested topics
- page, word, file, and formatting constraints
- required forms, attachments, and representations
- evaluation or market-research signals
- submission instructions and deadlines
- company evidence needed for each response section
- unresolved questions, assumptions, and approval points

Use exact source language where compliance depends on wording.

### 3. Draft the response package

Optionally apply the bundled `govtribe-govcon-writing` skill to drafting, rewriting, shortening, or prose review using the established requirement map and evidence. Otherwise follow the writing steps here. Review-only requests produce findings; file conversion alone preserves accepted wording.

- Match the buyer's requested order and terminology.
- Lead with direct answers before supporting narrative. Connect supported capabilities to the intended reader's mission and decision; do not substitute generic sales language or invent evaluation preferences.
- Tailor the response to the user's company, role, market, and known differentiators without overstating them.
- Keep claims traceable to company-provided or retrieved evidence.
- Keep missing evidence and confirmation items in internal review notes. Use unmistakable placeholders in a review draft when needed, but do not add them to government-facing fields when buyer instructions prohibit caveats or extra text. Missing mandatory facts leave the draft incomplete.
- Deliver the requested coordinated package, such as cover letter, narrative, survey answers, information sheet, checklist, and submission email. Include only components permitted by the buyer in the external package.

### Purposeful proposal and CONOPS illustrations

Use an illustration when requested or when it materially explains the proposed service. Name the intended reviewers, their mission and the decision the figure supports in the visual brief. Ground it in the source requirement and supported solution narrative; distinguish proposed/conceptual elements from verified capability and past performance. Build a self-contained visual brief naming audience, mission, decision, supported content, palette/style, aspect ratio, selected asset revision and occurrence, caption and alt text. Reuse approved customer artwork. Use the host's image generation or editing capability only when available; it is separate from GovTribe MCP. Access image binaries through authorized host attachments/downloads or file tools; vector retrieval is not image access. Preserve the original and edited assets and inspect the saved image before embedding. A host-created image does not automatically become a GovTribe User File or receive a GovTribe generation identifier. If generation is unavailable, reuse an authorized supplied asset, use an appropriate deterministic diagram, or omit optional decoration. Disclose an explicitly requested illustration that could not be produced.

Check buyer page, file and formatting limits before allocating figure space. Keep required wording, precise process labels, values and citations in editable text/shapes/tables; use deterministic charts for measured comparisons. Do not replace an approved logo, seal or fixed template illustration unless the request calls for that edit. A crowded matrix or compliance workbook does not need generated decoration.

Embed the inspected figure through the host's destination-format capability, add a useful caption and alt text, render and inspect the final artifact. Reuse selected imagery during text-only revisions; on an image edit preserve approved wording, page geometry and unaffected artwork. Generating a figure does not complete the requested response package.

### 4. Populate the template faithfully

- Preserve required headings, tables, fields, sheet names, page layout, and file type.
- Fill existing fields rather than recreating a different document unless the source template is unusable.
- Identify blank or uncertain fields in review notes instead of fabricating answers; preserve buyer restrictions on text inside the form.
- Retain previously accepted user edits during follow-up revisions.
- Use the external host's provider-neutral document, spreadsheet, PDF, or presentation capability for artifact construction and render validation. If unavailable, deliver the validated Markdown, CSV, or JSON source artifact and state what was not rendered or visually verified.

### 5. Support iterative completion

Treat follow-ups such as "provide this as a Word document," "use this template," or "fill this out too" as continuation of the same proposal workflow. Reuse the established source inventory, response requirements, company context, and approved draft language.

## Output contract

Return:

1. completed response artifact or artifacts
2. concise submission-readiness summary
3. assumptions and user-confirmation items
4. missing evidence or source files
5. final compliance and formatting checks

Keep the handoff, missing evidence, and internal review notes separate from government-facing copy. A review draft is not prepared for submission while material facts or applicable final-file checks remain unresolved. Report only checks actually performed; drafting or generating a file does not establish submission or receipt.

For advisory-only asks, return a prioritized response strategy and section outline rather than forcing a full document.

## Boundary rules

- Use `govtribe-capture-workflows` when the user is still deciding whether or how to pursue the opportunity.
- Use `govtribe-pricing-data` when the unresolved issue is primarily staffing, rates, FTEs, wrap assumptions, or price evidence.
- A request to extract one fact from a document is file retrieval, not this workflow.
- A generic solicitation summary is not enough when the user requested a completed response or populated template.
