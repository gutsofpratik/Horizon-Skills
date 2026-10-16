---
name: architecture-author
description: >
  Write and maintain architecture docs — the documents that say what each system is,
  where it runs, what it depends on, and the real names of things (cloud projects,
  clusters, namespaces, hostnames, buckets). The heart of it is an interview that pins
  down what each system name actually means before anything is written. Use when asked
  to write, extend or improve architecture documentation, to document a system, or to
  fill a gap the `architecture` skill could not answer.
argument-hint: "<the system or systems to document>"
---

# Architecture author

Architecture docs describe what systems *are*: where they run, what they depend on, and
the real names of things. They pair with runbooks — runbooks own *procedures* (how to
diagnose and fix a failure), architecture owns *facts* (what the component is in the
first place) — and each side chains to the other rather than absorbing it. This skill
writes and maintains those docs. Answering questions from them is the `architecture`
skill's job, and every write starts there: you search what already exists before
writing anything.

## Before you start

Do both of these before anything else here:

1. **Load the `extensions` skill and have it map the estate**: which plugins are
   registered, where each lives, and their sync state.
2. **Load the `architecture` skill and follow it through its search** for each system
   name in scope. It searches every place architecture docs can live. What it finds
   shapes the whole job: an existing doc means extending it, not writing a sibling.

Skipping them doesn't fail loudly. It just means you wrote a second copy of a doc that
already existed, somewhere nobody looked.

## The job

Author or extend architecture docs. The heart of it is an interview that resolves what
system names actually mean before anything is written: the names people use are
ambiguous, and boundaries are decisions the owner makes, not facts an agent infers.
→ [references/write.md](references/write.md)

Where the new docs go, and how to check they will be found, is
[references/homes.md](references/homes.md).

## The taxonomy

Architecture docs work when they follow a small structural spec — systems are
directories (one per thing responders reason about separately, regardless of repo
layout), views are root files answering one cross-system question, estate services
(observability, the data platform, CI) are directories whose README routes across
their tools, the README is the map, and churny values are pointed at rather than
copied. The spec lives in [references/format.md](references/format.md); a corpus may
carry its own FORMAT.md, which takes precedence.
[references/concerns.md](references/concerns.md) catalogs the recurring concerns
(deployment, database, events, …) and the questions each file answers, and
[references/examples/](references/examples/README.md) is a complete worked example
corpus to calibrate depth against.

## What this skill is not for

Answering questions from existing docs (that's the `architecture` skill), diagnosis and
fixes (the runbook that owns the failure), current runtime state (replica counts, flag
values — the docs point at where those live), and product or code-level documentation
(API references, user guides).
