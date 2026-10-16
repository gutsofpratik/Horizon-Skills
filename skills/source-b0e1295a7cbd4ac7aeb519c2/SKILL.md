---
name: chronograph-tvpi-attribution-by-company
description: Decompose a fund's total value / TVPI into per-company contributions, split realized
  vs. unrealized, and rank top contributors and detractors — using Chronograph investment metrics.
when_to_use: "Use when explaining where a fund's value and performance come from. Triggers:
  \"attribution by company\", \"which companies drive our TVPI/MOIC\", \"top contributors and
  detractors\", \"realized vs unrealized by company\", \"where is the value concentrated\". For
  period valuation moves use chronograph-markup-markdown-brief."
---

# TVPI Attribution by Company

**Requirements:** A connected Chronograph MCP server as a GP client, with per-investment invested / realized / unrealized values.

## Overview
Decompose a fund's total value into per-company contributions and show how each company contributes to TVPI (total value ÷ paid-in), split into realized and unrealized. Rank contributors and detractors and show how concentrated value is — answering "what is actually driving the fund."

## Chronograph MCP usage
Use the **`investment-metrics`** tool for per-investment invested capital, realized proceeds, and unrealized value (gross), for the as-of period. Use fund-level metrics for the fund's total paid-in (the TVPI denominator) and entity resolution to scope. A portfolio company may be held through **multiple investments** — aggregate investment-level values to the company level for company attribution. Never default currency to USD; display `—` where unavailable.

## Workflow
1. Resolve the fund (or portfolio) and the as-of period.
2. Pull per-investment invested, realized, and unrealized (gross) from `investment-metrics`. Pull the fund's total paid-in for the TVPI denominator.
3. Aggregate investments to companies (a company may have multiple investments); compute each company's total value (realized + unrealized) and its contribution to fund TVPI; decompose into realized and unrealized components.
4. Rank companies by contribution; identify top contributors and detractors and the concentration of value (e.g. share from the top 5).
5. Optionally compute period-over-period movement in each company's contribution.
6. Present an attribution table or value waterfall with the realized/unrealized split and a concentration summary.

## Method notes
- This is a **gross, company-level** attribution. The bridge from gross company value to the fund's **net** TVPI (fees, carry, fund expenses, leverage) is out of scope — state that the attribution is gross and does not reconcile to net without that bridge.
- Be explicit about the paid-in basis used for the denominator.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Lead with top contributors and detractors and the value-concentration headline.
- Table: company, invested, realized, unrealized, total value, contribution to TVPI, realized/unrealized split.
- State as-of date, currency, gross basis, and the gross-to-net caveat.

## Guardrails

- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
- Draft analyst work product for performance attribution — not investment advice.
- Keep the math transparent and label every source; never fabricate investment- or company-level values.
- If the Chronograph connector is not available, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.
