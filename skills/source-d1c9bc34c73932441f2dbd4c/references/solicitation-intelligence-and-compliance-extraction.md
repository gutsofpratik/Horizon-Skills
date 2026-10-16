# Solicitation Intelligence and Compliance Extraction

## Overview
- Use this workflow when the user wants an RFP, solicitation, amendment, or source package read for requirements, deadlines, evaluation criteria, submission instructions, and compliance risks.
- Stay in this workflow when the expected output is extraction, interpretation, risk triage, and next actions, not a full proposal artifact.
- Prefer concise, source-backed guidance that helps a proposal or capture team decide what matters next.
- If the user asks for a workbook, requirement matrix, compliance matrix, or Section L / Section M crosswalk artifact, switch to [Build Proposal Control Workbook](./build-proposal-control-workbook.md).
- If the user asks for a writer-facing outline, storyboard, skeleton, or drafting package, switch to [Build Annotated Proposal Outline](./build-annotated-proposal-outline.md).

## Inputs to resolve
Resolve as many of these inputs as are available from the request, GovTribe opportunity context, government files, user files, and conversation context. Do not block if some are missing.
- Solicitation, RFP, RFQ, RFI, notice, task-order request, grant package, or bid package
- Amendments, conformed solicitation files, Q&A, addenda, or revised attachments
- Attachments, exhibits, PWS, SOW, SOO, CDRLs, referenced standards, pricing templates, forms, certifications, and reps and certs
- GovTribe opportunity metadata, notice history, source links, file metadata, and relevant agency or jurisdiction context
- User-provided business context, deadlines, priority questions, or known compliance concerns

If critical source files are missing, produce a partial extraction, label the missing files, and explain which conclusions depend on those missing sources.

## Source priority
Use the strongest controlling source available:

1. Latest conformed solicitation or latest full solicitation package.
2. Amendments, Q&A, addenda, and official clarifications that modify the solicitation.
3. Attachments, exhibits, forms, pricing templates, PWS, SOW, SOO, CDRLs, referenced standards, and submission portals or instructions.
4. GovTribe opportunity metadata, notice history, file metadata, and surrounding context.
5. User-provided assumptions or business context.

When sources conflict, prefer the latest controlling source and call out the conflict. Do not treat GovTribe metadata or snippets as a substitute for exact solicitation language when compliance depends on wording.

Use prior user files only when the user asks to compare against earlier proposal work, reuse a prior format, or incorporate company-specific reusable material. Read [Prior User File Context](./prior-user-file-context.md) before searching prior files.

## Retrieval guidance
- Preserve the resolved target, provided source files and requested source scope. For needed record lookup or refresh, select the tool by established target type: `Search_Federal_Contract_Opportunities` for federal contract opportunities, `Search_State_And_Local_Contract_Opportunities` for state/local contract opportunities, `Search_Federal_Grant_Opportunities` for federal grant opportunities, or `Search_Pursuits` for pursuits. Use `Search_GovTribe` when the type remains unresolved; a solicitation number, notice ID, title or URL alone does not establish a federal-contract type. Use `Search_Government_Files` and `Search_User_Files` to build the source inventory.
- Use snippets only for triage or source selection. If a snippet indicates that exact wording matters, retrieve the file text.
- When `content_snippet`, metadata, or summarized context is not enough, use [Vector-Store Content Retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until the requested files are ready, then use focused `Search_Vector_Store` queries.
- Use the external host's native citation format for source metadata returned with retrieved passages.
- When vector retrieval skips pricing schedules, spreadsheet workbooks, CSV/TSV files, CLIN tables, budget templates, or staffing matrices, use the host's attachment or spreadsheet capability. If none is available, disclose the coverage gap, return a labeled Markdown or CSV partial result, and request a supported export only when the skipped content materially changes the answer.
- Use `Documentation` for current MCP schemas, parameters, response fields, or freshness-sensitive behavior; use the bundled `govtribe-docs-*.md` references for stable guidance.
- Preserve exact language for mandatory requirements, evaluation criteria, submission instructions, page limits, forms, certifications, set-aside or access constraints, and deadline rules.

## Extraction targets
Capture the solicitation intelligence needed for compliance triage:
- Deadlines, time zones, question dates, site visit dates, submission dates, and amendment acknowledgement timing
- Submission method, portal, delivery address, file naming, packaging, volume structure, signatures, copies, and format controls
- Section L equivalents, instructions to offerors, required response content, mandatory attachments, and certifications
- Section M equivalents, evaluation factors, subfactors, relative importance, price or cost treatment, past performance treatment, pass/fail criteria, adjectival or point-scored criteria, and discriminator language
- Work requirements from PWS, SOW, SOO, statement of need, technical requirements, deliverables, and performance standards
- Special contract requirements, representations, certifications, and SAM registration or reps and certs currency requirements
- Pricing instructions, CLINs, cost elements, pricing templates, basis of award, options, and required price narratives
- Page limits, font, spacing, margin, file size, redaction, branding, table, graphics, and appendix rules
- Forms, representations, certifications, security, clearance, facility, small-business, set-aside, vehicle, registration, and access constraints
- Proposal risks, ambiguities, missing files, conflicting instructions, unstated assumptions, and likely Q&A candidates

## Amendment and Q&A deltas
When amendments, addenda, revised attachments, or Q&A are present:
- Identify changed deadlines, submission instructions, pricing templates, scope requirements, evaluation criteria, page limits, attachments, and forms.
- Distinguish added, removed, replaced, and clarified requirements.
- Flag whether each change affects compliance, pricing, schedule, review strategy, or proposal content.
- Avoid keeping stale pre-amendment language as the controlling rule unless the later source explicitly preserves it.
- If the amendment set appears incomplete, say which amendment or Q&A files are missing before drawing final conclusions.

## Procedure

### 1) Build the source inventory
- List every source reviewed, including title or filename, source type, date or amendment number when available, and whether full text or only metadata/snippets were available.
- Identify the controlling source package and any missing or partial files.
- Separate government-provided source files from GovTribe metadata and user-provided context.
- Do not stop at Section L and Section M when the package contains work requirements, special contract requirements, representations, certifications, attachments, or referenced standards elsewhere.

### 2) Extract the compliance-critical facts
- Pull deadlines, submission controls, Section L equivalents, Section M equivalents, work requirements, deliverables, pricing instructions, page limits, forms, certifications, and access constraints.
- Preserve exact source language when a missed word could change compliance.
- Use concise interpretation only after the exact requirement or evaluation language is clear.
- Assign stable requirement IDs in any table-like output so later workbook, outline, Q&A, and review work can refer back to the same extracted item.

### 3) Triage risks and gaps
- Flag preventable compliance failures first, such as late submission, missing forms, page-limit violations, unacknowledged amendments, missing pricing template entries, or mandatory certifications.
- Flag ambiguity, source conflicts, and missing files separately from confirmed requirements.
- Recommend Q&A items only when the source ambiguity materially affects compliance, price, schedule, or proposal strategy.
- Flag unresolved solicitation defects, restrictive language, missing provisions, ambiguous evaluation factors, or conflicting instructions early for customer review, Q&A, or legal counsel as appropriate.

### 4) Decide whether to hand off
- Stay in this workflow when the user needs an executive readout, compliance watchlist, extracted requirements, amendment impact summary, or next actions.
- Switch to [Build Proposal Control Workbook](./build-proposal-control-workbook.md) when the user needs a workbook, requirement matrix, compliance matrix, Section L / Section M crosswalk, submission tracker, or spreadsheet artifact.
- Switch to [Build Annotated Proposal Outline](./build-annotated-proposal-outline.md) when the user needs a writer-facing outline, storyboard, proposal skeleton, work package, or drafting package.

## Default output
Return a concise response with these sections:

1. `Executive Summary`: What the solicitation requires, what matters most, and the strongest compliance risks.
2. `Compliance Watchlist`: High-risk deadlines, mandatory submissions, file/package controls, amendment acknowledgements, forms, certifications, and missing-source risks.
3. `Requirement and Evaluation Table`: A compact table with requirement ID, source citation, requirement or evaluation language, proposal implication, risk level, and next action.
4. `Amendment and Q&A Changes`: Changed deadlines, changed requirements, added or removed attachments, clarifications, and compliance impact.
5. `Source Coverage`: Sources reviewed, sources only partially available, missing files, and assumptions.
6. `Next Actions`: Near-term proposal, pricing, Q&A, source retrieval, or artifact handoff actions.

If the source package is large, summarize the most important rows in the response and offer to continue into a workbook or outline only when the user asks for that artifact.

## Output rules
- Be source-backed and compliance-focused.
- Use exact solicitation language where wording controls compliance.
- Keep interpretation separate from source language.
- Label partial or missing-source conclusions clearly.
- Do not invent deadlines, requirements, evaluation weights, forms, or instructions that are not supported by the sources.
- Do not create a workbook, matrix artifact, or outline by default.

## Common failure modes to avoid
- Producing an oversized workbook when the user asked for extraction and triage
- Relying on snippets when exact Section L, Section M, amendment, or submission wording is needed
- Treating GovTribe metadata as controlling solicitation language
- Missing amendment-driven deadline or attachment changes
- Mixing confirmed source requirements with assumptions
- Hiding missing files or partial-source coverage
- Treating a successful vector-store read of PDFs or documents as complete package coverage when spreadsheet-like pricing files were skipped
- Failing to hand off when the user explicitly asks for a matrix, workbook, crosswalk, outline, or storyboard
