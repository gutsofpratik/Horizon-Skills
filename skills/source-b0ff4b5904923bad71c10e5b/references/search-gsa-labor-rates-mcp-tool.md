---
name: search-gsa-labor-rates-mcp-tool
description: Quick reference for the `Search_GSA_Labor_Rates` MCP tool, including search inputs, filters, aggregations, selected fields, and compact JSON examples.
---

# Search GSA Labor Rates

Use this guide for `Search_GSA_Labor_Rates` when the top-level pricing workflow is already clear and you only need the tool mechanics.

## Use this source when
- The question is about GSA Schedule labor-rate rows rather than occupational wages.
- The user needs labor-category, vendor, IDV, vehicle, SIN, category, worksite, education, business-size, clearance, or contract-year context.
- The task is to compare a proposed or modeled rate against visible Schedule labor-rate evidence.

## Core inputs
- `query`: keyword or semantic search text.
- `search_mode`: use `keyword` for exact terms, IDs, contract numbers, SINs, and aggregation-heavy work; use `semantic` for concept discovery.
- `page` and `per_page`: use normal pagination. Set `per_page` to `0` when only aggregations are needed.
- `fields_to_return`: select fields from the current public `Search_GSA_Labor_Rates` schema returned by `Documentation`.
- `aggregations`: request rollups such as price statistics, percentiles, top vendors, top IDVs, top SINs, top categories, and top rate years.
- `sort`: use a `{ "key": "...", "direction": "asc|desc" }` object.

## Common fields
- `govtribe_id`
- `labor_category`
- `price`
- `min_years_experience`
- `contract_start`
- `contract_end`
- `worksite`
- `education_level`
- `business_size`
- `security_clearance`
- `sin`
- `rate_year`
- `rate_group_key`
- `vendor`
- `federal_contract_idv`
- `federal_contract_vehicle`
- `federal_contract_vehicle_subcategories`

## Common filters
- `gsa_labor_rate_ids`
- `vendor_ids`: accepts GovTribe vendor IDs and UEIs.
- `federal_contract_idv_ids`
- `federal_contract_vehicle_ids`
- `federal_contract_vehicle_subcategory_ids`
- `price_range`
- `experience_range`
- `contract_start_date_range`
- `contract_end_date_range`
- `labor_category`
- `vendor_name`
- `contract_number`
- `education_level`
- `worksite`
- `business_size`
- `security_clearance`
- `sin`
- `category`
- `subcategory`
- `rate_year`
- `rate_group_key`

## Useful aggregations
- `price_stats`
- `price_percentiles`
- `min_years_experience_stats`
- `rate_group_count`
- `top_vendors_by_doc_count`
- `top_idvs_by_doc_count`
- `top_vehicles_by_doc_count`
- `top_fcv_subcategories_by_doc_count`
- `top_labor_categories_by_doc_count`
- `top_contract_numbers_by_doc_count`
- `top_education_levels_by_doc_count`
- `top_worksites_by_doc_count`
- `top_business_sizes_by_doc_count`
- `top_security_clearance_values_by_doc_count`
- `top_sins_by_doc_count`
- `top_categories_by_doc_count`
- `top_subcategories_by_doc_count`
- `top_rate_years_by_doc_count`

## Stable rules
- Use `query` plus `search_mode`, not `keyword`, `mode`, `search_by`, or `contract_year`.
- Use `fields_to_return` for row fields; there is no separate `item_fields_to_return`.
- Use `federal_contract_idv_ids` or `contract_number` for the schedule contract anchor. `rate_group_key` is not the IDV; it groups sibling contract-year rows for the same labor-rate family.
- Group sibling contract-year rows with `rate_group_key` and sort by `rateYear` or dates when the user asks for current, next-year, or following-year comparisons.
- Prefer exact entity filters when the vendor, IDV, vehicle, or subcategory is already known.
- Treat returned values as Schedule labor-rate evidence, not wages and not guaranteed payable order rates.

## JSON examples

Broad labor-category search:

```json
{
  "query": "\"program manager\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "labor_category",
    "price",
    "vendor",
    "federal_contract_idv",
    "rate_year"
  ],
  "sort": {
    "key": "price",
    "direction": "asc"
  }
}
```

Aggregation-only filter discovery:

```json
{
  "query": "\"systems engineer\"",
  "search_mode": "keyword",
  "per_page": 0,
  "aggregations": [
    "price_stats",
    "top_labor_categories_by_doc_count",
    "top_education_levels_by_doc_count",
    "top_worksites_by_doc_count",
    "top_sins_by_doc_count",
    "top_rate_years_by_doc_count"
  ]
}
```

Search from a GovTribe vendor entity:

```json
{
  "vendor_ids": [
    "<vendor_govtribe_id_or_uei>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "labor_category",
    "price",
    "vendor",
    "federal_contract_idv"
  ],
  "aggregations": [
    "price_stats",
    "top_idvs_by_doc_count",
    "top_sins_by_doc_count"
  ]
}
```

Search from exact GovTribe MAS IDV entities:

```json
{
  "federal_contract_idv_ids": [
    "<federal_contract_idv_govtribe_id>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "labor_category",
    "price",
    "federal_contract_idv",
    "federal_contract_vehicle",
    "rate_group_key"
  ],
  "aggregations": [
    "price_stats",
    "price_percentiles",
    "top_labor_categories_by_doc_count",
    "top_sins_by_doc_count"
  ]
}
```
