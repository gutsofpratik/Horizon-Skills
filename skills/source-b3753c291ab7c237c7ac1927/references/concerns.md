# The concern catalog

The recurring operational concerns of a system, and the questions each concern file
answers. Use this when writing (or reviewing) a system's docs: the catalog says what a
file of each kind is *for*, and the worked example in [examples/](examples/README.md)
shows the calibrated depth — match it.

This is a menu, not a checklist. A system's README covers every concern in a line or two
until one has enough to say for its own file (under ~30 lines it stays a README
section). Most small systems never split at all; a primary system typically ends up with
three to six concern files. Environments and APIs-and-routing usually span systems; when
they do, they're views (root files — see [format.md](format.md)), as in the worked
example.

## The depth rule

Every concern file strikes the same balance: enough to orient a responder or an agent
and route them onward — never a manual. The test for each fact: does it help someone
align on what this thing is and find the deeper source? Concretely:

- Open with the operational shape in a paragraph: the whole story, compressed.
- Name the authoritative home for depth in the first few lines ("authoritative detail
  lives in X — this file is the operational shape"), and delegate to it rather than
  rewriting it. When a deeper doc exists, this file carries the key facts and a link.
- Name identifiers verbatim — they're what greps, searches, and agents key on.
- Teach how to *read* situations ("a deploy that fails when auto-sync is off is the
  paused-deploys signal"), name levers without walking them, and chain failure modes to
  the owning runbook by exact title.

## The concerns

**Deployment** — how a merged change becomes running production code. What builds, what
gates what, in what order; how staging participates; how migrations are sequenced; how
to roll back and hotfix (levers, named); how to read a slow, stuck, or paused deploy;
where deploys are visible (annotations, change events, a deploy log).

**Environments** — what environments exist and what each is for. When the count is
sensible (under ~10), list all of them — no sampling — each with its compact identifier
chain: the environment's name, the account or project it lives in, the cluster it runs
on, the namespace or service names within it (e.g. "staging, in the `acme-staging` GCP
project, on the `staging` Kubernetes cluster, under the `app` namespace"). Precise
compact identifiers here are the single highest-value content in the corpus: they're
what every search, query, and console session keys on. Then: what differs between
staging and production (data, scale, alerting); how to tell which environment you're
looking at; where authoritative infrastructure config lives.

**Runtime** — what actually runs: clusters, services/deployments, worker pools, cron;
which workloads are user-facing vs background; scaling shape (what autoscales, what is
pinned — pointing at the config that owns the numbers); where to see what's running now.

**Database** — engine and hosting, with real instance names. When a system has several
databases per environment, list each one and what it holds — and state the naming
convention across environments explicitly (`atlas-<env>-db`), so an identifier seen in
one environment derives its counterparts. Then: how the application connects (pools,
poolers, roles); replicas and what routes to them; partitioning or sharding shape; how
migrations run and where they live; backup/restore shape (lever, named). The failure
modes (lock contention, replication lag) chain to runbooks.

**Caching and shared state** — each cache or shared store that exists and what it's
*for* (one line each — the "what breaks if this vanishes" framing); the canonical module
in code that governs each one and what it enforces (key naming, TTLs, serialization —
and that nothing bypasses it); TTLs and eviction only where load-bearing; what is
deliberately not cached. The code↔infrastructure coupling applies to every
infrastructure concern (the queue publisher, the database router, the storage client),
not just caches — name the governing module wherever one exists.

**Events and messaging** — how asynchronous work moves: queues/topics/streams with real
names; ordering and delivery guarantees that shape incident behavior (at-least-once,
DLQs); how backlogs surface and where they're visible; what re-queues on deploy or
restart.

**APIs and routing** — every public hostname, each with what serves it and where TLS
terminates; internal vs public API split; rate limiting and auth at the edge (named, not
specified). Then two anchors: **walk one representative request end-to-end** (DNS → load
balancer → service → what handles it) so the whole path exists once as a concrete story;
and **list the deliberately unauthenticated paths** (webhooks, health checks, public
pages) — during an incident, "is this endpoint supposed to answer without auth?" needs a
lookup, and an unauthenticated path that isn't listed is a finding to flag, not proof of
compromise.

**Observability** — where logs, metrics, traces, and errors go, with datasource names
exactly as queries and tools reference them. Then three things that earn their space:
a **correlation keys table** — the identifying fields that join telemetry together
(request ID, trace ID, build SHA, environment, tenant ID), with a column for which of
logs / metrics / traces / deploy events each field appears in, because that join map is
how anyone pivots between signals; **where alert definitions live in code** (the
code-owner rule applied to alerting — monitors-as-Terraform, alert rule files); and the
two or three **dashboards that matter, by exact name or slug**.

This file owns the producer side only. When the tooling itself has enough to say —
vendor account layout, an error-tag vocabulary, which severities page — that's an
estate service directory (see [format.md](format.md)), not more lines here: this file
keeps where *this* system's signals go and links the estate service for the tools
themselves.

## What a concern file never holds

Diagnosis steps (a runbook), current values that churn (point at the owning config),
vendor product documentation (link it), and another system's facts (its own directory).
