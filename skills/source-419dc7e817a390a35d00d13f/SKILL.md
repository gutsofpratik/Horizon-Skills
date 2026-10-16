---
name: chronograph-portfolio-company-one-pager
description: >
  Generate one-pagers and investor reports for private equity portfolio companies. Handles live data
  fetching via the Chronograph MCP OR an uploaded Excel model, metric formatting, AI-generated or
  model-sourced commentary, and rendering a fully styled HTML one-pager.
when_to_use: >
  Use whenever a user asks to generate a company tearsheet, one-pager, investor report, portfolio
  overview, or company deep-dive — especially when they name a company or ask to "build a report",
  "create a one-pager", or "show me a tearsheet". Also trigger when the user asks to include
  commentary, quarterly updates, investment narratives, or any Investment Overview in the report
  output. Also trigger for LP quarterly updates, valuation summaries, and portco performance pages —
  any output that combines financials, valuation, and return data for a single portfolio company.
  This is a GP-side report that needs GP-level data (company financials and per-investment gross
  returns). Not for LP portfolio cashflow or pacing analysis (use chronograph-cashflow-forecast) or
  LP fund-meeting prep (use chronograph-gp-meeting-prep).
---

# GP Report Builder

Generates a fully styled, self-contained HTML investor report for a named portfolio company.
Supports two data source modes, two report types, and automatic brand detection from uploaded
templates. **Read this skill and its references fully before writing a single line of HTML.**

**Requirements:** A connected Chronograph MCP server as a GP client. These workflows are designed for
permissioned Chronograph users to connect to their private investment data, or an uploaded
Excel model for Model mode.

This SKILL.md is the orchestration layer. Two references carry the bulky detail — load each
when you reach the step that needs it:

- `references/brand-tokens.md` — branding resolution: template extraction, Chronograph
  defaults, the full brand token schema, theme handling, and the user confirmation line.
- `references/rendering.md` — layout structure, all panel specifications, the CSS variable
  scaffold, and the formatting ruleset.

---

## Step 0 — Resolve Branding

Brand tokens are resolved automatically — the user never fills in a config file manually.
Follow `references/brand-tokens.md` end to end:

1. **Check the conversation for an uploaded brand template** (HTML/CSS, PDF, image, PPTX,
   design tokens). If present, extract its colors, fonts, logo, and footer text. Most recent
   file wins on conflict.
2. **If no template is present, apply the Chronograph defaults silently** — do not ask for
   branding.
3. **Resolve every token in the Brand Token Schema** (from the template or the defaults),
   including the dark/light theme determination and contrast handling.
4. **Confirm in a single short line** before generating (or ask one focused question if brand
   detection was low-confidence). Do not ask if defaults were applied.

---

## Step 1 — Determine Report Mode

**Data source mode:**

| Signal | Mode |
|---|---|
| User uploads an Excel model (.xlsx) or references an uploaded file | **Model mode** — read data from the file |
| No file uploaded; company exists in the connected data platform | **MCP mode** — fetch live from the platform |
| Both available | Prefer the model for financials and commentary; use MCP to supplement metadata and returns |

**Report type:**

| User asks for… | Report type |
|---|---|
| One-pager, tearsheet, company report, GP report | **GP One-Pager** |
| LP update, quarterly update, LP quarterly report | **LP Quarterly Update** |

If unclear, default to **GP One-Pager**.

---

## Step 2 — Resolve the Company & Fetch Data

### MCP Mode

All data is fetched from the user's connected **Chronograph MCP server**. The agent must have
the Chronograph MCP connected before running the skill in MCP mode; if it isn't connected,
prompt the user to connect it, or fall back to Model mode if a file is available.

**GP access required.** This report needs GP-level data — company financial line items and
per-investment **gross** returns — that the Chronograph MCP exposes only to GP-authenticated
identities. If the connected identity does not expose those tools (for example, an LP/investor
login), stop and tell the user this report requires GP access. Treat missing GP tools as an
access-type mismatch, not ordinary missing data: do not produce an empty report filled with
`—`, and never substitute LP-level net figures. If the user only has LP access, point them to
`chronograph-cashflow-forecast` or `chronograph-gp-meeting-prep`.

Inspect the connected Chronograph MCP's tool list at runtime and pick the appropriate tool for
each step below based on the tool descriptions the server provides. Do not hard-code tool
names — read the live descriptions to stay current.

### Fetch sequence

Work through these steps in order. At each step, identify the right Chronograph tool from its
description, call it to fetch what the report needs, and hold the result for the rendering
steps that follow. The skill does not need a fixed schema — only the values listed below in
plain language.

**1. Resolve the company.** Find the tool that searches for companies, funds, and other
portfolio entities by name. Use it to turn the user's input into a canonical company. If
multiple candidates come back, prefer the closest name match; ask the user only if genuinely
ambiguous.

**2. Get the company's basic facts.** Use the tool that retrieves core portfolio entity
records. Fetch what the **Header Strip** needs: company name, sector, industry, geography, HQ,
and the company's reporting currency. Request only what the header renders — the tool's
description will list what's available.

**3. Get the company's investments.** Using the same core-entity retrieval tool, fetch the
list of investments associated with the company. The **Investment Returns Table** needs one
row per investment: investment name, the fund it belongs to, entry date, exit date if
applicable, and whether it has exited.

**4. Get the company's financial line items.** Find the tool for company-level financial
metrics. Make a discovery / help call first, passing the company ID, to see what's available.

**Metric selection rule.** Always query by the platform's metric type when one is available
for the line item — even if the company's display label differs. Use a company-specific mapped
metric definition only when no metric type covers the line item or the request is inherently
tenant-specific (bespoke KPIs, commentary fields, operating metrics, custom valuation inputs).

Priority:

1. Platform metric type
2. Company-specific mapped metric definition (only if no metric type exists)
3. Name-based metric search (only if neither of the above resolves)

Do not pick a company-specific metric because its label is a closer word match than an
available metric type. Metric types drive querying; display labels drive presentation.

What the report needs (query via the metric type whenever available):

- **Financial Performance Table:** Revenue, Gross Profit, EBITDA, the company's adjusted
  EBITDA series, and Net Debt. Pull the last 4–5 trailing-twelve-month periods plus the most
  recent quarter.
- **Valuation Summary Table:** Enterprise Value, valuation multiple, Total Debt, Cash, Net
  Debt, Equity Value — current quarter and prior quarter.
- **KPI Strip:** the latest values for LTM Revenue, LTM Adj. EBITDA, Enterprise Value, and Net
  Debt.

Use LTM for income-statement items, As-of for balance items. The discovery response will tell
you which period types are supported per metric.

**5. Get per-investment returns.** Find the tool for investment-level performance. It uses
gross performance figures (not net — net lives elsewhere on the platform and is the wrong tool
for the GP one-pager). The **Investment Returns Table** needs, per investment: invested
capital, realized proceeds, unrealized value, MOIC, and IRR. Sum across investments to populate
the MOIC card in the **KPI Strip**.

**6. Resolve any non-standard metrics by name.** If the user asks the report to include a
tenant-specific KPI that isn't part of the platform's standard metric set — e.g. a custom
operating metric — use the metric-name search tool to resolve it to an ID before querying the
company-metrics tool.

### Currency

Use the company's reporting currency as returned in step 2. **Do not default to USD.** If the
user explicitly asks for a different currency, pass that through to each tool call.

### If something is missing

- Company not found → ask the user to confirm spelling; try the legal name.
- A metric returns no value → display `—`. Never fabricate.
- A tool returns a schema or help error → comply with the introspection call it asks for and retry.
- Chronograph MCP not connected → prompt the user to connect it, or fall back to Model mode. While the connector is unavailable, do not reference Chronograph-specific schemas, private tool names, field mappings, or retrieval recipes.

### Model Mode

Read the uploaded Excel file using pandas (`data_only=True`). Extract from:

| Tab | Data to extract |
|---|---|
| `Overview` | Company name, HQ, fiscal year end, fund name(s), investment names, entry dates, ownership % |
| `Performance` | Revenue, Gross Profit, EBITDA, Adj. EBITDA (Reported and Valuation basis), Net Debt — last 4–5 LTM periods |
| `Valuation` | EV, valuation multiple, equity value, net debt — current and prior quarter; commentary text (Business Update, Rationale for Conclusion, Rationale for Discount); per-investment cost, realized, unrealized, MOIC |

**Currency and scale:** Check the `Figures In` field on the Overview tab. If `1000`
(thousands), divide all financial values by 1,000 before displaying in millions. Note the
`Local Currency` field and include it in the report header.

**If commentary is present in the model**, use it verbatim (lightly edited for grammar only).

---

## Step 3 — Render the Report

Build the HTML per `references/rendering.md`, which carries the layout structure, every panel
specification, the CSS variable scaffold, and the formatting ruleset. Populate the CSS
variables from the brand tokens resolved in Step 0; all panels inherit them.

Key invariants (the reference has the full detail):

- The **Financial Performance table must sit directly above the Valuation Summary table** in
  the same (left) column.
- The bar chart is **inline SVG only** — no external JS or D3.
- Unavailable values render as `—`; never fabricate.

---

## Step 4 — LP Quarterly Update Additions

When report type is **LP Quarterly Update**:

1. Header eyebrow → `LP QUARTERLY UPDATE · Q[N] YYYY`
2. Commentary must come from model verbatim — never AI-generate for LP reports
3. Add an optional **valuation bridge note** below the Valuation Summary table:
   *"EV increase driven by multiple expansion from X.Xx to Y.Yx; EBITDA contribution +$Zm"*

---

## Step 5 — Output

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*

- **File name:** `[company_name_lowercase_underscored]_[report_type]_[quarter].html`
  - Examples: `ashworth_health_gp_report.html` · `ashworth_health_lp_update_q4_2024.html`
- **Single self-contained HTML file** — all CSS in `<style>`, all data inline
- **No external JS** — bar chart is inline SVG
- **Footer:** `© {firm_name} | {website} | {confidentiality_label}` (omit blank fields)
- Save to the outputs directory and present the file to the user

---

## Error Handling

| Situation | Action |
|---|---|
| No brand template and no defaults configured | Apply Chronograph defaults silently |
| Brand template provided but colors are ambiguous | Apply best-guess tokens; surface the one-line confirmation (Step 0) |
| Logo URL returns 404 or is empty | Fall back to firm name as heading-font text |
| Company not found via MCP | Ask user to confirm spelling; try alternate names |
| Metric unavailable | Display `—`; never fabricate |
| Commentary empty in model | AI-generate; label `(AI-generated)` in small `text_muted` |
| IRR null for all investments | Omit IRR column |
| Cost split unavailable for a tranche | Show combined row; note gap in footnote |
| Model and MCP figures conflict | Flag in footnote; prefer model figures |
| `Figures In` = 1000 | Divide all values by 1,000 before displaying in millions |
| Light-theme brand detected | Swap text tokens to dark; verify contrast ≥ 4.5:1 before rendering |
| Chronograph MCP not connected (MCP mode) | Prompt user to connect; fall back to Model mode if a file is available |

---

## Data & Brand Checklist (verify before rendering)

**Brand**
- [ ] Brand tokens resolved — from uploaded template or Chronograph defaults
- [ ] One-line brand confirmation output to user (or low-confidence question asked)
- [ ] CSS variables set; Google Fonts `<link>` in `<head>`
- [ ] Logo rendered or firm-name fallback applied
- [ ] Theme (dark/light) confirmed; contrast ratios verified

**Data**
- [ ] Data source mode determined (Model or MCP)
- [ ] Report type determined (GP One-Pager or LP Quarterly Update)
- [ ] Currency and scale confirmed (`Figures In` handling applied if needed)
- [ ] Financial Performance table: 4 periods + vs. PY column
- [ ] Valuation Summary: PQ vs CQ + delta — in same column as Financial Performance
- [ ] Bar chart: 4 periods, bars labelled, y-axis auto-scaled
- [ ] Investment Returns: per-investment rows + total row
- [ ] Commentary: model text verbatim if available; empty blocks collapsed
- [ ] Footer: firm name, website, confidentiality label (omit blanks)
- [ ] Single self-contained HTML file, no external JS

---

## Reference Files

- `references/brand-tokens.md`: branding resolution — template extraction, Chronograph
  defaults, brand token schema, theme handling, confirmation line.
- `references/rendering.md`: layout structure, panel specifications, CSS scaffold, and
  formatting rules.

## Guardrails

- **Not advice.** Draft analyst work product for informational purposes only — not investment, legal, tax, accounting, or valuation advice, and not a recommendation to buy, sell, or hold. Stage every output for review and sign-off by a qualified professional.
- **No autonomous actions.** Draft and flag only; never approve, execute, or externally distribute. LP-facing or external distribution requires human (e.g. IR/CCO) sign-off outside this skill.
