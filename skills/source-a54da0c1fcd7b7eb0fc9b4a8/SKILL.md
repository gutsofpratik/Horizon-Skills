---
name: connect
description: Check the Wingspan connection and report who it is signed in as. Run this after installing the plugin or after re-authorizing, or whenever you want to confirm Claude is reading the right Wingspan account.
disable-model-invocation: true
---

# Check the Wingspan connection

Call `who_am_i`. It takes no arguments and performs a real authenticated read,
so a successful answer proves the whole connection works end to end.

Then report, in plain sentences:

- **Connected as** — the person's email address, when the connection
  identifies an individual. No name is returned. An authorization granted
  through the browser identifies the company account rather than the
  individual, and the person comes back unavailable; say that it identifies the
  account, and do not present it as a problem.
- **Reading as** — the account from `account` when present, otherwise the
  matching entry in `accounts`. `actingAsAccountId` is always null here,
  because `who_am_i` takes no `accountId`; ignore it.
- **Accounts reachable** — the entries in `accounts`, by name, noting any that
  sit under a parent account. Mention that a tool can be pointed at one of them
  with its `accountId` if the user needs a different one. An empty `accounts`
  list is legitimate, not a fault.

Then say what the connection is for in one line: these tools read the
contractors this account pays, what it owes them, and their onboarding
paperwork, and they can create contractor records and draft payments after
showing a preview. Paying, approving and anything requiring an extra identity
challenge stay in the Wingspan app.

## If it fails

Follow the `troubleshooting-connection` skill. In short: an authentication
failure means re-authorizing through `/mcp`; no Wingspan tools at all means the
server is not connected, and that skill says how to tell the two apart.
