# zoom-mcp RUNBOOK — 5-Minute Preflight

Quick diagnostic checklist before using the Zoom MCP server.

## Preflight Checklist

**1. Token exported for the bundled connector?**
```bash
echo "${ZOOM_MCP_ACCESS_TOKEN:+set}"
echo "${ZOOM_MEETINGS_MCP_ACCESS_TOKEN:+set}"
echo "${ZOOM_CANVAS_MCP_ACCESS_TOKEN:+set}"
echo "${ZOOM_CHAT_MCP_ACCESS_TOKEN:+set}"
echo "${ZOOM_TASKS_MCP_ACCESS_TOKEN:+set}"
echo "${ZOOM_REVENUE_ACCELERATOR_MCP_ACCESS_TOKEN:+set}"
echo "${ZOOM_WHITEBOARD_MCP_ACCESS_TOKEN:+set}"
```
If empty, export the relevant token using [concepts/oauth-setup.md](concepts/oauth-setup.md).

**2. Tool discovery working?**
- Confirm the client can see 9 default Zoom MCP tools: `search_meetings`,
  `create_new_file_with_markdown`, `search_zoom`, `get_meeting_assets`,
  `get_recording_resource`, `get_file_content`, `recordings_list`,
  `hub_create_file_from_content`, and `hub_get_file_content`.
- For product-specific servers, compare the visible tools with
  [references/servers.md](references/servers.md).
- The current catalog includes Meetings, Canvas, Chat, Tasks, Revenue Accelerator, and
  Whiteboard MCP surfaces in addition to the default Zoom MCP server.
- If your client exposes raw protocol inspection, verify `tools/list` succeeds.
- Compare the visible tools with [references/tools.md](references/tools.md).

**3. Correct OAuth scopes on the token?**

Minimum Zoom MCP scopes for this guide:
- `ai_companion:read:search` — Search across Zoom Meeting, Zoom Chat, and Zoom Doc
- `meeting:read:search` — Search and view meetings
- `meeting:read:assets` — View a meeting's assets
- `cloud_recording:read:list_user_recordings` — Lists all cloud recordings for a user.
- `cloud_recording:read:content` — read recording content scope
- `docs:write:import` — Create Zoom Docs from Markdown through the main Zoom MCP server
- `docs:read:export` — Read Zoom Docs or My Notes Markdown content
- `hub:write:content` — Create Hub files from content
- `hub:read:content` — Read Hub file content

Canvas, Chat, Tasks, Revenue Accelerator, and Whiteboard use separate scope sets. See
[references/servers.md](references/servers.md) and the child guidance where applicable.

**4. AI Companion features enabled?**

Go to Zoom web portal → **Admin → Account Management → Account Settings → AI Companion**.
Confirm **Smart Recording** and **Meeting Summary** are enabled if you expect semantic search,
meeting assets, or transcript-rich recording content to be useful.

## Quick Fixes

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `-32001 Access token is required` | Token env var missing or empty | Export `ZOOM_MCP_ACCESS_TOKEN`, then restart Claude Code |
| `-32001 Invalid access token, does not contain scopes:[meeting:read:search]` | Missing semantic-search scope | Add `meeting:read:search` and mint a new user token |
| `-32001 Invalid access token, does not contain scopes:[meeting:read:assets,...]` | Missing meeting-assets scope | Add `meeting:read:assets` and mint a new user token |
| `-32001 Invalid access token, does not contain scopes:[ai_companion:read:search]` | Missing cross-Zoom search scope | Add `ai_companion:read:search` and mint a new user token |
| `-32001 Invalid access token, does not contain scopes:[cloud_recording:read:list_user_recordings,...]` | Missing recordings-list scope | Add `cloud_recording:read:list_user_recordings` |
| `-32001 Invalid access token, does not contain scopes:[cloud_recording:read:content]` | Missing recording-content scope | Add `cloud_recording:read:content` |
| `-32001 Invalid access token, does not contain scopes:[docs:read:export]` | Missing Docs export scope | Add `docs:read:export` and mint a new user token |
| `-32001 Invalid access token, does not contain scopes:[hub:read:content]` | Missing Hub content-read scope | Add `hub:read:content` and mint a new user token |
| `-32602 Can not found tool: ... in this MCP Server` | Wrong endpoint surface or wrong tool name | Re-run `tools/list` and use the current tool names for the active MCP server |
| `-32603 Call handle error` | Missing required parameters or server-side call handling failure | Re-check required arguments against the live schema and retry |
| `Upstream API returned error status code: 400 ... invalid param` | Invalid parameter value passed through to the underlying Zoom API | Fix the specific argument value, such as `parent_id` for Docs creation on the Canvas MCP server |
| Search returns no useful meeting content | AI Companion features missing or data not indexed | Enable Smart Recording + Meeting Summary, widen the search window, or fall back to `recordings_list` |

## Auth Reality Check

Use user OAuth as the documented execution path for Zoom MCP content tools in this plugin.
Do not rely on Server-to-Server OAuth as a supported MCP auth model here.

## Where to Get Help

- Developer forum: https://devforum.zoom.us/
- Zoom support: https://support.zoom.com/
- MCP protocol docs: https://modelcontextprotocol.io/
