# Block: core-kpis

The first row of the dashboard. Five tiles, each showing a single number with a period-over-period delta below it.

## What it shows

| Metric | Format | Comparison |
|---|---|---|
| Sessions | Integer | Δ% vs prior period |
| Engagement | Percentage | Δ percentage points |
| Conversion | Percentage | Δ percentage points |
| AOV | Currency | Δ% vs prior period |
| RPS | Currency | Δ% vs prior period |

Order on the dashboard: Sessions → Engagement → Conversion → AOV → RPS. Don't reorder; this is the canonical first-row of any ecomm dashboard and operators recognize it.

## Data source

Noibu only. No commerce-platform connector required — every metric here is computed from Noibu's session-level data.

## MCP calls

One call per period (current and prior), or one call with `compareToPrevious: true` if the response shape supports it cleanly. Both periods share the same measure shape:

```json
{
  "domainId": "<config.domain.id>",
  "input": {
    "periodOptions": {
      "dateTimeRange": { "startTime": "<period_start>", "endTime": "<period_end>" }
    },
    "queryInput": {
      "measures": [
        { "aggregate": { "measureAlias": "sessions", "measureFunc": "COUNT", "target": { "field": "SESSION_ID" } } },
        { "predefined": { "measure": "BOUNCE_RATE", "measureAlias": "bounce_rate" } },
        { "predefined": { "measure": "CONVERSION_RATE", "measureAlias": "cvr" } },
        { "predefined": { "measure": "REVENUE_PER_SESSION", "measureAlias": "rps" } },
        { "aggregate": { "measureAlias": "aov", "measureFunc": "AVG", "target": { "field": "CHECKOUT_COMPLETE_TOTAL_VALUE" } } }
      ],
      "orderBy": { "measureAlias": "sessions", "direction": "DESCENDING" }
    }
  }
}
```

Compute `engagement = 1 - bounce_rate` client-side. The dashboard's JS handles this — the skill just needs to ship the call.

## Time windows

The dashboard's time selector controls the window:

- **24h** — current: rolling last 24h. Prior: the 24h before that.
- **7d** — current: rolling last 7 days. Prior: the 7 days before that.
- **30d** — current: rolling last 30 days. Prior: the 30 days before that.

All comparisons are vs the prior period of the same length. The dashboard surfaces this with a single line under the header ("All metric changes are compared to the previous period of the same length") so individual deltas don't need to repeat the context.

## Methodology tooltips

Two acronyms in this block need tooltips. Render them with `acronymTip()` (the dotted-underline-on-hover pattern):

- **AOV** → "Average order value — total revenue divided by orders."
- **RPS** → "Revenue per session — total revenue divided by sessions."

One metric needs a definition tooltip even though it's spelled out:

- **Engagement** → "Share of sessions that scrolled or clicked — derived from Noibu's bounce signal (engaged = not bounced)."

## Empty state

If a measure returns null or zero across a window with non-zero sessions, show the value as `—` and the delta as `—`. If sessions itself is zero (no traffic), show the whole tile row with `—` values and a small subtitle like "No traffic in this window." Don't fake the math.

## Polarity

All five metrics are higher-is-better. Up arrows in success-green, down arrows in warning-orange. No inversions to worry about for this block.
