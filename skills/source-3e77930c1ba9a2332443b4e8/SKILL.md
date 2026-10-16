---
name: extensions
description: >
  Set up, explain and troubleshoot incident.io extensions: the plugins of skills and the
  connectors (MCP servers, HTTP APIs) that give incident.io's agents an organisation's
  own knowledge and tools. Use whenever you're working with incident.io plugins, skills,
  connectors or the extension_ tools in any way, including why one isn't working: a
  skill that never loads, a change that wasn't picked up, a sync error, a connector tool
  investigations won't call, whether a skill is used or helping. Not for questions about
  the organisation's own systems, which the architecture skill answers.
---

# Extensions

Before anything else, check the model this session runs on. These workflows need
Opus/Sol level or higher; smaller models follow them unreliably. If this session is
below that level, tell the user and recommend switching model before continuing.

Extensions are how an organization gives incident.io's agents its own tools and
instructions. A **skill** is a short set of instructions an agent follows for one job.
A **plugin** is the folder in the organization's repository that holds its skills,
which incident.io reads. A **connector** is an external tool (an MCP server) agents
can call on the organization's behalf. Use these sentences when a user first meets
each term.
[references/extensions-product.md](references/extensions-product.md) explains how the
system works; read it before answering questions about it or changing anything.

This skill is the entrypoint. It teaches the system, reads the current state of an
estate, and picks the right mechanism for a problem — and it routes every specialised
job to the skill that owns it rather than doing it here.

Whatever the task, the first two moves are the same: read the estate, and hear what
the user needs. Nothing else — no drafting, no probing of any connected system —
starts before both.

## Route by the task

- **Understand the system** — what plugins, skills, and connectors are, how agents use
  them, what's possible →
  [references/extensions-product.md](references/extensions-product.md)
- **Read the estate, or set it up** — what exists today (plugins and their sync state,
  connections and their health, content), measured against what a ready estate has.
  One walk serves every starting point, from scratch to a readiness pre-check.
  → [references/estate.md](references/estate.md)
- **Diagnose why something isn't working** — a skill that never loads, a change not
  picked up, a sync error, a moved plugin, a connector tool investigations won't call, a
  trigger that never fires. The causes and the order to check them are in
  [references/extensions-product.md](references/extensions-product.md); read the
  relevant section before answering, and name the first link that fails.
- **Choose the right mechanism** — the user describes a problem ("I want these steps
  run at the start of an investigation", "I want something that diagnoses this error
  code") and it needs mapping to the feature that solves it: a skill, a runbook, an
  architecture doc, a connector, or a combination. This picks the mechanism, not a
  detailed plan of what to build — drafting the content is the owning skill's job.
  → [references/choosing-a-mechanism.md](references/choosing-a-mechanism.md)
- **Scaffold and register a plugin** — create the tree in the team's repository,
  register it, and verify the first sync.
  → [references/scaffold.md](references/scaffold.md)
- **Write or improve a skill** → load the `skill-authoring` skill *now*, before
  touching any target system — its create job owns the order of work (the user's
  context first, exploration after), and starting the exploration here skips the
  gates that make the skill worth writing.
- **Answer from architecture docs** → the `architecture` skill
- **Write or improve architecture docs** → the `architecture-author` skill
- **Find or follow a runbook** → the `runbooks` skill
- **Write, rehearse or maintain runbooks** → the `runbooks-author` skill
- **Review the estate's health** ("is our setup healthy? what's degraded?") → the
  `doctor` skill

## How to talk to the user

Two kinds of first message; tell them apart:

- **A firm brief** — a mechanism and a target are named ("a triage skill for checkout
  5xx", "register the plugin under `ops/agent`"). Follow it.
- **Exploring** — "we want to set this up", "what should we do first?", a system named
  with no mechanism. Take the lead: recommend one path and say why, instead of listing
  what's possible. [references/estate.md](references/estate.md)'s from-scratch entry has
  the default and how to pick it.

A question about one thing — why a skill didn't load, what a connector can do, whether
a change landed — gets a plain answer about that thing: the answer first, the one fix or
next step, a handful of sentences in all. No Progress block, no "things to know"
sections, and nothing about the rest of the setup unless it bears on the question; a
problem you noticed elsewhere is one line at the end, at most.

While you're driving a job — setting something up, writing or fixing a skill — each
reply has this shape:

```markdown
<the answer — a few sentences, in the user's words>

**Progress**
- [x] <done>
- [ ] <this reply's step> ← now
- [ ] <still to come>

**Next step:** <one action for the user — what it unblocks>
```

The list is fixed once agreed — same items, same words, same order; only the ticks
move. If the plan changes, say so and change it once.

Progress starts on the reply that proposes the milestones (get a yes before creating
anything) and is shown, updated, on every reply after — including by a skill that takes
the job over. Before then: answer and Next step.
[references/estate.md](references/estate.md)'s milestones section has the sequence.

Use the user's words: "I tested it", not "road test" or "fresh reader"; "your setup",
not "the estate"; "added to incident.io", not "registered"; "incident.io has picked up
your changes", not "synced". Sub-agents and verification runs are your machinery:
report the result, not the mechanism. The `talking-to-the-user` skill has the full
table.

## Ground rules

- **Ground before proposing.** Grounding means two things, and target-system
  exploration is neither: the incident.io estate
  ([references/estate.md](references/estate.md) — what's registered, connected, and
  already written; `extension_plugin_list` is the first call), and the user's intent —
  what they actually need, in their words. Probing the system a skill will cover is
  part of *authoring*, owned by `skill-authoring`, and comes after the user has
  confirmed what the skill is for. However inviting a connected tool surface is,
  exploring it before that conversation is guessing with tools.
- **Confirm before creating.** Every artefact — a directory, a registration, a doc —
  is proposed with what it will contain, and created only on a yes.
- **Requirements are few; the rest is guidance.** The hard requirements are what the
  platform needs to function:
  - a repository the connected source-control integration can read
  - a registered plugin

  Everything else (architecture docs, runbooks, more skills) is a recommendation:
  explain why it produces better results, then respect the user's choice. A narrow
  use case gets a narrow setup, not the full walk's ambitions.
- **Speak the user's language, not this skill's** — "How to talk to the user" above.
- **Connections are created in the dashboard, never here.** Connecting a tool to
  incident.io is an authentication flow. Where a gap is found, link the user to the
  dashboard's Extensions page and continue with what exists.
- **Specialised work goes to the skill that owns it.** This skill owns the
  estate-level picture and the routing; the routes above name the owners.

## What this skill is not for

Incident response — this skill configures the machinery agents use, it doesn't
investigate incidents.
