# Rendering

The exact output anatomy for modeled performance, projected wealth, assumptions, fee treatment, methodology links and unsupported configuration callouts. Visual primitives, colours, geometry and number formats come from `design-tokens.md`; this file names the blocks and rules for this skill.

## Mechanism

Render **inline in the conversation** using the richest form the host displays there:

1. The host's own inline visualization capability — line charts, range charts, cards or components that render in the conversation itself.
2. Fallback when rich cards/charts are unavailable: markdown tables. Tables must preserve the same labels, series and values as the richer visual.

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
- Open with a direct classification: modeled performance, projected wealth, methodology, fee treatment, unsupported configuration, or route-only.
- Put fee treatment and assumptions near the chart or table they affect.
- Use only returned fields and approved methodology links.
- Links sit at the end of the section that uses them. Use descriptive link text; never print a bare URL unless links do not render.

## Modeled performance line chart

Use when the response returns a time-series of modeled or simulated performance.

- X-axis: returned dates or periods in response order.
- Y-axis: returned value, cumulative return or growth value, using the unit returned.
- Series: subject portfolio first unless the source lists a benchmark/reference first; comparison series follow the source order and use categorical slots from `design-tokens.md`.
- Labels: show direct series labels or a legend. Do not rely on colour alone.
- Fee note: directly beneath the chart when fee treatment is returned or discussed.

Fallback when rich cards/charts are unavailable:

| Period | This portfolio | Benchmark |
|---|---|---|
| 1 year | 6.2% | 5.8% |
| 3 years | 18.4% | 17.1% |

## Projected wealth path

Use for projected wealth, modeled future value or outcome paths.

- Show the base path as a line when only one path is returned.
- Show additional returned paths as separate labeled series in source order.
- Use categorical slots from `design-tokens.md` for multiple wealth projections. Keep the same subject in the same slot across all projection blocks in the response.
- Show the active advisory fee in a compact callout directly under the chart: rate applied, included/excluded when returned, and whether fee treatment is visible.
- If a value arrives already formatted, print it verbatim.
- State that the result is modeled and depends on returned assumptions; do not call it a forecast or guarantee.

Fallback when rich cards/charts are unavailable:

| Horizon | Projected value | Assumptions shown |
|---|---|---|
| 5 years | $1,250,000 | Returned assumptions |
| 10 years | $1,480,000 | Returned assumptions |

## Projection range or fan chart

Use only when lower/base/upper ranges, confidence bands, scenario bands or percentiles are returned.

- Center path: base or median returned value.
- Range: lower and upper returned values; label both.
- Bands: use a subtle categorical fill at lower opacity for each returned subject. The center path uses the matching categorical slot at full stroke weight.
- When multiple projections are returned, render one fan per subject or directly labeled overlapping bands only when labels remain legible. Do not rely on colour alone.
- Horizon cap: Advisor Center wealth projections are capped at 10 years. Do not render or imply a longer path.
- Do not invent confidence levels or missing bounds.

Fallback when rich cards/charts are unavailable:

| Horizon | Lower | Base | Upper |
|---|---|---|---|
| 10 years | $900,000 | $1,200,000 | $1,500,000 |

## Assumptions and fee treatment table

Use a compact table whenever assumptions, methodology fields or advisory-fee treatment are material to the answer. When rich cards are available, show advisory fee as a compact callout card near the performance or projection exhibit.

Fee callout anatomy:

1. **Label** — `Advisory fee`.
2. **Rate** — active rate applied, if visible.
3. **Treatment** — included, excluded, configurable, or not visible, using returned fields.
4. **Persistence note** — include only when explaining fee settings: non-zero fees persist; a zero-fee setting applies only to the current analysis.

| Field | Returned value | How to read it |
|---|---|---|
| Advisory fee | 0.75% | Applies to net modeled values when returned as included. |
| Time horizon | 10 years | Longest returned horizon. |
| Methodology | Returned methodology name | Use the linked methodology when provided. |

Rules:

- Include fee inclusion/exclusion/configurability when returned.
- If fee treatment is not visible, say `Fee treatment is not visible in the current output.`
- Do not reconstruct formulas or assumptions not returned.

## Unsupported configuration callout

Use a short callout for unsupported horizons, currencies, unavailable paths or route-only requests.

Callout anatomy:

1. **Status** — `Unavailable here` or `Route available`.
2. **What was requested** — one short phrase.
3. **Available path** — closest supported horizon, supported analysis path, or Advisor Center route when available.
4. **Limit** — what is not available in this chat or Advisor Center workflow.

Fallback when rich cards/charts are unavailable:

| Status | Request | Available path | Limit |
|---|---|---|---|
| Unavailable here | 100-year performance | Supported returned horizon | Longer history was not returned. |

## Methodology and source links

- Use returned methodology links only.
- If no methodology link is returned, say `No methodology link returned in the current response.`
- Use Advisor Center routes for workflow continuation when returned.
- Never build methodology or workflow URLs by pattern.

## Absent data

- Missing fee treatment: state that it is not visible.
- Missing projection range: show the returned path only; do not create a band.
- Missing realized history: state that realized client account history was not returned.
- Unsupported horizon: state the limit and closest supported path only when returned.

## Posture

- Say modeled performance, historical simulation, projected wealth or modeled outcome when those terms match the returned output.
- Do not present modeled output as realized client history.
- Do not call projected outcomes forecasts, predictions, likelihoods or guarantees.
- The data and methodology fields are Advisor Center outputs; the reading is generated; the decision is the advisor's.
