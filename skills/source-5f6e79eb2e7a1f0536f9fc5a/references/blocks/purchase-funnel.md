# Block: purchase-funnel

A 5-step vertical bar funnel. Each step is a column with a header (label + headline value + period-over-period delta) above a bar. Bars occupy the left half of each column; a gradient trapezoid in the right half visually links each bar to the next. Hovering a bar or the grey drop-zone above it surfaces a tooltip with the absolute session count and the number of sessions lost from the previous step.

**Headline value:** for step 1, the absolute session count (e.g. `7,209 sessions`); for steps 2–5, the percentage of step 1 (e.g. `49.3%`). Both lead with `↑`/`↓ Npp` next to them when there's period-over-period change.

## What it shows

| Step | Definition | Source |
|---|---|---|
| 1 | Enter store | All sessions |
| 2 | View product | Sessions with `PRODUCT_VIEW_COUNT > 0` |
| 3 | Add to cart | Sessions with `CONVERSION_FUNNEL_DEPTH ≥ 1` |
| 4 | Start checkout | Sessions with `CONVERSION_FUNNEL_DEPTH ≥ 2` |
| 5 | Checkout complete | Sessions with `CONVERSION_FUNNEL_DEPTH = 4` |

Notice the Add to Cart step uses funnel depth, not the explicit ATC event count. This is intentional and is documented in the methodology tooltip below — see the "Add to cart" entry. It keeps the funnel monotonic when sessions reach cart stage via express-checkout flows.

## Data source

Noibu only.

## MCP calls

Two queries per period (current and prior), in parallel:

**Query 1 — Funnel depth distribution.** Group sessions by `CONVERSION_FUNNEL_DEPTH`:

```json
{
  "queryInput": {
    "measures": [
      { "aggregate": { "measureAlias": "sessions", "measureFunc": "COUNT", "target": { "field": "SESSION_ID" } } }
    ],
    "groupBy": { "fieldSegments": ["CONVERSION_FUNNEL_DEPTH"] }
  }
}
```

Returns one row per depth bucket (null, 1, 2, 3, 4). Compute cumulative reach:

- Step 3 (Add to cart) = sum of rows where depth ≥ 1
- Step 4 (Start checkout) = sum of rows where depth ≥ 2
- Step 5 (Checkout complete) = row where depth = 4
- Step 1 (Enter store) = sum of all rows

**Query 2 — Product-view sessions.** Depth doesn't track product views as a step. Separate query:

```json
{
  "queryInput": {
    "measures": [
      {
        "aggregate": {
          "measureAlias": "pv_sessions",
          "measureFunc": "COUNT",
          "target": { "field": "SESSION_ID" },
          "filters": [{ "fieldName": "PRODUCT_VIEW_COUNT", "operator": "GREATER_THAN", "comparisonValues": ["0"] }]
        }
      }
    ]
  }
}
```

## Computed values

For each step, the dashboard renders three things:

1. `pctReach` = step_count / step_1_count × 100 (the percentage label above the bar)
2. `pctDelta` = current_pctReach − prior_pctReach (in percentage points; the small colored delta)
3. Tooltip on hover: total session count + drop-offs from previous step (`prev.count − this.count`)

## Bar height scaling

Bar 1 (Enter store) is always anchored at full chart height — it's the funnel's denominator and can never be smaller than later steps. Bars 2..5 are sqrt-scaled relative to bar 1 so smaller drop-off steps stay readable without dwarfing.

If bar 2's natural height would fall below 55% of the chart (extreme drop-off cases), the dashboard scales bars 2..5 up to keep them readable and renders bar 1 with a sawtooth-cut top to indicate it's been compressed for scale. For typical ecomm conversion rates this never triggers; for stores with steep first-step drops it kicks in automatically.

## Methodology tooltips

One term in this block needs a tooltip:

- **Add to cart** → "Counts sessions that reached cart stage by any means, including express-checkout flows that bypass the standard add-to-cart event."

The reason: `CONVERSION_FUNNEL_DEPTH ≥ 1` includes sessions that went straight from product page to checkout via Apple Pay / Shop Pay / Buy Now buttons without firing an explicit add-to-cart event. If we used `ADDED_TO_CART_COUNT > 0` instead, the funnel would be non-monotonic (Start Checkout could include sessions not in Add to Cart). Depth-based counting fixes that and is more accurate to "reached cart-intent stage."

## Empty state

If sessions = 0 in the window, render the funnel block with all bars at MIN_H and a centered "No traffic in this window" overlay.

If a step count > 0 but earlier step count = 0 (data anomaly), don't render the bar — show "—" for the percentage and skip the bar visual.
