---
name: api-mocking
description: Use when creating a stand-in backend from a collection or OpenAPI spec, testing failure scenarios, or sharing a Code Mock through a workspace and deployed URL. Keeps mock behavior reusable in the repository and distinguishes example replay from stateful behavior. Use for requests such as "mock this backend".
---

# API Mocking

A saved mock lets frontend work and API checks proceed without a live backend,
while preserving the behavior for later sessions, teammates, and CI. Its value
depends on the contract it represents: a plausible response invented locally
can hide an integration mismatch.

1. Reuse a maintained contract or owner's mock before generating behavior.
   Use **api-discovery** to find another service's resource and
   **api-simulation** when a real service calls several mocked dependencies.
   This skill covers CLI Code Mocks; MCP `createMock` creates classic mocks
   that serve collection examples and has a different lifecycle.
2. Generate locally with `postman mock generate <source> -n <name>`, where
   the source is a collection file/directory or OpenAPI spec. The resulting
   `config.yaml` and `default.js` under `postman/mocks/<name>/` are reviewable
   artifacts; `default.js` is the HTTP server itself. Generating without a
   source creates a sample cart API, useful for learning mock behavior but
   not evidence about the user's API.
3. Run the folder with `postman mock run <path>`. Local generation and runs
   work without login. Read the actual listening URL: an occupied configured
   port can cause automatic fallback; an explicit `--port` makes that conflict
   fail instead. Restart after handler edits because there is no hot reload.
4. Choose response behavior to match the test. `x-mock-scenario` selects a
   name from `config.yaml`; an unknown name silently uses the default.
   `x-mock-response-code` selects an existing example with that status and
   cannot create a missing error response. Verify the intended body/status,
   not merely that a request returned 200.
5. Example replay does not connect a write to a later read. For workflows
   needing that relationship, use async `pm.state` in the handler. Seed and
   reset records so tests can reproduce a starting state; return the
   contract's missing-record response. Local runs start with empty state,
   while deployed servers retain it between requests. Callers share state
   unless sessions isolate them via `x-mock-session`; local session handling
   needs `interceptRequests: true`, and deployed mocks need sessions enabled.
   That config also supplies parsed `req.body` and `req.query`.
6. Preserve custom behavior when refreshing from a changed contract.
   `postman mock generate <source> --update <path>` regenerates the default
   handler while retaining name, port, and scenarios; inspect the diff before
   relying on custom stateful code again. Use command-specific `-h` for
   supported options rather than carrying flags across actions.

## Share when a remote caller needs it

A local folder can be pushed later without rebuilding the mock.
`postman mock push <path>` records its workspace mapping in
`.postman/resources.yaml`; retain that mapping with the files. Use
**bootstrap** for unresolved binding/authentication and publishing consent.
A push can update what an already deployed server serves, so it is a shared
behavior change, not merely a backup. `generate --workspace` instead creates
only a workspace definition, with no local folder to run or review.

Deploy the workspace mock when a teammate, remote CI job, or webhook sender
needs a durable URL. Code Mock deployment is private by default and requires
`x-api-key`; use `--public` only for an intended public audience. Read
`postman mock deploy -h` for deployment options. A local test needs no deploy.

Use the workspace mock ID returned by the workspace operation for `get`,
`run`, `deploy`, and `delete`. For logs, fetch that mock with `mock get` and
use its separate `mockServerId` with `mock log`; do not infer one ID from the
other. Logs help establish which requests reached the deployed server.

Deleting a mock requires stopping local runs and, for a workspace mock,
taking down its deployed server first. Workspace deletion leaves the local
mapping behind; remove that stale entry if deletion was intended.

## Verification

Report whether the result is local, pushed, or deployed, its actual URL and
visibility when applicable, and observed scenario responses. Use
**api-testing**'s mock run options to reuse collection assertions; passing
against a mock establishes behavior under that model, not live compatibility.
