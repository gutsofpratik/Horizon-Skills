# App Playwright

Drive the FiftyOne App via the Playwright MCP — operator/plugin verification, demo and screencast recording, and end-to-end UI automation against a live `fo.launch_app(...)` session.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-app-playwright** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)
- The [Playwright MCP server](https://github.com/microsoft/playwright-mcp) connected to your AI assistant
  - **NOTE**: The [default config](https://playwright.dev/docs/getting-started-mcp#headed-mode) for the Playwright MCP uses 'headed' mode, meaning a browser will launch; if the optional `--headless` flag is enabled, no browser will open and users will need to navigate to `localhost:<PORT>` to observe the session.

## Usage

Ask your AI assistant:

```
"Use Playwright to verify my operator updates the sidebar after Execute"
"Record a screencast of my plugin running on the quickstart dataset"
"Automate the FiftyOne App to filter the grid by a sample tag"
"My FiftyOne session keeps dying after reload_dataset — help me automate it safely"
```

The skill launches the App with a refresh-over-WebSocket pattern that avoids the
session-killing `browser_navigate`-after-`reload_dataset` crash, then drives the
React/MUI UI with stable selectors.

## What it covers

- The #1 crash: never navigate or reload after an operator calls `ctx.ops.reload_dataset()`
- Launcher patterns: `remote=True`, trigger-file IPC, non-persistent clones with a safe pre-delete guard
- MUI/React gotchas: controlled inputs, comboboxes, synthesized clicks, dialog scrolling
- Finding elements with `data-cy` selectors and leaf-text matching
- Sidebar tag filtering, modal navigation, recording pacing, and scoped cleanup

## Bundled scripts

- `scripts/launch_app.py` — parameterized launcher implementing the trigger-file refresh loop

## See also

- [FiftyOne App docs](https://docs.voxel51.com/user_guide/app.html)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Discord community](https://discord.gg/fiftyone-community)
