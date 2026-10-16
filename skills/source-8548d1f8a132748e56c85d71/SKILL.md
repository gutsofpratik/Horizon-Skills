---
name: talking-to-the-user
description: >
  How the incident.io skills speak to the person in the session: what the user hears
  and what goes in the record, ending each reply with one next step, keeping a fixed
  milestone list through a multi-step job, and using the user's words instead of the
  skills' own vocabulary. Load it before you reply to the user while running any other
  incident.io skill.
---

# Talking to the user

What's specific to this plugin about how its skills speak to the person in the session.
General style — length, tone, formatting — is the user's own agent's business and isn't
set here. The reply shape (answer, Progress, Next step) is in each skill's SKILL.md.

## Only what changes what they do next

Everything a skill learns has two audiences: the user, and the record (the report a
job files — an estate report, a review, a pull request description). The record gets
the machinery: checks run and passed, tools present or absent, tool output, sync
states, why steps run in this order, what was declined and why. The user gets only
what changes what they do next: a decision that is theirs, an action only they can
take, a blocker, anything created or changed in their repository or account. When
machinery matters to them, give its consequence — "incident.io can't read that
repository yet" — not the mechanism.

## One next step

While a skill is driving a job, each reply ends with the one thing the user does now
and what it unblocks. One step, never a list. The block is for what only the user can
do; when the next move is yours, do it in the same reply. Where creating something
needs a yes, the yes is the next step. Where a choice is theirs to make, offer the
options with your recommendation marked, and the next step is "pick one". A one-off
question, a filed report and an unattended run have no block.

## Milestones

A multi-step job lays out its milestones once the goal is agreed — in dependency
order, each with what "done" looks like — and gets a yes before anything is created.
That yes covers every artefact the list names with what it will contain; anything not
on the list is proposed separately. Show the list on every reply until the job is done
— it's how the user knows where they are — after the answer, before the Next step. Once
agreed, the list is fixed: same milestones, same words, same order on every reply, and
only the ticks move. Rewriting it each turn is disorienting. When the plan genuinely
changes, say so in the answer and change the list once: a milestone that turns out
unnecessary is struck, not silently dropped; a declined recommendation is marked
declined. A skill that picks up the job mid-way keeps updating
the list it inherited. The sequence belongs to the job's own reference — for plugins
and skills, the `extensions` skill's estate reference.

## Their words, not ours

The user may not have read any file in this plugin; never rely on it. Don't cite a
reference filename, a ground rule or a step number at them, and describe what happened
rather than how you did it. The vocabulary of this plugin's references — readers, road
tests, claims lists, the estate walk, loads and funnels — is for you. Sub-agents, fresh
sessions and verification runs are your machinery: report their result, never their
existence, and don't comment on your own process ("the road test doing its job").

> Both readers are back. First rehearsal failed on two delivery rules — the road test
> doing its job. Fixed: 310 lines in `ops/skills/dashboard-data-staleness/SKILL.md`,
> plus two `ops/README.md` rows.

says:

> I tested it twice as a newcomer would; two things failed the first time and I fixed
> them. It adds 310 lines in `ops/skills/dashboard-data-staleness/SKILL.md` and two
> rows to `ops/README.md`.

| Don't say | Say |
|---|---|
| the estate, the estate walk | your setup; "checking what you have" |
| registered | added to incident.io |
| synced, sync state, sync error | incident.io has (or hasn't) picked up your changes |
| mount name | the name it shows up under |
| road-test, rehearsal, verify, a (fresh) reader, "the readers are back" | "I tested it"; "tested it as a newcomer would" |
| delivery rules, output contract, the format | what it has to include; how it has to be laid out |
| the source-control integration | incident.io's access to your GitHub or GitLab |
| the create job, the improve job | writing the skill; fixing the skill |
| the claims list | the facts I checked |
| the interview | our conversation; "what you've told me" |
| a load, assessed loads, the funnel | a time an agent used it; how it did |
| carry, earn its place, lean on, the home of, own | include, is useful, uses, lives in, is responsible for |
| this plugin (meaning incident.io's skills) | "me", or "the incident.io skills" |

Plugin, skill, connector, runbook and architecture doc are the dashboard's own words:
keep them, and explain each once, in one sentence, when the user first meets it.
