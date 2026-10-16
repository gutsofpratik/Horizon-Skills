---
name: setup-zoom-mcp
description: Decide when Zoom MCP is the right fit and produce a safe setup plan for Claude. Use when planning AI workflows over Zoom data, deciding between MCP and REST, or defining a hybrid MCP architecture.
argument-hint: "<AI workflow or MCP use case>"
---

# /setup-zoom-mcp

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Plan a Zoom MCP workflow and decide when to use MCP alone versus a hybrid REST API + MCP architecture.

## Usage

```text
/setup-zoom-mcp $ARGUMENTS
```

## Workflow

1. Determine whether the goal is deterministic automation, AI tool orchestration, or a hybrid.
2. Identify whether the client uses Claude's published connector or requires a manually registered General App.
3. For manual registration, select the default, Meetings, Canvas, Chat, Tasks, Revenue Accelerator, or Whiteboard MCP template through [setup-zoom-marketplace-app](../setup-zoom-marketplace-app/SKILL.md).
4. If MCP is appropriate, identify the likely Zoom MCP surface and transport assumptions.
5. If MCP alone is not enough, define the REST API responsibilities separately.
6. Call out auth, scope, and client capability constraints, especially the difference between Claude Cowork and Claude Code auth paths.
7. End with a minimal proof-of-concept sequence.

## Output

- Recommended MCP strategy
- Connector expectations
- Hybrid boundaries if REST is also required
- Risks and setup notes
- Relevant skill links

## Auth Rules

- **Claude Cowork**: use the published Zoom connector and complete OAuth in Claude's connector flow.
- **Claude Code**: for manual OAuth, start from the matching Marketplace MCP template, complete user-level OAuth, export `ZOOM_MCP_ACCESS_TOKEN`, reconnect the plugin, then continue with this skill.
- Scope requirements differ by MCP server. Use the server-specific scope sets below and the detailed tables in [../zoom-mcp/concepts/oauth-setup.md](../zoom-mcp/concepts/oauth-setup.md).

## Current Zoom MCP Servers

Use [the current server catalog](../zoom-mcp/references/servers.md) for the complete tool-to-scope
mapping. The production endpoints and scope families below were verified on 28 Jul 2026.

| Server | Endpoint | Scope set |
|---|---|---|
| Zoom MCP | `https://mcp.zoom.us/mcp/zoom/streamable` | `meeting:read:search`, `meeting:read:assets`, `ai_companion:read:search`, `cloud_recording:read:list_user_recordings`, `cloud_recording:read:content`, `docs:write:import`, `docs:read:export`, `hub:write:content`, `hub:read:content` |
| Zoom Meetings MCP | `https://mcp.zoom.us/mcp/meeting/streamable` | `meeting:read:search`, `meeting:read:assets`, `cloud_recording:read:list_user_recordings`, `cloud_recording:read:content` |
| Zoom Canvas MCP | `https://mcp.zoom.us/mcp/canvas/streamable` | `docs:read:*`, `docs:write:*`, `docs:update:*`, and `docs:delete:*` scopes required by the selected Canvas tools |
| Zoom Chat MCP | `https://mcp.zoom.us/mcp/chat/streamable` | `team_chat:read:*`, `team_chat:write:*`, and `team_chat:update:*` scopes required by the selected Chat tools |
| Zoom Tasks MCP | `https://mcp.zoom.us/mcp/tasks/streamable` | `tasks:read:*`, `tasks:write:*`, `tasks:update:*`, and `tasks:delete:*` scopes required by the selected Tasks tools |
| Zoom Revenue Accelerator MCP | `https://mcp.zoom.us/mcp/revenue_accelerator/streamable` | `zra:read:*` scopes required by the selected Revenue Accelerator tools |
| Zoom Whiteboard MCP | `https://mcp.zoom.us/mcp/whiteboard/streamable` | `whiteboard:read:*`, `whiteboard:write:*`, `whiteboard:update:*`, and `whiteboard:delete:*` scopes required by the selected Whiteboard tools |

Do not request wildcard scopes. Expand the exact granular scopes from the catalog for the tools
the workflow will call. The old `/mcp/docs` and `/mcp/team_chat` paths are legacy compatibility
surfaces, not new server entries.

## Related Skills

- [design-mcp-workflow](../design-mcp-workflow/SKILL.md)
- [setup-zoom-marketplace-app](../setup-zoom-marketplace-app/SKILL.md)
- [choose-zoom-approach](../choose-zoom-approach/SKILL.md)
