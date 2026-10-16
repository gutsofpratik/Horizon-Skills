---
name: api-simulation
description: Use when developing or testing a real service that calls other HTTP APIs. Composes reusable dependency mocks on one local port, verifies which upstream calls the service made, and exercises dependency failures without requiring every service to run. Use for requests such as "run this service with mocked dependencies".
---

# API Simulation

A simulation runs your service for real while replacing its HTTP dependencies
with reproducible mocks. Owners' mocks contribute contract knowledge outside
the checkout; a saved `.sim.yaml` makes the same environment available to a
teammate or CI instead of rebuilding ad hoc fakes each session.

1. Identify the calls affected by the change from HTTP clients and base-URL
   configuration. Reuse an existing simulation when it covers those calls.
   **api-discovery** can reveal additional dependencies in shared code or
   other repositories; newly added calls still need local inspection. Only
   HTTP dependencies become mock members—databases, queues, and caches need
   their own test setup. The service under test stays outside the simulation.
2. Prefer each owner's maintained mock, found through its workspace and
   imported with `postman dependency add mock <id>`. A matching name alone
   does not establish ownership. When none is available, generate from the
   maintained contract through **api-mocking** and identify assumptions.
   If workspace access is unavailable, continue with available local contracts
   and report the provenance gap rather than making login a prerequisite to
   local work. Use stateful behavior when a write must affect a later read.
3. Compose members with unique route keys. With path routing, a request to
   `http://localhost:<port>/<routeKey>/...` selects a member and strips the
   route key before the mock sees it. Keep service base URLs aligned with
   those addresses; a mock's separately deployed URL bypasses the simulation's
   fault injection and logging.

   ```yaml
   simulation: feeds-dev
   routing: path
   mocks:
     - routeKey: acs
       path: ../mocks/acs/config.yaml
     - routeKey: workspaces
       path: ../.dependencies/mocks/workspace-service/config.yaml
   ```

   Use [the simulation schema](reference/sim_yaml_schema.md) when authoring
   members or overrides, and `postman simulation -h` for the installed
   command surface. Local `.sim.yaml` runs need no login; workspace IDs do.
4. Run the file with an explicit `--port` and `--output ndjson`. An implicit
   busy port may change automatically and leave the service pointed elsewhere.
   Keep stderr separate from the event log; the listening event establishes
   actual member addresses. Restart the simulation after mock edits.
   In its own terminal, Ctrl+C stops it. For background runs, track the actual
   serving process: signaling only the launcher can leave members running.
5. Call the changed route on the real service, then inspect member request
   events for route, method, status, and duration. A started member with no
   expected requests is not evidence that the dependency path worked.
   Distinguish unknown route keys from unmodeled endpoints and crashed mock
   handlers; fix wiring or mock coverage before attributing these to the
   service. Fork imported mocks into `postman/mocks/` before customization,
   because `dependency update` replaces downloaded files.
6. Inject faults when recovery behavior is at risk. Member
   `scenarios[].overrides.conditions` supplies latency, errors, rate limits,
   or chaos; a scenario path alone does not inject faults, and
   `overrides.bypass` is ignored. Isolate conditions to attribute the outcome.
   Rejected requests can fail before the mock logs them, so also inspect
   the real service's response. Members share `pm.state`; namespace their
   keys to prevent unrelated mocks overwriting each other's records.
7. Keep owned mocks, simulations, and dependency declarations in the PR so
   others can reproduce the test; `postman dependency install` restores
   imported members after a clone. Exclude raw request logs from commits
   because headers and bodies can contain tokens. A passing simulation
   validates behavior under the modeled contract. Before a compatibility
   claim at release, verify the changed interaction against the real upstream
   in an appropriate environment, or state that verification is outstanding.

A local loop needs no push or deployment. `simulation push` uploads members
as well as the simulation, including copies of imported mocks, so review its
sharing scope through **bootstrap**. Unlike Code Mock deployment,
`simulation deploy` is public by default; establish intended exposure and
use `--private` when access should require an API key.

## Verification

Report what ran for real, where each mock came from, expected calls actually
observed, and the service's response to any injected failure. These distinguish
a tested dependency path from a simulation that merely started successfully.
