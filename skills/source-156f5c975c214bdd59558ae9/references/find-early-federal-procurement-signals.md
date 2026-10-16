---
title: Find Early Federal Procurement Signals
description: How to surface expiring awards, forecasts, early notices, active solicitations, and corroborating budget or news signals for a federal market slice.
---

# Find Early Federal Procurement Signals

Use this reference when the user wants early federal demand signals before a requirement matures into a fully active solicitation.

## Goal
- Resolve the target scope, then surface distinct evidence buckets:
  - expiring awards, IDVs, or vehicles
  - federal forecasts
  - early notices
  - active solicitations
  - corroborating budget, web, or government-related news signals
- Keep stage progression explicit instead of collapsing everything into one undifferentiated list.

## Workflow

### 1. Resolve the target scope first
- Normalize the topic, capability, agency, NAICS, PSC, or related seed record into a search-ready scope.
- Resolve agencies and classifications into reusable IDs when they materially improve filtering.
- Keep the default windows bounded. Use the next 12 to 24 months for lifecycle signals and shorter recent windows for notices, budget signals, and news.
- If the scope is too vague to search well, ask for the minimum missing detail and stop.

### 2. Run the lifecycle pass first
- Use `Search_Federal_Contract_Awards` with `ultimate_completion_date_range` to find awards expiring in the next 12 to 24 months.
- Use `Search_Federal_Contract_IDVs` and `Search_Federal_Contract_Vehicles` with `last_date_to_order_range` to find expiring instruments in the same window.
- Carry the strongest agency, office, NAICS, PSC, vendor, vehicle, or IDV filters into this pass.
- Treat expiring lifecycle records as lead indicators, not as proof that near-term demand already exists.

### 3. Run the forecast pass second
- Use `Search_Federal_Forecasts` as the formal planning surface.
- Start with an aggregation-first view when the slice is broad, then pull rows with release timing, agency context, set-aside posture, and contacts.
- Use the forecast pass to understand formal planned demand before looking at notices.

### 4. Run the early-notice pass third
- Use `Search_Federal_Contract_Opportunities` with early-stage notice types such as `Pre-Solicitation` and `Special Notice`.
- Carry concrete topic, agency, NAICS, PSC, and requirement language into this pass.
- Keep this pass future-facing or very recent. When notice rows expose due dates, prefer future due dates or notices that closed within roughly the last 6 months.
- Use `posted_date_histogram`, `top_opportunity_types_by_doc_count`, `top_opportunity_states_by_doc_count`, and `top_federal_contract_vehicles_by_doc_count` when a broad early-notice cohort needs posted-month volume, lifecycle mix, or vehicle concentration before row review.
- Exclude stale early notices that are no longer informative.
- Treat RFI or sources-sought style asks as query language, not as a guaranteed dedicated notice enum.

### 5. Run the active-solicitation pass fourth
- Use `Search_Federal_Contract_Opportunities` again with `Solicitation` plus a future-facing due-date filter.
- Use `due_date_histogram`, `top_opportunity_states_by_doc_count`, `top_opportunity_types_by_doc_count`, and `top_federal_contract_vehicles_by_doc_count` when the user needs active solicitations by due month, status, type, or vehicle concentration.
- Use this pass only to show active demand that appears to belong to the same market slice.

### 6. Run the budget and news pass fifth
- Use `Search_Government_Related_News_Articles` over a recent window with the strongest topic, agency, NAICS, PSC, or requirement terms.
- Use the host's provider-neutral web-browsing or search capability for official budget, appropriations, and planning pages that signal funded or prioritized demand.
- Start with these shared source lists:
  - [Federal Budget Data](./federal-budget-data.md)
  - [State Budget Data](./state-budget-data.md)
- Federal budget sites to inspect:
  - OMB and President's Budget materials
  - agency congressional budget justifications, budget office pages, and CFO pages
  - House and Senate appropriations bills, reports, and explanatory statements
  - agency acquisition forecasts, strategic plans, and IT or capital planning pages
- State budget sites when the workflow expands into adjacent state or comparative signals:
  - governor budget office or OMB pages
  - legislative appropriations or fiscal committee pages
  - statewide capital budget or capital improvement plan pages
  - agency budget request and strategic planning pages
- Treat budget, web, and news results as corroborating context. Do not let them outweigh forecasts, notices, solicitations, or expiring lifecycle records.
- If web browsing is unavailable, use the bundled official source lists, GovTribe forecasts and news, and the evidence already retrieved. Label unverified budget context, provide the relevant official source links, and request a supported document export only when the missing budget evidence would materially change the conclusion.

### 7. Use stage-progression recovery before generic semantic broadening
- If one stage is strong and another stage is unexpectedly thin, prefer one same-family `similar_filter` recovery pass before a broad semantic pass.
- Only after that should you use `search_mode: "semantic"` for conceptual or synonym-heavy topics.
- Keep structural filters in place and do not let semantic expansion flatten stage distinctions.

### 8. Dedupe and stage the findings
- Keep expiring lifecycle records, forecasts, early notices, active solicitations, budget or web signals, and news in separate buckets.
- If multiple records appear to describe the same requirement, keep the stage progression explicit rather than collapsing the records into one row.
- Remove weak or off-topic news and loose keyword matches from the final set.

## Output contract
- Return a short scope summary, a concise search approach, a stage-by-stage signal summary, compact tables for each populated stage, key progression notes, risks or gaps, and confidence.
- Keep the stage labels explicit:
  - `Expiring Award / IDV / Vehicle`
  - `Forecast`
  - `Pre-Solicitation`
  - `Special Notice / RFI / Sources Sought`
  - `Active Solicitation`
  - `Budget / Funding Signal`
  - `Government-Related News`
- If one stage is empty, say so clearly instead of implying demand exists at that stage.
