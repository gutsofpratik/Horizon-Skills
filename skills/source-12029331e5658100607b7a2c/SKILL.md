---
name: guided-benchmark-selection
description: Helps choose or confirm a benchmark subject for portfolio comparison. Use when asked what benchmark fits, to compare a portfolio to a model or index, to set a benchmark, or to use an advisor-saved portfolio as the benchmark. Skip when a benchmark is already selected and the advisor is asking for the analysis itself.
---

# Guided Benchmark Selection

## Operating role

Use this skill to organize returned Advisor Center 360° benchmark data, comparison candidates, analytics, links, and workflow routes so the advisor can choose the benchmark path.

## Context

A benchmark can come from three places: the BlackRock model shelf, a market index, or an advisor's own saved portfolio used as a custom comparison point. All three are available benchmark types. When the advisor has not said which type they want, ask rather than assuming; each path resolves the benchmark subject differently.

The generated output is not a BlackRock-authored conclusion. Advisor Center 360° provides data, analytics, links, and workflow routes; the assistant organizes those results; the advisor decides which benchmark, if any, to use.

## Inline rendering

Render benchmark prompts, candidate shortlists, confirmations, and comparison visuals inline in the conversation as each decision point is reached. Use `references/design-tokens.md` for visual primitives and `references/rendering.md` for output anatomy. Do not render into a document, canvas, webpage, side panel, file, or download.

**Sequence — call, write, then call.** Write each prompt, shortlist, or confirmation before issuing the next dependent call.

```text
read portfolio allocation/risk profile → write benchmark type prompt if needed
list/resolve candidates → write candidate shortlist
advisor confirms → apply benchmark to requested analysis
```

## Scope and routing

- Own benchmark choice, benchmark confirmation, candidate shortlists, and benchmark-subject setup.
- Route away when the benchmark is already selected and the advisor asks for the analysis itself; use the analysis path that accepts the confirmed benchmark.
- Route broad portfolio review to `portfolio-review` and portfolio creation/import requests to `guided-portfolio-builder`.

## How to think

- Start by identifying the advisor's comparison objective.
- Treat BlackRock models, market indexes, and advisor-created portfolios as different benchmark types with different lookup paths.
- Compare candidates using returned allocation, risk, objective, holdings, expense, and performance fields when those fields are returned.
- Present benchmark candidates as comparison options, not directives.
- Ask for confirmation before applying an inferred benchmark.

## Visual rule

Every chart or card generated in this workflow must use local `references/design-tokens.md` at the point it is created. Do not use default chart-library or card palettes.

If the host cannot load the reference files, still use the richest inline visual form
first. Benchmark path choices use three equal cards when available. Candidate shortlists
use cards for two to four candidates. Markdown tables are fallback only.

Do not ask for a second confirmation after the advisor selects one returned candidate or
after an exact ticker resolves to one index. Ask only when the match is ambiguous, the
vehicle type is unclear, or a persistent change requires confirmation.

## Tools

| Tool | Purpose |
|---|---|
| `analyze_portfolio` / `analyze_characteristics` | Read the portfolio's own asset allocation and risk profile first. |
| `list_models` | List BlackRock and third-party model candidates, with classification metadata (short_name, risk_profile, objective, family_vehicle) for shortlisting. |
| `get_model` | Read a shortlisted candidate's actual allocation/holdings to compare. |
| `search_securities` | Resolve a named index (for example, `[INDEX_NAME]`) directly from the securities universe. The vehicle type must be index. |
| `create_portfolio` | Wrap a resolved index security as a single-holding portfolio so it can be addressed as a benchmark subject. |
| `list_portfolios` / `get_portfolio` | Find and confirm one of the advisor's own saved portfolios to use as a custom benchmark. |

## Workflow

### Step 1: Confirm which type of benchmark

Classify the likely benchmark path before using any lookup tool. If the advisor already named a specific benchmark (for example, "use `[INDEX_NAME]`" or "benchmark it against `[CUSTOM_PORTFOLIO_NAME]`"), skip ahead to the matching step below. If the surrounding context points strongly to one path, state the inferred path and ask for confirmation before proceeding. If context is weak, ask which they'd prefer:

- **A BlackRock model** — selected from the model shelf by allocation alignment.
- **An index** — a market benchmark such as an equity or fixed income index.
- **One of their own saved portfolios** — a custom model they've already built, used as the comparison point.

### Step 2a: BlackRock model

1. **Read the portfolio's own profile first.** Use `analyze_portfolio`'s asset-class allocation and total risk (or `analyze_characteristics` if already loaded). The match has to be grounded in the portfolio's actual numbers.
2. **Call `list_models`** to see the full set of BlackRock candidates.
3. **Shortlist 3–5 candidates using the model metadata**, not just the name: `short_name` (e.g., "60/40" signals a 60% equity / 40% fixed-income split), `risk_profile`, `objective`, and `family_vehicle` all narrow the shelf toward plausible comparison candidates before any allocation is compared line-by-line.
4. **Call `get_model` on each shortlisted candidate** and compare its actual allocation against the portfolio's actual allocation from step 1.
5. **Present 2–3 comparison candidates**, each with one line grounded in the real comparison (e.g., "62% equity / 38% fixed income vs. this portfolio's 65%/35%"). If using a chart or card for allocation or risk comparison, apply the local design tokens before presenting. If none show close alignment, say so plainly.

Write the candidate shortlist now; wait for advisor confirmation before applying a benchmark to an analysis.

### Step 2b: Index

An index lives in the securities universe, not the model shelf — a different lookup from Step 2a.

1. Ask which index if not already named.
2. Call `search_securities` to resolve it directly from the securities universe. Remember that indices have vehicle type index.
3. Confirm the match with the advisor before proceeding — index naming conventions vary, so confirm you've found the one they mean.
4. Once confirmed, use `create_portfolio` to hold that index security on its own (a single-holding portfolio is fine for an index), giving it an id that can be passed as the benchmark subject.

Write the resolved index confirmation before creating the benchmark subject.

### Step 2c: Advisor's own saved portfolio

1. Call `list_portfolios` to find the advisor's saved portfolio by name.
2. Confirm the match with the advisor: "Use [portfolio name], last updated [date], as the benchmark?"
3. Call `get_portfolio` to confirm it's ready to use.

Write the saved-portfolio confirmation before using it as the benchmark subject.

### Step 3: Apply the benchmark

Before applying the benchmark, state the selected benchmark and the returned facts that match the advisor's comparison request. Once the advisor confirms the choice, pass it as `benchmark: {type, id}` on the tools that accept it: `simulate_performance`, `compare_performance`, `analyze_scenarios`, `get_opportunities_and_issues`, `analyze_characteristics`, `analyze_esg`, `analyze_risk`. (`analyze_portfolio`, `project_wealth`, and `get_fund_health_and_ideas` don't take a benchmark.)

If the advisor's original prompt asked for comparison or analysis, apply the confirmed benchmark to that analysis in the same flow. If the advisor only asked to choose or set a benchmark, stop after confirmation and identify comparison as an available next path.

## Source and link discipline

Every material metric, analytic result, methodology detail, security or fund reference, and Advisor Center 360° workflow route must come from the returned Advisor Center 360° payload or an approved public, security, fund, or methodology page.

When the payload includes an Advisor Center 360° URL, methodology URL, security or fund URL, or source link, surface it near the relevant data or analytics section. If both an Advisor Center 360° route and a public page are returned, use the Advisor Center 360° route for workflow continuation and the public page for security, fund, or methodology context.

Do not cite BlackRock as the source of advisor or assistant-generated review points. BlackRock provides portfolio data and analytics; the advisor interprets those analytics and decides what matters.

If a metric, link, methodology detail, Funds to Explore entry, projection value, or workflow route is not returned, label it unavailable rather than filling the gap from memory.

## Presentation standards

Apply `references/design-tokens.md` and `references/rendering.md` every time visuals or formatted outputs are available.

- Keep outputs advisor-facing and concise. Do not write client-ready copy.

## Guardrail

Frame every shortlist as comparison candidates for the advisor's consideration. Model or index alignment is a factual statement about allocation similarity, not a directive. If a chart or card is generated without applying the local design tokens, treat that as a defect and revise it before presenting. Never use an inferred benchmark type without advisor confirmation.
