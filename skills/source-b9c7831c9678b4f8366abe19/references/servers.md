# Zoom MCP Server Catalog

This is the canonical server inventory for this plugin. It was checked against the
[Zoom MCP server directory](https://developers.zoom.us/docs/mcp/servers/) and the
product-specific Zoom MCP pages on 28 Jul 2026.

The production endpoints below use `mcp.zoom.us`. The current product pages publish
Streamable HTTP endpoints; use the live server's discovery response as the authority for
transport and schema details.

## Current Official Servers

| Server | Production endpoint | Tools | Scope families |
|---|---|---:|---|
| Zoom MCP Server | `https://mcp.zoom.us/mcp/zoom/streamable` | 9 | Meetings, recordings, AI Companion search, Docs, Hub |
| Zoom Meetings MCP Server | `https://mcp.zoom.us/mcp/meeting/streamable` | 4 | Meeting search/assets, recordings |
| Zoom Canvas MCP Server | `https://mcp.zoom.us/mcp/canvas/streamable` | 18 | Canvas/Docs file, block, collaborator, and access operations |
| Zoom Chat MCP Server | `https://mcp.zoom.us/mcp/chat/streamable` | 20 | Chat messages, channels, contacts, files, sessions |
| Zoom Tasks MCP Server | `https://mcp.zoom.us/mcp/tasks/streamable` | 20 | Task, step, comment, assignee, and collaborator operations |
| Zoom Revenue Accelerator MCP Server | `https://mcp.zoom.us/mcp/revenue_accelerator/streamable` | 15 | Conversations, deals, analysis, scorecards, CRM, teams |
| Zoom Whiteboard MCP Server | `https://mcp.zoom.us/mcp/whiteboard/streamable` | 11 | Whiteboard and collaborator operations |

The plugin's `.mcp.json` contains all 7 current official server definitions. Each server uses
its own environment variable in the bundle so deployments can isolate tokens if needed. A
single user-level OAuth token may be assigned to all variables when it has the required scopes.

Official product pages:

- [Zoom MCP Server](https://developers.zoom.us/docs/mcp/zoom/)
- [Zoom Meetings MCP Server](https://developers.zoom.us/docs/mcp/zoom-meetings-mcp-server/)
- [Zoom Canvas MCP Server](https://developers.zoom.us/docs/mcp/zoom-canvas-mcp-server/)
- [Zoom Chat MCP Server](https://developers.zoom.us/docs/mcp/zoom-chat-mcp-server/)
- [Zoom Tasks MCP Server](https://developers.zoom.us/docs/mcp/zoom-tasks-mcp-server/)
- [Zoom Revenue Accelerator MCP Server](https://developers.zoom.us/docs/mcp/zoom-revenue-accelerator-mcp-server/)
- [Zoom Whiteboard MCP Server](https://developers.zoom.us/docs/mcp/zoom-whiteboard-mcp-server/)

## Legacy Compatibility Paths

These endpoints may still respond, but they are not current entries in Zoom's published server
directory:

- `https://mcp.zoom.us/mcp/docs/streamable` — older dedicated Docs surface. Current Docs tools
  are published through the Canvas MCP server and the default Zoom MCP server.
- `https://mcp.zoom.us/mcp/team_chat/streamable` — older Team Chat path. The current server is
  the Zoom Chat MCP server at `/mcp/chat/streamable`.

Do not use a legacy path for a new integration unless the live client configuration specifically
requires it. Use only the current `mcp.zoom.us` production host.

## Zoom MCP Server

Endpoint: `https://mcp.zoom.us/mcp/zoom/streamable`

| Tool | Required scope |
|---|---|
| `create_new_file_with_markdown` | `docs:write:import` |
| `get_file_content` | `docs:read:export` |
| `get_meeting_assets` | `meeting:read:assets` |
| `get_recording_resource` | `cloud_recording:read:content` |
| `hub_create_file_from_content` | `hub:write:content` |
| `hub_get_file_content` | `hub:read:content` |
| `recordings_list` | `cloud_recording:read:list_user_recordings` |
| `search_meetings` | `meeting:read:search` |
| `search_zoom` | `ai_companion:read:search` |

## Zoom Meetings MCP Server

Endpoint: `https://mcp.zoom.us/mcp/meeting/streamable`

| Tool | Required scope |
|---|---|
| `get_meeting_assets` | `meeting:read:assets` |
| `get_recording_resource` | `cloud_recording:read:content` |
| `recordings_list` | `cloud_recording:read:list_user_recordings` |
| `search_meetings` | `meeting:read:search` |

## Zoom Canvas MCP Server

Endpoint: `https://mcp.zoom.us/mcp/canvas/streamable`

| Tool | Required scope |
|---|---|
| `canvas_add_file_collaborators` | `docs:write:collaborator` |
| `canvas_delete_block` | `docs:delete:content` |
| `canvas_delete_file` | `docs:delete:file` |
| `canvas_get_file_general_access_setting` | `docs:read:general_access` |
| `canvas_get_file_metadata` | `docs:read:file` |
| `canvas_get_spec` | `docs:read:export` |
| `canvas_insert_block` | `docs:write:content` |
| `canvas_list_all_file_children` | `docs:read:list_children` |
| `canvas_list_file_collaborators` | `docs:read:list_file_collaborators` |
| `canvas_modify_file_collaborator_role` | `docs:update:collaborator` |
| `canvas_modify_file_general_access_setting` | `docs:update:general_access` |
| `canvas_modify_file_metadata` | `docs:update:file` |
| `canvas_remove_file_collaborator` | `docs:delete:collaborator` |
| `canvas_replace_range_of_blocks` | `docs:update:content` |
| `canvas_transfer_file_ownership` | `docs:update:file_owner` |
| `canvas_update_block` | `docs:update:content` |
| `create_file_with_content` | `docs:write:import` |
| `get_file_content` | `docs:read:export` |

## Zoom Chat MCP Server

Endpoint: `https://mcp.zoom.us/mcp/chat/streamable`

| Tool | Required scope |
|---|---|
| `zoom_chat_channel_create` | `team_chat:write:user_channel` |
| `zoom_chat_channel_get_by_id` | `team_chat:read:channel` |
| `zoom_chat_channel_member_role_update` | `team_chat:update:channel_member_role` |
| `zoom_chat_channel_members_add` | `team_chat:write:members` |
| `zoom_chat_channel_members_list` | `team_chat:read:list_members` |
| `zoom_chat_channel_update` | `team_chat:update:user_channel` |
| `zoom_chat_channels_list` | `team_chat:read:list_user_channels` |
| `zoom_chat_channels_search` | `team_chat:read:list_user_channels` |
| `zoom_chat_contact_add` | `team_chat:write:contact_information` |
| `zoom_chat_contacts_get_by_id` | `team_chat:read:list_contacts` |
| `zoom_chat_contacts_search` | `team_chat:read:list_contacts` |
| `zoom_chat_files_search` | `team_chat:read:list_user_files` |
| `zoom_chat_message_get_by_id` | `team_chat:read:list_user_messages` |
| `zoom_chat_message_replies_list` | `team_chat:read:list_user_messages` |
| `zoom_chat_message_send` | `team_chat:write:user_message` |
| `zoom_chat_message_update` | `team_chat:update:user_message` |
| `zoom_chat_messages_fetch` | `team_chat:read:list_user_messages` |
| `zoom_chat_messages_filter` | `team_chat:read:list_user_messages` |
| `zoom_chat_messages_search` | `team_chat:read:list_user_messages` |
| `zoom_chat_sessions_recent_list` | `team_chat:read:list_user_sessions` |

## Zoom Tasks MCP Server

Endpoint: `https://mcp.zoom.us/mcp/tasks/streamable`

| Tool | Required scope |
|---|---|
| `add_comment` | `tasks:write:comment` |
| `add_tasks_assignees` | `tasks:write:assignees` |
| `add_tasks_collaborators` | `tasks:write:collaborators` |
| `bulk_create_task_steps` | `tasks:write:task` |
| `create_task` | `tasks:write:task` |
| `delete_task_comment` | `tasks:delete:comment` |
| `delete_task_steps` | `tasks:write:task` |
| `get_a_task_comments` | `tasks:read:comments` |
| `get_assignees_of_a_task` | `tasks:read:assignees` |
| `get_my_tasks` | `tasks:read:list_tasks` |
| `get_task_collaborators` | `tasks:read:list_collaborators` |
| `get_task_detail` | `tasks:read:task` |
| `get_task_step` | `tasks:read:task` |
| `list_task_steps` | `tasks:read:task` |
| `remove_task_assignee` | `tasks:delete:assignees` |
| `remove_task_collaborator` | `tasks:delete:collaborator` |
| `reorder_task_steps` | `tasks:write:task` |
| `trash_task` | `tasks:delete:trash_task` |
| `update_task` | `tasks:update:task` |
| `update_task_step` | `tasks:update:task` |

## Zoom Revenue Accelerator MCP Server

Endpoint: `https://mcp.zoom.us/mcp/revenue_accelerator/streamable`

| Tool | Required scope |
|---|---|
| `get_conversation_analysis` | `zra:read:conversation_analysis` |
| `get_conversation_comments` | `zra:read:list_conversation_comments` |
| `get_conversation_transcript` | `zra:read:conversations` |
| `get_customer_accounts` | `zra:read:crm_customer_contact` |
| `get_customer_contacts` | `zra:read:crm_customer_contact` |
| `get_deal_activities_v2` | `zra:read:list_deal_activities` |
| `get_deal_analysis` | `zra:read:deal` |
| `get_deal_detail_v2` | `zra:read:deal` |
| `get_deal_stages` | `zra:read:deal` |
| `get_manager_team_and_member` | `zra:read:team` |
| `get_scorecard_sessions` | `zra:read:conversation_scorecards` |
| `search_conversations` | `zra:read:list_conversations` |
| `search_deals` | `zra:read:list_deals` |
| `search_indicators` | `zra:read:indicator` |
| `search_internal_users` | `zra:read:user` |

## Zoom Whiteboard MCP Server

Endpoint: `https://mcp.zoom.us/mcp/whiteboard/streamable`

| Tool | Required scope |
|---|---|
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
