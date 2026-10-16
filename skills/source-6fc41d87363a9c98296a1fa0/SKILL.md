---
name: handoff
description: Prepare an incident or on-call handoff document. Creates structured summary for shift changes or incident commander transitions.
argument-hint: [incident-id]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Incident & On-Call Handoff

You are preparing a handoff document for either incident response or on-call shift transitions.

## Workflow

### 1. Determine Handoff Type

If `$ARGUMENTS` contains an incident ID:
- **Incident Handoff**: Create handoff for specific incident
- Call `mcp__rootly__getIncident` with the provided ID
- Call `mcp__rootly__listIncidentAlerts` for associated alerts

If no incident ID provided:
- **On-Call Handoff**: Create general shift handoff
- Call `mcp__rootly__get_oncall_handoff_summary` or relevant on-call endpoints
- Call `mcp__rootly__search_incidents` filtered to recent active incidents

### 2. Generate Incident Handoff

For incident-specific handoffs:

```markdown
# Incident Handoff: [incident-title]

**Handoff Time**: [current-time]  
**Incident ID**: [short-id]  
**Severity**: [severity]  
**Current Status**: [status]  
**Started**: [started-at] ([duration] ago)

## Current Situation
[Brief summary of what's happening now]

## What's Been Done
- [action 1]
- [action 2]
- [action 3]

## Immediate Next Steps
1. [priority action]
2. [next action]
3. [monitoring action]

## Key Contacts
- **Incident Commander**: [if assigned]
- **On-Call**: [current on-call person]
- **Escalation Path**: [relevant escalation details]

## Important Notes
[Any critical context, gotchas, or special considerations]

## Monitoring
- [key dashboards/alerts to watch]
- [specific metrics to monitor]
```

### 3. Generate On-Call Handoff

For general on-call handoffs:

```markdown
# On-Call Handoff

**Handoff Time**: [current-time]  
**Previous On-Call**: [if determinable]  
**Incoming On-Call**: [current/next on-call]

## Active Incidents
[List current active incidents with brief status]

## Recent Activity (Last 24h)
- [incident summaries]
- [any resolved issues]

## Ongoing Concerns
- [items requiring monitoring]
- [scheduled maintenance]
- [known issues]

## Escalation Paths
[Current escalation contacts and procedures]

## Key Dashboards
[Important monitoring dashboards to check]

## Upcoming Events
[Deployments, maintenance, or other scheduled activities]
```

### 4. Formatting Notes

- Keep handoffs concise but comprehensive
- Include actionable next steps
- Highlight any time-sensitive items
- Provide context for complex situations
- Include relevant links/IDs for quick access