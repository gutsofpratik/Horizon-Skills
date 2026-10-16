---
name: vscode-extension-builder
description: Build, run, and smoke-test the vscode-extension-builder generator — scaffold a VS Code extension (command/theme/snippets type), compile it, package it with vsce, and install it into VS Code. Use when asked to run this generator, verify it still works, test the scaffolder, or smoke-test the extension-builder skill end to end.
---

This repo is itself a Claude Code skill (`vscode-extension-builder`) that
scaffolds, compiles, packages, and installs VS Code extensions on behalf of a
user. There's no server or GUI of its own to launch — "running" it means
driving its generator script and the downstream npm/vsce/code pipeline it
tells an agent to run. Drive it via
`.claude/skills/vscode-extension-builder/driver.mjs`, which exercises
that entire pipeline for a throwaway extension and reports pass/fail per
stage.

## Prerequisites

Node.js, npm, and (optionally) the VS Code `code` CLI on PATH. Verified
versions in this container:

```bash
node --version   # → v24.16.0
npm --version    # → 9.8.0
code --version   # → 1.121.0 (optional — driver skips install stages without it)
```

`vsce` is not a prerequisite to install — it's invoked via `npx --yes
@vscode/vsce`, same as the real skill does, so nothing is installed globally.

## Setup / Build

None. There's no root `package.json` to install for this repo itself — the
only "build" step happens per-generated-extension, which the driver handles.

## Run (agent path)

```bash
node ".claude/skills/vscode-extension-builder/driver.mjs" --type command
```

This scaffolds a throwaway extension named `smoke-command-<timestamp>` into a
fresh OS temp directory, then runs: scaffold → `npm install` → `npm run
compile` → `npx @vscode/vsce package`, checking a concrete artifact after
each stage (package.json exists, `out/extension.js` exists, a `.vsix` was
produced). It prints `PASS`/`FAIL` per stage and deletes the temp directory
afterward (pass `--keep` to leave it on disk for inspection). Exit code is
non-zero if any stage failed.

```
=== scaffold (create-extension.js) ===
PASS: scaffold (create-extension.js)
=== npm install ===
PASS: npm install
=== npm run compile ===
PASS: npm run compile
=== vsce package ===
PASS: vsce package
=== vsix produced ===
PASS: vsix produced
```

Other extension types (no compile/package step — just confirm the
type-specific asset was generated):

```bash
node ".claude/skills/vscode-extension-builder/driver.mjs" --type theme
node ".claude/skills/vscode-extension-builder/driver.mjs" --type snippets
```

To also exercise the real `code --install-extension` step (installs into
*this machine's* actual VS Code, then cleans up after itself):

```bash
node ".claude/skills/vscode-extension-builder/driver.mjs" --type command --install --uninstall-after
```

| flag | effect |
|---|---|
| `--type command\|theme\|snippets` | which scaffold type to drive (default `command`) |
| `--keep` | don't delete the temp output dir afterward; path is printed |
| `--install` | also run `code --install-extension` on the packaged `.vsix` (command type only, requires `code` on PATH) |
| `--uninstall-after` | with `--install`, uninstall the smoke extension afterward so it doesn't linger in the real VS Code |

## Run (human path)

Same thing the actual skill (`skills/vscode-extension-builder/SKILL.md`) tells
an agent to do for a real user request — not something a human runs directly
for verification. To reproduce by hand:

```bash
node "skills/vscode-extension-builder/scripts/create-extension.js" \
  --name my-ext --displayName "My Ext" --description "..." \
  --publisher local-dev --type command --dir /path/to/my-ext
cd /path/to/my-ext
npm install
npm run compile
npx --yes @vscode/vsce package --allow-missing-repository
code --install-extension my-ext-0.0.1.vsix
```

## Test

There's no separate unit test suite — the driver above *is* the test: it
fails loudly (non-zero exit, `FAIL` line) at whichever stage broke.

---

## Gotchas

- **`spawnSync(..., { shell: true })` on Windows mis-tokenizes paths with
  spaces.** This repo lives under a path containing spaces
  (`AI Skills\vscode-extension-generator`). Running `node <script>` through
  `cmd.exe` (`shell: true`) silently splits the path at the space and fails
  with `Cannot find module 'C:\Users\Surya'`. Fix: only pass `shell: true`
  for `npm`/`npx`/`code` (which need it to resolve their `.cmd` shims on
  Windows) — call `node` directly without a shell.
- **`os.fsRealpathSync` doesn't exist** (that's a `fs` function, not `os`).
  Use `fs.realpathSync(os.tmpdir())` when resolving a temp dir before
  `mkdtempSync`.
- **The generator refuses a non-empty output dir.**
  `create-extension.js` exits with an error if `--dir` already exists and has
  files in it — always scaffold into a fresh directory (the driver uses
  `fs.mkdtempSync` for this).
