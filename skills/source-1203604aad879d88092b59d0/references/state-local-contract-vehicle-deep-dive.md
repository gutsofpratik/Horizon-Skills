---
title: State and Local Contract Vehicle Deep Dive
description: How to exhaustively gather context for a state and local contract vehicle using child-IDV and downstream-award analysis, `govtribe_ai_summary`, attached files, and cautious buyer, vendor, and opportunity expansion.
---

# State and Local Contract Vehicle Deep Dive

Use this reference when the user wants a deep dive on a single state and local contract vehicle and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means loading the target, using `govtribe_ai_summary`, child `state_local_contract_idvs`, downstream awards, and any attached files to understand how the vehicle is structured and actually used, then building the strongest buyer, category, opportunity, and vendor context.
- Prefer exact structured overlap through child IDVs, child-award activity, state, categories, contacts, and files before semantic expansion.
- Prefer direct nested relationships already on the target before making extra search calls.
- If the target, nested child IDVs, file previews, downstream award samples, or the strongest related opportunity are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain what the vehicle is for, which child instruments and buyers matter most, how it is being used in practice, what the most important attached-file signals are, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `description`
  - `contracting_organization`
  - `award_date`
  - `potential_completion_date`
  - `contract_type`
  - `state`
  - `unspsc_categories`
  - `nigp_categories`
  - `government_files`
  - `state_local_contract_idvs`
  - `points_of_contact`
  - `govtribe_ai_summary`
- If the target is not already in context, fetch it by exact GovTribe ID or exact quoted vehicle name.

### 2. Reuse direct structured relationships and treat child IDVs plus downstream awards as the primary evidence layer
- Use the target's direct relationships before starting broader searches:
  - `state`
  - `unspsc_categories`
  - `nigp_categories`
  - `government_files`
  - `state_local_contract_idvs`
  - `points_of_contact`
- State and local vehicle metadata is often thin. Treat `govtribe_ai_summary`, child `state_local_contract_idvs`, downstream awards, and attached files as the primary interpretive surfaces when they are present.
- Use `govtribe_ai_summary` early to:
  - orient the vehicle before broader searches
  - identify whether the vehicle looks multi-holder, schedule-like, goods-heavy, services-heavy, or narrowly scoped
  - generate sharper child-IDV, award, and file queries
- Use nested `state_local_contract_idvs` early to:
  - understand how many child instruments appear to sit under the vehicle
  - identify the most important holders, terms, or subordinate lanes
  - infer whether the vehicle behaves more like a broad statewide purchasing structure or a narrow program-specific lane
- Do not assume the top-level vehicle row by itself explains actual usage. In practice, usage usually becomes clear only after looking at child IDVs, downstream awards, files, and the AI summary.

### 3. Rehydrate exact child IDVs before broader fan-out
- If nested `state_local_contract_idvs` are present, use them before any semantic market search.
- If the nested IDV rows are too sparse, rehydrate them with `Search_State_And_Local_Contract_IDVs` using exact `state_and_local_contract_i_d_v_ids`.
- If the vehicle exposes many child IDVs, do not blindly expand all of them at once.
- Start with the most informative subset first:
  - the most relevant child IDs surfaced by `govtribe_ai_summary`
  - the child IDs that best match the user's question
  - the child IDs that appear most central after the first downstream-award pass
- Use the child-IDV pass to answer:
  - which holders or subordinate instruments matter most
  - whether the child instruments look homogeneous or split across distinct lanes
  - whether term, scope, or category differences within the vehicle materially change interpretation

### 4. Pull downstream award activity to understand how the vehicle is actually used
- There is no direct child-award field on the vehicle LLM surface.
- Use `Search_State_And_Local_Contract_Awards` with `similar_filter={govtribe_type:"state_local_contract_vehicle",govtribe_id:target.govtribe_id}` after the target and child-IDV pass.
- Use awards to answer:
  - which buyers are actually ordering through the vehicle
  - which categories dominate real usage
  - whether usage is concentrated in a few entities or spread broadly
  - which vendors or holders appear repeatedly in actual awarded work
- For initial shape, prefer aggregations before wide row pulls.
- For concrete examples, follow the aggregation pass with a modest recent-award sample.
- If the award results are thin, say that clearly and rely more heavily on child IDVs, files, categories, and `govtribe_ai_summary`.

### 5. Review attached files when they exist
- If `government_files` is empty, skip file retrieval.
- If `government_files` is present, treat those files as high-value context because they often contain the practical ordering, pricing, amendment, and participation details that the top-level vehicle row does not.
- Preview the exact file IDs with `Search_Government_Files` using `government_file_ids`.
- Request:
  - `name`
  - `posted_date`
  - `content_snippet`
  - `download_url`
  - `parent_record`
  - `found_in_file_contacts`
  - `govtribe_ai_summary`
- Use `content_snippet` plus `govtribe_ai_summary` to decide which files matter most.
- If the snippet already answers the question, stop there.
- If the snippet only suggests relevance, or the task depends on exact wording, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until ready, and call `Search_Vector_Store`. Cite returned source metadata with the external host's native citation format; for a material skipped file, use the host's attachment or spreadsheet capability or disclose the gap.
- Prioritize file questions that surface high-value vehicle context:
  - ordering instructions or eligibility rules
  - pricing, discount, or catalog structure
  - amendments, renewals, or extension terms
  - scope boundaries and exclusions
  - participating entity rules or compliance requirements

### 6. Use child line items only when a child IDV or award makes them materially useful
- Vehicles do not expose `line_items` directly.
- If a child IDV or downstream award suggests pricing structure, quantity patterns, or catalog behavior that matters to the user's question, follow that child record into `Search_Line_Items`.
- Use this pass to answer:
  - what is actually being bought beneath the vehicle
  - whether pricing appears catalog-like, quantity-based, or service-hour based
  - whether the vehicle covers one dominant lane or many distinct purchased components
- Skip line-item expansion if child-IDV, award, file, and summary context already answer the user's question.

### 7. Build the exact buyer and category neighborhood first
- Use the target's `state`, `nigp_categories`, `unspsc_categories`, child-IDV evidence, and downstream-award findings before semantic fan-out.
- Some vehicles, child IDVs, or child awards can carry very large `unspsc_categories` or `nigp_categories` lists.
- Treat long category lists as broad indexing or recall metadata, not as proof that every attached code is equally central to the vehicle.
- When category counts are unusually large, use child IDVs, downstream awards, files, and `govtribe_ai_summary` to identify the dominant usage lane instead of flattening the vehicle into every attached category.
- Use `Search_State_And_Local_Contract_Vehicles` or `Search_State_And_Local_Contract_Awards` with the strongest exact anchors first:
  - `state_ids`
  - `contact_ids`
  - the strongest few `nigp_category_ids`
  - the strongest few `unspsc_category_ids`
  - relevant recent `award_date_range`
- Exclude the target vehicle itself from vehicle cohort passes.
- Use aggregations before wide row pulls when you need market shape instead of more rows.
- Use the neighborhood pass to answer:
  - whether this vehicle sits in a recurring buyer-and-category lane
  - whether usage is concentrated in one state or one kind of contracting entity
  - whether the vehicle looks central to the lane or more niche

### 8. Treat vendor and holder analysis as evidence-driven, not automatic
- Vehicle rows do not expose a normalized vendor field.
- Let child IDVs and downstream awards determine which holders or vendors matter most.
- If you have a strong candidate company name, resolve it with `Search_Vendors` using exact quoted names and conservative skepticism.
- Do not silently turn a name match into a definitive vendor identity.
- Use vendor expansion to answer:
  - whether the apparent holders have broader public-sector footprint
  - whether one holder dominates usage or multiple holders appear active
  - whether certifications or structure materially change interpretation

### 9. Resolve contact and related-opportunity context only after the structured passes
- Use `points_of_contact` first when the target already exposes them.
- Use `Search_Contacts` when the nested rows are thin and the question depends on richer contact context or file-surfaced contacts.
- For contact expansion, prefer either:
  - exact `contact_ids` already on the target, or
  - `referenced_govtribe_ids=[target.govtribe_id]` with public POC-style `reference_types`
- Use `Search_State_And_Local_Contract_Opportunities` with `similar_filter={govtribe_type:"state_local_contract_vehicle",govtribe_id:target.govtribe_id}` only after the child-IDV, award, summary, and file passes.
- Use these passes to answer:
  - which office appears to own or manage the vehicle
  - whether the same contacts recur across files or related opportunities
  - whether a likely originating or related opportunity surfaces useful requirement or compliance context

### 10. Use semantic expansion only after the structured passes, then stop with a context package
- If exact child-IDV, award, file, buyer, and opportunity context is still thin, use semantic expansion.
- Good semantic fan-out targets are:
  - related state and local vehicles
  - related state and local opportunities
  - related state and local IDVs
  - related state and local awards
- Build the semantic query from the target's `name`, `govtribe_ai_summary`, `description`, and the strongest child-IDV, downstream-award, or file clues.
- Treat semantic results as analogs or market-lane evidence, not proof of exact lineage.
- Good stopping points usually include:
  - the target vehicle
  - the most useful `govtribe_ai_summary` takeaways
  - the strongest child-IDV findings
  - the strongest downstream-award findings
  - any material file-derived findings
  - the strongest buyer, category, or holder signals
  - the most relevant related-opportunity context
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly related, duplicative, or too far from the user's question.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "keyword",
  "state_and_local_contract_vehicle_ids": [
    "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "description",
    "contracting_organization",
    "award_date",
    "potential_completion_date",
    "contract_type",
    "state",
    "unspsc_categories",
    "nigp_categories",
    "government_files",
    "state_local_contract_idvs",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "per_page": 1
}
```

Resolve the target by exact quoted vehicle name when only the title is known:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "query": "\"<VEHICLE_NAME>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "award_date"
  ],
  "per_page": 5
}
```

Rehydrate exact child IDVs exposed on the target:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "state_and_local_contract_i_d_v_ids": [
    "<STATE_LOCAL_CONTRACT_IDV_ID_1>",
    "<STATE_LOCAL_CONTRACT_IDV_ID_2>",
    "<STATE_LOCAL_CONTRACT_IDV_ID_3>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "awardee_name",
    "contracting_organization",
    "award_date",
    "potential_completion_date",
    "contract_number",
    "contract_type",
    "line_items",
    "government_files",
    "state_local_contract_awards",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 25
}
```

Pull a recent downstream-award sample using the vehicle as the seed:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_vehicle",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  },
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "awardee_name",
    "contracting_organization",
    "award_date",
    "contract_amount",
    "cumulative_value",
    "line_items",
    "government_files",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 25
}
```

Build a compact downstream-award usage rollup before pulling many rows:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_vehicle",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  },
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "award_date_range": {
    "from": "now-5Y/d",
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

Preview attached files by exact file IDs before vector-store staging:
Tool: `Search_Government_Files`
```json
{
  "search_mode": "keyword",
  "government_file_ids": [
    "<GOVERNMENT_FILE_ID_1>",
    "<GOVERNMENT_FILE_ID_2>",
    "<GOVERNMENT_FILE_ID_3>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "posted_date",
    "content_snippet",
    "download_url",
    "parent_record",
    "found_in_file_contacts",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "postedDate",
    "direction": "desc"
  },
  "per_page": 10
}
```

Follow one notable child record into line items when pricing or quantities matter:
Tool: `Search_Line_Items`
```json
{
  "state_local_contract_idv_ids": [
    "<STATE_LOCAL_CONTRACT_IDV_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "name",
    "description",
    "quantity",
    "unit_of_measure",
    "unit_price",
    "subtypes",
    "nigp_category",
    "unspsc_category",
    "state_local_contract_award",
    "state_local_contract_idv",
    "state_local_contract_vehicle"
  ],
  "sort": {
    "key": "unitPrice",
    "direction": "desc"
  },
  "per_page": 50
}
```

Search for a related or likely originating opportunity using the vehicle as the seed:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_vehicle",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  },
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "posted_date",
    "due_date",
    "jurisdictions",
    "government_files",
    "nigp_categories",
    "unspsc_categories",
    "points_of_contact"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Search for peer vehicles while excluding the target:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_vehicle",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  },
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "state_and_local_contract_vehicle_ids": [
    "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  ],
  "state_and_local_contract_vehicle_ids_operator": "not_in",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contracting_organization",
    "award_date",
    "potential_completion_date",
    "contract_type",
    "state_local_contract_idvs",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Resolve public points of contact when the nested target rows are thin:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "referenced_govtribe_ids": [
    "<STATE_LOCAL_CONTRACT_VEHICLE_ID>"
  ],
  "reference_types": [
    "pointOfContact",
    "externalFile"
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
