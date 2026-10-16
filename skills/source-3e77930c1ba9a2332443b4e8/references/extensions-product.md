# The extensions product

Extensions are how an organization gives incident.io's agents its own tools and
instructions: the internal systems incident.io has no way to reach, and the procedures a
team wants followed rather than rediscovered. Both get used at the right moment in the
same investigation as everything else — skills alongside native telemetry, connector
calls alongside native integrations.

The human-facing documentation lives at
<https://docs.incident.io/nexus/extensions/overview> — point users there for
anything they want to read themselves. Everything is configured from the dashboard's
Extensions page (`https://app.incident.io/~/nexus/extensions`).

## Two ways to extend

- **Plugins are content agents read.** A plugin is a directory of skills in one of the
  organization's repositories. A skill is a `SKILL.md` file explaining how to do
  something in their environment. Agents load a skill when it matches the work in front
  of them, then follow it.
- **Connectors are systems agents call.** A connector is a remote MCP server or an HTTP
  API (described by an OpenAPI spec) the organization has connected, exposing tools an
  agent can use to query something incident.io has no native integration for.

The rule for choosing between them: content the organization wants agents to **follow**
is a plugin; a system it wants agents to **query** is a connector. Most teams end up
with both — a skill is the procedure, a connector is what carries it out.

### Built on open standards

Skills, plugins, and connectors are open formats (agent skills, the Claude Code
plugin format, MCP), so a plugin written for incident.io also loads in the team's own
coding agents. The guarantee runs one way: nothing in the format prevents a plugin's
skills being used locally, but a skill written for local tooling isn't automatically
suitable for incident.io's agents.

## Where extensions get used

- **In investigations.** Skills load when they fit what the investigation is trying to
  understand, and skills that describe themselves as triage run at the start (see
  below). Connector tools are called the way any other source is queried, and what
  comes back becomes evidence in a finding.
- **In the agent.** `@incident` in an incident channel or the dashboard reaches the same
  skills and connectors, so a question in a channel can draw on them too. Extensions
  don't require investigations to be useful.

## Plugins

Skills are the standard format — directories under `skills/`, each holding a `SKILL.md`
with frontmatter, plus any reference files alongside. Two things specific to
incident.io: selection matches the frontmatter description against the work at hand,
and that's the only thing read before deciding whether to load a skill; and only skills
are read — anything else the plugin contains (commands, agent definitions for the
team's own tooling) is synced but ignored.

Skills a team already keeps for its coding agents (a `.claude/skills` folder, a
marketplace repo) use the same format and would load, but every skill added goes live
for incident.io's agents in real incidents. Ones written for development — writing
migrations, reviewing pull requests — don't help there and pull selection off course.
Don't recommend adding such a folder as it is: recommend a separate incident plugin
that adapts what's useful, or adding it with hand-picked skills only, and say why.

A plugin is a logistical unit, not a runtime concept: which plugin or repository a
skill lives in has no effect on whether it's selected. The description does all the
selecting, so semantic scoping belongs there — "describes Sentry errors for mobile
apps; not for other contexts" — never in a plugin or repo name.

### What a skill can draw on

A skill isn't limited to what's written in it: the agent following one has everything
the run can reach — the organization's telemetry, its allowlisted connector tools, its
connected code and documentation, and the investigation's work so far. That's why good
skills name the need, not the tool; the `skill-authoring` skill owns the craft of
writing skills that get selected and followed.

### Syncing

Plugins sync from a GitHub or GitLab repository the organization has connected for
code. incident.io scans for a `.claude-plugin/plugin.json` or a `skills/` directory
containing at least one `SKILL.md` — at the repository root or under a subpath.

- Skills are read-only to incident.io: it never writes to the repository, and an
  investigation can't change a skill based on what it learns.
- Plugins re-sync on a schedule, and can be synced on demand. A sync reads the
  repository's default branch, so a skill still on a branch isn't there to pick up.
  Each sync records the commit it read, so it's always possible to tell which version
  of a skill an investigation followed.
- Skill selection is either automatic (every skill in the current version, including
  newly-synced ones) or an explicit allowlist — under an allowlist, a skill merged
  later stays off until someone enables it, so a merge can't quietly change agent
  behaviour.
- A sync or a move only starts one: the call returns `pending`. Read
  `extension_plugin_list` again until the plugin shows `synced` or `error` (usually
  seconds) and report that — a reply that stops at "pending" leaves the user to check.
  A `sync_error` shown while `pending` is the previous attempt's.
- A plugin whose directory or repository moved fails to sync with
  `plugin_directory_missing` (or `repository_unavailable` after a rename). Move the
  plugin to the new location (`extension_plugin_update` with the new repository or
  subpath) — never remove and add it again, which throws away its usage history and
  skill selection.

### Triage skills

A skill that describes itself as being for triage — owning a system's or an incident
class's opening procedure — is identified by Investigations and executed at the start
of the investigation, alongside the initial searches, so its findings are in hand when
the first hypothesis is formed. This is how teams get custom triage: encode where an
investigation of a given kind should look first, and first hypotheses come back faster
and more accurate. Nothing else marks a skill as a triage skill — the name and
description are the whole signal. The `skill-authoring` skill carries a dedicated
reference on writing them.

### Triggers: running a skill at a fixed moment

When a skill must run every time, not when its description happens to match, it's a
trigger, declared in `incident.yaml` at the plugin root:

```yaml
investigations:
  - id: deploy-log-first
    when: initial_searches       # or investigation_start
    skill: deploy-log            # a skill dir in this plugin
    blocks: false                # true makes the first hypothesis wait for it
    frequency: every             # or once
```

- Only two moments fire today: `investigation_start` and `initial_searches`. Others the
  docs mention (`on_hypothesis`, `before_conclusion`, `on_question`) and `if:` aren't
  built — a trigger using one is **dropped at sync without an error**, and so is any
  malformed entry. A sync that succeeds says nothing about the file.
- A trigger fires only while its skill is enabled in the plugin's selection.
- No tool lists triggers or reports dropped ones, and `incident.yaml` isn't readable
  through the incident.io connection: check the file in the repository yourself against
  these rules.
- `ignore:` in the same file keeps paths (evals, scratch notes) out of the sync. A
  leading `/` anchors a pattern at the plugin root; `.gitignore` doesn't apply.

### Usage is recorded and assessed

Every skill load is recorded, and after the run is scored a retrospective assessment
judges it: was the skill followed, did following it help, and what specifically held it
back. Observations are deduplicated into issues anchored to the file and quote they're
about. This feedback is the raw material for improving skills — the `skill-authoring`
skill's improve job consumes it — and it also catches skills reaching for tools that
aren't connected.

## Connectors

A connector is a remote MCP or HTTP server. On connection its tools are discovered — 
names, descriptions, arguments — and agents pick, call, and read them from that. Facts
an agent advising on connectors should know:

- **Prefer native integrations.** When incident.io supports something as a telemetry
  data source, connect it there, not through its MCP server — the telemetry system
  speaks each product's query language and learns the shape of the data, which a
  generic tool call can't match. Connectors are for systems with no native integration.
- **Every tool has a class, and the class decides where it can run.** `read` (the server
  marks it read-only, or an HTTP `GET`), `write` (it changes something but says it
  destroys nothing, or an HTTP `POST`), `destructive` (`PUT`, `DELETE`, or a change the
  server doesn't rule destructive), and `unknown` — an MCP tool whose server declared no
  hints at all. Each tool is switched on or off, and each class has a rule per surface:
  chat, MCP clients, and investigations (allow, deny, or only named people or teams).
  Investigations run unattended: they never call write or destructive tools, and
  `unknown` tools are off for them by default — so a connector whose server sends no
  hints is invisible to investigations until someone allows unknown tools for them.
- **Read access from `extension_connector_list`'s `tool_access`**, which lists every
  tool, switched-off ones included, with its class and rule on each surface. Its
  `tools` field is narrower: only what *this session* can call from an MCP client. It
  says nothing about investigations, and a tool missing from it may still exist.
- **Why a tool wasn't called**, in order: is the connector healthy
  (`connection_status`, `reconnection_reason`); is the tool on; is its class allowed on
  that surface; does any skill tell agents when to reach for it. Name the first that
  fails.
- **Private networks.** A server reachable only inside the organization's network is
  reached through the connector proxy: a small service the organization runs inside
  its network, set up in Settings → Connectors (the same word for a different thing),
  then picked under Network access when adding the connector. Plain `http://` works
  only through the proxy. Never suggest exposing the server publicly.
- **Failure is non-fatal.** An unreachable server or a missing tool doesn't stop a run;
  the investigation carries on with what it has, and connection problems surface on the
  connector's dashboard page.

Connectors are created and configured only in the dashboard — endpoint, auth (bearer
token or OAuth), which tools are on, and who may call them where. There is no session
tool for any of it, and connector access is read-only from here: link the user to the
connector's page under Extensions. Pair every connector with a skill that says when to
use it and what its results mean — the connector is the ability to call something, the
skill is why you'd want to.

## What a session can do

Where the session has the incident.io connection, extensions are operated through the
tools prefixed `extension_`. List what the session actually exposes rather than
trusting any written snapshot — surfaces differ, some expose a subset, and the set
changes. The names say the job: they cover plugin registration and syncing, connector
and skill inventories, usage and feedback reads, and verifying proposed content before
it lands.

Creating or changing connectors and removing plugins stay in the dashboard.
