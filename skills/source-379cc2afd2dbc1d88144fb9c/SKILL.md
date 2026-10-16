---
name: respond
description: "[experimental] Investigate and respond to a production incident. Pulls context, finds similar past incidents, suggests solutions, and enables coordination. Forked-subagent flow may not have MCP access in all Claude Code contexts -- prefer /rootly:status + /rootly:brief for now."
argument-hint: [incident-id]
disable-model-invocation: true
context: fork
agent: rootly:incident-investigator
allowed-tools:
  - mcp__rootly__*
---

# Incident Response (experimental)

> **Experimental**: this skill uses `context: fork` to delegate to the `incident-investigator` agent. In some Claude Code contexts the forked subagent does not inherit the plugin's MCP tools, in which case the agent will stop and report rather than fall back to bash/curl. If that happens, use the inline alternatives:
> - `/rootly:brief <incident>` — stakeholder summary
> - `/rootly:status` — service health
> - `/rootly:oncall` — current responders

You are helping the user investigate and respond to a production incident. This runs in a forked context to keep incident data separate from the main coding session.

## Workflow

### 1. Identify the Incident

**If `$ARGUMENTS` contains an incident reference**:
1. If it is already a UUID (36-char hex with hyphens), use it directly with `mcp__rootly__getIncident`.
2. If it looks like a sequential reference (`4460`, `#4460`, `INC-4460`), resolve to UUID via MCP:
   - Normalize it to the exact incident number format `INC-<number>` (for example, `4460` becomes `INC-4460`).
   - Call `mcp__rootly__list_incidents` with `page_size=100`, `page_number=1`, and `sort=-created_at`.
   - Scan the returned `incidents` array for an exact `incident_number` match. If found, use the corresponding `incident_id` as the UUID.
   - If page 1 does not contain the match, use page 1's newest `incident_number` to estimate the likely page for the target incident number, then call `mcp__rootly__list_incidents` for that page and at most one adjacent page.
   - On every page, match only on `incidents[*].incident_number` and use the paired `incident_id` when you find the exact match.
   - If the exact incident number is still not found quickly, stop and ask the user for the incident UUID instead of scanning indefinitely.
3. Use the resolved UUID for all subsequent MCP calls.
4. Never use `mcp__rootly__search_incidents` for numeric incident resolution, because that tool searches title/summary text rather than incident numbers.
5. Never walk paginated lists indefinitely. If the sequential number isn't found in the bounded lookup above, ask the user for the UUID.

**If no incident ID provided**:
1. Call `mcp__rootly__search_incidents` filtered to active status (`started`)
2. If no active incidents, report "No active incidents found" and stop
3. If multiple active incidents, list them sorted by severity (critical first, then high, then medium, then low) and ask the user to select one
4. For long lists, show critical/high severity first with a note about additional lower-severity incidents

### 2. Gather Full Context

Once you have the incident ID:

1. Call `mcp__rootly__getIncident` to get the full incident record
2. Call `mcp__rootly__get_alert_by_short_id` or search alerts for associated alert details and timeline
3. Call `mcp__rootly__find_related_incidents` to find historically similar incidents
4. Call `mcp__rootly__suggest_solutions` to get resolution recommendations
5. Call `mcp__rootly__get_oncall_handoff_summary` for current team status

### 3. Present Response Brief

```
## Incident Response Brief

### Summary
**[Incident title]** (ID: [id])
- **Status**: [status] | **Severity**: [severity]
- **Started**: [time] ([duration] ago)
- **Affected services**: [list]

### Timeline
[Key events from alert and incident data, chronological]

### Related Historical Incidents
[Top matches from find_related_incidents]
- [Incident title] ([date]) - Confidence: [score] - Resolution: [what fixed it]
[If all scores < 0.3: "Low confidence matches -- manual investigation recommended"]

### Suggested Solutions
[From suggest_solutions, ranked by confidence]
1. [Solution] (confidence: [score], source: [incident/runbook])

### Current Responders & On-Call
- **Assigned**: [responders]
- **On-call**: [name] (since [time])
- **Next handoff**: [time]

### Available Actions
The following actions require your explicit approval:
- Update severity
- Add responder
- Post status update
- Escalate to next on-call
```

### 4. Human-in-the-Loop for Write Operations

**CRITICAL**: NEVER execute write operations automatically. Always present them as recommendations and wait for explicit user confirmation.

Write operations include:
- `updateIncident` (changing severity, status, or any incident field)
- Adding or removing responders
- Posting status updates
- Escalating incidents
- Any other mutation of Rootly data

When the user approves an action, execute it and report the result.

### 5. Error Handling

- **MCP tool errors**: Report the specific error message and suggest manual steps (e.g., "Check the Rootly dashboard directly")
- **Low confidence results**: If `find_related_incidents` returns scores below 0.3, explicitly flag: "These matches are low confidence -- consider manual investigation"
- **Missing data**: If any tool call returns empty results, note it and continue with available data rather than failing entirely
