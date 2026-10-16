---
name: oncall
description: Show current on-call status, shift metrics, and health indicators for your team. Use to check who's on-call, handoff context, or on-call workload.
argument-hint: [team-name]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# On-Call Dashboard

You are showing the user a compact on-call dashboard. Gather data and present it concisely.

## Workflow

### 1. Gather Data

Make these calls (in parallel if possible):

1. `mcp__rootly__get_oncall_handoff_summary` -- Current and next on-call, shift context
2. `mcp__rootly__get_oncall_shift_metrics` -- Workload data (hours, incident count)
3. `mcp__rootly__check_oncall_health_risk` -- Fatigue and health risk indicators

If `$ARGUMENTS` contains a team name, pass it to scope the queries.

### 2. Present Dashboard

```
## On-Call Dashboard

### Current On-Call
- **Who**: [name]
- **Since**: [start time] ([hours] hours into shift)
- **Incidents this shift**: [count]

### Next On-Call
- **Who**: [name]
- **Handoff**: [time] ([hours] from now)

### Shift Health
- **Hours worked**: [current hours] / [shift length]
- **Fatigue risk**: [LOW / MEDIUM / HIGH]
- **Workload**: [incidents handled] incidents, [pages received] pages

### Recent Incidents This Shift
[List of incidents handled during current shift, if any]
| Severity | Title | Duration | Status |
|----------|-------|----------|--------|
| ... | ... | ... | ... |
```

Keep the output compact. If any data source returns an error or empty result, omit that section rather than showing empty tables.
