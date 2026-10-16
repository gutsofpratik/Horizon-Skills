---
name: release-installer
description: Release @postman/postman-plugin, the npx installer and Pi package, to npm - a release candidate on the `next` dist-tag or a plain version on `latest`. Use when asked to cut, publish, tag or ship an installer release or rc, promote an rc to latest, resume a release in progress, or retry one that failed.
argument-hint: rc | latest | <version>
disable-model-invocation: true
allowed-tools: Bash(node .claude/skills/release-installer/scripts/release.mjs:*), Bash(git fetch:*), Bash(git status:*), Bash(git ls-remote:*), Bash(git show:*), Bash(git worktree list:*), Bash(git worktree add:*), Bash(npm ci:*), Bash(npm test:*), Bash(npm audit:*), Bash(npm pack:*), Bash(npm run test:pi-harness:*), Bash(gh run list:*), Bash(gh run view:*), Bash(git push -u origin release/*), Bash(gh pr create:*), Bash(gh pr view:*)
---

# Release @postman/postman-plugin

Release to cut: **$ARGUMENTS** (`rc`, `latest`, or an exact version; if empty, ask which).

Pushing the tag `@postman/postman-plugin@<version>` is the release. `release.yml`
checks the tag, runs the tests, publishes to npm with trusted publishing and
provenance, and creates the GitHub release page. The version picks the dist-tag:
a plain version goes to `latest`, `-rc.N` to `next`.

The helper below does the mechanical parts. Run it from the root of the
checkout you release from:

```bash
node .claude/skills/release-installer/scripts/release.mjs <command>
```

Below, `release.mjs <command>` means that line.

## Rules

- **Publish only by pushing the tag.** Never run `npm publish` yourself, not even
  with `--registry` aimed at a local registry. An `~/.npmrc` that scopes
  `@postman` to npmjs.org outranks `--registry` and publishes to real npm with
  your token.
- **Ask the user before you push a tag.** Say the version and the dist-tag, and
  push only on a yes. npm versions are immutable. `allowed-tools` leaves `git push`
  and `git tag` out on purpose, so the push also asks for permission.
- **Never move or delete a pushed tag.** A release that went wrong gets the next
  version.
- **An rc is tagged on a `release/` branch that never merges.** Its branch is
  pushed only so the smoke run can check its commit out; never open a PR for it.
  `main` only ever carries plain versions.
- **Tag only a commit whose smoke run is green.** `release.mjs smoke <commit>`
  installs every agent's latest release on Linux and Windows against that exact
  commit. It runs before the tag because a pushed tag can't be retried away: a
  failure there would burn the version.
- **A `latest` release goes through a PR.** `main` needs an approval, and
  `release.yml` refuses a `latest` tag that isn't on `main`. Tag the PR's merge
  commit.
- **The version lives in three files:** `installer/package.json`,
  `installer/package-lock.json` and both headers in `mcp.pi.json`. `bump` sets
  all three, and `npm test` fails when `mcp.pi.json` disagrees.
- **Work in a worktree off `origin/main`**, never in a checkout with other work
  in it.

## Resume first

Run `status`, then find the first matching state for the version and skip to it:

| State | Go to |
| --- | --- |
| The tag is on origin (`git ls-remote --tags origin refs/tags/<tag>`) | Step 5; `watch` returns at once for a finished release |
| `latest` only: the release PR is merged, but there's no tag yet | Step 4b, tagging |
| `latest` only: the release PR is open | Step 4b, waiting |
| A `release/postman-plugin-<version>` branch exists, locally or on origin | [Resume a prepared release](#resume-a-prepared-release) |
| None of these | Step 1 |

### Resume a prepared release

Pick up the commit the branch already has; never recreate the branch from
`origin/main`, which would drop that commit. Use the first line that applies:

```bash
git worktree list | grep 'release/postman-plugin-<version>'           # a worktree has it: cd into that path
git worktree add .claude/worktrees/release-<version> release/postman-plugin-<version>    # a local branch only
git worktree add --track -b release/postman-plugin-<version> .claude/worktrees/release-<version> origin/release/postman-plugin-<version>    # origin only
```

In that worktree, `release.mjs check <version> HEAD` must pass. It also checks
that the commit carries the version. Then run Step 3's tests, and go to Step 4.

## Step 1 — Pick the version

```bash
release.mjs status                            # dist-tags, and what changed since npm's latest
release.mjs suggest rc [patch|minor|major]
release.mjs suggest latest [patch|minor|major]
```

With no level, `suggest` continues an open rc line: `next` is `0.2.0-rc.1` and
`latest` is `0.1.0`, so `rc` gives `0.2.0-rc.2` and `latest` gives `0.2.0`.
Pass a level to start a new line instead. Pick the level from `status`'s
changes:

- **minor**: a new agent route, a new skill, or a new installer command or flag
- **patch**: fixes and wording
- **major**: a breaking change to the CLI's commands, flags or exit codes

Promote an open rc line only when it holds everything `status` lists. Tell the
user the version and why, and wait for their confirmation.

## Step 2 — Pre-flight

```bash
release.mjs check <version>
```

It fails when the version already exists on npm or origin, when it would move its
dist-tag backwards, when `release.yml` can't map it to a dist-tag, or when `gh`
isn't signed in. Fix every `FAIL` before going on. Exit 2 means npm, GitHub or
origin didn't answer; nothing was checked, so fix the connection and rerun it.

## Step 3 — Prepare the release commit

```bash
git fetch origin
git worktree add .claude/worktrees/release-<version> -b release/postman-plugin-<version> origin/main
cd .claude/worktrees/release-<version>
node .claude/skills/release-installer/scripts/release.mjs bump <version>
(cd installer && npm ci && npm test && npm audit --omit=dev --audit-level=high && npm pack --dry-run)
```

`release.yml` runs the same audit before publishing, so a finding there would
otherwise fail only after the tag is pushed.

Also run the Pi harness against a throwaway Pi. It is what CI's `pi` job runs:

```bash
PI_PREFIX=$(mktemp -d) && npm install --no-save --prefix "$PI_PREFIX" @earendil-works/pi-coding-agent
(cd installer && PI_BIN="$PI_PREFIX/node_modules/.bin/pi" npm run test:pi-harness)
```

`git status --short` must show only the three version files. Commit them as
`release: @postman/postman-plugin <version>`.

## Step 4a — Tag an rc

```bash
git push -u origin release/postman-plugin-<version>
node .claude/skills/release-installer/scripts/release.mjs check <version> HEAD
node .claude/skills/release-installer/scripts/release.mjs smoke HEAD
git tag -a @postman/postman-plugin@<version> -m "@postman/postman-plugin <version>"
```

Run `smoke` with the Monitor tool; it takes about seven minutes and exits 0 on
green. Tag only when `check` and `smoke` both pass; for a red `smoke`, see
[When smoke fails](#when-smoke-fails).

Confirm with the user, then `git push origin @postman/postman-plugin@<version>`.
Go to Step 5.

## Step 4b — Release `latest` through a PR

```bash
git push -u origin release/postman-plugin-<version>
gh pr create --base main --title "release: @postman/postman-plugin <version>" --body-file <body>
```

The body lists what ships (`status`'s changes since the last `latest`), the
checks Step 3 ran, and that the merge commit gets tagged next. Then stop. The PR
needs an approval, so give the user the PR link and tell them to run
`/release-installer <version>` again once it merges.

Once it has merged, tag the merge commit. Rerun the checks against it first:
the PR may have changed after Step 3, or another release may have shipped
while it waited for approval.

```bash
MERGE=$(gh pr view release/postman-plugin-<version> --json mergeCommit --jq .mergeCommit.oid)
git fetch origin main
release.mjs check <version> "$MERGE"
release.mjs smoke "$MERGE"
git tag -a @postman/postman-plugin@<version> -m "@postman/postman-plugin <version>" "$MERGE"
```

Tag only when `check` and `smoke` both pass. Confirm with the user, then push the tag.

### When smoke fails

`smoke` names the failed job and step. Read it with
`gh run view <id> --log-failed` before deciding:

| Failed | Likely cause | Do |
| --- | --- | --- |
| an install, list or remove step | an agent's latest release changed a command the installer sends | stop and tell the user; fix the installer on `main` in its own PR, then release from the new commit |
| a harness step | the latest Pi, Droid or OpenCode loads the package differently | stop and tell the user; same as above |
| Kimi's install script, or a download | network or the vendor's host | rerun `smoke` once; tell the user if it fails again |

Nothing has been tagged at this point, so a red `smoke` costs no version.

## Step 5 — Watch it until it's live

Start this right after pushing the tag. Run it with the Monitor tool, so each line
reaches you as it prints, and wait for it to exit instead of polling yourself:

```bash
release.mjs watch <version> [--minutes N]   # default 30
```

It follows the tag's `release.yml` run to the end, then polls npm until the
version is live. Live means npm serves it, its dist-tag points at it, and
`npx @postman/postman-plugin@<version> --version` downloads and runs it. It
prints one line per change and exits 0 once live. It exits 1 with the reason
when the run fails, naming the failed job and step, or when the timeout passes
first. Pass each line on to the user as it arrives.

When the run fails, match the failed step:

| `release.yml` failed on | What happened | Do |
| --- | --- | --- |
| the tag does not match `package.json` | the tag is on the wrong commit; nothing was published | cut the next version from Step 1 |
| a latest release must be tagged on main | the tag is not on `main`; nothing was published | cut the next version from Step 1 |
| would move the dist-tag back | a newer version shipped meanwhile; nothing was published | cut a higher version |
| audit or tests | nothing was published | fix it on `main` in its own PR, then cut the next version |
| the release page, after npm published | the package is live and only the page is missing | `gh workflow run release.yml --ref <tag> -f tag=<tag>`: it skips the publish and creates the page. Then `release.mjs watch <version> --new-run`, which follows the retry instead of the failed run |
| the npm token exchange (404 on PUT) | the trusted-publisher link is broken, usually a renamed workflow | stop and tell the user; the npm package settings need an owner. Once they have repaired it: `gh workflow run release.yml --ref <tag> -f tag=<tag>`, then `release.mjs watch <version> --new-run` |

## Step 6 — Verify what shipped

```bash
release.mjs verify <version>
(cd installer && PI_PACKAGE=npm:@postman/postman-plugin@<version> PI_BIN="$PI_PREFIX/node_modules/.bin/pi" npm run test:pi-harness)
```

In a resumed session `PI_PREFIX` is gone; install Pi again as in Step 3.

`verify` checks npm, the dist-tag, the release page and its pre-release flag, and
`npx @postman/postman-plugin@<version> --version`. For `latest` it also reports
whether Pi's gallery lists the package yet; the gallery indexes npm on its own
schedule, so a 404 right after release is not a failure. The harness installs
the published version into Pi and checks the skills, the mandate and the MCP
server it registers.

For an rc, ask the user to try it by hand in Pi, the one step no script covers:
`pi install npm:@postman/postman-plugin@<version>`, then `/mcp login postman`
inside a Pi session, and a Postman task.

## Step 7 — Report and clean up

Report the version, the dist-tag, and the links to the npm page, the release page
and the run. Remove the worktree with `git worktree remove`, and delete an rc's
local `release/` branch; its tag keeps the commit.
