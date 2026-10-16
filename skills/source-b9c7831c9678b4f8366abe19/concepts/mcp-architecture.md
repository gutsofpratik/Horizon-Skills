# MCP Architecture — Zoom MCP Server

## What is MCP?

Model Context Protocol (MCP) standardizes how AI systems connect to external tools and data
sources. Zoom exposes hosted MCP surfaces that clients can discover and call over MCP.

## Hosted Zoom MCP Surfaces

Zoom currently publishes seven product-specific MCP servers. The canonical endpoint and tool
inventory is in [references/servers.md](../references/servers.md).

| Server | Streamable HTTP endpoint |
|---|---|
| Zoom MCP | `https://mcp.zoom.us/mcp/zoom/streamable` |
| Zoom Meetings MCP | `https://mcp.zoom.us/mcp/meeting/streamable` |
| Zoom Canvas MCP | `https://mcp.zoom.us/mcp/canvas/streamable` |
| Zoom Chat MCP | `https://mcp.zoom.us/mcp/chat/streamable` |
| Zoom Tasks MCP | `https://mcp.zoom.us/mcp/tasks/streamable` |
| Zoom Revenue Accelerator MCP | `https://mcp.zoom.us/mcp/revenue_accelerator/streamable` |
| Zoom Whiteboard MCP | `https://mcp.zoom.us/mcp/whiteboard/streamable` |

The former `/mcp/docs` and `/mcp/team_chat` paths are compatibility paths and should not be
selected for new integrations. The folder [../team-chat/SKILL.md](../team-chat/SKILL.md) remains
the compatibility location for current Zoom Chat MCP guidance.

## Discovery Model

Do not hardcode tool counts in client logic.

Use the MCP protocol `tools/list` response as the current source of truth for:
- tool names
- descriptions
- parameter schemas
- newly added or removed tools

## Current Capability Shape

The current Zoom MCP catalog covers:
- semantic meeting search
- cross-Zoom search over meetings, Team Chat, Zoom Docs, and My Notes
- meeting asset retrieval
- recording resource retrieval
- Zoom Docs and Hub content creation and retrieval
- Canvas, Chat, Tasks, Revenue Accelerator, and Whiteboard operations

If the task requires deterministic meeting CRUD, use the REST API skill instead of assuming
those operations exist on the current Zoom MCP surface.

## Authentication Model

User OAuth is the primary documented path.
Use user OAuth as the expected auth model for the bundled Zoom MCP servers in this plugin.

## Protected Resource Metadata

The hosted MCP surfaces advertise supported scopes through OAuth protected-resource metadata.
Zoom MCP protected-resource metadata currently exposes:
- `ai_companion:read:search`
- `meeting:read:assets`
- `meeting:read:search`
- `cloud_recording:read:content`
- `cloud_recording:read:list_user_recordings`
- `docs:write:import`
- `docs:read:export`
- `hub:write:content`
- `hub:read:content`

Canvas MCP tools use granular Docs scopes such as:
- `docs:read:export`
- `docs:write:import`
- `docs:read:file`
- `docs:write:content`
- `docs:update:content`
- `docs:delete:content`

Chat MCP tools use granular Chat scopes such as:
- `team_chat:read:list_user_messages`
- `team_chat:write:user_message`
- `team_chat:update:user_message`
- `team_chat:read:list_user_channels`
- `team_chat:write:user_channel`

Tasks MCP tools use granular Tasks scopes such as:
- `tasks:read:list_tasks`
- `tasks:read:task`
- `tasks:write:task`
- `tasks:update:task`
- `tasks:delete:trash_task`

Revenue Accelerator MCP tools use `zra:read:*` granular scopes.

Whiteboard MCP tools use current user-level scopes:
- `whiteboard:write:whiteboard`
- `whiteboard:read:list_whiteboards`
- `whiteboard:read:whiteboard`

Zoom Chat MCP tools currently require scopes such as:
- `team_chat:write:user_message`
- `team_chat:update:user_message`
- `team_chat:write:contact_information`
- `team_chat:write:user_channel`
- `team_chat:update:user_channel`
- `team_chat:write:members`

## Retrieval Model

`search_meetings` is not just a title filter. It is a semantic retrieval path over meeting
content, recap-linked assets, and recording-linked artifacts.

Useful result families:
- recap-oriented results with AI summaries and linked assets
- recording-oriented results for post-meeting content retrieval

When writing parsers, validate the live response shape from the server rather than relying on
older example field names.

## Feature Prerequisites

AI Companion features such as **Smart Recording** and **Meeting Summary** are feature
prerequisites for useful semantic retrieval and recap-linked content. They do not replace the
required OAuth scopes.

## Error Layering

Failures can happen at two layers:
- MCP protocol layer (`-32001`, `-32602`, `-32603`)
- underlying Zoom API-style permission/resource failures surfaced through the MCP response

See [../references/error-codes.md](../references/error-codes.md).
