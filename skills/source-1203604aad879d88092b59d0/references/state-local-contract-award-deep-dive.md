---
title: State and Local Contract Award Deep Dive
description: How to exhaustively gather context for a state and local contract award using line-item-first interpretation, `govtribe_ai_summary`, attached files, direct related IDV/opportunity context, vehicle context, and cautious vendor discovery.
---

# State and Local Contract Award Deep Dive

Use this reference when the user wants a deep dive on a single state and local contract award and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means loading the target, using `line_items`, `govtribe_ai_summary`, and any attached files to understand the award, then building the strongest related IDV, vehicle, opportunity, buyer, and vendor context.
- Prefer exact structured overlap through line items, state, categories, contacts, and nested files before semantic expansion.
- Prefer direct nested relationships already on the target before making extra search calls.
- If the target, nested line items, file previews, or the strongest related parent records are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain what was awarded, what the priced or purchased components appear to be, which buyer and category lane it sits in, whether parent structure is likely in play, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `description`
  - `awardee_name`
  - `contracting_organization`
  - `award_date`
  - `completion_date`
  - `estimated_annual_value`
  - `contract_amount`
  - `cumulative_value`
  - `contract_number`
  - `contract_type`
  - `updated_at`
  - `state`
  - `state_local_contract_idv`
  - `state_local_contract_opportunity`
  - `line_items`
  - `unspsc_categories`
  - `nigp_categories`
  - `government_files`
  - `points_of_contact`
  - `govtribe_ai_summary`
- If the target is not already in context, fetch it by exact GovTribe ID or exact quoted contract number.

### 2. Reuse direct structured relationships and treat line items as the primary evidence layer
- Use the target's direct relationships before starting broader searches:
  - `state`
  - `state_local_contract_idv`
  - `state_local_contract_opportunity`
  - `line_items`
  - `unspsc_categories`
  - `nigp_categories`
  - `government_files`
  - `points_of_contact`
- State and local award metadata is often thin. Treat `line_items` and `govtribe_ai_summary` as the primary interpretive surfaces when they are present.
- Use `govtribe_ai_summary` early to:
  - orient the award before broader searches
  - identify whether this looks goods-, services-, labor-, or construction-oriented
  - generate sharper line-item and file queries
- Use nested `line_items` early to:
  - identify the real priced components of the award
  - infer pricing basis such as unit-price, quantity-based, or schedule-like structure
  - spot whether the bulk of the award appears concentrated in a few items or spread across many
- Some state and local awards carry very large `unspsc_categories` or `nigp_categories` lists.
- Treat long category lists as broad indexing or recall metadata, not as proof that every attached code is equally central to the award.
- When category counts are unusually large, use `line_items`, `govtribe_ai_summary`, and files to identify the dominant scope instead of summarizing the record as a giant mixed-category award.
- Let nested line items and source files outrank the summary when exact pricing, quantities, deliverables, or contractual obligations matter.

### 3. Rehydrate line items before broader award-side fan-out
- If nested `line_items` are present, use them before any semantic market search.
- If the nested rows are too sparse, rehydrate them with `Search_Line_Items` using exact `line_item_ids` or the parent `state_local_contract_award_ids`.
- Use the line-item pass to answer:
  - what was actually bought
  - which units of measure and quantities matter
  - whether there are useful unit-price comparables
  - whether the award implies catalog, schedule, recurring service, or one-time purchase behavior
- If the award does not expose useful line items, say that clearly and rely more heavily on `govtribe_ai_summary`, categories, files, and related awards.

### 4. Review attached files when they exist
- If `government_files` is empty, skip file retrieval.
- If `government_files` is present, treat those files as high-value context because award-side top-level metadata is often incomplete.
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
- Prioritize file questions that surface high-value award context:
  - value or term modifications
  - scope clarifications or exclusions
  - price schedules or awarded bid tabs
  - contract renewals or option structure
  - compliance, insurance, or performance obligations

### 5. Build the exact buyer and category neighborhood first
- Use the target's `state`, `nigp_categories`, `unspsc_categories`, and `points_of_contact` before semantic fan-out.
- Use `Search_State_And_Local_Contract_Awards` with the strongest exact anchors first:
  - `state_ids`
  - `contact_ids`
  - relevant recent `award_date_range`
- Use aggregations before wide row pulls when you need buyer or category shape instead of more award rows.
- Use the neighborhood pass to answer:
  - whether the buyer has a recurring purchasing lane here
  - whether the same categories dominate recent awards
  - whether this award is part of a broader spending pattern or an outlier
- If the target award itself has an unusually large category fan-out, do not overfit the neighborhood search to every attached code. Start with the strongest few category clues surfaced by line items, files, or `govtribe_ai_summary`.

### 6. Fan out to related IDVs, vehicles, and opportunities only after the structured passes
- If the target already exposes `state_local_contract_idv` or `state_local_contract_opportunity`, use those direct relationships before any `similar_filter` fan-out.
- There is still no direct parent-vehicle relationship on this award surface.
- Use `similar_filter` from the target award only after the line-item, summary, file, buyer/category passes, and any direct parent relation reuse.
- Good fan-out targets are:
  - `Search_State_And_Local_Contract_IDVs`
  - `Search_State_And_Local_Contract_Vehicles`
  - `Search_State_And_Local_Contract_Opportunities`
- Keep the strongest state and category constraints in place when they improve precision.
- Use this pass to answer:
  - whether the award appears to sit under a master contract or vehicle
  - whether a likely originating opportunity can be surfaced
  - whether similar parent structures recur in the same market lane

### 7. Treat vendor and incumbent analysis as evidence-driven, not automatic
- State and local awards expose `awardee_name`, not an exact vendor linkage field.
- Only start vendor analysis after the award itself, related awards, line items, or files provide a strong company name.
- If you have a strong candidate vendor, resolve it with `Search_Vendors` using exact quoted names and conservative skepticism.
- Do not silently turn a name match into a definitive vendor identity.
- Use vendor expansion to answer:
  - whether the named awardee appears to have broader public-sector footprint
  - whether certifications or structure materially change the interpretation
  - whether the same company appears repeatedly in the buyer or category lane

### 8. Resolve buyer and contact context when it changes the answer
- Use `points_of_contact` first when the target already exposes them.
- Use `Search_Contacts` when the nested rows are thin and the question depends on richer contact context or file-surfaced contacts.
- For contact expansion, prefer either:
  - exact `contact_ids` already on the target, or
  - `referenced_govtribe_ids=[target.govtribe_id]` with public POC-style `reference_types`
- Use this pass to answer:
  - which office appears to own the awarded work
  - whether the same contacts recur across files, related opportunities, or peer awards
  - whether there are signals of ongoing relationship or follow-on potential

### 9. Use semantic expansion only after the structured passes
- If exact line-item, summary, file, and buyer/category context is still thin, use semantic expansion.
- Good semantic fan-out targets are:
  - related state and local awards
  - related state and local IDVs
  - related state and local vehicles
  - related state and local opportunities
- Build the semantic query from the target's `name`, `govtribe_ai_summary`, `description`, and the strongest line-item or category clues.
- Treat semantic results as analogs or market-lane evidence, not proof of exact lineage.

### 10. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the target award
  - the most useful `govtribe_ai_summary` takeaways
  - the most informative line-item findings
  - any material file-derived findings
  - the strongest related IDV, vehicle, or opportunity context
  - any defensible awardee or incumbent signals
  - the most relevant buyer or contact context
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly related, duplicative, or too far from the user's question.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "state_and_local_contract_award_ids": [
    "<STATE_LOCAL_CONTRACT_AWARD_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "description",
    "awardee_name",
    "contracting_organization",
    "award_date",
    "completion_date",
    "estimated_annual_value",
    "contract_amount",
    "cumulative_value",
    "contract_number",
    "contract_type",
    "updated_at",
    "state",
    "state_local_contract_idv",
    "state_local_contract_opportunity",
    "line_items",
    "unspsc_categories",
    "nigp_categories",
    "government_files",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "per_page": 1
}
```

Resolve the target by exact quoted contract number when only the award number is known:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "query": "\"<CONTRACT_NUMBER>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date"
  ],
  "per_page": 5
}
```

Rehydrate all line items under the exact award when pricing or quantities matter:
Tool: `Search_Line_Items`
```json
{
  "state_local_contract_award_ids": [
    "<STATE_LOCAL_CONTRACT_AWARD_ID>"
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

Build a compact buyer and category rollup for the award's state lane:
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

Search for related parent IDVs using the award as the semantic seed when no direct `state_local_contract_idv` is available:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_award",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_AWARD_ID>"
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
    "potential_completion_date",
    "contract_number",
    "contract_type",
    "state_local_contract_awards",
    "points_of_contact"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Search for related parent vehicles using the award as the semantic seed:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_award",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_AWARD_ID>"
  },
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contracting_organization",
    "award_date",
    "potential_completion_date",
    "contract_type",
    "state_local_contract_idvs",
    "points_of_contact"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Search for a likely originating opportunity using the award as the semantic seed when no direct `state_local_contract_opportunity` is available:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_award",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_AWARD_ID>"
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

Resolve public points of contact when the nested target rows are thin:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "referenced_govtribe_ids": [
    "<STATE_LOCAL_CONTRACT_AWARD_ID>"
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
