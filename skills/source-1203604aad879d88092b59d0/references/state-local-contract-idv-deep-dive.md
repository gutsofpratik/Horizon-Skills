---
title: State and Local Contract IDV Deep Dive
description: How to exhaustively gather context for a state and local contract IDV using child-award and line-item-first interpretation, `govtribe_ai_summary`, attached files, direct parent-vehicle context when available, and cautious vendor discovery.
---

# State and Local Contract IDV Deep Dive

Use this reference when the user wants a deep dive on a single state and local contract IDV and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means loading the target, using `state_local_contract_awards`, `line_items`, `govtribe_ai_summary`, and any attached files to understand how the IDV is actually used, then building the strongest related vehicle, opportunity, buyer, and vendor context.
- Prefer exact structured overlap through child awards, line items, state, categories, contacts, and nested files before semantic expansion.
- Prefer direct nested relationships already on the target before making extra search calls.
- If the target, nested awards, nested line items, file previews, or the strongest related vehicle or opportunity are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain what the IDV is, how it is being used, what the dominant buyers and categories are, whether a parent vehicle is likely in play, and what the most relevant unresolved questions are.

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
  - `potential_completion_date`
  - `contract_number`
  - `contract_type`
  - `state`
  - `state_local_contract_vehicle`
  - `line_items`
  - `unspsc_categories`
  - `nigp_categories`
  - `government_files`
  - `state_local_contract_awards`
  - `points_of_contact`
  - `govtribe_ai_summary`
- If the target is not already in context, fetch it by exact GovTribe ID or exact quoted contract number.

### 2. Reuse direct structured relationships and treat child awards plus line items as the primary evidence layer
- Use the target's direct relationships before starting broader searches:
  - `state`
  - `state_local_contract_vehicle`
  - `line_items`
  - `unspsc_categories`
  - `nigp_categories`
  - `government_files`
  - `state_local_contract_awards`
  - `points_of_contact`
- State and local IDV metadata is often thin. Treat `state_local_contract_awards`, `line_items`, and `govtribe_ai_summary` as the primary interpretive surfaces when they are present.
- Use `govtribe_ai_summary` early to:
  - orient the IDV before broader searches
  - infer whether the instrument looks schedule-like, catalog-like, service-heavy, or commodity-heavy
  - generate sharper award, line-item, and file queries
- Use nested `state_local_contract_awards` early to:
  - understand who is actually ordering under the IDV
  - see whether usage is concentrated or broad
  - infer whether the IDV behaves more like a single-holder lane or a broader usage vehicle
- Use nested `line_items` early to:
  - identify the actual priced or purchased components
  - understand pricing basis, units, and quantity signals
  - determine whether the contract is being used in one narrow lane or across several categories
- Some child awards or IDVs can carry very large `unspsc_categories` or `nigp_categories` lists.
- Treat long category lists as broad indexing or recall metadata, not as proof that every attached code is equally central to the instrument.
- When category counts are unusually large, use child awards, line items, `govtribe_ai_summary`, and files to identify the dominant usage lane instead of flattening the IDV into every attached category.
- Let child awards, line items, and source files outrank the summary when exact pricing, quantities, terms, or obligations matter.

### 3. Rehydrate exact child awards and line items before broader fan-out
- If nested `state_local_contract_awards` are present, use them before any semantic market search.
- If the nested award rows are too sparse, rehydrate them with `Search_State_And_Local_Contract_Awards` using exact `state_and_local_contract_award_ids`.
- If nested `line_items` are present but too sparse, rehydrate them with `Search_Line_Items` using the parent `state_local_contract_idv_ids`.
- Use the award and line-item passes to answer:
  - which buyers are actually using the IDV
  - which vendors appear beneath it
  - what categories and quantities dominate usage
  - whether there are meaningful unit-price or contract-amount patterns
- If the IDV does not expose useful child awards or line items, say that clearly and rely more heavily on `govtribe_ai_summary`, categories, files, and related-record searches.

### 4. Review attached files when they exist
- If `government_files` is empty, skip file retrieval.
- If `government_files` is present, treat those files as high-value context because the top-level IDV row is often incomplete.
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
- Prioritize file questions that surface high-value IDV context:
  - ordering rules or eligibility
  - scope boundaries and exclusions
  - renewal, option, or completion-window details
  - pricing schedules or catalogs
  - participating entity guidance

### 5. Build the exact buyer and category neighborhood first
- Use the target's `state`, `nigp_categories`, `unspsc_categories`, `points_of_contact`, and child award evidence before semantic fan-out.
- Use `Search_State_And_Local_Contract_IDVs` with the strongest exact anchors first:
  - `state_ids`
  - `contact_ids`
  - `nigp_category_ids`
  - `unspsc_category_ids`
  - relevant recent `award_date_range`
- Exclude the target IDV itself from this cohort pass.
- Use aggregations before wide row pulls when you need market shape instead of more IDV rows.
- Use the neighborhood pass to answer:
  - whether this IDV sits in a recurring buyer-and-category lane
  - whether similar IDVs cluster in the same state or category family
  - whether this looks like a major instrument in the lane or a narrower one-off
- If the target IDV or its child awards have unusually large category fan-out, do not overconstrain the peer search to every attached code. Start with the strongest few category clues surfaced by child awards, line items, files, or `govtribe_ai_summary`.

### 6. Surface likely parent vehicle and related opportunity context only after the structured passes
- If the target already exposes `state_local_contract_vehicle`, use that direct relationship before broader fan-out.
- Otherwise, use `Search_State_And_Local_Contract_Vehicles` with `similar_filter={govtribe_type:"state_local_contract_idv",govtribe_id:target.govtribe_id}` to find the most likely parent or sibling vehicle context.
- Use `Search_State_And_Local_Contract_Opportunities` with the same `similar_filter` to look for likely originating or related opportunities.
- Use these passes to answer:
  - whether the IDV appears to roll up into a broader vehicle
  - whether there is a likely originating solicitation or buyer pattern behind it
  - whether the parent structure changes how to interpret the child award activity

### 7. Treat vendor analysis as evidence-driven, not automatic
- State and local IDVs expose `awardee_name`, not an exact vendor linkage field.
- For single-award or visibly concentrated IDVs, start with the named `awardee_name`.
- For broader or mixed-use IDVs, let the child awards determine which vendors matter most.
- If you have a strong candidate vendor, resolve it with `Search_Vendors` using exact quoted names and conservative skepticism.
- Do not silently turn a name match into a definitive vendor identity.
- Use vendor expansion to answer:
  - whether the holder appears to have broader public-sector footprint
  - whether certifications or structure materially change interpretation
  - whether usage appears dominated by one holder or competitively distributed

### 8. Resolve buyer and contact context when it changes the answer
- Use `points_of_contact` first when the target already exposes them.
- Use `Search_Contacts` when the nested rows are thin and the question depends on richer contact context or file-surfaced contacts.
- For contact expansion, prefer either:
  - exact `contact_ids` already on the target, or
  - `referenced_govtribe_ids=[target.govtribe_id]` with public POC-style `reference_types`
- Use this pass to answer:
  - which office appears to own the IDV
  - whether the same contacts recur across files, child awards, or related opportunities
  - whether there are signals of ongoing usage or follow-on relationship building

### 9. Use semantic expansion only after the structured passes
- If exact child-award, line-item, summary, file, and buyer/category context is still thin, use semantic expansion.
- Good semantic fan-out targets are:
  - related state and local IDVs
  - related state and local vehicles
  - related state and local opportunities
  - related state and local awards
- Treat similar-IDV results as analogs or market-lane evidence, not proof of the same parent structure.
- Build the semantic query from the target's `name`, `govtribe_ai_summary`, `description`, and the strongest child-award or line-item clues.

### 10. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the target IDV
  - the most useful `govtribe_ai_summary` takeaways
  - the strongest child-award usage findings
  - the most informative line-item findings
  - any material file-derived findings
  - the strongest related vehicle or opportunity context
  - any defensible holder or vendor signals
  - the most relevant buyer or contact context
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly related, duplicative, or too far from the user's question.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "state_and_local_contract_i_d_v_ids": [
    "<STATE_LOCAL_CONTRACT_IDV_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "description",
    "awardee_name",
    "contracting_organization",
    "award_date",
    "potential_completion_date",
    "contract_number",
    "contract_type",
    "state",
    "state_local_contract_vehicle",
    "line_items",
    "unspsc_categories",
    "nigp_categories",
    "government_files",
    "state_local_contract_awards",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "per_page": 1
}
```

Resolve the target by exact quoted contract number when only the IDV number is known:
Tool: `Search_State_And_Local_Contract_IDVs`
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

Rehydrate exact child awards exposed on the target:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "state_and_local_contract_award_ids": [
    "<STATE_LOCAL_CONTRACT_AWARD_ID_1>",
    "<STATE_LOCAL_CONTRACT_AWARD_ID_2>"
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
    "contract_number",
    "contract_type",
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

Rehydrate all line items under the exact IDV when pricing or quantities matter:
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

Build a compact peer-IDV market profile while excluding the target:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "nigp_category_ids": [
    "<NIGP_ID_OR_CODE>"
  ],
  "unspsc_category_ids": [
    "<UNSPSC_ID_OR_CODE>"
  ],
  "award_date_range": {
    "from": "now-5Y/d",
    "to": "now/d"
  },
  "state_and_local_contract_i_d_v_ids": [
    "<STATE_LOCAL_CONTRACT_IDV_ID>"
  ],
  "state_and_local_contract_i_d_v_ids_operator": "not_in",
  "aggregations": [
    "dollars_obligated_stats",
    "top_states_by_doc_count",
    "top_contract_entities_by_dollars_obligated",
    "top_nigp_codes_by_dollars_obligated",
    "top_unspsc_codes_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Search for a likely parent vehicle using the IDV as the semantic seed when no direct `state_local_contract_vehicle` is available:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_idv",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_IDV_ID>"
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

Search for a likely originating or related opportunity using the IDV as the semantic seed:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_idv",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_IDV_ID>"
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
    "<STATE_LOCAL_CONTRACT_IDV_ID>"
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
