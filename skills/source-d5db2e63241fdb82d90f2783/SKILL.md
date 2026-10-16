---
name: chronograph-look-through-exposure-scan
description: Aggregate an LP's look-through portfolio exposure across funds — by company, sector,
  geography, vintage, strategy, and currency — and surface concentration, using the Chronograph
  top-exposures tool.
when_to_use: 'Use when an LP or fund-of-funds wants to understand its true underlying exposure
  across managers. Triggers: "what do we actually own", "look-through exposure", "how concentrated
  are we", "single-name exposure across funds", "sector/geography breakdown", "are we overexposed to
  X". Not for single-fund or single-company reporting.'
---

# Look-Through Exposure Scan

**Requirements:** A connected Chronograph MCP server as an LP client.

## Overview
Aggregate the LP's underlying exposure across all its fund commitments, looking through to the portfolio-company level — answering "what do we actually own, and where are we concentrated." Produce exposure breakdowns and concentration flags, not a data dump.

## Chronograph MCP usage
The Chronograph MCP (connected as an LP client) exposes a **`top-exposures`** tool — the primary engine for this skill. It aggregates the LP's exposure to underlying companies across all of its funds, and double-clicks into the specific funds and investments associated with each company. Use it to build the company-level exposure ranking, then expand any company into the funds and investments behind it.

For supporting fund-level attributes (strategy, vintage, geography, reporting currency), use entity resolution and the fund-metadata path. Never default currency to USD; resolve from fund metadata and state the FX conversion basis.

## Workflow
1. Set scope: portfolio, group, or selected commitments; choose the exposure basis (NAV, or NAV + unfunded).
2. Call `top-exposures` to get ranked company-level exposure across the LP's funds.
3. For the top names — or any company on request — use `top-exposures` to drill into the funds and investments behind that company.
4. Aggregate exposure across dimensions — company / single name, sector, geography, vintage, strategy, currency — normalizing to one reporting currency (state the FX basis).
5. Compute concentration: top-10 names and their weight, largest single-name %, sector and geography weights, vintage and strategy mix; optionally an HHI per dimension.
6. Present the concentration headline, the breakdowns, and the ability to expand any company into its underlying funds and investments.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Lead with the concentration headline (top names, largest exposures, any flags).
- Show breakdowns by single name, sector, geography, vintage, strategy, and currency.
- Offer per-company drill-down into the underlying funds and investments.
- State the currency / FX basis and as-of date. Never fabricate holdings.

## Guardrails

- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
- Draft analyst work product for exposure monitoring — not investment, legal, or tax advice.
- This is an insight / aggregation tool, not a data export; present concentration and exposure, not raw holdings tables intended for offline reuse.
- If the Chronograph connector is not available, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.
