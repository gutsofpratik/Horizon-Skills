---
name: cover
description: Offer to cover someone else's on-call shift. Lists upcoming shifts on a team or schedule and creates an override placing you on the chosen one after explicit confirmation. Write action - never executes without confirming.
argument-hint: [optional team-or-schedule-name]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Offer to Cover a Shift

You are helping the user volunteer to take someone else's upcoming on-call shift. This is the inverse of `/rootly:swap`. **Write action — explicit confirmation required.**

## Workflow

### 1. Identify the user

Call `mcp__rootly__getCurrentUser` to capture the current user's `user_id` and team membership.

### 2. Determine the scope

Parse `$ARGUMENTS`:
- Empty → show the user's own teams' upcoming shifts (next 14 days), filtered to shifts assigned to *other* people.
- A name → resolve to a team via `mcp__rootly__listTeams` or a schedule via `mcp__rootly__listSchedules`. If multiple matches, list them and ask.

### 3. Pull candidate shifts

Call `mcp__rootly__listShifts` (or `list_shifts`) for the chosen schedule(s) over the next 14 days.

Filter:
- Exclude shifts already assigned to the current user.
- Exclude shifts that have already started or are in the past.

### 4. Present the list

```
## Upcoming shifts you could cover

| # | Schedule | When | Currently | Length |
|---|---|---|---|---|
| 1 | [name] | [start] → [end] | [user name] | [duration] |
| 2 | [name] | [start] → [end] | [user name] | [duration] |
[max 10]

Reply with the shift number you'd like to cover, or `none` to cancel.
```

If there are zero matches, say "No upcoming shifts available to cover in [scope]." and stop.

### 5. On user selection

When the user picks a number:

1. Optionally call `mcp__rootly__check_responder_availability` for the current user against that time window to verify they don't have a conflict. If a conflict exists, surface it and ask if the user wants to proceed anyway.
2. Show the proposal:

```
**Proposed coverage:**
- **Shift**: [Schedule] [start] → [end] (timezone)
- **Currently assigned**: [original user]
- **You will cover**: [your name]
- **Conflict check**: [no conflicts | conflict with X — proceed anyway?]

Confirm to create the override? (yes / no)
```

3. Wait for explicit `yes`. Anything else → cancel.

### 6. On confirmation

Call `mcp__rootly__createOverrideShift` with:
- `schedule_id` of the target shift's schedule
- `data.type = "shifts"`
- `data.attributes.starts_at` and `data.attributes.ends_at` matching the shift window
- `data.attributes.user_id` = current user's integer Rootly user ID

Echo the result:

```
✅ Override created. You're now on call for [Schedule] [start] → [end].
- Override ID: [uuid]

Recommended next steps:
- Let [original user] know in Slack so they can plan around it.
- Verify in /rootly:my that the shift now appears under your upcoming on-call.
```

### 7. Guidelines

- **Never** mutate without confirmation. Same rule as `/rootly:swap`.
- If the user has a conflict and proceeds anyway, the system should still create the override — but flag the conflict clearly in the success message so the user remembers to resolve it.
- Show timezones explicitly. Always.
- If `createOverrideShift` returns an error (permission, schedule not editable), surface the exact error and don't retry silently.
