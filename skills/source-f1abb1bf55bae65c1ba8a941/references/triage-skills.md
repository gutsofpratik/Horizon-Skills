# Triage skills

A triage skill owns one subject — a system, a failure family, a signature — and carries
the team's procedure for it.

How a caller finds and uses one is the platform's business and changes without notice.
This file is the part that is yours: what a skill needs when the caller is an agent
mid-incident rather than a person at a keyboard.

Read [format.md](format.md) and [what-works.md](what-works.md) first — they carry the
rules every skill follows. Nothing below repeats them; this is only the delta.

## Your name and description are the whole of selection

Nothing marks a skill as a triage skill. There is no field to declare and no file that
binds one to a moment: the frontmatter name and description are read against the
incident, and that is the entire decision.

- **Name the skill after what it owns.** The name is the quickest signal a caller has,
  and the first thing a person scanning your plugin understands, so spend it on the
  subject. `payments-ledger` or `checkout-queue-triage` says what it covers;
  `incident-triage` or `production-issues` says what everything covers.
- **The name that counts is the frontmatter `name`, not the directory.** format.md is
  right that the directory name is the skill's identity — usage history and allowlists
  key on it — but selection reads the frontmatter. A skill in `skills/twilio-triage/`
  whose frontmatter says `name: twilio` is chosen as `twilio`. Keep the two the same
  unless you have a reason not to.
- **The description has to back the name up.** It holds the veto: a fitting name over a
  vague description loses to a plain name over a sharp one. Apply format.md's
  description rules strictly — lead with the subject stated broadly, then the two or
  three signals only you match.
- **A subject can be a class of incident, not just a system.** Selection reads
  everything the incident carries, not only its error string — how it is classified,
  what its fields record, what it is called. A team that handles one class the same way
  every time can own that class: name it for the class and say so in the description.
- **Name the subject, however broad it is.** "Incident triage" or "production issues"
  names no subject at all, so there is nothing to match on. Saying which incidents to
  run on is fine even when the answer is all of them: a skill for working out which
  customers an incident affects, against your own tenancy model, applies to everything
  and still has a subject worth matching.
- **Use the words your organization uses.** Selection matches your name and description
  against what the incident actually carries. A skill named for a severity your
  organization does not use by that name, or for internal shorthand nothing records,
  matches nothing.

## Nobody is there to ask

The procedure runs once, unattended. There is no one to answer a follow-up, confirm a
guess, or pick between two branches.

- **Every branch is written down before it runs.** A step that ends in a decision needs
  the decision rule beside it.
- **State your entry conditions.** You may be reached with the failure already
  characterised, or with little more than a symptom. Say how to resolve the identifier
  the request didn't carry, and require an inferred one to be labelled inferred — see
  format.md's entry conditions.
- **A step that assumes a console, a laptop or a teammate stalls the procedure.** You are
  followed with the session's tools, not by the person who wrote you.

## You are not the first to look

An automated caller usually arrives holding evidence already: the alert, recent changes,
messages, prior incidents. Whether it hands you a summary or a mounted workspace differs
by environment ([agent-environments.md](agent-environments.md) has the map)
— what holds everywhere is that re-deriving what it already gathered spends the
incident's time on facts it was handed.

- **Start from carried evidence**, per what-works.md's rule, then query into the gaps.
- **Say what you need rather than fetching it twice.** Where a fact is likely already in
  hand, name it as an input instead of writing a step to go and get it.

## Your findings are someone else's evidence

Assume your output is lifted into a larger picture rather than read as a standalone
report. That changes two things.

- **State your output contract once**, per what-works.md, as a short set of headings.
  A procedure that ends in a fixed shape gets carried accurately; one that trails off in
  prose gets summarised away.
- **Every claim carries where it came from.** A caller can only attribute what you
  attribute. An unattributed finding is dropped, or carried without provenance — which
  is worse.
- **Say plainly when the answer is not there.** what-works.md's abstention rule matters
  more than usual: a confident guess made early gets built on.

## Round-trips cost time, depth does not

Whatever reaches for your procedure is waiting on it, and during an incident that wait is
paid by the people responding. But the cost is in how many times your skill has to go and
ask, not in how much it has to say. Time spent getting the question right tends to be
repaid by the work nobody then has to redo.

what-works.md's cost rule carries the mechanics: name which calls are expensive, rank on
the cheap ones and confirm with the dear ones, and give every search a stop rule. Two
things this caller adds:

- **Count the round-trips, not the words.** A procedure that could be three queries and is
  twelve delays every conclusion behind it, however tersely it is written. Say which calls
  can be made together, so a caller doesn't serialise what it could ask at once.
- **Say where a step is slow, and what it buys.** Then a caller can skip it on its own
  judgement rather than discovering the cost midway.

So don't truncate a step that decides the answer, and don't pad one that doesn't. Being
fast is not the same as being brief. The test is whether a responder would thank you for
the wait.

## What earns the reach

- **One subject, owned.** The utility shape in what-works.md is the target: teach the
  agent to interrogate one system, and the procedures fall out of that understanding.
- **Something a generic caller cannot work out.** Your value is the part that is true
  only of your estate — the vocabulary, the trap, the check that is obvious to your team
  and invisible from outside it.
- **Reading results correctly.** Confusing zero with failure is the most common way a
  correct procedure produces a wrong answer — see what-works.md's rule that the two never
  render the same.

## What gets you skipped

- **A skill with no stated subject.** "Incident triage" or "production issues" gives a
  caller nothing to match on. Applying to every incident is fine; saying nothing about
  what you do is not.
- **A skill that assumes a conversation.** Nobody is there to answer.
- **A skill that re-runs what the caller already swept.** Those results are already in
  hand.

A skill that never gets chosen is a problem with the name or the description, not with
the body — the body is only read once selection has already happened.
