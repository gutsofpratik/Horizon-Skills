---
name: setup-zoom-marketplace-app
description: Create, update, select, or validate the Zoom Marketplace app that owns an integration. Use for General App manifests, Server-to-Server OAuth apps, Meeting SDK apps, scopes, event subscriptions, app-owned credentials, or choosing a scenario template before product implementation.
argument-hint: "<integration scenario or existing app configuration>"
---

# /setup-zoom-marketplace-app

Set up the Zoom Marketplace app boundary before implementing OAuth, API, SDK, webhook, WebSocket, RTMS, Team Chat, Contact Center, Phone, Zoom Apps, or MCP workflows.

## Workflow

1. Identify whether the task creates a new app or updates an existing app, then classify the product scenario, actor, account ownership, and app model.
2. Inspect the machine-readable template index and verify `app_type`, `usage`, `unsupported_app_types`, and `supports_manifest_update` before selecting the narrowest template.
3. When the app requires public URLs, obtain the user's own HTTPS app base URL and implemented route paths before creating it. Use their hosted service, or help them expose their local app with ngrok or Cloudflare Tunnel. Do not invent an endpoint or reuse a helper operator's endpoint.
4. For a new app, replace sample names, URLs, domains, contacts, commands, and scopes. Keep only scopes required by the exact operations.
5. Check whether tools from `app-builder-for-agents` are available. When the helper supports the required validation, creation, or update operation, use it as the preferred execution path without requiring the user to name the server again.
6. Before any write operation, show a concise preview of the target account, app model, display name, user-owned URLs, scopes, products, and subscriptions, then obtain explicit confirmation.
7. For an existing General App, export its complete manifest, apply the requested changes in memory, validate with its `app_id`, replace it, and export it again. Never apply a static template directly.
8. For a new General App, validate the inner `manifest` and check both HTTP status and the response `ok` value before creating it.
9. Create native S2S and Meeting SDK apps with the required master scope; these are create requests, not General App manifests.
10. Complete post-create setup that the public schema does not reliably encode, including WebSocket delivery and some webhook or RTMS event subscriptions.
11. Store generated secrets in a secret manager, record only safe environment-variable names, and return to the owning product workflow.

## Helper Tool Chaining

- Apply this section whenever another plugin skill routes here, including `start`, planning,
  OAuth, SDK, API, bot, webhook, and MCP workflows.
- Discover the connected `app-builder-for-agents` tools and inspect their input schemas; do not
  invent tool names or arguments.
- Prefer a supported helper tool over asking the user to run Marketplace API requests manually.
- Use read and validation operations before writes when the helper exposes them.
- Treat create, update, credential generation, scope changes, subscription changes, and deletion
  as account mutations. Require confirmation immediately before the first mutation and again if
  the target account, app, URLs, scopes, or operation changes.
- After a successful mutation, read back the app or exported manifest and compare it with the
  approved configuration. Do not declare success from the write response alone.
- If the helper is unavailable, unauthenticated, or does not support the required operation,
  report that limitation and continue by producing the validated payload and exact manual or API
  steps. Never claim that an app was created or changed when no write tool succeeded.
- After app setup, return to the originating skill and continue its OAuth or product workflow.

## Optional Claude Code Marketplace Helper

To let Claude Code create or validate Marketplace apps programmatically, register a separately
hosted Marketplace helper MCP server. This plugin does not bundle or host that helper server.
Start the helper first, expose its `/mcp` endpoint over HTTPS, and register the current endpoint:

```bash
claude mcp add --transport http \
  app-builder-for-agents \
  https://marketplacehelper.asdc.cc/mcp
```

The current helper endpoint is `https://marketplacehelper.asdc.cc/mcp`. If it changes, update the
Claude Code server registration with the new `/mcp` URL. If you run a different local helper
instance, expose its port with `ngrok http HELPER_PORT` or
`cloudflared tunnel --url http://localhost:HELPER_PORT` instead.
The helper MCP URL is only a Claude Code server registration value. Never use its hostname,
the helper operator's OAuth client ID, the helper operator's authorization URL, or the helper
operator's callback URL as an OAuth redirect, home URL, allow-list entry, or webhook URL in an
app created for a user.
Only register a helper endpoint that you trust because it can create or modify Marketplace apps
and may handle app credentials. After registration, use `/setup-zoom-marketplace-app`; this skill
selects the helper automatically when its tools are available.

### Local Tunnel URL Synchronization

When the app being created or updated runs locally, expose the app with `ngrok` or Cloudflare
Tunnel before using the helper. The helper's own public MCP endpoint and the app's public test
URL are separate concerns.

Before creating or updating the app, collect the current app tunnel hostname and the actual
route paths. For a development configuration, update the matching fields in the manifest:

- `oauth_information.development_redirect_uri`
- `oauth_information.oauth_allow_list`
- `features.development_home_uri`, when the app has a home URL
- `event_subscription.subscriptions[].development_webhook_url`, when the app has webhooks

Build any OAuth authorization URL from the client ID Zoom issues for the user's app and the
exact redirect URI configured for that app. Do not substitute credentials or URLs from the
Marketplace helper deployment. If a required app endpoint is not available, help the user start
a tunnel or obtain their hosted endpoint before creating the app.

After every tunnel restart, assume the previous hostname is invalid and update these development
URLs before testing OAuth, opening the app home page, or waiting for webhook delivery. Do not
replace production URLs with an ephemeral tunnel unless the user explicitly requests that.
The tunnel forwards traffic only; the local server must implement each route and its OAuth or
webhook validation behavior.

## Primary References

- [Marketplace app management](../rest-api/references/marketplace-apps.md)
- [Marketplace template selector](../rest-api/references/marketplace-app-templates.md)
- [Machine-readable template index](../rest-api/assets/marketplace-apps/marketplace-manifest-template-index.json)
- [General App manifest update workflow](../rest-api/references/marketplace-manifest-update-workflow.md)
- [OAuth](../oauth/SKILL.md)
- [REST API](../rest-api/SKILL.md)

## Guardrails

- Do not mix user and admin scope suffixes in one General App.
- Do not use S2S for Meeting/Webinar RTMS or Team Chat chatbot subscriptions.
- Do not invent `webhook` or `webhook_only` app types.
- Do not use a General App manifest update workflow for native `s2s_oauth` or `meeting_sdk` apps.
- Use only the user's own tunnel or hosted endpoints for their app's OAuth redirect, allow-list,
  home, and webhook URLs. Never copy the Marketplace helper's endpoint or its operator's OAuth
  app credentials into a user app.
- Never remove existing scopes or event subscriptions during an update unless the user explicitly requests it.
- Do not print, commit, or retain generated client secrets in logs or test artifacts.
- Treat schema validation as necessary but not sufficient; licensing, entitlements, authorization, and Marketplace review can still block runtime use.
