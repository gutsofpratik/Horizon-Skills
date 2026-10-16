# OAuth Setup — Zoom MCP Server

## Overview

The documented path for Zoom MCP is a **General app** using **user-level OAuth**.
Each user authorizes with their own Zoom account, and the resulting bearer token is passed by
the bundled connector in [`.mcp.json`](../../../.mcp.json).

Authentication path depends on the Claude product:

- **Claude Cowork**: use the published Zoom connector in Claude's connector directory and complete OAuth there.
- **Claude Code**: manually complete Zoom user-level OAuth, export `ZOOM_MCP_ACCESS_TOKEN`, reconnect the plugin, then use [`/setup-zoom-mcp`](../../setup-zoom-mcp/SKILL.md).

## Step 1: Create a General App with User-Level OAuth

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us) → **Develop** → **Build App**.
2. Create a **General app**.
3. Configure the app for **user-level OAuth** for the per-user MCP path.
4. Set a redirect URL for your client or local test environment.
5. Note the client ID and client secret.

### If You Do Not Already Have a Redirect Endpoint

For development, two pragmatic options are:

**Option 0: `localhost` and manually copy the code**

Example:

```text
http://localhost:3000/oauth/zoom/callback
```

If the local app does not actually handle the callback yet, the browser may show a failed page
load. You can still copy the `code` and `state` values from the browser URL and paste them into
Claude or your terminal flow so the token exchange can continue manually.

Pros:
- no tunnel and no third-party capture service
- fastest setup if you only need the authorization code once
- keeps the authorization code on your machine

Cons:
- manual copy/paste step every time
- no automatic code exchange or refresh flow
- less convenient if you repeat the auth flow often

**Option 1: `ngrok` in front of a local callback server**

Example:

```text
Local app: http://localhost:3000/oauth/zoom/callback
Public redirect URL: https://your-subdomain.ngrok.app/oauth/zoom/callback
```

Pros:
- best match for the real OAuth flow because your own app receives the callback directly
- easy to inspect requests locally while keeping your app logic in one place
- useful if you also need to exchange the code for tokens automatically

Cons:
- requires running a local server plus the tunnel
- slightly more setup than a capture-only endpoint
- you are exposing a local service to the internet, so keep the callback narrow and temporary

**Option 2: `webhook.site` for one-off callback capture**

Example:

```text
https://webhook.site/your-token
```

Pros:
- fastest path when you just need to capture the authorization redirect once
- no local server required
- easy to inspect the query string and copy out `code` and `state`

Cons:
- not a full OAuth app backend; you still need to exchange the code for tokens yourself
- weaker fit for repeated development flows and team usage
- the authorization code is sensitive, so only use this for short-lived development testing and
  avoid shared or long-lived capture URLs

Practical recommendation:
- use plain `localhost` if you only need a one-off auth code and are fine copying it manually
- use `ngrok` if you are building a real integration or expect to repeat the flow
- use `webhook.site` only for quick one-off testing when you do not yet have a callback handler

## Step 2: Configure Zoom MCP Scopes

Add the MCP-specific granular scopes required by the tools you want to use.

### Main Zoom MCP server

Required scopes, accurate as of 28 Jul 2026:

| Product Area | Scope | Zoom label | Needed for |
|--------------|-------|------------|------------|
| AI Companion | `ai_companion:read:search` | Search across Zoom Meeting, Zoom Chat, and Zoom Doc, returning the most relevant results based on the query. | semantic MCP search |
| Meeting | `meeting:read:search` | Search and view meetings | `search_meetings` |
| Meeting | `meeting:read:assets` | View a meeting's assets | `get_meeting_assets` |
| Recording | `cloud_recording:read:list_user_recordings` | Lists all cloud recordings for a user. | `recordings_list` |
| Recording | `cloud_recording:read:content` | read recording content scope | `get_recording_resource` |
| Zoom Docs | `docs:write:import` | Create new file by import | `create_new_file_with_markdown` |
| Zoom Docs | `docs:read:export` | Read file content in Markdown format | `get_file_content` |
| Zoom Hub | `hub:write:content` | Create a new file from content | `hub_create_file_from_content` |
| Zoom Hub | `hub:read:content` | Read file content in the requested format | `hub_get_file_content` |

For the main Zoom MCP server at `https://mcp.zoom.us/mcp/zoom/streamable`, the current published
scope set is the 9 scopes listed above.

Minimum recommendation for the main Zoom MCP connector:
- use a General app
- use user-level OAuth
- include the 9 main MCP scopes above on the same app when all default tools are needed

For the current Zoom Canvas MCP connector:
- use `https://mcp.zoom.us/mcp/canvas/streamable`
- add only the exact Canvas/Docs scopes for the tools you will call
- use [references/servers.md](../references/servers.md) for the complete mapping

For the current Zoom Chat MCP connector:
- use `https://mcp.zoom.us/mcp/chat/streamable`
- add only the exact Chat scopes for the tools you will call
- use [../team-chat/SKILL.md](../team-chat/SKILL.md) for tool behavior and write-safety rules

For the current Zoom Meetings MCP connector:
- use `https://mcp.zoom.us/mcp/meeting/streamable`
- add `meeting:read:search`, `meeting:read:assets`,
  `cloud_recording:read:list_user_recordings`, and `cloud_recording:read:content` as needed

For the current Zoom Tasks MCP connector:
- use `https://mcp.zoom.us/mcp/tasks/streamable`
- add the exact `tasks:read:*`, `tasks:write:*`, `tasks:update:*`, and `tasks:delete:*` scopes
  required by the selected tools

For the current Zoom Revenue Accelerator MCP connector:
- use `https://mcp.zoom.us/mcp/revenue_accelerator/streamable`
- add the exact `zra:read:*` scopes required by the selected tools

### Current Zoom Whiteboard MCP server

For `https://mcp.zoom.us/mcp/whiteboard/streamable`:

Documented tool scopes, accurate as of 28 Jul 2026:

| Tool | Required scope |
|------|----------------|
| `add_a_whiteboard_collaborator` | `whiteboard:write:collaborator` |
| `create_a_whiteboard` | `whiteboard:write:whiteboard` |
| `create_a_whiteboard_by_script` | `whiteboard:write:whiteboard` |
| `create_a_whiteboard_for_brainstorming` | `whiteboard:write:whiteboard` |
| `create_a_whiteboard_for_meeting_summary` | `whiteboard:write:whiteboard` |
| `create_a_whiteboard_for_strategy_analysis` | `whiteboard:write:whiteboard` |
| `delete_a_whiteboard_collaborator` | `whiteboard:delete:collaborator` |
| `get_a_whiteboard` | `whiteboard:read:whiteboard` |
| `get_a_whiteboard_collaborator` | `whiteboard:read:list_collaborators` |
| `list_whiteboards` | `whiteboard:read:list_whiteboards` |
| `update_a_whiteboard_collaborator` | `whiteboard:update:collaborator` |

Whiteboard MCP uses a separate scope set. See [../whiteboard/SKILL.md](../whiteboard/SKILL.md).

The old `/mcp/docs` and `/mcp/team_chat` paths are retained only for compatibility with existing
client configurations. Use [the current server catalog](../references/servers.md) for every exact
tool-to-scope mapping and the official product links.

## Step 3: Authorize and Exchange for Tokens

1. Construct the authorization URL:
   ```
   https://zoom.us/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI
   ```
2. Sign in as the Zoom user who should authorize the app and approve the requested scopes.
3. Copy the `code` from the redirect URL.
4. Exchange the code for tokens:
   ```bash
   curl -X POST https://zoom.us/oauth/token \
     -u "CLIENT_ID:CLIENT_SECRET" \
     -d "grant_type=authorization_code&code=CODE&redirect_uri=REDIRECT_URI"
   ```
5. Store the returned `access_token` and `refresh_token`.

Treat the refresh token as **single-use**:
- every successful refresh can return a new refresh token
- persist the newly returned refresh token atomically with the new access token
- stop using the old refresh token after a successful refresh
- avoid concurrent refresh requests against the same stored token

If you used `webhook.site`, the callback will arrive as a captured request and the `code`
parameter will be in the query string. Exchange it immediately and do not keep using the same
capture URL longer than necessary.

## Step 4: Enable AI Companion Features

Smart Recording and Meeting Summary are feature prerequisites for useful semantic meeting
search, meeting assets, and transcript-rich recording content.

In the Zoom web portal:
1. Go to **Admin → Account Management → Account Settings → AI Companion**.
2. Enable **Smart Recording**.
3. Enable **Meeting Summary**.

Important:
- these settings do **not** replace the OAuth scopes above
- they affect whether useful recap and transcript content exists for MCP retrieval

## Step 5: Provide the Token to the Bundled MCP Connector

Export the token environment variable used by this plugin:

```bash
export ZOOM_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_MEETINGS_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_CANVAS_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_CHAT_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_TASKS_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_REVENUE_ACCELERATOR_MCP_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export ZOOM_WHITEBOARD_MCP_ACCESS_TOKEN="YOUR_WHITEBOARD_ACCESS_TOKEN"
```

Verification:
- restart Claude Code or re-enable the plugin so the bundled MCP server restarts with the token
- in Claude Code, use [`/setup-zoom-mcp`](../../setup-zoom-mcp/SKILL.md) after exporting the token
- confirm the client can see 9 default Zoom MCP tools: `search_meetings`,
  `create_new_file_with_markdown`, `search_zoom`, `get_meeting_assets`,
  `get_recording_resource`, `get_file_content`, `recordings_list`,
  `hub_create_file_from_content`, and `hub_get_file_content`
- for Canvas MCP, confirm the client can see the Canvas tools required by the workflow
- if your client exposes protocol inspection, use `tools/list` as the authority for the live catalog
- run a simple tool such as `recordings_list` to verify the token has the correct MCP scopes

## Token Lifecycle

| Property | Details |
|----------|---------|
| Access token expiry | About 1 hour |
| Refresh flow | Exchange `refresh_token` for a new `access_token` and replacement `refresh_token` |
| Client update | Update `ZOOM_MCP_ACCESS_TOKEN`, then restart Claude Code or re-enable the plugin |

Refresh exchange:

```bash
curl -X POST https://zoom.us/oauth/token \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN"
```

After a successful refresh:
- replace the stored access token
- replace the stored refresh token
- treat the previously used refresh token as spent
- restart Claude Code or re-enable the plugin if you are injecting tokens through env vars

## Environment Variables

```bash
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_MCP_ACCESS_TOKEN=your_access_token
ZOOM_MEETINGS_MCP_ACCESS_TOKEN=your_access_token
ZOOM_CANVAS_MCP_ACCESS_TOKEN=your_access_token
ZOOM_CHAT_MCP_ACCESS_TOKEN=your_access_token
ZOOM_TASKS_MCP_ACCESS_TOKEN=your_access_token
ZOOM_REVENUE_ACCELERATOR_MCP_ACCESS_TOKEN=your_access_token
ZOOM_WHITEBOARD_MCP_ACCESS_TOKEN=your_whiteboard_access_token
ZOOM_REFRESH_TOKEN=your_refresh_token
```

See also: [../../oauth/SKILL.md](../../oauth/SKILL.md)
