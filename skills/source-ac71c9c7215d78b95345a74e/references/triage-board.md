# Rendering the triage board

Render everything in one `show_widget` as a stack of cards in this order: **overview card**, then **priority cards**, then **action bar**. Wrap all cards in `<div style="display:flex;flex-direction:column;gap:16px;padding:4px;">`.

---

## 1. Overview card

Header strip: **"Overview"** on the left, `[domain] · [date range]` on the right.

**Layout — two sections:**

*Conversion rate block (always visible, no expand):*
Show Site Wide, Mobile, and Desktop as three equal side-by-side blocks under a shared "CONVERSION RATE" section label. Each block: device name in uppercase small text, CVR% at 20px bold, sessions in small secondary text below. No separate stat line above — the site-wide block replaces it.

*Three blocks below (collapsed / expanded):*
- **Top country** — flag + name, sessions, CVR
- **Best converting channel** — humanized name, CVR. Skip `(none)/(none)`.
- **Most visited channel** — humanized name, sessions. Skip `(none)/(none)` — show the next real channel instead.

Toggled by a single "Show more / Show less" centered text link. Expanded shows 3 tables (5 rows max each):
- **Countries** — Country (with flag) · Sessions · CVR · Rev/session
- **Best converting channels** — Channel · Sessions · CVR · Rev/session. Ranked by CVR ↓. Exclude `(none)/(none)`.
- **Most visited channels** — Channel · Sessions · CVR · Rev/session. Ranked by sessions ↓. Include `(none)/(none)` here (unlike collapsed view). If `(none)/(none)` ≥ 5% of total sessions or broken UTM macros exist, show a banner below the table (see template below) — do not add pills inline.

**Channel name humanization** — display a readable name; show raw `source / medium` in a `title` tooltip on hover:
- `sendlane / email` → "Sendlane Email" · `rivo / email` → "Rivo Email" · `facebook / cpc` → "Facebook Ads" · `ig / social` → "Instagram" · `google / cpc` → "Google Ads" · `google / product_sync` → "Google Shopping" · `chatgpt.com / –` → "ChatGPT"
- No obvious mapping → capitalize source + append medium: `steam / referral` → "Steam Referral"
- `(none) / (none)` → "Direct / Unknown"

```html
<style>
.tbl{width:100%;border-collapse:collapse;font-size:13px;}
.tbl th{font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-secondary);text-align:left;padding:0 8px 8px 0;border-bottom:0.5px solid var(--color-border-tertiary);}
.tbl td{padding:8px 8px 8px 0;border-bottom:0.5px solid var(--color-border-tertiary);color:var(--color-text-primary);font-size:13px;}
.tbl tr:last-child td{border-bottom:none;}
.pill-warn{display:inline-block;font-size:11px;font-weight:500;padding:2px 7px;border-radius:4px;background:#FEF3C7;color:#92400E;margin-left:6px;}
.pill-err{display:inline-block;font-size:11px;font-weight:500;padding:2px 7px;border-radius:4px;background:#FEE2E2;color:#991B1B;margin-left:6px;}
</style>

<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);display:flex;align-items:center;justify-content:space-between;">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">Overview</span>
    <span style="font-size:11px;color:var(--color-text-tertiary);">[domain] · [date range]</span>
  </div>
  <div style="background:var(--color-background-primary);padding:18px 20px;">

    <!-- Conversion rate — always visible -->
    <div style="margin-bottom:16px;">
      <p style="font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-secondary);margin:0 0 12px;">Conversion rate</p>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;">
        <div>
          <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 8px;">Site wide</p>
          <p style="font-size:20px;font-weight:600;color:var(--color-text-primary);margin:0 0 4px;">[CVR%]</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions</p>
        </div>
        <div>
          <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 8px;">Mobile</p>
          <p style="font-size:20px;font-weight:600;color:var(--color-text-primary);margin:0 0 4px;">[CVR%]</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions</p>
        </div>
        <div>
          <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 8px;">Desktop</p>
          <p style="font-size:20px;font-weight:600;color:var(--color-text-primary);margin:0 0 4px;">[CVR%]</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions</p>
        </div>
      </div>
    </div>

    <!-- 3 collapsible blocks -->
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;border-top:0.5px solid var(--color-border-tertiary);padding-top:14px;" id="seg-collapsed">
      <div>
        <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 6px;">Top country</p>
        <p style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin:0 0 4px;">[flag] [name]</p>
        <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions · [X%] CVR</p>
      </div>
      <div>
        <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 6px;">Best converting channel</p>
        <p style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin:0 0 4px;">[humanized name — skip Direct/Unknown]</p>
        <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[X%] CVR</p>
      </div>
      <div>
        <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 6px;">Most visited channel</p>
        <p style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin:0 0 4px;">[humanized name — skip Direct/Unknown]</p>
        <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions</p>
      </div>
    </div>

    <button onclick="toggleSeg()" id="seg-btn" style="font-size:12px;color:var(--color-text-secondary);background:none;border:none;cursor:pointer;text-decoration:underline;text-underline-offset:2px;display:block;margin:12px auto 0;width:fit-content;">Show more</button>

    <div id="seg-expanded" style="display:none;margin-top:16px;border-top:0.5px solid var(--color-border-tertiary);padding-top:14px;">
      <table class="tbl" style="margin-bottom:24px;table-layout:fixed;">
        <colgroup><col/><col style="width:100px"/><col style="width:72px"/><col style="width:110px"/></colgroup>
        <thead><tr><th>Country</th><th>Sessions</th><th>CVR</th><th>Rev / session</th></tr></thead>
        <tbody>[Up to 5 rows, flag emoji per country]</tbody>
      </table>
      <table class="tbl" style="margin-bottom:24px;table-layout:fixed;">
        <colgroup><col/><col style="width:100px"/><col style="width:72px"/><col style="width:110px"/></colgroup>
        <thead><tr><th>Best converting channels</th><th>Sessions</th><th>CVR</th><th>Rev / session</th></tr></thead>
        <tbody>[Up to 5 rows — exclude (none)/(none), humanized names with title tooltip]</tbody>
      </table>
      <table class="tbl" style="margin-bottom:16px;table-layout:fixed;">
        <colgroup><col/><col style="width:100px"/><col style="width:72px"/><col style="width:110px"/></colgroup>
        <thead><tr><th>Most visited channels</th><th>Sessions</th><th>CVR</th><th>Rev / session</th></tr></thead>
        <tbody>[Up to 5 rows — humanized names with title tooltip. Do NOT add pills inline here.]</tbody>
      </table>
      [If (none)/(none) share ≥ 5%: render the banner below. If broken UTM macros exist: render the red banner below. Otherwise omit.]
      <div class="pill-warn" style="display:block;width:100%;box-sizing:border-box;padding:8px 12px;border-radius:6px;font-size:12px;margin-top:4px;">[X]% of sessions have no UTM attribution — likely direct traffic or missing tracking parameters on campaigns.</div>
      <div class="pill-err" style="display:block;width:100%;box-sizing:border-box;padding:8px 12px;border-radius:6px;font-size:12px;margin-top:4px;">Broken UTM macros detected (e.g. <code>{{</code>) — campaign links may not be tracking correctly.</div>
    </div>
    <div style="display:flex;justify-content:flex-end;padding-top:12px;margin-top:4px;">
      <button onclick="sendPrompt('Save segment overview as dashboard for [domain]')" style="padding:5px 12px;font-size:12px;font-weight:500;color:var(--color-text-primary);background:none;border:0.5px solid var(--color-border-tertiary);border-radius:6px;cursor:pointer;">Save as Artifact</button>
    </div>
  </div>
</div>

<script>
function toggleSeg(){
  const exp=document.getElementById('seg-expanded');
  const col=document.getElementById('seg-collapsed');
  const btn=document.getElementById('seg-btn');
  const open=exp.style.display==='none';
  exp.style.display=open?'block':'none';
  col.style.display=open?'none':'grid';
  btn.textContent=open?'Show less':'Show more';
}
</script>
```

---

## 2. Priority cards

Top 3 signals ranked by sessions affected (descending). Show exactly 3 — do not mention or surface additional signals.

Each card: signal type + sessions affected in header · segment name · one sentence (key number + why it matters) · Investigate button. No actions, tables, or bullets on the card.

Signal type labels: `LOW MOBILE CONVERSION` · `HIGH-TRAFFIC UNDERPERFORMER` · `CAMPAIGN DRAG` · `LOCALIZATION GAP` · `HIGH-VALUE CHANNEL` · `DEVICE GAP`

```html
<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);display:flex;align-items:center;justify-content:space-between;">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">[Signal type]</span>
    <span style="font-size:11px;font-weight:500;padding:2px 8px;border-radius:4px;background:var(--color-background-tertiary);color:var(--color-text-secondary);">~[N] sessions affected</span>
  </div>
  <div style="background:var(--color-background-primary);padding:20px;">
    <p style="font-size:15px;font-weight:500;margin:0 0 8px;color:var(--color-text-primary);">[Segment name]</p>
    <p style="font-size:14px;color:var(--color-text-secondary);line-height:1.6;margin:0 0 16px;">[Key number + why it matters in one sentence]</p>
    <button onclick="sendPrompt(&quot;Investigate this segment signal: [signal type] — [segment name], [domain], [key metrics], [follow-up data already gathered]&quot;)" style="padding:6px 14px;font-size:13px;font-weight:500;color:var(--color-text-primary);background:var(--color-background-secondary);border:0.5px solid var(--color-border-tertiary);border-radius:6px;cursor:pointer;">Investigate ↗</button>
  </div>
</div>
```

---

## 3. Action bar

```html
<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">Export &amp; Schedule</span>
  </div>
  <div style="background:var(--color-background-primary);padding:16px 20px;display:flex;gap:8px;justify-content:flex-end;">
    <button onclick="sendPrompt('Export segment analysis as PDF for [domain]')"
      style="padding:6px 14px;font-size:13px;font-weight:500;color:var(--color-text-primary);background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);border-radius:6px;cursor:pointer;">
      Download Report
    </button>
    <button onclick="sendPrompt('Schedule segment analysis for [domain]')"
      style="padding:6px 14px;font-size:13px;font-weight:500;color:var(--color-background-primary);background:var(--color-text-primary);border:0.5px solid var(--color-text-primary);border-radius:6px;cursor:pointer;">
      [Schedule Insights — OR — Edit schedule if a task already exists]
    </button>
  </div>
</div>
```
