---
name: search-service-contract-inventory-mcp-tool
description: Guide for using `Search_Service_Contract_Inventory` as service-labor footprint, workshare, FTE, and derived hourly-rate context in pricing and price-to-win workflows.
---

# Search Service Contract Inventory

Use this guide when pricing work needs Service Contract Inventory context.

`Search_Service_Contract_Inventory` is not a wage source, not a MAS ceiling-rate source, and not a substitute for award or transaction history. It is useful when a service-heavy pricing workflow needs to understand reported contractor labor footprint, incumbent workshare, FTE/hour intensity, subcontractor reliance, agency/vendor footprint, and derived hourly-rate context.

## Best Uses
- Price-to-win and recompete pricing for professional services, O&M, help desk, staff augmentation, and other labor-heavy service work
- Contractor-reliance and workforce-rebalancing context that affects staffing realism
- Incumbent or predecessor workshare analysis across prime and subcontractor slices
- FTE, hours, and subcontractor intensity checks against a proposed labor mix
- Derived hourly-rate context on prime records when paired with BLS, GSA labor-rate, line-item, award, or company-provided pricing evidence

## Core Contract
This tool follows the standard GovTribe `Search_*` shape.

Use:
- `query`
- `page`
- `per_page`
- `search_mode`
- `aggregations`
- `sort`
- `fields_to_return`

Use `keyword` search mode for exact contract numbers, vendors, IDs, fiscal years, and aggregation-heavy work. The SCI search is keyword-only.

## Most Useful Filters
- `service_contract_inventory_record_ids`
- `fiscal_year`
- `role`: use `prime` for row-level dollar, total-hour, and derived-rate context; use `sub` for subcontractor hour and FTE slices.
- `vendor_ids`
- `federal_contract_award_ids`
- `federal_contract_idv_ids`
- `psc_category_ids`
- `naics_category_ids`
- `contracting_federal_agency_ids`
- `funding_federal_agency_ids`
- `contract_number`
- `place_of_performance_state`
- `place_of_performance_country`
- `date_signed_range`
- `base_effective_date_range`
- `hours_invoiced_range`
- `ftes_range`
- `total_dollar_amount_invoiced_range`
- `total_contractor_hours_invoiced_range`
- `total_ftes_range`
- `subcontractor_count_range`
- `sub_hours_share_range`
- `derived_hourly_rate_range`

## Most Useful Aggregations
- `hours_invoiced_stats`
- `ftes_stats`
- `total_dollar_amount_invoiced_stats`
- `total_contractor_hours_invoiced_stats`
- `total_ftes_stats`
- `subcontractor_count_stats`
- `sub_hours_share_stats`
- `derived_hourly_rate_stats`
- `top_fiscal_years_by_doc_count`
- `top_roles_by_doc_count`
- `top_vendors_by_doc_count`
- `top_awards_by_doc_count`
- `top_idvs_by_doc_count`
- `top_psc_categories_by_doc_count`
- `top_naics_categories_by_doc_count`
- `top_contracting_agencies_by_doc_count`
- `top_funding_agencies_by_doc_count`
- `top_place_of_performance_states_by_doc_count`
- `top_contract_numbers_by_doc_count`

## Most Useful Returned Fields
- `govtribe_id`
- `fiscal_year`
- `role`
- `contract_number`
- `description`
- `place_of_performance`
- `hours_invoiced`
- `ftes`
- `total_dollar_amount_invoiced`
- `total_contractor_hours_invoiced`
- `total_ftes`
- `total_dollars_obligated`
- `total_base_and_all_options_value`
- `subcontractor_count`
- `sub_hours_share`
- `derived_hourly_rate`
- `vendor`
- `federal_contract_award`
- `federal_contract_idv`
- `psc_category`
- `naics_category`
- `contracting_federal_agency`
- `funding_federal_agency`
- `source_url`

## Working Rules
- Use SCI as a context layer for pricing, not as the sole pricing answer.
- Use `role: ["prime"]` and `subcontractor_count_range.max = 0` when the user needs a cleaner derived hourly-rate proxy.
- Treat `derived_hourly_rate` as source-row context based on total dollars invoiced divided by total contractor hours invoiced. It is not a loaded labor-category rate and it may blend labor, workshare, fee, and scope effects.
- Do not use subcontractor records for per-subcontractor pricing; SCI does not report per-subcontractor dollars.
- Pair SCI with `BLS_Occupational_Wage_Data` for wage/cost realism, `Search_GSA_Labor_Rates` for market-visible ceiling-rate context, `Search_Line_Items` for awarded unit-price evidence, and federal award/IDV tools for award lifecycle and obligations.
- For PTW, use SCI to challenge staffing volume, incumbent labor intensity, and prime/sub workshare assumptions before narrowing the recommended range.

## Examples
Find prime-only service records with higher derived hourly-rate context:

```json
{
  "role": ["prime"],
  "derived_hourly_rate_range": {
    "min": 150
  },
  "subcontractor_count_range": {
    "max": 0
  },
  "fields_to_return": [
    "govtribe_id",
    "fiscal_year",
    "contract_number",
    "description",
    "derived_hourly_rate",
    "total_dollar_amount_invoiced",
    "total_contractor_hours_invoiced",
    "total_ftes",
    "vendor",
    "federal_contract_award"
  ],
  "sort": {
    "key": "derivedHourlyRate",
    "direction": "desc"
  }
}
```

Summarize workshare context for a service-heavy PTW review:

```json
{
  "query": "\"help desk\"",
  "search_mode": "keyword",
  "fiscal_year": [2024],
  "per_page": 0,
  "aggregations": [
    "hours_invoiced_stats",
    "total_dollar_amount_invoiced_stats",
    "total_ftes_stats",
    "subcontractor_count_stats",
    "sub_hours_share_stats",
    "top_vendors_by_doc_count",
    "top_contracting_agencies_by_doc_count",
    "top_psc_categories_by_doc_count",
    "top_roles_by_doc_count"
  ]
}
```
