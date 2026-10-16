# Performance reference

## CWV thresholds

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| FCP | ≤ 1.8s | ≤ 3.0s | > 3.0s |
| TTFB | ≤ 800ms | ≤ 1.8s | > 1.8s |

---

## What Noibu MCP provides vs what needs Chrome

**Noibu MCP (`noibu_get_page_visits`):**
- p75 CWV scores per page/URL (LCP, CLS, INP, FCP, TTFB)
- `CLICKED_SELECTORS_WITH_COUNTS` — CSS selectors + click counts per page (useful for INP: cross-reference most-clicked elements on a high-INP page to narrow down candidates)
- Visual error count per page

**Requires Chrome DevTools:**
- The specific LCP element (tag, source, attributes)
- CLS shift sources (which elements are moving and by how much)
- The specific INP slow element selector and phase breakdown

The Noibu performance console shows element-level detail for INP (via the `id=` parameter in the console URL) but this is not exposed through the MCP tools — it requires navigating to the console in Chrome.

When Chrome isn't available: use `CLICKED_SELECTORS_WITH_COUNTS` as supporting context for INP, and fall back to pattern-based recommendations for LCP and CLS element identification.

---

## DevTools diagnostics

### Device emulation

Match emulation to where the issue is worst in Noibu data. Mobile emulation is **required** for mobile CWV findings — without it, CLS and LCP issues produce silent false negatives. Use a mid-range Android device with Fast 3G throttling. Always hard reload with cache disabled when measuring.

### LCP

Use the Noibu recommend bucket to direct the investigation:

| Bucket | Where to look |
|---|---|
| TTFB | Server response time, CDN config, app/plugin overhead |
| Load Delay | Render-blocking scripts, missing preload hint, resource discovery order |
| Load Duration | Image file size, format (WebP vs JPEG), CDN delivery |
| Render Delay | JS blocking paint, lazy-loaded element, CSS blocking render |

Key check: is the LCP image in the initial HTML? Use View Source — not Inspect, which shows the post-JS DOM. If the image URL only appears after JS runs, the browser can't discover it early regardless of other optimisations.

### CLS

Only shifts where `hadRecentInput` is `false` count toward CLS — filter accordingly.

Common causes in rough frequency order: images missing `width`/`height`, late-injected content (popovers, loyalty widgets, banners), carousels with no pre-JS height, font swap with large metrics difference, client-side rendered results grids injecting after paint.

### INP

The dominant phase tells you where to dig:

| Dominant phase | Likely cause |
|---|---|
| Input Delay | Main thread busy at click time — third-party scripts initialising, carousels, analytics |
| Processing Time | Event handler too heavy — large re-renders, synchronous DOM queries, complex filter logic |
| Presentation Delay | Layout thrashing, large paint area, expensive animation |

If SVG sub-elements appear as separate tap targets in Noibu data, the fix is `pointer-events: none` on SVG children plus wrapping the SVG in a `<button>`.

## Data-HTML mismatch

If Noibu shows a poor score but page inspection looks clean (no lazy hero, no missing dimensions, scripts deferred), the cause is likely runtime — server response time, slow CDN, or render-blocking JS execution that doesn't show in static HTML. Don't conclude "no issue found" from clean inspection alone.

---

## Technical details fields

Rendered only when the operator explicitly asks or the Technical details chip is selected in the share widget. Render exactly these fields in order, omitting any with no data. No placeholder text, no commentary between fields.

- **Score** — one combined line: `[Metric] p75 [value] — [band]`
- **Sub-metric breakdown** — when available
- **Affected element** — CSS selector from Chrome inspection
- **Detected anti-pattern** — specific pattern found during page inspection
- **Browser impact** — when applicable
- **OS impact** — when applicable
- **File/line** — only when source enrichment ran
