---
name: zoom-mcp/whiteboard
description: |
  Guidance for Zoom Whiteboard MCP. Use for Whiteboard MCP auth, endpoints, ID mapping,
  current user-level scopes, and tool workflows such as list_whiteboards and get_a_whiteboard.
  Prefer this skill when the request is specifically about Whiteboard MCP rather than general Zoom MCP.
user-invocable: false
triggers:
  - "whiteboard mcp"
  - "zoom whiteboard mcp"
  - "zoom mcp whiteboard"
  - "zoom whiteboard tools"
  - "list zoom whiteboards"
  - "get zoom whiteboard"
  - "zoom whiteboard id"
  - "zoom wb/db"
---

# Zoom MCP Whiteboard

Dedicated guidance for Zoom's Whiteboard MCP server.

## Endpoints

| Transport | URL |
|-----------|-----|
| Streamable HTTP (recommended) | `https://mcp.zoom.us/mcp/whiteboard/streamable` |

## Authentication

- Start app registration from the
  [Whiteboard MCP template](../../rest-api/assets/marketplace-apps/marketplace-manifest-template-for-mcp-whiteboard.json).
- **User OAuth with Whiteboard scopes** is the documented path for Whiteboard MCP execution.
- The bundled connector expects the token in `ZOOM_WHITEBOARD_MCP_ACCESS_TOKEN`.

Reference: [references/authentication-and-identifiers.md](references/authentication-and-identifiers.md)

## Required Scopes

Whiteboard MCP tool scopes:
- `add_a_whiteboard_collaborator` → `whiteboard:write:collaborator`
- `create_a_whiteboard` → `whiteboard:write:whiteboard`
- `create_a_whiteboard_by_script` → `whiteboard:write:whiteboard`
- `create_a_whiteboard_for_brainstorming` → `whiteboard:write:whiteboard`
- `create_a_whiteboard_for_meeting_summary` → `whiteboard:write:whiteboard`
- `create_a_whiteboard_for_strategy_analysis` → `whiteboard:write:whiteboard`
- `delete_a_whiteboard_collaborator` → `whiteboard:delete:collaborator`
- `get_a_whiteboard` → `whiteboard:read:whiteboard`
- `get_a_whiteboard_collaborator` → `whiteboard:read:list_collaborators`
- `list_whiteboards` → `whiteboard:read:list_whiteboards`
- `update_a_whiteboard_collaborator` → `whiteboard:update:collaborator`

## Whiteboard ID Mapping

For Whiteboard MCP, use the identifier from the URL segment after `/wb/db/`, not the numeric
segment after `/p/`.

Example:

```text
https://us05whiteboard.zoom.us/wb/db/6iktP8hJT3e5qaCuwFuAGg/p/180968285929472
                                     ^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^
                                     whiteboard_id            page/subresource id
```

## Available Tools

The current Whiteboard MCP tool surface is:

- `add_a_whiteboard_collaborator`
- `create_a_whiteboard_for_brainstorming`
- `list_whiteboards`
- `create_a_whiteboard`
- `get_a_whiteboard`
- `get_a_whiteboard_collaborator`
- `create_a_whiteboard_by_script`
- `update_a_whiteboard_collaborator`
- `delete_a_whiteboard_collaborator`
- `create_a_whiteboard_for_meeting_summary`
- `create_a_whiteboard_for_strategy_analysis`

Some MCP clients namespace server tools in the UI. Treat the raw tool names above as
authoritative.

Reference: [references/tools.md](references/tools.md)

## Read Workflow

1. Use a user OAuth token with the Whiteboard read scopes.
2. Call `list_whiteboards` to discover accessible whiteboards and confirm the correct `whiteboard_id`.
3. Call `get_a_whiteboard` with that `whiteboard_id`.

## Chaining

- Parent MCP skill: [../SKILL.md](../SKILL.md)
- OAuth guidance: [../concepts/oauth-setup.md](../concepts/oauth-setup.md)
- General routing: [../../general/SKILL.md](../../general/SKILL.md)

## References

- [references/authentication-and-identifiers.md](references/authentication-and-identifiers.md) - Auth behavior and Whiteboard ID mapping.
- [references/tools.md](references/tools.md) - Whiteboard MCP tool catalog.
