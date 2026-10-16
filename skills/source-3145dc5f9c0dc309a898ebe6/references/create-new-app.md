# Create a new app

Read this reference only for a new deployable Forge app.

## Decide before scaffolding

Resolve enough of the architecture to choose an appropriate current scaffold. Retrieve the exact module and scaffolding documentation before selecting a template.

Check prerequisites only when creation is imminent. Retrieve current requirements, then inspect Node.js, Forge CLI, and authentication state. If login is required, direct the user to run `forge login` interactively without sharing credentials.

Confirm the destination, app name, and Developer Space. If multiple spaces are available, require the user to choose. If one is available, inform the user before using it. Explain that `forge create` registers an external app identity in the selected Developer Space.

Immediately before non-interactive creation, show that the helper passes the current CLI option for accepting Forge terms and any applicable billing consent, then obtain explicit authorization. Do not invoke the helper without that authorization. If authorization is absent, let the user complete the current interactive `forge create` flow; never accept terms on the user's behalf.

## Choose one scaffold branch

### Stable template-first branch

Prefer a current module-specific `forge create` template when it cleanly matches the architecture. Use `scripts.create_forge_app` with the current documented template name. Do not use an undocumented registry as an independent source of truth.

Run the helper from the skill directory:

```bash
python3 -m scripts.list_templates --validate <current-documented-template>

python3 -m scripts.create_forge_app \
  --template <current-documented-template> \
  --name <app-name> \
  --dev-space-id <selected-id> \
  --directory <parent-directory>
```

### Compositional branch

Consider a blank `forge create` app when the app needs several modules, no suitable stable template exists, or deliberate module composition is clearer.

```bash
python3 -m scripts.create_forge_app \
  --template blank \
  --name <app-name> \
  --dev-space-id <selected-id> \
  --directory <parent-directory>
```

Before using `forge module add`, retrieve its current lifecycle and CLI documentation. If it is non-GA, obtain agreement to that exposure. Inspect `forge module add --dry-run` before applying changes, and never use `--force` without explicit approval for the specific overwrites or dependency upgrades.

Official entries:

- `forge create`: <https://developer.atlassian.com/platform/forge/cli-reference/create/>
- Developer Spaces: <https://developer.atlassian.com/platform/forge/developer-space/create-developer-space/>
- Module command tutorial: <https://developer.atlassian.com/platform/forge/build-a-jira-app-with-the-module-command/>
- `forge module add`: <https://developer.atlassian.com/platform/forge/cli-reference/module-add/>

## Handle creation failure

Show the complete failure and triage it by cause:

- If the CLI requires interaction, provide the exact current interactive `forge create` command for the user to run in their terminal.
- If no Developer Space exists, direct the user to create one in the Atlassian developer console, then retry after they confirm the target.
- If the destination already exists, use a different confirmed name or destination. Never delete or overwrite the existing directory without explicit authorization.
- If authentication is missing or expired, direct the user to run `forge login` interactively without sharing credentials, then retry.
- For any other failure, preserve the command output, retrieve the relevant current documentation, and explain what blocks creation before asking for the input or external change needed to continue.

Never construct a replacement app ID or manual scaffold. Route to `forge-debugger` if diagnosis of a persistent failure becomes the primary task.
