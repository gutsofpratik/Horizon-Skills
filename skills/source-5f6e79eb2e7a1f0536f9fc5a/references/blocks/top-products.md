# Block: top-products

A 5-row table of the products with the most session traffic in the selected period, with each product's add-to-cart rate alongside.

## What it shows

| Column | Format | Notes |
|---|---|---|
| Top Products by Traffic | Product title | Truncate with ellipsis if very long |
| Sessions | Integer | Sessions that viewed the product page |
| Add to Cart | Percentage with benchmark indicator | ATC sessions ÷ product-view sessions |

The Add to Cart column carries the centered-bar benchmark indicator — each row's ATC rate is compared to the site-wide ATC rate (the topline reference), with the tick at the topline value. Above-topline rates show in success-green; below in warning-orange.

## Data source

Noibu only. Product titles, view events, and ATC events all come from Noibu's session data via the `VIEWED_PRODUCT_TITLES` and `ADDED_TO_CART_PRODUCT_TITLES` collections — works for any merchant Noibu monitors regardless of commerce platform.

If the user has a commerce-platform connector (e.g., Shopify) it can enrich the product titles with images or canonical URLs, but it's not required for this block.

## MCP calls

One query per period. Group by product title (`arrayJoin` on `VIEWED_PRODUCT_TITLES`), with two measures:

```json
{
  "queryInput": {
    "measures": [
      { "aggregate": { "measureAlias": "sessions", "measureFunc": "COUNT", "target": { "field": "SESSION_ID" } } },
      {
        "aggregate": {
          "measureAlias": "atc_sessions",
          "measureFunc": "COUNT",
          "target": { "field": "SESSION_ID" },
          "filters": [{ "fieldName": "ADDED_TO_CART_COUNT", "operator": "GREATER_THAN", "comparisonValues": ["0"] }]
        }
      }
    ],
    "groupBy": {
      "arrayJoin": { "arrayJoinCollection": "VIEWED_PRODUCT_TITLES" }
    },
    "orderBy": { "measureAlias": "sessions", "direction": "DESCENDING" },
    "limit": 5
  }
}
```

Compute `atcPct = atc_sessions / sessions * 100` per row.

## Site-wide ATC rate (for the indicator)

The benchmark tick on each row's indicator is the **site-wide ATC rate over the same period**. Compute it once:

`site_atc_pct = (sessions where ADDED_TO_CART_COUNT > 0) / (sessions where PRODUCT_VIEW_COUNT > 0) × 100`

The skill computes this from one of the existing queries (purchase-funnel pulls these counts already) so this block doesn't need an extra call — just read the values from the funnel block's response if both blocks are enabled. Otherwise, run the site-wide query separately.

## Methodology tooltips

The "Add to Cart" header is spelled out — no acronym tooltip needed.

If the user wants more detail about how the site-wide rate is computed, that lives in the centered-bar indicator's hover tooltip ("X% above/below site avg") which is automatic.

## Empty state

If the user's commerce events aren't being captured by Noibu (no product-view events recorded in the window), render the block with a "No product data in this window — check that product page tracking is firing" message instead of an empty table.

## Polarity

Higher ATC rate is better. Above-topline rows render the indicator in success-green; below in warning-orange.
