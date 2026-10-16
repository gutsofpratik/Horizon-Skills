---
title: State and Local Contract Opportunity Deep Dive
description: How to exhaustively gather context for a state and local contract opportunity using file-first interpretation, `govtribe_ai_summary`, exact geography and category overlap, related award-side context, and bounded incumbent discovery.
---

# State and Local Contract Opportunity Deep Dive

Use this reference when the user wants a deep dive on a single state and local contract opportunity and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means loading the target, using `govtribe_ai_summary` plus the most useful attached files to understand the requirement, then building the exact geography and category neighborhood, the strongest related awards, IDVs, and vehicles, and the most important open gaps.
- Prefer exact structured overlap through state, jurisdiction, categories, contacts, and attached files before semantic expansion.
- Prefer direct nested relationships already on the target before making extra search calls.
- If the target, file previews, linked jurisdictions, linked categories, or the strongest related awards are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain what the opportunity is, what the files actually require, which buyer and category lane it sits in, what the strongest predecessor or incumbent signals are, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `solicitation_number`
  - `name`
  - `posted_date`
  - `due_date`
  - `description`
  - `updated_at`
  - `state`
  - `jurisdictions`
  - `government_files`
  - `unspsc_categories`
  - `nigp_categories`
  - `points_of_contact`
  - `govtribe_ai_summary`
- If the target is not already in context, fetch it by exact GovTribe ID or exact quoted solicitation number.

### 2. Reuse direct structured relationships and define the exact market lane
- Use the target's direct relationships before starting broader searches:
  - `state`
  - `jurisdictions`
  - `government_files`
  - `unspsc_categories`
  - `nigp_categories`
  - `points_of_contact`
- These direct fields often answer the first wave of context questions without extra search calls.
- State and local opportunity metadata is often thin. Treat `govtribe_ai_summary` and `government_files` as the primary interpretive surfaces when they are present.
- Call out early which exact anchors are actually present:
  - one state versus multi-jurisdiction context
  - one clear NIGP or UNSPSC lane versus several
  - whether public points of contact are already exposed
- Use `govtribe_ai_summary` early to:
  - orient the requirement before broader searches
  - generate sharper file-search questions
  - identify likely product, service, construction, or compliance themes that the sparse row fields may not expose directly
- State and local opportunities do not expose a federal-style notice-chain key or an exact opportunity-to-award linkage scalar on this surface. Do not invent one.
- Treat jurisdictions, categories, dates, and files as the main exact anchors for the deep dive.

### 3. Preview attached government files before escalating to full retrieval
- If `government_files` is empty, skip file retrieval.
- If `government_files` is present, preview the attached files with `Search_Government_Files` scoped by exact `state_local_contract_opportunity_ids`.
- Request:
  - `name`
  - `posted_date`
  - `content_snippet`
  - `download_url`
  - `parent_record`
  - `found_in_file_contacts`
  - `govtribe_ai_summary`
- Use `content_snippet` to decide which files are likely worth deeper retrieval.
- For state and local opportunities, the bulk of the actionable value often sits in the files rather than in the top-level row metadata.
- Use `govtribe_ai_summary` together with `content_snippet` to decide:
  - which files likely matter most
  - what questions to ask first
  - whether the summary appears to rely on details that should be verified in the source files
- If the snippet already answers the question, stop there.
- If the snippet only suggests that a file matters, or the task depends on exact wording, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until ready, and call `Search_Vector_Store`. Cite returned source metadata with the external host's native citation format; for a material skipped file, use the host's attachment or spreadsheet capability or disclose the gap.
- Let the source files outrank `govtribe_ai_summary` when exact wording, compliance obligations, pricing structure, or submission rules matter.
- Prioritize file questions that surface high-value state/local context:
  - submission method, portal, and timing quirks
  - pre-bid or pre-proposal meeting rules
  - pricing schedule or bid-form structure
  - local preference or participation-goal requirements
  - bonding, insurance, licensing, or registration requirements
  - addenda that change due dates, scope, or forms

### 4. Build the exact geography and category neighborhood first
- Use `Search_State_And_Local_Contract_Opportunities` with the strongest exact target anchors before semantic fan-out:
  - `state_ids`
  - `jurisdiction_ids`
  - `nigp_category_ids`
  - `unspsc_category_ids`
  - `contact_ids`
- Exclude the target opportunity itself from this cohort pass.
- Keep the search bounded with recent `posted_date`, active or recent `due_date_range`, and small `per_page`.
- Use the neighborhood pass to answer:
  - whether this is part of a recurring buyer-and-category lane
  - whether nearby opportunities use similar category codes, timing, or contact patterns
  - whether the target appears isolated or part of a broader procurement rhythm

### 5. Fan out to related awards, IDVs, and vehicles only after the exact neighborhood pass
- There is no exposed exact opportunity-to-award bridge here, so use `similar_filter` from the target opportunity after the geography and category pass.
- Good fan-out targets are:
  - `Search_State_And_Local_Contract_Awards`
  - `Search_State_And_Local_Contract_IDVs`
  - `Search_State_And_Local_Contract_Vehicles`
- Keep the strongest state, jurisdiction, category, and contact constraints in place when they improve precision.
- Use the award-side pass to answer:
  - whether there is a likely predecessor or similar awarded contract
  - whether a master contract or parent structure appears to be in play
  - whether the same issuing entity or buyer lane appears repeatedly
  - whether there is enough corroboration to discuss likely incumbents

### 6. Resolve buyer and contact context when it changes the answer
- Use `jurisdictions` and `state` from the target first.
- Use `Search_Contacts` when the nested `points_of_contact` are thin and the question depends on richer contact context or contact references surfaced in files.
- For contact expansion, prefer either:
  - exact `contact_ids` already on the target, or
  - `referenced_govtribe_ids=[target.govtribe_id]` with `reference_types` bounded to public POC-style signals
- Use this pass to answer:
  - which office or buyer appears to own the procurement
  - whether the same contacts recur across related files or opportunities
  - whether outreach should focus on procurement, program, or both

### 7. Treat incumbent and vendor discovery as evidence-driven, not automatic
- State and local opportunities do not expose exact vendor linkage on this surface.
- Only start vendor or incumbent analysis after awards, IDVs, vehicles, or files surface strong candidate names.
- If you have a strong candidate incumbent or likely bidder from related award-side records, resolve that company with `Search_Vendors` using exact quoted names and conservative skepticism.
- Do not overclaim vendor identity when the evidence is only a similar opportunity or a loosely matching company name.

### 8. Use semantic expansion only after the structured passes
- If exact file review plus the geography, category, and contact passes are thin, use semantic expansion.
- Good semantic fan-out targets are:
  - related state and local opportunities
  - related state and local awards
  - related state and local IDVs
  - related state and local vehicles
- Build the semantic query from the target's `name`, `govtribe_ai_summary`, `description`, and the strongest category signals.
- Treat semantic results as analogs or market-lane evidence, not proof of exact predecessor lineage.

### 9. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the target opportunity
  - the most useful `govtribe_ai_summary` takeaways
  - the most useful file-derived requirements
  - the strongest geography and category cohort
  - the strongest related awards, IDVs, and vehicles
  - any defensible incumbent or likely-bidder signals
  - the most relevant buyer or contact context
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly related, duplicative, or too far from the user's question.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "state_and_local_contract_opportunity_ids": [
    "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "posted_date",
    "due_date",
    "description",
    "updated_at",
    "state",
    "jurisdictions",
    "government_files",
    "unspsc_categories",
    "nigp_categories",
    "points_of_contact",
    "govtribe_ai_summary"
  ],
  "per_page": 1
}
```

Resolve the target by exact quoted solicitation number when only the bid number is known:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "query": "\"<SOLICITATION_NUMBER>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "posted_date",
    "due_date"
  ],
  "per_page": 5
}
```

Preview attached government files before vector-store staging:
Tool: `Search_Government_Files`
```json
{
  "search_mode": "keyword",
  "state_local_contract_opportunity_ids": [
    "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
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

Load the exact geography and category neighborhood while excluding the target:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "jurisdiction_ids": [
    "<JURISDICTION_ID_OR_FIPS>"
  ],
  "nigp_category_ids": [
    "<NIGP_ID_OR_CODE>"
  ],
  "unspsc_category_ids": [
    "<UNSPSC_ID_OR_CODE>"
  ],
  "posted_date": {
    "from": "now-180d/d",
    "to": "now/d"
  },
  "due_date_range": {
    "from": "now-30d/d",
    "to": "now+180d/d"
  },
  "state_and_local_contract_opportunity_ids": [
    "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
  ],
  "state_and_local_contract_opportunity_ids_operator": "not_in",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "posted_date",
    "due_date",
    "state",
    "jurisdictions",
    "nigp_categories",
    "unspsc_categories",
    "points_of_contact"
  ],
  "sort": {
    "key": "dueDate",
    "direction": "asc"
  },
  "per_page": 15
}
```

Search for related awards using the opportunity as the semantic seed:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_opportunity",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
  },
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "award_date_range": {
    "from": "now-5Y/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "awardee_name",
    "contracting_organization",
    "award_date",
    "contract_number",
    "contract_type",
    "contract_amount",
    "cumulative_value",
    "government_files",
    "points_of_contact"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Search for related parent IDVs using the opportunity as the semantic seed:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_opportunity",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
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

Search for related vehicles using the opportunity as the semantic seed:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "state_local_contract_opportunity",
    "govtribe_id": "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
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

Resolve public points of contact when the nested target rows are thin:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "referenced_govtribe_ids": [
    "<STATE_LOCAL_CONTRACT_OPPORTUNITY_ID>"
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
