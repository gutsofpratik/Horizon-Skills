---
name: retro
description: "[experimental] Generate a structured post-incident retrospective from incident data. Forked-subagent flow may not have MCP access in all Claude Code contexts."
argument-hint: [incident-id]
disable-model-invocation: true
context: fork
agent: rootly:retro-analyst
allowed-tools:
  - mcp__rootly__*
---

# Retrospective Generator (experimental)

> **Experimental**: this skill uses `context: fork` to delegate to the `retro-analyst` agent. In some Claude Code contexts the forked subagent does not inherit the plugin's MCP tools. If the agent reports MCP tools unavailable, use `/rootly:brief <incident>` for a basic incident summary instead.

You are generating a structured post-incident retrospective. The output should be copy-pasteable markdown.

## Workflow

### 1. Get Incident Data

The incident ID should be provided in `$ARGUMENTS`. If not provided, ask the user for it.

1. Call `mcp__rootly__getIncident` for the full incident record
2. Check the incident status:
   - If status is `started` (still active), warn the user: "This incident is still active. Retrospectives are typically done after resolution. Continue anyway?" Wait for confirmation before proceeding.

### 2. Gather Context

1. Call `mcp__rootly__get_alert_by_short_id` or alert search tools for the alert timeline
2. Call `mcp__rootly__find_related_incidents` to check for recurring patterns

### 3. Generate Retrospective

Output as clean, copy-pasteable markdown:

```markdown
# Retrospective: [Incident Title]

**Incident ID**: [id]
**Date**: [date]
**Duration**: [start] to [end] ([total duration])
**Severity**: [severity]

## Summary
[1-2 sentence summary of what happened]

## Impact
- **Duration**: [time from detection to resolution]
- **Affected services**: [list]
- **Severity**: [level]
- **User impact**: [description if available]

## Timeline
| Time | Event |
|------|-------|
| [time] | [event] |
| ... | ... |

## Root Cause Analysis
[Analysis based on incident data, alerts, and resolution steps]

## Contributing Factors
- [Factor 1]
- [Factor 2]

## What Went Well
- [Positive aspect 1]
- [Positive aspect 2]

## What Could Be Improved
- [Improvement area 1]
- [Improvement area 2]

## Action Items
| Action | Owner | Priority |
|--------|-------|----------|
| [action] | [owner if identifiable] | [high/medium/low] |

## Pattern Note
[If find_related_incidents shows similar past incidents:]
"This is the Nth incident of this type in the last 90 days. Consider systemic fixes."
[If no similar incidents: omit this section]
```

Base the analysis on actual incident data. Do not fabricate details. If information is unavailable, note it as "Not available in incident data" rather than guessing.
