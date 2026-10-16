# Rendering the triage board

The final deliverable of full analysis. Loaded before any queries run so it's ready when needed.

Render everything in one `show_widget` as a stack of cards: **Overview card** first, then ranked **Priority cards**, then **Action bar**. Wrap all cards in `<div style="display:flex;flex-direction:column;gap:16px;padding:4px;">` with a visually-hidden `<h2>` summary first.

---

## Overview card

One card with the same chrome as the Priority cards: header strip with **"Overview"** on the left and `[domain] · [date range]` on the right, then a body with the stat line, funnel, and top products/collections/types section.

- **Stat line** (above funnel) — `[total sessions] · [site CVR%] conversion rate · Median order $[X]`
- **Funnel** — exactly 3 steps, in this order: **Viewed Product** → **Added to Cart** → **Completed Order**. The funnel is product-scoped, **not** site-wide sessions — step 1 is sessions that viewed any product. Step 1 shows an absolute count; steps 2–3 show **% of step 1**. Flag the largest drop with a danger pill (`↓N%`) on that step's header. **Do not use "All Sessions" as a funnel stage.**

**Bar scaling — bar and connector MUST use the same fraction, or the slope won't meet the bars.** For each step compute `f = sqrt(stepCount ÷ step1Count)` (so f₁ = 1), with `bodyHeight = 150`:
- Bar height = `round(f × 150)` px
- Bar top T = `round((1 − f) × 100)` %
- Connector (right half of column, omit on last): `clip-path: polygon(0% Tᵢ%, 100% Tᵢ₊₁%, 100% 100%, 0% 100%)`

**Hover tooltip** per step: `[sessions] · [% of step 1] · [N] lost from previous step` (step 1: `[sessions] · base of product funnel`).

Stage label: `font-size:11px; font-weight:500; letter-spacing:0.4px; text-transform:uppercase; color:var(--color-text-secondary)`. Step 1 value = absolute count at `font-size:16px; font-weight:500`; steps 2–3 = percentage.

**Top products / collections / types** (another `border-top`):

*Collapsed state* — 3 metric blocks side by side, each showing the #1 item. Keep each block compact and consistent: truncate the name to one line.
- Label: `font-size:11px; font-weight:500; text-transform:uppercase; color:var(--color-text-secondary); margin:0 0 6px`
- Name: `font-size:13px; font-weight:500; color:var(--color-text-primary); margin:0 0 4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis`
- Sessions + CVR: `font-size:12px; color:var(--color-text-secondary); margin:0`

The toggle is a **centered text link** — no border, no background — that reads "Show more" (collapsed) / "Show less" (expanded). Place it centered below the three blocks. Style: `font-size:12px; color:var(--color-text-secondary); background:none; border:none; cursor:pointer; text-decoration:underline; text-underline-offset:2px; display:block; margin:12px auto 0; width:fit-content`.

A single click expands all three sections together. **When expanded, hide the three metric blocks** (`top-collapsed` div) — they are replaced by the tables, not shown alongside them. *Expanded state* shows a table for each (Products, Collections, Product Types):
- **First column header = the table title** (e.g. "Top products by sessions") — no separate label element above the table
- All other column headers: left-aligned
- First column: name only (no bar). Second column: bar only — a dedicated column with no header text, fixed width ~80px, containing a proportional bar; bar style: `height:6px; background:var(--color-text-secondary); border-radius:2px` on a `background:var(--color-background-secondary)` track (width % = sessions ÷ max sessions in that table × 100). All bars align in the same column.
- **Products:** Sessions · Add-to-cart rate · Conversion rate
- **Collections:** Sessions · Conversion rate · Rev/session
- **Product Types:** Sessions · Conversion rate · Rev/session
- Omit Product Types table if all types are within 20% CVR of each other

**Overview card template:**

```html
<style>
.cf-col{position:relative;flex:1;min-width:0;}
.cf-body{position:relative;height:150px;margin-top:14px;cursor:help;}
.cf-tip{position:absolute;bottom:calc(100% + 8px);left:0;background:var(--color-text-primary);color:var(--color-background-primary);font-size:11px;line-height:1.45;padding:6px 9px;border-radius:6px;opacity:0;pointer-events:none;transition:opacity .12s;z-index:50;white-space:nowrap;}
.cf-tip-r{left:auto;right:0;}
.cf-body:hover .cf-tip{opacity:1;}
.cf-div{position:absolute;top:0;right:0;width:0.5px;height:100%;background:var(--color-border-tertiary);}
.tbl{width:100%;border-collapse:collapse;font-size:13px;}
.tbl th{font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-secondary);text-align:left;padding:0 8px 8px 0;border-bottom:0.5px solid var(--color-border-tertiary);}
.tbl td{padding:8px 8px 8px 0;border-bottom:0.5px solid var(--color-border-tertiary);color:var(--color-text-primary);font-size:13px;}
.tbl tr:last-child td{border-bottom:none;}
.tbl th:first-child,.tbl td:first-child{padding-right:24px;}
</style>

<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);display:flex;align-items:center;justify-content:space-between;">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">Overview</span>
    <span style="font-size:11px;color:var(--color-text-tertiary);">[domain] · [date range]</span>
  </div>
  <div style="background:var(--color-background-primary);padding:18px 20px;">
    <p style="font-size:12px;color:var(--color-text-secondary);margin:0 0 16px;">[total sessions] · [site CVR%] conversion rate · Median order $[X]</p>

    <div style="display:flex;">
      [Repeat once per funnel step (3 total). cf-div on every column except last. Step 1 value = absolute count; steps 2–3 = % of step 1. Danger pill on largest-drop step only.]
      <div class="cf-col">
        <div class="cf-div"></div>
        <div style="padding:0 16px 0 12px;">
          <div style="font-size:11px;font-weight:500;letter-spacing:0.4px;color:var(--color-text-secondary);text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">[Stage label]</div>
          <div style="font-size:16px;font-weight:500;color:var(--color-text-primary);margin-top:2px;">[value — count for step 1, % for steps 2–3]</div>
        </div>
        <div class="cf-body">
          <div class="cf-tip">[tooltip: sessions · % of step 1 · N lost from previous]</div>
          <div style="position:absolute;left:0;width:50%;bottom:0;height:150px;background:var(--color-background-tertiary);border-radius:4px 4px 0 0;"></div>
          <div style="position:absolute;left:0;width:50%;bottom:0;height:[barPx]px;background:var(--color-text-primary);border-radius:4px 4px 0 0;"></div>
          <div style="position:absolute;right:0;width:50%;bottom:0;height:150px;background:var(--color-background-tertiary);clip-path:polygon(0% [thisTop]%,100% [nextTop]%,100% 100%,0% 100%);"></div>
        </div>
      </div>
    </div>

    <div style="margin-top:16px;padding-top:12px;border-top:0.5px solid var(--color-border-tertiary);">
      [Collapsed: 3 metric blocks side by side]
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;" id="top-collapsed">
        <div>
          <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 6px;">Top product</p>
          <p style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin:0 0 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">[name]</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions · [X%] CVR</p>
        </div>
        <div>
          <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 6px;">Top collection</p>
          <p style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin:0 0 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">[name]</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions · [X%] CVR</p>
        </div>
        <div>
          <p style="font-size:11px;font-weight:500;text-transform:uppercase;color:var(--color-text-secondary);margin:0 0 6px;">Top type</p>
          <p style="font-size:13px;font-weight:500;color:var(--color-text-primary);margin:0 0 4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">[name]</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">[N] sessions · [X%] CVR</p>
        </div>
      </div>
      <button onclick="toggleTop5()" id="top5-btn" style="font-size:12px;color:var(--color-text-secondary);background:none;border:none;cursor:pointer;text-decoration:underline;text-underline-offset:2px;display:block;margin:12px auto 0;width:fit-content;">Show more</button>

      [Expanded: 3 tables, hidden by default]
      <div id="top-expanded" style="display:none;margin-top:16px;margin-bottom:4px;">
        <table class="tbl" style="margin-bottom:20px;">
          <thead><tr>
            <th style="width:40%;">Top products by sessions</th>
            <th style="width:80px;"></th>
            <th>Sessions</th>
            <th>Add-to-cart</th>
            <th>Conversion</th>
          </tr></thead>
          <tbody>[5 rows: name, bar, sessions, ATC%, CVR]</tbody>
        </table>

        <table class="tbl" style="margin-bottom:20px;">
          <thead><tr>
            <th style="width:40%;">Top collections by sessions</th>
            <th style="width:80px;"></th>
            <th>Sessions</th>
            <th>Conversion</th>
            <th>Rev / session</th>
          </tr></thead>
          <tbody>[5 rows: name, bar, sessions, CVR, revenue/session formatted as $X.XX]</tbody>
        </table>

        <table class="tbl">
          <thead><tr>
            <th style="width:40%;">Top product types by sessions</th>
            <th style="width:80px;"></th>
            <th>Sessions</th>
            <th>Conversion</th>
            <th>Rev / session</th>
          </tr></thead>
          <tbody>[5 rows: name, bar, sessions, CVR, revenue/session formatted as $X.XX]</tbody>
        </table>
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;padding-top:12px;margin-top:4px;">
      <button onclick="sendPrompt('Save product overview as dashboard for [domain]')" style="padding:5px 12px;font-size:12px;font-weight:500;color:var(--color-text-primary);background:none;border:0.5px solid var(--color-border-tertiary);border-radius:6px;cursor:pointer;">Save as Artifact</button>
    </div>
  </div>
</div>

<script>
function toggleTop5(){
  const exp=document.getElementById('top-expanded');
  const col=document.getElementById('top-collapsed');
  const btn=document.getElementById('top5-btn');
  const open=exp.style.display==='none';
  exp.style.display=open?'block':'none';
  col.style.display=open?'none':'grid';
  btn.textContent=open?'Show less':'Show more';
}
</script>
```

Bar cell (second column, no header): `<td><div style="height:6px;background:var(--color-background-secondary);border-radius:2px;"><div style="width:[N]%;height:100%;background:var(--color-text-secondary);border-radius:2px;"></div></div></td>` — width % = sessions ÷ max sessions in that table × 100. Name cell contains name text only — no bar.

---

## Priority cards

Top 3 ranked by sessions affected (descending). If more signals exist, add a muted line: "N more signals — ask to see them."

Sessions affected — use the sessions most directly impacted:
- Low add-to-cart rate → view sessions for that product
- Cart abandonment → ATC sessions for that product
- Low collection conversion → sessions that viewed the collection
- Underperforming product type → sessions that viewed that type
- High bounce rate → view sessions for that product

Signal type labels: LOW ADD-TO-CART RATE · CART ABANDONMENT · LOW COLLECTION CONVERSION · UNDERPERFORMING PRODUCT TYPE · HIGH BOUNCE RATE

**Card template:**

```html
<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);display:flex;align-items:center;justify-content:space-between;">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">[Signal type]</span>
    <span style="font-size:11px;font-weight:500;padding:2px 8px;border-radius:4px;background:var(--color-background-tertiary);color:var(--color-text-secondary);">~[N] sessions affected</span>
  </div>
  <div style="background:var(--color-background-primary);padding:20px;">
    <p style="font-size:15px;font-weight:500;margin:0 0 8px;color:var(--color-text-primary);">[Product or collection name]</p>
    <p style="font-size:14px;color:var(--color-text-secondary);line-height:1.6;margin:0 0 16px;">[Key number + why it matters in one sentence]</p>
    <button onclick="sendPrompt(&quot;Investigate this product signal: [signal type] — [product/collection name], [domain], [key metrics], [follow-up data already gathered]&quot;)" style="padding:6px 14px;font-size:13px;font-weight:500;color:var(--color-text-primary);background:var(--color-background-secondary);border:0.5px solid var(--color-border-tertiary);border-radius:6px;cursor:pointer;">Investigate ↗</button>
  </div>
</div>
```

Each card body contains exactly three things: the product/collection name, one sentence of finding, and the Investigate button. No tables, no metrics, no bullet points, no additional data — all supporting evidence lives in the Investigate flow.

**If no signals are found**, render a single card in place of the priority cards:

```html
<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">No Priority Signals</span>
  </div>
  <div style="background:var(--color-background-primary);padding:20px;">
    <p style="font-size:14px;color:var(--color-text-secondary);line-height:1.6;margin:0;">[One sentence: what the data shows and why no signals stand out — e.g. "CVR and ATC rates are consistent across top products and collections, with no outliers above the traffic thresholds for this store size."]</p>
  </div>
</div>
```

---

## Action bar

Rendered as the last element of the same `show_widget`, after all priority cards.

Wrap the buttons in a card container (same chrome as the other cards). Schedule report is the primary action — filled dark button. Export PDF is secondary — outlined.

```html
<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);overflow:hidden;">
  <div style="background:var(--color-background-secondary);padding:8px 20px;border-bottom:0.5px solid var(--color-border-tertiary);">
    <span style="font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.06em;">Export &amp; Schedule</span>
  </div>
  <div style="background:var(--color-background-primary);padding:16px 20px;display:flex;gap:8px;justify-content:flex-end;">
    <button onclick="sendPrompt('Export product analysis as PDF for [domain]')"
      style="padding:6px 14px;font-size:13px;font-weight:500;color:var(--color-text-primary);background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);border-radius:6px;cursor:pointer;">
      Download Report
    </button>
    <button onclick="sendPrompt('Schedule product analysis for [domain]')"
      style="padding:6px 14px;font-size:13px;font-weight:500;color:var(--color-background-primary);background:var(--color-text-primary);border:0.5px solid var(--color-text-primary);border-radius:6px;cursor:pointer;">
      [Schedule Insights — OR — Edit schedule if a task already exists]
    </button>
  </div>
</div>
```
