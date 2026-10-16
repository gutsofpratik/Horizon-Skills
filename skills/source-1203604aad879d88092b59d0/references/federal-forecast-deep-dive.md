---
title: Federal Forecast Deep Dive
description: How to exhaustively gather context for a federal forecast using exact agency and timing overlap, related opportunity and award discovery, incumbent and vehicle context, and contact-focused follow-up.
---

# Federal Forecast Deep Dive

Use this reference when the user wants a deep dive on a single federal forecast and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means loading the target, the exact agency-and-timing forecast neighborhood, the most relevant related opportunities and predecessor awards, any surfaced vehicle or incumbent context, and the most important open gaps.
- Prefer exact structured overlap through agency, contacts, timing, set-aside posture, and place of performance before semantic expansion.
- Prefer direct nested relationships already on the target before making extra search calls.
- If the target, linked agency, linked contacts, nearby forecast cohort, or the strongest related opportunity or award are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain what the forecast is, how likely it is to progress, what requirement lane it sits in, who likely holds adjacent or predecessor work, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `forecast_type`
  - `set_aside`
  - `estimated_solicitation_release_date`
  - `estimated_award_start_date`
  - `estimated_award_value`
  - `descriptions`
  - `updated_at`
  - `federal_agency`
  - `place_of_performance`
  - `points_of_contact`
  - `govtribe_ai_summary`
- If the target is not already in context, fetch it by exact GovTribe ID.

### 2. Reuse direct structured relationships and classify the forecast
- Use the target's direct relationships before starting broader searches:
  - `federal_agency`
  - `place_of_performance`
  - `points_of_contact`
- These direct fields often answer the first wave of context questions without extra search calls.
- Call out early which forecast lane you are in, because it changes the downstream search priority:
  - `Recompete`: prioritize predecessor awards, incumbents, and vehicle context.
  - `Exercise of Option`: prioritize the likely current award and transaction chronology.
  - `New Requirement`: prioritize adjacent forecasts, related opportunities, and mission-lane analogs.
- Forecasts do not expose a federal-contract-opportunity-style exact notice-chain key on this LLM surface. Do not invent one.
- Forecasts also do not expose attached `government_files` here. Do not assume there are files to stage.

### 3. Build the exact agency-and-timing forecast neighborhood first
- Use `Search_Federal_Forecasts` with the exact `federal_agency_ids` from the target before semantic fan-out.
- Keep the search bounded around the target's `estimated_solicitation_release_date` and exclude the target forecast itself.
- If `points_of_contact`, `place_of_performance`, or `set_aside` are strong signals on the target, keep them in place for the first neighborhood pass.
- Use the neighborhood pass to answer:
  - whether this forecast sits in a recurring agency lane
  - whether nearby forecasts cluster around the same office, contact set, or timing window
  - whether the target looks isolated or part of a broader planned portfolio

### 4. Search for related opportunities and stage progression
- Forecasts do not currently expose an exact opportunity-linkage scalar on this surface, so use `similar_filter` on the target forecast after the exact agency-and-timing pass.
- Keep the strongest target constraints in place when they are available:
  - `federal_agency_ids`
  - `place_of_performance_ids`
  - `contact_ids`
  - likely `opportunity_types`
- If `estimated_solicitation_release_date` is near or past, prioritize `Pre-Solicitation`, `Special Notice`, and `Solicitation` results.
- Use the opportunity pass to answer:
  - whether the forecast appears to have progressed into a posted notice
  - whether the requirement looks reshaped, delayed, or quiet
  - whether a likely solicitation family or notice thread has emerged

### 5. Search for predecessor or adjacent awards and likely incumbents
- Use `Search_Federal_Contract_Awards` with `similar_filter={govtribe_type:"federal_forecast",govtribe_id:target.govtribe_id}` after the structured forecast pass.
- If the target has a clear `federal_agency`, keep the strongest matching agency filter in place when it improves precision.
- For `Recompete` and `Exercise of Option` forecasts, treat this as a high-priority step.
- Use the award pass to answer:
  - whether there is a likely predecessor award
  - who the likely incumbent vendor is
  - whether the work appears tied to a known IDV or vehicle
  - whether the set-aside and mission lane align with recent obligated history
- If a likely current award emerges and the question depends on option, extension, or mod chronology, use `Search_Federal_Transactions` on that award after you resolve it exactly.

### 6. Follow chain-up and vendor context only when surfaced
- If related opportunities or awards surface a `federal_contract_idv` or `federal_contract_vehicle`, fetch those exact parent records next.
- If likely predecessor awards surface an `awardee`, resolve that vendor exactly before widening to broader vendor history.
- If likely teammate or subcontract posture matters, use `Search_Federal_Contract_Sub_Awards` only after a strong predecessor award or incumbent vendor has been identified.
- Use this pass to answer:
  - whether the forecast is likely to stay on an existing vehicle
  - whether incumbency is concentrated or contested
  - whether vendor or teammate posture materially changes the capture picture

### 7. Resolve agency and contact context when it changes the answer
- Use `Search_Federal_Agencies` when you need a cleaner agency profile, acronym, or defense-versus-civilian framing than the nested target provides.
- Use `Search_Contacts` when the nested `points_of_contact` are thin and the question depends on richer contact context, role clarity, or contact-reference patterns.
- Use agency and contact expansion to answer:
  - which office appears to own the forecast
  - whether the same contacts appear repeatedly across related notices
  - whether outreach should center on program, contracting, or both

### 8. Use semantic mission fan-out only after the structured passes
- If exact agency-and-timing overlap plus the first related opportunity and award passes are thin, use semantic expansion.
- Good semantic fan-out targets are:
  - related forecasts
  - related federal contract opportunities
  - related federal contract awards
- Build the semantic query from the target's `name`, `govtribe_ai_summary`, and `descriptions`.
- Keep the strongest agency, set-aside, place-of-performance, and timing constraints in place when they still fit.
- Treat semantic results as analogs or mission-lane evidence, not proof of exact lineage.

### 9. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the target forecast
  - the most relevant nearby forecast cohort
  - the strongest related opportunities
  - the strongest predecessor or adjacent awards
  - any surfaced IDV, vehicle, or incumbent context
  - the most relevant agency or contact context
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly related, duplicative, or too far from the user's question.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_Federal_Forecasts`
```json
{
  "search_mode": "keyword",
  "federal_forecast_ids": [
    "<FEDERAL_FORECAST_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "forecast_type",
    "set_aside",
    "estimated_solicitation_release_date",
    "estimated_award_start_date",
    "estimated_award_value",
    "descriptions",
    "updated_at",
    "federal_agency",
    "place_of_performance",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "per_page": 1
}
```

Load nearby forecasts in the same agency-and-timing lane while excluding the target:
Tool: `Search_Federal_Forecasts`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "estimated_solicitation_release_date_range": {
    "from": "<TARGET_RELEASE_DATE_MINUS_180D>",
    "to": "<TARGET_RELEASE_DATE_PLUS_180D>"
  },
  "federal_forecast_ids": [
    "<FEDERAL_FORECAST_ID>"
  ],
  "federal_forecast_ids_operator": "not_in",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "forecast_type",
    "set_aside",
    "estimated_solicitation_release_date",
    "estimated_award_start_date",
    "updated_at",
    "federal_agency",
    "points_of_contact"
  ],
  "sort": {
    "key": "estimated_solicitation_release_date",
    "direction": "asc"
  },
  "per_page": 10
}
```

Search for related posted notices using the forecast as the semantic seed:
Tool: `Search_Federal_Contract_Opportunities`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "federal_forecast",
    "govtribe_id": "<FEDERAL_FORECAST_ID>"
  },
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "opportunity_types": [
    "Solicitation",
    "Pre-Solicitation",
    "Special Notice"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "opportunity_type",
    "opportunity_state",
    "part_of_mas",
    "set_aside_type",
    "posted_date",
    "due_date",
    "federal_meta_opportunity_id",
    "federal_contract_vehicle",
    "federal_agency",
    "points_of_contact"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Search for likely predecessor or adjacent awards using the forecast as the semantic seed:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "federal_forecast",
    "govtribe_id": "<FEDERAL_FORECAST_ID>"
  },
  "award_date_range": {
    "from": "now-5Y/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date",
    "dollars_obligated",
    "awardee",
    "parent_of_awardee",
    "federal_contract_idv",
    "federal_contract_vehicle",
    "funding_federal_agency",
    "contracting_federal_agency",
    "originating_federal_meta_opportunity_id",
    "originating_federal_contract_opportunity"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Resolve the most important public points of contact when the nested target rows are thin:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID_1>",
    "<CONTACT_ID_2>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "email",
    "phone",
    "title",
    "role",
    "organization",
    "parent_organization_details",
    "updated_at"
  ],
  "per_page": 10
}
```

Resolve a surfaced parent IDV exactly before making pricing or holder claims:
Tool: `Search_Federal_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "federal_contract_idv_ids": [
    "<FEDERAL_CONTRACT_IDV_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "contract_number",
    "name",
    "award_date",
    "last_date_to_order",
    "ceiling_value",
    "contract_type",
    "pricing_type",
    "solicitation_procedures",
    "extent_competed",
    "legislative_mandate",
    "multiple_or_single_award",
    "awardee",
    "parent_of_awardee",
    "federal_contract_vehicle",
    "price_lists",
    "originating_federal_meta_opportunity_id",
    "originating_federal_contract_opportunity"
  ],
  "per_page": 1
}
```
