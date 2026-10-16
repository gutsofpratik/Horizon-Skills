# Rendering

The exact output anatomy for opportunity checks, fund-health detail and Funds to Explore rows. Visual primitives, colours, geometry and number formats come from `design-tokens.md`; this file names the blocks and rules for this skill.

## Mechanism

Render **inline in the conversation** using the richest form the host displays there:

1. The host's own inline visualization capability — cards, charts or components that render in the conversation itself.
2. Fallback when rich cards/charts are unavailable: markdown tables. Tables must carry the same labels and fields as the richer visual.

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
- Start with one sentence: `<n> opportunities flagged, <m> clear.` Add whether fund details or links are available only when returned.
- Keep every opportunity grounded in returned fields. Do not create checks, links, products or next steps that were not returned or listed as approved in `SKILL.md`.
- Put citations and links near the block they support. Link text is descriptive; never print a bare URL unless links do not render.

## Opportunity summary grid

Use a **3-column** equal-width grid for the opportunity summary when cards are available. Cards have no internal scrolling. Keep flagged cards first, then clear cards. Preserve returned order within each group unless severity, count, impact or materiality is returned.

Each card contains, in order:

1. **Status label** — `FLAGGED` or `CLEAR`, uppercase, bold, letter-spaced. Flagged uses the Warning/Critical status role indicated by returned severity; clear uses Good.
2. **Rule title** — returned title, weight 600, primary ink.
3. **One-line explanation** — one sentence from returned comment, value, threshold, count or comparison fields.
4. **Available path** — flagged cards only; returned route, fund-detail route, approved content link, or methodology link when available. For fund-health cards, use `Review flagged funds in this chat` as the primary path when any fund needs review or immediate attention. Hyperlink only true routes and content links. If the returned fund-health URL is a methodology page, label it `Fund health methodology` and show it as a secondary source link, not as the fund-detail path.

Card state rules:

- Every card is a status card per `design-tokens.md` § Status: the role's card wash
    across the card, its subtle border at `1px`. Flagged takes the returned severity
    role, clear takes Good.
- Clear cards are never blank; include returned value, threshold or comparison when available.
- Thresholds appear only for threshold-based checks.

Fallback when rich cards/charts are unavailable:

| Status | Opportunity | Portfolio observation | Available path |
|---|---|---|---|
| FLAGGED | High Cash Position | Cash is 20.0%, above the returned threshold. | Put cash to work |
| CLEAR | Drift from Benchmark | Drift is within the returned threshold. | None offered |

## One-line explanations

| Returned shape | Explanation shape |
|---|---|
| Threshold check with value | `<value> — above/below the <threshold> threshold.` |
| Portfolio-vs-benchmark signal | `Portfolio <value> vs. benchmark <value>, a <difference> difference.` |
| Count-based fund-health signal | `<count> funds returned fund-health flags.` |
| Returned comment only | Use the returned comment as-is or shorten without changing meaning. |

Do not write only `clear`. Do not imply action from a flagged state.

## Fund-detail cards

Use the standard fund-health card anatomy where fund-health detail overlaps: card grid, status dot plus words, name, meta, flag rows, divider, and tail rows.

Default to cards, not a full-width table, when the host can render cards. Use a
**4-column equal-width card grid** with wrapped rows for full fund-health lists. Do not
collapse fund-detail output into one full-width card per fund unless the host cannot
render a card grid or only one fund is returned. Apply the returned status to the whole
card as a status card per `design-tokens.md` § Status — the role's card wash and subtle
border — and still keep the status tag with dot plus words in the header.

For 20+ holdings, keep the visual surface. Flagged funds use full cards. On-track funds
may use compact status cards, but each compact card still shows ticker, category,
weight, a green `On track` status tag, and the Funds to Explore tail. Never replace the
fund-health visual with a plain ticker/category/weight markdown table when cards are
available.

Order cards by returned status: `consider_immediate_attention`, `consider_review`,
`on_track`, `unavailable`. Within a status, drivers fired descending, then returned
order. Each card contains:

1. **Header** — ticker or returned holding name; status tag with dot and returned status words.
2. **Name** — returned fund or security description when different from header.
3. **Meta** — category, weight, expense ratio, yield or as-of date when returned, joined with ` · `.
4. **Flag rows** — driver chips, one per returned driver, with finding icon; if no
    drivers are returned and the holding was judged, use a green status tag
    `✓ No drivers flagged`. If no verdict was returned, use a Neutral tag
    `— No verdict returned`.
5. **Tail rows** — returned Funds to Explore entries first, then methodology link,
   security link, fund link or Advisor Center route.

Cards must scale to at least four returned Funds to Explore entries per holding. Keep alternatives within the relevant fund card, preserve returned order, and use a compact row for each entry: label, returned name, returned note or metric, and hyperlink when returned.
Every card must show the Funds to Explore area: returned entries when present; `No
Funds to Explore returned` when absent. Never omit the area because the fund is clear,
because the card is in a full list, or because the response has many holdings.

The cards are the flagged-fund breakdown. After the grid, write at most three bullets:
first item to inspect, why it outranks the rest using returned metrics, and coverage
gaps. Do not write one paragraph per flagged fund.

Fallback when rich cards/charts are unavailable:

| Fund | Name | Status | Meta | Drivers | Funds to Explore |
|---|---|---|---|---|---|
| ABCD | Returned fund name | ● Consider review | Large blend · 3.5% · 13bps | ⚑ Returned driver | Funds to Explore · Returned fund |

Meta labels are explicit when space permits: allocation %, yield, expense ratio in bps, category, and as-of date. Do not show an unlabeled number in a fund card.

## Funds to Explore rows

Render portfolio alternatives as `Funds to Explore`, even when an upstream payload or older skill text uses another internal label. Each row uses only returned values:

- Label: `Funds to Explore`
- Value: returned fund, product or comparison candidate name
- Link: returned product, fund, security, methodology or Advisor Center URL when present, shown as descriptive hyperlink text with the link role from `design-tokens.md`
- Note: one short returned rationale or value when present

Do not rank a row as preferred. Do not create an alternative that was not returned.

## Link-outs and available paths

- Use Advisor Center routes for workflow continuation when returned.
- Use approved public links from `SKILL.md` only for the matching opportunity area.
- Link labels must name the actual destination. A methodology URL is always labeled as
    methodology, never as a fund-details tab, fund-detail route, or chat drilldown.
- For red or flagged fund-health opportunities, the first available path is in-chat
    review of the flagged funds. Methodology and source links are secondary.
- If an exact link is absent, write `No link returned for this item.` Do not build one by pattern.
- Table links use the link role from `design-tokens.md`; the markdown fallback uses markdown links.
- Do not finish an opportunity or fund-health response with no links if any Advisor
    Center route, methodology, security, fund, source, or product link was returned.

## Absent data

- Missing status: use Neutral / unknown and words `No verdict returned`.
- Missing path: write `None offered` in the path column.
- Missing metric: say the metric was not returned; do not infer zero.
- Empty opportunity set: write a short clear-state response and still identify that no opportunity checks were returned.

## Posture

- The data and returned comments are Advisor Center outputs; the reading is generated; the decision is the advisor's.
- Use comparison, consideration and available-path language.
- Do not present a flagged card as a directive.
