---
name: chronograph-fund-quarterly-review-pack
description: Generate a consolidated quarterly review pack for a single fund — a fund-level summary
  plus a one-pager section for every portfolio company in the fund — using Chronograph data.
when_to_use: 'Use when a GP wants a full quarterly review of one fund covering all of its portfolio
  companies. Triggers: "build the Q[N] review pack for [fund]", "fund quarterly review", "one-pagers
  for the whole fund", "portfolio review for [fund]", "deck covering every portco in the fund". For
  a single company use chronograph-portfolio-company-one-pager; for LP-side analysis use the lp-
  skills.'
---

# Fund Quarterly Review Pack

**Requirements:** A connected Chronograph MCP server as a GP client. This pack needs GP-level data (company financials and gross per-investment returns); if the connection is an LP client, stop and tell the user the pack requires GP access rather than producing an empty pack.

## Overview
Produce one consolidated, consistently branded review for a single fund: a fund-level summary on top, then a per-company section for every portfolio company in the fund, plus what changed this quarter. This is the one-pager skill, fanned out across a fund's holdings, with a roll-up layer added.

## Company vs. investment nuance
A portfolio **company** may be held through **multiple investments** — across more than one fund, across rounds or tranches, or via different vehicles. Within a single fund a company can still map to more than one investment. When enumerating the fund's holdings, group investments by company so each company gets one section, and aggregate that company's investment-level figures (cost, value, returns) up to the company — while preserving the per-investment breakdown where it matters (e.g. the returns table). Do not list the same company twice because it has two investments.

## Shared infrastructure
Each per-company section reuses `chronograph-portfolio-company-one-pager` — its data fetch sequence, panel specs, brand tokens, and formatting rules. Resolve brand tokens once and apply them across the whole pack so every section is visually consistent.

## Workflow
1. Resolve the fund and the reporting quarter. Confirm brand (one line) once for the whole pack.
2. Pull fund-level figures: NAV, called, distributed, unfunded, DPI/TVPI/RVPI, gross and net performance, and movement vs. prior quarter.
3. Enumerate the fund's investments and group them by company (see the company vs. investment nuance above).
4. For each company, run the one-pager fetch + render to produce its section (full one-pager, or a condensed section for large funds — see Scaling), aggregating multiple investments where present.
5. Build the fund summary: performance and cashflow snapshot, top contributors/detractors, notable markups/markdowns, exits and new investments, and a short "what changed this quarter."
6. Assemble into a single pack — fund summary first, then company sections — and output.

## Scaling
- For funds with many holdings, default to a condensed one-row-per-company summary table plus full one-pagers for the top holdings (by NAV or cost); offer to expand all on request.
- State how many companies were included and whether any were omitted for missing data.

## Chronograph MCP usage
Inspect live tool descriptions; do not hard-code tool names. Follow the one-pager skill's fetch discipline (metric type over display label; gross per-investment returns; never default currency to USD). Display `—` for unavailable values; never fabricate.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Single consistently branded artifact (HTML or document) with a fund summary then per-company sections.
- Run the one-pager's data & brand checklist for each company section.
- State the as-of quarter, currency, and that values are GP-reported / Chronograph-derived.

## Guardrails

- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
- GP investor-communication tool, not investment, legal, tax, audit, or valuation advice.
- Never fabricate financials, valuations, returns, or commentary; collapse empty sections.
- Never substitute LP-level net figures to fill a GP pack.
- If the Chronograph connector is not available, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.
