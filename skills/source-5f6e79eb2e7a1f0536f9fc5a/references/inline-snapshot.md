# Inline snapshot (default view)

This is the default output of Store Pulse — rendered every time, before any artifact
exists and regardless of whether one already does. It replaces the old behavior of
gating everything behind Setup/Open. See SKILL.md's "Default flow" for when this runs.

**Unlike the live dashboard, this is a snapshot you compute, not a live-fetching
widget.** Run the `core-kpis` and `purchase-funnel` queries yourself (via the Noibu tool,
following `references/blocks/core-kpis.md` and `references/blocks/purchase-funnel.md`)
*before* calling `show_widget`, then bake the resulting numbers into the HTML as literal
values. The widget has no `callMcpTool` access and never re-fetches — it's a one-shot
rendering of data you already have, same as how `triage-board.md` works for other Noibu
skills. Always the last 24h window, compared to the prior 24h.

## Response shape

1. **Chat text first** — 2-3 sentences of plain prose, no bullets, no headers. Lead with
   the most notable thing (a drop, a surprise, a trend). Mix wins and concerns. Specific
   numbers, not exhaustive — this is the "Editorial snapshot" summary and follows the same
   voice as before.
2. **Then `show_widget`** — the KPI row + funnel, nothing else. No text, no summary,
   no headers inside the widget — those live in the chat response.
3. **One short closing line** after the widget so the turn doesn't end on a bare widget
   (a `show_widget` call with nothing after it can register as "no visible output").
   Name what it is, don't recap it.
4. **Then the investigate-thread question** — see "Where to next" below.

**These four steps are strictly sequential — never call `AskUserQuestion` in the same
batch as `show_widget`, and never before the chat-text summary exists.** The
investigate-thread options in step 4 are *derived from* the summary you write in step 1
(see "Where to next" below) — they cannot be decided, let alone shown, before that text
exists. If it's ever tempting to fire `show_widget` and `AskUserQuestion` together as
"independent" tool calls, they aren't independent here: treat step 4 as blocked on step
3's closing line actually being emitted first. Asking the follow-up before (or instead
of) showing the summary is a sequencing bug, not a stylistic choice.

## Widget

This is a `show_widget` surface, not `create_artifact` — it **does** receive the host's
injected design tokens (confirmed from `product-analysis/references/triage-board.md`,
a live production widget that styles its Overview card entirely with
`var(--color-background-primary|secondary|tertiary)`, `var(--color-text-primary|secondary|tertiary)`,
`var(--color-border-tertiary)`, and `var(--border-radius-lg)`, with no local `:root` block
of its own). Use those same tokens for the card chrome below so this widget matches the
Overview-card look used by the other Noibu skills. The only things defined locally are
the two semantic delta colors (`--sn-pos` / `--sn-neg`), because no confirmed global token
exists for those — same approach `funnel-visualization`'s `funnel-template.html` takes.

The funnel reuses that same `funnel-template.html` rendering logic (proportional bar
scaling, drop-zone that spans exactly to the previous step's bar top, gradient trapezoid
connector, compressed-first-bar zigzag) rather than hand-computed pixel math — it's the
already-debugged, shared implementation. Feed it raw session counts per step (not
percentages); it derives bar heights and header percentages itself.

**Two separate cards, not one.** The Overview card (header + KPIs + funnel) and the
Save & Schedule actions card are sibling cards in a `flex-direction: column` stack, each
with their own header-strip chrome — mirroring how `triage-board.md` keeps its Overview
card and Action bar as separate cards rather than one combined block. Don't merge the
buttons back into the Overview card's body.

```html
<style>
  :root { --sn-pos: #046249; --sn-neg: #894c06; }
  @media (prefers-color-scheme: dark) { :root { --sn-pos: #2db87a; --sn-neg: #d47c1a; } }
  .sp-ov {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    border: 0.5px solid var(--color-border-tertiary);
    border-radius: var(--border-radius-lg);
    overflow: hidden;
  }
  .sp-ov-head {
    background: var(--color-background-secondary);
    padding: 8px 20px;
    border-bottom: 0.5px solid var(--color-border-tertiary);
    display: flex; align-items: center; justify-content: space-between;
  }
  .sp-ov-label {
    font-size: 12px; font-weight: 500; letter-spacing: 0.06em;
    color: var(--color-text-secondary); text-transform: uppercase;
  }
  .sp-ov-meta { font-size: 11px; color: var(--color-text-tertiary); }
  .sp-ov-body { background: var(--color-background-primary); padding: 18px 20px; }

  .sp-kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
  .sp-kpi {
    background: var(--color-background-secondary);
    border-radius: var(--border-radius-lg);
    padding: 16px;
  }
  .sp-kpi-label {
    font-size: 11px; font-weight: 500; letter-spacing: 0.22px;
    color: var(--color-text-secondary); text-transform: uppercase;
  }
  .sp-kpi-value { font-size: 20px; line-height: 32px; font-weight: 500; color: var(--color-text-primary); margin-top: 6px; }
  .sp-kpi-delta { font-size: 11px; font-weight: 500; display: inline-block; margin-top: 4px; }
  .sp-kpi-delta.up { color: var(--sn-pos); }
  .sp-kpi-delta.down { color: var(--sn-neg); }
  .sp-kpi-delta.flat { color: var(--color-text-secondary); }

  .spf-wrap { margin-top: 16px; padding-top: 16px; border-top: 0.5px solid var(--color-border-tertiary); }
  .spf-fi { display: grid; grid-template-rows: auto 208px; gap: 20px 0; position: relative; }
  .spf-fh, .spf-fb { display: flex; }
  .spf-fb { height: 208px; }
  .spf-sh { flex: 1; min-width: 0; padding-right: 20px; position: relative; display: flex; flex-direction: column; gap: 4px; }
  .spf-sl { font-size: 12px; font-weight: 500; line-height: 18px; color: var(--color-text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-transform: uppercase; letter-spacing: 0.22px; }
  .spf-sm { display: flex; align-items: baseline; gap: 8px; width: 100%; white-space: nowrap; overflow: hidden; }
  .spf-mv { font-size: 15px; font-weight: 500; line-height: 20px; color: var(--color-text-primary); flex: 0 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .spf-dv { font-size: 11px; font-weight: 500; line-height: 18px; flex-shrink: 0; white-space: nowrap; }
  .spf-sv { flex: 1; position: relative; height: 208px; min-width: 0; }
  .spf-fi { --f-drop-bg: var(--color-background-tertiary); --f-bar: var(--color-text-primary); --f-val: var(--color-text-primary); --f-con: linear-gradient(to bottom, rgba(0,0,0,0.14), rgba(0,0,0,0.03)); --f-zz: var(--color-background-primary); --f-vline: var(--color-border-tertiary); }
  @media (prefers-color-scheme: dark) { .spf-fi { --f-con: linear-gradient(to bottom, rgba(255,255,255,0.16), rgba(255,255,255,0.03)); } }
  /* The vertical divider lines between funnel columns are drawn 1200px tall (see the
     funnel-template.html this is ported from) so they reach past the bars at any card
     height, then get clipped at the card edge. Without this, they bleed straight through
     whatever sits below the funnel — this was the cause of the funnel appearing to
     "overlap" the actions card in an earlier round. */
  .spf-wrap { margin-top: 16px; padding-top: 16px; border-top: 0.5px solid var(--color-border-tertiary); overflow: hidden; }

  /* Actions — its own card, same chrome as the Overview card, matching the
     "Export & Schedule" action-bar pattern other Noibu skills use. Not appended inside
     the Overview card's body. */
  .sp-actions-card {
    border: 0.5px solid var(--color-border-tertiary);
    border-radius: var(--border-radius-lg);
    overflow: hidden;
  }
  .sp-actions-head {
    background: var(--color-background-secondary);
    padding: 8px 20px;
    border-bottom: 0.5px solid var(--color-border-tertiary);
  }
  .sp-actions-label {
    font-size: 12px; font-weight: 500; letter-spacing: 0.06em;
    color: var(--color-text-secondary); text-transform: uppercase;
  }
  .sp-actions-body {
    background: var(--color-background-primary);
    padding: 16px 20px;
    display: flex; justify-content: flex-end; gap: 8px;
  }
  .sp-btn {
    padding: 6px 14px; font-size: 13px; font-weight: 500; border-radius: 6px; cursor: pointer;
    border: 0.5px solid var(--color-border-tertiary); background: var(--color-background-primary); color: var(--color-text-primary);
  }
  .sp-btn.primary { background: var(--color-text-primary); color: var(--color-background-primary); border-color: var(--color-text-primary); }
</style>

<div style="display:flex;flex-direction:column;gap:16px;">
  <h2 style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Store Pulse snapshot for [domain]: last 24 hours vs. previous 24 hours</h2>

  <div class="sp-ov">
    <div class="sp-ov-head">
      <span class="sp-ov-label">Store Pulse</span>
      <span class="sp-ov-meta">[domain] · Last 24h</span>
    </div>
    <div class="sp-ov-body">
      <div class="sp-kpis">
        <!-- One .sp-kpi per metric: Sessions, Engagement, Conversion, AOV, RPS — same order,
             same values/format/delta convention as core-kpis.md. -->
        <div class="sp-kpi">
          <div class="sp-kpi-label">Sessions</div>
          <div class="sp-kpi-value">[value]</div>
          <div class="sp-kpi-delta [up|down|flat]">[arrow] [delta]</div>
        </div>
        <!-- repeat for Engagement, Conversion, AOV, RPS -->
      </div>

      <div class="spf-wrap">
        <div id="spFunnel"></div>
      </div>
    </div>
  </div>

  <div class="sp-actions-card">
    <div class="sp-actions-head">
      <span class="sp-actions-label">Save &amp; Schedule</span>
    </div>
    <div class="sp-actions-body">
      <button class="sp-btn" onclick="sendPrompt('Schedule Store Pulse report for [domain]')">Schedule report</button>
      <button class="sp-btn primary" onclick="sendPrompt('Save Store Pulse dashboard for [domain]')">Save as artifact</button>
    </div>
  </div>
</div>

<script>
// Funnel renderer — ported from querying-noibu-data/references/funnel-template.html
// (already debugged there: proportional bar scaling, compressed-first-bar zigzag,
// drop-zone that spans exactly to the previous bar's top, gradient connector trapezoid).
// STEPS: raw session counts per step, in order. delta on step 0 is a % change of the
// session count; delta on steps 1+ is a percentage-point change of pctReach (matches
// purchase-funnel.md). Root cause of the old bug: the drop-zone and connector were
// hand-computed with static values instead of driven by this shared algorithm.
// Tooltips use the native `title` attribute (not a custom absolute-positioned tooltip
// div) — deliberately, so there's no overflow-at-the-edge failure mode to debug in a
// one-shot static snapshot. See purchase-funnel.md's tooltip requirement; a native
// title tooltip still surfaces the session count + dropoff text on hover.
(function () {
  const STEPS = [
    // { name: "Enter store", sessions: [count], delta: [pct change, e.g. -10.7] },
    // { name: "View product", sessions: [count], delta: [pp change, e.g. 8.3] },
    // { name: "Add to cart", sessions: [count], delta: [pp change] },
    // { name: "Start checkout", sessions: [count], delta: [pp change] },
    // { name: "Checkout complete", sessions: [count], delta: [pp change] },
  ];
  const root = document.getElementById('spFunnel');
  root.innerHTML = '<div class="spf-fi"><div class="spf-fh" id="spfH"></div><div class="spf-fb" id="spfB"></div></div>';
  const CH = 208, COMP = 3.5;
  const s0 = STEPS[0], s1 = STEPS[1];
  const isC = s1 && s0.sessions / s1.sessions >= COMP;
  const ref = isC ? s1.sessions : s0.sessions;
  const maxH = isC ? CH - 32 : CH;
  function tpx(i) {
    if (i === 0 && isC) return 0;
    const h = Math.min(STEPS[i].sessions / ref, 1) * maxH;
    const raw = Math.round(CH - h);
    return (isC && i === 1) ? Math.max(raw, 32) : raw;
  }
  const fn = n => { if (n >= 1e6) return (n/1e6).toFixed(1).replace(/\.0$/, '') + 'M'; if (n >= 1e4) return (n/1e3).toFixed(1).replace(/\.0$/, '') + 'K'; return (n || 0).toLocaleString(); };
  const fp = (a, b) => { const r = (a / b * 100).toFixed(1); return (r === '0.0' && a > 0) ? '<0.1%' : r + '%'; };
  const fd = (d, isFirst) => {
    const unit = isFirst ? '%' : 'pp';
    const r = parseFloat(Math.abs(d).toFixed(1));
    if (r === 0) return { txt: '± 0', col: 'var(--color-text-secondary)' };
    return { txt: (d > 0 ? '&uarr; ' : '&darr; ') + r + unit, col: d > 0 ? 'var(--sn-pos)' : 'var(--sn-neg)' };
  };
  function addZz(parent) {
    const svg = `<svg width="600" height="7" viewBox="-300 0 600 7" style="position:absolute;top:32px;left:0;right:0;margin:auto;display:block" aria-hidden="true"><path d="${Array.from({length:151},(_,k)=>{const x=-300+k*4; const y=((Math.floor(x/4)%2)+2)%2===0?1:5; return (k?'L':'M')+x+','+y;}).join('')}" fill="none" stroke-width="2" style="stroke:var(--f-zz)"/></svg>`;
    parent.insertAdjacentHTML('beforeend', svg);
  }
  const H = document.getElementById('spfH'), B = document.getElementById('spfB');
  const tops = STEPS.map((_, i) => tpx(i));
  STEPS.forEach((s, i) => {
    const hd = document.createElement('div');
    hd.className = 'spf-sh';
    const hasDelta = s.delta != null;
    const metTxt = i === 0 ? fn(s.sessions) + ' sessions' : fp(s.sessions, s0.sessions);
    let deltaHtml = '';
    if (hasDelta) { const { txt, col } = fd(s.delta, i === 0); deltaHtml = `<span class="spf-dv" style="color:${col}">${txt}</span>`; }
    hd.innerHTML = `<div class="spf-sl">${s.name}</div><div class="spf-sm"><span class="spf-mv">${metTxt}</span>${deltaHtml}</div>`;
    if (i < STEPS.length - 1) { const vl = document.createElement('div'); vl.style.cssText = 'position:absolute;right:12px;top:0;width:0.5px;height:1200px;background:var(--f-vline);pointer-events:none'; hd.appendChild(vl); }
    H.appendChild(hd);

    const v = document.createElement('div'); v.className = 'spf-sv';
    const tp = tops[i];
    const pS = i > 0 ? STEPS[i - 1] : null, nTp = i < STEPS.length - 1 ? tops[i + 1] : null;
    const pt = i > 0 ? tops[i - 1] : 0;

    if (pS) {
      const dPct = ((1 - s.sessions / pS.sessions) * 100).toFixed(1);
      const da = document.createElement('div');
      da.style.cssText = `position:absolute;left:0;right:50%;bottom:0;top:${pt}px;background:var(--f-drop-bg);border-radius:4px 4px 0 0;cursor:help`;
      da.title = `${fn(s.sessions)} sessions · ${dPct}% dropoff from ${pS.name}`;
      v.appendChild(da);
    }
    if (nTp !== null) {
      const conH = CH - tp, p1pct = ((nTp - tp) / conH * 100).toFixed(2);
      const con = document.createElement('div');
      con.style.cssText = `position:absolute;right:0;top:${tp}px;width:50%;height:${conH}px;clip-path:polygon(0 0%,100% ${p1pct}%,100% 100%,0 100%);background:var(--f-con);pointer-events:none`;
      v.appendChild(con);
    }
    const bar = document.createElement('div');
    bar.style.cssText = `position:absolute;left:0;right:50%;bottom:0;top:${tp}px;background:var(--f-bar);border-radius:4px 4px 0 0;overflow:hidden;cursor:help`;
    bar.title = pS ? `${fn(s.sessions)} sessions · ${((1 - s.sessions/pS.sessions)*100).toFixed(1)}% dropoff from ${pS.name}` : `${fn(s.sessions)} sessions · top of the funnel`;
    if (i === 0 && isC) addZz(bar);
    v.appendChild(bar);
    B.appendChild(v);
  });
})();
</script>
```

Render via `show_widget` with `title: "store_pulse_snapshot"` and a short loading message
(e.g. `["Pulling today's numbers..."]`).

## Where to next

After the widget and closing line, offer via `AskUserQuestion` (single-select):

- Header: "Where to next?"
- Question: "Pick a thread to pull on."
- 3 options drawn from the summary you just wrote — each targeting a specific signal
  (drop, surprise, trend, outlier), same order as mentioned in the summary. Frame as
  something to investigate, e.g. "Why did conversion fall 8pp?"
- 4th option: **"Not right now"**.
- If fewer than 3 distinct threads surfaced, fill in with defaults: "Where's the biggest
  revenue opportunity?", "What changed since yesterday?"

Route the pick:
- **Investigation prompt** → treat as a fresh question. Don't answer from the snapshot
  alone — let normal skill-selection pick the right Noibu skill. Frame in the user's
  terms, not Store Pulse's block names.
- **"Not right now"** → acknowledge briefly, end.

## Button clicks

- **"Save as artifact"** arrives as `Save Store Pulse dashboard for [domain]` → see
  SKILL.md's "Save as artifact" flow.
- **"Schedule report"** arrives as `Schedule Store Pulse report for [domain]` → see
  SKILL.md's "Schedule report" flow.
