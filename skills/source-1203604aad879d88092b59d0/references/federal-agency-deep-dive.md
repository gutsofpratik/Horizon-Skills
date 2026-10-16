---
title: Federal Agency Deep Dive
description: How to exhaustively gather context for a federal agency using exact agency-ID anchoring across federal contract and grant surfaces, obligations rollups, pipeline views, active vehicles, contracting personnel, and selective file retrieval for central linked notices.
---

# Federal Agency Deep Dive

Use this reference when the user wants a deep dive on a single federal agency and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means locking the exact agency scope, then using that exact agency ID to build the strongest contract spend, pipeline, active vehicle, contact, and grant context without drifting into unrelated agencies.
- For federal agencies, prefer aggregation-first analysis on each major surface and use row retrieval mainly to anchor the narrative with representative examples.
- Prefer exact agency-ID filtering across awards, opportunities, forecasts, IDVs, vehicles, grants, and contacts before semantic expansion.
- Prefer funding-agency views first when the user cares about owned demand, then rerun contracting-agency views when procurement execution or assisted acquisition behavior matters.
- If the target, recent award rollups, active pipeline, or top contacts are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain what the agency appears to buy or fund, which vendors and categories dominate, what the near-term pipeline looks like, which contract vehicles and contacts matter most, whether grant activity is material, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `alternate_name`
  - `acronym`
  - `defense_or_civilian`
  - `updated_at`
- If the target is not already in context, fetch it by exact GovTribe ID, exact quoted agency name, or exact quoted acronym.

### 2. Lock exact agency scope before cross-surface fan-out
- Treat the resolved target agency as the exact scope anchor for all downstream searches.
- The current agency LLM surface is intentionally thin. Do not assume it exposes parent or child hierarchy, mission detail, or acquisition-office structure directly.
- Do not silently roll the analysis up to a parent department or widen it across sibling agencies unless the user explicitly asks for department-level scope.
- If the contract-side story differs materially between `funding_federal_agency_ids` and `contracting_federal_agency_ids`, treat that as a real signal about assisted acquisition or procurement delegation, not as a contradiction.

### 3. Build the contract spend and market-structure view first
- Start with `Search_Federal_Contract_Awards` scoped by exact `funding_federal_agency_ids=[target.govtribe_id]`.
- Use an aggregation-first pass before pulling many rows.
- Use the funding-agency award pass to answer:
  - total obligations
  - top awardees
  - dominant NAICS and PSC lanes
  - set-aside posture
  - leading IDVs and vehicles
- If the question is about who buys on the agency's behalf or where issuance is delegated, rerun a complementary pass using `contracting_federal_agency_ids=[target.govtribe_id]`.
- After the aggregation pass, pull a modest recent-award sample so the narrative includes concrete flagship records.
- After the exact agency fetch, this spend rollup is usually a good parallel branch with pipeline and contact discovery.

### 4. Surface the active contract pipeline early
- Use `Search_Federal_Contract_Opportunities` with exact `federal_agency_ids=[target.govtribe_id]` for the live and recent notice view.
- Use `Search_Federal_Forecasts` with the same exact agency ID for planned requirements.
- Keep these passes bounded with sensible near-term windows:
  - opportunities: usually `due_date_range` over the next 6 to 12 months
  - forecasts: usually `estimated_solicitation_release_date_range` over the next 6 to 12 months
- Use the pipeline pass to answer:
  - which requirement lanes are active now
  - whether upcoming work matches historic spend lanes
  - whether set-aside posture or contact concentration is changing
- If contract opportunity or forecast results are very sparse, say that clearly instead of inferring a broad pipeline from thin evidence.

### 5. Map the active contract vehicle portfolio
- Use `Search_Federal_Contract_IDVs` with exact `funding_federal_agency_ids=[target.govtribe_id]` first.
- Focus on active or still-orderable instruments using `last_date_to_order_range` when the user cares about current access paths.
- Use the IDV pass to answer:
  - which vehicles or IDVs appear central to the agency's buying activity
  - whether the agency leans toward single-award or multiple-award structures
  - which awardees or holders dominate active portfolio access
- Use `Search_Federal_Contract_Vehicles` when the IDV and award evidence shows clear master-vehicle concentration or when the user explicitly asks about vehicle families.
- Treat vehicles as top-level structure and IDVs as agency-usable access paths. Do not collapse them into one layer.

### 6. Surface contracting personnel and office signals
- Use `Search_Contacts` with exact `federal_agency_ids=[target.govtribe_id]`.
- Favor public-signal reference types such as `pointOfContact` and `transactionContact` when the goal is contracting-personnel mapping rather than generic contact discovery.
- Use this pass to answer:
  - which contracting personnel or offices recur
  - whether the same people appear across awards, opportunities, forecasts, and files
  - whether certain contacts cluster around specific mission lanes or vehicles
- When a few contacts look especially central, use them to narrow follow-up award, opportunity, or forecast searches rather than broadening the whole agency view.

### 7. Add the grant footprint only when it is relevant or material
- Not every agency needs a full grant branch.
- Add it when:
  - the user explicitly asks about grants
  - the agency is visibly grant-active
  - the mission suggests grants are a meaningful channel
- Use `Search_Federal_Grant_Awards` with exact `funding_federal_agency_ids=[target.govtribe_id]` to measure grant spend and top programs.
- Use `Search_Federal_Grant_Programs` with exact `federal_agency_ids=[target.govtribe_id]` to understand recurring program structure.
- Use `Search_Federal_Grant_Opportunities` with exact `federal_agency_ids=[target.govtribe_id]` to understand active grant pipeline.
- Use the grant branch to answer:
  - whether grant activity is central or peripheral to the agency
  - which programs dominate
  - whether open grant opportunities line up with the agency's visible mission or funding activity categories

### 8. Pull representative anchor records and only then review files
- Once the main award, opportunity, forecast, IDV, vehicle, or grant-program passes identify the most central records, pull a small set of representative anchors.
- Good anchor candidates are:
  - 3 to 5 recent flagship contract awards
  - 3 to 5 central active opportunities or forecasts
  - 2 to 4 notable active IDVs
  - a few key grant programs or grant opportunities when the grant branch matters
- Do not default to file retrieval at the agency level.
- Only review files when a selected contract or grant opportunity appears central and its attached files are likely to contain material scope, requirement, or compliance detail.
- For those selected notices, preview exact `government_file_ids` with `Search_Government_Files` and use `content_snippet` first.
- If the snippet only suggests relevance, or the task depends on exact wording, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until ready, and call `Search_Vector_Store`. Cite returned source metadata with the external host's native citation format; for a material skipped file, use the host's attachment or spreadsheet capability or disclose the gap.

### 9. Use semantic expansion only after the exact agency-ID passes
- If the exact agency-ID view is still too thin, use bounded semantic expansion.
- Good semantic targets are:
  - related contract opportunities
  - related forecasts
  - related grant programs
  - peer agencies only when the user asks for comparison or white-space context
- Treat semantic results as adjacent-market evidence, not as direct agency lineage.
- Do not use semantic expansion to compensate for an unresolved agency-scope decision. Resolve the exact agency first.

### 10. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the target agency and exact scope decision
  - the strongest contract spend and market-structure signals
  - the near-term contract pipeline
  - the most important active IDVs or vehicles
  - the most relevant contracting personnel
  - the grant footprint when it is material
  - a few representative anchor records
  - any material file-derived findings from those anchor records
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly connected, duplicative, or outside the user's real scope.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_Federal_Agencies`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "alternate_name",
    "acronym",
    "defense_or_civilian",
    "updated_at"
  ],
  "per_page": 1
}
```

Resolve an agency by exact quoted name when only the label is known:
Tool: `Search_Federal_Agencies`
```json
{
  "query": "\"<FEDERAL_AGENCY_NAME>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "alternate_name",
    "acronym",
    "defense_or_civilian"
  ],
  "per_page": 5
}
```

Build a funding-agency contract spend rollup first:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "funding_federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_awardees_by_dollars_obligated",
    "top_funding_federal_agencies_by_dollars_obligated",
    "top_contracting_federal_agencies_by_dollars_obligated",
    "top_naics_codes_by_dollars_obligated",
    "top_psc_codes_by_dollars_obligated",
    "top_set_aside_types_by_dollars_obligated",
    "top_idvs_by_dollars_obligated",
    "top_federal_contract_vehicles_by_dollars_obligated",
    "top_transaction_points_of_contact_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Pull representative recent contract awards for the agency's funded work:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "funding_federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date",
    "dollars_obligated",
    "set_aside_type",
    "awardee",
    "contracting_federal_agency",
    "funding_federal_agency",
    "naics_category",
    "psc_category",
    "federal_contract_vehicle",
    "federal_contract_idv",
    "originating_federal_meta_opportunity_id",
    "originating_federal_contract_opportunity",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 15
}
```

Run a complementary contracting-agency pass when procurement execution matters:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "contracting_federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_awardees_by_dollars_obligated",
    "top_funding_federal_agencies_by_dollars_obligated",
    "top_contracting_federal_agencies_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Surface near-term federal contract opportunities for the agency:
Tool: `Search_Federal_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+180d/d"
  },
  "aggregations": [
    "top_federal_agencies_by_doc_count",
    "top_set_aside_types_by_doc_count",
    "top_naics_codes_by_doc_count",
    "top_psc_codes_by_doc_count",
    "top_contacts_by_doc_count"
  ],
  "per_page": 0
}
```

Surface upcoming federal forecasts for the agency:
Tool: `Search_Federal_Forecasts`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "estimated_solicitation_release_date_range": {
    "from": "now/d",
    "to": "now+365d/d"
  },
  "aggregations": [
    "top_federal_agencies_by_doc_count",
    "top_set_aside_types_by_doc_count",
    "top_naics_codes_by_doc_count",
    "top_contacts_by_doc_count"
  ],
  "per_page": 0
}
```

List active or still-orderable IDVs tied to the agency:
Tool: `Search_Federal_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "funding_federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "last_date_to_order_range": {
    "from": "now/d",
    "to": null
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date",
    "last_date_to_order",
    "ceiling_value",
    "contract_type",
    "multiple_or_single_award",
    "set_aside",
    "awardee",
    "federal_contract_vehicle",
    "funding_federal_agency",
    "contracting_federal_agency",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "lastDateToOrder",
    "direction": "asc"
  },
  "per_page": 15
}
```

Resolve agency-associated contacts and contracting personnel:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "reference_types": [
    "pointOfContact",
    "transactionContact"
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
  "per_page": 15
}
```

Measure the agency's grant-award footprint when grants are material:
Tool: `Search_Federal_Grant_Awards`
```json
{
  "search_mode": "keyword",
  "funding_federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_awardees_by_dollars_obligated",
    "top_federal_grant_programs_by_dollars_obligated",
    "top_locations_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Surface agency-linked grant programs and open grant opportunities:
Tool: `Search_Federal_Grant_Programs`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "cfda_number",
    "description",
    "federal_agency",
    "federal_grant_awards",
    "federal_grant_opportunities",
    "govtribe_ai_summary"
  ],
  "per_page": 10
}
```

Tool: `Search_Federal_Grant_Opportunities`
```json
{
  "search_mode": "keyword",
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+365d/d"
  },
  "aggregations": [
    "top_federal_agencies_by_doc_count",
    "top_federal_grant_programs_by_doc_count",
    "top_points_of_contact_by_doc_count"
  ],
  "per_page": 0
}
```
