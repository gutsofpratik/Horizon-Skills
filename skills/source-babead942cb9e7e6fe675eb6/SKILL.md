---
name: aiven-getting-started
description: "This skill should be used when: (1) the user mentions Aiven, asks about databases, Kafka, streaming, or managed services, and the Aiven MCP tools are unavailable or unauthenticated; (2) the user asks to \"get started with Aiven\", \"set up Aiven\", \"I'm new to Aiven\", \"how to start using Aiven\", \"connect my Aiven account\", \"use Aiven\", \"try Aiven\", \"sign up for Aiven\", or \"create an Aiven account\"; (3) any Aiven tool call fails due to authentication or connection issues. Handles authentication and onboarding so the user can start using Aiven services."
---

# Aiven Authentication & Onboarding

This skill ensures the user is authenticated with Aiven before any operation can proceed. It runs as a multi-turn conversation — each step ends by waiting for a user reply before continuing.

All Aiven tools live on the **plugin:aiven:aiven** MCP server.

## Entry points

This skill triggers in two situations — the flow differs slightly:

**The user asked to get started** — this includes direct skill invocation (e.g. `/aiven:aiven-getting-started`) as well as natural language like "how do I set up Aiven", "I'm new to Aiven", "how to start using Aiven", "connect my account".
→ Follow the full onboarding flow starting at Step 1. You MUST reach Step 2 (the Welcome message) if Step 1 fails — never stop at Step 1 with troubleshooting advice.

**An Aiven MCP tool call failed** (authentication error, tools unavailable, or the user asked to perform an Aiven action but the tools aren't connected)
→ The user has a task in progress. Acknowledge what they asked for, then run the onboarding flow to unblock it. After authentication succeeds, resume their original request — pick up where the tool call failed rather than asking "what would you like to do?"

## Step 1: Check authentication

Try to call `aiven_project_list` on server `plugin:aiven:aiven` with no parameters. This is the fastest way to check if the user is already connected.

**Success** → If the user had a pending task (e.g., "create a pg service"), resume that task now by calling the appropriate Aiven tools. If there was no pending task, say:

> Your Aiven account is connected! You have access to [N] projects. Here's what I can help you with:
> - **Build and deploy an application** on top of your data services (PostgreSQL, Kafka, and more)
> - **Explore your existing services** and data
> - **Create new data services** or manage existing ones
>
> What would you like to do?

Then wait for the user's reply.

**Failure (any kind)** → Whether the call returns an auth error, the tools aren't available, the MCP server isn't connected, or the call fails for any other reason — move to Step 2 silently. Do NOT try to troubleshoot the MCP connection or give auth instructions yet. Just proceed to Step 2.

## Step 2: Ask about existing account

The user might be brand new to Aiven or might already have an account. Ask first so the response is relevant:

> **Welcome to Aiven** — Easily deploy managed databases, streaming, and apps, such as: PostgreSQL, Kafka, OpenSearch, and more.
>
> Do you already have an Aiven account?

Wait for the user's reply — the next step depends on their answer.

## Step 3: Guide based on answer

**User has an account** → Connect it:

> Let's connect your account.

Then give auth instructions for their IDE:
- **Cursor**: Go to Settings → Tools & MCP, find the "aiven" Plugin MCP Server, and click authenticate.
- **Claude Code**: Run `/plugin`, go to Installed, select "aiven MCP", and press Enter to auth.

Then:

> Once you've authenticated, just send me a message and I'll verify the connection.

Wait for the user's reply.

**User needs a new account** → Show the signup link first, then what's included:

> No problem! You can create your free account here — no credit card needed:
>
> → https://console.aiven.io/signup
>
> Here's what you get for free:
>
> - **PostgreSQL** or **MySQL** — 1 GB storage, 1 GB RAM, 20 connections
> - **Apache Kafka** — 250 kb/s throughput, 3-day retention, 5 topics
> - **OpenSearch** — 20 GB storage, 4 GB RAM, 20 shards
> - **Valkey** — 1 GB RAM
>
> You also get **$300 in free trial credits** to try any service at full scale for 30 days.
>
> After you've created your account and verified your email, just send me a message and I'll help you connect the plugin.

Wait for the user's reply.

**User declines** →

> No worries! Whenever you're ready, just ask me to help you get started with Aiven.

## Step 4: Verify connection

When the user replies after authenticating, call `aiven_project_list` to verify the connection — just check directly rather than asking if they've finished.

If it works and the user had a pending task, resume it now — call the appropriate Aiven tools to fulfill the original request. Otherwise, say:

> You're connected to Aiven! Here are some things I can help you with:
> - **Build and deploy an app** — with managed databases and streaming, up and running in minutes
> - **Create free-tier services** — PostgreSQL, MySQL, Kafka, OpenSearch, Valkey, and more
>
> What would you like to do?

## Guidelines

- Keep the conversation friendly and low-pressure. The free tier requires no credit card.
- Always verify authentication by calling `aiven_project_list` — it's the source of truth.
- Each step waits for a user reply before continuing. This keeps the conversation natural and avoids overwhelming the user with information they didn't ask for.
