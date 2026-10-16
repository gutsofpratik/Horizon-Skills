# The estate

What a ready incident.io agent estate has, how to measure what exists, and where to
route what's missing. Replies follow
the `talking-to-the-user` skill. One walk, three
starting points:

- **From scratch** — nothing exists yet. Where the request doesn't say what to build,
  recommend **one triage skill for the class of incident that pages this team most
  often**: the fastest route to an agent using their knowledge in a real incident, and
  it pulls in the connections and architecture docs it needs. When a system is named
  ("the agent should know about checkout"), propose the triage skill for its commonest
  incident, writing its architecture doc on the way. Otherwise read what pages (check 7)
  before asking, and ask only when the tools are absent or the read is empty. Where a
  problem *is* stated ("investigations don't know our feature flags"),
  [choosing-a-mechanism.md](choosing-a-mechanism.md) maps it. Alternatives, for a user
  who wants them: a skill for working with a connector; architecture docs first;
  runbooks (their skills come first); an empty plugin, content to follow.

  Then walk the checks as a setup run, creating in the order the milestones section
  below gives. Whatever wasn't chosen first
  stays a standing offer once setup has landed — never a gate before it. A failed
  check is an exit:
  hand the fix to the route named beside it, then come back and continue the walk.
  Fixes that happen in the dashboard (connections, integrations) are linked, not
  waited on — continue with what exists and note the gap.
- **Existing skills, but no incident plugin** — the team already keeps skills or docs
  for their own agents. The same setup run as from scratch, with one difference: the
  existing content is material to adapt into the new plugin, not a home to take over —
  check 3 says how to tell which situation a found plugin is.
- **A working plugin, adding to it** — the user wants a new skill or doc, or advice.
  The walk is a readiness pre-check: confirm everything the new piece needs exists
  (the connections it leans on, a healthy sync, skill selection that will pick it up),
  record it, and hand over to the owning skill. Nothing is created here.

Whatever the starting point, a walk against a mature estate produces mostly "in place"
lines. That's the walk working, not failing.

## Milestones

The format, the plan-level yes and the re-show rule are in
the `talking-to-the-user` skill. This section owns the
sequence. Derive the list from the task — a narrow goal gets a short list, and
prerequisites (GitHub or GitLab access, a connection the skill leans on) appear only
when they're missing. Three points are fixed whenever content ships: it is tried out
before it is merged; for a first plugin, it is merged before the plugin is added to
incident.io ([extensions-product.md](extensions-product.md)'s syncing section says
why); and the list closes with reviewing how the skill did in real incidents and
bringing fixes back. For an existing plugin, drop the "added" line — incident.io picks
a merged skill up on its own — unless it selects skills by allowlist; then the line is
"enabled in the plugin's skill list". What the user checks in the pull request is the
`skill-authoring` skill's hand-over step.

```markdown
**Progress**
- [x] Checkout triage skill drafted
- [x] Tried out by a fresh reader and fixed
- [ ] Pull request opened ← now
- [ ] Pull request reviewed (facts checked) and merged
- [ ] Plugin added to incident.io from `acme/ops` → `agent/`
- [ ] incident.io has picked up the skill
- [ ] Issues from real incidents reviewed in the dashboard and fixed here
```

## What ready looks like

Two tiers, and the difference matters. **Hard requirements** are what the platform
needs before anything can work — hold these. Everything else is a **recommendation**
that produces better results — explain why, then respect the user's choice.

Required:

- A source-control integration (GitHub or GitLab) incident.io can read the plugin's
  repository through — without it, nothing syncs
- A plugin registered and syncing cleanly, with the skills the team intends enabled

Recommended:

- The connections the team's skills lean on, healthy — nothing awaiting
  re-authentication. (Required in one case: a skill that reads through a connection
  can't work without it, so a narrow goal inherits the connections it needs.)
- Architecture docs and runbooks somewhere agents can find them
- Skills in the plugin that earn their place in real incidents

When several pieces are missing, fix in that order: source control gates plugin
registration, and connections bound what any skill can do, so both come before content
that leans on them. Every creation is proposed and confirmed before it's made, per the
skill's ground rules.

Match the walk's depth to the user's intent. Some users want the detailed setup;
others have one narrow use case in mind ("I just want a triage skill for checkout
failures"). For a narrow intent, hold the requirements that goal actually needs,
recommend the rest in a line each, and proceed — a recommendation declined is a report
line, never a blocker.

## 1. What can this session reach?

Feature-test, don't assume. Absence changes the route, not the goal — note presence or
absence without comment:

- **The incident.io connection** — try a cheap read (`extension_plugin_list`). Without
  it, every measurement below comes from the user and the dashboard; say so and carry
  on.
- **The extension tools** on that connection — some surfaces expose a subset of
  `extension_plugin_list` / `extension_plugin_create` / `extension_plugin_sync` /
  `extension_plugin_update`.
- **A filesystem and repository** — is the session in a checkout the team can land
  changes from?

Where the session can reach the plugin's repository, check it for a previous estate
report (a dated file, or the registering pull request) — it carries what earlier runs
considered and declined, so this run doesn't re-litigate it.

## Configuration

### 2. Source control

**Ready:** a GitHub or GitLab integration connected, covering the repository the plugin
lives (or will live) in.

**Measure:** no extension surface reports this — ask the user, or have them confirm on
the dashboard's integrations page, and record it as user-confirmed.

**Missing:** link the user to the dashboard's integrations page. Nothing plugin-shaped
can be registered until this exists.

### 3. The plugin

**Ready:** a plugin registered against the team's repository, last sync completed, and
skill selection covering what the team intends (automatic mode, or an allowlist that
includes the skills they expect agents to load).

**Measure:** `extension_plugin_list` — each plugin's name, sync state, and skills.
Without the tool, ask the user to read the dashboard's Extensions page.

**Missing or broken:**

- No plugin → [scaffold.md](scaffold.md) creates and registers one — for a first
  skill, after it is merged (the milestones section above).
  Never create a second plugin beside a working one without the user asking.
- A sync error → the repository is unreachable or the tree malformed; scaffold.md's
  verify step covers diagnosing it. A `plugin_directory_missing` error means the plugin
  moved: move it (extensions-product.md's syncing section), never add it again.
- Selection excluding an expected skill → `extension_plugin_update` (or the dashboard)
  enables it; confirm which skills before changing selection, since it's set
  whole-state.
- No `AGENTS.md` (or `CLAUDE.md`) at the plugin root telling agents to load the
  `extensions` skill before editing here → offer to add one
  ([scaffold.md](scaffold.md)'s tree section has the instruction and the harness
  naming rule).

**A plugin found on disk:** when the session's checkout holds a plugin (a
`.claude-plugin/` manifest, or a `skills/` tree of `SKILL.md` files), classify it
before working in it:

- **It's the registered plugin** — its repository and subpath match an entry in
  `extension_plugin_list`. This is the estate's plugin: new skills go in it.
- **It's not registered** — a plugin the team keeps for other tooling. Don't take it
  over: registering an existing plugin wholesale ships every skill in it to
  incident.io's agents, and content written for other callers may not fit. Create the
  incident plugin fresh ([scaffold.md](scaffold.md)) and treat the found plugin's
  skills and docs as material — adapt what earns its place through the
  `skill-authoring` skill, rather than syncing it as-is.

### 4. Connections

**Ready:** the connectors the team's skills lean on, connected and healthy —
`connection_status` good, no `reconnection_reason` set. Telemetry data sources are
not part of this walk: their health is the `doctor` skill's.

**Measure:**

1. `extension_connector_list` — each connector with its type, enabled state,
   capabilities, health, and `tool_access`: every tool with its class and its rule
   for chat, MCP clients and investigations. Read that for what investigations can
   call; `tools` is only what this session can call from an MCP client.
   `tools_unlisted: true` means callable but not named — say "tools unlisted", never
   "no tools".
2. Without the tool, ask the user to read the Connectors tab of the dashboard's
   Extensions page and record what they report.

Record when each connection was made where a surface or the user can say — a young
connection changes how its data reads in check 7.

**Missing or broken:** connections are created and re-authenticated in the dashboard,
never from a session. Case by case:

- Missing → link the user to the dashboard's Extensions page, note the gap, and
  continue with what exists.
- Needing re-authentication → a finding for the report.
- Disabled → a status line, not a gap, unless evidence lives behind it.
- Exists but lacks the auth type or tools a stated goal needs → a blocker to surface
  now, before any authoring starts — not something to discover after a skill is
  written against it.

## Content

### 5. Architecture docs and runbooks

**Ready:** a corpus of each exists somewhere agents can find it — the repository, a
plugin, or a connected provider like Notion or Confluence.

**Measure:** use the search jobs of the `runbooks` and `architecture` skills rather
than re-deriving them — a quick probe of each skill's find/answer surface is enough to
say "a corpus exists at <where>" or "none found". Where those skills aren't loadable,
ask the user where theirs live and record the answer as user-reported.

**Missing:** neither corpus is a gate on setup.

- Architecture docs are written just-in-time: creating a skill captures the docs that
  skill needs through the `architecture-author` skill; a general corpus can
  follow — during setup where the user wants it.
- Runbooks are most valuable once there's incident history to curate from (the
  `runbooks-author` skill's curate job mines closed incidents); a team with an
  already-practised procedure can write one any time — writing the skill it leans
  on first.

### 6. Skills

**Ready:** the plugin holds skills that earn their place in real incidents — including,
where the team wants custom triage, skills that describe themselves as such.

**Measure:** the skill list from `extension_plugin_list`, read against what actually
pages (check 7). An empty or thin skills list on a young estate is normal, not a gap.

**Missing:** writing a skill is the `skill-authoring` skill's create job, and mapping a
problem to the right mechanism first is
[choosing-a-mechanism.md](choosing-a-mechanism.md). Propose, don't push: the paging
read says where a skill would earn its keep, and the user decides what's worth writing.

### 7. What actually pages

Read this only when the question is what to build — it answers which incident class
pages this team most. Skip it when only checking configuration. Two cheap reads, where
the session has them:

- `alert_stats(group_by: ["source"], sort_groups_by: "workload", created_after: "<~90
  days ago>")` — which alert sources generate the most on-call work, in workload
  minutes, not just counts.
- `incident_stats(group_by: ["type"], sort_groups_by: "workload", created_after: "<~90
  days ago>")` — where incident time goes; grouping by `team` answers the same question
  per team.

A source connected more recently than the window ranks on partial data — say so rather
than reporting it as the top source. A young organization with little history is
normal: record the volumes and move on. Without the tools, ask the user; their answer is
as good a goal.

## The estate report

Fill in the block below at the end of the walk — every line either sourced from a tool,
confirmed by the user, or an honest `unknown — <how to find out>` — and keep it in the
plugin's repository, as a dated file or the pull request description, so the next run
sees what was already considered. On a setup run, add what was created and what happens
next: when agents will see the skills, where feedback will accumulate, and the standing
offers — a general architecture corpus, and runbooks once there are incidents to learn
from. Don't show the block to the user: they hear what's in place, what's missing for
their goal, and the next step, with the full report offered.

```markdown
# Estate report — <date>

- **Session:** <incident.io connection? extension tools? repo checkout?>
- **Source control:** <GitHub/GitLab integration state, user-confirmed | unknown>
- **Plugin:** <name — sync state — skill count | none>
- **Connections:** <name — type — status — capabilities — connected since, one line each | none beyond incident.io>
- **Content:** <runbooks corpus at <where> | none found; architecture docs likewise>
- **Paging:** <top sources/types by workload over the window | little history | skipped>
- **Gaps:** <each missing or broken piece, with the route that fixes it | none>
```
