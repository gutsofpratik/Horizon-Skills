---
title: Find Federal Recompete Opportunities
description: How to find expiring awards, IDVs, or vehicles that look like likely follow-on federal work.
---

# Find Federal Recompete Opportunities

Use this reference when the user wants likely federal recompetes or expiring follow-on work, either from a broad market scope or from a specific seed record.

## Goal
- Resolve the target scope, identify lifecycle records nearing meaningful end dates, and rank only the records that look credibly likely to produce follow-on action.
- Keep lifecycle semantics explicit. Do not treat every expiring record as a likely recompete.

## Workflow

### 1. Resolve the scope and classify it
- Resolve vendors, agencies, classifications, and identifiers that materially improve filtering.
- If the user supplied a specific award, IDV, or vehicle, classify it as a seed record.
- If the user supplied a broader vendor, agency, NAICS, PSC, or work area, treat it as a market scope.
- If the scope is too vague to search credibly, ask for the minimum missing detail and stop. Prefer `Show_Question_Flow` or `Show_Option_List` when the missing scope choice is bounded and structured.

### 2. Choose the lifecycle retrieval path
- Award path: use `Search_Federal_Contract_Awards` with `ultimate_completion_date_range`.
- IDV path: use `Search_Federal_Contract_IDVs` with `last_date_to_order_range`.
- Vehicle path: use `Search_Federal_Contract_Vehicles` with `last_date_to_order_range`.
- Use the strongest available vendor, agency, classification, type, and set-aside filters in all cases.

### 3. Use aggregation only when the cohort is broad
- Run an aggregation-only market-sizing pass only when the scope is broad enough that concentration, dominant awardees, vehicles, categories, or set-aside posture materially improve later review.
- Skip the aggregation branch when the workflow is obviously narrow or seed-record driven.
- Treat aggregation results only as market-shape evidence, not as proof that any specific record is a likely recompete.

### 4. Always run a row-level lifecycle pass
- Pull rows for awards, IDVs, or vehicles using the same stable base filters as the aggregation pass when one was used.
- Do not assume the first page is enough.
- If the workflow began from a seed record, keep the seed for context but exclude it from the discovery set unless the user explicitly asked for a one-record evaluation.

### 5. Broaden only after the direct lifecycle pass
- If the search began from a strong seed record, prefer one same-family `similar_filter` widening pass before generic semantic expansion.
- Use `search_mode: "semantic"` only after the direct pass and keep the strongest lifecycle, agency, classification, type, and set-aside filters in place.
- Do not use cross-dataset similarity jumps.

### 6. Pull transactions only when they materially sharpen lifecycle interpretation
- Use `Search_Federal_Transactions` only after awards, IDVs, or vehicles are identified and recent modification activity matters to likely follow-on interpretation.
- Treat transaction rows as supporting lifecycle evidence, not as the primary search surface.

### 7. Judge likely follow-on quality, then rank
- Use returned descriptions, summaries, lineage fields, task orders, blanket purchase agreements, and supporting transaction evidence to judge whether the work looks ongoing, recurring, or likely to be recompeted.
- Exclude records that are already effectively closed out, weakly relevant, structurally mismatched, or only supported by keyword overlap.
- Rank the survivors with explicit priority labels and lower confidence if cleanup materially reshapes the ranking.

## Output contract
- Return a short scope summary, a concise search approach, an optional market-size or concentration summary when aggregation was used, a ranked likely-recompetes table, a short exclusion section, and confidence.
- Prefer `Show_Stats_Display` for KPI summaries.
- Use `Show_Chart` when the market-shape evidence fits a standard inline `trend`, `comparison`, or `leaderboard`.
- When the visual needs long labels, source notes, or presentation polish, use the host's provider-neutral document or presentation capability. If it is unavailable, return the validated Markdown table plus chart-ready rows and state that a polished rendering was not produced.
- If the search began from a seed record, identify the seed clearly and do not include it in the ranked table unless the user explicitly asked for that.
- If no credible likely recompetes remain after review, say so clearly and stop.
