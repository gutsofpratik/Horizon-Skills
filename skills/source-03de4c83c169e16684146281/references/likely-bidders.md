---
title: Likely Bidders
description: How to identify likely bidders or recipients for a target federal, grant, or state and local opportunity.
---

# Likely Bidders

Use this reference when the user wants the most likely vendors or recipients for a specific federal contract, federal grant, or state and local opportunity.

## Goal
- Resolve the target opportunity, recover the strongest comparable historical awards, and rank likely bidders or recipients with explicit caveats.
- Use prior awards as the primary evidence surface. Do not substitute peer opportunities for bidder evidence.
- For a document-style deliverable, prefer the structure in `assets/likely-bidders-brief-template.md` from the skill root.
- Before delivering a customer-facing brief, bidder table, or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).

## Workflow

### 1. Resolve the target opportunity exactly
- Use the correct opportunity surface:
  - `Search_Federal_Contract_Opportunities`
  - `Search_Federal_Grant_Opportunities`
  - `Search_State_And_Local_Contract_Opportunities`
- Resolve reusable IDs for agencies, programs, taxonomies, states, and jurisdictions when they materially tighten later award searches.
- If the target does not resolve cleanly enough to one opportunity, ask for the minimum missing detail and stop. Prefer `Show_Question_Flow` or `Show_Option_List` when the remaining choice is bounded and structured.

### 2. Extract the strongest comparable signals
- Reuse title, agency or jurisdiction, description, NAICS, PSC, grant program, NIGP, UNSPSC, set-aside or eligibility constraints, vehicle or instrument type, value band, place, and due-date context.
- Keep contract, grant, and state/local paths separate instead of forcing one shared comparable-award workflow.

### 3. Start with filter-first historical award matching
- Contract path: use `Search_Federal_Contract_Awards` with direct thread linkage first when `federal_meta_opportunity_id` is available, then keep the strongest agency, NAICS, PSC, set-aside, vehicle, date, and value filters in place.
- Grant path: use `Search_Federal_Grant_Awards` with the strongest program, agency, assistance-type, date, value, and place filters.
- State and local path: use `Search_State_And_Local_Contract_Awards` with the most precise first-pass query built from exact identifiers, title phrases, scoped description terms, and the strongest geography or taxonomy filters.
- Use peer-opportunity similarity only to tighten later state and local award retrieval, not as bidder evidence by itself.

### 4. Run an aggregation pass before final ranking
- Use an aggregation-only pass on the comparable-award cohort to understand concentration, dominant awardees, vehicles, programs, taxonomies, and overall market shape.
- For state and local work, use opportunity aggregations only when active-solicitation market shape materially sharpens the state and local award interpretation.

### 5. Broaden only after the direct pass
- If a `similar_filter` branch already recovers enough comparable records, skip generic semantic broadening.
- Use `search_mode: "semantic"` only after the keyword and aggregation passes, and keep the strongest structural filters in place.
- If file content materially sharpens the target scope, use `Search_Government_Files` first. When snippets are not enough, follow the bundled [vector-store retrieval guide](./govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, then `Search_Vector_Store`, and cite returned source metadata through the host's native citation format.

### 6. Compare candidates and rank
- Score candidates on direct scope overlap, repeated wins, same agency or customer, same classification or program, same vehicle or assistance pattern, similar value range, recent relevant activity, and eligibility fit.
- Normalize awardees with `Search_Vendors` only when entity consolidation or parent-child structure materially affects the ranking.
- Exclude candidates that are only keyword-adjacent, structurally mismatched, or too thinly supported.
- If any ranked bidder is a credible teaming partner rather than a head-on competitor, use `references/team-on-an-opportunity.md` to discover whether they have already created a teaming interest on the opportunity.

## Output contract
- Return a short target-opportunity summary, a compact search-approach note, a comparable-market summary, a ranked likely-bidders table, a short exclusion section, and confidence.
- Make rendered briefs read like competitive intelligence memos, not raw ranking spreadsheets. Open with a competitive read that identifies the most likely bidder, field shape, concentration, access discriminator, confidence, and primary uncertainty.
- Prefer `Show_Stats_Display` for KPI summaries.
- Use `Show_Chart` when the comparable-market summary fits a standard inline `trend`, `comparison`, or `leaderboard`.
- If `Show_Chart` cannot support long labels, annotations, or presentation styling, use the host's provider-neutral chart capability. When no such capability exists, preserve the ranking as a labeled Markdown table and provide CSV or JSON companion data.
- Keep the rendered bidder ranking table narrow enough for portrait Markdown/PDF output. Prefer columns like `Rank`, `Bidder`, `Likelihood`, and `Why they are on the list`.
- Do not force key evidence, vehicle access, eligibility, caveats, and confidence into one wide ranking table. Put details in a separate bidder evidence digest with `Bidder`, `Strongest evidence`, and `Caveat / watch item`.
- Keep the target opportunity summary as prose or a short table. Avoid listing every opportunity field if it pushes the ranking below the fold.
- Include concise validation steps when final vehicle, set-aside, incumbent lineage, eligibility, or file evidence could materially change the ranking.
- Combine confidence and validation steps near the end of rendered briefs; avoid a standalone confidence section when it would create a sparse trailing PDF page.
- Put full aggregation data, row-level comparable awards, excluded candidates, scoring notes, and vendor-normalization details in companion CSV or JSON artifacts when needed.
- If companion artifact links create a trailing blank page in a rendered PDF, omit them from the rendered brief and provide them in the final response instead.
- Make concentration and caveats explicit on the strongest candidates.
- If the evidence is too thin for a credible ranking, say so clearly instead of padding the list.
