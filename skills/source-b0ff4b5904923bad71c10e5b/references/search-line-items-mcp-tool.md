---
name: search-line-items-mcp-tool
description: Guide for using `Search_Line_Items` to pull state/local awarded line-item pricing evidence, unit prices, quantities, and parent award context.
---

# Search Line Items

Use this guide when the right pricing source is `Search_Line_Items`.

`Search_Line_Items` is for awarded state/local line-item pricing evidence. It is not a wage benchmark and not a MAS ceiling-rate benchmark.

## Best Uses
- Historical awarded unit-price comparisons
- Quantity-backed comparable line items
- State/local pricing evidence tied to a known award, IDV, or vehicle
- Rehydrating nested `line_items` returned by parent award or IDV tools

## Core Contract
This tool follows the standard GovTribe `Search_*` shape, not the pricing-tool `mode` pattern.

Use:
- `query`
- `page`
- `per_page`
- `search_mode`
- `aggregations`
- `sort`
- `fields_to_return`

## Most Useful Filters
- `line_item_ids`: best when the parent tool already returned nested line items
- `state_ids`: narrow to a known state
- `nigp_category_ids`
- `unspsc_category_ids`
- `state_local_contract_award_ids`
- `state_local_contract_idv_ids`
- `state_local_contract_vehicle_ids`
- `unit_of_measurements`
- `unit_price_range`
- `quantity_range`

## Most Useful Aggregations
- `unit_price_stats`
- `quantity_stats`
- `top_unit_of_measurements_by_doc_count`
- `top_nigp_codes_by_doc_count`
- `top_unspsc_codes_by_doc_count`
- `top_states_by_doc_count`

## Most Useful Returned Fields
- `description`
- `unit_price`
- `quantity`
- `unit_of_measure`
- `subtypes`
- `state`
- `state_local_contract_award`
- `state_local_contract_idv`
- `state_local_contract_vehicle`
- `nigp_category`
- `unspsc_category`

## Working Rules
- Use `Search_Line_Items` when the user wants actual awarded line-item evidence, not normalized labor benchmarks.
- Prefer parent entity filters when the contract context is known.
- Use `line_item_ids` when a parent search already gave you the exact nested line items to rehydrate.
- Check `unit_of_measure` before comparing prices. Similar descriptions can still be incomparable if one row is per `Hour` and another is per `Each`.
- Use aggregations early when the result set is large and the user needs fast orientation instead of row-by-row review.
- Do not expect a direct line-item GovTribe URL. Navigation should come from the nested parent award / IDV / vehicle.

## Examples
Find comparable awarded service line items for a known state/local award:

```json
{
  "state_local_contract_award_ids": ["<state_local_contract_award_id>"],
  "fields_to_return": [
    "govtribe_id",
    "description",
    "unit_price",
    "quantity",
    "unit_of_measure",
    "state_local_contract_award",
    "nigp_category",
    "unspsc_category"
  ],
  "sort": {
    "key": "unitPrice",
    "direction": "asc"
  }
}
```

Compare like-for-like rows by unit price and quantity range:

```json
{
  "query": "network switch",
  "unit_of_measurements": ["Each"],
  "unit_price_range": {
    "min": 100,
    "max": 500
  },
  "quantity_range": {
    "min": 1,
    "max": 25
  },
  "fields_to_return": [
    "description",
    "unit_price",
    "quantity",
    "unit_of_measure",
    "state",
    "state_local_contract_idv"
  ]
}
```

Use nested line item ids from a parent award or IDV response:

```json
{
  "line_item_ids": [
    "<line_item_id_1>",
    "<line_item_id_2>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "description",
    "unit_price",
    "quantity",
    "unit_of_measure",
    "state_local_contract_award"
  ]
}
```
