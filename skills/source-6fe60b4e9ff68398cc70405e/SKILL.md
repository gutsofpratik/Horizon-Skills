---
name: troubleshooting-connection
description: Diagnose Wingspan connection and permission problems. Use when a Wingspan tool returns an authentication or permission error, when the tools report nothing at all, when an answer looks like it came from the wrong company or the wrong account, or when someone asks "am I connected to Wingspan", "is my login still valid", "why can't Claude see my contractors", "why is this empty", "these are not my contractors".
---

# Troubleshooting the Wingspan connection

The Wingspan tools read one company's records, over a connection the user
authorized in their browser. When something looks wrong, the question is
almost always which account the tools are reading as, or whether the
authorization is still good.

## Run `who_am_i` first

`who_am_i` takes no arguments and is the only honest check that the connection
works, because it performs a real authenticated read. What it reports:

- The signed-in person's email address, and no name, when the connection
  identifies a person. An authorization granted through the browser identifies
  the company account rather than the individual, and in that case the person is
  reported as unavailable — that is expected, not a fault.
- `actingAsAccountId` — always null from `who_am_i`, because it takes no
  `accountId`; ignore it. The account the answers are about is `account`, which
  the browser authorization names, or the entry in `accounts` matching the
  signed-in person. Other tools read as a child account only when a call passes
  `accountId`.
- `accounts` — the accounts this connection can reach, with names and any
  parent account. An empty list is legitimate, not a fault.

Report what it says before theorising.

## Not authorized, or authorization expired

An authentication failure means the connection needs re-authorizing. In Claude
Code, run `/mcp`, pick the `wingspan` server, and complete the login in the
browser. Other Claude clients have the same step under their connector or MCP
settings.

Two things worth knowing so you can describe this accurately:

- Access is granted for a short window and then renewed automatically. This
  plugin asks for the permission that makes silent renewal possible, so a
  working connection normally stays working without anyone doing anything.
- If the renewal itself fails — the authorization was revoked, or the browser
  session is long gone — every tool starts failing at once. Re-authorizing
  through `/mcp` is the fix, not retrying the tool.

If a tool reports that the token was rejected, the message carries a request id
when Wingspan supplied one. Give that id to the user; it is the handle Wingspan
support needs to find the failure.

## The answers are for the wrong company

Two causes, and `who_am_i` distinguishes them.

**The connection is bound to a different account than the user expected.**
`account` names the account the authorization covers when the report carries
one; otherwise it is the entry in `accounts` matching the signed-in person.
`accounts` shows what else is reachable. A person who works with more than one
Wingspan account has to authorize the one they mean.

**The company is an organization with child accounts.** Nine of the ten
tools take an optional `accountId` that acts as one child account instead of the
default; `who_am_i` takes no arguments at all. Use `accountId` only when the user
names a specific child account, and take the id from `who_am_i`'s `accounts`
list. Do not guess an id, and do not sweep across children unasked.

## The answers are empty

Before concluding there is no data:

- `search_contractors` defaults to active contractors and excludes archived
  ones. A name search that finds nothing reports how many archived contractors
  do match; offer to look there.
- `search_payables` excludes cancelled payments unless asked for them.
- A contractor with no engagement assignment has no paperwork summary at all,
  so the tabs that filter on paperwork will not return them.
- These tools answer only for the company doing the paying. If the user wants
  to know what someone owes *them*, these tools cannot answer it, and their own
  Wingspan account is where to look.

The `finding-contractors` and `checking-payments` skills cover each of those in
more detail.

## What the error messages mean

| The tool says | What happened |
| --- | --- |
| Not found | No such record is visible to this account. A record belonging to a different account also reads as not found, on purpose. |
| Not a well-formed id | The id is the wrong shape. Use the id a search result carried, not one copied from elsewhere. |
| Invalid request | The arguments contradict each other. The message says which pair; fix it and call again. |
| The token was rejected | The authorization is no longer accepted. Re-authorize through `/mcp`. |

## When the tools are not there at all

If no Wingspan tools appear, the plugin is installed but its server is not
connected. Check `/mcp` for the `wingspan` entry and its status. If connecting
reports that the endpoint cannot be found, this account does not have Wingspan's
Claude connection turned on; the user's Wingspan account team can turn it on.

## Finish these in the Wingspan app

- Signing in, resetting a password, and anything to do with multi-factor
  authentication.
- Reviewing or revoking which applications have access to the account.
- Creating, rotating or deleting an API key, or managing a service account.
- Changing which accounts a person can reach, and their permissions.

Every one of those is protected by an extra identity challenge, which cannot be
completed in a conversation. There is no workaround to look for.
