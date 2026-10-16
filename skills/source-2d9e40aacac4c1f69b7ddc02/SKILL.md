---
name: setup
description: Set up the Rootly plugin. Verifies MCP server connection via OAuth2 or API token and guides through configuration. Run this after installing the plugin.
disable-model-invocation: true
allowed-tools:
  - Bash
  - mcp__rootly__*
---

# Rootly Plugin Setup

You are running the first-time setup for the Rootly Claude plugin. Follow these steps in order:

## Step 1: Verify MCP Connection

First, test the MCP server connection by calling `mcp__rootly__get_server_version`.

- **Succeeds**: The MCP server is reachable. Continue to Step 2.
- **Fails with 401 / OAuth prompt**: Claude should automatically start the OAuth2 flow -- a browser window will open for you to log in to Rootly and grant access. Once authorized, retry `mcp__rootly__get_server_version`.
- **Fails with other error**: MCP server connection issue. Check network connectivity to `https://mcp.rootly.com`.

## Step 2: Verify Authentication

Call `mcp__rootly__getCurrentUser` to confirm your identity.

- **Succeeds**: Authentication is working. Report the authenticated user and team, then continue to Step 3.
- **Fails**: Authentication issue. Provide troubleshooting:

> **Authentication Troubleshooting**
>
> This plugin uses **OAuth2** by default -- Claude handles the login flow automatically when it connects to the MCP server. No API token is needed for MCP commands.
>
> If OAuth2 is not working:
> 1. Ensure your Rootly organization has OAuth2 enabled
> 2. Try disconnecting and reconnecting the MCP server: `/mcp` > find Rootly > disconnect > reconnect
> 3. Check that your browser can reach `https://rootly.com/oauth/authorize`
>
> **Fallback: API Token (for hook scripts or environments without browser access)**
>
> Hook scripts (active-incident warnings on commit/push) still need an API token:
> 1. Go to your Rootly dashboard: **Settings > API Keys**
> 2. Create a new API key
> 3. Provide the token through the plugin's userConfig prompt, or `export ROOTLY_API_TOKEN="..."`
>
> API tokens are optional for MCP commands -- OAuth2 is the recommended auth method.

Then stop here -- no further steps possible without working authentication.

## Step 3: Service Mapping Configuration

Check if `.claude/rootly-config.json` exists in the current project directory.

**If the file does NOT exist**, offer to create it:

1. Ask the user which Rootly service(s) correspond to this repository
2. Ask which team owns this service (optional)
3. Create `.claude/rootly-config.json` with the format:
   ```json
   {
     "services": ["service-name-1", "service-name-2"],
     "team": "team-name"
   }
   ```

**If the file exists**, read and display its current configuration.

## Step 4: Show Quick-Start Guide

Once setup is complete, display:

> **Rootly plugin is ready!**
>
> **Authentication**: OAuth2 (logged in as {user name})
>
> | Command | Description |
> |---------|-------------|
> | `/rootly:deploy-check` | Check deployment safety before pushing |
> | `/rootly:respond [incident-id]` | Investigate and respond to an incident |
> | `/rootly:oncall` | View on-call dashboard |
> | `/rootly:retro [incident-id]` | Generate post-incident retrospective |
> | `/rootly:status` | Service health overview |
> | `/rootly:ask [question]` | Ask questions about your incident data |
> | `/rootly:brief [incident-id]` | Generate stakeholder brief for executives |
> | `/rootly:handoff [incident-id]` | Prepare incident or on-call handoff docs |
>
> Hooks are active:
> - **Session start**: Connection validation (already ran)
> - **Pre-commit/push**: Active critical incident warnings (requires API token in plugin config)
