# Rendering

The exact output of the three sections: every block's anatomy, dimensions, strings and
fallback form. Colours and type sizes are roles in `design-tokens.md`; this file only names
them. Anything not specified here is not rendered. Never add, rename, reorder or
decorate a block, label or string.

## Mechanism

Render **inline in the conversation** using the richest form the host displays there:

1. The host's own inline visualization capability — charts, cards, tables or components
  that render in the conversation itself.
2. Fallback when rich cards/charts are unavailable: markdown tables. Tables must preserve the same labels and values as the
  richer visual.

Capability selection is mandatory. Before writing any markdown table fallback, decide
whether the current host can render the specified inline visual mark for the block. Use
the richer mark when any inline chart, card, component, or visualization channel is
available. Use markdown tables only when no inline visual channel exists, the inline
render fails, or the host explicitly cannot display that block's richer mark. Do not
choose markdown tables for speed, familiarity, or because the fallback example is
easier to copy.

Do not render into a document, canvas, webpage, side panel, file, or download. Do not
use raw HTML, raw SVG, or box-drawing art. Never describe the mechanism or fallback to
the advisor.

## Page

- Heading levels: header `##`, sections `###`. Nothing else is a heading.
- The section heading is the **first thing written** in a section, before any
  tool call that emits its visual, in the exact wording and capitalisation
  given at that section's own heading below. A heading written after the visual
  renders beneath it, which is wrong. Order of writing is order of appearance.
- Vertical rhythm: `24px` between blocks · `8px` between a block label and its mark ·
  `4px` between a mark and its legend · `16px` before prose.
- Every block is: **label** (secondary ink, sentence case, the exact string given
  below) → **mark** → **legend** where specified. Never append qualifiers to a label.
- Prose under a section: the **bold lead** — one sentence, at most 20 words, the verdict
   — then plain-weight bullets as each section specifies. No other paragraphs,
  except the closest model template in the closing.
- The section's citations are its **last lines**, one per link, exact form:
  `Open in Advisor Center here.` then `Methodology here.` when present, each
  with `here` as a table link to its URL. Never print a URL as visible text
    anywhere; the words carry the link.
- At the markdown fallback a link is a markdown link. Where links do not render at
  all, print the URL in full after the words.
- The only other links anywhere are a rule's own `recommendation_link`, as the
  table link in the observations table, an idea's own `product_url` on the fund
  card tail, and the closest model's `comparison_url` in the closing.

## Header

```
## Summary Analysis — <subject name>
<value> · <n> holdings · <tax status> · analytics as of <day month year>
```

- Line 2 is secondary ink at rung 1, plain text in the markdown fallback. Drop any part not carried;
  keep the ` · ` separators between the parts that remain.
- `<value>` per the currency format. Household: `<n> accounts · <n> holdings`. Model: no
  value, no holdings.
- The as-of date appears **here only**: from the step-1 response, else
  `get_analysis_date`. Header and section 1 render together once `analyze_portfolio`
  returns.

## Blocks

### Stat tiles

One row, tiles of equal width filling the row, `12px` apart, never wrapping. Each tile
is a card on the page background: label above, figure below, both left-aligned. A tile
holds one figure, or two joined by ` / ` when its label names both in the same order.
No borders, no icons, no sparklines.

Fallback when rich cards/charts are unavailable — a two-row table, column heads are the tile labels:

| Total value | Holdings | Total risk | Top 5 |
|---|---|---|---|
| $850,000 | 10 | 18.4% | 54.2% |

### Stacked bar

- Bar: full width, bar height, the two outer ends rounded, segments square between,
  `2px` surface gap between segments.
- Segment width = the slice's own formatted figure as a percentage of the bar. Any width
  not covered by shown segments is track colour — never stretch segments to fill.
- Segments in response order on slots 1–5; the `Other` segment on the Other colour.
- Legend beneath, one wrapping line, entries `■ <name as returned> <formatted figure>`
  separated by `16px`; the `Other` entry is `■ Other` with no figure.

Fallback when rich cards/charts are unavailable — one row per slice, column heads exactly as shown, bar = round(share ÷ 100 × 20)
cells, minimum one:

| Asset allocation | Share | Bar |
|---|---|---|
| Equity | 92.90% | ███████████████████ |
| Fixed Income | 7.10% | █ |
| Other | | |

### Paired bars

Two rows. Each row: label `160px` left-aligned in primary ink · track filling the
remaining width in track colour · fill from the left, bar height, radius at both ends ·
value `56px` right-aligned. Row 1 is the reference on slot 1, row 2 the subject on slot
2. Scale: the larger value rounded up to the next 5% = full track. Only when a
reference was named — never invent one.

Fallback when rich cards/charts are unavailable:

| Total risk in context | Total risk | Bar |
|---|---|---|
| `<benchmark name>` | 13.8% | ██████████████░░░░░░ |
| This portfolio | 18.4% | ████████████████████ |

### Column chart

- Plot: `280px` tall, full width. Y-axis `56px` at the left with tick labels in
  secondary ink right-aligned to the axis. Gridline at every step; the zero line in axis
  colour. No x-axis line.
- Scale: from the data minimum to the data maximum, each rounded outward to the next
  step; step `5%` or `$50K`. If all values share a sign, the zero line is the plot's top
  (all negative) or bottom (all positive).
- Categories equally spaced left to right in the order given. Column width `60%` of the
  category slot for one series; for two, each column `28%` of the slot with a `2px` gap,
  reference left on slot 1, subject right on slot 2.
- Every column: radius at its free end; value label at `4px` beyond the free end
  (below a negative column, above a positive one), primary ink.
- Category name beneath the slot, centred, secondary ink, never wider than its slot,
  wrapping to at most three lines. A name that still does not fit is not truncated:
  the plot keeps every character, so the name may run to a fourth line rather than
  lose text.
- Legend below the plot, left-aligned, only for two series: `■ <reference name>` `16px`
  `■ <subject name>`.

Fallback when rich cards/charts are unavailable — one row per category, columns in series order; a lone series has one value
column headed `This portfolio`:

| Scenario | `<benchmark name>` | This portfolio |
|---|---|---|
| Recession (2007-09) | -38.5% | -41.2% |

### Opportunity cards

Grid of three equal columns, `12px` gaps, rows as needed; cards top-aligned and
stretched to the row's tallest. Use for fired opportunity signals and, when returned,
clear opportunity checks. Do not make this a markdown table when the host can render
cards.

Card: radius `8px`, padding `12px`, filled with the status role's card wash and
bordered `1px` in its subtle border — the returned severity for a flagged signal,
defaulting to Warning; Good for a clear check. Inside, top to bottom, `6px` apart:

1. **Status label** — `FLAGGED` or `CLEAR`, uppercase, weight 600, letter-spaced.
  Flagged uses the returned severity role, defaulting to Warning. Clear uses Good.
2. **Opportunity** — returned title, weight 600, primary ink.
3. **Portfolio observation** — returned comment. When `contributors` is non-empty, add a
  secondary line `<ticker> <amount>` per contributor, comma-separated.
4. **Available path** — returned alternative, route or content link. Link text from the
  returned alternative field; target `recommendation_link` printed verbatim, never
  rewritten or shortened. For fund-health opportunities, use `Review flagged funds in
  this chat` as the primary path when any fund needs review or immediate attention. If
  the returned URL is a methodology page, label it `Fund health methodology` and show it
  as a secondary source link, not as the available path. No returned path: `None
  offered`.

When clear checks are not returned, do not claim a clear count. Say only which rules
were flagged.

Fallback when rich cards/charts are unavailable:

| Status | Opportunity | Portfolio observation | Available path |
|---|---|---|---|
| FLAGGED | High Cash Position | Your portfolio currently holds higher-than-average cash allocation of 20.00% | [Put cash to work](<recommendation_link>) |

### Cards

- Grid of three equal columns, `12px` gaps, rows as needed; cards top-aligned and
  stretched to the row's tallest.
- Card: card-border `1px`, radius `8px`, padding `12px`, surface fill. Inside, top to
  bottom, `6px` apart:
  1. **Header** — identifier left, weight 600; status dot and words right, `12px`,
     both top-aligned with the identifier, `8px` between them. The status wraps
     to as many lines as it needs, each line right-aligned; the dot stays on the
     first line with the first word. Never truncate the words, never shrink them
     below `12px`, never let them overlap the identifier.
  2. **Name** — secondary ink.
  3. **Meta** — secondary ink, parts joined by ` · `.
  4. **Flag rows** — one per line: icon, space, text.
  5. **Divider** — `1px` divider colour, `8px` above and below.
  6. **Tail** — one line per item.

Fallback when rich cards/charts are unavailable — one row per card:

| Fund | Name | Status | Meta | Drivers fired | Funds to Explore |
|---|---|---|---|---|---|
| **{ticker}** | {description} | ● Consider review | Real estate · 3.50% · 13bps | ⚑ Higher downside capture | Funds to Explore · {value} |

### Closest model

This block is a **mark**, not prose: render it at rung 1 per
`design-tokens.md` § Mechanism, in the same inline visualization the other
blocks use. The left side is the model card; the right side is the comparison
prompt. The fallback table below applies only when rung 1 is unavailable —
never as the default because the block sits in the closing. Never render closest
model as a sentence followed by a markdown table when cards are available.

Two columns, `24px` apart: the model card at `220px` fixed on the left, comparison
prompt prose filling the rest on the right, both top-aligned.

- **Card** — card-border `1px`, radius `8px`, `16px` padding, surface fill.
  Inside, top to bottom:
  1. **Pill** — `Closest fit`, `12px`, Informational subtle background,
     Informational subtle border, Informational text, radius `4px`,
     `4px 12px` padding.
  2. **Name** — `<name>`, weight 600, primary ink, `8px` below the pill.
  3. **Rows** — five lines, `12px` apart, label left in secondary ink, value in
     primary ink filling the rest of the row with every line of it flush right,
     including when it wraps. The label never wraps; the value wraps instead.
     Exact labels and order:
     `Model split` `<short_name>` · `Risk profile` `<risk_profile>` ·
     `Objective` `<objective>` · `Vehicles` `<family_vehicle>` ·
     `Rebalance` `<family_trade_frequency>`.
     Omit a row whose value is absent; never a blank or a dash.
- **Comparison prompt prose** — no table. Print the filled template below verbatim.
  Beneath it, an **action button** per `design-tokens.md` § Geometry, labelled exactly
  `Run side-by-side comparison in this chat.`, whose click sends that label into the
  conversation as the advisor's next message. It is a button, never a line of prose,
  never a link. The Advisor Center link is secondary:
  only when `closest_model.comparison_url` is returned, add `Open comparison in
  Advisor Center here.` with `here` as a table link. Never print the URL as visible
  text; the bare URL is what wrecks the block's width.
- `risk_profile`, `objective`, `family_vehicle` and `family_trade_frequency`
  arrive lower-case, from the `list_models` row and never from
  `closest_model`. Capitalise the first word only; print `ETF`, `MF` and `SMA`
  upper-case. So `moderate aggressive` → `Moderate aggressive`,
  `etf only` → `ETF only`. The template's own words are not restyled.

Template, filled and printed exactly:

Within the BlackRock '<family>' model family, the closest match on your
portfolio's equity/fixed-income split is the '<name>' — '<short_name>' against your
'<equity_pct>'/'<fixed_income_pct>'. The match is on the split only, not the
underlying holdings. Do you want to run a side-by-side comparison in this chat?

Primary action: Run side-by-side comparison in this chat.

Secondary source link, when returned: Open comparison in Advisor Center here.
(here → closest_model.comparison_url)

Fallback when rich cards/charts are unavailable — the model card as one two-column
table, then the template and primary action as plain text beneath. Do not use a wide
summary table.

| Closest fit | BlackRock Target Allocation ETF 80/20 Model |
|---|---|
| Model split | 80/20 |
| Risk profile | Moderate aggressive |
| Objective | Aggressive |
| Vehicles | ETF only |
| Rebalance | Quarterly |

Within the BlackRock '<family>' model family, the closest match on your portfolio's
equity/fixed-income split is the '<name>' — '<short_name>' against your
'<equity_pct>'/'<fixed_income_pct>'. The match is on the split only, not the underlying
holdings. Do you want to run a side-by-side comparison in this chat?

Primary action: Run side-by-side comparison in this chat.

Secondary source link, when returned: Open comparison in Advisor Center here.


## 1. Portfolio snapshot

Order, exact block labels:

1. Stat tiles (no label)
2. Benchmark tiles — **only when the advisor named a benchmark**
3. `Asset allocation` stacked bar
4. `Risk by account` stacked bar — **household only**
5. `Equity — geographic exposure` stacked bar
6. `Total risk in context` paired bars — **only when the advisor named a benchmark**
7. Bold lead, then up to three bullets in this order, each only when its block rendered:
   allocation · equity geography · total risk against the benchmark. Then citations.

**Stat tiles** — drop any tile whose figure is absent; never re-space to hide the gap:

| Subject | Tiles, in order | Figure source and format |
|---|---|---|
| Saved portfolio | `Total value` · `Holdings` · `Total risk` · `Top 5` | step-0 record currency · integer · `total_risk` fraction → one decimal % · five largest fractions summed → one decimal % |
| Household | `Total value` · `Accounts` · `Holdings` · `Total risk` | as above; accounts integer |
| Model | `Total risk` | as above |

`Top 5` renders **only when the step-0 record carries per-holding weights**.

**Benchmark tiles** — a second row: `Benchmark` (the name as listed) ·
`Equity split (portfolio vs benchmark)` (`<subject equity>% / <benchmark equity>%`, each
the equity slice's formatted figure from its own `analyze_portfolio` response).

**Stacked bars**

- Slices are `asset_allocation`, `account_contributions`, `regions` respectively, in
  response order. Omit any slice whose magnitude is below `0.05%`.
- The first five shown slices take slots 1–5. Any further slices, and any returned slice
  itself named *Other*, merge into one `Other` segment with no figure.
- `Risk by account` labels each segment from the member entries in
  `list_household_portfolios`. No name for an id: no legend entry, never the id.
- Never a status icon or status word on a slice, whatever its hue.

**Total risk in context** — row 1 `<benchmark name>` with the benchmark's `total_risk`
from the second `analyze_portfolio` call; row 2 `This portfolio` (`This household` /
`This model`) with the subject's.

## 2. Scenarios

Order: `Scenario impact on portfolio value (<unit>)` column chart · value-basis note ·
observations per `SKILL.md` § Step 2 · citations.

- `<unit>` is `$K` when `value_base_source` is `nav` and no benchmark is named, else `%`.
  Dollar columns are sized on `impact_value`, tick labels `$0`, `-$50K`, …, value labels
  two lines: the full currency figure, then the formatted `impact` in parentheses
  beneath it, verbatim, centred on the column, `2px` apart, both primary ink.
  Percent columns are sized on the numeric field and labelled with the formatted
  `impact` verbatim, one line, no parenthetical.
- Categories most-negative first on `impact_value`, named by `display_name`.
- **Benchmark named**: two series, `benchmark_impact` on slot 1 and `impact` on slot 2,
  both absolute, legend `■ <benchmark name>  ■ <subject name>`. `relative_impact` is
  quoted in observations, never drawn.
- **At most ten categories.** More returned: the ten largest magnitudes, and directly
  beneath the chart the line `<n> further scenarios not shown.` Never omit a
  positive-impact row that falls inside the ten.
- `value_base_source` = `default`: the line `Dollar impacts use an illustrative
  investment amount, not this portfolio's value.` directly beneath the chart.

## 3. Opportunities, fund health, Funds to Explore

Order: bold lead · opportunity cards · fund-health card grid · footnote · commentary per `SKILL.md`
§ Step 3 · citations.

- **Lead** when `signals` is empty: exactly `**Nothing flagged.**` When not: `**<n> rules
  flagged.**` (`**1 rule flagged.**`). If clear checks are not returned, do not add a
  clear count.
- **Opportunity cards** — one card per signal, response order; omitted entirely when
  `signals` is empty. Use the card anatomy under § Blocks. Do not render these as a
  table unless rich cards/charts are unavailable.
  - `Opportunity`: `title`.
  - `Portfolio observation`: `comment`; when `contributors` is non-empty, a second line
    in secondary ink `<ticker> <amount>` per contributor, comma-separated.
  - `Available path`: link text from the returned alternative field, target `recommendation_link` printed
    verbatim, never rewritten or shortened. For fund-health opportunities, use `Review
    flagged funds in this chat` as the primary path when any fund needs review or
    immediate attention. If the returned URL is a methodology page, label it `Fund
    health methodology` and show it as a secondary source link. No returned path: `None
    offered`.
  - `value`, `threshold_low`, `threshold_high`, `breach_threshold` are not shown; the
    comment carries the figure. Cite them in commentary.

- **Fund-health cards** — use full cards for flagged funds and compact status cards for
  on-track funds when needed. The card grid itself is the flagged-fund breakdown; do not
  follow it with one paragraph per flagged fund.
- **Commentary** — at most three bullets after the visuals: first item to inspect, why
  it outranks the rest using a returned metric, and coverage gaps. Do not restate every
  driver in prose; the cards already show them.

**Cards** — one per fund in `funds`, rendered as a 4-column equal-width card grid when
the host supports cards. Use wrapped rows for long lists. Do not collapse to full-width
fund cards unless the host cannot render a card grid or only one fund is returned. Tint
the whole card with the returned status's subtle background and border while still
showing the status dot and words in the header. Order: `consider_immediate_attention`,
`consider_review`, `on_track`, `unavailable`; within a status, drivers fired descending,
then `funds` order.

For 20+ holdings, still use the card grid. Flagged funds use full cards. On-track funds
may use compact status cards, but each compact card still shows ticker, category,
weight, a green `On track` status tag, and the Funds to Explore tail. Never replace the
fund-health visual with a plain ticker/category/weight markdown table when cards are
available.

| Part | Exact content |
|---|---|
| Header left | `ticker`; else `description`; both absent: `Unidentified holding` |
| Header right | status tag with dot in the role's fill + words: `consider_immediate_attention` → Critical, `Consider immediate attention` · `consider_review` → Warning, `Consider review` · `on_track` → Good, `On track` · `unavailable` → Neutral, `No verdict` |
| Name | `description`; omitted when absent or already used as the header |
| Meta | `<category> · <weight as returned> · <expense ratio>bps · <yield>% yield` — omit absent parts. Expense ratio arrives in percent; print integer bps (`0.03` → `3bps`) |
| Flag rows | driver chips, one per driver that fired: `⚑` in the driver's `severity` role icon colour, then the driver's own label. None and judged: green status tag `✓ No drivers flagged`. None and `unavailable`: Neutral tag `— No verdict returned` |
| Tail | one line per idea: `Funds to Explore · <value>`, the `value` as a table link to the idea's `product_url` printed verbatim. No `product_url`: the `value` plain. None: `No Funds to Explore returned`. The tail is mandatory on every card, including clear funds and full-list requests. |

**Footnote** — secondary ink, one line, only the parts that apply, in this order:
`<n> non-fund holdings and <m> unresolved holdings sit outside fund health.` ·
`<k> funds returned no verdict.`

## Closing

In this order: **Caveats** (bullets per `SKILL.md`) · **Closest model** — the block
under § Blocks, only when step 1 carried one · **Follow-ups** per `SKILL.md`
§ Closing, ending with `Say which of those you want and I'll run it on this portfolio.`
Do not mention report generation, PDFs, or Generate Report in the closing unless the
advisor asked for a report.

## Citing and attributing

- Each link sits at the end of the section that used it, in the exact form under
  § Page. Every link in the review is a table link on its own words, never a
  visible URL — including the closing's closest-model link.
  Never paraphrase a link away, never build a URL by pattern. Add after the
  comparison link, once per review, in section 1: `That view renders live under its own
  analysis date and fee settings, so its figures can differ from these.`
- A returned Advisor Center, comparison, methodology, fund or product link is never
  optional decoration. Surface it near the visual it supports. If section 1 returns
  `comparison_url`, the review must contain at least one `Open in Advisor Center here.`
  link.
- Link labels must name the actual destination. A methodology URL is always labeled as
  methodology, never as a fund-details tab, fund-detail route, or chat drilldown. For red
  or flagged fund-health opportunities, the first path is reviewing the flagged funds in
  chat; methodology and source links are secondary.
- The figures are the platform's. The reading is yours. The decision is the advisor's.
  Attribute an upstream comment, verdict or alternative **to upstream**,
  in its own words, and say it is unvetted against the advisor's constraints.
- Never credit the data provider with a conclusion it did not draw.

## Absent data

- Omit the tile, row, segment or column; never a blank, a dash or a zero-length mark.
- Show what came back; **name what did not**, in the footnote or a bullet. Keep every
  section — omitting one reads as a clean result. An empty result set is a finding.
- Never infer an unreturned value. *Not returned* ≠ *returned as zero or none*.
- A positives-only response cannot support a claim about what was checked and passed.
- Two verdicts that disagree in one visual are information, not an error. Never
  reconcile them.
