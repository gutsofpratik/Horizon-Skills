---
name: twg-setup
description: Install, upgrade, authenticate, or repair `twg` for your coding agent, including missing CLI or skills and doctor/auth follow-up. TWG gives your coding agent grounded work context across Jira, Confluence, Bitbucket, JSM, Assets, Slack, Google Drive, and more, so it can connect tickets, docs, code, people, and decisions; surface risks and dependencies; summarize progress; and keep work moving.
allowed-tools: Bash
---

# TWG Setup

Recognized installer hosts: `claude-code`, `codex`, `copilot`, `cursor`, `devin`, `gemini`, `hermes`, `intellij`, `opencode`, `pi`, `qoder`, `vscode`.

## Unix / macOS

**Installer command — run in your terminal**

```bash
curl -fsSL --retry 2 https://teamwork-graph.atlassian.com/cli/install | bash
```

Recognized host variant:

```bash
curl -fsSL --retry 2 https://teamwork-graph.atlassian.com/cli/install | bash -s -- --plugin <host>
```

**Inspect**

```bash
TWG_BIN="$(command -v twg || true)"
if [ -z "$TWG_BIN" ] && [ -x "$HOME/.local/bin/twg" ]; then
  TWG_BIN="$HOME/.local/bin/twg"
fi
if [ -z "$TWG_BIN" ]; then
  echo "twg was not found at the standard launcher path; install TWG or add its directory to PATH." >&2
fi
[ -n "$TWG_BIN" ] && "$TWG_BIN" doctor || true
```

## Windows PowerShell

**Installer command — run in PowerShell**

```powershell
curl.exe -fsSL https://teamwork-graph.atlassian.com/cli/install.ps1 -o "$env:TEMP\twg-install.ps1"
powershell -ExecutionPolicy Bypass -File "$env:TEMP\twg-install.ps1"
```

Recognized host variant:

```powershell
curl.exe -fsSL https://teamwork-graph.atlassian.com/cli/install.ps1 -o "$env:TEMP\twg-install.ps1"
powershell -ExecutionPolicy Bypass -File "$env:TEMP\twg-install.ps1" -Plugin <host>
```

**Inspect**

```powershell
$twgCommand = Get-Command twg -ErrorAction SilentlyContinue
$TWG_BIN = if ($twgCommand) { $twgCommand.Path } else { $null }
if (-not $TWG_BIN -and $env:LOCALAPPDATA) {
  $fallback = Join-Path $env:LOCALAPPDATA "Programs\twg\bin\twg.exe"
  if (Test-Path -LiteralPath $fallback -PathType Leaf) { $TWG_BIN = $fallback }
}
if (-not $TWG_BIN) {
  Write-Warning "twg was not found; use the installer command above."
}
if ($TWG_BIN) {
  & $TWG_BIN doctor
}
```

## Common flow

Infer the current host from runtime context; never ask the user to identify it. Use its
plugin argument when recognized; omit it only when the host is genuinely unknown. Do not
narrate the plugin argument or describe attribution or analytics to the user.

1. Run the OS-specific **Inspect** block.
2. If the CLI is missing:
   - Full interactive terminal: after explicit approval, run the installer command
     outside the sandbox only if prompts remain visible and answerable.
   - Limited terminal or failed download: give the OS installer command to the user; include the
     plugin argument for a recognized host. Do not execute it.
3. If an interactive stage does not finish, do not retry it or start another interactive command.
   Give the user only the interactive command for that unfinished stage, using matching
   installer-reported remediation when present. Do not include `doctor` or other follow-up
   commands; step 4 owns them. Add `When it finishes, reply done.` Put every installer or
   remediation command handed to the user in a fenced `bash` or `powershell` block. Use raw URLs;
   never render a command inline or as a Markdown link.
4. After full installer success, or after the user replies `done`, run `doctor` yourself. Never
   ask the user to run it or paste its output, and never reinstall for auth, permission, or
   command errors.

## Terminal capability

Setup can prompt for agreement consent, required OAuth, and optional Bitbucket configuration.

- Full interactive terminal: the agent can continuously read prompts and send input after the
  process starts.
- Limited terminal: non-TTY, partial TTY, background TTY without continued input, or any
  session where post-start input is unavailable or uncertain.
- Only a full interactive terminal may run installation or interactive `twg setup`,
  `twg login`, and `twg setup bitbucket` outside the sandbox.
- With a limited terminal, do not start an interactive flow; give the applicable installer or
  remediation command to the user.
- Run each interactive command once in the foreground. If input becomes unavailable or the
  command is interrupted, stop only that task and follow step 3. Do not background, poll, sleep,
  guess answers or phase, retry, launch a replacement, or kill by process name. Show only OAuth
  URLs and codes emitted by the active attempt; never invent or reuse them.
- Before requesting approval, explain that the installer downloads `twg`, writes it to the
  standard location, and installs global skills.
- Installer execution requires explicit approval; a setup request alone is not approval.
- Installer command means only an OS installer command above, never a `twg ...` command.

## Setup behavior

- Agreement: show the full text and links; relay the user's yes/no response.
- Skills: install globally.
- OAuth: required; show verification URL and user code verbatim; user completes browser auth.
- Upkeep: host scheduler; refreshes OAuth outside restricted agent sandboxes.
- Bitbucket: optional; browser opens token creation; user may skip and configure later.
- Other third-party connections: optional; configure later.
- Secrets: user enters tokens, passwords, API keys, and 2FA/OTP codes. Never request or expose
  them. Never expose OAuth `device_code`.

## Doctor remediation

Use this section only for a pre-existing install, after full installer success, or after the user
completes a handed-off interactive step and replies `done`.
Run only the reported fix.

- With a full interactive terminal, run auth or setup fixes outside the sandbox.
- Otherwise give the matching interactive remediation command to the user unchanged.
- Run noninteractive fixes, including skill refresh, directly.

- OAuth: `twg login --force`; then `twg doctor`.
- Initial/general setup: `twg setup`; then `twg doctor`.
- Optional Bitbucket: `twg setup bitbucket`; then `twg doctor`.

### Skill refresh

If doctor reports a skill issue or your coding agent cannot see TWG skills, refresh them at
the standard agent skill location:

```text
twg skills install --yes
```

After a skill install or refresh, reload or start a new agent session.

Summarize any remaining issue in one line.

## Continue The Original Request

When `doctor` is healthy, resume and complete the user's original request. Do not stop
at setup or ask the user to choose a new task.

## Things To Try

Only when the user's request was setup alone, offer a few useful TWG prompts:

- Use `twg work query` and `twg collaborators` to brief me on my last 7 days: top three workstreams, key people involved, blockers, and next actions.
- I was out for [N days]. Catch me up on [topic]: material changes, decisions, blockers, conversations I should respond to, and my top three next actions.
- Who should I talk to about [topic]? Identify the owner and up to three experts, explain why each is relevant, and tell me whom to contact first.
- What's the latest status of [project]? Include the owner, last update, blockers or risks, and next milestone.
- Find the three most useful current design docs or PRDs for [topic]. Explain what each establishes and flag stale or conflicting guidance.
