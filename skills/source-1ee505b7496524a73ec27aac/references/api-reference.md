# API Reference Pointers

This doc is intentionally lightweight; prefer the official REST reference for the authoritative schema.

## Team Chat API (user-level)

- Send message: `POST /v2/chat/users/me/messages`
- Typical needs:
  - list channels
  - post to channel / DM
  - thread replies

## Chatbot API (bot-level)

- Send bot message: `POST /v2/im/chat/messages`
- Get the bearer token from `POST https://zoom.us/oauth/token` with
  `grant_type=client_credentials`.
- Do not use an authorization-code or user OAuth token for chatbot messages.
- Include `robot_jid`, `to_jid`, `user_jid`, and `account_id` in the request body.
- Treat the outbound response status and body as the message result; webhook HTTP 200 only
  confirms event receipt.

## Notes

- If you see "invalid access token" errors, check:
  - app type (General App OAuth vs others)
  - scopes
  - whether the user re-consented after scope changes
