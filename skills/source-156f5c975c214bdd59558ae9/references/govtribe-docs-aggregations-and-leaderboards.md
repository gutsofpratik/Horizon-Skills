<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Aggregations and leaderboards

- Canonical GovTribe Docs page: [https://govtribe.com/docs/govtribe-for-agents/guides/aggregations-and-leaderboards](https://govtribe.com/docs/govtribe-for-agents/guides/aggregations-and-leaderboards)

Use aggregations when the user needs a summary of a scoped search cohort instead of a list of individual records.

## When to use aggregations

Aggregations are the right path for:

- counts and totals
- percentages or ratios
- top lists, rankings, and leaderboards
- distributions by agency, vendor, category, location, or time period
- monthly lifecycle trends, such as posted opportunities by month or active solicitations by due month
- dashboard-style KPI rollups

Aggregation-first analysis should usually keep the default keyword behavior. Do not send `search_mode` unless the selected search tool supports it and the question genuinely needs semantic matching.

## Construction rules

Build the cohort first, then ask for the aggregation.

| Step | Guidance |
| --- | --- |
| Select the search tool. | Choose the `Search_*` tool for the record type being summarized. |
| Add filters. | Apply agency, vendor, category, location, set-aside, status, and date filters before aggregating. |
| Anchor free-text queries precisely. | Use quoted phrases in `query` for named services, programs, work descriptions, identifiers, and other terms that must stay together. |
| Choose aggregation keys. | Use the exact aggregation keys supported by the selected tool. |
| Avoid row payloads when unnecessary. | Use `per_page: 0` for aggregation-only requests. |
| Keep cohorts consistent. | Use the same base filters when comparing counts, percentages, or time windows. |

## Scope the cohort before aggregating

The `query` value defines which records enter the aggregation. If the query is too broad, long-tail matches can skew every returned bucket, including top vendors, agencies, categories, locations, and dollar rollups.

Use `search_mode: "keyword"` with quoted phrase anchors when the user names a specific market, service, program, description, or identifier. If the selected tool does not expose `search_mode`, omit it and still use keyword-style quoted phrases in `query`.

Use `+` when two anchors must both match. For example, prefer `"home oxygen" + "medical equipment"` over `home oxygen delivery and medical equipment support for veterans` when the aggregation should summarize records that mention both core concepts.

Use broader unquoted text, semantic search, prefix matching, or fuzzy matching only when the user asks for exploratory sizing or related-language discovery. When broadening a query, pair it with structured filters when possible and review a small row sample before treating the rollup as authoritative.

## Choose aggregation keys

The tool page is the source of truth for available keys. Common patterns are:

| Need | Common key pattern | Example |
| --- | --- | --- |
| Sum, average, minimum, and maximum values. | `*_stats` | `dollars_obligated_stats` |
| Rank entities by value. | `top_*_by_dollars_obligated` | `top_awardees_by_dollars_obligated` |
| Rank IDV entities by ceiling value. | `top_*_by_ceiling_value` | `top_awardees_by_ceiling_value` |
| Rank entities by result count. | `top_*_by_doc_count` | `top_federal_agencies_by_doc_count` |
| Compare categories or locations. | `top_*_by_doc_count` or `top_*_by_dollars_obligated` | `top_naics_codes_by_doc_count`, `top_locations_by_dollars_obligated` |
| Trend records by month. | `*_date_histogram` | `posted_date_histogram`, `due_date_histogram`, `award_date_histogram`, `last_date_to_order_histogram` |

If the user asks "which vendors/agencies/categories dominate this space?", choose a top-list aggregation. If they ask "how much?" or "how many?", choose a stats aggregation or compare the returned total count.

## Summarize federal transaction values

[Search federal transactions MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-federal-transactions-mcp-tool) covers contract awards, contract IDVs, assistance awards, contract subawards, and assistance subawards. Set `transaction_types` explicitly when the question needs a particular population. For prime contract activity, use `["contract_award", "contract_idv"]`. Omitting the filter leaves the family population unrestricted, including any unrecognized stored families; combining prime and subaward amounts does not produce unduplicated government spending.

| Aggregation | Interpretation |
| --- | --- |
| `transactions_by_type` | Matching transaction counts by family, with each bucket's signed amount in `sum_value.value`. |
| `positive_value_stats` | Statistics for amounts strictly greater than zero. |
| `negative_value_stats` | Statistics for amounts strictly less than zero; the sum remains negative. |
| `dollars_obligated_stats` | Net statistics across present amounts, including actual zeros. |

Transaction dollar statistics and dollar leaderboards use signed `total_value` in USD, including any reported non-federal amount. For +$100 and −$20 actions, the positive sum is $100, the negative sum is −$20, and the net sum is $80. A ceiling-only change adds no obligation dollars. See [Federal award values and transactions](https://govtribe.com/docs/data-model/guides/federal-award-values-and-transactions) for the amount meanings across families.

Zero and missing amounts enter neither positive nor negative statistics. Net statistics exclude absent amounts from their count and average, but already stored zeros cannot be reclassified as missing source amounts. Use family bucket counts to count matching transactions, including those without an amount.

All requested transaction aggregations summarize the full filtered population, independently of the returned page size and the 10,000 hit-count threshold. Each aggregation includes `amount_basis: "total_value"` and `transaction_types` so the agent can state the basis and population with the result. Explicit family selections return their deduplicated list; omitted, null, or empty selections return `transaction_types: null` for the unrestricted family population.

Tool: `Search_Federal_Transactions`

```json
{
  "transaction_types": ["contract_award", "contract_idv"],
  "query": "\"cloud migration\"",
  "aggregations": [
    "transactions_by_type",
    "positive_value_stats",
    "negative_value_stats",
    "dollars_obligated_stats"
  ],
  "per_page": 0
}
```

## Use date histograms for monthly trends

Date histogram aggregations return monthly buckets for the scoped result set. Use them when the user needs timing, workload, or trend context before reviewing individual records.

Common date histogram bucket fields are:

| Field | Meaning |
| --- | --- |
| `key` | The bucket timestamp value returned by the tool. |
| `key_as_string` | The formatted month label, such as `2026-06`. |
| `doc_count` | The number of matching records in that month. |

Scope the cohort before interpreting monthly buckets. For opportunity work, apply filters such as agency, NAICS, PSC, set-aside, vehicle, opportunity type, opportunity status, posted date, or due date before using `posted_date_histogram` or `due_date_histogram`.

Use `per_page: 0` for aggregation-only requests. When charting a trend, treat returned buckets as the matched months in the scoped cohort; add zero-value months only after you have chosen the full comparison window.

## Summarize workspace portfolio work

Workspace portfolio rollups use the same aggregation pattern as public-record searches: build the cohort first, then request the summary. `Search_Pursuits` is the main portfolio rollup tool because pursuits carry pipeline, stage, owner, creator, tag, value, due-date, estimated-award-date, and updated-date fields.

Common pursuit portfolio questions include:

| Need | Use |
| --- | --- |
| Total estimated and probable pursuit value. | `estimated_value_stats`, `probable_value_stats` |
| Pipeline, stage, owner, creator, or tag distribution. | `top_pipelines_by_doc_count`, `top_stages_by_doc_count`, `top_owners_by_doc_count`, `top_creators_by_doc_count`, `top_tags_by_doc_count` |
| Due-date and estimated-award timing. | `due_date_histogram`, `estimated_award_date_histogram` |
| Recently updated versus stale pursuits. | `updated_at_histogram`, `updated_at_staleness` |

For pipeline-level stage distribution, call `Search_Pursuits` with `pipeline_ids` and `top_stages_by_doc_count`. `Search_Pipelines` summarizes pipeline records by owner, creator, and tag, but pipeline records do not expose a per-stage pursuit distribution aggregation.

Portfolio value and timing:

Tool: `Search_Pursuits`

```json
{
  "aggregations": [
    "estimated_value_stats",
    "probable_value_stats",
    "due_date_histogram",
    "estimated_award_date_histogram"
  ],
  "per_page": 0
}
```

Pipeline stage distribution:

Tool: `Search_Pursuits`

```json
{
  "pipeline_ids": ["<pipeline_govtribe_id>"],
  "aggregations": [
    "top_stages_by_doc_count"
  ],
  "per_page": 0
}
```

Pipeline owner and tag distribution:

Tool: `Search_Pipelines`

```json
{
  "aggregations": [
    "top_owners_by_doc_count",
    "top_creators_by_doc_count",
    "top_tags_by_doc_count"
  ],
  "per_page": 0
}
```

## Interpret stale pursuit buckets

`updated_at_staleness` groups the scoped pursuit cohort into four recency buckets:

| Bucket | Meaning |
| --- | --- |
| `updated_last_7_days` | Pursuits updated in the last 7 days. |
| `updated_8_to_30_days_ago` | Pursuits last updated 8 to 30 days ago. |
| `updated_31_to_90_days_ago` | Pursuits last updated 31 to 90 days ago. |
| `stale_over_90_days` | Pursuits not updated in more than 90 days. |

Use owner, creator, pipeline, stage, tag, or pursuit ID filters before requesting stale buckets when the user asks about a specific team member, pipeline, capture lane, or shortlist. Use the returned buckets to decide whether to follow up with row-level searches for specific owners, stages, or pipelines.

## Percentages and matched cohorts

For percentage questions, run matched numerator and denominator requests. The denominator request should represent the full scoped population. The numerator request should use the same scope plus the qualifying condition.

Denominator:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "award_date_range": {
    "from": "now-12M/d",
    "to": "now/d"
  },
  "aggregations": ["dollars_obligated_stats"],
  "per_page": 0
}
```

Numerator:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "award_date_range": {
    "from": "now-12M/d",
    "to": "now/d"
  },
  "set_aside_types": ["Total Small Business"],
  "aggregations": ["dollars_obligated_stats"],
  "per_page": 0
}
```

## Displaying rollups

Use [Show stats display](https://govtribe.com/docs/govtribe-for-agents/tools/show-stats-display-mcp-tool) for KPI cards, totals, averages, percentages, and small metric groups.

Use [Show chart](https://govtribe.com/docs/govtribe-for-agents/tools/show-chart-mcp-tool) for standard inline trend, comparison, or leaderboard charts when the aggregation output can be converted into clean rows and series.

Use a text answer when the result is small, exploratory, or primarily a decision about which follow-up search to run.

## Examples

Award value and top awardees:

Tool: `Search_Federal_Contract_Awards`

```json
{
  "query": "\"cloud migration\"",
  "search_mode": "keyword",
  "award_date_range": {
    "from": "now-2y/d",
    "to": "now/d"
  },
  "naics_category_ids": ["541512"],
  "aggregations": [
    "dollars_obligated_stats",
    "top_awardees_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Opportunity count leaders by agency and NAICS:

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "query": "\"cybersecurity support\"",
  "search_mode": "keyword",
  "due_date_range": {
    "from": "now/d",
    "to": "now+90d/d"
  },
  "set_aside_types": ["Total Small Business"],
  "aggregations": [
    "top_federal_agencies_by_doc_count",
    "top_naics_codes_by_doc_count"
  ],
  "per_page": 0
}
```

Opportunity due-month trend and lifecycle mix:

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "opportunity_types": ["Solicitation"],
  "due_date_range": {
    "from": "now/d",
    "to": "now+12M/d"
  },
  "aggregations": [
    "due_date_histogram",
    "top_opportunity_states_by_doc_count"
  ],
  "per_page": 0
}
```

IDV ceiling leaders and ordering-window trend:

Tool: `Search_Federal_Contract_IDVs`

```json
{
  "query": "\"cybersecurity operations\"",
  "search_mode": "keyword",
  "aggregations": [
    "ceiling_value_stats",
    "top_awardees_by_ceiling_value",
    "last_date_to_order_histogram"
  ],
  "per_page": 0
}
```

Chart a leaderboard after converting aggregation buckets to rows:

Tool: `Show_Chart`

```json
{
  "id": "top-awardees-by-obligation",
  "kind": "leaderboard",
  "title": "Top awardees by obligated dollars",
  "rows": [
    {
      "awardee": "Example Systems LLC",
      "dollars_obligated": 128500000
    },
    {
      "awardee": "Example Mission Services Inc.",
      "dollars_obligated": 74200000
    }
  ],
  "labelKey": "awardee",
  "series": [
    {
      "key": "dollars_obligated",
      "label": "Dollars obligated"
    }
  ],
  "valueFormat": {
    "kind": "currency",
    "currency": "USD",
    "compact": true
  },
  "maxItems": 10
}
```

Display KPI cards after extracting stats:

Tool: `Show_Stats_Display`

```json
{
  "id": "award-rollup",
  "title": "Award cohort summary",
  "stats": [
    {
      "key": "award_count",
      "label": "Awards",
      "value": 384,
      "format": {
        "kind": "number",
        "compact": true
      }
    },
    {
      "key": "total_obligated",
      "label": "Total obligated",
      "value": 2145000000,
      "format": {
        "kind": "currency",
        "currency": "USD",
        "compact": true
      }
    }
  ]
}
```

## Related articles

- [MCP tools](https://govtribe.com/docs/govtribe-for-agents/tools): Review tool-specific aggregation keys and filter fields.
- [Date filtering](https://govtribe.com/docs/govtribe-for-agents/guides/date-filtering): Build date-bounded cohorts before rollups.
- [Location filtering](https://govtribe.com/docs/govtribe-for-agents/guides/location-filtering): Build location-scoped cohorts before rollups.
- [Show stats display](https://govtribe.com/docs/govtribe-for-agents/tools/show-stats-display-mcp-tool): Render KPI-style rollups from structured stat values.
- [Show chart](https://govtribe.com/docs/govtribe-for-agents/tools/show-chart-mcp-tool): Render standard trend, comparison, or leaderboard charts.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
