# Rendering

The exact output anatomy for draft holdings, security-resolution confirmations, source summaries, variation comparisons and write-confirmation prompts. Visual primitives, colours, geometry and number formats come from `design-tokens.md`; this file names the blocks and rules for this skill.

## Mechanism

Render **inline in the conversation** using the richest form the host displays there:

1. The host's own inline visualization capability — tables, cards, comparison charts or components that render in the conversation itself.
2. Fallback when rich cards/charts are unavailable: markdown tables. Tables must preserve the same labels and values as the richer visual.

Capability selection is mandatory. Before writing any markdown table fallback, decide
whether the current host can render the specified inline visual mark for the block. Use
the richer mark when any inline chart, card, component, or visualization channel is
available. Use markdown tables only when no inline visual channel exists, the inline
render fails, or the host explicitly cannot display that block's richer mark. Do not
choose markdown tables for speed, familiarity, or because the fallback example is
easier to copy.

Do not render into a document, canvas, webpage, side panel, file, or download. Do not use raw HTML, raw SVG, or box-drawing art. Never describe the mechanism or fallback to the advisor.

## Page

- Heading levels: response header `##`, sections `###`. Nothing else is a heading.
- Render progressively: show draft inputs, then resolution status, then write confirmation, then created portfolio summary only after confirmation and tool completion.
- Write operations need an explicit confirmation block before the tool call.
- Use only returned security, portfolio, model and analytics fields.
- After a successful write, the analysis handoff — and only that — is a single
  action button from `design-tokens.md`, labelled with the exact prompt to
  send. Every other available path stays prose or a table column, and the
  write tool itself is never behind a button.

## Draft holdings table

Use when the advisor provides tickers, identifiers, uploaded holdings or described allocations.

| Holding | Identifier supplied | Draft weight | Source | Status |
|---|---|---|---|---|
| `[TICKER]` | Ticker | 12.0% | Uploaded statement | Needs resolution |

Rules:

- Preserve every input row. Do not drop blanks or unparseable identifiers.
- Include `Source` only when the payload or uploaded document identifies one. Omit the column when no source is returned or inferred from the uploaded file.
- Mark unresolved rows with a Warning status pill: `Needs resolution`.
- Mark resolved rows with a Good status pill: `Resolved`.
- If a returned BlackRock product link is available, place it in a `Product link` column with descriptive link text and the link styling from `design-tokens.md`.
- State inferred column mappings above the table when a document or spreadsheet is parsed.
- Percentages use the number format in `design-tokens.md` unless the input already formatted the value.

## Resolved/unresolved confirmation table

Show one consolidated confirmation table after security lookup, not a separate response per resolved ticker.

| Input | Matched security | Identifier used | Weight | Resolution |
|---|---|---|---|---|
| `[TICKER]` | `[SECURITY_NAME]` | `ticker:[TICKER]` | 12.0% | Resolved |
| `[AMBIGUOUS_TICKER]` | Multiple candidates | `ticker:[AMBIGUOUS_TICKER]` | 5.0% | Needs advisor selection |

Rules:

- Resolved rows use Good status pills.
- Ambiguous or unresolved rows use Warning status pills.
- When a returned BlackRock product link is available, use a descriptive hyperlink in the row. Do not build product links by ticker pattern.
- Do not choose between ambiguous share classes.
- Stop before writing if any row remains unresolved.

## Source model or source portfolio card

Use when building from an existing model or saved portfolio.

Card anatomy:

1. **Header** — returned portfolio or model name.
2. **Meta** — source type, last updated date, holdings count, value or model family when returned.
3. **Key facts** — allocation split, objective, risk profile or vehicle when returned.
4. **Available action** — an action button sending the advisor's confirmation, or the returned workflow route.

Fallback when rich cards/charts are unavailable:

| Source | Type | Key facts | Available action |
|---|---|---|---|
| Model name | BlackRock model | 60/40 · Moderate | Use as source after confirmation |

## Write-confirmation prompt

Use before every real write: `create_portfolio` or `clone_portfolio`.

Confirmation block anatomy:

1. **Write action** — `Create portfolio` or `Create variation`.
2. **What will be written** — count of holdings, source, parent portfolio if any.
3. **Open items** — unresolved holdings, missing metadata or inferred mapping
	caveats. List them, then collect them in one pass using the host's input
	or elicitation channel when it has one: a pick list for any field whose
	accepted values come from the tool schema, a typed answer for open values
	like name and total value. Prose is the fallback when no input channel
	exists. Never make the advisor restate a value the form could have taken.
4. **Confirmation question** — ask for an explicit yes before the write.

Fallback when rich cards/charts are unavailable:

| Write action | What will be written | Open items |
|---|---|---|
| Create portfolio | 12 resolved holdings | Portfolio type confirmation needed |

Do not call the write tool from the same response that first displays unresolved or ambiguous inputs.

## Created portfolio summary

After a successful write, show a compact summary:

| Created portfolio | Portfolio type | Holdings | Source | Next path |
|---|---|---|---|---|
| Returned name | Returned type | 12 | Uploaded statement | Portfolio review available |

Use returned id only internally. Do not print ids unless the advisor explicitly needs them.

When rich cards are available, prefer a compact save-result card over a table: name, portfolio type, holdings count, source when returned, and next path. Use a table only when the host cannot render the card or when multiple created items must be compared. The next path on that card is an action button, not prose.

## Original-vs-variation comparison

Use only after a variation exists or returned comparison analytics are available.

- For allocation, risk or modeled comparison, use paired bars or side-by-side cards patterned on `design-tokens.md`.
- For allocation-only part-to-whole comparisons, use a donut or stacked bar when the host supports it. Use paired bars for before/after metric comparisons and line charts only for time-series values.
- Original portfolio uses the first comparison slot; variation uses the second.
- Name the factual source of the variation: returned fund-health flag, returned Funds to Explore entry, or risk contribution.
- Do not frame the variation as preferred.

Fallback when rich cards/charts are unavailable:

| Metric | Original | Variation |
|---|---|---|
| Equity | 62.0% | 60.5% |
| Total risk | 14.2% | 13.8% |

## Funds to Explore in variation workflows

When a holding change idea comes from fund-health output, render it as `Funds to Explore`. If upstream or older text uses another label, the advisor-facing label remains `Funds to Explore`.

| Current holding | Returned basis | Funds to Explore | Link |
|---|---|---|---|
| Current fund | Returned flag or risk contribution | Returned fund | Returned product link |

Do not create or rank alternatives not returned by the tool.
When multiple Funds to Explore entries are returned for one holding, keep them inside that holding's card or row. Preserve returned order unless the payload supplies a ranking or materiality field.

## Link-outs and citations

- Put Advisor Center, fund, security or methodology links near the relevant table/card.
- Use descriptive link text; never print a bare URL unless links do not render.
- Do not build links by pattern.

## Absent data

- Missing weight: label `Weight not provided` and ask before write.
- Missing security match: label `No match returned` and ask for correction.
- Missing portfolio type, mandate, tax status or total value: collect via the
	open-items form; do not default.
- Missing variation basis: state no checkable basis was returned.

## Posture

- Treat holdings and extracted data as draft until confirmed.
- Treat writes as real data changes and ask first.
- The data and returned ideas are Advisor Center outputs; the reading is generated; the decision is the advisor's.
