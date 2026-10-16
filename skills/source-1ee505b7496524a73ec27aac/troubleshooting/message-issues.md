# Message Issues

## Messages Not Sending

- Confirm you're using the correct API:
  - Team Chat API uses user OAuth token
  - Chatbot API uses a `grant_type=client_credentials` token + `robot_jid`
- Include `robot_jid`, `to_jid`, `user_jid`, and `account_id` in every chatbot message payload.
- Inspect the outbound API response status and body; a webhook HTTP 200 only acknowledges receipt.

## Card Not Rendering

- Validate the card JSON payload against known-good examples.
- Simplify to a minimal card and add components incrementally.
