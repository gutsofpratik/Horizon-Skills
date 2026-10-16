---
name: trend
description: Reliability trend summary for a service, team, or the whole org. Reports incident volume, severity mix, and MTTR direction over a window (default 30 days). Use for standups, 1-on-1s, or quarterly reviews.
argument-hint: [service-or-team-name | "all"]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Reliability Trend

You are summarizing whether things are getting better or worse, scoped to a service, team, or the whole org.

## Workflow

### 1. Determine scope

Parse `$ARGUMENTS`:
- Empty or `all` → org-wide.
- A name → resolve to a service or team using the same approach as `/rootly:lookup`:
  1. Try `mcp__rootly__listServices` first.
  2. Fall back to `mcp__rootly__listTeams`.
  3. If multiple matches, list the top 5 and ask the user to disambiguate.

### 2. Pull the chart data

**Service scope:**
- Call `mcp__rootly__getServiceIncidentsChart` for the last 30 days.
- Call `mcp__rootly__getServiceUptimeChart` for the same window if available.
- Call `mcp__rootly__listIncidents` filtered to the service over the last 30 days (page_size=100) for severity and resolution timing.

**Team scope:**
- Call `mcp__rootly__getTeamIncidentsChart` for the last 30 days.
- Call `mcp__rootly__listIncidents` filtered to the team over the last 30 days for severity and MTTR.

**Org scope:**
- Call `mcp__rootly__listIncidents` over the last 30 days (page_size=100, sort=-created_at). If the volume exceeds one page, note the truncation and proceed with a partial picture rather than walking pages.

### 3. Pull the comparison window

Repeat the same call for the **previous 30-day window** (days 31–60). This gives a baseline for trend direction.

### 4. Compute the metrics

For each window, compute:
- **Total incidents**
- **Severity mix** (count per severity, with critical+high highlighted)
- **MTTR** — for resolved incidents only, average `resolved_at - started_at`. Skip incidents with missing timestamps rather than imputing.
- **Repeat incidents** — count of incidents whose service or root cause appears more than once in the window. (Best-effort: if `cause` data is absent, skip this metric and note it.)

Compare current vs previous to derive trend direction:
- **Improving**: incident count down ≥10% AND MTTR not significantly worse.
- **Degrading**: incident count up ≥10% OR MTTR up ≥25%.
- **Stable**: anything else.

### 5. Render

```
## Reliability Trend: [scope name]
*30-day window vs prior 30 days*

### Headline
**[Improving 📈 / Stable ➡️ / Degrading 📉]** — [one-sentence summary]

### Metrics
| Metric | This period | Prior period | Δ |
|---|---|---|---|
| Total incidents | [N] | [N] | [+/-N (%)] |
| Critical/High | [N] | [N] | [+/-N] |
| MTTR | [duration] | [duration] | [+/-duration] |
| Repeat incidents | [N] | [N] | [+/-N] |

### Severity Mix (this period)
- 🔴 Critical: [N]
- 🟠 High: [N]
- 🟡 Medium: [N]
- 🟢 Low: [N]

### Top Incidents (most recent / highest severity)
- [INC-XXXX] [title] ([severity], [duration])
- [INC-YYYY] [title] ([severity], [duration])
[max 5]

### What I'd flag
[Concise observations:]
- [e.g. "Critical count doubled — both incidents on payments-api in the same week"]
- [e.g. "MTTR worsening despite stable volume — investigate response process"]
- [e.g. "No incidents this period on this service — expected or coverage gap?"]
```

### 6. Read-only

This skill never mutates Rootly state.

### 7. Error handling

- If a chart endpoint isn't available for the scope (some MCP versions only support service-level, not team-level), compute metrics manually from `listIncidents` and proceed.
- If the prior window has no data, skip the comparison row and label the headline "Insufficient history".
- If incident count is below 5 in either window, add a caveat: "*Sample size is small — trend may not be meaningful.*"
