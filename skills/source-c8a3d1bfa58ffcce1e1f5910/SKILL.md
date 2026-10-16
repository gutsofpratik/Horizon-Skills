---
name: wealth-projections
description: Explains modeled performance, projected wealth, methodology, advisory-fee treatment, and unsupported performance or projection requests. Use when asked to show modeled performance, project wealth, explain projection assumptions, check whether fees are included, or handle an unavailable horizon or configuration. Skip when the advisor asks for a broad portfolio review or only needs benchmark setup.
---

# Wealth Projections

## Operating role

Use this skill to organize returned Advisor Center 360° performance data, projection data, assumptions, links, and workflow routes so the advisor can review the modeled output.

## Context

Performance and projection outputs require clear labeling. Modeled performance from current holdings is not the client's realized track record. Wealth projections are modeled outcomes based on assumptions, not guarantees. Advisory-fee assumptions can affect interpretation, so make them visible every time this skill discusses modeled performance or projected wealth.

The generated output is not a BlackRock-authored conclusion. Advisor Center 360° provides data, analytics, links, methodology fields, and workflow routes; the assistant organizes those results; the advisor decides what matters and what, if anything, to do next.

## Inline rendering

Render modeled performance, projected wealth, assumptions, fee notes, and unsupported-configuration callouts inline in the conversation as soon as each supported output is returned. Use `references/design-tokens.md` for visual primitives and `references/rendering.md` for output anatomy. Do not render into a document, canvas, webpage, side panel, file, or download.

**Sequence — call, write, then call.** Write the first supported output with its fee and methodology note before adding follow-up methodology detail or routing an unsupported request.

```text
classify request → call supported performance/projection path
write chart + fee/methodology note
advisor asks for more detail → write methodology or route unsupported request
```

## Scope and routing

- Own modeled performance, projected wealth, methodology explanation, fee-treatment explanation, and unsupported horizon or configuration handling.
- Route broad first-pass review requests to `portfolio-review`.
- Route benchmark choice/setup requests to `guided-benchmark-selection` before performance or projection analysis that needs a benchmark.
- Route Advisor Center workflows to `ac360-capability-router` when they are available in Advisor Center but not available in this chat.

## How to think

- Classify the request before using tools: simulated performance, realized history, projected wealth, methodology, fees, or unsupported configuration.
- Keep modeled, simulated, projected, and realized results distinct.
- Explain assumptions only from returned fields or approved methodology pages.
- Put fee treatment near the result it affects.
- Treat unsupported horizons, currencies, and configurations as routing issues, not calculation prompts.

## Visual rule

Every chart or card generated in this workflow must use local `references/design-tokens.md` at the point it is created. Do not use default chart-library or card palettes.

If the host cannot load the reference files, still use the richest inline visual form
first. Time-series and projection ranges render as charts when available; assumptions,
fees, and caveats render as compact cards or callouts when available. Markdown tables
are fallback only. Never show tool names, field names, ids, or missing-reference
commentary in the advisor-facing answer.

## Supported analysis paths

Use this table before later references to a "supported path." A supported path means one of these Advisor Center 360° tool or workflow routes is available for the advisor's request.

| Supported path | Use when | Tool or route | Do not use it for |
|---|---|---|---|
| Modeled performance | The advisor asks for simulated or modeled returns for the current portfolio. | `simulate_performance` or `compare_performance` when available. | Realized client account history or unsupported time periods. |
| Wealth projection | The advisor asks for projected wealth, outcome ranges, or modeled future values. | `project_wealth` when available. | Guarantees, forecasts, or horizons not returned by the tool. |
| Methodology and assumptions | The advisor asks how modeled performance or projections are calculated. | Returned methodology fields and approved methodology links. | Reconstructing formulas or assumptions not returned. |
| Advisory-fee treatment | The advisor asks whether fees are included or the result depends on fee settings. | Returned fee fields and visible configuration state. | Inferring gross/net treatment when the output does not say. |
| Advisor Center workflow | The advisor asks for a workflow available in Advisor Center but not available in this chat. | `ac360-capability-router`. | Creating an approximate calculation in place of the unavailable workflow. |
| Unsupported configuration | The advisor asks for an unavailable horizon (i.e. >10 years), currency, or configuration. | State the limitation clearly and identify the closest supported path when returned. | Inventing longer histories, currencies, or projection settings. |

## Route map

| Advisor request | Route | Required explanation |
|---|---|---|
| Modeled performance | Use the supported performance analysis path when available. | State whether results are modeled from current holdings and not realized client history. |
| Wealth projections or outcome ranges | Use the supported wealth projection path when available. | State that projections are modeled outcomes. Mention assumptions and BlackRock capital market assumptions when relevant. |
| Methodology or assumptions | Explain the methodology fields returned by the tool or route to the methodology page when available. | Include methodology links only when approved links are available. |
| Advisory-fee questions | Explain whether advisory fees are included, excluded, visible, or configurable in the output. | If fees affect net outcomes, show the fee treatment near the affected values. |
| Unsupported horizon, currency, or configuration | State the limitation and identify the closest available supported path. | Do not invent longer histories, projections, currencies, or configurations. |
| Advisor Center 360° workflow unavailable in this chat | Hand off to `ac360-capability-router`. | Use neutral Advisor Center 360° routing language. |

## Workflow

### Step 1: Classify the request

Decide whether the advisor wants modeled performance, wealth projection, methodology, fee assumptions, an unsupported horizon/configuration, or an Advisor Center 360° workflow unavailable in this chat.

If the request is a broad portfolio review, use `portfolio-review` instead. If the request is only benchmark setup, use `guided-benchmark-selection` instead. If the request is known as unavailable in this chat or unsupported across Advisor Center 360° workflows, use `ac360-capability-router`.

### Step 2: Use the supported analysis path

For supported modeled performance or wealth projection requests, choose the path before calling:

- Use `simulate_performance` for one saved portfolio's historical simulation or modeled performance.
- Use `compare_performance` for two to five saved subjects or a portfolio-and-benchmark performance comparison.
- Use `project_wealth` for future value, projected wealth, or outcome ranges. Advisor Center wealth projections are capped at 10 years.
- Use `guided-benchmark-selection` first when the advisor asks for a comparison but the benchmark subject is missing or ambiguous.

Use only returned fields. Do not fill in missing returns, confidence ranges, historical windows, or projected values from memory.

Write the supported output inline before making any follow-up methodology, fee, or routing call.

### Step 3: State fee assumptions every time

Whenever the response discusses modeled performance or wealth projections, include a short fee note:

- Whether advisory fees are included, excluded, configurable, or not visible in the returned output.
- Whether the values are gross or net when the tool result provides that detail.
- Whether fee settings are visible before any net outcomes are reused outside the analysis.

If the returned data does not specify fee treatment, say that fee treatment is not visible in the current output.

Advisory fee is configurable and, once set to a non-zero rate, persists across analyses. A zero-fee setting applies only to the analysis in which it was set. Because of this, confirm the active fee rate each time you report modeled performance or projected wealth, and state the rate applied.

### Step 4: Clarify modeled performance

For modeled performance, state that the result is modeled from current holdings and assumptions. Do not present it as the client's realized historical return.

Use comparison language. Say "modeled performance" or "historical simulation" when those terms match the tool output.

### Step 5: Clarify wealth projections

For projected wealth outcomes, state that the result is modeled and depends on assumptions, inputs, and market scenarios. Reference BlackRock capital market assumptions when relevant. Include approved methodology links when they are available.

If the methodology link is unavailable, summarize only the methodology fields returned by the tool and say that no methodology link is available in the current response.

### Step 6: Handle unsupported requests

For unsupported horizons or configurations, state the limitation plainly and identify the closest available supported path. Examples:

| Unsupported ask | Response shape |
|---|---|
| Performance for 100 years | State that Advisor Center 360° supports up to 10 years for this analysis. Identify the supported 10-year window or a modeled projection path when available. |
| Wealth projection beyond 10 years | State that Advisor Center 360° wealth projections are capped at 10 years. Identify the 10-year projection path when available. |
| Unsupported currency | State that Advisor Center 360° analytics are available in USD only. |

## Output shape

Use visuals when the interface supports them:

- Use a line chart for time-series performance or projected wealth paths, using the local design tokens before presenting.
- Use a fan chart or range chart for projection ranges when returned, using the local design tokens before presenting.
- Use a table for assumptions, fees, time horizon, and methodology notes.
- Use a short callout or card for the key caveat. If using a card, apply the local design tokens before presenting.

Keep the explanation brief. Show what the numbers mean, what assumptions affect them, and which supported paths are available next.

## Source and link discipline

Every material metric, analytic result, methodology detail, security or fund reference, and Advisor Center 360° workflow route must come from the returned Advisor Center 360° payload or an approved public, security, fund, or methodology page.

When the payload includes an Advisor Center 360° URL, methodology URL, security or fund URL, or source link, surface it near the relevant data or analytics section. If both an Advisor Center 360° route and a public page are returned, use the Advisor Center 360° route for workflow continuation and the public page for security, fund, or methodology context.

Do not cite BlackRock as the source of advisor or assistant-generated review points. BlackRock provides portfolio data and analytics; the advisor interprets those analytics and decides what matters.

If a metric, link, methodology detail, Funds to Explore entry, projection value, or workflow route is not returned, label it unavailable rather than filling the gap from memory.

## Presentation standards

Apply `references/design-tokens.md` and `references/rendering.md` every time visuals or formatted outputs are available.

- Keep outputs advisor-facing and concise. Do not write client-ready copy.

## Guardrail

Do not present modeled results as realized returns. Do not call wealth projections forecasts or guarantees. Do not invent unsupported horizons, currencies, methodology links, fee treatment, confidence bands, or historical performance. Include advisory-fee assumptions every time modeled performance or wealth projections are discussed. If a chart or card is generated without applying the local design tokens, treat that as a defect and revise it before presenting. Use approved methodology links only when available, and route known Advisor Center 360° workflows unavailable in this chat through `ac360-capability-router`.
