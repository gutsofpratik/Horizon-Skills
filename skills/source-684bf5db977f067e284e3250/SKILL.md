---
name: data-informed-planning
description: Use when planning a product feature, fix, or prioritization task where Pendo usage data, signals, issues, or customer feedback could ground the plan in real product behavior — e.g. "plan a fix for the pricing-page dropoff", "what should I build next", "improve the welcome flow". Skip for pure code refactors, infra, or tooling work.
---

# Data-Informed Planning

## Overview

A composition layer over `/superpowers:writing-plans`. Gathers relevant Novus + Pendo MCP data first, then hands the planner a "Data Context" block so the resulting plan is grounded in real usage, not assumptions.

**Core principle:** Don't reinvent planning. Inject product reality into the planner that already exists.

## Prerequisites

This skill requires both MCP servers that ship with the `pendo-analytics` plugin:

- **Novus MCP** (server name `novus`) — artifact graph, signals, issues, product wiki, opinionated metrics
- **Pendo MCP** (server name `pendo-external`) — Voice of Customer, NPS, PES, session replays, segments/accounts, visitor data, entity discovery

Both are auto-configured when the plugin is installed. Run `/mcp` once to authenticate each.

The skill delegates to the `superpowers:writing-plans` skill when available. Install the `superpowers` plugin alongside this one for best results. If `superpowers` is not installed, the skill will produce the plan directly using the gathered Data Context instead of delegating.

## Step 0: Precheck (REQUIRED before classifying)

Verify both MCPs are reachable with cheap calls:

- `get_pendo_apps` (Novus) — confirms Novus auth
- `list_all_applications` (Pendo) — confirms Pendo auth

If either fails:
- Tell the user which MCP is unreachable and how to fix it (run `/mcp`)
- Offer to proceed with whichever MCPs are available, **clearly noting the gap** in the Data Context Caveats
- Do NOT silently skip — the planner needs to know what data wasn't available

Also check whether `/superpowers:writing-plans` is available. If not, note it and plan to use the fallback in Step 4.

## When to Use

Use when:
- The request touches user-facing product behavior (feature, UX, fix, launch, deprecation)
- The request asks "what should I work on" / "what's broken" / "where should I focus"
- The request names a page, feature, funnel, journey, or guide
- The user wants a plan but hasn't told you which data should inform it

Do NOT use when:
- Task is a pure code refactor with no user-visible change
- Task is infra / build / CI / tooling / docs
- User already supplied the relevant data inline

If unsure, run the classifier (Step 1). If it returns `gather: false`, fall through to `/superpowers:writing-plans` directly.

## Workflow

0. **Precheck** — confirm both Novus and Pendo MCPs are reachable
1. **Classify intent** — decide whether to gather data, and which tools to call (see `classifier.md`)
2. **Gather** — call the selected MCP tools **in parallel** (single message, multiple tool uses)
3. **Summarize** — produce a Data Context block (≤ 250 words + artifact IDs)
4. **Delegate** — invoke `/superpowers:writing-plans` with `<original request> + Data Context`
5. **Stop** — let the planner own the plan. Do not double-plan.

## Step 1: Intent Classifier

See `classifier.md` (alongside this file). Output shape:

```json
{
  "intent": "feature | fix | prioritization | diagnosis | funnel-journey | non-product",
  "gather": true,
  "novus_tools": ["get_product_wiki", "list_signals"],
  "pendo_tools": ["get_feedback_insights"],
  "scope": { "appId": "...", "artifactId": "...", "name": "..." }
}
```

Tool names are bare — matching the convention used by the other skills in this plugin. The source split (`novus_tools` / `pendo_tools`) exists for the precheck and the "prefer Novus when overlap" rule, not disambiguation; tool names don't collide between the two MCPs.

If `gather: false` → stop and call `/superpowers:writing-plans` directly.

## Step 2: Gather

Call the selected MCP tools in parallel. Rules:

- **Always include `get_product_wiki`** (Novus) for `feature` intent — gives the planner product structure
- **Prefer Novus over Pendo when both expose similar data** — Novus responses are pre-processed and tied to the artifact graph the planner can reference. Reach for raw Pendo only when you need a slice Novus doesn't expose (segment/account breakdowns, VoC, sentiment, raw visitor queries)
- **Funnel and journey analysis live only in Novus** — there is no Pendo MCP equivalent
- If a tool returns empty, errors, or fails a product-line check (e.g. NPS, Session Replay, Agent Analytics not in subscription), note it in Caveats and move on — don't retry

## Step 3: Data Context Block

Target ≤ 250 words. Use this template:

```markdown
## Data Context (Novus + Pendo MCP — fetched <ISO timestamp>)

**Product:** <productName>  ·  **Scope:** <page / feature / funnel + id, or "app-wide">

**Relevant signals (N):**
- <title> — <priority> · <one-line takeaway> · `<id>`

**Relevant issues (N):**
- <title> — <one-line takeaway> · `<id>`

**Voice of customer (N items):**
- <theme> — <count> mentions · <sample quote or sentiment> · `<feedback-id>`

**Engagement / sentiment:**
- PES: <score> (<window>)  ·  NPS: <score> (<window>)
- <metric>: <value>

**Caveats:**
- <e.g. "tagging is misconfigured — page/feature metrics unreliable; see signal b7d4…">
- <e.g. "Pendo MCP unreachable; VoC + PES not included">
- <e.g. "NPS tool gated — subscription doesn't include NPS product line">
```

Always populate **Caveats** when:
- A `list_signals` result surfaces a data-quality issue (broken tagging, stale metrics)
- An MCP was unreachable in the precheck
- A product-line gate blocked a tool
- A tool returned empty when you'd expect data

The planner must know when not to trust the numbers.

## Step 4: Delegate

If `/superpowers:writing-plans` is available, delegate:

```
/superpowers:writing-plans

<original user request>

---

<Data Context block>
```

The planner writes the plan. This skill ends here.

**Fallback (superpowers not installed):** If the `superpowers` plugin is not available, write the plan directly. Use the Data Context block to ground your plan in the gathered data. Structure the plan with: goal, key findings from the data, prioritized action items, success metrics, and risks/caveats. Keep the same data-driven rigor — the only difference is you're writing the plan yourself instead of delegating.

## Quick Reference

Tool names are bare. Prefer Novus for overlapping data; pull Pendo for VoC, sentiment, segment/account slicing, or session-level diagnostics.

| Intent | Novus tools | Pendo tools | Must-include |
|---|---|---|---|
| feature | `get_product_wiki`, `list_signals`, `get_related_artifacts` | `get_feedback_insights`, `get_ideas`, `productEngagementScore` | wiki + (insights OR ideas) |
| fix | `list_issues`, `list_signals`, `get_page_metrics`/`get_feature_metrics` | `sessionReplayList`, `devlogEvents`, `visitorQuery` | issues |
| prioritization | `list_signals`, `list_issues`, `get_headline_metrics` | `get_feedback_insights`, `productEngagementScore`, `npsScore` | signals + issues + insights |
| diagnosis | `get_page_metrics`, `get_feature_metrics`, `get_funnel_analysis`, `list_signals` | `sessionReplayList`, `visitorQuery`, `segmentList` | metrics + signals |
| funnel-journey | `get_funnel_analysis`, `get_journey_analysis`, `get_related_artifacts` | (none — Novus owns funnel/journey) | funnel/journey analysis |
| non-product | (none) | (none) | — bail to planner |

## Common Mistakes

- **Skipping the precheck** — silent MCP failure = silently bad plans. Run Step 0.
- **Double-planning** — writing a plan yourself after gathering. STOP, hand off.
- **Sequential MCP calls** — always parallel; latency compounds.
- **Pulling raw Pendo when Novus has it** — Novus responses are linked to artifacts the planner can reference. Pendo raw is for breakdowns Novus doesn't cover.
- **Retrying gated tools** — if NPS / Session Replay / Agent Analytics tools return product-line errors, the subscription doesn't include them. Note in Caveats and move on.
- **Ignoring data quality** — surface tagging warnings, missing-MCP warnings, and product-line gates in Caveats.
- **Over-gathering** — stick to the classifier's tool list; the planner doesn't need raw event dumps.
- **Skipping classifier on "obvious" requests** — "refactor the dashboard component" reads product-y but is code work; classifier correctly returns `non-product`.

## Red Flags — STOP

- About to call >6 MCP tools → over-gathering; narrow scope first
- About to write the plan yourself → call `/superpowers:writing-plans`
- Gathering when intent is `non-product` → classifier said skip
- Data Context >250 words → compress; link IDs, don't paste blobs
- Skipped precheck and one MCP is dead → output will mislead the planner; run Step 0
- A Novus tool name appears in `pendo_tools` (or vice versa) → swap to the correct array
