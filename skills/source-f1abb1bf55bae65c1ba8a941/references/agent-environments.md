# Agent environments

The skills in this plugin run in two environments: a coding agent on your machine
(Claude Code or similar), and incident.io's hosted agents (investigations, chat). Both
provide the same capabilities, through different tools and different filesystems. This
document describes what each environment provides: where files live, which tools answer
which needs, and the search strategy every skill uses. Read it when writing a new skill
for this plugin, or when debugging why a skill behaves differently in one environment.

## The two environments

| | Your machine | incident.io hosted |
|---|---|---|
| Filesystem | Real: the working directory is your repo | Virtual and sandboxed: read-only mounts plus a writable scratch space |
| Shell | Full | Sandboxed interpreter: `cat`, `grep`, `find`, `jq`, pipelines — no host processes, no general network |
| incident.io | The MCP connection (`document_search`, `incident_show`, `log_query`, …) | Native tools with the same capabilities (names differ; see below) |
| Other providers | Whatever MCPs the session has (Notion, a wiki, …) | The organization's connected tools, where the run has them |
| Writes | Real files, real systems — confirm before writing anywhere external | The scratch space only; everything else is read-only |

## Filesystem layout

**On your machine**, content lives where your team put it. The working directory is the
repo, and content sits in its conventional locations (`runbooks/`, `docs/architecture/`,
and so on — each skill's find/answer job lists the locations it checks). Installed
plugin content lives under your client's plugin root: in Claude Code, plugins are cached
under `~/.claude/plugins/`, and the running plugin can locate its own files via
`${CLAUDE_PLUGIN_ROOT}`. incident.io's own skills can also come through the incident.io
MCP server's skill tools with no plugin installed; their files are then read through
those tools, not from disk.

**In incident.io's hosted agents**, every session gets the same workspace:

| Path | Access | Holds |
|---|---|---|
| `/plugins/<name>` | read-only | Each plugin the organization has connected, one mount per plugin |
| `/work` | writable | Scratch space — everything the agent produces goes here |
| `/investigation` | read-only | Investigation runs only: the incident and each completed check's output, as files |

Skills are loaded with the `skill <path>` command. Every load sets two environment
variables: `$SKILL_DIR` (the loaded skill's own directory) and `$PLUGIN_ROOT` (its
plugin's mount root).

**Never hardcode a root.** The same skill's files sit under a plugin cache on a laptop,
under `/plugins/<name>` when synced from a repo, and under a different mount for
first-party plugins. Reach your own files through the environment's variable
(`$PLUGIN_ROOT` hosted, `${CLAUDE_PLUGIN_ROOT}` in Claude Code). Reach other content by
searching for it, not by assuming where it is.

## Capabilities, by environment

A skill states what it needs — "search the organization's documents" — and each
environment meets that need with its own tool:

| Need | Your machine | incident.io hosted |
|---|---|---|
| Search the organization's documents | `document_search` on the incident.io MCP | The native document search tools |
| Read one document in full | `document_show` | The native document read tool |
| Incident context | `incident_show` / `incident_list` / the investigation tools | Native incident tools, plus `/investigation` as files |
| Telemetry (logs, metrics, traces) | The `telemetry` skill | Native telemetry query tools |
| Code and git history | Your workspace's own search (grep, git) | Hosted code search tools, where the run has them |
| Plugin content | The plugin cache on disk | The `/plugins/*` mounts |
| Producing output | Files in your workspace, or your reply | `/work`, and the run's result |

Two rules follow for skill text. First: name tools by their portable MCP names
("`document_search` on your incident.io MCP connection"), never by a client-prefixed
form. Second: when a capability may be absent, say what to do instead — and match the
fallback to the job. A search job skips a missing surface silently. A curation job stops
rather than fabricate. An execution job records `unknown — tried <what>`. These differ
on purpose; don't flatten them into one rule.

## The shared search strategy

Every content-finding job in this plugin (runbooks' Find, architecture's Answer)
searches the same four surfaces, in the same order:

1. **The current workspace** — the content's conventional locations. Map first, grep
   second: a well-formed corpus has a README routing table that resolves most lookups in
   one hop, so try it before searching the tree. Then grep for the literal string (the
   error message, the identifier), then for title keywords.
2. **Installed plugins** — the plugin trees available to the session (`/plugins/*`
   hosted; the plugin cache locally). Search them the same way: README index first,
   then grep.
3. **The organization through incident.io** — document search, with both phrasings: the
   literal string as keywords, the conceptual question as a semantic query. This surface
   covers documents synced from providers (Notion, Confluence, GitHub) and content from
   plugins the organization has connected — places the local filesystem can't see. Read
   candidates in full before trusting a match.
4. **Provider search tools the user points at** — a Notion search, a wiki search —
   searched with the same two phrasings.

The results from all surfaces merge under three rules:

- **Rank**: an exact title match beats a match on routing strings, which beats a body
  match. A document that owns the subject beats one that mentions it.
- **Dedupe by title**: the same document often exists on two surfaces — in a repo, and
  in the synced copy of that repo. Treat same title as same document, and prefer the
  copy that lives next to the code: it's the version most likely to be current.
- **A miss is a finding**: "nothing owns this" is a real answer. Report it with the
  nearest rejected candidates, and offer to write what's missing.

A skill that adds a surface or changes the merge should say so, and say why. The value
of one shared strategy is that you learn it once.

## What a skill must never assume

- That any surface exists. Every one is checked for, including the incident.io MCP
  itself.
- A specific mount root or plugin path. Use the environment's variables, and search.
- Network access in the hosted sandbox. The connected tools the session exposes are the
  only external reach.
- That tool names carry a client prefix. Portable names only.
- That it is running during an incident. The same skill serves an investigation, a chat
  question, and documentation work with no incident in sight.
