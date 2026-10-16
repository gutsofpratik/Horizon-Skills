---
name: chronograph-markup-markdown-brief
description: Identify which portfolio companies were marked up or down this period, quantify each
  change, surface the stated basis, and rank by impact on fund NAV — using Chronograph investment
  metrics.
when_to_use: 'Use when reviewing valuation changes across a fund or portfolio for a period.
  Triggers: "what got marked up/down this quarter", "valuation changes", "biggest write-ups and
  write-downs", "what drove the NAV change", "markup brief". Useful for GP valuation review and IC
  prep; LP analysts can use it too. For a full per-company report use
  chronograph-portfolio-company-one-pager.'
---

# Markup / Markdown Brief

**Requirements:** A connected Chronograph MCP server as a GP client, with investment-level valuation data for the current and prior period.

## Overview
For a fund or portfolio over a chosen period, identify the holdings whose valuations moved, quantify each move in amount and percent, rank by impact on fund NAV, and surface the stated basis for the change where the data or commentary supports it. The brief sharpens a valuation review or IC discussion.

## Chronograph MCP usage
Use the **`investment-metrics`** tool for per-investment valuation and value data — carrying / equity value, unrealized value, and (where available) EV and the valuation multiple — for both the current and prior period. Use entity resolution to scope the fund/portfolio, and document/commentary retrieval for the stated rationale. A portfolio company may be held through **multiple investments** — aggregate investment-level marks to the company level when you report by company. Never default currency to USD; display `—` where unavailable.

## Workflow
1. Set scope (fund or portfolio) and the comparison periods (current vs. prior quarter by default).
2. Pull per-investment value for both periods from `investment-metrics` — carrying / equity value, unrealized value, plus EV and the valuation multiple where available.
3. Compute the change per investment, and roll up per company (a company may span multiple investments): absolute and percent, and the contribution to the fund's NAV change. Rank by absolute NAV impact.
4. Separate genuine value changes from cashflow effects — a position can move on follow-on investment or realization, not just re-marking. Flag which is which where the data allows.
5. Surface the stated basis where available: multiple expansion/compression, EBITDA/revenue change, a financing round, comp-set change, FX, or written commentary.
6. Present ranked markups and markdowns with drivers, NAV impact, and the period.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Lead with the largest NAV movers (up and down).
- Table: company (and investment where it adds clarity), prior value, current value, Δ amount, Δ %, NAV impact, stated basis, source.
- Distinguish re-mark from cashflow-driven changes.
- State as-of dates, currency, and gross vs. net basis.

## Guardrails

- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
- Draft analyst work product for valuation review — not investment, audit, or valuation advice.
- Report the basis from the data; do not infer a reason the materials do not support.
- Do not imply a missing rationale is misconduct; frame it as a question or follow-up.
- If the Chronograph connector is not available, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.
