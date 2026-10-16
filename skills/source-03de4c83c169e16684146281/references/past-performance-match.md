---
title: Past Performance Match
description: How to assess whether a target company's past performance aligns to a specific federal contract or grant requirement.
---

# Past Performance Match

Use this reference when the user wants defensible past-performance references for a specific company and a specific contract, grant, or file-based requirement.

## Goal
- Resolve the company and the target requirement, recover the strongest comparable past performance, and write a defensible reference memo that explains the most important gaps or risks.
- Keep the answer focused on evidence-backed comparability, not on generic capability marketing.
- Use `assets/past-performance-reference-memo-template.md` from the skill root for document-style outputs.
- Before delivering a customer-facing memo or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).

## Workflow

### 1. Resolve the target company first
- Resolve the company with `Search_Vendors` whenever the input maps cleanly to a vendor record.
- Reuse vendor identity, classifications, certifications, and parent-child context only when they materially affect interpretation.
- If the company does not resolve cleanly enough to search, ask for the minimum missing detail and stop.

### 2. Resolve the target requirement into the best available surface
- Contract path: resolve the opportunity with `Search_Federal_Contract_Opportunities` and keep its agency, NAICS, PSC, set-aside, vehicle, timing, and scope language.
- Grant path: resolve the opportunity or program with `Search_Federal_Grant_Opportunities` or `Search_Federal_Grant_Programs` and keep its agency, program, assistance-type, timing, and scope language.
- File-first path: if the requirement is primarily an uploaded artifact, extract the requirement from user files before constructing award searches.
- If the requirement remains too vague, ask for the minimum missing detail and stop.

### 3. Use file evidence explicitly
- Read [Prior User File Context](./prior-user-file-context.md) before searching user files for company-provided past performance, capability statements, proposal excerpts, or uploaded requirement files.
- Use `Search_User_Files` only when those files materially improve the requirement basis or internal reference story.
- If the resolved opportunity exposes `government_files`, use `Search_Government_Files` before final scoring.
- Reuse `content_snippet` first.
- When exact file language materially improves requirement extraction, follow the bundled [vector-store retrieval guide](./govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, then `Search_Vector_Store`, and cite returned source metadata through the host's native citation format.

### 4. Start with company-constrained award retrieval
- Contract path: use `Search_Federal_Contract_Awards` with `vendor_ids` plus the strongest opportunity-derived agency, classification, set-aside, vehicle, date, value, and place filters.
- Grant path: use `Search_Federal_Grant_Awards` with `vendor_ids` plus the strongest program, agency, assistance-type, date, value, and place filters.
- When the resolved opportunity exposes direct lineage such as `federal_meta_opportunity_id`, use that before broader comparability logic.
- Request explicit row fields needed for scope, timing, value, customer, and lineage interpretation.

### 5. Broaden only after the direct pass
- If the company-constrained cohort is thin or vague, run one seeded `similar_filter` recovery pass from the resolved opportunity while keeping `vendor_ids` and the strongest structural filters in place.
- Use `search_mode: "semantic"` only after the direct pass and keep the strongest requirement-derived filters in place.
- Do not let semantic broadening replace the company-constrained award pass.

### 6. Compare, score, and trim
- Score candidate references on scope overlap, customer overlap, classification overlap, contract or assistance structure, operational environment, value band, recency, and requirement text alignment.
- Use file evidence to sharpen the requirement side, not to replace award-side matching.
- Exclude weak keyword-adjacent work, mismatched agencies, and records that only partly resemble the requirement.
- Normalize vendor identity only when legal-entity or parent-child context materially affects the interpretation.
- Select an anchor reference first, then decide which references are supporting evidence and which should be withheld or reserved.
- Treat score as a defensibility aid, not the memo itself. Do not let a matching table replace the argument.
- If the gap analysis surfaces requirement dimensions the company cannot defensibly cover alone, use `references/team-on-an-opportunity.md` to find a partner whose past performance closes the gap.

## Output contract
- Start with a reference decision that states match posture, recommended use, anchor reference, main proof point, main limitation, and confidence.
- Keep decision-table cells short enough to render cleanly; put detailed proof in the anchor reference profile instead.
- Include a requirement basis section that names the concrete requirement dimensions the references must prove.
- Use a short bulleted reference-set index, not a matching table. Include the anchor and the most important support reference only; move reserve, weak, or do-not-use references into prose.
- Write an anchor reference profile in prose with evidence basis, why it is defensible, limits to disclose, and how to frame it.
- Separate supporting references from the anchor so weaker proof points do not dilute the strongest story.
- Include gap/risk assessment and evidence traceability so a reviewer can see which requirement and award facts support the conclusion.
- Make the scoring rationale explicit for the best references and explicit about meaningful gaps, but keep long analysis out of table cells.
- If there is not enough evidence for a defensible match, say so clearly instead of stretching the comparison.
- Validate full requirement-to-reference match memos before finalizing. A requested evidence-collection brief without a target requirement instead uses source-inventory and document contract checks; preserve its actual evidence count and concise owner actions. Full match-memo section/count minimums do not apply to that distinct deliverable.
- For a full match memo, run:
  `python3 scripts/validate_past_performance_match_memo.py path/to/past_performance_match.md`
