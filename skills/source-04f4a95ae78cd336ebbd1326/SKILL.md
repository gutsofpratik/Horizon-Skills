---
name: my
description: Personal Rootly dashboard. Shows your open action items, your active incidents (where you're a responder), and your upcoming on-call shifts. Use to start the day or to context-switch back into incident work.
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Your Rootly Dashboard

You are building a personal status board for the current Rootly user. Read-only, focused, and quick to scan.

## Workflow

### 1. Identify the user

Call `mcp__rootly__getCurrentUser`. Capture:
- `user_id` (UUID) — for filtering downstream calls
- `name` and `email` — for the header
- Team membership if present in the response

If `getCurrentUser` fails, stop with a clear auth error message.

### 2. Pull the three data slices in parallel

You may issue these tool calls in parallel where the model supports it. Keep each call narrow — we want a fast dashboard, not a full audit.

**a. Open action items**
- Call `mcp__rootly__listAllIncidentActionItems` (first page, page_size = 50).
- Filter to items where `assigned_to_user_id` (or equivalent field) matches the user, with status not in `done`/`closed`/`cancelled`.

**b. Active incidents you're on**
- Call `mcp__rootly__listIncidents` with `filter_status=started` and `filter_user_id=<user_id>` if supported, or with the user's team via `filter_team_ids` if individual filtering isn't available.
- Page size 25 is plenty.

**c. Upcoming shifts**
- Call `mcp__rootly__listShifts` for the current user, scoped to the next 7 days.
- If individual user filtering isn't available, fall back to `mcp__rootly__list_shifts` and filter client-side.

### 3. Render the dashboard

```
## [User name]'s Rootly Dashboard
*[email] — [primary team if known]*

### Active Incidents ([N])
[For each: severity badge, INC-XXXX, title, your role, started X ago]
- 🔴 [INC-XXXX] [title] — your role: [responder/IC/observer], started [duration] ago
- 🟡 [INC-YYYY] [title] — your role: [responder], started [duration] ago

[If zero: "No active incidents you're responding to."]

### Open Action Items ([N])
[Cluster by incident, max 10 items]

#### [INC-XXXX] [title]
- [ ] [description] — due [date or "no due date"]
- [ ] [description]

[If zero: "No open action items assigned to you."]

### Upcoming On-Call ([N] shifts in the next 7 days)
- [Schedule name]: [start] → [end] ([role/level if available])
- [Schedule name]: [start] → [end]

[If currently on call:]
**Currently on call**: [Schedule name] until [end time].

[If zero: "No on-call shifts in the next 7 days."]

---

### Quick links
- `/rootly:status` — service health overview
- `/rootly:oncall` — full team on-call schedule
- `/rootly:action add <incident> "<desc>"` — capture a follow-up
- `/rootly:swap` — request a shift swap
```

### 4. Tone & formatting

- Compact. This is meant to be glanceable, not a full report.
- Use severity emoji or symbols if they render in the user's terminal: 🔴 (critical), 🟠 (high), 🟡 (medium), 🟢 (low). If unsure, use plain text labels.
- Cap each section at the most-relevant 10 items. If there are more, append a single line: "(+N more — run /rootly:status or check Rootly UI)".

### 5. Error handling

- If any one slice fails (e.g. shifts API returns 500), render the other two and add a short note: "*Could not load on-call shifts: [error]*".
- Never leave a section blank with no explanation.
