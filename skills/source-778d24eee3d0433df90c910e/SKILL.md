---
name: action
description: Manage incident action items from the terminal. Subcommands - list (default - your open action items) or add <incident> "<summary>" (create one on an incident). Use to capture follow-ups during or after an incident without opening the Rootly UI.
argument-hint: [list | add <incident> "<summary>"]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Action Items

You are helping the user view or update incident action items in Rootly.

## Subcommand routing

Parse `$ARGUMENTS`:

- Empty or starts with `list` → **List mode** (default).
- Starts with `add <incident-ref> ` → **Add mode**. The remainder is the description.
- Anything else → show the usage from `argument-hint` and stop.

---

## List mode

Goal: show the user their open action items, sorted by incident severity then age.

1. Call `mcp__rootly__getCurrentUser` to get the user's UUID.
2. Call `mcp__rootly__listAllIncidentActionItems` and filter results client-side by `assigned_to_user_id` matching the current user, plus status not in `done`/`closed`/`cancelled`.
3. For each item, the response usually includes an `incident_id` or `incident` reference. Cluster results by incident.
4. Render:

```
## Your Open Action Items ([N] total across [M] incidents)

### [INC-XXXX] [Incident title] ([severity])
- [ ] [Action item description] — due [date or "no due date"], priority [priority]
- [ ] [Action item description] — due [date], priority [priority]

### [INC-YYYY] [Incident title] ([severity])
- [ ] [Action item description] — due [date], priority [priority]
```

If there are zero open items, say so plainly: "No open action items assigned to you."

---

## Add mode

Goal: create a new action item on an incident. **Write action — requires explicit confirmation.**

1. Parse the incident reference from `$ARGUMENTS` (UUID, `INC-XXXX`, or bare number).
2. Resolve the incident by calling `mcp__rootly__getIncident` with the reference exactly as the user provided it. The MCP server now accepts UUIDs plus sequential forms like `4460`, `#4460`, and `INC-4460`.
3. Parse the action item summary: everything after the incident reference, stripped of surrounding quotes.
4. Show a preview to the user:

```
**About to create action item:**
- Incident: [INC-XXXX] [title]
- Summary: [summary]
- Assigned to: [you / unassigned per default]
- Priority: medium (default — adjust in Rootly UI if needed)

Confirm to create? (yes / no)
```

5. **Wait for the user's reply.** Do not call `mcp__rootly__createIncidentActionItem` until they say yes.
6. On confirmation, call `mcp__rootly__createIncidentActionItem` with:

```json
{
  "incident_id": "[resolved incident UUID]",
  "data": {
    "type": "incident_action_items",
    "attributes": {
      "summary": "[summary]",
      "priority": "medium",
      "status": "open"
    }
  }
}
```

Echo the resulting action item ID and any URL.
7. On rejection, acknowledge and stop without making the call.

---

## Guidelines

- Never mutate Rootly state without explicit confirmation. The "yes" must come from the user, not be assumed.
- Show what will change before the call, not after.
- If a write fails mid-flight, surface the exact error so the user can decide whether to retry.
- If `mcp__rootly__listAllIncidentActionItems` is rate-limited or paginates, take just the first page (50 items). The user can re-run if they need more.
- Do not imply that action items can be marked done through this skill until the MCP exposes an update action item tool.
