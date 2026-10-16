---
name: architecture
description: >
  Answer questions about how the organisation builds, deploys, and runs its software —
  what a system is, where it runs, what it depends on, and the real names of things
  (cloud projects, clusters, namespaces, hostnames, buckets) — from architecture docs
  wherever they live. Use when asked "how does X run", "what is Y", "where does Z live",
  or when grounding a component before debugging it.
argument-hint: "<an estate question to answer>"
---

# Architecture

Architecture docs describe what systems *are*: where they run, what they depend on, and
the real names of things. They pair with runbooks — runbooks own *procedures* (how to
diagnose and fix a failure), architecture owns *facts* (what the component is in the
first place). This skill answers estate questions (the estate: everything you run and
where) from those docs, cited — never from general knowledge. General knowledge is
exactly what these docs exist to override: a team's setup differs from defaults in
precisely the ways worth writing down.

## Where you are running

You are a coding agent with incident.io's skills.

- **Before you start:** load the `extensions` skill and have it map the estate — which
  plugins are registered, where each lives, and their sync state. Skipping it doesn't
  fail loudly. It just means you searched the local half of the estate and reported it
  as the whole.
- **Where to search:** the four places in
  [where-docs-live.md](references/where-docs-live.md), in its order. Read it before
  searching, even when you think you know where the docs are.
- **Where live config lives:** the workspace.
- **When the docs have a gap:** if the user wants it filled now, that's the
  `architecture-author` skill.
- **When the question is really "how do I fix this failure":** hand over to the
  `runbooks` skill. Its Find job owns routing a symptom to its runbook.
- **How to reply:** in the voice the `talking-to-the-user` skill sets — lead with the
  answer, be concise, one next step where there is one.

## 1. Pin the subject

Reduce the question to the system or identifier it is about: a service name, a
hostname, a cluster, a bucket, a deployment. Keep both the literal identifier (for
keyword search and grep) and the question phrasing (for semantic search).

## 2. Search

Search the places above, in their order. Start each corpus at its README — a
well-formed corpus has a "Where do I look?" routing table that resolves most questions
in one hop. Do not grep the tree before trying the map; the map exists so one hop finds
the owning file. Grep only when the map misses. Document search results carry a source
provider and generated tags; architecture-shaped documents describe systems and
infrastructure rather than procedures.

## 3. Answer from the owning doc

- **Quote identifiers verbatim** — project IDs, cluster and pool names, hostnames,
  subscription names. A paraphrased identifier is worse than none.
- **Cite the doc** each fact came from, and the authoritative config repo where the
  doc names one.
- **Respect what the docs deliberately do not hold.** Values that churn — replica
  counts, resource limits, machine types, current flag state — are pointed at, not
  copied. Answer with where the current value lives, not a number the docs never
  promised. If the live config above holds that value, read it and say where it came
  from.
- **Keep it short.** Most questions resolve to a few sentences and one or two doc
  references.

## 4. When the docs do not cover it

First make sure that is what happened. A place you couldn't reach is not a place with no
docs, and reporting an unreachable corpus as a missing one sends someone to write a
document that already exists. Name what you couldn't search.

Once it's genuinely a gap, say so explicitly. Answer from other evidence when you have
it — deploy manifests, service definitions, config, a connected system's own listing —
clearly labelled with where it came from, not the docs. Never silently substitute general
knowledge for a missing doc.

Then note the gap as a curation candidate: a question the docs could not answer is a
section waiting to be written. Handle it as "Where you are running" says.

## Rules

- Read-only, always: this skill explains; it never mutates, flips flags, or runs
  commands that change state.
- Route, don't absorb: if the question is really "how do I fix this failure", ground
  the component here, then hand over as "Where you are running" says.

## What this skill is not for

Writing or maintaining architecture docs, diagnosis and fixes (the runbook that owns the
failure), current runtime state (replica counts, flag values — the docs point at where
those live), and product or code-level documentation (API references, user guides).
