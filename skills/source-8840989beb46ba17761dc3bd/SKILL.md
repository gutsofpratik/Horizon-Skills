---
name: app-health
description: Generate a shareable health report for one application, summarizing engagement, acquisition, retention, average time, stickiness, frustration signals, and survey scores into a verdict and next steps. Use this skill whenever someone asks how healthy an app is, wants an app health report, wants an overall picture of how an application is doing, or asks about an app's engagement, retention, stickiness, or friction at the application level — even if they don't say "app health" explicitly. This is app-level (a whole application), not account-level — for a single customer account use account-health, and for a single feature use feature-adoption.
---

# App Health Report

Produce a shareable health report for one app, covering how many people use it, whether it keeps gaining and holding on to them, how engaged they are while they are there, where they hit friction, and how they rate it — then reach a verdict and recommend next steps.

## Tools

This skill uses **Pendo MCP tools** exclusively. All tool references below refer to the Pendo connector tools (prefixed `Pendo:` in the tool list).

Before starting, call `Pendo:list_all_applications` to get the available subscription IDs and app IDs. Every subsequent Pendo tool call requires a `subId` (subscription ID) and the app-level tools require an `appId`. The health metrics come from:

- `Pendo:appUsage` — active visitors/accounts, event volume, average time, and the four frustration counts (rage clicks, dead clicks, error clicks, u-turns), scoped to one app via `appId`.
- `Pendo:appUsageTimeSeries` — the same usage metrics as a per-period (weekly or daily) trend across the window; also the basis for the monthly DAU/MAU stickiness ratios.
- `Pendo:acquisitionTrend` — new visitors and new accounts (first interaction inside the window) per period.
- `Pendo:cohortRetentionCurve` — the retention curve for the app's new visitors, with cohort size per period.
- `Pendo:surveyScores` — NPS, CSAT, and PMF survey scores with response counts.
- `Pendo:activityQuery` — page/feature-level breakdown to locate where frustration is concentrated when a category needs drill-down.

## Parameters

- **app_id**: The application to report on (resolved in Step 0).
- **timeframe**: The time period for analysis (default: last 90 days).

## Step 0: Resolve and Confirm the App

The report covers **one** app. Resolve `app_id` before gathering any data.

1. Call `Pendo:list_all_applications`. If there is exactly one application, use it (state which one).
2. If the user named an app, match it to an application in the list.
3. If there are multiple applications and the user hasn't specified one, present the list and ask which app to report on. Do not silently pick.
4. If the user names several apps, report on one and say which — or ask which they want.

## Questions This Report Answers

This is the contract — the report is judged on whether it answers these.

1. **Engagement** — How many visitors and accounts are active in the app, how much are they doing, and is that growing or declining versus the prior period?
2. **Acquisition** — How many new visitors and accounts is the app gaining, and is that rate rising or falling?
3. **Retention** — Do the visitors the app acquires keep coming back, and where does the retention curve settle?
4. **Average time** — How long are visitors spending in the app, and is that trending up or down?
5. **Stickiness** — How often do active visitors come back — the DAU/MAU ratio — and is it improving?
6. **Frustration signals** — Where are visitors hitting friction (rage clicks, dead clicks, error clicks, u-turns), is friction rising, and what is it concentrated on?
7. **Survey scores** — What do NPS, CSAT, and PMF survey responses say about how users feel about the app, and how has that moved?
8. **Verdict** — Taken together, is the app healthy, mixed, showing concern, or at risk — and what next steps should be taken?

## Evidence the Report Needs

Use a 90-day window unless the user specifies otherwise. Scope every metric to the resolved app — pass the `app_id` explicitly in every data-gathering request — and keep that scope identical between a metric and its comparison period: a count and its baseline must cover the same app over the same length of window, or the trend is meaningless. Stickiness is the one metric that is not measured over the full window — see below. Gather these in parallel where possible.

- **Engagement** (`appUsage`, `appUsageTimeSeries`): active visitors, active accounts, and event volume for the window and for the prior equivalent window, plus a per-period (weekly or daily) trend across the window so a shift in momentum is visible.
- **Acquisition** (`acquisitionTrend`): new visitors and new accounts — those whose first interaction with the app falls inside the window — per period across the window, with the prior-window comparison.
- **Retention** (`cohortRetentionCurve`): the retention curve for the app's new visitors, both the rate per period and the rate it settles at, with the cohort size behind each period so reliability can be judged.
- **Average time** (`appUsage`): average time in the app per visitor, and per active day where available, for the window and the prior window.
- **Stickiness** (`appUsageTimeSeries`): DAU/MAU measured monthly, never across the whole window. Compute one ratio per 30-day month inside the window — three of them for a 90-day window — each built from that month alone: MAU is the unique visitors active in that month, DAU is the average of that month's daily active visitors. Average the DAU across every calendar day in the month, weekends included — don't drop weekend buckets or divide by business days only, and count a day that returns no bucket as zero rather than skipping it. The MAU denominator spans the whole month, so dropping days from the numerator inflates the ratio. The trend is then month over month, and the comparison for the latest ratio is the 30 days before it, not the prior 90 days. A ratio whose denominator is unique visitors across the full window is not stickiness — the denominator grows with the window while the numerator does not, so the figure comes out far too low. If only one ratio can be obtained, scope it to the most recent 30 days and say so.
- **Frustration signals** (`appUsage`, then `activityQuery` to drill down): app-level rage clicks, dead clicks, error clicks, and u-turns for the window versus the prior window, and — where the data allows — the pages or features carrying the most of them.
- **Survey scores** (`surveyScores`): NPS, CSAT, and PMF survey scores for the app over the window, each with its response count and its movement versus the prior window.
- **Data gaps:** any evidence category that failed, returned nothing, or could not be collected (e.g. no surveys running, no frustration data). Carry these to the report as gaps rather than filling them in with guesses.

The evidence above is ideal, not a hard prerequisite. If a category is missing or empty, continue with the grounded data that exists. If no meaningful data can be collected at all, do not generate the report; briefly tell the user there was no data available for this app.

**Cohort metrics carry their definition.** Retention and stickiness mean nothing without how they were measured, so keep each definition alongside its number: for retention, who is in the cohort and how they qualified, the window, the period length and the number of periods, and the cohort size per period; for stickiness, what counted as daily active and as monthly active, the 30-day month each figure covers, and the ratio behind the figure. If a retention rate or a DAU/MAU figure arrives without its cohort, window, and configuration, get the definition or leave the metric out — a bare number reads as precise when it isn't.

## Output Format

Generate a single structured report. Derive the trends and the verdict yourself from the gathered data — don't just restate numbers.

```
## App Health Report: {app_name}
**App ID**: {app_id}
**Period**: {timeframe}

### Verdict
{Healthy / Mixed / Showing concern / At risk} — {2-3 sentences synthesizing the signals below into an overall read.}

### Engagement
- **Active Visitors**: {count} (vs {previous} prior period) {↑/↓ %}
- **Active Accounts**: {count} (vs {previous}) {↑/↓ %}
- **Events**: {count} (vs {previous}) {↑/↓ %}
- **Trend**: {per-period trajectory in words, flagging any partial first/last bucket}

### Acquisition
- **New Visitors**: {count} (vs {previous}) {↑/↓ %}
- **New Accounts**: {count} (vs {previous}) {↑/↓ %}
- **Trend**: {is the acquisition rate rising or falling}

### Retention
- **Curve**: {rate per period, e.g. week 1 → week 2 → ...}
- **Settles at**: {steady-state rate}
- **Cohort**: {who qualified, window, period length, cohort size per period}

### Average Time
- **Per Visitor**: {duration} (vs {previous}) {↑/↓ %}
- **Per Active Day**: {duration if available}

### Stickiness (DAU/MAU)
- **Monthly ratios**: {month 1}: {ratio} | {month 2}: {ratio} | {month 3}: {ratio}
- **Trend**: {month-over-month direction}
- **Definition**: {what counted as DAU and MAU, the 30-day months covered}

### Frustration Signals
- **Rage clicks**: {count} (vs {previous}) | **Dead clicks**: {count} | **Error clicks**: {count} | **U-turns**: {count}
- **Concentrated on**: {top pages/features carrying friction, if available}

### Survey Scores
- **NPS**: {score} ({n} responses) {↑/↓ vs previous}
- **CSAT**: {score} ({n} responses)
- **PMF**: {score} ({n} responses)

### Data Gaps
{Any evidence category that was attempted but unavailable — e.g. "No CSAT survey running", "Retention data unavailable".}

### Recommended Next Steps
{2-4 concrete actions grounded in the data. Where an in-app action fits, name the Pendo guide type (walkthrough, tooltip, lightbox, banner, Resource Center module) and the target segment — not a vague "add in-app guidance".}
```

## Rules

- **The report covers one app.** Resolve `app_id` in Step 0 and state which app it is. If the user names several, report on one and say which, or ask.
- Always pass the confirmed `app_id` (and `subId`) explicitly in every data-gathering request, and keep the app scope and window length identical between a metric and its comparison period.
- **Stickiness is monthly, never window-wide.** Compute DAU/MAU per 30-day month; a ratio whose denominator is unique visitors across the whole window is wrong.
- **Retention and stickiness must carry their definition** — cohort, window, and configuration — not a bare number.
- Default timeframe is 90 days if not specified.
- Run evidence-gathering steps in parallel when possible to save time.
- If a category returns no results (e.g. no surveys, no frustration data), note it in the Data Gaps section rather than leaving it blank or guessing. A missing category is a finding, not a failure.
- Derive the trends and the verdict yourself from the gathered data — don't hand back raw numbers without a read on what they mean.
- Close with next steps that name a concrete Pendo in-app action (guide type + target segment) where one fits.
- Keep user-facing responses minimal outside the report — let the report speak for itself.
