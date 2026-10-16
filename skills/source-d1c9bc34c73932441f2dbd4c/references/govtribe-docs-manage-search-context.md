<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Manage search context

- Canonical GovTribe Docs page: [https://govtribe.com/docs/govtribe-for-agents/guides/manage-search-context](https://govtribe.com/docs/govtribe-for-agents/guides/manage-search-context)

Manage what enters the model context before requesting broad records. GovTribe `Search_*` MCP tools can summarize a result set with aggregations, return compact records with `fields_to_return`, and then expand only the shortlisted records that need deeper review.

Progressive discovery works in three steps:

1. Explore the cohort. Use `aggregations` and `per_page: 0` when rows are not needed.

2. Narrow the search. Use the aggregate buckets or filters that matter.

3. Request focused records. Use `fields_to_return`, then expand fields only for selected records.

This keeps token usage lower and helps agents answer the next decision before carrying unnecessary record detail forward.

## Rerank a bounded shortlist

Use [Rerank Search Results](https://govtribe.com/docs/govtribe-for-agents/tools/rerank-search-results-mcp-tool) when the first retrieval step found a reasonable shortlist, but the next question needs a different ordering goal. MCP clients can use this tool after retrieval as a second-stage ordering pass over at most 50 GovTribe records; it is not a replacement for searching, filtering, sorting, or aggregating.

Prefer `search_results_id` after a typed `Search_*` tool returns a replayable result set. Use `candidates[]` after `Search_GovTribe`, after merging records from multiple searches, or after hand-curating a short list of GovTribe IDs.

Reranking front-loads available strategic priority signals before the record's semantic search text. For award-style records, GovTribe can include obligated value, ceiling value, buyer, awardee, award or contract type, program, vehicle, competition context, UAS or drone indicators, and routine small-BPA cues so ranking goals can weigh more than exact phrase matches. Explicit `candidates[]` snippets are added as candidate context after the record is rehydrated, so agents can preserve useful clues from a previous broad search or hand-curated shortlist.

Keep `max_results` to the number of records the answer needs. When `rerank_status` is `failed_open`, the response returned source order because runtime reranking failed.

## Explore without records using aggregations

Use `aggregations` when the agent needs to understand a search cohort before reading individual records. Aggregations can answer counts, distributions, top-N leaders, value rollups, and other summary questions without returning result rows.

Set `per_page: 0` when the user only needs the rollup. Add filters, date ranges, location filters, categories, or search text first so the aggregation summarizes the intended cohort.

Aggregation-first award rollup:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "query": "\"cloud modernization\"",
  "search_mode": "keyword",
  "aggregations": ["top_awardees_by_dollars_obligated"],
  "per_page": 0
}
```

Use the returned buckets to decide what to do next. For example, an agent might choose a top awardee, agency, location, NAICS code, PSC code, or date window from the rollup before requesting matching records.

## Shape returned records with fields_to_return

Use `fields_to_return` when the agent needs records back. It chooses which fields a dataset-specific `Search_*` tool includes in each returned record; it does not change matching, filtering, sorting, aggregation, paging, or search mode.

| Rule | What it means |
| --- | --- |
| `fields_to_return` is optional. | Omit it when the record ID alone is enough. |
| Allowed values come from the tool reference. | Use the exact field names listed in the selected tool's `Available Fields` table. |
| Omitted or empty requests return `govtribe_id`. | Start there when the next step only needs IDs for follow-up calls. |
| Unselected fields are removed from records. | Request relationship, summary, description, file, contact, category, and financial fields only when the current step needs them. |
| Records do not include high-volume child-record lists. | `fields_to_return` shapes each record's own fields. Smaller related-record arrays such as government files, points of contact, and price lists are still returned inline when requested. Retrieve high-volume children such as task orders, sub-awards, grant awards, or grant opportunities with a second call to the child record's `Search_*` tool. |
| Search scores are explicit. | Typed `Search_*` record rows include `score` as a number when the result is relevance-ranked and `null` when the result set is not score-ranked or a score is unavailable. |

Focused opportunity scan:

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "query": "\"zero trust architecture\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "name",
    "govtribe_url",
    "posted_date",
    "due_date",
    "opportunity_state"
  ],
  "per_page": 10
}
```

Award follow-up for a selected result:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "federal_contract_award_ids": ["<FEDERAL_CONTRACT_AWARD_ID>"],
  "fields_to_return": [
    "govtribe_id",
    "name",
    "govtribe_url",
    "award_date",
    "dollars_obligated",
    "awardee",
    "contracting_federal_agency",
    "place_of_performance"
  ],
  "per_page": 1
}
```

Avoid requesting every available field during the first pass. Add fields only for the shortlisted records that still need deeper review.

## Look up child records in two calls

A record does not carry a list of its high-volume child records. A federal contract IDV does not return its task orders, a federal grant program does not return its grant awards, and a federal contract award does not return its sub-awards. Reaching those child records always takes a second search call.

1. Resolve the parent record. Search for the parent with the tool that owns it and keep the returned `govtribe_id`.

2. Search the child records. Call the child record's `Search_*` tool and pass that ID to the matching parent filter.

The second call is a full search, not a capped sample. It accepts filters, date ranges, sorts, paging, `fields_to_return`, and aggregations, so an agent can rank the child set, page through all of it, or roll it up without reading every row.

### Parent filters on child search tools

| Records the agent wants | Child search tool | Parent filter |
| --- | --- | --- |
| IDVs in a contract vehicle subcategory | `Search_Federal_Contract_IDVs` | `federal_contract_vehicle_subcategory_ids` |
| Awards made from a federal contract opportunity | `Search_Federal_Contract_Awards` | `federal_contract_opportunity_ids` |
| IDVs made from a federal contract opportunity | `Search_Federal_Contract_IDVs` | `federal_contract_opportunity_ids` |
| Task orders under a federal contract IDV | `Search_Federal_Contract_Awards` | `federal_contract_idv_ids` |
| Sub-awards under a federal contract award | `Search_Federal_Contract_Sub_Awards` | `federal_contract_award_ids` |
| Contract awards tied to a DOD acquisition program | `Search_Federal_Contract_Awards` | `dod_acquisition_program_ids` |
| Grant awards under a federal grant program | `Search_Federal_Grant_Awards` | `federal_grant_program_ids` |
| Grant opportunities under a federal grant program | `Search_Federal_Grant_Opportunities` | `federal_grant_program_ids` |
| Grant sub-awards under a federal grant award | `Search_Federal_Grant_Sub_Awards` | `federal_grant_award_ids` |

Not every parent-child pairing has a filter. Blanket purchase agreements held under a parent IDV have no parent filter today. Check the child tool's page in the [MCP tools](https://govtribe.com/docs/govtribe-for-agents/tools) reference before assuming one exists, and narrow with `query`, date ranges, or other available filters when no parent filter is listed.

`federal_contract_opportunity_ids` has one limit worth knowing. GovTribe stores at most 500 opportunity IDs per award or IDV, so a record linked to more opportunities than that, such as a Multiple Award Schedule award, may not match every opportunity it belongs to. When the question involves MAS or another very high-volume schedule, treat an empty result as inconclusive and check `federal_meta_opportunity_ids` or the vehicle relationship before concluding no linked records exist. See [Filter by related records and hierarchies](https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies).

First call, resolve the parent IDV:

Tool: `Search_Federal_Contract_IDVs`

```json
{
  "query": "FA823224D0002",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "name",
    "contract_number"
  ],
  "per_page": 1
}
```

Second call, search the task orders under it:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "federal_contract_idv_ids": ["<FEDERAL_CONTRACT_IDV_ID>"],
  "fields_to_return": [
    "govtribe_id",
    "name",
    "award_date",
    "dollars_obligated",
    "awardee"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 25
}
```

Use `per_page: 0` with `aggregations` on the second call when the question is about the shape of the child set rather than its individual rows.

## Related articles

- [Choose a search mode and write queries](https://govtribe.com/docs/govtribe-for-agents/guides/choose-a-search-mode-and-write-queries): Choose keyword or semantic search and write `query` values that fit the selected tool.
- [Aggregations and leaderboards](https://govtribe.com/docs/govtribe-for-agents/guides/aggregations-and-leaderboards): Use rollups when counts, distributions, or leaderboards answer the question better than rows.
- [Filter by related records and hierarchies](https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies): Understand how parent, category, organization, and connected-record filters match.
- [MCP tools](https://govtribe.com/docs/govtribe-for-agents/tools): Review tool-specific arguments, available fields, filters, sorts, and aggregation keys.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
