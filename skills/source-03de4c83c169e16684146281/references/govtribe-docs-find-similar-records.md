<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Find similar records

- Canonical GovTribe Docs page: [https://govtribe.com/docs/govtribe-for-agents/guides/find-similar-records](https://govtribe.com/docs/govtribe-for-agents/guides/find-similar-records)

Use `similar_filter` when an agent has one useful GovTribe record and needs to find comparable or related records through a supported `Search_*` MCP tool. Similarity is useful for follow-on discovery, likely bidders, comparable awards, related opportunities, similar vendors, and past-performance research.

## What `similar_filter` does

`similar_filter` accepts a `govtribe_type` and `govtribe_id` for a source record. GovTribe prefers the source record's AI summary, then uses other substantive descriptive text when an AI summary is unavailable. Depending on the record type, that fallback can include descriptions, title or name fields, pursuit description, linked pursuit record context, buyer or category context, and other usable text signals.

The request shape does not change when GovTribe uses fallback text. GovTribe normalizes fallback text and ignores blank, placeholder, or very short values so weak source records do not become poor similarity anchors.

The selected tool still controls the returned record type, filters, sorts, fields, and whether rows or aggregations are returned. Check the tool page before using `similar_filter`; not every search tool exposes it.

## When to use it

Use `similar_filter` when the user wants records like a known record, not merely records that share one field value.

| User need | MCP pattern |
| --- | --- |
| Find likely bidders for an opportunity. | Search vendors or awards with `similar_filter` from the opportunity, plus agency, category, or date filters when needed. |
| Find predecessor or follow-on work. | Search awards, IDVs, forecasts, or opportunities with `similar_filter` from the known record. |
| Find comparable past performance. | Search awards using `similar_filter` from a target opportunity or award, then add vendor or category filters if needed. |
| Expand from one strong file or record. | Search the relevant record type with `similar_filter`, then inspect returned relationship fields. |

Use direct ID filters when the user asks for records tied to a specific agency, vendor, category, vehicle, IDV, pursuit, or saved search. Use `query` when the important part is wording. Use `similar_filter` when the whole source record is the anchor.

## Request shape

`similar_filter` uses this shape:

```json
{
  "similar_filter": {
    "govtribe_type": "<GOVTRIBE_TYPE>",
    "govtribe_id": "<GOVTRIBE_ID>"
  }
}
```

The source record must exist and have enough summary or fallback descriptive text for similarity search. If the tool returns `similar_filter_source_has_no_similarity_text`, choose another source record, remove `similar_filter`, or use `query` plus structured filters instead.

## Add constraints carefully

Combine `similar_filter` with filters when the user cares about a specific cohort, but avoid over-constraining the request before reviewing the result shape.

- Add date filters for recency, due dates, award windows, or completion horizons.
- Add agency, vendor, category, location, or set-aside filters only when they are part of the user's actual scope.
- Use `fields_to_return` to keep the first pass compact.
- Treat `aggregations` with `similar_filter` as exploratory. Because `similar_filter` uses a semantic source-record signal, aggregation buckets can include near-neighbor matches that are useful for discovery but less reliable as final counts, rankings, or leaderboards. Review a small row sample, add structured filters when possible, and follow [aggregation cohort-scoping guidance](https://govtribe.com/docs/govtribe-for-agents/guides/aggregations-and-leaderboards#scope-the-cohort-before-aggregating) before treating the rollup as authoritative.

## Examples

Find opportunities similar to a known opportunity:

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "similar_filter": {
    "govtribe_type": "federal_contract_opportunity",
    "govtribe_id": "<FEDERAL_CONTRACT_OPPORTUNITY_ID>"
  },
  "due_date_range": {
    "from": "now/d",
    "to": "now+180d/d"
  },
  "fields_to_return": ["govtribe_id", "name", "govtribe_url", "due_date", "federal_agency"],
  "per_page": 10
}
```

Find comparable awards for past-performance analysis:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "similar_filter": {
    "govtribe_type": "federal_contract_opportunity",
    "govtribe_id": "<FEDERAL_CONTRACT_OPPORTUNITY_ID>"
  },
  "award_date_range": {
    "from": "now-5y/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "name",
    "awardee",
    "contracting_federal_agency",
    "dollars_obligated",
    "award_date"
  ],
  "per_page": 10
}
```

Explore a similar-work cohort after reviewing a small row sample:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "similar_filter": {
    "govtribe_type": "federal_contract_award",
    "govtribe_id": "<FEDERAL_CONTRACT_AWARD_ID>"
  },
  "award_date_range": {
    "from": "now-3y/d",
    "to": "now/d"
  },
  "aggregations": [
    "top_awardees_by_dollars_obligated",
    "dollars_obligated_stats"
  ],
  "per_page": 0
}
```

## How Similar differs from query and filters

`query` asks GovTribe to match text or meaning from a user-supplied phrase. Structured filters ask GovTribe to match specific fields or relationships. `similar_filter` asks GovTribe to use the source record as the semantic anchor.

Do not pair `similar_filter` with a broad semantic `query` unless one narrow clarifying phrase is genuinely needed. A broad query can compete with the source-record signal and make the request harder to reason about.

## Related articles

- [Choose a search mode and write queries](https://govtribe.com/docs/govtribe-for-agents/guides/choose-a-search-mode-and-write-queries): Choose when a normal `query` is a better fit than `similar_filter`.
- [Filter by related records and hierarchies](https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies): Use direct relationship filters when the user needs a specific agency, vendor, category, or parent-record relationship.
- [Manage search context](https://govtribe.com/docs/govtribe-for-agents/guides/manage-search-context): Use aggregations and focused returned fields before expanding similar results.
- [Search federal contract opportunities](https://govtribe.com/docs/govtribe-for-agents/tools/search-federal-contract-opportunities-mcp-tool): Review one search tool that supports `similar_filter`.
- [Search federal contract awards](https://govtribe.com/docs/govtribe-for-agents/tools/search-federal-contract-awards-mcp-tool): Review award filtering, returned fields, and aggregation options.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
