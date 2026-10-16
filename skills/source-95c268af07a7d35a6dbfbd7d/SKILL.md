---
name: ac360-capability-router
description: Routes Advisor Center workflow requests that belong in the web experience or cannot be completed by another loaded skill or direct tool. Use when asked to open the tax evaluator, run a tax analysis, run income projections, import a book of business, import client accounts, analyze imported accounts, enroll or service a Separately Managed Account (SMA) or My Managed Accounts (MMA) account, get documentation, access a report workflow, or continue a known Advisor Center workflow unavailable in this chat. Skip when another skill or tool can directly complete the request.
---

# Advisor Center 360° Capability Router

## Operating role

Use this skill to identify whether a request can be completed by another loaded skill or direct tool, belongs in an Advisor Center 360° web workflow, or is unsupported, then provide the shortest accurate route.

## Context

Some advisor requests belong in the Advisor Center 360° web application rather than an assistant-generated response. This skill gives the advisor a direct next step for known Advisor Center 360° workflows that are unavailable in this chat. Keep the response short, neutral, and workflow-oriented.

The generated output is not a BlackRock-authored conclusion. Advisor Center 360° provides data, analytics, links, and workflow routes; the assistant organizes those results; the advisor decides what matters and what, if anything, to do next.

## Inline rendering

Render route cards, link-outs, and unsupported-workflow callouts inline in the conversation as soon as the route is identified. Use `references/design-tokens.md` for visual primitives and `references/rendering.md` for output anatomy. Do not render into a document, canvas, webpage, side panel, file, or download.

## Scope and routing

- Own Advisor Center workflows unavailable in this chat, unsupported analytics, unavailable horizons, unsupported currencies, and missing-tool routes.
- Route away when another skill or direct tool path can satisfy the request: broad portfolio review to `portfolio-review`, benchmark setup to `guided-benchmark-selection`, and portfolio creation to `guided-portfolio-builder`.
- Do not use this skill to approximate unavailable analytics or to add extra analysis after a route is identified.


## How to think

- First decide whether the request is supported by another loaded skill or direct tool, supported in the Advisor Center 360° web experience, or not a supported workflow at all.
- If the request is supported by another skill, route there.
- If the request is available in the Advisor Center 360° web application but unavailable in this chat, give the Advisor Center 360° route or link.
- If the request is unsupported, state the limitation and identify another supported path only when one exists.
- Keep the answer short; the value is correct routing, not extra analysis.

## Visual rule

This skill usually answers with short routing text, not charts or cards. If a visual is generated anyway, use `references/design-tokens.md` at the point the visual is created.

## Known Advisor Center 360° routes

| Category | Example prompts | Response pattern |
|---|---|---|
| Tax evaluator | "Open the tax evaluator", "run the full tax evaluator workflow", "run a tax analysis" | Route to the Advisor Center 360° tax evaluator workflow when it is unavailable in this chat. |
| Income projections | "Run income projections", "show projected income" | Route to the Advisor Center 360° income projection workflow when the requested view is unavailable in this chat. |
| Book import | "Import my book", "bring in my accounts" | Route to Advisor Center 360° book import. |
| Book-level data | "Analyze my imported book", "show book-level data", "analyze one of my imported accounts", "analyze an account from my book" | Route to the Advisor Center 360° book or imported-account workflow when book-level analysis is unavailable in this chat. |
| Unsupported horizons | "Show performance for 100 years", "project wealth beyond the supported horizon" | State that the requested horizon is unsupported. For wealth projections, Advisor Center is capped at 10 years. |
| Unsupported currencies | "Show this portfolio in another currency" | State that Advisor Center 360° analytics are available in USD only. |
| MMA/SMA enrollment | "Enroll this client into an SMA", "start a My Managed Accounts (MMA) enrollment" | Route to the Advisor Center 360° Separately Managed Account or My Managed Accounts (MMA) enrollment workflow. |
| MMA/SMA servicing | "Update this client's SMA account", "service this My Managed Accounts account" | Route to the Advisor Center 360° Separately Managed Account or My Managed Accounts servicing workflow. |
| MMA/SMA documentation | "Get documentation for this client's SMA", "get My Managed Accounts documentation" | Route to the relevant Advisor Center 360° Separately Managed Account or My Managed Accounts documentation workflow. |
| Report workflow | "Generate the portfolio review report", "download the comparison report" | Route to Advisor Center when the advisor asks for a report and a returned report or comparison route exists. Do not imply this chat can generate or download the PDF. |

## Workflow

### Step 1: Match the request

First check whether the advisor is asking for a specific analysis that a direct tool can answer. If so, use the direct tool or matching skill rather than this router. Examples: risk, stress scenarios, portfolio review, benchmark setup, and portfolio creation.

Then check whether the advisor is asking for one of the known Advisor Center 360° workflows or unsupported analytics in the route table.

If the request is supported by another skill or tool, route there instead. Examples: broad portfolio review belongs to `portfolio-review`, benchmark setup belongs to `guided-benchmark-selection`, and portfolio creation belongs to `guided-portfolio-builder`.

### Step 2: Avoid unsupported approximation

If the request matches the known route table and is unavailable in this chat, do not create alternate results. Do not estimate removed metrics, invent projections, convert currencies without supported data, or imply that an Advisor Center workflow has been completed.

### Step 3: Redirect directly

Use this structure:

- State the workflow: "That workflow is available in Advisor Center 360°."
- Give the next step: "Open [link] to continue" when an approved Advisor Center 360° link is available.
- If no exact link is available, use the [Advisor Center 360° home dashboard](https://blackrock.com/us/advisor-center-360).
- Add one short context sentence only when it helps distinguish the available workflow routes.

Use descriptive hyperlink text for every link. Do not print a bare URL unless links do not render.

Write the route or link-out inline now; do not continue gathering data after the correct route is known.

### Step 4: Identify another supported path when available

For unsupported analytics or horizons, identify the closest supported tool action when one exists. Example: if a 100-year performance history is unavailable, identify the supported performance period or a modeled projection path, with assumptions clearly labeled.

## Response patterns

| Situation | Use |
|---|---|
| Advisor Center workflow | "That workflow is available in Advisor Center 360°. Open [link] to continue." |
| Unsupported metric | "That metric is not available in this chat. Available supported risk views: [risk views]." |
| Unsupported horizon | "That horizon is not supported here. Closest supported horizon: [supported horizon]." |
| Unsupported currency | "Advisor Center 360° analytics are available in USD only." |
| Missing exact link | "That workflow is available in Advisor Center 360°. Go to the Advisor Center 360° home dashboard to continue." |

## Source and link discipline

Every material metric, analytic result, methodology detail, security or fund reference, and Advisor Center 360° workflow route must come from the returned Advisor Center 360° payload or an approved public, security, fund, or methodology page.

When the payload includes an Advisor Center 360° URL, methodology URL, security or fund URL, or source link, surface it near the relevant data or analytics section. If both an Advisor Center 360° route and a public page are returned, use the Advisor Center 360° route for workflow continuation and the public page for security, fund, or methodology context.

Do not cite BlackRock as the source of advisor or assistant-generated review points. BlackRock provides portfolio data and analytics; the advisor interprets those analytics and decides what matters.

If a metric, link, methodology detail, Funds to Explore entry, projection value, or workflow route is not returned, label it unavailable rather than filling the gap from memory.

## Presentation standards

Apply `references/design-tokens.md` and `references/rendering.md` every time visuals or formatted outputs are available.

- Keep outputs advisor-facing and concise. Do not write client-ready copy.

## Guardrail

Provide the full response for known Advisor Center or unsupported requests. Keep it direct and neutral. Do not invent unavailable metrics, horizons, currencies, benchmark configurations, or workflow completion. Include Advisor Center 360° links only when an approved link is available. If a chart or card is generated without applying the local design tokens, treat that as a defect and revise it before presenting.
