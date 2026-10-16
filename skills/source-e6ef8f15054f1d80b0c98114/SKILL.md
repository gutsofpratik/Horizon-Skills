---
name: alert
description: Triage a Rootly alert by short ID. Pulls the alert record, its event timeline, related alerts in the same group, and any incident the alert is attached to. Use when a page comes in and you want context before opening Rootly.
argument-hint: [short-id]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Alert Triage

You are helping the user triage a Rootly alert. Alerts are the upstream signal that may or may not become incidents. The goal is to give the user enough context in one place that they can decide: ignore, acknowledge, escalate, or open an incident.

## Workflow

### 1. Resolve the alert

`$ARGUMENTS` should contain a short alert ID (e.g. `A-1234` or `1234`).

- If `$ARGUMENTS` is empty: report "No alert ID provided. Pass a short ID like `A-1234` or `1234`." and stop.
- Otherwise call `mcp__rootly__get_alert_by_short_id` with the value as given.
- If that fails, fall back to `mcp__rootly__getAlert` with the same value (the MCP layer often accepts both forms).
- If both fail, surface the error and stop.

### 2. Gather context

Once you have the alert UUID:

1. Call `mcp__rootly__listAlertEvents` (or filter by alert) to get the event timeline.
2. If the alert response includes an `alert_group_id` or `group` reference, call `mcp__rootly__getAlertGroup` for sibling alerts.
3. If the alert is attached to an incident, the response usually carries an `incident_id`. Call `mcp__rootly__getIncident` for incident context.
4. Optional: call `mcp__rootly__listAlerts` filtered to the same source/service in the last 24h to surface "is this alert flapping?"

Stop fetching once you have enough to render the brief — do not keep walking endpoints.

### 3. Present the alert brief

```
## Alert Brief: [alert title]

**Short ID**: [short-id] | **Source**: [source] | **Urgency**: [urgency]
**Started**: [time] ([duration] ago) | **State**: [state]
**Service**: [service or "unmapped"]

### Summary
[Alert summary or first event message]

### Event Timeline
- [time] [event-type]: [message]
- [time] [event-type]: [message]
[at most 8 events, oldest first]

### Group Context
[If part of a group:]
This alert is one of [N] in group [group-name]. Other open alerts in the group:
- [short-id] [title] ([state])

[If flapping detected:]
**Flapping**: this source has fired [N] alerts in the last 24h on the same service.

### Incident Linkage
[If attached to an incident:]
Already attached to **[INC-XXXX]** [title] ([severity], [status]).

[If not attached:]
Not attached to an incident.

### Suggested Next Step
[Pick one based on the data:]
- "Acknowledge — looks like a known transient pattern"
- "Open an incident — first occurrence, customer-facing surface"
- "Escalate — already linked to a critical incident with no responder yet"
- "Ignore — historical noise from this source on this service"
```

### 4. Read-only

This skill never mutates Rootly state. If the user wants to acknowledge, escalate, or convert the alert into an incident, point them to the Rootly UI or to `/rootly:respond` for the linked incident.

### 5. Error handling

- **Alert not found**: report the short ID and suggest checking the format (e.g. `A-1234`).
- **MCP tool errors**: report the specific error and continue with whatever data you have.
- **No event timeline available**: note it and skip that section rather than failing entirely.
