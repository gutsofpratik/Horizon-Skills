# Export PDF

Build a clean document PDF from the analysis **already in this conversation** — the same numbers shown on the board. This is export-only:

- **Do not call any Noibu query tools, and do not re-run the analysis.** Reuse the exact figures from the board above. Re-querying would shift the numbers (the window moves) so the PDF wouldn't match what the user is looking at.
- **If the analysis isn't in context** (e.g. a fresh session with no prior board), ask the user to run the checkout analysis first — don't silently regenerate it.

Build the HTML as a clean document, not a styled widget. No card chrome, no CSS variables, no widget layout. Use plain HTML elements with minimal inline styles.

**Structure** (in order):
1. `<h1>` — domain and date range (e.g. "Checkout Analysis — atari.com · May 11–Jun 10 2026")
2. **Summary** — one short paragraph (2–3 sentences) in plain prose, directly under the `<h1>` (no heading). Synthesize checkout health: the headline completion/conversion read, the single biggest leak, and the top priority to act on. Built from the in-context analysis — no new queries.
3. **Overview section** — `<h2>Overview</h2>`, the key stats as a sentence (checkout completion, biggest reliable drop, errors, median order, discount rate), then an inline SVG funnel (see below), then the payment/delivery mix as plain `<table>` elements (only if populated).
4. For each priority signal — `<h2>[Signal title]</h2>` (e.g. "Cart-to-checkout leak before checkout begins"), then a short paragraph with the key number, sessions affected, and why it matters.

**SVG funnel.** Appears immediately after the key-stats sentence, before any tables. Generate an inline `<svg width="600" height="200">` with all values hardcoded from real data. Four columns for the checkout steps (Added to cart → Started checkout → Payment submitted → Completed order), column width 120px, 40px gaps (colX = 0, 160, 320, 480). For each step compute `f = sqrt(stepCount ÷ step1Count)` (step1 = Added to cart), then `barH = round(f × 120)` and `barTop = 190 − barH`. Per column: stage label text (`y=20`, font-size 10, fill="#888", uppercase), value text (`y=48`, font-size 15, fill="#111" — step 1 the count, steps 2–4 the % of cart), a ghost rect (`x=colX, y=70, height=120, fill="#ebebeb"`), a real bar rect (`x=colX, y=barTop, height=barH, fill="#000"`). Between columns, a connector polygon: `points="[rightEdge],[barTop_this] [nextLeftEdge],[barTop_next] [nextLeftEdge],190 [rightEdge],190" fill="#ebebeb"`. Omit the connector on the last column. If intermediate steps are uninstrumented (Principle 2), show only the instrumented steps.

**CSS — minimal, no variables:**
```html
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 14px; color: #111; padding: 32px; max-width: 800px; margin: 0 auto; }
  h1 { font-size: 20px; font-weight: 600; margin: 0 0 4px; }
  h2 { font-size: 15px; font-weight: 600; margin: 32px 0 8px; border-top: 1px solid #e0e0e0; padding-top: 20px; }
  p { line-height: 1.6; margin: 0 0 12px; color: #444; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 16px; }
  th { text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #666; border-bottom: 1px solid #e0e0e0; padding: 0 12px 6px 0; }
  th:first-child { visibility: hidden; }
  td { padding: 7px 12px 7px 0; border-bottom: 0.5px solid #f0f0f0; }
  h2 + p { margin-top: 0; }
</style>
```

`page-break-inside: avoid` on each `<h2>` section. Write to a temp file, then pass to the `pdf` skill.
