# Live Segment Dashboard

Build a persistent artifact using `mcp__cowork__create_artifact`.

**Goal:** replicate the overview card from triage-board.md — conversion rate block + expanded dimension tables (Countries, Best converting channels, Most visited channels) — fetching data fresh via `callMcpTool` on every open. No priority cards.

**Probe before building.** Call the session search tool once with a minimal query to confirm the exact tool name and response shape. Build the parser around what you observe — `r.structuredContent ?? JSON.parse(r.content[0].text)`.

---

## Structure

At the very top, a single header row using `display:flex; align-items:flex-start; justify-content:space-between`:
- Left: domain name as title (`font-size:18px; font-weight:600`) with subtitle `"Based on Noibu data"` below it (`font-size:12px; color:var(--color-text-tertiary); margin-top:2px`)
- Right: **7d / 30d / 90d** tab selector. Default: 30d. Store the selected range in `localStorage` so it persists across opens.

Below that: the overview card — no "Overview" header strip, no domain/date line (already shown above). Use `new Date()` at runtime to compute the window end; subtract the selected days for the start.

**Conversion rate block** — always visible, 3 equal columns: Site Wide · Mobile · Desktop. Each shows CVR% at 20px bold, sessions in small secondary text. Section label "Conversion rate" above.

**Three tables** — always expanded, no collapsed state, no Show more/Show less toggle. Use `table-layout:fixed` with shared column widths (Sessions: 100px, CVR: 72px, Rev/session: 110px). The first column header carries the table title — no separate label element above each table:
- First column: **"Countries"** · Sessions · CVR · Rev / session (5 rows, flag emoji)
- First column: **"Best converting channels"** · Sessions · CVR · Rev / session (5 rows, exclude Direct/Unknown, humanized names)
- First column: **"Most visited channels"** · Sessions · CVR · Rev / session (5 rows, humanized names)

If Direct/Unknown accounts for ≥ 5% of total sessions, show the amber UTM banner below the Most visited channels table.

Show a loading skeleton (grey placeholder bars, `background:var(--color-background-secondary)`) while fetching. Show an inline error message per section if a call fails — don't crash the whole page.

No action bar. No 'Save as Artifact' button inside the artifact itself.

Outer wrapper: `<div style="padding:16px;display:flex;flex-direction:column;gap:16px;">`.

---

## Fetching data

Fire queries **in series** (one at a time, awaiting each before starting the next) to avoid MCP timeouts from parallel calls. Update each section's loading state individually as its query resolves so the page fills in progressively.

Queries needed (same as triage board Step 1):
1. Device breakdown — group by device type, sessions, CVR, rev/session
2. Country breakdown — group by country, sessions, CVR, rev/session (limit 30, sessions ↓)
3. Channel breakdown — group by UTM source + UTM medium, sessions, CVR, rev/session (limit 30, sessions ↓)

Use `window.cowork.callMcpTool(name, args)`. The domain is baked in at creation time — derive it from the analysis already in context. The date window is computed at runtime from the selected tab (7d/30d/90d).

List all tools called in the artifact's `mcp_tools` array.

---

## Artifact metadata

- `title`: "Segment Overview — [domain]"
- `description`: "Live segment overview for [domain] — conversion rate by device, country, and channel"
- `mcp_tools`: list the tools the artifact calls
