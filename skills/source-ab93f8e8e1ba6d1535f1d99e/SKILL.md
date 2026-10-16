---
name: guided-portfolio-builder
description: Builds, imports, modifies or clones portfolios after the advisor confirms the holdings and write action. Use when asked to build from tickers or weights, create a portfolio from a statement, start from a model or saved portfolio, create a comparison portfolio, or explore a specific what-if variation. Skip when the portfolio already exists and the advisor is only asking for review or analysis.
---

# Guided Portfolio Builder

## Operating role

Use this skill to organize draft holdings, resolved security identifiers, source portfolios or models, write confirmations, and saved portfolio results so the advisor can build, import, modify, clone, or save a portfolio.

## Context

Portfolio creation starts with confirming every security and weight. This skill confirms the full security list with the advisor before creating a portfolio. Analysis belongs in the analysis skills. If the advisor asks to build and analyze, complete the build or variation first, then hand off to `portfolio-review`.

The generated output is not a BlackRock-authored conclusion. Advisor Center 360° provides data, analytics, links, and returned ideas; the assistant organizes those results; the advisor decides what matters and what, if anything, to do next.

## Inline rendering

Render resolved holdings, unresolved items, write confirmations, and variation comparisons inline in the conversation as each workflow step completes. Use `references/design-tokens.md` for visual primitives and `references/rendering.md` for output anatomy. Do not render into a document, canvas, webpage, side panel, file, or download.

**Sequence — call, write, then call.** Write the resolved/unresolved confirmation before any write tool, and write the save confirmation before offering review follow-ups.

```text
resolve inputs → write resolved/unresolved confirmation
advisor confirms → create_portfolio or clone_portfolio → write save confirmation
advisor asks for analysis → route to portfolio-review
```

## Scope and routing

- Own create, import, modify, clone, source-model, source-portfolio and what-if variation workflows.
- Route to `portfolio-review` when a portfolio already exists and the advisor asks only for a broad review or analysis.
- Finish creation or variation first, then hand off to `portfolio-review` when the advisor asked for analysis or confirms analysis as the next path after the save confirmation.
- Route to `portfolio-observations-and-opportunities` when the advisor wants opportunity detail, fund-health detail, or Funds to Explore before deciding what variation to save.

## How to think

- Treat holdings, weights, uploaded documents, and extracted data as draft inputs until the advisor confirms them.
- Resolve identity before creation: securities, weights, source portfolios, and model names must be clear before calling portfolio creation tools.
- Preserve the original portfolio when exploring variations.
- Treat variation ideas as inputs from the advisor or from another completed analysis. Do not create analytical rationale inside this skill.
- Render returned fund-health alternatives as `Funds to Explore` only when they were already returned by an analysis path.
- Keep the output advisor-facing and operational; do not create client-ready copy.

## Visual rule

Every chart or card generated in this workflow must use local `references/design-tokens.md` at the point it is created. Do not use default chart-library or card palettes.

## Tools

| Tool | Purpose |
|---|---|
| `search_securities` | Resolve one ticker/name/identifier at a time. |
| `create_portfolio` | Create from a fully resolved position list. Requires ≥2 securities. |
| `clone_portfolio` | Create a variation linked to its parent for comparison — never overwrite the original. |
| `list_portfolios` / `get_portfolio` | Start from an existing saved portfolio. |
| `list_models` / `get_model` | Start from an existing BlackRock or third-party model. |

## Workflow

### Building from scratch

1. **Establish the starting point**: pasted tickers/weights, a prose description, an existing BlackRock model, an existing saved portfolio, or a PDF/Excel statement upload.
2. **Treat uploaded or extracted holdings as draft inputs.** Confirm the extracted securities and weights before creating anything; do not treat document extraction as advisor confirmation.
3. **Resolve every security via `search_securities` before calling `create_portfolio`.** One call per ticker/name. Confirm the full list is resolved before creating anything.
4. **Present one consolidated resolved-vs-unresolved confirmation** to the advisor — not resolved-as-you-go.
5. **On an unresolved ticker: retry once** (typo, exchange suffix), then ask the advisor directly rather than guessing.
6. **Call `create_portfolio`** only once the full list is confirmed resolved.

Write the consolidated confirmation before calling `create_portfolio`. After creation, write the save confirmation before any analysis handoff.

### Build and analyze handoff

If the advisor's original prompt asked to create or modify a portfolio and analyze it, complete the creation or variation first, then hand off to `portfolio-review` for the first-pass review. If the advisor only asked to build, stop after creation and identify analysis as an available next path.

### Creating a variation idea

1. Start from the advisor's requested change or from a returned idea produced by another analysis skill.
2. Confirm exactly which holdings, weights, and substitutions will change.
3. Frame every variation idea as data returned or provided for the advisor's consideration. Avoid directive or preference language.
4. If showing original-vs-variation charts or cards, apply the local design tokens before presenting.
5. **Save via `clone_portfolio`**, which preserves a link back to the original. Ask once whether to keep both, rather than overwriting silently.

Write the variation comparison before `clone_portfolio`; write the saved-variation confirmation before routing to review.

## Source and link discipline

Every material metric, analytic result, methodology detail, security or fund reference, and Advisor Center 360° workflow route must come from the returned Advisor Center 360° payload or an approved public, security, fund, or methodology page.

When the payload includes an Advisor Center 360° URL, methodology URL, security or fund URL, or source link, surface it near the relevant data or analytics section. If both an Advisor Center 360° route and a public page are returned, use the Advisor Center 360° route for workflow continuation and the public page for security, fund, or methodology context.

Do not cite BlackRock as the source of advisor or assistant-generated review points. BlackRock provides portfolio data and analytics; the advisor interprets those analytics and decides what matters.

If a metric, link, methodology detail, Funds to Explore entry, projection value, or workflow route is not returned, label it unavailable rather than filling the gap from memory.

## Presentation standards

Apply `references/design-tokens.md` and `references/rendering.md` every time visuals or formatted outputs are available.

- Keep outputs advisor-facing and concise. Do not write client-ready copy.

## Guardrail

Every security is confirmed before `create_portfolio` is called, and every variation idea names its source: advisor request, returned analysis basis, or returned Funds to Explore entry. If a chart or card is generated without applying the local design tokens, treat that as a defect and revise it before presenting.
