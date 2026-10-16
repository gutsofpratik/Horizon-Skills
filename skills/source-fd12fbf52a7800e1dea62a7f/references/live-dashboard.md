# Live Checkout Dashboard

Build a persistent artifact using `mcp__cowork__create_artifact`.

**Goal:** replicate the Overview card from `triage-board.md` — the stepped funnel, the two stat lines (funnel health + order profile), and the payment/delivery bar charts — but fetching data fresh via `callMcpTool` on every open. No priority cards, no action bar.

**Probe before building.** Call the Noibu session-search tool once with a minimal query to confirm the exact tool name and response shape. Build the parser around what you observe — `r.structuredContent ?? JSON.parse(r.content[0].text)`.

---

## Structure

At the very top, a header block:
- Domain name as the title (`font-size:18px; font-weight:600`)
- Subtitle: `"Based on Noibu data"` (`font-size:12px; color:var(--color-text-tertiary); margin-top:2px`)

Below that, a date-range selector: **7d / 30d / 90d** tabs. Default: 30d. Store the selection in `localStorage` so it persists across opens. Use `new Date()` at runtime to compute the window end; subtract the selected days for the start.

Below it: the Overview card — identical HTML, bar-scaling logic (`f = sqrt(step ÷ step1)`), hover tooltips, and stat lines to the `triage-board.md` Overview card. Copy the template directly; do not reimagine it. Render the payment/delivery charts only when populated.

Show a loading skeleton (grey placeholder bars, `background:var(--color-background-secondary)`) while fetching. Show an inline error message per section if a call fails — don't crash the whole page.

Do **not** include a 'Save as artifact' button inside the artifact itself.

Outer wrapper: `<div style="padding:16px;display:flex;flex-direction:column;gap:16px;">`.

---

## Fetching data

Run the queries **in series** — `await` each `window.cowork.callMcpTool(name, args)` before starting the next, on page load and on every date-range change. Do **not** use `Promise.all` / parallel fan-out: too many concurrent MCP calls cause timeouts. Render each section as its own result arrives (keep its skeleton until then) so the page fills in progressively rather than waiting for all of them. Guard each call in its own try/catch so one failure doesn't stop the rest. The domain is baked in at creation time — derive it from the analysis already in context; the window comes from the selected range.

Queries needed (same as triage-board Step 1):
- Funnel by depth (Q1) — for the stepped funnel + checkout completion.
- Cart & order value (Q2) — median order, discount rate, items/order. **Compute these exactly as Q2 defines them**, or the artifact won't match the board:
  - **Discount rate = discounted ÷ checkout-entering sessions (funnel depth ≥ 2)**, using the **completion-time** discount field. Do NOT use all sessions as the denominator, and do NOT use the checkout-start discount field — both badly understate the rate.
  - Median order value and median items/order: among completed orders, same as Q2.
- Payment method mix (Q3) and Delivery method mix (Q4) — for the two bar charts; render only if populated.
- Priority errors on checkout pages (Q5) — for the errors count.
- Device conversion split (Q6) — for the Mobile / Desktop stat.

List every tool the artifact calls in its `mcp_tools` array.

---

## Artifact metadata

- `title`: "Checkout Overview — [domain]"
- `description`: "Live checkout overview for [domain] — funnel, key stats, and payment/delivery mix"
- `mcp_tools`: list the tools the artifact calls
