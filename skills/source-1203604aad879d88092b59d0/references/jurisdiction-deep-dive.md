---
title: Jurisdiction Deep Dive
description: How to exhaustively gather context for a jurisdiction using exact jurisdiction-scoped opportunity and government-file branches first, then bounded award, IDV, vehicle, vendor, and contact follow-up to build a capture-ready state and local market view.
---

# Jurisdiction Deep Dive

Use this reference when the user wants a deep dive on a single jurisdiction and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means locking the exact jurisdiction first, then using that exact scope to build the strongest near-term pipeline, file, buyer, vendor, category, and market-structure view without drifting into unrelated local entities.
- For jurisdictions, prefer aggregation-first analysis on each major surface and use row retrieval mainly to anchor the narrative with representative examples.
- The jurisdiction target itself is thin. Most of the value lives in downstream state and local opportunities, files, awards, IDVs, and vehicles rather than in the target row alone.
- Prefer exact `jurisdiction_ids` branches first where the surface supports them, especially `Search_State_And_Local_Contract_Opportunities` and `Search_Government_Files`.
- Treat award, IDV, and vehicle context as bounded approximation layers unless the surface exposes a true jurisdiction filter.
- If the target, recent opportunity rollups, strongest files, or central anchor records are already in context, reuse them instead of refetching the same records.
- Stop once you can explain what this jurisdiction appears to buy, what is due soon, which categories and entities dominate, which vendors or contracts recur, what the key file-derived signals are, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `fips_code`
  - `updated_at`
- If the target is not already in context, fetch it by exact GovTribe ID, exact quoted jurisdiction name, or exact FIPS code.

### 2. Lock exact jurisdiction scope before wider fan-out
- Treat the resolved jurisdiction as the exact scope anchor.
- Use `jurisdiction_ids=[target.govtribe_id]` when supported. If the downstream surface or existing context works better with FIPS, `jurisdiction_ids=[target.fips_code]` is also valid.
- The current jurisdiction LLM surface does not expose a parent state, summary, or procurement narrative directly.
- Resolve parent-state context from the first exact opportunity or file branch when it appears, or from known user context if the state is already clear.
- Do not silently widen the analysis to the whole state unless the user asks for a broader state view.

### 3. Build the exact near-term opportunity pipeline first
- Start with `Search_State_And_Local_Contract_Opportunities` using exact `jurisdiction_ids`.
- Use an aggregation-first pass before pulling many rows.
- Keep the first opportunity pass bounded:
  - usually `due_date_range` over the next 60 to 180 days
  - sometimes `posted_date_range` over the last 6 to 12 months when the user cares about recent notice cadence
- Use the exact opportunity pass to answer:
  - what is due soon
  - which UNSPSC and NIGP families dominate
  - whether there is one issuing pattern or multiple independent buying lanes
  - whether the jurisdiction appears active, seasonal, or sparse
- After the aggregation pass, pull a modest due-soon row sample so the narrative includes concrete opportunities.
- Because state and local metadata is often thin, treat `govtribe_ai_summary`, attached files, and points of contact on these opportunities as higher-value evidence than the raw target row.

### 4. Preview exact jurisdiction files early
- Use `Search_Government_Files` with exact `jurisdiction_ids`.
- For jurisdictions, files often contain some of the most useful evidence:
  - procurement manuals
  - registration instructions
  - bid forms
  - addenda
  - technical requirements
  - procurement portal or compliance instructions
- Start with metadata plus `content_snippet`.
- Use the file preview pass to answer:
  - which documents look central to current procurement behavior
  - whether the jurisdiction relies on a specific portal, registration process, or compliance package
  - whether there are recurring procurement terms or policy constraints
- If a file only looks potentially relevant from metadata or `content_snippet`, and the question depends on exact wording, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until ready, and call `Search_Vector_Store`. Cite returned source metadata with the external host's native citation format; for a material skipped file, use the host's attachment or spreadsheet capability or disclose the gap.

### 5. Build the recent award and vendor view as a bounded approximation
- The current state and local award surface does not expose an exact `jurisdiction_ids` filter.
- Build the award-side view with a bounded approximation:
  - exact quoted `query` on the jurisdiction name
  - resolved `state_ids` when available
  - sometimes a category constraint from the exact opportunity pass
  - a trailing 12 to 24 month `award_date_range`
- Start with an aggregation-first pass before pulling many rows.
- Use the award pass to answer:
  - which vendors recur
  - which contract entities recur
  - which UNSPSC and NIGP families dominate
  - whether the jurisdiction appears to rely on repeat contracts or fragmented one-off awards
- Treat these award results as evidence-backed approximations, not guaranteed exact jurisdiction lineage.
- After the aggregation pass, pull a modest recent-award sample and use `govtribe_ai_summary`, `line_items`, and `government_files` to sharpen what the jurisdiction is actually buying.

### 6. Map nearby IDV and vehicle structure only after opportunities and awards
- The current state and local IDV and vehicle surfaces also do not expose exact `jurisdiction_ids`.
- Use them after the exact opportunity pass and the bounded award pass have identified the strongest state and category lanes.
- Prefer structured constraints such as:
  - resolved `state_ids`
  - dominant `nigp_category_ids`
  - dominant `unspsc_category_ids`
- Use the IDV and vehicle passes to answer:
  - whether the jurisdiction appears to buy through recurring contracts or cooperative structures
  - whether one vehicle family or parent contract pattern materially shapes access to work
  - whether the strongest opportunities and awards sit inside a broader reusable contracting infrastructure
- Treat these as neighboring market-structure signals, not as exact jurisdiction-owned records unless the selected rows clearly reference the jurisdiction.

### 7. Derive contacts and buyer signals from exact anchor records
- Do not start with a loose contact search.
- Instead, use the exact opportunity and exact file branches to find the strongest anchor records first.
- Then:
  - reuse nested `points_of_contact` from opportunity rows
  - use `Search_Contacts` with `referenced_govtribe_ids` set to the most central opportunity, award, or file IDs
- Use the contact branch to answer:
  - which people or mailboxes recur
  - whether the same procurement office appears across multiple opportunities or files
  - whether a few contacts seem central to the jurisdiction's buying behavior
- Treat contact context as record-derived and role-specific, not as a separate loose discovery pass.

### 8. Use semantic expansion only after the exact and bounded passes
- If the exact opportunity branch, exact file branch, and bounded award-side view are still too thin, use bounded semantic expansion.
- Good semantic targets are:
  - state and local opportunities
  - state and local awards
  - state and local IDVs
  - state and local vehicles
- Treat semantic results as adjacency signals for market context, not proof of exact jurisdiction lineage.
- Do not use semantic expansion to compensate for an unresolved jurisdiction scope decision.

### 9. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the exact jurisdiction target
  - the strongest near-term opportunity signals
  - the most relevant jurisdiction-scoped files
  - the most useful category and issuing-entity rollups
  - the bounded recent-award and vendor view
  - any clearly relevant IDV or vehicle structure
  - the most central contacts or procurement offices
  - a few representative anchor records
  - a short list of unresolved gaps
- Do not keep expanding if new records are weakly connected, duplicative, or mostly state-wide rather than jurisdiction-specific.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_Jurisdictions`
```json
{
  "search_mode": "keyword",
  "jurisdiction_ids": [
    "<JURISDICTION_ID_OR_FIPS>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "fips_code",
    "updated_at"
  ],
  "per_page": 1
}
```

Resolve a jurisdiction by exact quoted name when only the label is known:
Tool: `Search_Jurisdictions`
```json
{
  "query": "\"<JURISDICTION_NAME>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "fips_code"
  ],
  "per_page": 5
}
```

Build the exact near-term opportunity rollup first:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "jurisdiction_ids": [
    "<JURISDICTION_ID_OR_FIPS>"
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

Pull representative due-soon opportunities for the jurisdiction:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "jurisdiction_ids": [
    "<JURISDICTION_ID_OR_FIPS>"
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

Preview exact jurisdiction-scoped government files:
Tool: `Search_Government_Files`
```json
{
  "search_mode": "keyword",
  "jurisdiction_ids": [
    "<JURISDICTION_ID_OR_FIPS>"
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

Build the bounded recent-award view after state resolution:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "query": "\"<JURISDICTION_NAME>\"",
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

Pull representative recent awards to sharpen vendor and scope context:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "query": "\"<JURISDICTION_NAME>\"",
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

Map nearby IDV structure after identifying the strongest state and category lanes:
Tool: `Search_State_And_Local_Contract_IDVs`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "nigp_category_ids": [
    "<TOP_NIGP_ID_OR_CODE>"
  ],
  "unspsc_category_ids": [
    "<TOP_UNSPSC_ID_OR_CODE>"
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

Map nearby vehicle structure after identifying the strongest state and category lanes:
Tool: `Search_State_And_Local_Contract_Vehicles`
```json
{
  "search_mode": "keyword",
  "state_ids": [
    "<STATE_ID_OR_USPS>"
  ],
  "nigp_category_ids": [
    "<TOP_NIGP_ID_OR_CODE>"
  ],
  "unspsc_category_ids": [
    "<TOP_UNSPSC_ID_OR_CODE>"
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

Pull record-derived contacts from the strongest exact anchor records:
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
