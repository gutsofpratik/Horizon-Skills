---
name: bls-occupational-wage-data-mcp-tool
description: Quick reference for the `BLS_Occupational_Wage_Data` MCP tool, including modes, response shaping, stable row fields, and compact JSON examples.
---

# BLS Occupational Wage Data

Use this guide for `BLS_Occupational_Wage_Data` when the top-level pricing workflow is already clear and you only need the BLS tool mechanics.

## Use this source when
- The question is about occupational wages by role, geography, industry, or level.
- The user needs a wage baseline that may later be escalated or burdened.
- The user starts with a business-facing labor role and needs the closest defensible BLS proxy title.

## Modes
- `filters`: discover legal next-step narrowing values and modeling defaults
- `search`: return wage rows that can be reviewed or used in pricing analysis

## Default response shapes
- `search`
  - `items`
  - `summary`
  - `empty`
- `filters`
  - `occupation_names`
  - `occupation_codes`
  - `occupation_levels`
  - `states`
  - `industries`
  - `areas`
  - `summary`
  - `modeling_presets`

## Top-level response shaping
Use `fields_to_return` to retain only the top-level fields needed for the current step.

### Allowed `search` fields
- `items`
- `aggregations`
- `summary`
- `empty`

### Allowed `filters` fields
- `occupation_names`
- `occupation_codes`
- `occupation_levels`
- `states`
- `industries`
- `areas`
- `summary`
- `modeling_presets`

## Search row fields
Use `item_fields_to_return` in `search` mode to retain only the row attributes you need under `items`.

- `_id`
- `sort`
- `area_name`
- `area_code`
- `areatype_code`
- `bls_with_footnotes_id`
- `industry_code`
- `industry_name`
- `occupation_name`
- `occupation_code`
- `occupation_level`
- `rate`
- `h_mean`
- `h_median`
- `national_h_mean`
- `national_h_median`
- `series_year`
- `state_name`
- `state_code`
- `load_date`
- `footnote_codes_series`
- `footnote_codes_value`
- `footnote_text_series`
- `footnote_text_value`

## Stable rules
- Use `keyword` as the occupation anchor.
- Treat `occupation_name` and `occupation_code` as keyword aliases, not raw filters.
- Use `filters` mode output as the source of valid narrowing values.
- When narrowing to one area, pass both `area_name` and `normalized_area_name`.
- When location plus narrow industry causes weak results, try `000000` / `All Industries`.
- Treat returned values as wage-oriented modeling inputs, not fully burdened bill rates, not standalone pricing conclusions, and not contract ceiling rates or awarded prices.

## JSON examples

Broad occupation discovery:

```json
{
  "mode": "filters",
  "keyword": "program manager",
  "state_name": ["Virginia"]
}
```

Narrow search with response shaping:

```json
{
  "mode": "search",
  "keyword": "Project Management Specialists",
  "occupation_level": ["Senior"],
  "state_name": ["Virginia"],
  "fields_to_return": ["items", "summary"],
  "item_fields_to_return": ["_id", "occupation_name", "occupation_level", "state_name", "rate", "h_median"],
  "ordering": "rate",
  "sort": "asc"
}
```

Search using a GovTribe NAICS category id:

```json
{
  "mode": "search",
  "keyword": "Project Management Specialists",
  "state_name": ["Virginia"],
  "naics_category_ids": ["<govtribe_naics_category_id>"],
  "fields_to_return": ["items", "summary"]
}
```

Search with raw aggregations explicitly requested:

```json
{
  "mode": "search",
  "keyword": "Project Management Specialists",
  "state_name": ["Virginia"],
  "fields_to_return": ["items", "aggregations", "summary", "empty"]
}
```
