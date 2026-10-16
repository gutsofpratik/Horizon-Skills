# Architecture format

The structural spec for architecture docs. It's guidance with a precedence rule: a
corpus may carry its own FORMAT.md at its root, and when it does, the corpus's rules
win. The consumers are a responder mid-incident and an agent grounding itself before
it debugs — both need to find the owning file fast and trust what it says.

The contract with runbooks: runbooks own *procedures* (how to diagnose and fix);
architecture owns *facts* (what a thing is, where it runs, what it depends on). Each
side chains to the other rather than absorbing it.

## Three kinds of file

**Systems are directories.** A thing earns a system directory when responders reason
about it separately during an incident — usually because it is deployed differently. The
repository is irrelevant to this test: a system can share a repo and a deploy with
another and still be its own directory, or live in a separate repo entirely. Even a
system whose doc is one README gets a directory: the top level is the estate list, and
uniformity is what makes it scannable.

**Views are root-level files.** A view answers one question that spans systems
("what's behind each hostname", "how does each system participate in staging"), states
how each system participates, and links down for detail. A view never holds per-system
detail, and a system doc never answers a cross-system question. Even when 90% of the
estate is one system, its detail still lives in its directory: the dominant system is
exactly where "global" docs silently decay into that system's docs.

**Estate services are directories too.** Some of what responders reason about isn't a
system you ship but a family of tools serving every system — observability, the data
platform, CI. An estate service passes the same test (when the log pipeline breaks,
that's a different failure world from any product system) without being one deployment,
so its docs take a different shape: the README opens with the routing question the
service owns ("where do our signals go, and which tool answers which question") and
carries a tool-routing table, and each tool with enough to say gets its own file, held
to the same size discipline as a concern file. The split with per-system concern files:
the system's file owns the producer side (where *this* system's signals go, its
correlation keys, its dashboards), the estate service owns the tools themselves
(accounts and projects, tag vocabularies, what pages, where alert definitions live) —
each links the other, and one fact still lives once.

**`README.md` is the map**: the estate table (one row per system or estate service),
the views, and a "Where do I look?" routing table mapping questions to owning files.
Nothing else lives there. The map is what makes the corpus one-hop: any question
resolves from the map to its owning file without a tree search.

## Shapes

- **System README** — what the system is in a paragraph (opening with its boundary,
  stated explicitly), how it runs, its key identifiers, and — when split — a table of
  its concern files. Small systems stop here.
- **Concern file** — one operational concern of one system (`events.md`, `database.md`
  inside a system's directory). Split one out of the README only when it has enough to
  say; under ~30 lines it belongs as a section of the README.
- **View** — the cross-system answer, a participation list, and chains.
- **Estate service README** — the routing question the service owns, a
  what-each-tool-answers table, where alert or pipeline definitions live in code, and —
  when split — a table of its tool files. Small estates stop here.
- **Tool file** — one tool of one estate service (`sentry.md`, `datadog.md`): the
  account and project layout, the vocabulary its events or data carry, and what
  escalates. Concern-file discipline applies — split it out only when it has enough to
  say, and split *it* when it owns two subjects.

Target under ~100 lines per file; a file pushing 150 almost certainly owns two subjects.
Grow the corpus by adding directories and map rows, never by deepening the tree.

The recurring concerns a system splits into — deployment, environments, runtime,
database, caching, events, APIs, observability — and the questions each file answers are
cataloged in [concerns.md](concerns.md). A complete worked example corpus (an invented
company, written to the calibrated depth) is at [examples/](examples/README.md): when in
doubt about how deep a doc should go, match it. Every file strikes the same balance:
enough to align a reader or an agent on what the thing is and route them to the deeper
source — key facts, verbatim names, and pointers — never a manual. When a deeper doc
already exists, the concern file carries the critical facts and a link, not a rewrite.

## Writing rules

Hard rules — a change that breaks one goes back.

- **Facts, not procedures.** Steps to diagnose or fix belong in a runbook — link to it
  by its exact title. Operational *levers* may be named ("the lever is the per-org
  gate"), not walked.
- **One fact once.** A fact lives in the file that owns its subject; everyone else
  links. Identifiers (project IDs, hostnames, pool names) may repeat — tables are
  lookups — but an *explanation* appearing twice means one copy is in the wrong file.
- **Verbatim, verified identifiers.** Name real projects, clusters, namespaces,
  hostnames, buckets, paths, and flags exactly, and verify each exists against the code
  or config before shipping. A claim that doesn't verify gets dropped or generalized,
  not shipped.
- **Enumerate small, stable inventories completely.** When a system has a small
  inventory — environments, queues, public hostnames, database roles, caches — list
  every member with its identifiers, compactly. A complete list is what lets a reader
  notice the unexpected; a partial list or an "and others" can't. But never write "only
  these exist" or "there is no other X" — absolute negative claims go stale silently and
  then mislead. Instead, let a discrepancy be a finding: a member that exists but isn't
  listed means the doc has drifted or something is genuinely unexpected, and either is
  worth flagging. This is the counterpart to provenance over precision: the *set* is
  stable and gets enumerated; each member's churny attributes still get pointers. When
  members follow a naming convention across environments, state the convention once
  (`atlas-<env>-db`) anchored by one verified real name — the convention plus one member
  enumerates the whole grid compactly.
- **Provenance over precision.** Never pin a value that churns (replica counts, machine
  types, resource limits, timings, defaults): name the file or repo that owns the
  current value, so a stale doc degrades into a correct lookup instead of a wrong
  answer. If a number is genuinely worth quoting, point at its owner in the same
  sentence.
- **Name the code owner.** Where infrastructure has a canonical governing module in the
  code — the cache wrapper, the queue publisher, the database router — name it and state
  the coupling: what the code layer enforces (key naming, TTL policy, routing,
  serialization) and that nothing should bypass it. This link is how a reader turns an
  infrastructure symptom into a code search, and it's what makes "something is bypassing
  the wrapper" a checkable claim.
- **Chain out for failure modes.** Where a fact has a known way of breaking, link the
  owning runbook by its exact title.
- **Plain language.** Short sentences, sentence-case headings, no color, no emoji.

## Maintenance

- **Change the doc in the change that changes the fact.** Moving a deployment, renaming
  a cluster, or re-routing a path updates the owning doc in the same pull request.
- **Gaps are curation input.** When the `architecture` skill (or a responder) finds a question
  these docs can't answer, that's a missing section to write, not an answer to
  improvise. Collect the gaps rather than losing them.
- **Verify sweeps.** Every reference in a corpus following this format is greppable by
  design, so staleness is detectable mechanically: re-check identifiers, paths, and
  links against the code periodically and whenever touching a file. To run one, use the
  `runbooks-author` skill's verify mode pointed at this corpus — its claim-extraction rules
  apply unchanged; only the chain-link check differs.
