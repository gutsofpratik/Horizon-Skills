# Rendering

The exact output anatomy for benchmark path selection, candidate shortlists, allocation/risk comparisons, selected benchmark confirmation and link placement. Visual primitives, colours, geometry and number formats come from `design-tokens.md`; this file names the blocks and rules for this skill.

## Mechanism

Render **inline in the conversation** using the richest form the host displays there:

1. The host's own inline visualization capability — cards, paired bars, tables or components that render in the conversation itself.
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
- Start by classifying the benchmark path: BlackRock model, index, or advisor-saved portfolio.
- Present candidates as comparison options for advisor consideration, not directives.
- Ask for confirmation only when the benchmark is ambiguous, not yet selected, or a
	write/change action would persist. Do not ask again after the advisor selects one
	returned candidate or confirms one resolved ticker/index.
- Use only returned allocation, risk, objective, holdings, model, index and portfolio fields.

## Benchmark type selection cards

Use when the advisor has not clearly named the benchmark type.

Three cards, in this order:

1. **BlackRock model** — model shelf, allocation/risk fit, model metadata.
2. **Index** — named market index from securities universe.
3. **Saved portfolio** — advisor-owned portfolio used as a custom benchmark.

Each card contains:

- Type label.
- When to use: one short sentence from the request context.
- Required next input or lookup.

Fallback when rich cards/charts are unavailable:

| Benchmark type | Use when | Next step |
|---|---|---|
| BlackRock model | Compare against a model allocation. | Review model candidates. |
| Index | Compare against a named market index. | Resolve the index security. |
| Saved portfolio | Use an advisor-created portfolio. | Choose a saved portfolio. |

## Candidate shortlist cards

Use after model, index or saved-portfolio candidates are returned. Prefer cards for 2–4 candidates. Use a compact table when more candidates are returned or when the host cannot render cards.

Each card contains:

1. **Candidate name** — returned name, weight 600, primary ink.
2. **Type pill** — BlackRock model, index, or saved portfolio.
3. **Returned fit facts** — allocation, risk, objective, vehicle, holdings, expense, or performance fields when returned.
4. **Key differences** — one short comparison against the subject portfolio.
5. **Link** — returned model, security, methodology, or Advisor Center link when present.

Fallback when rich cards/charts are unavailable:

| Candidate | Type | Returned fit facts | Key differences | Link |
|---|---|---|---|---|
| Model name | BlackRock model | 60/40 · Moderate | Portfolio equity 62.0% vs model 60.0% | Open model |

Rules:

- Show 2–3 candidates when available; 3–5 only when the advisor needs a broader shelf view.
- Include returned allocation, risk profile, objective, vehicle or holdings facts that explain why each candidate is in the shortlist.
- If no close alignment is returned, say so plainly.
- Do not rank as best unless the returned data explicitly supports the comparison and the wording stays factual.

## Allocation and risk comparison

Use paired bars or side-by-side cards when returned values support comparison.

- Reference benchmark uses comparison slot 1 from `design-tokens.md`.
- Subject portfolio uses comparison slot 2.
- Label every series directly or through a legend.
- Use percentages, currency and counts per `design-tokens.md`.
- Do not compare fields that were not returned for both sides.

Fallback when rich cards/charts are unavailable:

| Metric | Benchmark | This portfolio |
|---|---|---|
| Equity | 60.0% | 62.0% |
| Fixed income | 40.0% | 38.0% |
| Total risk | 13.8% | 14.4% |

## Index resolution confirmation

Use when `search_securities` returns one or more possible index matches. Prefer confirmation cards when there are two to four possible matches. Use a table when there are more matches or when the host cannot render cards.

Fallback when rich cards/charts are unavailable:

| Input | Matched index | Identifier | Vehicle type | Confirmation |
|---|---|---|---|---|
| `[INDEX_NAME]` | `[INDEX_NAME] Index` | Returned identifier | Index | Confirm before use |

Rules:

- Confirm vehicle type is index before use.
- Ask if multiple index matches are returned, or if the returned match is not clearly an
	index.
- If the advisor already selected a returned candidate or supplied an exact ticker that
	resolves to one index, treat that as confirmation and proceed to the requested
	analysis. Do not ask for a second confirmation.
- Do not create a benchmark wrapper until the advisor has selected or confirmed the
	resolved index.

## Saved portfolio confirmation

Use when the benchmark is an advisor-owned saved portfolio.

| Portfolio | Last updated | Holdings | Value | Confirmation |
|---|---|---|---|---|
| Returned name | Returned date | 20 | $850,000 | Confirm before use |

Never guess between saved portfolios with similar names.

## Selected benchmark confirmation block

Use only when confirmation is still needed. Before applying the benchmark, show:

1. Selected benchmark name.
2. Benchmark type.
3. Returned facts that support the selection.
4. Analysis path it will be applied to.
5. Explicit confirmation question.

Fallback when rich cards/charts are unavailable:

| Selected benchmark | Type | Applies to | Confirmation needed |
|---|---|---|---|
| Returned name | BlackRock model | Scenario analysis | Yes |

## Methodology and links

- Put Advisor Center, model, security, methodology or comparison links near the candidate or selected benchmark they support.
- Use descriptive link text; never print a bare URL unless links do not render.
- Do not build links by pattern.

## Absent data

- Missing allocation: say allocation was not returned; do not infer from model name alone.
- Missing risk: omit risk comparison and say risk was not returned.
- Missing index vehicle type: ask for confirmation or another identifier.
- Missing link: write `No link returned for this candidate.`

## Posture

- Benchmark candidates are comparison options for advisor consideration.
- Alignment is a factual comparison of returned fields, not a directive.
- The data and returned candidate facts are Advisor Center outputs; the reading is generated; the decision is the advisor's.
