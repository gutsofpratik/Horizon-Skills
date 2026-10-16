# Scaffold and register the plugin

Create the plugin tree in the team's repository and register it with incident.io.
Check-first throughout: on a re-run, most of this file is verification.

## 1. Does a plugin already exist?

`extension_plugin_list` (or the dashboard's Extensions page). If the team already has
a plugin, everything below reduces to: put new skills in it, fix anything the estate
walk flagged (sync errors), and re-sync. Never create a second plugin beside a
working one without the user asking for it.

Registration needn't come first. For a first-time setup it comes after the first skill
is drafted, tried out and merged to the default branch — [estate.md](estate.md)'s
milestones section has the order and why. The steps below land it once that's done. A
user who wants the plugin set up empty, with content to follow, gets exactly that —
register the scaffold, with the `.claude-plugin/plugin.json` manifest so it can be found.
Tell them its syncs fail until the first skill merges: a sync needs at least one skill.

## 2. Resolve the home

Where the plugin lives is the team's call — present the options rather than assuming
how they keep their content, in the same order as every write in this plugin's skills:

1. **An existing repository** the team already keeps operational content in — the
   default where one exists. The plugin can live at the root or under a subpath
   (`plugins/ops/`, `agent/`), which keeps it comfortable inside an existing repo.
2. **A repository the user names.**
3. **A new repository** — propose one only when neither of the above exists.

A plugin already on disk that isn't registered with incident.io is not the home —
create the incident plugin fresh and adapt its content ([estate.md](estate.md)'s
check 3 has the classification).

How many plugins, and cut along what line, is the team's call — a plugin is a
logistical unit, so the choice affects governance, not selection. Start with one
plugin for everything by default.

Confirm the choice before writing anything: name the repository, the subpath, and
what will be created.

## 3. The tree

The minimum that syncs and serves:

```
<subpath>/
├── README.md            — the skills table and the connections table
├── AGENTS.md            — tells agents to load the extensions skill before editing here
└── skills/
    └── <first-skill>/
        └── SKILL.md
```

AGENTS.md needs one instruction from incident.io's side — load the `extensions` skill
before working on the plugin — so any agent editing the tree later picks up the
conventions and the estate context first:

```markdown
Load the incident.io `extensions` skill before doing anything in this directory —
including editing or writing skills. This is an incident.io plugin: the skills here
sync to incident.io and are followed by its agents in real incidents.
```

The rest of the file is the team's — anything else they want agents to know can live
alongside. Name the file for the harness the team uses — `AGENTS.md` for harnesses
that read the open convention, `CLAUDE.md` for Claude Code; where the team runs
several, keep one as the file and the other as a one-line pointer to it.

The tree can also carry `architecture/` and `runbooks/` directories alongside
`skills/` — the plugin's repository is the conventional home for those corpora too.
The `architecture` and `runbooks` skills own their formats and content: create the
directories only when the setup run is creating that content, and let those skills
say what goes in them.

The structural rules — directory names as identity, descriptions as triggers,
environment-neutral tool naming, what goes in the README's two tables — are the
`skill-authoring` skill's format reference.
Hold the scaffold to it from the first file: retrofitting conventions is how registries
drift. The skills themselves are drafted through `skill-authoring`'s create job.

## 4. Register

The repository must be reachable through the organization's connected GitHub or
GitLab integration — the estate walk's source-control check
([estate.md](estate.md), check 2) has this state; if it's unknown or missing, ask, and
link the user to the dashboard's integrations page before registering. (Reachability isn't checked at registration — an unreachable
repository surfaces as a `sync_error` in step 5, so a wrong guess here is caught,
just slowly.)

Confirm before calling: name the repository, the subpath, and every skill directory
that will go live — registration enables every skill under the subpath at once, so
pre-existing skills ship to the organization's agents in the same moment. Then, where
the session has the tool:

```
extension_plugin_create(provider: "github", repo_owner: "<owner>",
                        repo_name: "<repo>", subpath: "<subpath, omit for root>",
                        name: "<mount name>")
```

Set `name` deliberately. It defaults to the plugin directory or the repository name, so
two repositories that both keep their plugin at a conventional subpath — `ops/`,
`agent/` — ask for the same mount name. The mount is what agents see, so choose one that
stays distinct across the whole estate rather than relying on the default.

The first sync starts immediately, asynchronously. Without the tool, the dashboard's
Extensions page has the same add flow — walk the user through it with the values
above.

## 5. Verify the sync landed

Don't declare success on registration. Check `extension_plugin_list` a few moments
later: a healthy plugin shows a completed sync and the skills you scaffolded; an
inaccessible repository or malformed tree shows up in `sync_error`. Report either
outcome plainly. After later pushes, plugins re-sync on a schedule;
`extension_plugin_sync(plugin: "<name or id>")` pulls the change now instead.

If the plugin's skills are selected by an allowlist rather than automatically (a
dashboard setting), a new skill also needs enabling there — say so rather than
assuming pickup.

## 6. Return to the walk

Scaffolding is usually one exit from the estate walk. Return to
[estate.md](estate.md), continue any remaining checks, and record what was created in
its estate report — that section owns the report's shape and where it's kept.
