# Live Product Dashboard

Build a persistent artifact using `mcp__cowork__create_artifact`.

**Goal:** replicate the Phase 1 overview card from triage-board.md — funnel + collapsible top-5 tables (Products, Collections, Product Types) — but fetching data fresh via `callMcpTool` on every open. No priority cards.

**Probe before building.** Call the session search tool once with a minimal query to confirm the exact tool name and response shape. Build the parser around what you observe — `r.structuredContent ?? JSON.parse(r.content[0].text)`.

---

## Structure

At the very top, a single header row using `display:flex; align-items:flex-start; justify-content:space-between`:
- Left: domain name as title (`font-size:18px; font-weight:600`) with subtitle `"Based on Noibu data"` below it (`font-size:12px; color:var(--color-text-tertiary); margin-top:2px`)
- Right: **7d / 30d / 90d** tab selector. Default: 30d. Store the selected range in `localStorage` so it persists across opens.

Below that: the overview card — identical HTML and bar-scaling logic to triage-board.md. Copy the template directly; do not reimagine it. Use `new Date()` at runtime to compute the window end; subtract the selected days for the start.

5 rows per table (Products, Collections, Product Types).

The top products/collections/types section is always expanded — show the three tables directly, no collapsed state, no Show more/Show less toggle. Each table's first column header carries the table title (e.g. "Top products by sessions") — no separate label element above the table. Add `padding-right:24px` to first-column `th` and `td` cells to create spacing between the name column and the metrics.

Show a loading skeleton (grey placeholder bars, `background:var(--color-background-secondary)`) while fetching. Show an inline error message per section if a call fails — don't crash the whole page.

No action bar. No 'Save as dashboard' button inside the artifact itself.

Outer wrapper: `<div style="padding:16px;display:flex;flex-direction:column;gap:16px;">`.

---

## Fetching data

Fire queries **in series** (one at a time, awaiting each before starting the next) to avoid MCP timeouts from parallel calls. Update each table's loading state individually as its query resolves so the page fills in progressively rather than waiting for all queries to finish.

Queries needed (same as triage board Step 1):
1. Products by views (limit 5) — sessions, CVR, ATC rate, rev/session
2. Collections by sessions (limit 5) — sessions, CVR, rev/session
3. Product types by sessions (limit 5) — sessions, CVR, rev/session

Use `window.cowork.callMcpTool(name, args)`. The domain and date window are baked in at creation time — derive them from the analysis already in context.

List all tools called in the artifact's `mcp_tools` array.

---

## Artifact metadata

- `title`: "Product Overview — [domain]"
- `description`: "Live product overview for [domain] — funnel and top products/collections/types"
- `mcp_tools`: list the tools the artifact calls
