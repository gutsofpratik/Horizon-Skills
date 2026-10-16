# Write architecture docs

Author or extend architecture docs. This job exists to prevent one failure mode: an
agent that writes fluent, plausible architecture documentation around system boundaries
it guessed. The names people use for their systems are ambiguous — "the API", "the
platform", "the backend" — and where one system ends and the next begins is a decision
the team has made (or needs to make now), not a fact you can infer from a directory
listing. So the heart of this job is an interview, and the drafting comes second.

## 1. Search first

Never write before searching. The search is the skill's "Before you start" step:
the `architecture` skill, loaded and run on each system name in scope. If you have not
run it yet, run it now. What exists shapes everything after: an existing doc means
extending it, not writing a sibling, and the docs you find are evidence for the
interview.

## 2. Resolve the home

The writing ladder in [homes.md](homes.md) decides this — read it
before choosing, even when the answer looks obvious, because the right home depends on
where the team's corpus already is and on who needs to read the result. Confirm the
choice before writing into an external system.

## 3. The interview

Run it in the voice the `talking-to-the-user` skill
sets — one question at a time, carrying what it turns on.

Work system by system. For each system name the user uses, before writing anything:

**Enumerate the candidate referents you can actually see.** Ground every question in
evidence from the workspace and tools in reach — repo layout, deploy and infrastructure
config, service manifests, build files, the docs you already searched. Never present
invented options.

**Ask the user to pin the boundary.** One system at a time, one question at a time,
naming the specific candidates. The shape of a good question: "You said 'the platform'.
In this repo I can see a Go service under `server/`, a React app under `web/`, and a
Terraform directory deploying both. Is 'the platform' the Go service, the service plus
the web app, or the whole deployable unit?" The user's answer is a decision — record it,
don't relitigate it later.

**Apply the system test to decide structure.** A thing earns its own system directory
when responders reason about it separately during an incident — usually because it is
deployed differently. The repository is irrelevant to this test: two systems can share a
repo and a deploy, or one system can span repos. Ask the test directly when it's
unclear: "When the web app breaks, do the same people look at the same dashboards as
when the Go service breaks — or is it a different failure world?"

The test can also resolve to an **estate service** rather than a system: when the thing
reasoned about separately is a family of tools serving every system — observability, the
data platform, CI — it gets a directory whose README is a tool-routing table rather than
a system README, per [format.md](format.md). The tell during the interview: no answer to
"where is it deployed" makes sense, but "which tool answers which question" does.

**Capture resolutions in the doc, not just the conversation.** Each system README opens
by stating its boundary explicitly ("the Go binary in `server/`, deployed as `web` and
`worker`; the dashboard shares the repo but is its own system") — the next reader gets
the decision, not the ambiguity.

Interview discipline: few questions, concrete, grounded in visible evidence, one at a
time when boundaries are contested. If the user's answers are uncertain ("I think
those are the same thing?"), record the uncertainty in the doc as an open question
rather than resolving it by fiat.

## 4. Draft to the format

Write per [format.md](format.md) — or the corpus's own FORMAT.md, which wins. Structure
each system's docs from the concern catalog ([concerns.md](concerns.md)) — it lists the
questions each concern file answers — and calibrate depth against the worked example
corpus ([examples/](examples/README.md)): match the nearest example file rather than
inventing a shape. The rules that matter most while drafting:

- **Facts, not procedures.** Steps to diagnose or fix belong in a runbook — link to it
  by exact title. Levers may be named ("the lever is the per-org gate"), not walked.
- **Verbatim, verified identifiers.** Every project, cluster, namespace, hostname,
  bucket, path, and flag named gets checked against the code or config in reach. A claim
  that doesn't verify is dropped or generalized, never shipped.
- **Provenance over precision.** Never pin a value that churns — replica counts, machine
  types, limits, defaults. Name the file or repo that owns the current value, so a stale
  doc degrades into a correct lookup instead of a wrong answer.

Update the corpus README map (the estate table and "Where do I look?" routing table) in
the same change.

## 5. Views come from repeated cross-system questions

Don't write views speculatively. When the same question keeps spanning systems — "which
hostnames exist and what serves each", "how does each system participate in staging" —
that's a view: one root-level file answering that one question, with a participation
line per system and links down for detail. Propose it when the pattern appears.

## 6. Check it will be found

Run the closing check in [homes.md](homes.md): say which places will
surface the new docs, and give the user a test they can run.

## Extending an existing corpus

The interview still applies, scaled down: a new concern file or a boundary change gets
its candidates enumerated and its owner's confirmation before the edit. Pure fact
updates — a renamed cluster, a moved deployment — skip the interview; they follow the
format's maintenance rule instead (change the doc in the same change as the fact).
