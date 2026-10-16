---
name: announce
description: Draft a stakeholder-facing status update for an active incident, then post it after explicit confirmation. Useful for incident commanders pushing public-status-page or internal updates without opening the Rootly UI. Write action - never posts without confirming.
argument-hint: [incident-id]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Incident Announcement

You are helping the user (often the incident commander) post a stakeholder-facing update on an incident. **Write action — explicit confirmation required.**

## Workflow

### 1. Resolve the incident

`$ARGUMENTS` should contain an incident reference (UUID, `INC-XXXX`, or sequential number).

- If empty: call `mcp__rootly__listIncidents` with `filter_status="started"`, `page_size=10`, and `sort="-started_at"` and ask the user which incident to announce.
- Otherwise call `mcp__rootly__getIncident` with the incident reference exactly as provided. The MCP server accepts UUIDs plus sequential forms like `4460`, `#4460`, and `INC-4460`.

Once resolved, use the returned incident record for the full context.

### 2. Identify the publication target

Inspect the incident record for:
- An attached status page (often `status_page_id` or similar field)
- Public-facing flag (`is_public` / `private`)

If the incident has a status page attached:
- Call `mcp__rootly__getStatusPage` for the page details (name, URL).
- Call `mcp__rootly__listStatusPageTemplates` to surface preset update templates.

If no status page is attached, fall back to posting an **incident event** that surfaces in Rootly's internal stream — call `mcp__rootly__createIncidentEvent` instead. Make the distinction clear to the user.

### 3. Draft the update

Compose a 2–4 sentence update with this structure:

```
[Status verb: "Investigating" / "Identified" / "Monitoring" / "Resolved"] — [one-sentence summary of customer impact].
[Optional: what we know about the cause, briefly.]
[Optional: what we're doing about it.]
[Next update: in [duration] / when status changes.]
```

Keep it stakeholder-grade: no Rootly internal IDs, no engineer names, no jargon.

### 4. Show the draft

```
**Incident**: [INC-XXXX] [title] — [severity], [status]
**Posting to**: [Status page name + URL] | [Internal incident stream if no status page]
**Visibility**: [Public / Internal]

**Draft update:**

> [the drafted message]

Confirm to post this update? (yes / edit / no)
```

### 5. Handle the user's reply

- **`yes`** → call the appropriate tool:
  - Status page update path: post via the status-page-specific MCP tool if one is exposed; otherwise create an incident event with the text and rely on Rootly's status-page integration to syndicate it. Prefer `mcp__rootly__createIncidentEvent` with a clear `event_type` if a dedicated tool isn't available.
  - Internal-only path: call `mcp__rootly__createIncidentEvent` with this shape:

```json
{
  "incident_id": "[resolved incident UUID]",
  "data": {
    "type": "incident_events",
    "attributes": {
      "event": "[drafted message]",
      "visibility": "internal"
    }
  }
}
```
- **`edit`** → ask the user for revisions. Re-show the draft. Re-confirm.
- **`no`** or anything else → acknowledge, do not post.

### 6. After posting

```
✅ Update posted.
- [Status page URL if applicable]
- [Event ID]

Reminder: this skill posts a single update. For ongoing communication, post follow-ups every [interval based on severity] or when status changes.
```

### 7. Guidelines

- **Never** post without explicit `yes`. Stakeholder updates are visible and hard to retract.
- **Severity-aware tone**:
  - SEV0/SEV1 → calm, factual, frequent updates expected.
  - SEV2 → succinct, focused on impact.
  - SEV3+ → minimal, often only at status changes.
- **Resolved updates**: if the incident status is `resolved` or `closed`, default the verb to "Resolved" and include a one-line root-cause summary if available.
- **Edit loops**: don't infinitely revise. After two edit rounds, ask the user to type the exact text they want.
- If the user has no permission to post on the status page (API returns 403), surface the error clearly. Don't try to escalate.
