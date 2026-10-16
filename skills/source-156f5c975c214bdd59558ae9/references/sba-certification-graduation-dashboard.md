---
title: SBA Certification Graduation Dashboard
description: How to build a scoped certification-expiration exposure view for awards and IDVs using a selected SBA certification date.
---

# SBA Certification Graduation Dashboard

Use this reference when the user wants a scoped exposure analysis for awards and IDVs whose lifecycle extends beyond a selected SBA certification expiration date.

## Goal
- Apply one shared scope bundle to awards and IDVs, compute `gap_days` between lifecycle and the selected certification expiration date, and surface the strongest vendor and record-level exposures.
- Keep awards and IDVs separate throughout the workflow and the output.

## Workflow

### 1. Choose the certification track first
- If the user names a certification date explicitly, use it.
- If the user says only `SBA certification`, prefer `Show_Question_Flow` or `Show_Option_List` to collect which certification date should anchor the analysis before searching.
- Supported certification tracks for awards and IDVs:
  - 8(a): filter awards/IDVs with `vendor_sba_8a_expiration_date_range`; retrieve vendor rows with `sba_cert_8a_expiration_date`
  - 8(a) Joint Venture: filter awards/IDVs with `vendor_sba_8a_joint_venture_expiration_date_range`; retrieve vendor rows with `sba_cert_8a_joint_venture_expiration_date`
  - HUBZone: filter awards/IDVs with `vendor_sba_hubzone_expiration_date_range`; retrieve vendor rows with `sba_cert_hubzone_expiration_date`
  - Small Disadvantaged Business: filter awards/IDVs with `vendor_sba_small_disadvantaged_business_expiration_date_range`; retrieve vendor rows with `sba_cert_small_disadvantaged_business_expiration_date`
- Award and IDV rows do not return vendor certification date fields directly. After retrieving award/IDV rows, use `awardee.govtribe_id` values to call `Search_Vendors` and retrieve the selected vendor certification field.
- If the user says only `small`, use the same interactive input pattern to confirm whether they mean the small disadvantaged business expiration date before searching.
- Use one certification track per run unless the user explicitly wants a comparison.
- Default the certification and lifecycle windows to the next 12 months unless the user clearly requested a different defensible shared window.

### 2. Build one shared scope bundle
- Convert the user scope into the narrowest defensible bundle you can apply symmetrically to both datasets.
- If a requested filter cannot be applied cleanly to both awards and IDVs, say so clearly and prefer `Show_Question_Flow` or `Show_Option_List` for the scope clarification before searching.

### 3. Remember the dataset-specific lifecycle fields
- Awards:
  - filter with `ultimate_completion_date_range`
  - display `ultimate_completion_date`
  - output `set_aside_type`
- IDVs:
  - filter with `last_date_to_order_range`
  - display `last_date_to_order`
  - output `set_aside`
- Do not assume the two datasets share interchangeable lifecycle or set-aside field names.

### 4. Run count and aggregation passes first
- Use `Search_Federal_Contract_Awards` with the shared scope bundle, the award lifecycle window, and the selected certification filter.
- Use `Search_Federal_Contract_IDVs` with the shared scope bundle, the IDV lifecycle window, and the selected certification filter.
- Use aggregation-only passes to understand cohort size, dominant agencies, set-aside posture, vehicles, and whether the pool is too broad to review defensibly.
- If the cohort is too large, ask the user to de-scope before row retrieval, preferably with a bounded interactive choice when the narrowing options are clear.

### 5. Pull rows and compute `gap_days`
- Retrieve award rows sorted by `ultimate_completion_date`.
- Retrieve IDV rows sorted by `last_date_to_order`.
- Exclude rows missing the lifecycle date, `awardee.govtribe_id`, or the selected certification date on the joined vendor row.
- Compute `gap_days` from the award/IDV lifecycle date and the joined vendor certification date:
  - positive: lifecycle extends past certification expiration
  - zero or negative: work ends on or before certification expiration

### 6. Rank and trim
- Rank rows by `gap_days` descending, then by value.
- Keep awards and IDVs in separate ranked sections.
- Add a set-aside alignment label using returned text only.
- For IDVs, flag MAS, FSS, GWAC, OASIS, or similar shared-vehicle ceilings and avoid treating those ceilings as simple comparable exposure totals.
- Lower confidence when the remaining cohort is sparse, MAS-heavy, dependent on ambiguous parent-child identity, or mixes multiple certification interpretations.

## Output contract
- Return a certification-track and scope summary, a concise search approach, a cohort overview, separate awards and IDV exposure views, key patterns, risks or gaps, and confidence.
- Prefer `Show_Stats_Display` for the cohort overview.
- Use `Show_Chart` for standard inline exposure distributions, comparisons, or leaderboards.
- When the exposure view needs long labels, source notes, or presentation polish, use the host's provider-neutral document or presentation capability. If it is unavailable, return the validated Markdown table plus chart-ready rows and state that a polished rendering was not produced.
- Keep awards and IDVs separate throughout the answer.
- If the user explicitly wants multiple certification tracks compared, keep each certification in a separate section or table.
- Do not turn the result into a JSON payload or second output format unless the user explicitly asks for a file deliverable.
