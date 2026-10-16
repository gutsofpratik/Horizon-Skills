---
name: swap
description: Request someone to cover one of your upcoming on-call shifts. Lists your shifts, helps identify a candidate based on availability, and creates an override after explicit confirmation. Write action - never executes without confirming.
argument-hint: [optional shift selector — date or "next"]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Shift Swap Request

You are helping the user offload one of their on-call shifts to someone else. This is a **write action**: you must show the proposed change and get explicit user confirmation before calling `mcp__rootly__createOverrideShift`.

## Workflow

### 1. Identify the user

Call `mcp__rootly__getCurrentUser`. Capture `user_id`.

### 2. List the user's shifts

Call `mcp__rootly__listShifts` (or `list_shifts`) scoped to:
- The current user
- Next 14 days

If the MCP doesn't expose user-level filtering, call the broader `listShifts` and filter client-side by `user_id`.

### 3. Pick the target shift

- If `$ARGUMENTS` is empty: show the next 5 shifts and ask "Which shift do you want covered?"
- If `$ARGUMENTS` is `next`: pick the soonest upcoming shift.
- If `$ARGUMENTS` is a date or shift identifier: try to match.

If no match, list options and ask.

### 4. Find candidate coverers

For the shift's schedule and time window:
1. Call `mcp__rootly__create_override_recommendation` if it accepts the shift parameters — this is the cleanest path; it returns suggested coverers.
2. Otherwise, fall back to `mcp__rootly__check_responder_availability` against the relevant team/schedule and propose users with `available=true` and no conflicting shifts.
3. Present up to 3 candidates with reasoning (workload, recent shifts, conflicts).

If no candidates are available, surface that and stop.

### 5. Show the proposal

```
**Proposed shift swap:**
- **Shift**: [Schedule name] [start] → [end] ([duration])
- **Currently assigned**: you ([your name])
- **Proposed coverer**: [candidate name]
- **Why**: [reason — e.g. "no shifts this week, on team rotation"]

**Alternatives**:
- [other candidate] — [reason]
- [other candidate] — [reason]

Confirm to create the override? (yes / no / pick another)
```

### 6. Wait for confirmation

- **`yes`** → call `mcp__rootly__createOverrideShift` with this shape:

```json
{
  "schedule_id": "[schedule_id]",
  "data": {
    "type": "shifts",
    "attributes": {
      "starts_at": "[shift start ISO8601]",
      "ends_at": "[shift end ISO8601]",
      "user_id": [coverer user id]
    }
  }
}
```

Echo the resulting override ID and a confirmation line.
- **`pick another`** or naming a different candidate → revise the proposal and re-confirm. Do not execute on the first reply if the user is changing the candidate.
- **`no`** or any other answer → acknowledge and stop. Do not call the create tool.

### 7. After the override is created

Output:

```
✅ Override created.
- ID: [uuid]
- Coverer: [name]
- Window: [start] → [end]

Recommended next steps:
- Notify the coverer in Slack / your team channel.
- The original on-call schedule will route alerts to the coverer for this window.
```

### 8. Guidelines

- **Never** call `createOverrideShift` without confirmation. The "yes" must come from the user, not be inferred.
- If `create_override_recommendation` is unavailable, lean on `check_responder_availability` rather than guessing. Don't propose a coverer you can't verify is available.
- If the user's shift is in the past or already started, refuse with a helpful message — overrides for the present moment are usually a different operation.
- Show timezone explicitly in the proposal. Ambiguous times cause mistakes.
