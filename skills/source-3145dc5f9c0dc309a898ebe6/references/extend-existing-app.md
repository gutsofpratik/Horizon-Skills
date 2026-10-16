# Extend an existing app

Read this reference only when changing an existing Forge app.

## Understand the affected architecture

Locate the app from its manifest, read repository instructions, and check working-tree state. Inspect enough of the manifest, code, dependencies, configuration, and tests to understand the requested change. Base conclusions on actual wiring rather than directory names.

Identify the smallest set of affected surfaces before planning edits. Preserve unrelated changes and supported project conventions.

## Choose a compatible change strategy

Prefer the smallest compatible change. Separate migration from feature work when combining them would add unrelated risk or make verification ambiguous.

When considering the Forge module command, confirm its current lifecycle status and compatibility first. While it is non-GA, obtain agreement to that exposure and inspect `forge module add --dry-run` before applying changes. Never use `--force` without explicit approval for the specific overwrites or dependency upgrades.

Retrieve current documentation for affected modules and any observed legacy, deprecated, Preview, EAP, runtime, package, or manifest behavior. Plan validation from the actual impact of the change.
