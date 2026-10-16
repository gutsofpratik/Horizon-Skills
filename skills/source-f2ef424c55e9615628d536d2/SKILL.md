---
name: bootstrap
description: Use when resolving Postman CLI setup, authentication, or a repository workspace binding; initializing local API files; or importing, pulling, pushing, syncing, or sharing workspace resources. Reuses existing context and chooses sync direction without duplicating a workspace or rebinding a dependency. Use for requests such as "set up Postman for this repo".
---

# Bootstrap Postman for This Repo

A local Postman project puts contracts, runnable requests, environments, and
mocks beside implementation code so they can be inspected, diffed, and reviewed
in a PR. A workspace binding connects that work to maintained shared context.
Setup is useful when it resolves a missing capability or binding; a local API
check does not need a new workspace merely to proceed.

## Resolve only the missing setup

Inspect `postman --version`, `.postman/resources.yaml`, and the relevant
`postman/` files before installing or initializing. Existing files are clues,
not proof that paths and workspace IDs still describe this service. Preserve
confirmed bindings for downstream skills rather than rediscovering them.

**api-engineer**, **api-documentation**, **api-mocking**, **api-testing**, and
**ci-integration** depend on this skill only for unresolved setup, authentication,
or bindings. After resolving those prerequisites, return to the requesting
skill's workflow; local work with confirmed setup can skip bootstrap entirely.

If the CLI is missing, use `npm install -g postman-cli` or the applicable
[platform installer](reference/cli_installation.md). Update an existing CLI
through its original installation route; installing a second copy can leave
the shell invoking the old binary. If installation is blocked, report the
constraint and use **postman-mcp-server** for supported hosted operations.

Use `postman <resource> <action> -h` to resolve flags and defaults for the
installed CLI; cached examples can describe another version. Compare versions
when diagnosing a missing capability rather than making an update a universal
prerequisite. Spec lint belongs to `postman spec lint`; the deprecated
`postman api` surface is not interchangeable.

Local file operations need no normal login. `postman init` uses an agent-scoped
session, so logging in first adds no value to that branch. Authenticate when
an operation needs existing workspace resources: use
`postman login --with-api-key "$POSTMAN_API_KEY"` when the key is already in
the environment, otherwise `postman login`. Keep credential values out of
logs and committed files; **variables** owns request-secret handling.

## Owning workspace versus dependency

Read `localResources` and `workspace.id` in `.postman/resources.yaml`. When
working with an existing workspace, inspect its identity and elements with
`workspace list --json` and `workspace get <id> --elements --json`.
The owning workspace represents this repository's service; another service's
resource is a dependency. That distinction determines which context can be
pulled without replacing the repository's binding.

| State and intended outcome | Operation |
| --- | --- |
| Existing local layout meets the task | Reuse its files and bindings |
| This service has a workspace; work on it locally | `postman workspace pull <workspace-id>` |
| Only record this service's Git binding | `postman workspace connect-git <workspace-id> [path]` |
| Another service's collection, environment, or mock is needed | Use **api-discovery**'s dependency workflow |
| New project with no existing workspace | `postman init --json`; add `--visibility personal` or `--visibility team` when creating a workspace is intended |
| Bound workspace is authoritative | `postman workspace pull` |
| Validated local changes should be published | Preview with `postman workspace diff --push-strategy default`, then `postman workspace push` |

Inspect local changes before pulling so an import does not discard work.
Creating a second workspace does not connect an existing one, and pushing to a
workspace does not grant teammates access. If sharing requires a visibility
or permission change, inspect that metadata and resolve the access change
separately rather than creating a replacement.

`workspace diff` is read-only; use the strategy planned for the push.
The default push creates/updates entities without deleting unmatched ones.
`--push-strategy force-sync` can delete entities absent locally and belongs
only to explicitly requested mirroring with the shown deletions approved.
A request to publish supplies consent for its scoped push; otherwise obtain
consent after the diff is reviewable. See **ci-integration** for publishing
reviewed changes after merge.

## Interpret initialization without losing partial success

Run init inside the intended repository. It scaffolds Postman files and
`.postman/resources.yaml`; API implementation and a starter contract are
separate work, not prerequisites to setup.

`--json` avoids interactive prompts. Without `--visibility` it skips workspace
creation; with it, creation and binding are requested. Read `bindings` and
`exitCode` from the JSON payload. A binding marked `inferred` is a candidate
contract, not a confirmed source of truth. Exit 2 means multiple specs need
selection with `--spec <path>`. Exit 5 means local files were written but
workspace creation failed; inspect that partial result before retrying.

## Verification

Report the working CLI, relevant paths, and actual binding or remaining gap.
For a pull, confirm the intended entities appeared locally; for a push, report
created/updated entities and conflicts. Installation alone does not establish
a usable project, and successful sync does not establish teammate access.

## Reporting CLI and skill gaps

Concrete reports help fix recurring CLI failures and misleading skill guidance.
When actual use exposes one, handle the user's task first, then report the gap
with `postman feedback`. Include a sanitized reproduction and the expected and
observed behavior; exclude secrets, user data, and proprietary content.
