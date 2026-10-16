# Scheduling widget

Triggered when the operator clicks the "Schedule recurring scan" button. Load `show_widget` via ToolSearch and call it with `title: "schedule_tech_scan"` and loading messages `["Setting up schedule..."]`.

The widget renders fully expanded.

## Widget

```html
<style>
.chip{padding:6px 14px;font-size:13px;font-weight:500;border-radius:100px;cursor:pointer;background:var(--color-background-primary) !important;border:1px solid var(--color-border-tertiary) !important;color:var(--color-text-secondary) !important;}
.chip.on{background:#E6F1FB !important;border:1.5px solid #185FA5 !important;color:#0C447C !important;}
.fcard{padding:14px 10px;font-size:13px;font-weight:500;text-align:center;border-radius:var(--border-radius-md);cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:6px;background:var(--color-background-primary) !important;border:1px solid var(--color-border-tertiary) !important;color:var(--color-text-secondary) !important;}
.fcard.on{background:#E6F1FB !important;border:1.5px solid #185FA5 !important;color:#0C447C !important;}
.slabel{font-size:11px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:0.07em;margin:0 0 10px;}
.acard{border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-md);overflow:hidden;margin-bottom:8px;}
.acard.on{border-color:#185FA5;}
.acard-header{display:flex;align-items:center;gap:12px;padding:14px 16px;cursor:pointer;}
.atoggle{width:18px;height:18px;border-radius:4px;border:1.5px solid var(--color-border-tertiary);flex-shrink:0;display:flex;align-items:center;justify-content:center;}
.acard.on .atoggle{background:#185FA5;border-color:#185FA5;}
.acard-fields{padding:0 16px 14px;border-top:0.5px solid var(--color-border-tertiary);}
.afield-label{font-size:12px;font-weight:500;color:var(--color-text-secondary);margin:10px 0 6px;}
.ainput{width:100%;padding:8px 10px;font-size:13px;border:0.5px solid var(--color-border-tertiary);border-radius:6px;background:var(--color-background-secondary);color:var(--color-text-primary);box-sizing:border-box;}
</style>

<div style="border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);background:var(--color-background-primary);overflow:hidden;">
  <div style="padding:16px 20px 20px;">
    <p style="font-size:15px;font-weight:500;color:var(--color-text-primary);margin:0 0 24px;">Set up automations</p>

    <p class="slabel">Frequency</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:24px;" id="freq-wrap">
      <button class="fcard on" onclick="selectFreq(this)" data-value="weekly"><i class="ti ti-calendar" aria-hidden="true"></i>Weekly</button>
      <button class="fcard" onclick="selectFreq(this)" data-value="biweekly"><i class="ti ti-calendar-stats" aria-hidden="true"></i>Bi-weekly</button>
      <button class="fcard" onclick="selectFreq(this)" data-value="monthly"><i class="ti ti-calendar-month" aria-hidden="true"></i>Monthly</button>
    </div>

    <div id="day-section" style="margin-bottom:24px;">
      <p class="slabel">Day</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button class="chip on" onclick="selectDay(this)" data-value="Monday">Mon</button>
        <button class="chip" onclick="selectDay(this)" data-value="Tuesday">Tue</button>
        <button class="chip" onclick="selectDay(this)" data-value="Wednesday">Wed</button>
        <button class="chip" onclick="selectDay(this)" data-value="Thursday">Thu</button>
        <button class="chip" onclick="selectDay(this)" data-value="Friday">Fri</button>
      </div>
    </div>

    <div style="margin-bottom:24px;">
      <p class="slabel">Time</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;" id="time-section">
        <button class="chip" onclick="selectTime(this)" data-value="7:00 AM">7 am</button>
        <button class="chip on" onclick="selectTime(this)" data-value="9:00 AM">9 am</button>
        <button class="chip" onclick="selectTime(this)" data-value="12:00 PM">12 pm</button>
        <button class="chip" onclick="selectTime(this)" data-value="5:00 PM">5 pm</button>
      </div>
    </div>

    <p class="slabel">Automate</p>
    <p style="font-size:12px;color:var(--color-text-tertiary);margin:-4px 0 12px;">Select at least one. When automation runs, your digest shows links. When it can't run, it shows a prompt to copy into Cowork.</p>

    <!-- Auto-draft PR -->
    <div class="acard" id="pr-card">
      <div class="acard-header" onclick="toggleAuto('pr')">
        <div class="atoggle" id="pr-toggle"><svg id="pr-check" width="10" height="10" viewBox="0 0 10 10" fill="none" style="display:none"><path d="M1.5 5L4 7.5L8.5 2.5" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div>
          <p style="font-size:14px;font-weight:500;color:var(--color-text-primary);margin:0 0 2px;">Auto-draft PR</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">Creates a draft PR for each fixable error — ready to review and merge</p>
        </div>
      </div>
      <div class="acard-fields" id="pr-fields" style="display:none;">
        <p class="afield-label">GitHub repo</p>
        <input class="ainput" id="pr-repo" placeholder="mycompany/my-store" />
      </div>
    </div>

    <!-- Auto-create tickets -->
    <div class="acard" id="ticket-card">
      <div class="acard-header" onclick="toggleAuto('ticket')">
        <div class="atoggle" id="ticket-toggle"><svg id="ticket-check" width="10" height="10" viewBox="0 0 10 10" fill="none" style="display:none"><path d="M1.5 5L4 7.5L8.5 2.5" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div>
          <p style="font-size:14px;font-weight:500;color:var(--color-text-primary);margin:0 0 2px;">Auto-create tickets</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">Opens a ticket for each fixable finding</p>
        </div>
      </div>
      <div class="acard-fields" id="ticket-fields" style="display:none;">
        <p class="afield-label">Platform</p>
        <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;" id="ticket-platform-wrap">
          <button class="chip" onclick="selectTicketPlatform(this)" data-value="linear">Linear</button>
          <button class="chip" onclick="selectTicketPlatform(this)" data-value="jira">Jira</button>
          <button class="chip" onclick="selectTicketPlatform(this)" data-value="github-issues">GitHub Issues</button>
          <button class="chip" onclick="selectTicketPlatform(this)" data-value="notion">Notion</button>
        </div>
        <p class="afield-label">Team / project</p>
        <input class="ainput" id="ticket-team" placeholder="e.g. Issues Team" />
      </div>
    </div>

    <!-- Auto-share report -->
    <div class="acard" id="share-card">
      <div class="acard-header" onclick="toggleAuto('share')">
        <div class="atoggle" id="share-toggle"><svg id="share-check" width="10" height="10" viewBox="0 0 10 10" fill="none" style="display:none"><path d="M1.5 5L4 7.5L8.5 2.5" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div>
          <p style="font-size:14px;font-weight:500;color:var(--color-text-primary);margin:0 0 2px;">Auto-share report</p>
          <p style="font-size:12px;color:var(--color-text-secondary);margin:0;">Sends a findings digest of your top tech issues</p>
        </div>
      </div>
      <div class="acard-fields" id="share-fields" style="display:none;">
        <p class="afield-label">Send to</p>
        <p style="font-size:12px;color:var(--color-text-tertiary);margin:0 0 8px;">At least one required.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;" id="share-channels">
          <button class="chip" onclick="toggleChip(this)" data-value="email"><i class="ti ti-mail" style="font-size:14px;vertical-align:-1px;margin-right:4px;" aria-hidden="true"></i>Email</button>
          <button class="chip" onclick="toggleChip(this)" data-value="slack"><i class="ti ti-brand-slack" style="font-size:14px;vertical-align:-1px;margin-right:4px;" aria-hidden="true"></i>Slack</button>
          <button class="chip" onclick="toggleChip(this)" data-value="notion"><i class="ti ti-brand-notion" style="font-size:14px;vertical-align:-1px;margin-right:4px;" aria-hidden="true"></i>Notion</button>
        </div>
      </div>
    </div>

    <div style="display:flex;justify-content:flex-end;align-items:center;gap:12px;border-top:0.5px solid var(--color-border-tertiary);padding-top:16px;margin-top:16px;">
      <button onclick="sendPrompt('Skip scheduling for now')" style="padding:7px 16px;font-size:13px;font-weight:500;color:var(--color-text-secondary);background:transparent;border:none;cursor:pointer;">Skip</button>
      <button onclick="submitSchedule()" style="padding:7px 20px;font-size:13px;font-weight:500;color:var(--color-text-primary);background:var(--color-background-secondary);border:0.5px solid var(--color-border-secondary);border-radius:var(--border-radius-md);cursor:pointer;">Confirm</button>
    </div>
  </div>
</div>

<script>
var autoState={pr:false,ticket:false,share:false};
function toggleAuto(id){
  autoState[id]=!autoState[id];
  var card=document.getElementById(id+'-card');
  var fields=document.getElementById(id+'-fields');
  var check=document.getElementById(id+'-check');
  if(autoState[id]){card.classList.add('on');fields.style.display='block';check.style.display='block';}
  else{card.classList.remove('on');fields.style.display='none';check.style.display='none';}
}
function toggleChip(el){el.classList.toggle('on');}
function selectDay(el){document.querySelectorAll('#day-section .chip').forEach(b=>b.classList.remove('on'));el.classList.add('on');}
function selectTime(el){document.querySelectorAll('#time-section .chip').forEach(b=>b.classList.remove('on'));el.classList.add('on');}
function selectFreq(el){
  document.querySelectorAll('#freq-wrap .fcard').forEach(b=>b.classList.remove('on'));
  el.classList.add('on');
  document.getElementById('day-section').style.display=el.dataset.value==='monthly'?'none':'block';
}
function selectTicketPlatform(el){document.querySelectorAll('#ticket-platform-wrap .chip').forEach(b=>b.classList.remove('on'));el.classList.add('on');}
function submitSchedule(){
  var freq=document.querySelector('#freq-wrap .fcard.on')?.dataset.value||'weekly';
  var day=document.querySelector('#day-section .chip.on')?.dataset.value||'Monday';
  var time=document.querySelector('#time-section .chip.on')?.dataset.value||'9:00 AM';
  var parts=['frequency='+freq,'day='+day,'time='+time];
  if(autoState.pr){
    var repo=document.getElementById('pr-repo').value.trim();
    if(!repo){alert('Enter a GitHub repo for auto-draft PR.');return;}
    parts.push('auto_pr='+repo);
  }
  if(autoState.ticket){
    var platform=document.querySelector('#ticket-platform-wrap .chip.on')?.dataset.value;
    var team=document.getElementById('ticket-team').value.trim();
    if(!platform||!team){alert('Select a ticket platform and enter a team or project name.');return;}
    parts.push('auto_tickets='+platform+':'+team);
  }
  if(autoState.share){
    var shareChans=[...document.querySelectorAll('#share-channels .chip.on')].map(b=>b.dataset.value);
    if(!shareChans.length){alert('Select at least one delivery channel for the report.');return;}
    parts.push('auto_share='+shareChans.join('+'));
  }
  if(!autoState.pr&&!autoState.ticket&&!autoState.share){alert('Enable at least one automation.');return;}
  sendPrompt('Schedule tech scan: '+parts.join(', '));
}
</script>
```

## On submit

**Step 1 — Connector check.** Before doing anything else, silently check which of the following are missing from the current session: GitHub tools, Claude in Chrome tools. If any are missing, send one combined message and wait for a reply before continuing:

> "Before I set this up — connecting **[list of missing]** would make each scheduled scan more accurate. [One-line benefit per missing connector: GitHub → lets me point to the exact file and line that needs fixing; Claude in Chrome → lets me run live performance tests in a real browser.] Want to connect any of these now, or go ahead without them?"

- If they want to connect: call `suggest_connectors` for GitHub (UUID `fe983ccb-92c7-4df1-85af-b1c3340b89bb`); for Chrome, direct them to Settings → Customize. Wait for confirmation, then proceed.
- If they skip or say go ahead: proceed immediately, no follow-up.
- If both connectors are already present: skip this step entirely, say nothing.

**Step 2 — Automation connectors.** For each enabled automation that requires a connector, check if it's connected and connect it now if not:
- **auto_pr**: GitHub — UUID `fe983ccb-92c7-4df1-85af-b1c3340b89bb`
- **auto_tickets**: Linear (search registry), Jira (search registry), GitHub Issues `fe983ccb-92c7-4df1-85af-b1c3340b89bb`, Notion `69f3a300-cc60-48c4-b237-dfac56530dbf`
- **auto_share**: Slack `597f662f-36de-437e-836e-5a81013cbfbe`, Notion `69f3a300-cc60-48c4-b237-dfac56530dbf`, Email/Gmail (search registry)

Ask for any missing delivery details (email address, Slack channel, Notion page) before creating the task. Then create with `create_scheduled_task`. Task name: `tech-scan-[domain]`.

---

## Scheduled task prompt

> Run /tech-diagnosis for [domain]. When the proactive scan completes, execute the following automations for each finding, then compile a digest.
>
> **Automations:**
> [If auto_pr] For each fixable error and fixable performance issue: determine the fix, create a branch named `fix/[plain-description]` in repo [repo], commit the change, and open a draft PR titled with a plain-English summary. Collect the PR URL.
> [If auto_tickets] For each fixable JS error and performance issue (not vendor issues): create a ticket in [platform] / [team] with full diagnosis content. Ticket body (markdown): Summary paragraph → Technical details → Cause → Fix (recommended fix + any alternative). Priority mapping: critical → high; standard → medium. Title: `[severity] [summary] (affecting [segment])`. Collect the ticket URL.
> [If auto_share] Send the full digest (with Cowork prompts) to [destination] via [channel].
>
> **Digest format (for auto_share):**
> Title: `Tech scan — [domain] — [date]`. Structure: Overview block first, then findings in fixed order — fixable errors, performance issues, vendor issues. Up to 2 per category.
>
> Each finding includes: signal type label, one-line description, occurrence/session count, then one line per completed automation showing its link (e.g. "Draft PR: [url]" · "Ticket: [url]"). For any automation that could not run (connector unavailable, fix not a code change, etc.), show instead: "Type the following in Cowork:" followed by the relevant prompt.
>
> **Cowork prompts per finding type (fallback for auto_share):**
> - Fixable error: `/tech-diagnosis fix #[issue-id] on [domain]`
> - Vendor error: `/tech-diagnosis share with vendor #[issue-id] on [domain]`
> - Performance: `/tech-diagnosis fix [LCP|INP|CLS] on [page-url] for [domain]`

**Per channel:**
- **Email:** Subject: digest or overview title. Wrap Cowork prompts in `<code>`.
- **Slack:** Bold the title. Cowork prompts in backtick code blocks.
- **Notion:** Page title = digest/overview title. Each finding as heading + paragraph. Cowork prompts as fenced code blocks (triple backticks, unescaped).
