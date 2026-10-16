---
title: Relevant Opportunities
description: How to rank open federal contract or grant opportunities against a target company, solution, or capability profile.
---

# Relevant Opportunities

Use this reference when the user wants a ranked short list of open federal contract or grant opportunities for a target company, solution, or capability profile.

## Goal
- Resolve the target profile, extract reusable signals, search the open market, and rank only meaningfully relevant opportunities.
- Keep the result capture-oriented. Exclude broad market scans, buyer-expansion analysis, and single-record deep dives.
- Before delivering a customer-facing ranked list, workbook, or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).

## Workflow

### 1. Resolve the target profile first
- Resolve a vendor with `Search_Vendors` when the input maps cleanly to a company.
- Reuse company identity, offerings, customer alignment, classifications, certifications, geography, and recent relevant awards when they materially sharpen fit.
- If the target is only a website or plain-language profile, work from user-provided text and do not invent external website retrieval.
- If the target is too vague to search well, ask for the minimum missing detail and stop. Prefer `Show_Question_Flow` when the missing profile fields are a small structured set.

### 2. Pull prior user-file evidence only when it sharpens the profile
- Read [Prior User File Context](./prior-user-file-context.md) before searching user files.
- Use `Search_User_Files` only when capability statements, one-pagers, uploaded target material, prior capture briefs, or reusable company evidence materially sharpen the fit profile.
- Reuse `content_snippet` first.
- When file content is necessary to capture exact mission language, delivery model, or technical phrases, follow the bundled [vector-store retrieval guide](./govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, then `Search_Vector_Store`, and cite returned source metadata through the host's native citation format.

### 3. Resolve structured constraints before broad retrieval
- Resolve user-supplied agencies, NAICS, PSC, grant programs, geography, due-date, and eligibility constraints into reusable IDs when they materially tighten the market slice.
- Keep contract and grant filters separate instead of forcing one mixed search surface.

### 4. Start with keyword and filter-first open-opportunity retrieval
- Contract path: use `Search_Federal_Contract_Opportunities` with the strongest agency, NAICS, PSC, set-aside, location, due-date, and opportunity-type filters.
- Grant path: use `Search_Federal_Grant_Opportunities` with the strongest agency, program, funding-instrument, eligibility, and due-date filters.
- Request explicit row fields needed for scope, timing, agency, classification, and opportunity text.
- If the user asked for only active or open results, make that an explicit filter decision.

### 5. Use aggregation only when the scoped cohort is still broad
- Run an aggregation-first pass only when market sizing, concentration, or narrowing materially improves the ranking.
- Use cohort-shape aggregations to understand dominant agencies, classifications, programs, locations, and set-aside posture before row review.

### 6. Broaden only after the direct pass
- If the filter-first cohort is thin or repetitive, run one seeded `similar_filter` pass from the strongest kept contract or grant opportunity before generic semantic broadening.
- Use `search_mode: "semantic"` only after the direct pass and keep the strongest structural filters in place.
- Do not let semantic expansion replace the keyword and filter-first pass.

### 7. Validate and rank the surviving opportunities
- Compare each candidate against direct scope fit, mission fit, delivery model, classification overlap, contract or funding structure, eligibility, geography, and due-date practicality.
- Use `Search_Federal_Contract_Awards` or `Search_Federal_Grant_Awards` only when incumbent, prior-delivery, or market validation materially changes the ranking.
- Exclude weak keyword matches, broad adjacent work, and opportunities that are only tenuously connected to the target.
- Keep only opportunities that are genuinely pursuit-worthy.
- For top-ranked opportunities where teaming is a credible pursuit posture, use `references/team-on-an-opportunity.md` to discover existing teaming interests and coordinate matches.

## Output contract
- Return a short target-profile summary, a compact search-approach note, a market-slice summary, a ranked opportunities table, a short rejection section, and confidence.
- Prefer `Show_Stats_Display` for KPI summaries.
- Use `Show_Chart` when the cohort view fits a standard inline `trend`, `comparison`, or `leaderboard`.
- If `Show_Chart` cannot support long labels, annotations, or presentation styling, use the host's provider-neutral chart capability. When no such capability exists, preserve the cohort as a labeled Markdown table and provide CSV or JSON companion data.
- Keep fit labels evidence-based and explain caveats on the top opportunities.
- If the evidence is too thin for a credible ranking, say so clearly instead of padding the list.
