# Design tokens

The primitives every visual is built from: mechanism, colour, type, geometry, number
formats. Values and roles only — what each role means in a feature is decided by that
feature's rendering spec. Never use a colour absent from these tables. Colour applies
at rung 1 only.

## Mechanism

The spec says what to draw, never what to draw it with. Render **inline in the
conversation** using the richest form the host displays there:

1. **The host's own inline visualization capability** — a chart, component or artifact
   that renders in the conversation itself. Full palette and geometry apply.
2. **Fallback when rich cards/charts are unavailable: markdown tables**. Always works, no colour; labels and printed values
   carry every encoding.

Capability selection is mandatory. Before writing any markdown table fallback, decide
whether the current host can render an inline visual mark for this block. Use rung 1
when the host exposes any inline card, chart, component, or visualization channel. Use
markdown tables only when no inline visual channel exists, the inline render fails, or
the host explicitly cannot display that block's richer mark. Do not choose markdown
tables for speed, familiarity, or because the fallback example is easier to copy.

Excluded, because they have failed:

- **Raw HTML or SVG in the chat body** — escaped and shown as tags.
- **Box-drawing or bar art inside a code block** — the block is narrow and wraps.
- **Anything that opens outside the conversation** — a side panel, a file, a download.

Never describe the mechanism or a fallback to the reader.

## Typeface

Inherit the host's. Never set `font-family`, never ship or link a font.

## Ink, surface and chrome

| Role | Value |
|---|---|
| Primary text | `#000` |
| Secondary text | `#757575` |
| Disabled text | `#9e9e9e` |
| Surface | `#fff` |
| Page background | `#fafafa` |
| Card border | `#bdbdbd` |
| Divider, gridline, track, tooltip stroke | `#e0e0e0` |
| Axis line and ticks | `#757575` |
| Axis labels | `#000` |
| Plot band | `#000` at 5% opacity |
| Accent | `#ff4713` |
| Link | `#cb2600` |

Text always wears an ink token, never a series colour. Grid and axis are recessive; do
not strengthen them.

**Accent is interactive emphasis only** — an active legend item, a selected state —
never a data series. Series always take categorical slots.

## Categorical — identity

Thirteen slots, fixed order, assigned from 1, never cycled. Colour follows the entity,
never its rank. A feature that caps its categories folds the remainder into Other.

| Slot | Value | | Slot | Value |
|---|---|---|---|---|
| 1 | `#8f63bc` | | 8 | `#00a384` |
| 2 | `#008b5c` | | 9 | `#00a6f4` |
| 3 | `#ffce00` | | 10 | `#bf00b6` |
| 4 | `#fc9bb3` | | 11 | `#ff6d00` |
| 5 | `#cc0018` | | 12 | `#5d8e38` |
| 6 | `#6556ff` | | 13 | `#693aa0` |
| 7 | `#e74065` | | Other | `#616161` |

Every slot carries a direct label on the mark or its legend entry. Slots 2, 3 and 5
share hues with the status roles, so a categorical mark must never carry a status icon
or status words — the label is what says it is a category.

**Comparison series** take slots in the order the source app lists them: the reference
(benchmark or model) first on slot 1, the subject second on slot 2. A lone series takes
slot 1.

## Status — state

Always an icon **and** words; never colour alone.

| Role | Fill | Text and icon | Subtle background | Subtle border |
|---|---|---|---|---|
| Good | `#008b5c` | `#008b5c` | `#e5f5ed` | `#008b5c` |
| Warning | `#ffce00` | `#000` on fill, `#ffc300` icon | `#ffedb0` | `#ffce00` |
| Critical | `#cc0018` | `#d91120` | `#ffeaed` | `#d91120` |
| Informational | `#007ac9` | `#007ac9` | `#efe9f5` | `#8f63bc` |
| Neutral / unknown | `#616161` | `#313131` | `#e0e0e0` | `#e0e0e0` |

- Ink on a solid fill: `#fff`, except Warning which takes `#000`.
- A **status dot** is a filled circle in the role's fill, always followed by the words.
- Neutral means no state was determined: not a fifth severity, never Good.

## Financial direction

| Role | Text | Background | Series |
|---|---|---|---|
| Gain / increase | `#008b5c` | `#e5f5ed` | `#00a6f4` |
| Loss / decrease | `#d91120` | `#ffeaed` | `#f92f24` |

## Geometry

| Element | Rung 1 | Rung 2 (markdown fallback) |
|---|---|---|
| Bar | height `20px`, radius `4px` | `█` cells, **20 cells = the scale maximum**, minimum one cell for a non-zero value |
| Gap between stacked segments | `2px` surface colour | — |
| Track behind a paired bar | full width, gridline colour, same radius | `░` to 20 cells |
| Stat tile | card on page background, radius `8px`, padding `16px`; label `13px` secondary ink above, figure `24px` weight 600; tiles in one row, `12px` apart | a two-row table: labels, then figures |
| Column | width to fit, radius `4px` at the free end, `2px` gap within a pair, `24px` between groups; value label `12px` primary ink at the free end | one table row per category |
| Block label | `13px` secondary ink, sentence case, above the mark | bold line above the table |
| Legend | inline under the mark: `■` in the series colour, label in ink | the table's own column heads |
| Status dot | `10px` circle in the role's fill, `6px` before the words | `●` before the words |
| Status tag | `12px`, radius `4px`, `4px 8px` padding, role subtle background and border, role text; always icon plus words | words prefixed with `●` |
| Table link | link colour, weight 600, underlined, trailing ` ↗`, wraps freely | a markdown link |
| Table | header row weight 600 with a `1px` card-border rule beneath; rows parted by `1px` divider; `8px` cell padding; no fills | a markdown table |
| Card | `1px` card-border, radius `8px`, `12px` padding, surface fill, three across unless the feature spec names another column count | one row of a table |
| Side-by-side card | card `220px` fixed on the left, prose filling the rest, `24px` apart, both top-aligned; card `1px` card-border, radius `8px`, `16px` padding, surface fill | a table, then the prose beneath it |
| Pill | `12px`, radius `4px`, `4px 12px` padding, Informational subtle background and border, Informational text | bold words on their own line |
| Footnote | `12px` secondary ink | italic line under the table |
| Icons | finding `⚑` · clear `✓` · no verdict `—` | same |

Scale: shares of a whole 100% · paired bars the larger rounded up to the next 5% ·
columns span the data's minimum and maximum, each rounded outward to the next 5% (or
`$50K`) step, gridlines at every step, the zero line drawn.

## Links

- Rich rendering uses descriptive link text, the Link colour, underline, weight 600 and trailing ` ↗`.
- The markdown fallback uses standard markdown links with descriptive link text.
- Never print a raw URL as visible text unless links do not render.
- Do not build product, methodology, or workflow links by pattern. Use returned or approved links only.

## Numbers

**A value that arrived already formatted is printed verbatim** — never re-rounded or
restyled, even beside a figure you formatted differently. Sizing a bar from a formatted
figure is fine; ranking or totalling from one is not.

| Kind | Format |
|---|---|
| A rate or ratio held as a fraction | one decimal with `%` — `0.1261` → `12.6%` |
| Currency at or above a million | nearest thousand, thousands-separated |
| Currency below a million | nearest unit |
| A small fee or spread | basis points, integer |
| A count, rank or percentile | as-is |
| A date shown to a reader | day, month and year in words |

- Negatives take a minus sign, never parentheses. A value rounding to zero from below
  prints as zero.
- One precision per block. Unit named once, in the label.
