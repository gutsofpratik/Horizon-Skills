# Responding

The judgement calls when something is breaking: whether to declare, attach or merge —
and how to do each safely. Paging someone is the `on-call` skill's. Status mechanics (accepting, pausing, resolving)
live in `references/lifecycle.md`.

## Is there already an incident?

Before declaring from an alert or a report, check for an existing open incident for
the same problem — `incident_list` over the triage/active/paused categories, matching
on names with the concrete terms (service, error, component); there's no fuzzy
similarity search, so structural filters are what you have. Two failure modes to
avoid: declaring a duplicate splits the response while a team is already working in
another channel, and attaching to the wrong incident buries a real problem.

If the same problem already has an incident, **attach the alert to it** rather than
declaring — the alert links as related and the existing response absorbs it. Detach
only when an alert was routed to the wrong incident.

## Is it them, not us?

Before attributing a failure to the organisation's own systems, check whether a third party
it depends on is already broken: `external_service_status` reads the vendor status pages
incident.io monitors. It is the cheapest hypothesis to rule in or out, and timing is weak
evidence against it: vendors routinely publish an incident well after the organisation
starts seeing errors, so a later vendor timeline does not clear them.

The tools match vendor names exactly and do no guessing — their descriptions say how to
resolve a product or an abbreviation, and what an unmonitored vendor comes back as.

## Declaring

Declare when it's a real, new problem with no existing incident. `incident_create`
starts it in triage by default, which is correct unless a severity was explicitly
stated (ground rule: never invent one) — then it can start already-accepted. Creation
is rate limited (an org can only create so many incidents an hour), so a rejected
create is not something to retry in a loop.

## Merging (and unmerging)

Merge when two incidents are the same underlying problem. That's `incident_merge`,
not `incident_update`, and several sources merge into one target in a single call —
don't loop one call per source.

The judgement:

- You need the target's identifier (an INC reference or ID) — the tool merges into the
  incident you name and can't match a fuzzy description itself. If the user names it,
  act directly; if they describe it ("merge this into the CPU incident"), find it with
  `incident_list` (open statuses, matching on the name) and confirm the match before
  merging, because a merge into the wrong incident moves this one's data under it.
- Be decisive: one clarifying question if it's ambiguous, then act. Never offer to
  merge incidents you can't see.
- Report the outcome with a link to the incident you merged into — a merge that
  silently happened is one the user can't follow.

**`incident_unmerge`** reverses it, acting on the incident that was merged *away* and
deriving the target from that incident's own history. It restores the status the
incident held before the merge, and it's the only way to bring a merged incident
back.

## Starting or steering an investigation

An AI investigation runs checks in the background — telemetry, recent code changes,
similar past incidents — and builds a hypothesis from them. Which tool you need turns
on one question: is one already running? None → `investigation_start`. One running →
`investigation_steer`, which feeds new information in and redirects its focus.

The user sees both as "the investigation", so don't explain which you picked, and
never say you can't start another. "Investigate further" or "dig deeper" on an
incident that already has one is a steer.

**Offer before you start one.** Starting is visible to responders — it posts and pins
a message in the incident's channel — so when a request would
benefit from an investigation and none is running, say what it would gather and let
the user decide.

Steer when the conversation changes the investigation's direction: a correction ("it's
Redis, not Postgres"), telemetry pointing elsewhere, a responder stating the cause, the
user's own debugging contradicting or sharpening the hypothesis.
Not detail it would find anyway. If the finding came up while you were answering
something else, answer that first, then offer to feed it in.

A steer carries the current hypothesis, the correction and the evidence (the file, the
commit, the log line). It shows in the incident's channel under the user's name, and the
investigation re-assesses within a few minutes: say that, rather than claiming the
hypothesis has changed. A message posted to the channel is not a steer; the investigation doesn't read
it.

## Capturing work as it happens

**Actions** are work to fix the incident now; **follow-ups** are work for after it's
resolved. The tools enforce that split, and the user saying "action" doesn't on its own
make something one.

## Raising a code change

"Raise a change to fix the bug", "open a fix", "code it up", "make a PR" ask for an
actual pull request. A code change is not an action or a follow-up, and logging one of
those instead is the "different change as a stand-in" that ground rule 6 forbids.

No tool here opens one. In the user's repository, make the change
and open the pull request yourself, then share it as `references/writing.md` describes.
Without a repository, say you can't open one from here and offer to capture a follow-up so
the work isn't lost.
