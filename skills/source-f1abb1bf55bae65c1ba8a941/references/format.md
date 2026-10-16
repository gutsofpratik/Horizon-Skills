# Skill format

The rules a skill must follow to be found, loaded, and safely followed — in your own
plugin, and by every agent environment that loads it. Local conventions win: if the
plugin you're editing carries its own FORMAT.md or authoring conventions, follow those
where they conflict with this file.

## Anatomy

```
your-plugin/
├── README.md                  — the plugin's index: every skill, one row each
├── skills/
│   └── <dir-name>/
│       ├── SKILL.md           — frontmatter (name, description, the provenance
│       │                        stamp, optional client extras like argument-hint)
│       │                        + the instructions
│       └── references/        — detail loaded only when a job needs it
└── incident.yaml              — optional: sync settings, rarely needed
```

- **The directory name is the skill's identity.** Usage history, feedback, and any
  skill-selection settings key on it. Renaming the directory orphans its feedback and
  can silently drop the skill from an allowlist — treat a rename as a deliberate
  migration, not a tidy-up, and say so when proposing one.
- **SKILL.md is the only required file.** References are for detail a job loads on
  demand. Every reference must be reachable from SKILL.md — directly, or through the
  reference that owns its job — with each link saying when to read it. Where a job
  lives in its reference, the body doesn't repeat it: instruct the read instead
  ("read your job's file before answering, even when you think you know it"). Keep
  the tree shallow (a directory of worked examples may nest); a reference nothing
  links to is dead weight.
- **Scripts are for fragile, repeated operations** — something an agent would otherwise
  rewrite each time and sometimes get wrong. Most skills need none.
- **A repo that also installs as a coding-agent plugin** adds that client's manifest
  beside the tree (for Claude Code, `.claude-plugin/plugin.json`, and `.mcp.json` for
  bundled MCP servers). incident.io ignores these files; the skill content stays one
  tree serving both.
- Size is enforced at sync: single files up to 1 MiB, the whole tree up to 20 MiB, up to
  500 skills, and up to 500 files counting everything outside `skills/` plus the enabled
  skills' files. Symlinks and git submodules are skipped. Sync errors in the incident.io dashboard report violations, so trust those
  over this paragraph if they disagree.

## The provenance stamp

Every skill this plugin creates or edits carries the plugin's version in its
frontmatter, under `metadata` — the key the skill format reserves for extra fields, so
every client that validates frontmatter still accepts the file:

```yaml
---
name: fulfillment
description: >
  Inspect and unstick Acme's order-fulfillment pipeline. ...
metadata:
  incident-io-plugin-version: "0.19.0"
---
```

- **The value is this plugin's version.** If you loaded the skill through the
  incident.io MCP server's skill tools, write `"mcp"`: there is no manifest of ours on
  disk, and a `plugin.json` you can see belongs to the repo you're working in.
  Otherwise read it from this plugin's manifest — `plugin.json` at the plugin root —
  never typed from memory. In Claude Code the root is `${CLAUDE_PLUGIN_ROOT}`; anywhere
  else it is two directories above this skill's own folder. Quote it: unquoted, `0.19`
  is a number to YAML.
- **It means "last touched by".** Creating a skill writes it; improving a skill
  refreshes it to the current version, and a skill that never had one gains one on its
  first improve. So the estate converges with no separate sweep.
- **What it does and doesn't say.** incident.io reads the stamp at sync and shows which
  skills came through this flow, and with which version; `"mcp"` means it came through
  the MCP server's skill tools, with no version. It is a claim in a text file,
  nothing more. Whether a skill *works* is a separate fact incident.io records from
  verification runs against the skill's content — see the road test in create.md — and
  the stamp is never used to decide it.
- **Never write a stamp into a skill you didn't author or edit** in this session. The
  stamp says the flow ran; a stamp on hand-written content is a false claim.

## The description is the trigger

Agents choose skills by frontmatter alone — the body loads only after selection — and
they read your description alongside dozens of others. Optimise for activation: the
model should reach for the skill whenever its subject comes up, in any phrasing,
including ones you never predicted.

- **Lead with the subject, stated broadly.** One plain sentence for what the skill
  does, then the hook: "use whenever you're working with X in any way" activates on
  phrasings an utterance list never could — the model generalises from the subject far
  better than from a catalogue of example requests.
- **Add the few signals only this skill matches** — an error code, an alert name, a
  product term. Two or three high-precision signals beat ten paraphrases.
- **Name a moment only when it would be missed.** A skill that serves setup and serves
  growth must say both or it never fires the second time; moments the subject already
  implies don't need listing.
- **Negative scope only for a real near-miss** — one line, when agents demonstrably
  load the skill for a neighbouring job.
- **Short: two to four sentences.** Length works against you twice — it dilutes the
  subject hook, and it crowds the listing every other skill shares. A description that
  wants more is describing the body; move it there. Procedure, context, and caveats
  belong in the body anyway — a "when to use this" section there is invisible at
  selection time.

## Name what you call, never how an environment invokes it

A skill runs in more than one place: incident.io's hosted agents during investigations
and chat, and coding agents on your team's machines over MCP. Each environment binds the
same tools differently, and a skill that writes down one environment's invocation syntax
breaks in the others. The principle behind every rule here: **the skill names intent —
which tool, which datasource, which system — and the platform maps intent to the
environment's binding.** Before writing, know what connections your organization runs
(the plugin README's connections table records them), so the intent you name is one
every environment can meet.

- **Name the connection, then the bare tool.** "The incident.io connection's
  `incident_list`", then `incident_list` from there on. (Some corpora say "connector"
  — same convention, either noun; follow the corpus you're in.) The name is the stable
  identity; each environment maps it to its own binding. Resolution is the reader's, and it's
  mechanical: an agent matches the bare name against the session's available tools
  (preferring the candidate served by the named connection when there's more than
  one), and a person meets the dependency via the plugin README's connections table,
  which records where each connection comes from per environment. A bare name that
  matches nothing is the absence path, below.
- **Show arguments as data, not as a shell line:**

  ```
  incident_list(status_category: "open", page_size: 10)
  ```

- **Never write client-prefixed tool names** (`mcp__…__incident_list`) in a skill body —
  they are one client's bindings. The only place they belong is client-specific
  frontmatter such as `allowed-tools`, which other environments ignore.
- **Never write one environment's setup as instructions** — editing an `.mcp.json`,
  paths into a checkout, install commands. If a skill depends on a connection, record
  the dependency in the plugin README and let each reader meet it their own way.
- **When a tool may be absent, say what to do instead** — the absence path, below. See
  the plugin's [agent-environments doc](agent-environments.md) for the
  environment map these rules come from.
- **Name harness capabilities as intent, never as a client's tool.** Delegation,
  shell, searching, asking the user — every client exposes these differently, so write
  the need ("fan this out to a sub-agent where the session can spawn them; otherwise
  run it sequentially yourself — don't abort") rather than a client's agent types,
  model names, or slash commands. The absence path applies to these like any other
  dependency.
- **Portability rules protect skills that claim portability.** A skill that
  deliberately serves one environment — say so where the plugin records where each
  skill runs — may name that environment's tools and paths exactly; precision there is
  a feature, and "fixing" it for environments the skill never runs in breaks the one
  it has. The rules above bind the moment the skill claims both.
- **Reach the skill's own files through the environment's variable** (`$SKILL_DIR` for
  the skill's directory) rather than an absolute or repo-relative path — the same tree
  mounts at different roots per environment. Which variables exist per environment is
  the [agent-environments doc](agent-environments.md)'s table. A
  client-specific permission pin (an `allowed-tools` entry) is that client's concern:
  verify it in that client, and never let the body depend on it.

## Telemetry: the datasource is the intent

Telemetry is where implementation-pinning creeps in fastest, because each environment
may run the same query through different machinery. The stable facts a skill owns are
*where* a query belongs — the datasource — and *what* to run or ask. A telemetry tool
itself follows the normal naming rules (the connection, then the bare tool); what a
skill must never do is assume one environment's query machinery is the only route.

- **Flag the datasource whenever the query only means something against one source**:
  the data exists only there, replica-vs-primary changes the answer, retention or
  sampling differs. Where the reason isn't obvious, say it in the same breath — "the
  **production replica** datasource (Postgres) — that connects to the replica, so you
  read the replica's counters". A query any source could serve doesn't need the flag.
- **In prose**, name the datasource in bold at first mention, with its type in
  parentheses: "query the **production metrics** datasource (Prometheus)".
- **A pinned query** — one whose exact expression the skill's numbers depend on — is a
  fenced block whose first line is a comment naming the datasource in the block's own
  language:

  ```sql
  -- Datasource: order history
  SELECT count(*) FROM orders WHERE created_at > now() - interval '7 days'
  ```

  (`# Datasource: production metrics` in PromQL or LogQL.) The annotation travels with
  the query wherever it's copied.
- **An open question** is blockquoted question text, optionally naming the datasource:
  state what you want answered, not an expression. Most environments expose an
  ask-style telemetry tool that takes words and plans the query itself; the blockquote
  is its input. Where the session has no such tool, the blockquote still states the
  intent — answer it with what exists, or record the capability as missing.
- **Pin when exactness is load-bearing** (a known-good expression the skill's numbers
  depend on); prefer open questions where any correct query serves. Pinned queries are
  exact but go stale; open questions adapt but can wander.
- **Datasource constraints live next to the name** where the skill depends on them —
  retention windows, replica-vs-primary, query caps — per the provenance rule below.

## The absence path

Every dependency a skill names — a tool, a datasource, a sibling skill — needs the
"where the session doesn't have it" line, written as behavior in one sentence:

> Where the session has X, do A. Where it doesn't, <fallback> — and say so.

Three fallback classes, strongest first:

1. **An equivalent surface** — another route to the same fact, with the cost named:
   "judge from `pipeline_show`'s order ages alone" trades history for availability.
2. **The user or the dashboard** — ask, or name the page that shows it, and record
   the answer as user-reported.
3. **Abstention** — record the capability you wanted and didn't find, and fill the
   output contract honestly: the field reads "unchecked", never a guess.

Match the class to the cost of being wrong: a search job skips a missing surface
silently; a job that would fabricate without the tool stops and says so. And the
fallback is never setup instructions — connecting X is the user's job in the
dashboard, not a step the skill walks an agent through.

## Entry conditions

Some jobs can't start without knowing which thing they're about — which account, which
deployment, which batch. Where a job keys on one, requests routinely arrive without it:
"the dashboards are broken for one of our customers" names a symptom and no customer.
Write both halves:

> The job needs <identifier>. Where the request doesn't carry it, resolve it by <route
> from what the asker did provide> — or ask. Never proceed on a guess.

An agent that isn't given the identifier won't stop and ask. It will work out which one
was probably meant and carry on, and nothing in the answer will show that it guessed. So
say how to resolve the identifier, and require an inferred one to be labelled as inferred
in the output.

This and the absence path are companions: that one covers a capability the session lacks,
this one a fact the request lacks.

## Declare dependencies in the README

The plugin README owns two tables, updated in the same change as any skill (along with
the skill's own provenance stamp, above):

- **The skills table** — every skill directory, one row: name and what it does. This is
  the registry an agent reads first and the check a reviewer runs ("is the new skill
  listed?"). A skill missing from it is invisible to map-first navigation.
- **The connections table** — every connection the plugin's skills call, with where it
  comes from in each environment the team uses. A new skill that brings a new
  dependency adds the row in the same change. Where you don't know how an environment
  connects something, say so in the cell and ask — an honest gap beats an invented
  binding.

## Keep it honest

- **Verify every claim.** File paths, tool names, field names, and identifiers named in
  a skill get checked against the system they describe before shipping. A claim that
  doesn't verify is dropped or generalized to its pattern form.
- **Provenance over precision.** Don't pin values that churn — counts, limits, defaults.
  Name where the current value lives, so a stale skill degrades into a correct lookup.
  Where a skill must carry a volatile identifier, quarantine it per
  [what-works.md](what-works.md)'s one-dated-table rule rather than repeating it in
  prose.
- **Instruct the abstention.** Every job needs a written path for "the answer isn't
  here" — see [what-works.md](what-works.md)'s explicit-abstention-paths pattern for
  what that path carries.
- **One subject per skill.** A skill that serves two unrelated requests splits its
  description between them and triggers well for neither. Split it.

## incident.yaml, briefly

An optional file at the plugin root that can ignore directories at sync. Most plugins
don't need one: skills trigger from their descriptions, and that holds inside
investigations too — [triage-skills.md](triage-skills.md) covers what an automated
caller needs from a skill it reaches for mid-incident. When you do need
the file, the incident.io extensions documentation owns the schema; don't reproduce it
here.
