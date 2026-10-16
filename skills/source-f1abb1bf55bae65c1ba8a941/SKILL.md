---
name: skill-authoring
description: >
  Create and improve the skills in your own plugins — the ones incident.io's agents
  and your coding agents load. Use whenever you're writing, editing, or reviewing a
  skill in any way: creating one, improving one from usage feedback or a review
  brief, or asking what makes a good skill.
argument-hint: "<what the skill should do — or the skill to improve and why>"
---

# Skill authoring

A skill is instructions your agents follow: a SKILL.md with a triggering description,
plus references it loads on demand. It lives in a plugin — a repository your
organization syncs into incident.io and can also install into coding agents. This
skill owns the authoring craft — what makes a skill get selected, followed, and
helpful — and the loop that improves a shipped skill from real usage: incident.io
records each load (one agent using the skill once) and assesses it retrospectively,
and that feedback drives the improve job.

## The two jobs

- **Create** — author a new skill into the user's plugin: pin it down with concrete
  trigger examples, check nothing owns the job already, draft to the format, register
  it, ship it. → [references/create.md](references/create.md)
- **Improve** — edit an existing skill from evidence: read its usage feedback with
  improve.md's reading corrections applied, fix by theme without undoing credited
  strengths, verify the fix against the recorded issue where the session can, ship,
  confirm. → [references/improve.md](references/improve.md)

Both jobs load the same two files before drafting:
[references/format.md](references/format.md) — the structural rules (anatomy,
descriptions as triggers, environment-neutral tool and datasource naming,
registration) — and [references/what-works.md](references/what-works.md) — what the
best-performing skills share, from incident.io's own estate and the assessment of
real usage. Format answers "is this valid"; what-works answers "will this get
followed". [references/example.md](references/example.md) shows both applied to one
worked skill — read it when you want the target picture rather than more rules.

One further reference is conditional:
[references/triage-skills.md](references/triage-skills.md) — read it when the skill
should be reached for by incident.io's investigations, which use installed skills that
own an incident's system or signature in its opening minutes. Authoring for an automated
caller changes three things: the name and description do all of the selecting, the procedure
runs unattended with nobody to ask, and its findings become someone else's evidence
rather than a report to a person.

## Where the skills live

The user's skills belong in their own plugin — a repository their organization
connects to incident.io — never in this one. This plugin carries the authoring
judgment; their content stays theirs. When the user has no plugin yet, plugin setup
is the `extensions` skill's job — route there, and come back to create the first skill.

Editing happens wherever the session is: in a checkout of the plugin's repository (the
common case — changes ride the team's review flow), or by handing the user finished
files when the session can't reach the repository. Never write into a plugin the user
didn't point you at.

## What this skill is not for

Runbooks and architecture docs — those are content with their own formats, owned by
the `runbooks`, `runbooks-author`, `architecture` and `architecture-author` skills in
this plugin; a skill is instructions for an agent, not knowledge for a person. And reviewing all your
plugins at once ("are our skills healthy?") is the `doctor` skill's job — this skill
works one skill at a time, from evidence about that skill.

## Ground rules
- **Speak the user's language, not this skill's.** The user may not have read this
  file; say what you're doing plainly. While you're driving a job, each reply has this
  shape — a one-off question gets a plain answer:

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

  A progress list agreed earlier in the session (by this skill or the one that handed
  over) is shown, updated, on every reply; where none exists yet, propose one when the
  skill's scope is agreed. Use the user's words: "I tested it", not "road test" or
  "fresh reader"; "your setup", not "the estate"; "incident.io has picked up your
  changes", not "synced". Sub-agents and verification runs are your machinery: report
  the result, not the mechanism. The `talking-to-the-user` skill has the full
  table.
- **Stamp what you write.** Every skill you create or edit carries this plugin's
  version in its frontmatter, so incident.io can tell which skills came through this
  flow. If you loaded this skill through the incident.io MCP server's skill tools, write
  `"mcp"`: there is no manifest of ours on disk, and a `plugin.json` you can see belongs
  to the repo you're working in. Otherwise read the version from this plugin's manifest,
  `plugin.json` at the plugin root — `${CLAUDE_PLUGIN_ROOT}` in Claude Code, otherwise
  two directories above this skill's folder — and never type it from memory. If the
  manifest can't be read, write `"unknown"` and tell the user. The format is in
  format.md's provenance stamp section.
