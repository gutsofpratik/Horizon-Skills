---
title: Major Defense Program Deep Dive
description: How to exhaustively gather context for a major defense program using `description`, `govtribe_ai_summary`, linked federal contract awards, and transaction-backed award-family IDV and vehicle pivots when they materially structure program work.
---

# Major Defense Program Deep Dive

Use this reference when the user wants a deep dive on a single major defense program and the answer depends on more than the target row alone.

## Goal
- Exhaustive context means locking the exact program, understanding it first through `description` and `govtribe_ai_summary`, then using linked federal contract awards as the main structured evidence layer for spend, vendors, contracting context, and downstream IDV or vehicle pivots.
- Prefer the program's own summary and description before wider search expansion.
- Retrieve the program's awards with a second call before broader market searches. The program row does not carry an award list.
- Treat IDVs and vehicles as valid transaction-backed award-family pivots from the program, not as first-class nested fields on the program row.
- Treat managing-agency context as a supporting branch, not the main source of value.
- Stop once you can explain what the program is, how it is described, which awards and vendors dominate, which contracting offices recur, which ordering paths matter, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `name`
  - `code`
  - `acronyms`
  - `description`
  - `govtribe_ai_summary`
  - `defense_program_type`
  - `aaf_pathway`
  - `acquisition_category`
  - `updated_at`
  - `federal_agency`
- If the target is not already in context, fetch it by exact GovTribe ID, exact quoted program name, exact code, or exact acronym.

### 2. Treat the program narrative as the first evidence layer
- Start with `description` and `govtribe_ai_summary`.
- For major defense programs, most of the value is usually here plus the linked federal contract awards.
- Use `description` and `govtribe_ai_summary` early to answer:
  - what the program does
  - how the program is framed operationally
  - what capability lane or mission set it belongs to
  - which terms or themes should guide award-side follow-up
- Use `code`, `acronyms`, `defense_program_type`, `aaf_pathway`, and `acquisition_category` as supporting structure, not as the main analytical surface.

### 3. Retrieve the program's awards before broader search fan-out
- The program row does not carry an award list. Call `Search_Federal_Contract_Awards` with `dod_acquisition_program_ids` set to the program's `govtribe_id`.
- Page through the results rather than assuming the first page is complete.
- Use this direct-award pass to answer:
  - which vendors recur
  - which contracting and funding agencies recur
  - which NAICS and PSC lanes dominate
  - whether award activity appears concentrated or broad
- Treat this step as the base evidence layer for later IDV and vehicle pivots.
- The product's deeper IDV and vehicle views are effectively built from federal contract award transaction activity tied to the program, not from first-class IDV or vehicle relationships on the program row.
- If the award linkage is thin, say that clearly and rely on the summary plus a bounded broader award pass.

### 4. Build the broader award landscape only after the direct-award pass
- If you need a fuller contract picture, use `Search_Federal_Contract_Awards` with `similar_filter={govtribe_type:"dod_acquisition_program",govtribe_id:target.govtribe_id}`.
- Start with an aggregation-first pass before pulling many rows.
- Use the broader award pass to answer:
  - recent dollars obligated
  - top awardees
  - top contracting agencies
  - dominant PSC and NAICS families
  - whether the program's award activity is growing, narrowing, or shifting
- After the aggregation pass, pull a modest recent-award sample so the narrative includes representative records.

### 5. Keep agency context light and evidence-driven
- Use nested `federal_agency` first when present.
- If the managing agency materially changes the answer, fetch it exactly with `Search_Federal_Agencies`.
- Use this branch to answer:
  - who appears to manage the program
  - whether the agency context adds mission or acquisition framing the program row itself does not provide
- Do not default to a full federal-agency deep dive unless the user actually needs account-level context.

### 6. Pull vehicles or IDVs only when the award evidence makes them material
- Do not treat IDVs or vehicles as direct nested relationships on the major defense program row.
- Do treat them as legitimate transaction-backed award-family pivots when the program's award landscape suggests recurring ordering paths.
- When the current AI search surface allows it, prefer an exact `Search_Federal_Transactions` pass filtered by `major_defense_program_ids` to quantify top IDVs and vehicles before jumping into broader IDV or vehicle searches.
- If representative program awards clearly point to recurring IDVs or vehicles, or if the user explicitly wants ordering-path context, expand into:
  - `Search_Federal_Contract_IDVs`
  - `Search_Federal_Contract_Vehicles`
- The product UI derives these views from transaction activity tied to the program and award family.
- Use the transaction pass to identify the dominant ordering paths, then rehydrate the most important IDVs or vehicles with the dedicated search tools.
- If the exact transaction branch is still too thin, use the same `similar_filter={govtribe_type:"dod_acquisition_program",govtribe_id:target.govtribe_id}` used in the broader award pass, then sanity-check the results against representative program awards.
- Use this branch to answer:
  - whether the program is flowing through a small number of ordering paths
  - whether one vehicle family materially structures access to the work
  - which IDVs dominate recent obligations or ordering activity
  - whether schedules, GWACs, BPAs, or IDIQs are the real route to market
  - whether orderable vehicles or IDVs change the capture implications
- If the award rows and broader program-aligned pivots do not show meaningful recurring vehicle or IDV structure, skip this branch.

### 7. Treat related opportunities as secondary and bounded
- Do not default to a large opportunity scan from the program record.
- If the user explicitly wants current pipeline, or if the award and summary language strongly suggest active follow-on work, use `Search_Federal_Contract_Opportunities` with `similar_filter={govtribe_type:"dod_acquisition_program",govtribe_id:target.govtribe_id}`.
- Use this branch to answer:
  - whether there are recent or open solicitations clearly tied to the program
  - whether the upcoming opportunity language matches the established award-side lane
- Treat these as supporting pipeline signals, not as the core of the program analysis.

### 8. Do not default to file retrieval
- The major defense program surface itself does not expose files.
- Only move into file retrieval if a representative linked opportunity becomes central to the user's question and its attached files are likely to contain material requirement or compliance detail.
- In that case, follow the selected opportunity, preview `government_files` with `Search_Government_Files`, and use `content_snippet` first before vector-store staging.

### 9. Use broader semantic expansion only after the summary-and-awards path is exhausted
- This step is for looser adjacency searches after the bounded program-aligned pivots above.
- If the direct summary, direct awards, broader award pass, and any necessary IDV or vehicle pivots are still too thin, use bounded semantic expansion.
- Good semantic targets are:
  - federal contract awards
  - federal contract opportunities
  - peer major defense programs only when the user wants comparison
- Treat semantic results as adjacency signals, not proof of exact program lineage.

### 10. Stop with a context package, not a data dump
- Good stopping points usually include:
  - the target program
  - the most useful `description` and `govtribe_ai_summary` takeaways
  - the strongest linked-award findings
  - the broader award rollup when needed
  - the most relevant vendor and contracting-office signals
  - any material managing-agency context
  - any clearly relevant IDVs, vehicles, or opportunities
  - a short list of unresolved gaps
- Do not keep expanding if new records are only loosely related or if the guide has already answered the question through the summary-plus-awards-plus-ordering-paths evidence.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_Major_Defense_Programs`
```json
{
  "search_mode": "keyword",
  "major_defense_program_ids": [
    "<MAJOR_DEFENSE_PROGRAM_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "code",
    "acronyms",
    "description",
    "govtribe_ai_summary",
    "defense_program_type",
    "aaf_pathway",
    "acquisition_category",
    "updated_at",
    "federal_agency"
  ],
  "per_page": 1
}
```

Resolve a program by exact quoted name or code:
Tool: `Search_Major_Defense_Programs`
```json
{
  "query": "\"<PROGRAM_NAME_OR_CODE>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "code",
    "acronyms",
    "federal_agency"
  ],
  "per_page": 5
}
```

Rehydrate direct linked awards exposed on the target:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "federal_contract_award_ids": [
    "<FEDERAL_CONTRACT_AWARD_ID_1>",
    "<FEDERAL_CONTRACT_AWARD_ID_2>",
    "<FEDERAL_CONTRACT_AWARD_ID_3>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date",
    "dollars_obligated",
    "awardee",
    "contracting_federal_agency",
    "funding_federal_agency",
    "naics_category",
    "psc_category",
    "federal_contract_vehicle",
    "federal_contract_idv",
    "govtribe_ai_summary"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 25
}
```

Build the broader award rollup for the program:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "dod_acquisition_program",
    "govtribe_id": "<MAJOR_DEFENSE_PROGRAM_ID>"
  },
  "award_date_range": {
    "from": "now-24M/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_contracting_federal_agencies_by_dollars_obligated",
    "top_awardees_by_dollars_obligated",
    "top_psc_codes_by_dollars_obligated",
    "top_naics_codes_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Pull representative recent awards for the program:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "dod_acquisition_program",
    "govtribe_id": "<MAJOR_DEFENSE_PROGRAM_ID>"
  },
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
    "awardee",
    "contracting_federal_agency",
    "funding_federal_agency",
    "naics_category",
    "psc_category",
    "federal_contract_vehicle",
    "federal_contract_idv"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 15
}
```

Pull representative program-aligned IDVs when ordering context matters:
Tool: `Search_Federal_Contract_IDVs`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "dod_acquisition_program",
    "govtribe_id": "<MAJOR_DEFENSE_PROGRAM_ID>"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date",
    "last_date_to_order",
    "ceiling_value",
    "multiple_or_single_award",
    "contract_type",
    "awardee",
    "contracting_federal_agency",
    "federal_contract_vehicle"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Build an exact transaction-backed MDAP rollup of top IDVs and vehicles:
Tool: `Search_Federal_Transactions`
```json
{
  "major_defense_program_ids": [
    "<MAJOR_DEFENSE_PROGRAM_ID>"
  ],
  "major_defense_program_ids_operator": "in",
  "aggregations": [
    "dollars_obligated_stats",
    "top_idvs_by_dollars_obligated",
    "top_federal_contract_vehicles_by_dollars_obligated",
    "top_awardees_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Pull representative program-aligned vehicles when vehicle family matters:
Tool: `Search_Federal_Contract_Vehicles`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "dod_acquisition_program",
    "govtribe_id": "<MAJOR_DEFENSE_PROGRAM_ID>"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_type",
    "award_date",
    "last_date_to_order",
    "shared_ceiling",
    "set_aside_type",
    "federal_agency"
  ],
  "sort": {
    "key": "_score",
    "direction": "desc"
  },
  "per_page": 10
}
```

Resolve the managing agency when it materially changes the answer:
Tool: `Search_Federal_Agencies`
```json
{
  "federal_agency_ids": [
    "<FEDERAL_AGENCY_ID>"
  ],
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "alternate_name",
    "acronym",
    "defense_or_civilian"
  ],
  "per_page": 1
}
```

Pull representative related opportunities only when current pipeline matters:
Tool: `Search_Federal_Contract_Opportunities`
```json
{
  "search_mode": "semantic",
  "similar_filter": {
    "govtribe_type": "dod_acquisition_program",
    "govtribe_id": "<MAJOR_DEFENSE_PROGRAM_ID>"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "opportunity_type",
    "set_aside_type",
    "posted_date",
    "due_date",
    "descriptions",
    "federal_agency",
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
