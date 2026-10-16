---
title: Federal Buying Pattern Analysis
description: How to characterize how a federal buyer or buying lane actually buys a type of contract work.
---

# Federal Buying Pattern Analysis

Use this reference when the user wants to understand how a federal buyer or resolved buying lane behaves over time.

## Goal
- Resolve the market slice, ground it in a fixed last-24-month window, and characterize market structure from actual award behavior.
- Treat a federal buyer as a contracting agency, funding agency, named office or program, or contracting contact when that resolves cleanly to a buyer lane.
- Keep the answer focused on buying model, set-aside posture, value bands, concentration, and vehicle or IDV dependence.

## Workflow

### 1. Resolve the market slice first
- Resolve buyer names, offices, programs, or contacts into agency or office context when they materially sharpen the slice.
- Resolve the work dimension from user language, seed awards, IDVs, vehicles, contact context, returned award text, or repeated NAICS, PSC, vehicle, or IDV patterns in the cohort.
- Use NAICS, PSC, vehicle, or IDV filters once the work dimension is clear enough to narrow the lane.
- If the slice still resolves only to a very large department or agency with no work dimension, ask for narrower scope before market characterization.

### 2. Start with a historical award aggregation pass
- Use `Search_Federal_Contract_Awards` as the primary evidence surface.
- Keep stable award filters in place across later passes.
- Use aggregations to estimate market size, concentration, dominant agencies, set-aside posture, value bands, and whether vehicle concentration is strong enough to justify a dedicated parent-structure branch.

### 3. Follow with row-level award retrieval
- Use the same stable scope filters to pull representative award rows after the slice is narrowed by buyer plus work dimension, or by a stable office, vehicle, or IDV lane.
- Do not rely on agency-only row review for very large buyers.
- Do not assume the first page is representative.
- Tighten filters or rerun with a more representative sort if the first rows are dominated by outliers or weak lane matches.

### 4. Use vehicle or IDV structure only when it materially improves correctness
- Run `Search_Federal_Contract_IDVs` only when the award data cannot answer single-award vs multiple-award structure, parent-instrument dependence, or ordering behavior credibly.
- Run `Search_Federal_Contract_Vehicles` only when master-vehicle context materially improves the market characterization.
- Do not run both unless the evidence requires both.

### 5. Use a live-demand overlay only when it adds real value
- Use `Search_Federal_Contract_Opportunities` only when present-tense buying posture, set-aside shifts, or projection validation materially improve the answer.
- When the live-demand overlay is broad enough for rollups, use opportunity lifecycle aggregations to summarize posted-month signal volume, due-month workload, opportunity type or status mix, and vehicle concentration before choosing representative rows.
- Keep the live-demand overlay subordinate to the historical buying profile.
- If the live cohort is thin or empty, say so clearly instead of implying current demand exists.

### 6. Compare the recent 12 months against the prior 12 months
- Compare the most recent 12 months against the prior 12 months inside the fixed 24-month window.
- Call out only changes that materially affect the market characterization.
- Keep the same scope filters in both windows so the comparison stays valid.

### 7. Classify and trim
- Classify the lane using evidence-backed labels for buying model, award structure, set-aside posture, and concentration.
- Exclude cross-lane contamination, one-off outliers treated as the market, and thin live-demand evidence presented as projection.
- If the evidence is too sparse to characterize the market credibly, say so clearly and stop.

## Output contract
- Return a short buying-pattern summary, a concise search approach, a buying-pattern snapshot, core findings, optional vehicle or IDV findings, optional live-demand overlay, representative records, risks, and confidence.
- Use compact markdown tables for the buying-pattern snapshot and representative records.
- Use Mermaid only when concentration or trend evidence materially improves interpretation and the host can render it. Otherwise use a compact Markdown table or ordered comparison.
- Keep the live-demand overlay and any trend claim explicitly subordinate to the core historical award evidence.
