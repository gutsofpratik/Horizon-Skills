# Lifecycle

How an incident moves through its statuses, and the rules the status tools enforce.

Status changes go through `incident_update`'s `incident_status`. Prefer an intent
word — `accept`, `resolve`, `close` — which routes to the right destination for you.
A status name or ID also works. `config://organisation` shows each status with its
category. Reason in categories.

## The eight categories

- **triage** — reported, not yet assessed. No severity required; the team decides
  whether it's real.
- **active** — a live incident being worked. The org defines one or more active
  statuses (e.g. Investigating, Fixing, Monitoring).
- **paused** — temporarily on hold.
- **post-incident** — resolved, now in the learning phase (postmortem, review).
- **closed** — fully done.
- **declined** — a triage incident judged not to need a response.
- **merged** — folded into another incident.
- **canceled** — called off.

## Leaving triage — the fork

Triage has three exits, and **a triage incident cannot be canceled directly**: cancel
acts on an incident that's been accepted into a response, and this one hasn't. A `resolve` or `close` intent on a triage incident
declines it rather than resolving it.

- **Accept** → set an active status. This is the "yes, we're responding" decision.
- **Decline** → set the declined status. The right move when it turns out not to be a
  real incident — this, not cancel, is how you reject a triage incident (the tool
  rejects triage → canceled with "you can only cancel an incident when it's not in
  triage").
- **Merge** → same problem as an existing incident; read `references/responding.md`
  for the mechanics and the judgement.

**Accepting requires an incident type in the same call.** Incidents declared from
alerts often have no type. If the incident has no type, pass `incident_type_id`
alongside `incident_status` in one call — the type can only be set while still in
triage, so a later call can't fix it, and an accept without a type is rejected with
nothing applied.

## Pausing

Pausing a triage incident is one call: `incident_update` accepts it first, then
pauses it. Don't split it into two.

Pausing requires `unpause_at`, the time the incident should resume. Never hand-build
that timestamp — daylight-saving offsets shift, so a constructed one is silently
wrong. Resolve it from a known-good clock and pass the result through verbatim. A resume
point given as a day with no time means the start of that working day: resolve 09:00 in
the user's timezone rather than asking. Only ask how long when no end was given at all.

## Canceling

Cancel abandons an accepted incident that's no longer worth pursuing — set the
canceled status. It's rejected from triage (decline instead) and from declined, and
cancellation is terminal.

## Resolving and closing

To a responder, "resolved" means the response is over: the incident leaves its active
status. The request is the go-ahead, whatever the incident's files suggest about how
finished it is (ground rule 4). Where it lands is the org's configuration — a
post-incident status where the org runs a learning flow, closed otherwise — and nothing
in the incident tells you which. Pass the intent word and let it route rather than
picking a status by name.

- **Resolve** → `incident_status: resolve`. This starts the learning flow (postmortem,
  review) where the org runs one, which is why it's distinct from closing.
- **Close** → `incident_status: close`. Skips or ends the post-incident flow.

Resolving is a common point for a required-fields rejection (orgs often require fields
before resolution) — the required-fields ground rule covers how to handle it, and it
isn't resolve-only.

## Reopening — the asymmetry

- **Declined** can be reopened: back to triage (undeclined) or straight to an active
  status. Declining is a judgement, and judgements get revisited. Until then, a
  declined incident accepts *only* a status change — to change anything else, reopen
  it first.
- **Closed** can be reopened to an active status, when the work turns out not to be done.
  Nowhere else: not triage, paused or canceled.
- **Canceled** cannot be reopened. It's terminal.
- **Merged** only comes back via unmerge — a status change can't do it, because the
  merge moved its data into another incident.

## Streams

A stream has its own short lifecycle: open, then closed. It can't be paused, declined,
canceled or merged, and it has no severity, summary or custom fields of its own, so
those changes belong on the parent: make them there and say which incident you
changed. A public stream's updates are also posted in the parent's channel; a private
stream's aren't.

Close a stream with a final update saying how its work ended, because the closure is
announced in the parent's channel. A parent can't close, merge, decline or cancel while
any stream is open, and the refusal names them. Name them and ask whether to close
them, each with its own closing update, then the parent. Close none unasked, and don't
retry the parent's close while they're open.

## One call per change, and never repeat a success

Put everything that can share an `incident_update` call into one call. **Every execute
posts a real, visible message to the channel**, so a redundant call is spam the whole
response team reads: a rejected call applied nothing (fix it and call again), but an
accepted call has already posted, so never repeat it to "retry".
