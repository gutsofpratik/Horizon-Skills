---
name: brief
description: Generate a concise stakeholder brief for an incident. Creates executive summary with key details, impact, timeline, and current status.
argument-hint: [incident-id]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Incident Stakeholder Brief

You are creating a concise stakeholder brief for an incident. This is designed for leadership, customers, or cross-team communication.

## Workflow

### 1. Get Incident Details

If `$ARGUMENTS` contains an incident ID:
- Call `mcp__rootly__getIncident` with the provided ID
- Call `mcp__rootly__listIncidentAlerts` to get associated alerts

If no incident ID provided, prompt the user to specify one.

### 2. Generate Brief

Create a structured brief with these sections:

```markdown
# Incident Brief: [incident-title]

**Incident ID**: [short-id]  
**Severity**: [severity]  
**Status**: [status]  
**Started**: [started-at]  
**Duration**: [calculated duration]

## Impact Summary
[Brief description of customer/business impact]

## Current Status
[What's happening now - investigation, mitigation, resolution]

## Services Affected
- [list of affected services]

## Timeline (Key Events)
- **[time]**: [event description]
- **[time]**: [event description]

## Next Steps
[What's being done to resolve or prevent recurrence]

---
*Brief generated at [current-time] | Status may have changed since generation*
```

### 3. Formatting Guidelines

- Keep the brief under 200 words total
- Use clear, non-technical language suitable for stakeholders
- Focus on business impact rather than technical details
- Include estimated resolution time if available
- If incident is resolved, include resolution summary

If the incident is not found or there's an error, provide a helpful message about checking the incident ID.