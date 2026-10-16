---
title: State Deep Dive
description: How to exhaustively gather context for a state using exact statewide opportunities, awards, IDVs, vehicles, files, and jurisdiction drilldowns to build a capture-ready state and local market view.
---

# State Deep Dive

Use this reference when the user wants a deep dive on a single state and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means locking the exact state first, then using that exact scope to build the strongest opportunity, award, jurisdiction, file, vendor, category, and contract-structure view without drifting into neighboring states.
- For states, prefer aggregation-first analysis on each major surface and use row retrieval mainly to anchor the narrative with representative examples.
- The state target itself is thin. Most of the value lives in downstream state and local opportunities, awards, IDVs, vehicles, files, and the jurisdictions they cluster around.
- Prefer exact `state_ids` branches first on every surface that supports them.
- Treat jurisdictions as the main second-layer drilldown, not as the starting point.
- If the target, statewide rollups, strongest files, or top jurisdiction anchors are already in context, reuse them instead of refetching the same records.
- Stop once you can explain what the state appears to buy, which jurisdictions and entities are hottest, which vendors and categories dominate, what the near-term pipeline looks like, what contract structures matter, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `usps_code`
  - `updated_at`
- If the target is not already in context, fetch it by exact GovTribe ID, exact quoted state name, or exact USPS code.

### 2. Lock exact statewide scope before wider fan-out
- Treat the resolved state as the exact scope anchor for all downstream searches.
- Use `state_ids=[target.govtribe_id]` when that is already in context. If the downstream surface or user context works better with USPS, `state_ids=[target.usps_code]` is also valid.
- Do not silently widen to a multi-state regional view unless the user explicitly asks for it.
- Do not default to one jurisdiction too early. Start state-wide, then drill down into the jurisdictions that actually dominate the results.

### 3. Build the statewide opportunity pipeline first
- Start with `Search_State_And_Local_Contract_Opportunities` using exact `state_ids`.
- Use an aggregation-first pass before pulling many rows.
- Keep the first opportunity pass bounded:
  - usually `due_date_range` over the next 60 to 180 days
  - sometimes `posted_date` over the last 6 to 12 months when the user cares about recent notice cadence
- Use the statewide opportunity pass to answer:
  - how active the state is right now
  - which jurisdictions are generating the most opportunity volume
  - which UNSPSC and NIGP families dominate
  - whether there are a few concentrated hot spots or a broad statewide spread
- After the aggregation pass, pull a modest due-soon opportunity sample so the narrative includes concrete statewide anchors.
- Because state and local metadata is often thin, treat `govtribe_ai_summary`, attached files, and points of contact on these opportunities as higher-value evidence than the raw state target row.

### 4. Build the statewide award and vendor view next
- Use `Search_State_And_Local_Contract_Awards` with exact `state_ids`.
- Start with an aggregation-first pass before pulling many rows.
- Use the statewide award pass to answer:
  - total dollars
  - top contract entities
  - top vendors
  - dominant UNSPSC and NIGP families
  - whether the state's buying activity looks concentrated or fragmented
- After the aggregation pass, pull a modest recent-award sample and use `govtribe_ai_summary`, `line_items`, and `government_files` to sharpen what the state is actually buying.
- Compare the award view to the opportunity view so you can say whether current pipeline is aligned with historic spend or shifting into new lanes.

### 5. Use jurisdictions as the main drilldown layer
- After the statewide opportunity and award rollups, identify the top jurisdictions driving activity.
- Good sources for jurisdiction drilldown are:
  - `top_jurisdictions_by_doc_count` from statewide opportunities
  - the most repeated jurisdiction names surfaced in representative opportunity rows
  - the strongest state and local files or anchor records
- Once the hot jurisdictions are known:
  - fetch them with `Search_Jurisdictions` when exact IDs or FIPS values are available
  - or run follow-up opportunity passes with exact `jurisdiction_ids`
- Use the jurisdiction branch to answer:
  - which cities, counties, districts, or authorities matter most
  - whether the state-level market is really driven by a few large local buyers
  - where the user should drill deeper after the statewide view

### 6. Map statewide IDV and vehicle structure
- Use `Search_State_And_Local_Contract_IDVs` with exact `state_ids`.
- Use `Search_State_And_Local_Contract_Vehicles` with exact `state_ids`.
- Prefer aggregation-first passes before pulling many rows.
- Use these branches to answer:
  - whether the state relies on recurring parent contracts or cooperative structures
  - which categories are most associated with reusable contract vehicles
  - whether one contract family or procurement structure materially shapes access to work
- If the state-wide IDV or vehicle results are too broad, narrow them with the dominant `nigp_category_ids` or `unspsc_category_ids` from the statewide opportunity and award passes.

### 7. Preview statewide files after the main rollups
- Use `Search_Government_Files` with exact `state_ids`.
- For states, files are often useful for:
  - registration and procurement portal guidance
  - statewide cooperative or master-contract documentation
  - addenda and bid-package instructions
  - compliance or participation-goal language
- Start with metadata plus `content_snippet`.
- Use the file preview pass to answer:
  - which official procurement channels or portals recur
  - whether there are statewide procurement manuals or standard instructions worth knowing
  - which files look central enough for full content retrieval
- If a file only looks potentially relevant from metadata or `content_snippet`, and the task depends on exact wording, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until ready, and call `Search_Vector_Store`. Cite returned source metadata with the external host's native citation format; for a material skipped file, use the host's attachment or spreadsheet capability or disclose the gap.

### 8. Derive contacts from the strongest statewide anchor records
- Do not start with a loose statewide contact search.
- Instead, reuse the central opportunity, award, IDV, vehicle, or file anchors already identified.
- Then:
  - reuse nested `points_of_contact` from opportunity, award, IDV, or vehicle rows
  - use `Search_Contacts` with `referenced_govtribe_ids` set to the strongest anchor records
- Use the contact branch to answer:
  - which procurement people or mailboxes recur
  - whether the same people appear across multiple jurisdictions or entities
  - whether certain contacts cluster around key statewide categories or contract structures
- Treat contact context as record-derived and role-specific, not as a separate broad discovery pass.

### 9. Use semantic expansion only after the exact statewide passes
- If the exact statewide opportunity, award, IDV, vehicle, file, and jurisdiction passes are still too thin, use bounded semantic expansion.
- Good semantic targets are:
  - state and local opportunities
  - state and local awards
  - state and local IDVs
  - state and local vehicles
  - peer states only when the user wants comparison or white-space context
- Treat semantic results as adjacent-market evidence, not as direct statewide lineage.
- Do not use semantic expansion to compensate for an unresolved state-scope decision.

### 10. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the exact state target
  - the strongest statewide opportunity and award rollups
  - the top jurisdictions or buyer hot spots
  - the most relevant vendors and contract entities
  - any important IDV or vehicle structure
  - the most useful statewide files
  - the most central record-derived contacts
  - a few representative anchor records
  - a short list of unresolved gaps
- Do not keep expanding if new records are weakly connected, duplicative, or only repeat the same statewide lane without adding new evidence.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_States`
```json
{
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "usps_code",
    "updated_at"
  ],
  "per_page": 1
}
```

Resolve a state by exact quoted name when only the label is known:
Tool: `Search_States`
```json
{
  "query": "\"<STATE_NAME>\"",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "usps_code"
  ],
  "per_page": 5
}
```

Build the statewide opportunity rollup first:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+180d/d"
  },
  "aggregations": [
    "top_states_by_doc_count",
    "top_jurisdictions_by_doc_count",
    "top_unspsc_codes_by_doc_count",
    "top_nigp_codes_by_doc_count"
  ],
  "per_page": 0
}
```

Pull representative due-soon statewide opportunities:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+180d/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "solicitation_number",
    "posted_date",
    "due_date",
    "govtribe_ai_summary",
    "description",
    "state",
    "jurisdictions",
    "government_files",
    "unspsc_categories",
    "nigp_categories",
    "points_of_contact"
  ],
  "sort": {
    "key": "dueDate",
    "direction": "asc"
  },
  "per_page": 15
}
```

Build the statewide award and vendor rollup:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_contract_entities_by_dollars_obligated",
    "top_nigp_codes_by_dollars_obligated",
    "top_unspsc_codes_by_dollars_obligated",
    "top_states_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Pull representative recent statewide awards:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "awardee_name",
    "contracting_organization",
    "award_date",
    "contract_type",
    "contract_amount",
    "govtribe_ai_summary",
    "state_local_contract_idv",
    "state_local_contract_opportunity",
    "line_items",
    "unspsc_categories",
    "nigp_categories",
    "government_files",
    "points_of_contact"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 15
}
```

List jurisdictions inside the state for drilldown:
Tool: `Search_Jurisdictions`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "fips_code"
  ],
  "per_page": 25
}
```

Map statewide IDV structure:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "aggregations": [
    "dollars_obligated_stats",
    "top_contract_entities_by_dollars_obligated",
    "top_states_by_dollars_obligated",
    "top_nigp_codes_by_dollars_obligated",
    "top_unspsc_codes_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Map statewide vehicle structure:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "aggregations": [
    "dollars_obligated_stats",
    "top_contract_entities_by_dollars_obligated",
    "top_states_by_dollars_obligated",
    "top_nigp_codes_by_dollars_obligated",
    "top_unspsc_codes_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Preview statewide government files:
Tool: `Search_Government_Files`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "posted_date",
    "content_snippet",
    "download_url",
    "parent_record",
    "found_in_file_contacts"
  ],
  "sort": {
    "key": "postedDate",
    "direction": "desc"
  },
  "per_page": 15
}
```

Pull record-derived contacts from the strongest statewide anchors:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "reference_types": [
    "pointOfContact",
    "externalFile"
  ],
  "referenced_govtribe_ids": [
    "<STATE_LOCAL_OPPORTUNITY_ID>",
    "<STATE_LOCAL_AWARD_ID>",
    "<GOVERNMENT_FILE_ID>"
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
    "parent_organization_details"
  ],
  "per_page": 15
}
```
