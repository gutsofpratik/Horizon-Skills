---
name: zoom-mcp/team-chat
description: |
  Zoom Chat MCP server guidance. Use for Chat MCP endpoints, OAuth scopes, and tool
  workflows such as sending or editing messages, creating or updating channels, searching
  files, listing sessions, adding members, and sending contact invitations. The folder name
  remains `team-chat` for compatibility with existing links.
user-invocable: false
triggers:
  - "team chat mcp"
  - "zoom chat mcp"
  - "zoom team chat mcp"
  - "send zoom chat via mcp"
  - "edit zoom chat message mcp"
  - "create zoom chat channel mcp"
  - "add zoom chat channel members mcp"
  - "zoom_chat_message_send"
  - "zoom_chat_channel_create"
---

# Zoom MCP Chat

Dedicated guidance for Zoom's Chat MCP server. Zoom renamed Team Chat to Chat; the folder and
trigger names remain compatible with existing plugin references.

Use this MCP surface for agent-driven Team Chat actions. Use
[../../team-chat/SKILL.md](../../team-chat/SKILL.md) when the user needs deterministic REST
API implementation, custom backend retries, webhooks, reporting, or a production integration
that should not depend on agent tool invocation.

## Endpoints

| Transport | URL |
|-----------|-----|
| Streamable HTTP (recommended) | `https://mcp.zoom.us/mcp/chat/streamable` |

This plugin registers the Chat MCP surface in [../../../.mcp.json](../../../.mcp.json). Set
`ZOOM_CHAT_MCP_ACCESS_TOKEN` before enabling the plugin when a workflow needs Chat MCP tools.

## Authentication

- OAuth bearer tokens are passed through the MCP `Authorization` header.
- Start app registration from the
  [Chat MCP template](../../rest-api/assets/marketplace-apps/marketplace-manifest-template-for-mcp-team-chat.json).
- Use the server's OAuth protected-resource metadata to confirm the current scope advertisement.
- The server is scoped to the caller's account and subject to Chat policy restrictions.
- End-to-end encrypted, archived, retention-restricted, or policy-blocked chats may not be accessible or mutable through this surface.

## Required Scopes

Chat MCP scopes required by the current tools:

- `team_chat:read:channel`
- `team_chat:update:channel_member_role`
- `team_chat:write:members`
- `team_chat:read:list_members`
- `team_chat:update:user_channel`
- `team_chat:read:list_user_channels`
- `team_chat:read:list_contacts`
- `team_chat:read:list_user_files`
- `team_chat:read:list_user_messages`
- `team_chat:read:list_user_sessions`
- `team_chat:write:user_message`
- `team_chat:update:user_message`
- `team_chat:write:contact_information`
- `team_chat:write:user_channel`

## Safety Rules

This server contains read and write tools. Before invoking a write tool:

1. Confirm the user explicitly asked to send, edit, create, update, invite, or add members.
2. Resolve IDs carefully. `chat_session_id` may be a user/member ID, user email for 1:1 messages, or a channel ID.
3. Preview message/channel changes when the target or wording is ambiguous.
4. Do not guess channel IDs, message IDs, or invitee emails.
5. Prefer the REST Team Chat skill for bulk operations, durable retry logic, approval workflows, or audit-heavy production systems.

## Available Tools

The current Chat MCP tool surface is:

- `zoom_chat_channel_create`
- `zoom_chat_channel_get_by_id`
- `zoom_chat_channel_member_role_update`
- `zoom_chat_channel_members_add`
- `zoom_chat_channel_members_list`
- `zoom_chat_channel_update`
- `zoom_chat_channels_list`
- `zoom_chat_channels_search`
- `zoom_chat_contact_add`
- `zoom_chat_contacts_get_by_id`
- `zoom_chat_contacts_search`
- `zoom_chat_files_search`
- `zoom_chat_message_get_by_id`
- `zoom_chat_message_replies_list`
- `zoom_chat_message_send`
- `zoom_chat_message_update`
- `zoom_chat_messages_fetch`
- `zoom_chat_messages_filter`
- `zoom_chat_messages_search`
- `zoom_chat_sessions_recent_list`

Some MCP clients namespace server tools in the UI. Treat the raw tool names above as
authoritative after `tools/list`.

Reference: [references/tools.md](references/tools.md)

## Common Workflows

**Send a message:**

```text
zoom_chat_message_send
  chat_session_id: "CHANNEL_ID_OR_USER_ID_OR_EMAIL"
  message_content: "Deployment starts at 17:00 UTC."
  message_format: "text"
```

**Send a threaded reply:**

```text
zoom_chat_message_send
  chat_session_id: "CHANNEL_ID"
  parent_message_id: "PARENT_MESSAGE_ID"
  message_content: "Confirmed. I will post the follow-up here."
  message_format: "text"
```

**Edit a message sent by the caller:**

```text
zoom_chat_message_update
  chat_session_id: "CHANNEL_ID_OR_USER_ID"
  messageId: "MESSAGE_ID"
  message_content: "Updated status: deployment completed."
  message_format: "text"
```

**Create a channel:**

```text
zoom_chat_channel_create
  channel_name: "incident-response"
  channel_type: "private_channel"
  post_message_permission: "everyone"
  mention_all_permission: "channel_owner_and_admin"
  new_members_can_see_previous_messages_and_files: true
```

**Add members to a channel:**

```text
zoom_chat_channel_members_add
  channelId: "CHANNEL_ID"
  user_email_list:
    - "person@example.com"
```

## Chaining

- Parent MCP skill: [../SKILL.md](../SKILL.md)
- Deterministic Team Chat API skill: [../../team-chat/SKILL.md](../../team-chat/SKILL.md)
- OAuth guidance: [../concepts/oauth-setup.md](../concepts/oauth-setup.md)
- General routing: [../../general/SKILL.md](../../general/SKILL.md)

## References

- [references/tools.md](references/tools.md) - Chat MCP tool catalog, parameters, scopes, and constraints.
- Zoom docs: https://developers.zoom.us/docs/mcp/zoom-chat-mcp-server/
