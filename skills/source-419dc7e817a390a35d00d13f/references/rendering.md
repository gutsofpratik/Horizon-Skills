# Rendering Reference

Layout structure, panel specifications, CSS scaffold, and formatting rules for the HTML
report. All panels reference the brand tokens resolved per `references/brand-tokens.md`.

## Layout Structure

Both report types share the same structural template. The Financial Performance table must
always be **directly above** the Valuation Summary table in the same column.

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER — Logo · Company · Fund · Sector · HQ · Report date    │
│           Tag pills: sector, geography, fund, status           │
├─────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 cards, full width)                               │
│  LTM Revenue | LTM EBITDA | Enterprise Value | Net Debt | MOIC │
├───────────────────────────┬─────────────────────────────────────┤
│  LEFT COLUMN              │  RIGHT COLUMN                       │
│                           │                                     │
│  Financial Performance    │  Revenue & EBITDA Bar Chart         │
│  Table                    │  (last 4 LTM periods, SVG inline)  │
│                           │                                     │
│  Valuation Summary        │  Investment Returns Table           │
│  Table  ← must stay here  │                                     │
│                           │                                     │
├───────────────────────────┴─────────────────────────────────────┤
│  COMMENTARY (full width, up to 3 columns)                      │
│  Business Update | Valuation Rationale | Discount Rationale    │
├─────────────────────────────────────────────────────────────────┤
│  FOOTER — © {firm_name} | {website} | {confidentiality_label} │
└─────────────────────────────────────────────────────────────────┘
```

## Panel Specifications

### Header Strip

- Background: `bg_header` → `bg_primary` gradient, 135°
- **Logo:** if `logo_url` is set, render `<img src="{logo_url}">` at `logo_position`;
  maintain clearspace equal to the cap-height of the firm name on all sides
- **Logo fallback:** if `logo_url` is blank, render firm name in `font_heading`,
  `font_heading_weight`, 24px, `text_primary`
- Company name: `font_heading`, 28px, `accent_primary`
- Subtitle (fund · sector · HQ · date): `font_body`, 12px, `text_muted`
- Tag pills: `bg_secondary` fill, `accent_secondary` border, `font_body` 10px

### KPI Strip (5 cards)

| Card | Value |
|---|---|
| LTM Revenue | Current period revenue |
| LTM Adj. EBITDA | Valuation basis if available, else Reported |
| Enterprise Value | Current quarter EV |
| Net Debt | Current quarter net debt |
| Gross MOIC | Blended or primary investment MOIC |

- Card: `bg_secondary` background, 6px border-radius, `box-shadow: 0 2px 8px rgba(0,0,0,0.4)`
- Value: `font_heading`, 28px, `accent_primary`
- Label: `font_body`, 9px, uppercase, letter-spacing 0.05em, `text_primary`
- Delta: `▲ +X%` in `accent_positive` · `▼ -X%` in `accent_negative`

### Financial Performance Table (LEFT column, top)

Rows (LTM, 3 prior periods + current quarter, vs. PY column):

| Row | Notes |
|---|---|
| Revenue | |
| Gross Profit | |
| Gross Margin % | |
| EBITDA | |
| EBITDA Margin % | |
| **Adj. EBITDA (Valuation)** | Highlight row — `font_heading`, `accent_primary` value |
| **Adj. EBITDA Margin %** | Highlight row |
| Net Debt | |

- Header row: `table_header_bg`, `font_body` 9px uppercase, `text_primary`
- Alternating rows: `bg_secondary` / `bg_primary`
- Highlight rows: `rgba({accent_primary}, 0.06)` background
- Numeric columns right-aligned; label column left-aligned

### Valuation Summary Table (LEFT column, directly below Financial Performance)

| Row | Notes |
|---|---|
| Valuation Multiple | `X.Xx` |
| Adj. EBITDA (LTM) | currency |
| **Enterprise Value** | Highlight row |
| Total Debt | |
| Cash | |
| Net Debt | |
| **Total Equity Value** | Highlight row |

Prior Quarter vs Current Quarter, plus a delta column (`accent_positive` / `accent_negative`).

### Revenue & EBITDA Bar Chart (RIGHT column, top)

- **Inline SVG only** — no external JS or D3
- Side-by-side bars: Revenue in `accent_secondary`, Adj. EBITDA in `accent_negative`
- Current quarter Revenue bar: `accent_primary`
- 4 LTM periods on x-axis; `$Xm` labels above each bar
- Current quarter label: `font_heading`, `accent_primary`; prior: `font_body`, `text_muted`
- Y-axis gridlines: dashed, `rgba({accent_primary}, 0.08)`
- Legend: colour swatches + labels, `font_body` 9px
- Auto-scale: y-axis max = largest revenue × 1.2; bar heights proportional

### Investment Returns Table (RIGHT column, bottom)

| Column | Format |
|---|---|
| Investment name | Left-aligned |
| Entry date | `Mon YYYY` |
| Ownership % | `X.X%` |
| Cost (Gross) | `$Xm` |
| Realized | `$Xm` |
| Unrealized | `$Xm` |
| MOIC (Gross) | `X.XXx` — `font_heading`, `accent_primary` |

- Sort: largest cost first
- **Total / Blended** row at bottom in `font_heading`
- Add IRR column if available; omit column if all values null
- Unavailable values: `—`
- One-sentence QoQ note below table: `font_body` 9.5px, `text_muted`

### Commentary Section (full width, up to 3 columns)

1. **Business Update** — verbatim from model if present; AI-generated in MCP mode
2. **Rationale for Valuation Conclusion** — verbatim from model if present
3. **Rationale for Discount to Comps** — verbatim from model if present

- Eyebrow label: `accent_primary`, 9px, uppercase, letter-spacing 0.08em,
  1px bottom border in `accent_primary`
- Body: `font_body`, 11px, `text_muted`, line-height 1.6
- Collapse empty columns — never show a blank block

## CSS Variables & Font Loading

Populate these from the resolved brand tokens. Set once in `<style>`; all panels inherit
automatically.

```html
<!-- In <head> -->
<link href="{google_fonts_url}" rel="stylesheet">

<style>
:root {
  --bg-primary:        {bg_primary};
  --bg-secondary:      {bg_secondary};
  --bg-header:         {bg_header};
  --accent-primary:    {accent_primary};
  --accent-secondary:  {accent_secondary};
  --accent-negative:   {accent_negative};
  --accent-positive:   {accent_positive};
  --text-primary:      {text_primary};
  --text-muted:        {text_muted};
  --table-header-bg:   {table_header_bg};
}

body {
  font-family: '{font_body}', sans-serif;
  font-weight: {font_body_weight};
  background: var(--bg-primary);
  color: var(--text-primary);
  margin: 0;
}

h1, h2, h3, h4, .eyebrow, .kpi-value, .moic-value {
  font-family: '{font_heading}', sans-serif;
  font-weight: {font_heading_weight};
}
</style>
```

## Formatting Rules

| Type | Format |
|---|---|
| Currency (millions) | `$43.5m` |
| Negative / net cash | `($3.4m)` in `var(--accent-negative)` |
| Multiples | `1.41x` |
| Percentages | `15.7%` |
| Basis point changes | `+70bps` |
| Dates | `Q4 2024` or `31 Dec 2024` |
| MOIC | `4.97x` — heading font, `var(--accent-primary)` |
| Positive delta | `▲ +X%` — `var(--accent-positive)` |
| Negative delta | `▼ -X%` — `var(--accent-negative)` |
| Unavailable | `—` (em dash) — never fabricate |
