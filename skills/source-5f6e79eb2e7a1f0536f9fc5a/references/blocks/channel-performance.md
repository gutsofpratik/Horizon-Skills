# Block: channel-performance

A 6-row table showing how each traffic channel is performing — sessions, engagement, conversion, and revenue per session.

## What it shows

| Column | Format | Notes |
|---|---|---|
| Channel | String | One of six buckets (see channel mapping below) |
| Sessions | Integer | Channel volume |
| Engagement | Percentage with benchmark indicator | vs site-wide engagement |
| Conversion | Percentage with benchmark indicator | vs site-wide conversion |
| RPS | Currency with benchmark indicator | vs site-wide RPS |

The last three columns each carry a centered-bar benchmark indicator showing how the channel compares to the site-wide average for that metric.

## Channel mapping

Noibu returns sessions grouped by `UTM_SOURCE` (and optionally `UTM_MEDIUM`). The skill buckets these into six rows:

| Channel | Match rule |
|---|---|
| Direct | `utm_source` is empty/null |
| Paid | `utm_medium` ∈ (cpc, ppc, paid, paid_social, paidsocial) |
| Organic | `utm_medium` = organic OR referrer matches a search engine domain (google.com, bing.com, etc.) |
| Email | `utm_medium` = email OR `utm_source` matches known email tools (klaviyo, mailchimp, shopify_email, etc.) |
| Social | `utm_medium` = social OR `utm_source` matches social platforms (facebook, fb, instagram, ig, tiktok, twitter, etc.) |
| Referral | Anything else with a `utm_source` |

The skill applies this mapping after the query returns. Order rows by sessions descending.

## Data source

Noibu only. UTM data and revenue both come from Noibu's session-level fields.

## MCP calls

One query per period, grouped by `UTM_SOURCE` and `UTM_MEDIUM`:

```json
{
  "queryInput": {
    "measures": [
      { "aggregate": { "measureAlias": "sessions", "measureFunc": "COUNT", "target": { "field": "SESSION_ID" } } },
      { "predefined": { "measure": "BOUNCE_RATE", "measureAlias": "bounce_rate" } },
      { "predefined": { "measure": "CONVERSION_RATE", "measureAlias": "cvr" } },
      { "predefined": { "measure": "REVENUE_PER_SESSION", "measureAlias": "rps" } }
    ],
    "groupBy": { "fieldSegments": ["UTM_SOURCE", "UTM_MEDIUM"] },
    "orderBy": { "measureAlias": "sessions", "direction": "DESCENDING" },
    "limit": 50
  }
}
```

After the query returns, apply the channel mapping above. Aggregate rows that fall into the same bucket: sum sessions, weighted-average engagement / CVR / RPS by sessions.

## Site-wide reference (for indicators)

The benchmark tick on each row's indicators is the site-wide value of that metric for the same period. If the `core-kpis` block is enabled, read those values from its response. If not, run a separate site-wide query (same shape as the per-channel query but without `groupBy`).

## Methodology tooltips

- **Direct** (the row label) → "Sessions with no UTM source. Includes typed URLs, bookmarks, in-app browsers, and links with stripped referrer data — so it may absorb some untagged paid or social traffic."
- **RPS** (column header) → "Revenue per session — channel revenue divided by channel sessions."

The Engagement and Conversion column headers don't need tooltips — they're spelled out, and the engagement definition is already covered in the core-kpis tooltip if that block is on the dashboard.

## Empty state

If a channel bucket has zero sessions in the window, omit the row entirely — don't render an empty row with dashes. If ALL non-direct buckets are empty (the user has no UTM tracking set up), render the block with just the Direct row and a small note: "No tagged traffic in this window."

## Polarity

All four metrics are higher-is-better. Above-site indicators in success-green; below in warning-orange.
