# Hooks across vendors

Reference for Step 3. Read this before editing anything under `hooks/`. Both
failure modes documented here are silent: the pre-commit hook never reads
`hooks/`, and an agent that never finds or runs the hook still starts. CI's
route harnesses (CONTRIBUTING.md's "Checking what each route delivers") run
each agent on every OS its CI job covers and check that the mandate reaches its
model; Cursor's runs on Linux only, until #83 is fixed;
`installer/test/session-start-hook.test.js` runs the scripts directly.

## The plugin-root variable is the trap

The hook has to read a file inside the plugin, so it needs the plugin's own
install path. Every vendor names that differently, and only some substitute
`${...}` inside a hook's `command`:

| Vendor | What the hook gets | `${...}` substituted in `command`? |
| --- | --- | --- |
| Claude Code | `CLAUDE_PLUGIN_ROOT` | yes |
| Cursor | `CURSOR_PLUGIN_ROOT`, plus `CLAUDE_PLUGIN_ROOT` as an explicit alias | yes — in `command`, `args`, `env` values and `cwd`. Not `${PLUGIN_ROOT}` |
| Copilot / VS Code | `CLAUDE_PLUGIN_ROOT`, also injected into the hook's environment | yes |
| Codex | `PLUGIN_ROOT` and `PLUGIN_DATA`, plus `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA` for compatibility | yes — those four only, and it exports them too. Any other `${...}`, like `${DROID_PLUGIN_ROOT}`, reaches the shell as written |
| Factory Droid | `DROID_PLUGIN_ROOT`, plus `CLAUDE_PLUGIN_ROOT` for compatibility | yes — `${DROID_PLUGIN_ROOT}`, `$DROID_PLUGIN_ROOT`, `${CLAUDE_PLUGIN_ROOT}` and `$CLAUDE_PLUGIN_ROOT` |
| Kimi Code | `KIMI_PLUGIN_ROOT`, and cwd is set to the plugin root | not documented |
| Agent Plugins 1.0 (root `plugin.json`) | `PLUGIN_ROOT`, `PLUGIN_DATA` | **no** — the spec restricts expansion to `args`, `env` values and `cwd`, and defines no hooks component at all |
| OpenCode | **none, and none should be added** — the plugin locates the repo's files from `import.meta.url`, in an installed copy or a clone | n/a — it never reads `hooks/hooks.json` |
| Pi | **none** — the extension locates the tarball's files from `import.meta.url` | n/a — it never reads `hooks/hooks.json` |

So a single vendor token is wrong on every other route, and forking the file per
route re-creates the problem the shared `skills/` directory exists to avoid.
`hooks/hooks.json` runs one command everywhere but Codex (see below):

```
"${CLAUDE_PLUGIN_ROOT}/hooks/session-start" "${DROID_PLUGIN_ROOT}"
```

- **It names a script, not shell syntax.** cmd.exe, which Droid uses on
  Windows, resolves the extensionless path to `hooks/session-start.cmd`;
  every POSIX shell runs `hooks/session-start`. Both read
  `session-start-context.md` from their own directory, so neither needs the
  root again.
- **`${CLAUDE_PLUGIN_ROOT}` is the path token.** Claude Code, Cursor and Copilot
  substitute it, and Droid substitutes it as a compatibility alias.
- **The second argument is how the scripts know they are on Droid.** Only Droid
  substitutes `${DROID_PLUGIN_ROOT}`; elsewhere `sh` expands an unset variable
  to `""`. Droid's own `DROID_PLUGIN_ROOT` *environment variable* can't be the
  signal: on Windows it holds the placeholder `/PLUGIN_ROOT_NOT_EXPANDED_ERROR`.
- **Cursor is told apart by its environment, and gets JSON.** Cursor sets
  `CURSOR_PLUGIN_ROOT` in every plugin hook's environment and drops a hook
  whose stdout isn't JSON as `invalid_json`, so with it set the scripts print
  `{"additional_context": "<mandate>"}`. A third argument can't be the signal:
  `${CURSOR_PLUGIN_ROOT}` would reach Droid's cmd.exe unexpanded.
- **`hooks/session-start` must stay executable and LF.** The shell runs it by
  path, so it needs its mode bit, and `.gitattributes` pins it to LF so a
  Windows checkout with `core.autocrlf` doesn't hand bash a `\r` on every line.

## The context itself must stay agent-neutral

`hooks/session-start-context.md` is one file read by every route that has a
context mechanism — Claude Code, Cursor and Factory Droid through
`hooks/hooks.json`, Codex through its fallback to that same file, OpenCode and
Pi through their own code, and Kimi through a copy `scripts/build-manifest.js`
generates. Cursor, Droid, OpenCode, Pi and Kimi name skills without the
`postman:` prefix, so each gets `` `postman:<skill>` `` rewritten to the bare
name: the two plugins in code, the hook scripts for Droid and Cursor, and the
build script for Kimi's copy. Droid's Skill tool answers
`Skill "postman:api-engineer" not found` otherwise; Cursor sends a plugin skill
to its backend by path, and invokes it as `/<skill>`. So the file must not name
one vendor's machinery: "invoke it with the Skill tool" is an
instruction Codex and OpenCode cannot follow, and it reaches them verbatim.
Name the skill and let each agent use its own loading mechanism. A vendor that
needs different wording is a reason to fix the shared text, not to fork it.

## Which shell, and which OS

Claude Code runs a hook's `command` through `sh -c` on macOS and Linux, and on
Windows through Git Bash if installed or PowerShell if not. The `shell` field is
real and takes `"bash"` or `"powershell"`; this repo sets `"bash"`, which is
what keeps Windows on Git Bash. It is ignored if `args` is ever added, since
`args` switches to exec form and spawns the binary with no shell at all.

Droid ignores `shell` on Windows and runs the command through cmd.exe, after
substituting its root tokens itself; measured on `windows-latest`, with and
without Git on PATH. A command written in shell syntax prints nothing there,
which is why the command is a bare script path.

Cursor feeds the command its payload as a shell heredoc on macOS and Linux. On
Windows it runs the command through PowerShell and resolves an extensionless
script path by trying `.ps1`, `.exe`, `.bat` and `.cmd` beside it, so it runs
`hooks/session-start.cmd`, and a `session-start.ps1` added there would win. Read
from the bundles of Cursor CLI 2026.10.01. Measured on `windows-latest`, that CLI
runs no `sessionStart` hook headless at all, user-level or plugin
([#83](https://github.com/postmanlabs/postman-plugin/issues/83)).

`hooks/session-start` must stay POSIX-safe rather than bash-specific: dash is
`/bin/sh` on Debian and Ubuntu, and Codex has no `shell` field at all.
`hooks/session-start.cmd` is its twin for cmd.exe and has to change with it;
its `postman:` rewrite and Cursor's JSON go through Windows PowerShell, told
UTF-8 both ways because 5.1 assumes ANSI and the mandate has non-ASCII text,
and started with `PSModulePath` cleared because one inherited from `pwsh`,
which Cursor prefers, points 5.1 at PowerShell 7 modules it can't load.

Codex runs a hook through the shell of the session itself: the user's login
shell on macOS and Linux, and on Windows always PowerShell, falling back to
cmd.exe (`shell_detect.rs`'s `default_user_shell`). `cmd /d /c` runs from both.
Its `commandWindows` replaces `command` on Windows, which is the only reason the
route has its own `hooks/codex-hooks.json`.

Claude Code on a Windows box with no Git Bash falls back to PowerShell, where a
quoted path is a string, not a command, so the hook prints the path instead of
the mandate. Supporting it means a third, PowerShell form of the command.

## Some routes never look for the file

Discovery is the other half, and it is not uniform either:

| Vendor | Where it looks for the hook definition |
| --- | --- |
| Claude Code | `hooks/hooks.json` by default; a manifest `hooks` key can point elsewhere |
| Cursor | manifest `hooks` (path string or inline object); falls back to `hooks/hooks.json` |
| Codex | manifest `hooks`, resolved relative to the plugin root and required to stay inside it; otherwise `hooks/hooks.json`, its `DEFAULT_HOOKS_CONFIG_FILE`. This repo's `.codex-plugin/plugin.json` names `hooks/codex-hooks.json`, because the shared command is a quoted path, and Codex runs a hook through the session's shell, PowerShell on Windows, which prints a quoted path instead of running it. Codex's own file gives Windows `commandWindows`, `cmd /d /c` on `session-start.cmd` with no argument, which runs from PowerShell and cmd.exe alike and keeps the `postman:` names Codex resolves |
| Factory Droid | `hooks/hooks.json` at the plugin root, in the same `hooks`-wrapped shape as Claude Code. It finds the scripts through Droid's `${CLAUDE_PLUGIN_ROOT}` alias and gets `${DROID_PLUGIN_ROOT}` as its argument, which is what makes the scripts strip the `postman:` prefix. A top-level event key is the shape of a user's `.factory/hooks.json`, not a plugin's |
| Copilot / VS Code | layout-dependent — `hooks/hooks.json` for the Claude layout, `com.github.copilot/hooks/hooks.json` for Agent Plugins 1.0, `hooks.json` at the root for the Copilot layout |
| Kimi Code | **nowhere.** Hooks are an inline `hooks` array in the manifest, entries shaped `event` / `matcher` / `command` / `timeout`, and Kimi documents no default file to discover. It also discards a SessionStart hook's output, so the mandate goes through the manifest's `systemPromptPath` instead |
| OpenCode | **no `hooks.json`.** Nothing session-shaped in its config schema; the plugin pushes the mandate into the system prompt from its own hooks — see item 1 below |
| Pi | **no `hooks.json`.** Its extensions subscribe to events instead; the package's extension sets the mandate as a system-prompt section on `before_agent_start` |

The Kimi Code row is what a new route inherits if Step 3 is skipped: nothing
points the vendor at `hooks/hooks.json`, so the route ships without the
session-start mandate. A vendor in that position needs an entry in its own
manifest pointing back at the shared file. A hook was not enough for Kimi, since
it discards hook output; see CONTRIBUTING.md's "The Kimi Code plugin" for the
generated copy it reads instead. Never a hand-made copy of the markdown.

## What to establish for a new vendor

1. Whether it supports hooks at all — and if not, **whether it has a
   context-injection mechanism instead**. "No hooks" is not the end of the
   enquiry; stopping there ships a route whose skills load and whose agent never
   mentions Postman. A config-only vendor usually has a rules file for this —
   OpenCode's `instructions`, an array of paths whose contents go to the model,
   is one. A package route can do it in code: the OpenCode plugin reads the
   shared markdown and pushes it into the system prompt through
   `experimental.chat.system.transform` (v1) and `session.hook('context')` (v2).
   Either is always-on context rather than a `SessionStart` event, but the
   effect on the session is the one that matters. Record a limitation only
   after finding nothing.
2. The **event name** for session start, and **what its output must be**.
   Claude spells it `SessionStart`.
   Codex spells it the same way — verified: its `HooksFile` is
   `{description?, hooks: {…}}` with PascalCase event keys
   (`#[serde(rename = "SessionStart")]`), so this repo's file fires there
   unchanged. Cursor's own event list is camelCase (`sessionStart`), but it
   converts a plugin's Claude-format file, so the shared file fires there too —
   verified with Cursor CLI 2026.10.01. Cursor is also why the output matters:
   it accepts only JSON, where Claude Code and Droid take the plain mandate.
3. Whether it discovers `hooks/hooks.json`, or the manifest has to point at it.
4. Whether the entry shape is the matcher-nested object this repo's file uses,
   or something else (Kimi's flat array, Cursor's `version`-keyed file). Also
   check which keys inside a handler the vendor actually reads, and what the
   `matcher` is matched *against*. Codex takes `matcher` plus a handler with
   `command` / `timeout` / `async` / `statusMessage`, and its session-start
   `source` enum is `startup`, `resume`, `clear`, `compact`, `fork` — so this
   repo's `"startup|clear|compact"` matches there. But it has **no `shell`
   field**, so the `"shell": "bash"` in this repo's file is silently dropped on
   that route and the command runs under whatever shell Codex picks. It survives
   only because the command is POSIX-safe; keep it that way rather than relying
   on the key being honoured.
5. Which plugin-root variable it provides, and whether it substitutes `${...}`
   in `command` or only exports environment variables. If it offers neither
   form of `CLAUDE_PLUGIN_ROOT`, its manifest points at `hooks/session-start`
   with its own root instead.
6. Whether hooks require the user to trust them before they run. Codex skips
   plugin-bundled hooks until the definition is reviewed and trusted, so "the
   hook did not fire" is not always a bug in the hook.

## Never add a root-level file named `plugin.json`

It looks like the portable thing to do and it is the single most destructive
edit available in this repo. Codex pattern-matches that filename and routes the
plugin through its Agent Plugins loader, which has no hooks component, so
`hooks` in `.codex-plugin/plugin.json` is never read and every hook in the repo
goes dead — including the ones that work today.

**The trigger is the filename.** A config-only vendor's own root file is not
affected, and neither is a package route's `package.json`, OpenCode's at the root included:
each is a different name, in neither `DISCOVERABLE_PLUGIN_MANIFEST_PATHS` nor
the Agent Plugins set, so Codex never loads it and it cannot reroute anything.
