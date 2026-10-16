---
name: incidents
description: >
  Reading and changing incidents in incident.io: status, severity, roles, fields, updates,
  channel messages and the AI investigation. Use whenever you're working with an incident
  in any way, even a single read or change. Load it before the first incident, update,
  follow-up or investigation tool call: the tools accept changes the organisation's rules
  then reject, and this skill says what to check first. Not for fleet-wide statistics,
  runbooks or who is on call.
---

# Incidents

An incident is how incident.io tracks one thing going wrong: a reference (INC-123), a
status, a severity, the people responding, and a channel where the response happens.

The ground rules and the incident model are here. The rules the tools enforce, the
responder judgement and the writing craft are in the reference files: **read the
matching reference before acting, every time**.

## Match the task to its reference

- **Read, summarise, or answer questions about an incident** ("what's the impact",
  "who's leading", "catch me up", "what has the investigation found") → read
  `references/reading.md` first. It says how to read just what the task needs, and which
  lists truncate.
- **Change the incident** — status, severity, pause, resolve, close, roles, fields
  ("bump to P1", "accept this", "resolve it", "pause until Monday") → read
  `references/lifecycle.md` first. The tools reject transitions for reasons it explains
  (accept needs a type in the same call; triage can't be resolved, paused, or canceled;
  resolving can demand custom fields), and every rejected or repeated call is visible
  noise in the channel.
- **Respond to something breaking** — declare, attach an alert, merge duplicates
  ("there's an outage", "merge these") → read `references/responding.md` first. It
  carries the duplicate check.
- **Page someone, read pages or ack one** ("page the backend team", "I got paged") → the
  `on-call` skill owns paging and its safety rules; load it before an escalation tool.
- **Work with the incident's AI investigation** — a correction to its hypothesis, new
  evidence it didn't have, a request to look somewhere else, or a question about whether
  to start one → read `references/responding.md` first. It says when a remark is a steer
  the investigation needs fed in and when it is just a question to answer.
- **Write anything a human reads** — an update, the summary, customer or exec comms
  ("post an update", "suggest an update", "draft comms") → read
  `references/writing.md` **before drafting a word**. It says what to lead with, what
  never to restate, and how to keep your analysis labelled as theory.

A task that spans jobs reads each matching reference — "accept this and post an
update" is lifecycle.md then writing.md. Read the whole file, not a grep of it.

## How you reach the incident

You're working outside the incident channel, in a coding agent or a chat app, through the
incident.io plugin, the incident.io MCP server on its own, or the incident.io desktop app.
Below, "the plugin" also means the MCP server on its own, since it has the same tools. You can't
read the channel's messages, and what the user finds and changes here reaches neither the channel nor the investigation unless
it's shared in words.

The organisation's configuration is the `config://organisation` resource from the incident.io
tools (`resource_show` with that URI where the session can't read resources). `incident_pin`,
`escalations_list`, `identity_get`, `investigation_list`, `investigation_read` and `setup`
come only with the incident.io desktop app: where one is missing they're on the plugin, so say
what they'd need rather than calling it a limit of their organisation.

A call can fail for a reason that isn't the incident: the desktop app isn't running, they're
signed out, or the incident.io MCP server isn't set up in this session. Stop, say which in one
line with the fix ("open the incident.io desktop app and ask again"; "sign in again in the
app, then reconnect the incident.io server"), and point to the `doctor` skill for anything
more. Never report it as the incident not existing, and don't carry on by guessing.

`incident_show` returns the record (status, severity, roles, summary, the five most recent
updates) and leaves out the investigation and the postmortem unless you `include` them;
including `updates` returns every update, so it needs no `incident_update_list` after it. An
AI investigation's full record is a set of files:
`references/reading.md` says how to get them and what to read first.

Work out which incident they mean before anything else:

- **A reference given** ("INC-123", "123"): use it.
- **"My incident", "the one I'm on"**: where the session has `incident_pin`, call it with no
  arguments first. It returns the pinned incident's number only, so look it up with
  `incident_show` before you name it. With nothing pinned, or no `incident_pin`, list the
  user's incidents that aren't resolved (`incident_list` with `assigned_to: ["me"]` and
  `status_category` triage, active and paused), saying which are paused (on hold) or in
  triage (unconfirmed). With one, use it and say how you know ("you're the lead on the only
  incident you're in that isn't resolved"). With several, list them (reference, name,
  status, their role) and ask. Never take the organisation's newest incident.
- **"I got paged", "what woke me up"**: their pages are the `on-call` skill's, and many
  have no incident. Once they've picked one that has, its incident is this skill's.
- **Pinning** ("I'm on INC-123 now", "/incident INC-123"): on the desktop app,
  `incident_pin(incident_id: …)` makes it the incident later asks resolve to; `unset: true`
  clears it and deletes its downloaded investigation files. Pinning doesn't add anyone to the
  incident or give them a role. On the plugin there is no pin, so say so and carry the
  reference yourself for the rest of the session.

## The incident model

- **Identity**: a reference (INC-123) and a name.
- **Status**: where it is in its lifecycle. Every status belongs to one of eight
  categories — triage, active, paused, post-incident, closed, declined, merged,
  canceled — and the lifecycle rules are about categories, while the tools take an
  intent word or an org-specific status.
- **Severity**: how bad it is, on a ranked scale the organisation defines (higher rank
  = more severe). It drives who gets paged, so it is never guessed.
- **Roles**: who is doing what (lead, communications, and others the org configures).
- **Custom fields**: org-defined metadata (affected team, region, customer…).
- **Timestamps**: when key moments happened. Most are set automatically as the
  incident progresses; a few are yours to set.
- **Channel**: where the humans respond (Slack or Teams). Updates you post land here.

Hanging off it: **alerts** (may have triggered it), **escalations** (pages sent to
people), **updates** (the running narrative), **actions** (work to fix it *now*) versus
**follow-ups** (work for *after*), an optional AI **investigation**, and a **postmortem**.

The lifecycle, as a map (the enforced rules live in lifecycle.md):

```
                       ┌─────────┐
       accept          │ triage  │──decline──→ declined ─(undecline)─→ triage
  ┌───(needs type)─────┤         │──merge────→ merged ──(unmerge only)
  ▼                    └─────────┘
┌───────────┐
│  active   │──pause──→ paused ──(resume)──→ active
│ (the org's│──cancel──→ canceled  (terminal)
│ statuses) │──resolve─→ post-incident ──→ closed
└───────────┘──close───────────────────────→ closed
     ▲                                         │
     └───────────────── reopen ────────────────┘
```

An incident's **mode** says what kind of incident it is, and each one behaves differently:

- **standard**: a real, live incident, announced and counted in metrics. Most incidents
  are standard.
- **test**: practice. It isn't announced and is left out of lists and metrics, and
  workflows run on it only when a workflow opts in, but paging from it still wakes real
  people. Use it for "check the workflow fires" or a drill.
- **retrospective**: recording an incident that already happened. It's created closed
  (or in post-incident) and not announced, with its real times in its timestamps.
- **tutorial**: onboarding practice.
- **stream**: a workstream split off a large incident, on organisations with streams
  enabled. It has its own lead, updates, roles and actions; severity, type, custom fields,
  the summary and follow-ups stay on its parent. Use one to run parallel work (comms, a
  recovery, legal) instead of declaring a separate incident. A stream is started with
  `/inc stream` in Slack or from the dashboard; nothing you can call starts one, so its
  absence doesn't mean streams aren't enabled. A parent with open streams
  can't be closed, merged, declined or canceled until they're closed (lifecycle.md
  covers working in one). `incident_show` gives a stream's `parent` and a parent's
  `streams`. A private stream's name, status and lead are shown to everyone in its
  parent, but nothing else about it: name it, don't guess at what it holds.

Its **visibility** is public or private — and a
private incident you can't see comes back as *not found*, not *forbidden*. If a lookup
that should exist returns nothing, say it may be private and point the user to the
dashboard rather than probing.

## Ground rules

These apply to every job:

1. **Read the org's configuration before your first write** (`config://organisation`; the
   section above says how). It carries *this* organisation's statuses with their categories,
   severities, roles, incident types, custom fields and timestamps — plus who *you*
   are, so "my incidents" resolves. Every org renames the lifecycle, so a status name
   from this skill is wrong somewhere; reason in categories, act with this org's own
   values, and never guess an ID.
2. **Resolve custom-field values before setting them.** A field's option values are
   listed in `config://organisation`; a catalog-typed field takes a catalog entry's id,
   which you look up with the catalog reads — pass the id, never the name. `custom_field_values` does both
   in one call, whatever the field's type, and names the key its id goes in.
3. **A write can be rejected for missing required fields.** Some custom fields are
   required only before resolving, others on every change (a field required "always"
   blocks any accept, update, or resolve while it's empty). When the tool rejects an
   update for missing fields it names them — set those in the same call, filling them
   from context rather than asking the user field by field. A declare is different:
   when `incident_create` is rejected with a prefilled declare-form link, hand that
   link to the user — don't retry with guessed values, and don't resolve the missing
   fields yourself; the form is where they finish it.
4. **A requested change is yours to make, not to propose.** When the person has asked
   for the change, said what it should be, and you can tell which record they mean,
   make it and report what you did — don't ask them to confirm first; "declare an
   incident for this" already is the go-ahead. When they asked for the change but not
   what it should be ("set the incident type", "update pls"), don't ask either: fill
   sensible values from context and pass `action: suggest`, so the card is where they
   correct you (writing.md says how). Ask first only when you can't tell which record
   they mean, or when the change would destroy work they haven't pointed at — removing
   the one record they named is theirs to ask for, not yours to double-check. Paging is
   the one exception, and the `on-call` skill owns it: a page defaults to a draft.

   Three states turn a write into something else, so ask before these, even when
   asked: resolving a triage incident declines it; a follow-up that matches an existing
   one is a duplicate, so point at it; an update saying it's resolved, on an incident
   that's still active, needs the status question answered first. Don't count on the
   tool to reject them.
5. **Never invent a severity.** Only set one that has been explicitly stated — severity
   drives paging and escalation policy, so a guessed "sev2" can wake people a real
   triage would not have. With no severity given, leave the incident in triage for a
   responder to set.
6. **A missing tool or option is this organisation's configuration.** Tools and
   options appear only where the organisation has the feature enabled: streams, test and
   retrospective modes, paging and others. When one you need isn't there, check that this
   skill says the capability exists, never going on what the user says exists. If it does,
   tell the user it isn't enabled for this organisation and point them to the dashboard;
   if the skill doesn't name it, say you can't do it. Either way, never make a different
   change as a stand-in: no standard incident for a test or a past outage, no separate
   incident for a stream, no new private incident to change visibility. A tool that only
   some sessions have, and a call that fails for a reason that isn't the incident, are
   covered under "How you reach the incident".
7. **An empty search isn't proof it isn't there.** A merged incident lives on in the
   incident it was merged into, and a default `incident_list` search leaves merged
   incidents out: search the merged category too and follow `merged_into` to the live
   incident. A follow-up the user names that `follow_up_list` doesn't return may be a
   pending suggestion: check `suggestion_list` before saying it doesn't exist.
8. **A claim about how the platform behaves needs a source.** Who gets paged, who can
   see an incident, what can't be undone: say it as a tool returned it or this skill
   states it, and leave it out rather than guess.

## What this skill is not for

- **Fleet-wide analysis** — "how many P1s this quarter", on-call burden, alert noise.
  That's the analysis playbooks (`playbook://analysis`), which own the methodology;
  route fleet-wide questions there rather than paginating `incident_list` and counting
  by hand.
- **Finding runbooks** — routing a symptom to the procedure that owns it is the
  `runbooks` skill. Ground an incident here, hand over there.
