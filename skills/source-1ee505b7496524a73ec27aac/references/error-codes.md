# Error Codes (Common Patterns)

## Auth Errors

- `Invalid access token`
  - wrong token type (bot token used for user API, or vice versa)
  - missing scopes
  - token expired / revoked
- `401` with code `7010` (`Invalid authorization token`)
  - development token sent to the production API, or production token sent to the development API
  - Bot JID belongs to a different environment than the token
  - Client ID, Client Secret, Account ID, or Bot JID belongs to a different Marketplace app

## Webhook Errors

- No events received:
  - endpoint not reachable publicly
  - verification failing
  - wrong event subscription / wrong app/account

## Message Rendering Issues

- Card not rendering:
  - invalid JSON payload
  - unsupported component types
- Webhook returns `200` but no message appears:
  - webhook `200` only confirms event receipt
  - inspect the outbound `/v2/im/chat/messages` status and response body
  - confirm `user_jid` came from the incoming event or configured target context
