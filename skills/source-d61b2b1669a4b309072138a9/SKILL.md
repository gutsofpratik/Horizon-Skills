---
name: chronograph-commitment-pacing-planner
description: Plan forward fund commitments to reach and hold a target private capital allocation,
  using Chronograph portfolio data and a cashflow-projection model.
when_to_use: "Use when an LP wants to build or stress-test a commitment pacing plan — how much to
  commit per year, by strategy or vintage, to hit a target allocation or keep exposure steady.
  Triggers: \"how much should we commit next year\", \"build a pacing plan\", \"what pace keeps us
  at X% private markets\", \"model our vintage diversification\". Not for forecasting an existing
  portfolio's runoff alone (use chronograph-cashflow-forecast)."
---

# Commitment Pacing Planner

**Requirements:** A connected Chronograph MCP server as an LP client for the existing-portfolio baseline. Pure forward planning (no existing portfolio) can run from user-provided assumptions, with every figure labeled a planning assumption.

## Overview
Build a forward commitment plan that moves an LP toward — and holds — a target private capital allocation. The planner projects how new commitments translate into calls, distributions, NAV, and unfunded over time, layered on the existing portfolio's runoff, so the LP can see the commitment pace required to reach a target exposure and hold it through the J-curve.

## Shared infrastructure
This skill reuses the projection engine and baseline data path of `chronograph-cashflow-forecast` (entity resolution → fund metadata → net LP performance, plus the Takahashi-Alexander–style assumptions). It adds the target-seeking and vintage/strategy-diversification layer on top.

## Workflow
1. Clarify the objective: target allocation (% of total assets, or a target NAV/exposure level), planning horizon, strategy mix, and whether the LP has a fixed annual budget or wants the plan solved to hit the target.
2. Establish the baseline — pull existing commitments, NAV, unfunded, called, distributed, and net performance from Chronograph and project their runoff.
3. Resolve assumptions per strategy (contribution pace, bow/distribution curve, life, growth) from the shared methodology unless the LP provides custom ones.
4. Solve the schedule: the annual commitment (by strategy/vintage) that brings projected exposure to the target and holds it, respecting any budget constraint.
5. Project the combined path — calls, distributions, net cashflow, NAV, unfunded, exposure — separating existing-portfolio runoff from new-commitment contribution.
6. Present the plan: target line, commitment schedule, exposure path, vintage/strategy diversification, and the assumptions that drive it.

## Modes
- **Target-seeking** — solve for the pace that reaches/maintains the target.
- **Fixed-budget** — take the LP's budget as given; show the resulting exposure path vs. target.
- **Diversification overlay** — spread commitments across strategies/vintages to smooth concentration and the J-curve.

## Chronograph MCP usage
Inspect live tool descriptions; do not hard-code tool names. Use entity resolution → fund metadata → net LP performance for the baseline (same as the cashflow skill). Surface as-of date and currency (never default to USD), and label values net.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Always show the target, the commitment schedule, and the assumption table together.
- Separate existing-portfolio runoff from new-commitment projections; label actuals `A`, estimates `E`.
- Include a diversification view (commitments and exposure by vintage and strategy).
- On request, build an Excel workbook: Inputs, Commitment Schedule, Combined Projection, Exposure vs Target, Checks.
- Forecasts are scenario estimates under stated assumptions, not predictions.

## Guardrails

- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
- Draft analyst work product for pacing/liquidity planning — not investment, legal, tax, or actuarial advice.
- A commitment pace is what the model implies under stated assumptions, not a recommendation to commit.
- Planned commitments and their projected cashflows are user/model assumptions, never Chronograph actuals.
- If the Chronograph connector is not available, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.
