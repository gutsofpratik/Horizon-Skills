---
name: setup
description: Connect and troubleshoot QuickBooks for this plugin. Use when the QuickBooks tools are unavailable, unauthenticated, or failing, when the user has just installed the QuickBooks plugin, or when the user asks how to connect QuickBooks, sign in to QuickBooks, or fix a QuickBooks connection error.
---

# QuickBooks Plugin Setup

This plugin provides skills only. The QuickBooks tools come from the **QuickBooks connector** on
the user's Claude account. Follow SETUP.md at the plugin root — the same steps are summarized
here.

## Check the connection first

Check whether QuickBooks tools (names starting with `qbo_` or containing `quickbooks`) are
available in this session. If a read-only tool such as `company_info` succeeds, setup is
complete — tell the user and stop.

## Step 1: Connect QuickBooks in Claude (all surfaces)

1. Go to https://claude.ai/customize/connectors (in Claude: Customize in the sidebar, then
   Connectors).
2. Find QuickBooks and click Connect.
3. Log in with the Intuit account for the QuickBooks company and grant the requested permissions.

On Team and Enterprise plans, only admins can add connectors for the organization. If the user
cannot connect QuickBooks themselves, tell them to ask their Claude administrator to add it (on
Team plans the directory shows a Request button). After it is added, each person connects it from
Customize → Connectors.

## Step 2: Claude Code only

1. The user must be signed in with a claude.ai account: run `/login` and select it. Connectors
   are not loaded when an API key (ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN / apiKeyHelper), a
   third-party provider (Bedrock, Google Cloud Agent Platform), an Anthropic profile, or a
   `claude setup-token` credential is active — if `/mcp` doesn't list QuickBooks, have the user
   run `/status`, then `/login`.
2. Run `/mcp`: QuickBooks appears in the claude.ai section (never-used connectors are collapsed
   behind "Show unused connectors"). Authorization is completed on claude.ai (Step 1), never
   in-terminal.
3. Do **not** suggest adding the QuickBooks server with `claude mcp add`: a locally added server
   takes precedence over the claude.ai connector at the same URL and hides it — and it will fail
   to authenticate, since Intuit's authorization server does not permit the localhost redirect
   Claude Code's in-terminal OAuth uses. If such an entry exists, remove it with
   `claude mcp remove <name>`.

## Step 3: Verify

Have the user start a new session (or restart Claude Code) so the connector list reloads, then
run a read-only test such as "How is my business doing this month?".

## Troubleshooting

- **Disconnected / asks to authorize again**: Customize → Connectors → Reconnect.
- **`/mcp` shows "connected · session token rejected"**: run `/login` again, then reconnect the
  connector from `/mcp`. Re-authorizing the connector alone does not clear this.
- **Organization doesn't list QuickBooks**: ask the Claude administrator to add it.
- **Wrong company data**: disconnect and reconnect, choosing the correct QuickBooks company
  during Intuit sign-in.
