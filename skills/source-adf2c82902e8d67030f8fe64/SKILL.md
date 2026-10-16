---
name: on-call
description: >
  Who is on call in incident.io and how they get paged: schedules, rotas and shifts,
  overrides, cover requests, escalation paths, and pages (escalations). Use whenever
  you're working with any of these in any way, including plain reads ("who's on call
  tonight?", "when am I next on?") and paging ("page Ava", "ack my page", "has anyone
  acked?"). Load it before the first schedule, escalation or cover-request tool call:
  the tools return raw shifts and levels, and this skill says how to read them.
---

# On-call

A **schedule** holds **rotations**, each with members and **layers**: the positions
filled at the same time, like Primary and Secondary. "Primary" names a layer, not a
rotation. Shifts are computed from that configuration, so the rota isn't stored — it's rendered
for a time window. An **override** sits on top of the rotation for a window and changes
who is on call; the shifts it produces carry an `override_id`, which is how an override
is found and undone later. A **cover request** is the polite alternative: it asks the
schedule's members to volunteer, and an accepted request creates the override itself.

Only native incident.io schedules are visible. When an organisation manages on-call in
an external provider (PagerDuty, Opsgenie…), the tools say so — that means we cannot
see who is on call, never that nobody is. An organisation that doesn't run on-call in
incident.io at all has nothing here to read or change: say so plainly instead of
hunting for schedules that can't exist.

## How you reach the tools

This section is the only part that depends on where you run. The rest of the skill names
tools by their bare names and applies however you call them.

### Calling the tools

The tools are on the incident.io connection, called by the names this skill uses.

## Reading

- `schedule_show` renders a schedule's rotations and shifts over a window you choose —
  the window may reach into the past ("who was on call last Tuesday night?"), and
  `shifts_truncated: true` means narrow the window rather than summarise a partial
  picture. A shift with `uncovered: true` is a stretch nobody is on call for, so pages
  for that layer reach no one. With an `override_id`, an override cleared it; without
  one, the rota itself leaves the gap.
- "Am I on call?" / "when is someone next on?" is one `schedule_list` call with the
  `user` filter — `"me"` for the asker, a user ID or email for anyone else. Each result
  carries that user's in-progress and next shift; don't fetch whole schedules and
  compute it yourself.
- `cover_request_list` finds cover requests — "my open request", "Milly's request" —
  and returns the `cover_request_id` the respond and manage tools need. It defaults to
  pending requests; filter by `user` or `schedule_id` to narrow.
- "Who gets *paged*" is an escalation question, not a rota question —
  `escalation_path_show` resolves current on-call at every level, and each level's
  `schedules` names the schedules it pages. That is also how to answer "what uses this
  schedule": check the paths. A reference the tools don't show is unchecked, not absent,
  so say what you couldn't see rather than that nothing depends on it. A team's path comes
  from the team: `team_show` lists the paths it owns. Never pick a path because its name
  looks like the team's.
- When you hand someone over as the person to contact, check they can actually be
  reached: look them up with `user_list` and `include_inactive: true`, then read `state`
  and `seat_type`. Without that flag, a deactivated person just doesn't appear. Only an
  `on_call` or `on_call_responder` seat can be paged. The rota still renders a
  `responder`, a `viewer` or a deactivated person on their shifts, but nobody can page
  them, not even directly. Say so, and check whoever you name as taking over next the same
  way. A plain "who's on" question doesn't need the check.
- "What was I paged for?", "what woke me up", "did I miss a page" read the asker's own
  pages: `escalation_list` with `user: ["me"]` (or `escalations_list`, where the incident.io
  desktop app adds it), newest first. Each page carries
  `alert_title`, usually the reason it fired, and its incident's `incident_reference` and
  `incident_name` when it has one. Many pages have no incident; then the page and its alert
  are the answer, so don't go looking for one. `you` says whether each page targeted them and
  whether they acked it, so answer from the list rather than opening every page.
- On a page, a target with `not_paged_reason` was never paged, whatever else the record
  shows. A target without one isn't proof it arrived: check that person's seat the same
  way before saying the page reached them.
- For who is on call for a service or component, resolve it through the catalog first:
  that walk ends at the right escalation path. A rota is often named for the thing it
  covers, so when the catalog has no answer, look for a schedule named for X before
  saying you cannot tell.

## Paging

Paging needs the organisation to run on-call in incident.io: with no `escalation_create`
tool, say paging isn't available to them rather than improvising a substitute. Paging the
wrong person can wake them at 3am for something that wasn't theirs, and a page can't be taken
back, so:

- **Draft unless asked outright.** Send directly only when the user explicitly asked to page
  and there is exactly one obvious target. If the target is unnamed, ambiguous or a fuzzy
  match, ask first; never default to a team.
- **A question isn't a request.** "Can you page the backend team?" or "who's first-line on
  this?" asks what's possible: answer it, naming who you could page, but page no one.
- **Resolve every ID first.** A user, priority or escalation path comes from the catalog or
  the user list; when a lookup returns more than one candidate, ask which.
- `escalation_create` on a path returns a draft (`suggestion`), not a page. With
  `card_posted: false`, nobody sees it until you act: when the user asked for the page, send
  it with `action: execute` and only its `suggestion_id`, then say who it reaches. With
  `card_posted: true`, the card is in the conversation for the user to accept, so point them
  to it. Never call a draft paged.
- `escalation_respond` answers a page the user was sent: ack ("I've got this") stops it
  climbing the path, nack sends it on to the next level.

When the user asks which page to look at, offer one line per recent page (title, its
incident's reference and name, how long ago), newest first, and recommend one. Don't catch
them up on any page's incident until they've picked it.

## Changing cover

An **instruction** changes the rota now; a **request** asks people first. "Put me on",
"take Sarah off", "cover me for the next 2 hours" (said as a decision) are overrides.
"Can someone cover my shift?", "ask Alex to take Friday" are cover requests — even when
a person is named, asking is still asking.

Overrides:

- An override changes who gets paged, immediately and for real. When the user has asked
  for it and you can tell who covers, which rota, and from when to when, create it and
  report exactly that — don't ask them to confirm first. Ask first only when the person
  or the window is ambiguous, or for a swap between unlike shifts (below).
  Reminders, cancelling the user's own pending request, and reads never need asking.
- `NOBODY` clears the layer it's placed on for the window; use it only when asked to leave
  the rota uncovered. Afterwards, say plainly that pages for that layer reach no one in
  that window, not just that nobody is on call, and name anyone still on call on the
  schedule's other layers.
- A swap is two overrides, one on each shift. When the two shifts are on different
  layers or differ in length, confirm first, and say what each person ends up with (for
  example, back-to-back weeks). Otherwise, write both and report both.
- A schedule with several rotations or layers needs `rotation_id` and `layer_id`, or
  the create is refused. `schedule_show` lists each rotation's layers by name, and
  every shift carries `layer_name`, so "primary" is the layer named Primary. Put the
  override on the layer held by the person being replaced, even if that displaces an
  existing override.
- Creating an override replaces any existing override it overlaps on the same rotation and
  layer. The create result lists these as `displaced_overrides` — tell the user who you
  displaced, and offer to narrow the window if that wasn't intended.
- To undo one, `schedule_override_delete` takes the `override_id` from the create's
  result or from the shift it produced in `schedule_show`. Deleting an override doesn't
  bring back the ones the create displaced, so when you revert such a create, recreate them
  from its `displaced_overrides` rather than calling it restored on the delete alone.

Cover requests:

- Before raising one, or suggesting who to ask, check `cover_request_list` for a pending
  request on that shift. When one exists, say who it has already asked and who has
  responded, and nudge it rather than raising another.
  `cover_request_create` refuses a duplicate anyway.
- `cover_request_create` raises one. The requester must be on call during the
  requested window — you can only ask for cover of your own shift. When the user
  names who should cover ("can Alex take my shift?"), pass just that person in
  `candidate_user_ids` — naming a person doesn't turn the ask into an override.
- Write the request `message` in the first person, as the requester.
- Candidates respond with `cover_request_respond`: accept (the override is created
  automatically), decline, or offer part of the window. The requester drives theirs
  with `cover_request_manage`: cancel while pending, accept a partial offer
  (`candidate_user_id` from the request's candidates), or nudge non-responders.
- Both need a `cover_request_id`: when the user points at a request rather than
  handing you one ("remind them", "I'll take Milly's shift"), find it with
  `cover_request_list` first.

## Answering

- Refer to schedules, overrides, and cover requests by name in the reply — never by
  ULID. The IDs a follow-up action needs are already in this
  conversation's tool results; read them from there rather than asking the user.
- State times with an explicit timezone label, rendered for the user rather than in
  raw UTC when their timezone is known.
- After a write, own what changed: who is now on call instead of whom, and until when —
  never a bare "done".
