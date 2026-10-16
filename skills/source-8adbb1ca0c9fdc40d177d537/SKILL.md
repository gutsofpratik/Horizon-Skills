---
name: portfolio-observations-and-opportunities
description: Reviews returned portfolio opportunity checks, fund-health details, Funds to Explore, and approved follow-up links. Use when asked to show opportunities, explain why a fund is flagged, open fund details, show fund health, list clear checks, find Funds to Explore, or identify the next path from an opportunity. Skip when the advisor asks for a broad portfolio review before narrowing to opportunities.
---

# Portfolio Observations and Opportunities

## Operating role

Use this skill to organize returned opportunity checks, fund details, Funds to Explore, and workflow links so the advisor can review the data and choose the next path.

## Context

Advisor Center 360° opportunity results are a set of returned portfolio checks. Use them as a structured way to show what was flagged, what was clear, which fund-detail routes are available, and which returned content links are attached to a check. Do not elevate opportunity results over other portfolio analysis outputs such as overview, risk, performance, tax, characteristics, or fund details.

The generated output is not a BlackRock-authored conclusion. Advisor Center 360° provides data, analytics, links, and returned ideas; the assistant organizes those results; the advisor decides what matters and what, if anything, to do next.

Two advisor paths are common:

- **From opportunity results to next path**: The advisor asks to review all opportunity checks. Fund-health opportunities route to fund details. Broader opportunities route to the relevant analysis output or approved content link when available.
- **From overview to fund details**: A general portfolio review shows flagged opportunities, one of which is fund details. The advisor opens fund details, reviews the flagged dimensions, reviews any returned Funds to Explore, then can compare the existing portfolio with a saved variation if requested.

## Inline rendering

Render opportunity summaries, card grids, fund-detail cards, Funds to Explore rows, and link-outs inline in the conversation as each result is returned. Use `references/design-tokens.md` for visual primitives and `references/rendering.md` for output anatomy. Do not render into a document, canvas, webpage, side panel, file, or download.

**Sequence — call, write, then call.** Write the opportunity summary and grid before drilling into any selected opportunity.

```text
get_opportunities_and_issues → write opportunity summary + card grid
selected fund-health card → get_fund_health_and_ideas → write fund-detail cards + Funds to Explore
selected analytics card → call matching analysis only if requested → write drilldown
```

## Scope and routing

- Own opportunity checks, fund-health detail, Funds to Explore, approved content links, and opportunity-driven drilldowns.
- Route to `portfolio-review` when the advisor asks for a broad first-pass portfolio review rather than opportunity detail.
- Route to `guided-portfolio-builder` only after the advisor asks to create or save a variation from returned data.

## How to think

- Treat opportunities as returned portfolio checks, not as a separate conclusion layer.
- Sort flagged opportunity checks before clear checks regardless of return order.
- Keep flagged and clear states visually distinct through border, background, label color, and card copy.
- Show clear cards with the returned value, threshold, or portfolio-vs-benchmark comparison when one exists.
- For fund-health opportunities, route to in-chat fund details before showing Funds to
	Explore. If the returned link is a methodology page, label it as methodology, not as a
	fund-details tab or drilldown route.
- For broader flagged opportunities with an approved content link, show that content link as the available path unless the advisor asks for a deeper analytics view.
- Surface Funds to Explore only when returned by Advisor Center 360° or an approved security, fund, or methodology page.
- Surface Advisor Center 360° or approved public content links only when returned or listed in this skill.
- Keep the advisor-facing output neutral, data-grounded, and non-directive.

## Visual rule

Every opportunity card, fund-detail card, chart, or callout generated in this workflow must use local `references/design-tokens.md` at the point it is created. Do not use default chart-library or card palettes.

If the host cannot load the reference files, still use the richest inline visual form
first. Opportunity summaries use equal-width cards when available. Fund-health details
use a 4-column card grid when available, with whole-card status tint, status dot plus
words, drivers, and a mandatory Funds to Explore tail on every card. Markdown tables are
fallback only, and the fallback table must keep a `Funds to Explore` column.
For 20+ holdings, keep the visual surface: flagged funds use full cards; on-track funds
may use compact status cards with green tags. Do not switch to a plain markdown list or
ticker/category/weight table when cards are available.

## Tools

| Tool | When to call |
|---|---|
| `get_opportunities_and_issues` | Use when the advisor asks directly for opportunities, dashboard flags, outlier status, or opportunity checks. |
| `analyze_portfolio` | Use only when opportunities are already part of a first-pass portfolio review and the broader snapshot/scenarios/opportunities payload is needed. |
| `get_fund_health_and_ideas` | Use when the advisor asks to drill into fund-health flags, fund details, or returned Funds to Explore. |
| `get_security` / `search_securities` | Use only when a returned fund, ticker, or security/fund link needs identity resolution before showing details. |
| `analyze_risk` / `analyze_scenarios` / `analyze_characteristics` | Use only when the advisor asks for a deeper analytics view after seeing the opportunity card. |
| `ac360-capability-router` | Use when the requested opportunity workflow is available in Advisor Center but not available in this chat. |

## Opportunity checks and content links

Use returned opportunity names and labels where available. If the returned response maps to one of these known checks, keep the explanation aligned to the returned data and use the listed content link only when the opportunity is flagged or the advisor asks for resources.

| Opportunity check | Category | Explain with | Approved content link |
|---|---|---|
| Tax Worst Offender | Security Exposure | Estimated capital gains value, NAV percentage, and as-of details when returned. | [Tax evaluator](https://www.blackrock.com/us/financial-professionals/tools/tax-evaluator) |
| Red Flag Funds | Security Exposure | Count of flagged funds, status mix, triggered dimensions, and fund-details route. | Primary path is `Review flagged funds in this chat`. Use a returned Advisor Center 360° fund-details route only when it is explicitly a fund-details route. If the only returned URL is methodology, label it `Fund health methodology`. |
| High Cash Position | Concentration | Cash weight, category comparison, or threshold when returned. | [Fixed income resources](https://www.blackrock.com/us/financial-professionals/investments/products/fixed-income) |
| Single Security Risk | Security Exposure | Security name, weight, and risk contribution when returned. | [Concentrated stock resources](https://www.blackrock.com/us/financial-professionals/investments/products/managed-accounts/concentrated-stock) |
| Concentrated Stock Position | Concentration | Single-stock weight and threshold when returned. | [Concentrated stock resources](https://www.blackrock.com/us/financial-professionals/investments/products/managed-accounts/concentrated-stock) |
| High Individual Bond Allocation | Concentration | Individual bond weight and threshold when returned. | [Fixed income managed accounts](https://www.blackrock.com/us/financial-professionals/investments/products/managed-accounts/fixed-income) and [iBonds](https://www.blackrock.com/us/financial-professionals/investments/products/ibonds) |
| High Sensitivity to a Rate Cut | Scenario-Based | Portfolio impact, benchmark impact, and relative difference when returned. | [Target allocation resources](https://www.blackrock.com/us/financial-professionals/investments/products/model-portfolios/portfolio-rebalancing-insights/target-allocation) |
| Drift from Benchmark | Benchmark Comparison | Benchmark prerequisite, active risk or drift value, and any returned contributors. | [Target allocation resources](https://www.blackrock.com/us/financial-professionals/investments/products/model-portfolios/portfolio-rebalancing-insights/target-allocation) |

If a returned opportunity does not match this table, keep its returned title and explain only the returned fields.

## Workflow

### Step 1: Get opportunity status

Call `get_opportunities_and_issues` unless the current turn already has opportunity data from `analyze_portfolio`. Use the returned opportunity list, status fields, comments, values, thresholds, counts, and links. Do not create opportunity checks that were not returned.

### Step 2: Sort and summarize

Sort the cards in this order:

- Flagged opportunity checks first.
- Clear opportunity checks second.
- Within each group, preserve returned order unless the payload includes severity, count, impact, or materiality fields.
- If severity or impact is returned, sort highest severity or largest impact first within the flagged group.

Start with a one-sentence summary: number flagged, number clear, and whether fund details or content links are available.

### Step 3: Render the opportunity card grid

When the interface supports cards, render a 3-column grid of equal-size cards with no internal scrolling. If cards are unavailable, use a markdown table with the same fields and keep flagged rows first.

Write the summary and full card grid now, before calling any drilldown tool.

Every card follows this hierarchy:

- **Status label**: `FLAGGED` or `CLEAR`; small, uppercase, bold, letter-spaced; the Warning or Critical role per returned severity for flagged, Good for clear.
- **Rule title**: exactly as returned when present; bold, black, larger than body text.
- **One-line explanation**: one plain-English sentence built only from returned `comment`, `value`, threshold, count, or comparison fields.
- **Available path**: flagged cards only; small gray text when the payload returns next-step text, a workflow route, a fund-details route, or an approved content link. For red or flagged fund-health opportunities, the primary path is `Review flagged funds in this chat`; call `get_fund_health_and_ideas` when the advisor selects it. Hyperlink only true routes and content links. If the fund-health URL is a methodology page, label it `Fund health methodology` and present it as a secondary source link, not as the available path. For non-fund-health opportunities with an approved content link, use the content link as the available path.

Card state rules:

- **Flagged card**: a status card per `references/design-tokens.md` § Status in the returned severity role, with a `FLAGGED` label.
- **Clear card**: a status card in the Good role, with a `CLEAR` label.
- **Status roles are fixed**: the returned severity for flagged, Good for clear, Neutral when no status was returned. Never a colour absent from the token tables.
- **Clear is not blank**: if a value, threshold, or portfolio-vs-benchmark comparison exists, include it in the one-line explanation.
- **Threshold discipline**: include a threshold only for threshold-based checks; do not force one into qualitative or pass/fail checks.

### Step 4: Build one-line explanations

Use the shortest plain-English sentence that preserves the returned facts.

Examples:

| Returned shape | Card explanation shape |
|---|---|
| Threshold check with value | `[value] — below/above the [threshold] threshold.` |
| Portfolio-vs-benchmark signal | `Portfolio [value] vs. benchmark [value], a [difference] difference.` |
| Count-based fund-health signal | `[count] fund(s) flagged for fund-health review.` |
| Missing numeric context | Use the returned comment as-is or shorten it without changing meaning. |

Do not make a clear card read only "clear." Include the underlying number or comparison when available.

### Step 5: Route the drilldown

After the 3-column opportunity card grid, ask which card or area the advisor wants to open. Use the selected card to route:

| Selected area | Next path |
|---|---|
| Fund health | Call `get_fund_health_and_ideas` and show fund-detail cards. If the opportunity card is red or flagged, encourage reviewing the flagged funds in this chat before sending the advisor to methodology or external pages. |
| Capital gains or tax drag | Show returned tax/capital-gains fields and surface the approved tax evaluator content link when available; use `ac360-capability-router` only when the advisor asks for the Advisor Center tax evaluator workflow. |
| Benchmark drift | Show returned drift facts and the approved model-positioning content link when available. If benchmark details are missing, label them unavailable rather than routing into benchmark setup. |
| Rate-cut sensitivity or scenario signal | Show returned scenario facts and the approved model-positioning content link when available; call `analyze_scenarios` only when the advisor asks for scenario detail. |
| Single-security risk, stock concentration, cash, or bond concentration | Show returned exposure facts and the approved content link when available; call deeper analytics only when the advisor asks for them. |
| Content, security, fund, or methodology link | Surface the returned or listed approved link near the relevant card. |

For fund-health opportunities, show fund details before Funds to Explore. For broader opportunities, show the returned data and approved content link rather than creating a portfolio change path.

Write the selected drilldown now before asking whether the advisor wants another card or deeper analysis.

### Step 6: Show fund details and Funds to Explore

For fund-health drilldowns, prefer a 4-column fund-detail card grid whenever the host
can render cards. Use the full-card status tint plus the status dot and words in the
header. Use a compact table only when cards are unavailable, and keep a `Funds to
Explore` column in that table.

Each fund-detail card or fallback row includes:

- Holding name and ticker.
- Fund-health status: red/yellow/green when returned.
- Triggered criteria and returned rationale.
- Relevant value, threshold, or as-of date when returned.
- Returned alternatives labeled `Funds to Explore`, even if the payload uses an internal label such as `Benchmark idea`.
- Returned security, fund, methodology, or Advisor Center 360° links near the relevant holding.

Always surface the Funds to Explore area for every holding: show returned alternatives
when present, and show `No Funds to Explore returned` when absent. Do not omit the area
for clear funds, full-list requests, or long fund lists.

Keep follow-up commentary short. The visual cards carry driver detail; after the cards,
write at most three bullets covering the first item to inspect, why it outranks the
others using returned metrics, and any coverage gaps. Do not write one paragraph per
flagged fund.

For returned alternative categories, use advisor-facing labels:

| Returned idea type | Advisor-facing label |
|---|---|
| Core index ETF idea | `Funds to Explore` |
| Factor or minimum-volatility idea | `Funds to Explore` |
| Active or thematic ETF idea | `Funds to Explore` |
| Active mutual fund idea | `Funds to Explore` |

Show Funds to Explore as returned alternatives for the advisor's consideration. Do not imply a next action, and do not create an alternative that was not returned.

## Source and link discipline

Every opportunity status, material metric, analytic result, methodology detail, security or fund reference, Funds to Explore entry, approved content link, and Advisor Center 360° workflow route must come from the returned Advisor Center 360° payload, this skill's content-link table, or an approved public, security, fund, or methodology page.

When the payload includes an Advisor Center 360° URL, methodology URL, security or fund URL, or source link, surface it near the relevant opportunity card or fund-detail card. If both an Advisor Center 360° route and a public page are returned, use the Advisor Center 360° route for workflow continuation and the public page for security, fund, or methodology context.

Do not finish an opportunity or fund-health response with no links if any Advisor Center
360°, methodology, security, fund, source, or product link was returned.

Do not cite BlackRock as the source of advisor or assistant-generated review points. BlackRock provides portfolio data and analytics; the advisor interprets those analytics and decides what matters.

If a status, metric, link, methodology detail, Funds to Explore entry, projection value, or workflow route is not returned or listed as approved, label it unavailable rather than filling the gap from memory.

## Presentation standards

Apply `references/design-tokens.md` and `references/rendering.md` every time cards, charts, or formatted outputs are available.

- Keep outputs advisor-facing and concise. Do not write client-ready copy.

## Guardrail

Opportunity results are one portfolio-analysis output. Sort flagged before clear, keep every card grounded in returned fields, and make flagged and clear states visually distinct. If an opportunity card, fund-detail card, chart, or callout is generated without applying the local design tokens, treat that as a defect and revise it before presenting. Do not turn opportunities into directives, do not invent Funds to Explore or content links, and do not skip clear cards when the advisor asked for the opportunity set.
