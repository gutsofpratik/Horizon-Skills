<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Choose a search mode and write queries

- Canonical GovTribe Docs page: [https://govtribe.com/docs/govtribe-for-agents/guides/choose-a-search-mode-and-write-queries](https://govtribe.com/docs/govtribe-for-agents/guides/choose-a-search-mode-and-write-queries)

Use this guide when a GovTribe MCP search request needs a free-text `query` value or a `search_mode` choice. The selected MCP tool reference remains the source of truth for whether `search_mode` is supported.

## Choose a mode

| Mode | Use for | Query style |
| --- | --- | --- |
| `keyword` | Names, identifiers, exact phrases, literal term overlap, and supported keyword operators. | Search terms, quoted phrases, and supported simple-query operators. |
| `semantic` | Conceptual discovery when the user cares about meaning more than exact words. | Plain-language intent, with a few useful synonyms or paraphrases when they improve recall. |

If the selected tool does not list `search_mode`, omit it and use keyword-style query construction. Use keyword mode when an exact number, code, name, or phrase must match. Use semantic mode when the query is mainly about finding related records or discovering records that may use different terminology.

## Keyword search

Keyword mode runs an Elasticsearch `simple_query_string`-style search. It uses AND as the default operator across unmarked tokens and prioritizes direct term, phrase, and identifier overlap.

Use structured tool arguments for structured constraints. Do not encode agencies, vendors, categories, dates, values, locations, set-asides, statuses, workspace state, or capture state as `field:value` text in `query`.

For why some filters can include related records, hierarchy matches, or role-specific relationships, see [Filter by related records and hierarchies](https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies).

Supported keyword syntax:

| Operator | Function | Use when |
| --- | --- | --- |
| `"..."` | Exact phrase match. | Words must stay together as typed. |
| `+` | Require both terms or groups. | Multiple required concepts must match. |
| `\|` | Match either term or group. | Several terms could express the same idea. |
| `-` | Exclude the immediately following term or quoted phrase. | A positive query needs a specific exclusion. |
| `(...)` | Group terms and control precedence. | Alternatives share another required term. |
| `*` | Match terms that start with the prefix before `*`. | A root term should match several related word forms. |
| `~1`, `~2` | Match close spellings of the preceding term. | Minor spelling variation may otherwise hide results. |

Agents may quote exact identifiers, names, titles, and multi-word phrases; build `+`, `|`, `-`, and parenthetical groups for explicit boolean intent; use trailing `*` only for prefix broadening; and use `~1` or `~2` only when near spelling matches are useful.

Do not use field-scoped syntax such as `agency:NASA`, boosted terms such as `cloud^2`, or Lucene words such as `AND` and `OR`. Use `-` only with at least one positive term or phrase.

### Exact phrases with double quotes

Put quotes around words that must stay together. This is useful for program phrases, source-description language, service names, organization names, identifiers, and uncommon multi-word terms.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "keyword",
  "query": "\"technical peer review\""
}
```

Tool: `Search_Vendors`

```json
{
  "search_mode": "keyword",
  "query": "\"Example Systems LLC\"",
  "fields_to_return": ["govtribe_id", "name", "uei", "govtribe_url"]
}
```

### Required terms with +

Use `+` when two words, phrases, or groups must both match. This narrows a query while still letting each side match its own wording.

Tool: `Search_Federal_Contract_Awards`

```json
{
  "search_mode": "keyword",
  "query": "\"cloud migration\" + security",
  "fields_to_return": ["govtribe_id", "name", "awardee", "dollars_obligated"]
}
```

### Match different terms with |

Use `|` when any one of several terms or phrases can match. This is the keyword OR operator. Do not use uppercase `OR`; GovTribe treats it like search text.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "keyword",
  "query": "\"maintenance\" | \"repair\" | \"modernization\"",
  "fields_to_return": ["govtribe_id", "name", "due_date", "federal_agency"]
}
```

### Exclude terms with -

Use `-` to exclude the next term or quoted phrase. Always include at least one positive term or phrase before the exclusion.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "keyword",
  "query": "cybersecurity -staffing",
  "fields_to_return": ["govtribe_id", "name", "opportunity_state", "due_date"]
}
```

### Group terms with parentheses

Use parentheses when part of the query has several alternatives and another part must still apply. This is useful for compact searches with a shared requirement.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "keyword",
  "query": "\"cyber security\" + (training | exercises)",
  "fields_to_return": ["govtribe_id", "name", "federal_agency", "due_date"]
}
```

### Prefix and fuzzy broadening

Put `*` at the end of a term when matching several words that start the same way would help. Add `~1` or `~2` after a term when a close spelling match may help. Use both sparingly because they can pull in records that are not actually relevant.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "keyword",
  "query": "cloud* migration"
}
```

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "keyword",
  "query": "telematics~1 maintenance"
}
```

## Semantic search

Semantic mode retrieves records by meaning instead of exact word overlap. Keep the `query` value in natural language. Lightly reformulate only when it helps the search intent, such as adding a few high-value synonyms, describing the mission or problem, or softening a narrow phrase that might otherwise miss relevant records.

Keep structured constraints in tool arguments instead of embedding them into the semantic query. Do not use keyword operators in semantic mode.

### Describe the work

Use plain work descriptions when the exact title, category code, or source wording may vary.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "semantic",
  "query": "infrastructure upgrades for public facilities",
  "fields_to_return": ["govtribe_id", "name", "federal_agency", "due_date"]
}
```

### Describe the mission or problem

Use mission- or problem-oriented queries when the user knows what the work supports but not how a record will describe it.

Tool: `Search_Federal_Contract_Awards`

```json
{
  "search_mode": "semantic",
  "query": "financial statement audit and internal control review work",
  "fields_to_return": [
    "govtribe_id",
    "name",
    "awardee",
    "contracting_federal_agency",
    "dollars_obligated"
  ]
}
```

### Explore related wording

Use broader descriptions when the user wants related records that may not share a single phrase. Keep high-value structured constraints as tool arguments.

Tool: `Search_Federal_Contract_Opportunities`

```json
{
  "search_mode": "semantic",
  "query": "secure data linkage and information-sharing systems",
  "naics_category_ids": ["541512"],
  "fields_to_return": ["govtribe_id", "name", "naics_category", "due_date"]
}
```

## Related articles

- [Troubleshoot search results](https://govtribe.com/docs/govtribe-for-agents/guides/troubleshoot-search-results): Adjust GovTribe MCP search calls when results are too broad, too narrow, unrelated, or missing expected records.
- [Filter by related records and hierarchies](https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies): Understand how MCP filters can match through agencies, categories, organizations, contacts, jurisdictions, parent records, and related records.
- [Manage search context](https://govtribe.com/docs/govtribe-for-agents/guides/manage-search-context): Use aggregations and focused `fields_to_return` values before requesting richer records.
- [MCP tools](https://govtribe.com/docs/govtribe-for-agents/tools): Review tool-specific arguments, supported search modes, filters, fields, sorts, and aggregation keys.
- [Search GovTribe](https://govtribe.com/docs/govtribe-for-agents/tools/search-govtribe-mcp-tool): Run an integrated GovTribe finder search across public and workspace indexes.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
