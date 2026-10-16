# Forge Debugger Skill

Diagnoses known failures in Atlassian Forge apps. Use it when there is an observed symptom, error message, broken behavior, failed command, or log output to investigate.

This skill is the incident/debugging lane. It works from evidence such as `forge lint`, deploy output, tunnel/log output, stack traces, app visibility problems, resolver errors, or blank UI, then drives toward a root cause and fix.

## Use For

- `forge deploy`, `forge install`, `forge lint`, or CLI failures
- Blank UI, missing panels, missing macros, or modules that do not appear after install
- Resolver errors, `invoke()` mismatches, handler path problems, or unexpected `undefined` responses
- Permission/scope failures, 403s, 410 Gone API migration issues, or production vs development differences
- Custom UI build/deploy problems, missing static assets, or frontend not rendering
- Apps that previously worked and now fail

## Do Not Use For

- General pre-release readiness checks without an observed failure
- Deep security audit, SAST, authz, secrets, tenant isolation, exploitability, or CVSS reporting
- Cost optimization, invocation reduction, storage/log tuning, memory tuning, or trigger-frequency optimization
- Creating a new Forge app from scratch

## Specialist Handoffs

- Use `forge-app-review` for broad pre-deploy readiness and architecture review when nothing is known to be broken.
- Use `forge-security-review` for deep security audit, SAST, authz, secrets, tenant isolation, exploitability, and CVSS reporting.
- Use `forge-cost-optimizer` for reducing invocations, GB-seconds, storage/log volume, trigger frequency, memory, and Forge platform consumption.
- Use `forge-app-builder` for creating, deploying, and installing a new Forge app workflow.

## What It Checks

- CLI and environment: Forge CLI version, login state, Node/npm state, and whether commands run in the app root.
- Manifest wiring: module keys, resource paths, function handlers, handler path resolution, scopes, products, and environments.
- Build/deploy state: `forge lint`, Custom UI build artifacts, deploy/install output, and product/site mismatch.
- Runtime evidence: `forge logs`, tunnel output, resolver stack traces, permissions errors, and API response status.
- Source wiring: `invoke()` names vs `resolver.define()` names, handler exports, missing files, and frontend/backend contract mismatches.
- Cleanup: remove temporary debug logs or verbose diagnostics once the root cause is resolved.

## Debugging Flow

1. Classify the symptom: deploy-time, install/visibility, runtime, UI rendering, permissions, production-only, or regression.
2. Run cheap checks first: `forge lint`, versions, package install/build status.
3. Follow the evidence: deploy output, logs, tunnel output, stack traces, and manifest/source wiring.
4. Fix the first confirmed root cause before continuing to deeper layers.
5. Validate with the narrowest relevant command, then redeploy or reinstall when needed.

Interactive exceptions: `forge login` and `forge tunnel` may require the user to run them in their own terminal.

## Example Prompts

```text
My Forge issue panel is blank after deploy. Debug it.
```

```text
forge deploy fails with this manifest error: <paste error>
```

```text
My resolver returns undefined and there are no logs.
```

```text
The app works in development but fails in production on customer.atlassian.net.
```

```text
I get a 403 from requestJira after adding a new feature.
```

See [SKILL.md](SKILL.md) for the full diagnostic workflow and common error patterns.
