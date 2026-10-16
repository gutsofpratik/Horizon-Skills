---
name: lookup
description: Look up a service, team, or catalog entity in Rootly. Returns owner, on-call, recent reliability, dependencies, and any active incidents. Use when something breaks and the first question is who owns this.
argument-hint: [service-or-team-name]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Service / Team Lookup

You are answering "what is this thing and who owns it?" for a service, team, or catalog entity. The user may pass a partial or full name; do your best to resolve it.

## Workflow

### 1. Resolve the target

`$ARGUMENTS` is the search term. It might be:
- A service name (e.g. `payments-api`)
- A team name (e.g. `Platform`)
- A repository name
- A catalog entity slug

Strategy:
1. Try `mcp__rootly__listServices` with the term as a filter where supported. If the MCP tool offers a name/query filter, use it; otherwise fetch the first 50 and match client-side (case-insensitive substring).
2. If no service match, try `mcp__rootly__listTeams` similarly.
3. If still no match, try `mcp__rootly__listCatalogEntities` (across all catalogs).

Determine the **kind** of the resolved entity (`service`, `team`, or `catalog-entity`) — branch the rendering on that.

If multiple matches, list the top 5 and ask the user to disambiguate. Do not guess.

If no matches, say so and suggest the user check spelling or try a broader term.

### 2. Gather details — service path

If the resolved entity is a **service**:

1. Call `mcp__rootly__getService` for the full record. Capture: name, description, owning team, environment, slug, URL.
2. Call `mcp__rootly__getServiceUptimeChart` for the last 30 days (if the MCP supports a period parameter; otherwise default).
3. Call `mcp__rootly__listIncidents` with `filter_service_ids=<id>` and `filter_status=started` to surface active incidents on this service.
4. If the service references an owning team, call `mcp__rootly__getTeam` for the team's name and `mcp__rootly__get_oncall_schedule_summary` (or `mcp__rootly__get_oncall_handoff_summary`) for current on-call.
5. Optional: `mcp__rootly__listIncidents` filter by service in the last 90 days, page 1 only, to spot frequency.

### 3. Gather details — team path

If the resolved entity is a **team**:

1. Call `mcp__rootly__getTeam` for the record. Capture name, description, slug, members count if available.
2. Call `mcp__rootly__listServices` filtered by team to enumerate owned services.
3. Call `mcp__rootly__get_oncall_schedule_summary` for current on-call across the team.
4. Call `mcp__rootly__listIncidents` filtered by team and `status=started` for active incidents.

### 4. Gather details — catalog entity path

If the resolved entity is a **catalog entity**:

1. Call `mcp__rootly__getCatalogEntity` for the full record.
2. Note the catalog it belongs to (`mcp__rootly__getCatalog` if you need the catalog's name).
3. Surface any service/team references in the entity's properties.

### 5. Render

**Service rendering:**

```
## Service: [name]
*[slug] — [environment]*

### Ownership
- **Team**: [team name]
- **On-call right now**: [user name] (until [shift end])
- **Backup**: [backup name if available]

### Recent Reliability (30 days)
- Uptime: [percentage]
- Incidents: [count] ([critical: N, high: N, medium: N])
- MTTR: [duration]

### Active Incidents
[If any:]
- 🔴 [INC-XXXX] [title] — started [duration] ago
[If none:]
No active incidents.

### Description
[service description]
```

**Team rendering:**

```
## Team: [name]
*[slug] — [N members]*

### Owned Services ([N])
- [service-name] ([environment])
- [service-name] ([environment])
[max 10, then "+N more"]

### Currently On-Call
- [Schedule]: [user name] (until [time])

### Active Incidents ([N])
- 🔴 [INC-XXXX] [title]
[If none: "No active incidents."]
```

**Catalog entity rendering:**

```
## [Catalog] Entity: [name]
*[slug]*

### Properties
- [key]: [value]
- [key]: [value]

### Linked References
[Any service/team links found]
```

### 6. Read-only

This skill never mutates Rootly state.

### 7. Error handling

- If a downstream call fails (e.g. uptime chart API errors), render the rest of the data and add a one-line note: "*[Section]: not available — [error]*".
- Don't fail the whole response because one optional chart didn't load.
- If `getCurrentUser` is needed for context (and most cases don't require it), skip it.
