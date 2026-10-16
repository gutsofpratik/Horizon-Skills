---
name: chronograph-budget-vs-actuals-variance
description: Compare portfolio company operating actuals against budget/plan, compute variances,
  flag off-plan companies, and roll up to the fund, using Chronograph company metrics.
when_to_use: 'Use when a GP value-creation or monitoring team is tracking operating performance
  against plan. Triggers: "budget vs actuals", "variance analysis", "which companies are off-plan",
  "how are portcos tracking vs budget", "performance vs plan". For valuation moves use
  chronograph-markup-markdown-brief; for a full company report use
  chronograph-portfolio-company-one-pager.'
---

# Budget vs. Actuals Variance

**Requirements:** A connected Chronograph MCP server as a GP client.

## Overview
Compare portfolio company operating results (revenue, EBITDA, and other tracked KPIs) against budget or plan for the same periods, compute the variance in amount and percent, flag companies tracking off-plan beyond a threshold, trend the variance over time, and roll up to the fund.

## Scenarios — how budget and actuals are distinguished
Company operating metrics are retrieved with the **`company-metrics`** tool, which exposes a **Scenario** field that separates budget/plan figures from actuals. **Scenario labels are client-specific** — a client may name them differently (e.g. "Budget", "Plan", "Forecast", "Actual") and may carry more than one budget scenario (original vs. revised, or multiple cases). Before computing any variance:

1. Query `company-metrics` to see which Scenario values exist for the company.
2. **Confirm with the user** which Scenario represents actuals and which represents the budget/plan to compare against (and which to ignore) — do not assume from the labels.
3. Apply the confirmed scenarios consistently across every company and period in the analysis.

## Workflow
1. Resolve scope: a single company, a set, or the whole fund; and the periods to compare.
2. Establish the Scenario mapping (above) — confirm the actuals and budget scenarios with the user.
3. Pull the tracked metrics (revenue, gross profit, EBITDA, and any KPIs in scope) from `company-metrics` for both the actuals and budget scenarios, same periods.
4. Compute variance per metric: actual − budget, and percent variance; label favorable/unfavorable.
5. Flag companies off-plan beyond a threshold (default ±10%, configurable); trend variance across periods to show whether gaps are widening or closing.
6. Roll up to the fund and present per-company variance with off-plan flags and a coverage note.

## Chronograph MCP usage
Use the `company-metrics` tool for operating metrics; prefer platform metric types over display labels (same discipline as the one-pager), and select the Scenario per the confirmed mapping. Make the metric-discovery call before querying. Never default currency to USD; display `—` where a value is unavailable.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Per-company variance table: metric, period, actual, budget, Δ amount, Δ %, favorable/unfavorable.
- State which Scenario values were used for actuals vs. budget.
- Off-plan flags and a fund roll-up, plus coverage (which companies had both scenarios available).

## Guardrails

- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
- Draft analyst work product for operating monitoring — not investment, audit, or valuation advice.
- Distinguish actuals from budget/plan; never present a plan-scenario figure as an actual.
- Never fabricate budget or actual values; if a company lacks a budget scenario, flag it rather than estimating.
- If the Chronograph connector is not available, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.
