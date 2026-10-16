---
name: zoom-mcp
description: Guidance for Zoom's MCP server catalog. Use after routing to an MCP workflow when planning or troubleshooting tool-based access to Meetings, Canvas, Chat, Tasks, Revenue Accelerator, Whiteboard, recordings, meeting assets, transcripts, Zoom-wide search, or Docs. Use the current server catalog for endpoints and scopes.
user-invocable: false
triggers:
  - "zoom mcp"
  - "zoom mcp server"
  - "zoom mcp tools"
  - "zoom tools/list"
  - "zoom tools/call"
  - "ai companion transcript"
  - "agentic retrieval"
  - "zoom semantic meeting search"
  - "zoom search meetings by content"
  - "zoom meeting assets mcp"
  - "zoom recording resource mcp"
  - "zoom docs via mcp"
  - "zoom docs content via mcp"
  - "zoom canvas mcp"
  - "zoom meetings mcp"
  - "zoom chat search mcp"
  - "zoom tasks mcp"
  - "zoom revenue accelerator mcp"
  - "team chat mcp"
  - "zoom team chat mcp"
  - "zoom transcript via mcp"
  - "meeting transcript via mcp"
---

# Zoom MCP

Guidance for the bundled Zoom MCP connector in this Claude plugin. Prefer `design-mcp-workflow` or [setup-zoom-mcp](../setup-zoom-mcp/SKILL.md) first, then route here for tool-surface details, auth expectations, and MCP-specific constraints.

# Zoom MCP Server

Zoom's current hosted MCP catalog uses `mcp.zoom.us` for AI-agent access to:

- semantic meeting search
- cross-Zoom search over Team Chat messages, Zoom Docs, and My Notes
- meeting-linked asset retrieval
- recording resource retrieval
- Zoom Docs and Hub content creation and retrieval
- Canvas, Chat, Tasks, Revenue Accelerator, and Whiteboard product workflows

The complete current server and scope inventory is in
[references/servers.md](references/servers.md). The dedicated `/mcp/docs` path and the former
`/mcp/team_chat` path are retained only as legacy compatibility references; use Canvas and Chat
for new integrations.

Current tool names from the main Zoom MCP server, verified by `tools/list`:

- `create_new_file_with_markdown`
- `get_file_content`
- `get_meeting_assets`
- `get_recording_resource`
- `hub_create_file_from_content`
- `hub_get_file_content`
- `recordings_list`
- `search_meetings`
- `search_zoom`

Some MCP clients namespace server tools in the UI, for example `zoom-mcp:recordings_list`.
Treat the raw tool names above as authoritative.

Docs-specific MCP work can use the main `zoom-mcp` server or the current Zoom Canvas MCP server;
use the exact tool names exposed by the active server.

Whiteboard-specific MCP work is covered by the dedicated skill
[whiteboard/SKILL.md](whiteboard/SKILL.md).

Product-specific Chat MCP work is covered by the child skill
[team-chat/SKILL.md](team-chat/SKILL.md). The folder name is retained for compatibility with
existing links; the current official server is Zoom Chat at `/mcp/chat/streamable`.

> **Need the OAuth app/scopes first?** Use
> [Marketplace app management](../rest-api/references/marketplace-apps.md) to create or
> validate the General App, select user/admin scopes for MCP tools, and understand credential
> response shapes before minting the bearer token passed to the MCP server. Start from the
> [default Zoom MCP template](../rest-api/assets/marketplace-apps/marketplace-manifest-template-for-mcp-default.json), or
> select the matching Meetings, Canvas, Chat, Tasks, Revenue Accelerator, or Whiteboard template from the
> [Marketplace template selector](../rest-api/references/marketplace-app-templates.md). Automated
> selection must inspect the
> [template index](../rest-api/assets/marketplace-apps/marketplace-manifest-template-index.json)
> and require `app_type: general`, `usage: USER_OPERATION`, and
> `supports_manifest_update: true`.

## Quick Start

**1. Use the right auth path for your Claude product**

- **Claude Cowork**: use the published Zoom connector in Claude's connector directory and complete OAuth there.
- **Claude Code**: do not use the built-in `Authenticate` button for this server; complete Zoom user-level OAuth yourself and provide the token through `ZOOM_MCP_ACCESS_TOKEN`.

**2. Export the token expected by the bundled connector:**

```bash
export ZOOM_MCP_ACCESS_TOKEN="your_zoom_user_oauth_access_token"
```

**3. Enable or restart the plugin so Claude restarts the bundled MCP server definition.**

**4. Verify discovery:**
- Confirm the client can see 9 default Zoom MCP tools: `search_meetings`,
  `create_new_file_with_markdown`, `search_zoom`, `get_meeting_assets`,
  `get_recording_resource`, `get_file_content`, `recordings_list`,
  `hub_create_file_from_content`, and `hub_get_file_content`.
- If the client exposes raw protocol inspection, `tools/list` is the authoritative discovery source.
- The current catalog is documented in [references/tools.md](references/tools.md).

**5. In Claude Code, use `/setup-zoom-mcp` to continue the setup and workflow design.**

**6. Run the first useful call:**
```text
recordings_list
  userId: "me"
  from: "2026-03-01"
  to: "2026-03-06"
  page_size: 10
```

## Critical Notes

**1. User OAuth is the documented execution path**

Use a **General app** with **user-level OAuth** as the execution path for Zoom MCP
tool use in this plugin. Do not rely on Server-to-Server OAuth as a supported MCP auth model here.

**2. Zoom MCP uses MCP-specific granular scopes**

The Zoom MCP scope set is not the same as the older broad REST scopes.
The key scopes for the main Zoom MCP server at `https://mcp.zoom.us/mcp/zoom/streamable`,
accurate as of 28 Jul 2026, are:
- `ai_companion:read:search` — Search across Zoom Meeting, Zoom Chat, and Zoom Doc, returning the most relevant results based on the query
- `meeting:read:search` — Search and view meetings
- `meeting:read:assets` — View a meeting's assets
- `cloud_recording:read:list_user_recordings` — Lists all cloud recordings for a user.
- `cloud_recording:read:content` — read recording content scope
- `docs:write:import` — Create a new file by import
- `docs:read:export` — Read file content in Markdown format
- `hub:write:content` — Create Hub files from content
- `hub:read:content` — Read Hub file content

Other Zoom MCP servers use different scope sets. Use [references/servers.md](references/servers.md)
and the published Zoom MCP server pages as the source of truth for those surfaces.

**3. AI Companion features are feature prerequisites, not scope substitutes**

Semantic meeting search, meeting assets, and recording-content retrieval depend on account
features such as **Smart Recording** and **Meeting Summary** for useful results. These feature
settings do not replace the required OAuth scopes.

**4. Whiteboard is a separate MCP surface**

The Zoom MCP endpoint and the Whiteboard MCP endpoint are separate. Route Whiteboard-specific
requests to [whiteboard/SKILL.md](whiteboard/SKILL.md).

**5. Zoom Chat tools are a separate MCP surface**

The default Zoom MCP server includes read-only `search_zoom` for Chat and Docs search.
The Zoom Chat MCP server is separate and exposes read/write tools for messages, contacts,
channels, files, and sessions. Route Chat MCP requests to
[team-chat/SKILL.md](team-chat/SKILL.md).

**6. Use REST for deterministic meeting CRUD**

The current Zoom MCP tool surface does not expose deterministic
meeting create, update, or delete tools. If the user needs explicit meeting CRUD operations,
route to [../rest-api/SKILL.md](../rest-api/SKILL.md).

## Server Endpoints

| Transport | URL |
|-----------|-----|
| Streamable HTTP (recommended) | `https://mcp.zoom.us/mcp/zoom/streamable` |
| SSE (fallback) | `https://mcp.zoom.us/mcp/zoom/sse` |

All current product-specific endpoints are listed in [references/servers.md](references/servers.md).
The current official product paths include `/meeting`, `/canvas`, `/chat`, `/tasks`,
`/revenue_accelerator`, and `/whiteboard`.

## Search and Retrieval Model

`search_meetings` uses AI Companion retrieval rather than a plain metadata filter. In this
use the live MCP server as authoritative for response schema and scope behavior.

Two result families matter most:

- **Recap-oriented results**: AI summary, meeting-linked documents, recordings, and related assets
- **Recording-oriented results**: cloud recording references and transcript-capable resources

Use [examples/transcript-retrieval.md](examples/transcript-retrieval.md) for the main retrieval
workflow.

Use `search_zoom` instead of `search_meetings` when the task is cross-Zoom knowledge discovery
over Team Chat messages, Zoom Docs, or My Notes. Use `get_file_content` after `search_zoom`
when the user asks to inspect the Markdown content of a returned Zoom Doc or My Notes file.

## Tool Catalog

| Tool | Key Parameters | Required Scope |
|------|---------------|----------------|
| `create_new_file_with_markdown` | `content`*, `file_name`, `parent_id` | `docs:write:import` |
| `get_file_content` | `fileId`* | `docs:read:export` |
| `get_meeting_assets` | `meetingId`* | `meeting:read:assets` |
| `search_meetings` | `q`, `from`, `to`, `page_size`, `next_page_token` | `meeting:read:search` |
| `search_zoom` | `search_entities`*, `query`, `page_size` | `ai_companion:read:search` |
| `get_recording_resource` | `meetingId`*, `types`, `clip_num`, `play_time`, `raw_passcode`, `encode_passcode` | `cloud_recording:read:content` |
| `recordings_list` | `userId`*, `from`, `to`, `meeting_id`, `trash`, `trash_type`, `page_size`, `next_page_token` | `cloud_recording:read:list_user_recordings` |
| `hub_create_file_from_content` | `content`*, `file_type`* | `hub:write:content` |
| `hub_get_file_content` | `file_id`*, `format`* | `hub:read:content` |

\* Required parameter

Full parameter and output guidance: [references/tools.md](references/tools.md)

## Key Workflows

**Search meeting content, then retrieve assets:**
```text
search_meetings
  q: "Q4 planning discussion"
  from: "2026-03-01"
  to: "2026-03-06"
→ choose a returned meeting
→ get_meeting_assets  meetingId: "MEETING_ID_OR_UUID"
```

**List recordings, then retrieve recording resources:**
```text
recordings_list
  userId: "me"
  from: "2026-03-01"
  to: "2026-03-06"
→ choose a recording target
→ get_recording_resource  meetingId: "MEETING_UUID_OR_RECORDING_ID"
```

**Create a Zoom Doc from Markdown:**
```text
create_new_file_with_markdown
  file_name: "Q4 Planning Notes"
  content: "# Decisions\n\n- ..."
```

**Search Zoom Chat or Docs, then read a returned file:**
```text
search_zoom
  query: "Q4 planning decisions"
  search_entities:
    - entity_type: "zoom_doc"
      filters:
        doc_view: "notes"
  page_size: 10
→ choose a returned Zoom Doc file_id
→ get_file_content  fileId: "FILE_ID"
```

**Use Zoom Canvas MCP for current Docs and Canvas workflows:**
- `create_file_with_content`
- `get_file_content`
- `canvas_insert_block`
- `canvas_update_block`
- `canvas_replace_range_of_blocks`

## Error Reference

| Code | Meaning | Fix |
|------|---------|-----|
| `401 Unauthorized` | Missing or rejected bearer token at the endpoint | Set `ZOOM_MCP_ACCESS_TOKEN`, then restart Claude or re-enable the plugin |
| `-32001 Invalid access token` | Token expired, malformed, or missing required scopes | Refresh OAuth token and verify the MCP-specific scopes |
| `-32602 Can not found tool` | Requested tool name is not exposed by the active MCP server | Re-run `tools/list` and use the current tool names for that endpoint |
| `404` | Possible downstream resource-not-found response | Re-discover the target with `search_meetings` or `recordings_list` |

Full error reference: [references/error-codes.md](references/error-codes.md)

## Documentation

### Concepts
- [concepts/mcp-architecture.md](concepts/mcp-architecture.md) — MCP protocol, hosted endpoints, discovery, and capability model
- [concepts/oauth-setup.md](concepts/oauth-setup.md) — OAuth app creation, MCP-specific scopes, AI Companion prerequisites, token lifecycle

### Examples
- [examples/transcript-retrieval.md](examples/transcript-retrieval.md) — Search/assets and recording-resource workflows
- [examples/search-chat-docs.md](examples/search-chat-docs.md) — Cross-Zoom search over Team Chat, Zoom Docs, and My Notes
- [examples/create-zoom-doc.md](examples/create-zoom-doc.md) — Verified Zoom Docs creation flow
- [examples/search-and-act.md](examples/search-and-act.md) — Search, inspect assets, and hand off CRUD work to REST when needed
- [examples/meeting-lifecycle.md](examples/meeting-lifecycle.md) — Why meeting CRUD belongs in REST, plus the MCP-to-REST handoff pattern

### References
- [references/tools.md](references/tools.md) — Current Zoom MCP tool reference
- [references/servers.md](references/servers.md) — Current Zoom MCP server catalog, endpoints, and scope mappings
- [references/error-codes.md](references/error-codes.md) — MCP and Zoom API errors with fixes
- [whiteboard/SKILL.md](whiteboard/SKILL.md) — Dedicated Whiteboard MCP skill
- [team-chat/SKILL.md](team-chat/SKILL.md) — Zoom Chat MCP child skill; folder retained for compatibility

### Troubleshooting
- [troubleshooting/common-errors.md](troubleshooting/common-errors.md) — Scope failures, endpoint mixups, search/recording issues

### Operations
- [RUNBOOK.md](RUNBOOK.md) — 5-minute preflight and debugging checklist

## Related Skills

- [zoom-rest-api](../rest-api/SKILL.md) — Deterministic REST API access, including meeting CRUD
- [zoom-oauth](../oauth/SKILL.md) — OAuth implementation patterns
- [zoom-webhooks](../webhooks/SKILL.md) — Event-driven recording and meeting workflows
- [zoom-rtms](../rtms/SKILL.md) — Live media and transcript streams during active meetings
