# What works

What the best-performing skills share, drawn from incident.io's own estate — the
skills our agents follow most reliably — and from the retrospective assessment of real
usage. None of these are mandates: they're what the evidence keeps crediting, so a new
skill should have a reason to deviate rather than a reason to comply.
[example.md](example.md) shows most of them in one worked skill.

## The shape: a reusable utility, not a task script

The skills that keep earning loads are utilities: they teach an agent to *understand
and interrogate one system*, and the procedures fall out of that understanding. A
runbook, another skill, or a person can invoke them for any question about the system
— not just the one task the author had in mind. The anatomy that recurs:

1. **A model with its consequence.** One paragraph of system shape, ending in why it
   matters: "every message lands on exactly one of two regions — so a count from one
   region is never the whole picture." An agent holding the model can handle cases the
   procedure never enumerated; an agent holding only steps cannot.
2. **Scope, with owners for what's out of it.** "This skill covers operating X. How X
   is built is owned by <the architecture doc>; the recovery procedure by <the
   runbook>." One sentence per neighbor stops the skill absorbing them.
3. **Vocabulary.** The mapping between the system's names and the tools' names, with
   the traps: renames, case conventions, fields that look alike and aren't.
4. **The tool surface**, declared once (see the format's naming rules). The best form
   is a need-keyed table — "what you want → where it comes from" — with references in
   the same table as tools, so "where do I get X" has one answer surface.
5. **Reading results.** What the values mean, especially the edges: does null mean
   zero, unknown, or unreadable? Is absence confirmed or unqueried? Can one provider
   fail without failing the call? Spell these out — misreading null as zero is the
   single most common way a correct procedure produces a wrong answer.
6. **Common flows** — the two or three questions the system actually gets asked, each
   walked from evidence to answer.
7. **Negative space.** "Questions this can answer" and "what this skill doesn't do",
   with a route for each exclusion — the neighboring skill, the runbook, the
   dashboard. Include the off-ramp rule: a capability this skill's tools lack is not
   proof the thing can't be done; route it rather than declaring it impossible.

Not every skill earns the full anatomy. When the job is one fixed report or a single
narrow action, the shape collapses to the description, the output contract, and the
one flow — inventing a system model for a daily digest is padding, not craft. The
utility shape is for skills that answer many questions about one system; grow into it
when the second and third question arrive.

## Action requests are requests for the work

An action-shaped request — unblock the number, raise the ticket, requeue the batch —
is a request for this work, not for permission to start it: do the diagnosis and
produce the deliverable rather than offering to. Where the skill must not take the
action itself, teach the stance the best skills use: you draft; a human sends. Say
what the draft is for and where it goes, never that it was done. A skill that answers
action requests with offers leaves the asker exactly where they started.

## Destructive actions get gates

Where a tool changes the world (a purge, a kill, a delete), the best skills put a
numbered decision list in front of it: is the system healthy enough to act on, will it
recover by itself, what exactly is lost, is the loss acceptable per target, does the
action cover the whole surface or half of it. State what's reversible and how. Where a
real incident taught the lesson, cite it — one line of provenance keeps the gate from
reading as ceremony.

## Evidence discipline

- **Start from carried evidence.** Tell the agent what the incident, alert, or
  conversation already carries before sending it to tools: the error string on the
  alert, the identifiers in the thread. Skills that start from carried evidence finish
  faster and burn fewer calls than skills whose step 1 is always a fresh query.
- **Zero and failure never render the same.** "No results" and "the source couldn't
  be asked" are different findings; a source failure that renders as a clean result is
  the worst bug a skill can have. Distinguish them mechanically where possible.
- **Don't count your own footprints.** An agent investigating a system it is
  instrumented inside will find its own calls in that system's logs and traces — a
  phrase search for the symptom returns the searches. Say how to exclude the agent's
  own traffic wherever a skill searches for a string it also emits. Hits that turn out
  to be your own queries are not corroboration, and they read exactly like it.
- **Numbers carry their provenance.** The exact expression that produced a figure,
  a link to where it can be re-run, the version or commit the reading came from.
  A number the reader can't reproduce is an opinion.
- **Citations carry their lesson, not their particulars.** Naming the case that taught a
  rule is worth a line, but its specifics travel with it: an agent that matches a symptom
  to the cited case will reach for that case's subject and identifiers as though they
  were this one's. A worked example quoting a real symptom is the easiest way to make a
  skill answer confidently about the wrong subject. Cite for the lesson, and say in the
  same breath that the specifics are illustrative — a different subject every time.
- **Windows are anchored and honest.** Compute dates from the conversation's current
  date, never the model's sense of now; anchor analysis windows on when the event
  happened, not when the question was asked; where retention clips a baseline, clamp
  and say so. A source younger than the window ranks on partial data — present its
  ranking flagged as partial, never as the top source.
- **Costs are budgeted.** Name which calls are expensive, rank on the cheap ones and
  confirm with the dear ones, and give a stop rule: "after two empty attempts, report
  what you have and name the gap."

## Volatile values live in one place

The boundary: **identifiers and handles the skill can't work without go in one dated
table; measurements, counts, and limits are never pinned anywhere** — name where the
live value can be looked up instead. The table — never scattered prose — carries three
things: a "last verified <date>" stamp, the recipe for re-resolving a value that stops
working, and the instruction to write the corrected value back. A skill that pastes
the same identifier in six places is six edits behind the day it changes. The same
rule covers traps and lessons: state each once, where it bites, and point at it from
elsewhere — five prose copies of one trap drift independently. The rule is one copy,
not one location: a section designed to be handed over whole (a sub-agent brief, a
paste-ready block) may carry the table inside it, as long as it's the only copy.

## Literal-signature routing

A skill's internal branches are taken on literal string matches: the alert title, the
error code, the exact phrase a responder types. Routing tables that quote these
signatures verbatim get found; paraphrases don't. When a skill classifies requests
into cases, give each case the verbatim signals that identify it, not a
characterization. Descriptions are the exception — there the broad subject hook does
the activating, and verbatim signals appear only as the two or three highest-precision
additions (see the format's description rules).

## Explicit abstention paths

Assessments repeatedly credit skills that say what to do when the answer isn't there:
"an empty result means X, say so", "if neither lookup returns it, report it
unavailable and stop", "the honest answer may be that nothing needs doing — don't
manufacture a task". Skills without a written abstention path produce confident
guesses instead — the single most damaging failure the assessments record. The same
honesty covers routes: where data exists but nothing in reach serves it, say exactly
that rather than naming a route that doesn't exist.

## Conditional capability, not assumed capability

What a connection serves is an allowlisted subset that changes, so check a tool is
there rather than assuming its name — and that a tool is available is not a reason to
use it. Every dependency gets a fallback phrased as behavior, not setup — format.md's
absence path carries the canonical sentence form and the three fallback classes.
Skills that assume a tool exists fail loudly in the environments that lack it, and
never present a guess as though the missing tool had answered.

## An output contract, stated once

Skills whose answers end in a fixed set of headings get followed to completion; skills
that describe the output in prose get partial answers. State the contract once, show
the block, and say which fields survive abstention — an unanswerable section reads
`unknown — tried <what>`, never silence. And the reply itself carries the answer:
whoever asked is usually reading in chat and cannot open a file the agent wrote, so
"I've written the report to <path>" delivers nothing. Write files where the
environment collects them — as records — but never in place of the answer in the
reply. Two refinements from the best skills: give multi-step procedures
a "done when" line per step, so a half-finished step is visible to the agent running
it; and wherever you test the skill, assert the same headings, so a dropped output
shape fails on the contract rather than on a reviewer's mood.

## Road-tested before shipped

The defects that survive authoring are the ones the author can't see: instructions
that read two ways, a tool argument that was renamed, a step that assumes context only
the author holds. A fresh reader executing the draft cold finds them in one run —
every skill we road-tested this way surfaced fixes no review pass had caught. The
procedure is create's road-test step; the pattern is the reason to never skip it.

## Judgment in prose, plumbing in scripts

Where part of the job is deterministic — filtering, sorting, rendering a fixed format
— put it in a bundled script and have the skill call it, with the rule "edit the
script, not the prose, when the format changes". Keep the judgment (what matters, what
to say about it) in the skill body. Mixing the two gets both wrong: prose drifts from
the format, and scripts accrete judgment nobody reviews. A script is also a
portability liability — see the format's environment rules before bundling one.
