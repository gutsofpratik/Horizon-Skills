# HTML Generation Reference

This document contains all writing rules, button action wiring, and output file generation instructions
for producing Pendo guide HTML files. It is a self-contained reference — everything needed to generate
valid guide output is here.

---

## Copy Guidelines

Apply these writing rules universally:

- **Short and sweet**: Use the fewest words that are still effective. Never use 10 steps when 5 will do.
- **Active voice**: Write in active voice. No passive constructions.
- **No jargon**: Write for the end user, not internal teams. Avoid internal terminology.
- **No redundancy**: Don't repeat button copy in body text. Don't state the obvious.
- **Clear CTA**: Every step must have a clear call-to-action.
- **Proper spacing**: Always ensure proper spacing between sentences. Use correct punctuation throughout.
- **Sentence case for body, Title Case for headings**.

---

## Button Text Rules

- **Primary buttons**: Action-oriented — "Get Started", "Try Now", "Learn More", "Continue", "Next", "Finish", "Done"
- **Secondary buttons**: Passive — "Skip", "Later", "Cancel", "Not Now", "Back"
- **Walkthrough middle steps**: Primary = "Next" or "Continue" → `actions.advance(this)`, Secondary = "Back" → `actions.previous(this)`
- **Walkthrough finish step**: Primary = "Finish" or "Done" → `actions.advance(this)`, no secondary button
- **Dismissal buttons**: "Dismiss", "Close", "No thanks", "Cancel" → `actions.dismiss(this)`
- **Corner X close control**: the top-right × → `actions.dismiss(this)` (see Element IDs below)
- **Snooze buttons**: "Skip", "Later", "Not now", "Remind me later" → `actions.snooze(this, 86400000)`
- **Poll submit**: "Submit", "Send feedback" → `actions.submit(this)`
- **Link buttons**: "Learn more", "View docs", "Try it" (with URL) → `actions.openLink(this, url, '_blank')`
- **Never use**: "Click here", "OK" (unless it's a system-level alert)

---

## Length Limits

| Guide Type      | Max Copy Length                     |
|-----------------|-------------------------------------|
| Tooltip         | ~2 lines                            |
| Lightbox/Modal  | 1 paragraph or 4 lines; use bullets |
| Banner          | 1–2 sentences                       |
| Announcement    | 1 paragraph; generate excitement    |
| Poll            | 1 concise question per step         |

---

## Tone

- Friendly and approachable, never corporate or stiff
- Enthusiastic about features without being hyperbolic
- Respect the user's time — be concise

---

## Wire Button Actions

Every button in a Pendo guide must be wired to a **guide action**. Actions are dispatched via the
`actions` factory object — a plain JS helper created fresh inside each step's script wrapper IIFE.
See `references/pendo-components.md` for full API.

### Supported Actions

Each action takes the clicked element itself as its first argument (`this` from the click handler),
so the factory can derive the `elementId` and `elementType` it passes to `step.trackAction`.

| Action | Method | When to use |
|--------|--------|-------------|
| Advance guide | `actions.advance(this)` | Primary button that moves to the next step ("Next", "Continue", "Got it", "Get Started") |
| Previous step | `actions.previous(this)` | Secondary button that goes back one step ("Back", "Previous") |
| Dismiss guide | `actions.dismiss(this)` | Any control that closes the guide — the corner X, "Dismiss", "Close", "No thanks", "Cancel" |
| Snooze guide | `actions.snooze(this, 86400000)` | Button that hides the guide temporarily — default 1 day / 86400000ms ("Remind me later", "Not now", "Later", "Skip") |
| Submit poll + advance | `actions.submit(this)` | Button that submits poll/survey responses then advances ("Submit", "Send feedback") — one event |
| URL link | `actions.openLink(this, url, '_blank')` | Button or link that opens a URL in a new tab ("Learn more", "View docs", "Try it") |

### Button Text to Action Mapping

Apply these mappings when wiring button click handlers:

**Primary buttons (advance the guide forward):**
- "Next", "Continue", "Got it", "Get Started" → `actions.advance(this)`
- "Finish", "Done" (last step) → `actions.advance(this)` (advances past the final step, closing the guide)
- "Submit", "Send" (poll context) → `actions.submit(this)`

**Secondary buttons (passive/escape actions):**
- "Back", "Previous" → `actions.previous(this)`
- "Skip", "Later", "Not now", "Remind me later" → `actions.snooze(this, 86400000)`
- "Dismiss", "Close", "Cancel", "No thanks", corner X → `actions.dismiss(this)`

**Link-style buttons:**
- Any button whose purpose is to open a URL → `actions.openLink(this, 'https://...', '_blank')`
- If the guide should also close after opening the link, follow with `actions.dismiss(this)`

### Element IDs

Give every interactive element a stable `id`. The id feeds `uiElementId` in analytics and drives how
guide metrics classify the element:

- **Corner X close control** (the × in the top-right that dismisses the guide): use
  `id="pendo-close-guide-<hash>"` and set its visible text to `×`. This is what makes guide metrics
  label it a **"Close Button"** (both the element-type classification and the display name depend on it).
  Only the corner X gets this id — a "No thanks"/"Cancel" button that also dismisses is a regular button.
- **All other buttons and links**: use `id="pendo-button-<hash>"`, matching Pendo's native convention.
- `<hash>` is an 8-character random hex string (same style as poll ids), unique within the step.

### Element action metadata (`data-pendo-action`)

Also stamp each interactive element with a `data-pendo-action` attribute — a JSON array of the same
guideActivity action(s) the element reports through `step.trackAction`. `trackAction` only fires on click,
so guide metrics can't show an element's Action until it has at least one recorded click. The
`data-pendo-action` attribute lets metrics read the intended action straight from the stored HTML, so
every element shows its correct Action even with zero clicks.

Use the guideActivity action name(s) — the same values the `actions` methods pass to `track` — and wrap
the attribute in single quotes so the inner JSON can use double quotes:

| Action method            | `data-pendo-action`            |
|--------------------------|--------------------------------|
| `actions.advance(this)`  | `[{"action":"advanceGuide"}]`  |
| `actions.previous(this)` | `[{"action":"previousStep"}]`  |
| `actions.dismiss(this)`  | `[{"action":"dismissGuide"}]`  |
| `actions.snooze(this)`   | `[{"action":"guideSnoozed"}]`  |
| `actions.submit(this)`   | `[{"action":"submitPoll"}]`    |
| `actions.openLink(...)`  | `[{"action":"openLink"}]`      |

Keep `data-pendo-action` in sync with the handler — a button whose click calls `actions.advance(this)`
carries `data-pendo-action='[{"action":"advanceGuide"}]'`. For submit buttons list only `submitPoll`;
guide metrics expands it to "Submit Poll & Next Step".

### Rules

- Every button MUST have an action. No button should be purely decorative.
- Every interactive element MUST have a tracked `id` and a matching `data-pendo-action` attribute (see
  "Element IDs" and "Element action metadata" above), so it appears in guide metrics with the right Action.
- Use `addEventListener('click', ...)` for binding — never inline `onclick` attributes (CSP compatibility).
- Pass the clicked element (`this`) into the action — never `this.id`. The factory reads the id, tag,
  and text off the element and reports a `guideActivity` event before performing the behavior (see Analytics).
- For poll guides, use `<pendo-poll>` elements to declare and store responses, then call `actions.submit()`
  to send all values to Pendo and advance in one step. See the Poll Data section below.
- The snooze duration (86400000ms = 1 day) is the default. Adjust if the user specifies a different interval.

### Analytics (guideActivity)

Code-block guide clicks do not automatically produce `guideActivity` analytics, because the injected
HTML buttons are not part of the guide's `domJson` tree. The `actions` factory closes this gap by calling
`step.trackAction(...)` — a public method on the step — before running each behavior. From the passed
element it stages a `guideActivity` event with `uiElementId` (the element id), `uiElementType` (the tag,
e.g. `BUTTON`/`A`), and the action(s) performed. No visible text is captured; guide metrics displays
deleted code-block elements by their element id.

- `step.trackAction` is guarded (`if (step.trackAction)`) so guides still work on older agents that lack it.
- The behavior call (`step.advance()`, `step.dismiss()`, etc.) is unchanged; `trackAction` only adds analytics.
- `actions.submit` fires a single event with one `submitPoll` action — guide metrics expands that into
  "Submit Poll & Next Step", so do NOT also emit a separate advance event for the same click.
- Do not fire analytics yourself elsewhere — the factory is the single place that calls `trackAction`.

---

## Poll Data (Headless Components)

When a guide collects user input (ratings, free text, multiple choice), use `<pendo-poll>` elements
to declare each data field. The `actions.submit()` method in the script wrapper handles collecting all
values, calling `step.response()`, reporting a single `submitPoll` `guideActivity` event, and advancing.

### Poll ID Format

All poll IDs follow: `cb-{Type}-{shortRandom}`

- `cb` = code block origin prefix
- `{Type}` = data type: `NumberScale`, `FreeForm`, `SingleChoice`, `MultiSelect`, `Boolean`, or `Ranking`
- `{shortRandom}` = 8-character random hex

Examples: `cb-NumberScale-e7a21f04`, `cb-SingleChoice-a1b2c3d4`, `cb-MultiSelect-f5e6d7c8`

### Declaring polls

Add one invisible `<pendo-poll>` element per data field, placed after the visual HTML.
The `type` describes the data shape — the component handles serialization internally:

- **Always set `question="…"` on each `<pendo-poll>`**, copied verbatim from the visible question
  label you wrote for that poll. This is what links the prompt text to the poll id so it appears on
  the Poll Metrics page — the visible `<p>`/heading copy is NOT machine-readable. Escape the value
  for an HTML attribute (`&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`).
- **For `NumberScale` polls, set `scale="min-max"`** (e.g. `scale="1-5"`) matching the visible rating
  range. This lets the Poll Metrics distribution chart render its scale buckets. `Boolean` polls need
  no scale (they default to 0/1); text and choice types don't use it.

```html
<pendo-poll poll-id="cb-NumberScale-e7a21f04" type="NumberScale" scale="1-5" question="How satisfied are you?"></pendo-poll>
<pendo-poll poll-id="cb-SingleChoice-a1b2c3d4" type="SingleChoice" question="Which plan fits you?"></pendo-poll>
<pendo-poll poll-id="cb-FreeForm-b8c93d12" type="FreeForm" question="Anything else?"></pendo-poll>
```

### Storing values from custom UI

In the script wrapper, wire custom UI interactions to `.setValue()`:

```javascript
// Rating buttons
document.querySelectorAll('.rating-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    document.querySelector('[poll-id="cb-NumberScale-e7a21f04"]').setValue(parseInt(btn.dataset.value));
  });
});

// Free text
document.getElementById('feedback-input').addEventListener('input', function(e) {
  document.querySelector('[poll-id="cb-FreeForm-b8c93d12"]').setValue(e.target.value);
});

// Submit all polls + advance (single guideActivity event; the metrics UI expands
// submitPoll into "Submit Poll & Next Step")
// Markup: <button id="pendo-button-4d5e6f7a" data-pendo-action='[{"action":"submitPoll"}]'>Submit</button>
document.getElementById('pendo-button-4d5e6f7a').addEventListener('click', function() {
  actions.submit(this);
});
```

### Deployment requirement

Generated poll IDs MUST be registered in the step's `pollIds` array in the guide configuration.
Without this, `step.response()` will not exist and `actions.submit()` will not send data.

Include a comment at the top of generated poll guides listing the required poll IDs:

```html
<!-- DEPLOYMENT: Add these to step.pollIds: cb-NumberScale-e7a21f04, cb-FreeForm-b8c93d12 -->
```

---

## Generate the Output Files

Produce **one `.html` file per step**. Each step is a self-contained HTML/CSS/JS file — this matches
how Pendo's code block module works (one content payload per step). The Pendo agent handles rendering
each step at the right time and managing transitions between them.

For a 3-step walkthrough, produce 3 files: `step-1.html`, `step-2.html`, `step-3.html`.

### File structure (per step)
```html
<style id="pendo-inline-css" type="text/css">
  /* CSS for this step */
  .guide-container { position: relative; }
  .guide-close { position: absolute; top: 8px; right: 8px; width: 24px; height: 24px; border: none; background: transparent; font-size: 18px; line-height: 1; cursor: pointer; color: #555; }
</style>

<!-- HTML content for this step only -->
<div class="guide-container">
  <!-- Top-right X close control. Use a pendo-close-guide-<hash> id and × text so it
       is classified as "Close Button" in guide metrics. Omit for guides with no corner X. -->
  <button class="guide-close" id="pendo-close-guide-1a2b3c4d" aria-label="Close" data-pendo-action='[{"action":"dismissGuide"}]'>×</button>
  <h2>Step heading</h2>
  <p>Step body copy.</p>
  <div class="guide-buttons">
    <button id="pendo-button-2b3c4d5e" data-pendo-action='[{"action":"previousStep"}]'>Back</button>
    <button id="pendo-button-3c4d5e6f" data-pendo-action='[{"action":"advanceGuide"}]'>Next</button>
  </div>
</div>

<!-- Data layer (invisible, only needed for poll guides) -->
<!-- <pendo-poll poll-id="cb-NumberScale-xxxxxxxx" type="NumberScale" scale="1-5" question="How would you rate this?"></pendo-poll> -->

<script id="pendo-inline-script">
/*BEGIN PENDO PREVIEW STUBS*/
(function() {
  var toastCount = 0;
  function showToast(msg) {
    var t = document.createElement('div');
    var offset = 20 + (toastCount * 48);
    t.style.cssText = 'position:fixed;top:' + offset + 'px;right:20px;padding:12px 20px;border-radius:8px;background:#1a1a2e;color:#fff;font:14px system-ui,sans-serif;z-index:' + (99999 + toastCount) + ';opacity:0;transition:opacity 0.3s;pointer-events:none;';
    t.textContent = msg;
    document.body.appendChild(t);
    toastCount++;
    requestAnimationFrame(function() { t.style.opacity = '1'; });
    setTimeout(function() { t.style.opacity = '0'; setTimeout(function() { t.remove(); toastCount--; }, 300); }, 2500);
  }
  window.step = {
    advance: function() { showToast('→ step.advance()'); },
    dismiss: function() { showToast('✕ step.dismiss()'); },
    response: function(r) { showToast('✓ step.response(' + JSON.stringify(r) + ')'); },
    eventRouter: { eventable: { trigger: function(name, evt) {
      if (evt && evt.action === 'openLink') {
        var url = evt.params && evt.params[0] && evt.params[0].value;
        showToast('🔗 openLink(' + url + ')');
      } else {
        showToast('⚡ ' + (evt && evt.action || name));
      }
    }}}
  };
  window.guide = { id: 'preview-guide', findStepById: function() { return window.step; } };
  window.pendo = window.pendo || {};
  window.pendo.onGuidePrevious = function() { showToast('← pendo.onGuidePrevious()'); };
  window.pendo.onGuideSnoozed = function(a, b, d) { showToast('⏸ pendo.onGuideSnoozed(' + d + 'ms)'); };
  window.pendo.findGuideById = function() { return window.guide; };
})();
/*END PENDO PREVIEW STUBS*/

/*BEGIN COMPONENT REGISTRATION*/
(function(){if(customElements.get('pendo-poll'))return;var B={NumberScale:'NumberScale',FreeForm:'FreeForm',SingleChoice:'FreeForm',MultiSelect:'FreeForm',Boolean:'NumberScale',Ranking:'FreeForm'};class PendoPoll extends HTMLElement{connectedCallback(){this.style.display='none';this._value=undefined}get pollId(){return this.getAttribute('poll-id')}get type(){return this.getAttribute('type')}get backendType(){return B[this.type]||'FreeForm'}setValue(v){this._value=v;this.dispatchEvent(new CustomEvent('pendo-poll-change',{detail:{pollId:this.pollId,value:v,type:this.type},bubbles:true}))}getValue(){return this._value}getSerializedValue(){var v=this._value;if(v===undefined||v===null)return undefined;switch(this.type){case'NumberScale':return typeof v==='number'?v:parseInt(v,10);case'Boolean':return v?1:0;case'MultiSelect':case'Ranking':return Array.isArray(v)?JSON.stringify(v):String(v);default:return String(v)}}hasValue(){if(this._value===undefined||this._value===null)return false;if(this.type==='MultiSelect'||this.type==='Ranking')return Array.isArray(this._value)&&this._value.length>0;return this._value!==''}}customElements.define('pendo-poll',PendoPoll)})();
/*END COMPONENT REGISTRATION*/

(function(step, guide, pendo) {
  var polls = document.querySelectorAll('pendo-poll');

  // Reports a guideActivity analytics event for `el`, deriving id/type/text from
  // the DOM element, then the caller performs the behavior. `el` is the clicked
  // element (pass `this` from the handler). Guarded so guides still work on older
  // agents (and in local preview) that lack step.trackAction.
  function track(el, acts) {
    if (!step.trackAction || !el) return;
    step.trackAction({ elementId: el.id, elementType: el.tagName, actions: acts });
  }

  var actions = {
    submit: function(el) {
      var responses = [];
      polls.forEach(function(p) {
        if (p.hasValue()) responses.push({ pollId: p.pollId, value: p.getSerializedValue() });
      });
      if (responses.length) step.response(responses);
      track(el, [{ action: 'submitPoll' }]);
      step.advance();
    },
    advance: function(el) { track(el, [{ action: 'advanceGuide' }]); step.advance(); },
    previous: function(el) { track(el, [{ action: 'previousStep' }]); pendo.onGuidePrevious(); },
    dismiss: function(el) { track(el, [{ action: 'dismissGuide' }]); step.dismiss(); },
    snooze: function(el, d) { d = d || 86400000; track(el, [{ action: 'guideSnoozed', duration: d, timeUnit: 'ms' }]); pendo.onGuideSnoozed(guide.id, step.id, d); },
    openLink: function(el, url, target) {
      target = target || '_blank';
      track(el, [{ action: 'openLink', url: url, target: target }]);
      step.eventRouter.eventable.trigger('pendoEvent', {
        action: 'openLink', step: step,
        params: [{ name: 'url', value: url }, { name: 'target', value: target }]
      });
    }
  };

  document.getElementById('pendo-close-guide-1a2b3c4d').addEventListener('click', function() {
    actions.dismiss(this);
  });
  document.getElementById('pendo-button-2b3c4d5e').addEventListener('click', function() {
    actions.previous(this);
  });
  document.getElementById('pendo-button-3c4d5e6f').addEventListener('click', function() {
    actions.advance(this);
  });
})(step, guide, pendo);
</script>
```

### Script wrapper rules
- Always use the `<script id="pendo-inline-script">` tag.
- Preview stubs go first between `/*BEGIN PENDO PREVIEW STUBS*/` and `/*END PENDO PREVIEW STUBS*/`. These provide
  fake `step`, `guide`, and `pendo` objects that show a toast bubble when actions fire — enabling browser preview.
- Component registration goes between `/*BEGIN COMPONENT REGISTRATION*/` and `/*END COMPONENT REGISTRATION*/`.
  This registers the `<pendo-poll>` custom element. Always include this block — it uses a guard to prevent
  duplicate registration. Only `<pendo-poll>` is a custom element; actions are a plain JS object.
- Wrap all guide JavaScript in an IIFE: `(function(step, guide, pendo) { ... })(step, guide, pendo);` for clean
  variable scoping. Do NOT emit `/*BEGIN PENDO SCRIPT WRAPPER*/` or `/*END PENDO SCRIPT WRAPPER*/` markers — Pendo
  adds these automatically when it processes the content; emitting them here causes double-wrapping.
- The `actions` factory object MUST be created at the top of the wrapper IIFE (see template above). It provides
  `submit`, `advance`, `previous`, `dismiss`, `snooze`, and `openLink`. Use these for all button actions.
  Each action takes the clicked element (`this`) as its first argument and reports a `guideActivity`
  event via `step.trackAction(...)` before performing the behavior. The call is guarded (`if (step.trackAction)`),
  so guides still run on older agents; in local preview `step.trackAction` is simply absent and analytics is skipped.
- Never use inline `onclick` attributes — they break CSP-compliant content generation. Use `addEventListener` instead.
- The `<style>` tag must use `id="pendo-inline-css"` and `type="text/css"`.
- Do NOT wrap in `<!DOCTYPE html>`, `<html>`, `<head>`, or `<body>` tags — Pendo injects the content into its own container.

### EJS template tags
**NEVER add EJS template tags** (`<% %>`, `<%= %>`) to generated output. This includes the
`guide.id`/`step.id` variable resolution block.

### Walkthrough-specific output rules
- Each step is its own file — do NOT put multiple steps in a single file.
- Step navigation is handled by the Pendo agent via `step.advance()` and `pendo.onGuidePrevious()`.
- No need for show/hide logic, active classes, or step visibility CSS — Pendo manages that.
- Progress indicators ("Step X of Y") can be static text since each file knows its position.
- Name files with step number: `[guide-name]-step-1.html`, `[guide-name]-step-2.html`, etc.

### Complete walkthrough example (3-step with actions)

**step-1.html** — First step (snooze + advance):
```html
<style id="pendo-inline-css" type="text/css">
  .guide-container { font-family: system-ui, sans-serif; max-width: 480px; padding: 24px; border-radius: 8px; }
  .guide-container h2 { margin: 0 0 8px; font-size: 18px; color: #1a1a2e; }
  .guide-container p { margin: 0 0 20px; font-size: 14px; color: #555; line-height: 1.5; }
  .guide-progress { font-size: 12px; color: #999; margin-bottom: 12px; }
  .guide-buttons { display: flex; gap: 8px; justify-content: flex-end; }
  .btn-primary { padding: 10px 20px; border: none; border-radius: 8px; background: #1a1a2e; color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; }
  .btn-secondary { padding: 10px 20px; border: 1px solid #ccc; border-radius: 8px; background: transparent; font-size: 14px; cursor: pointer; }
</style>

<div class="guide-container">
  <p class="guide-progress">Step 1 of 3</p>
  <h2>Welcome to Analytics</h2>
  <p>Your new dashboard gives you real-time insights into how users engage with your product.</p>
  <div class="guide-buttons">
    <button class="btn-secondary" id="pendo-button-5e6f7a8b" data-pendo-action='[{"action":"guideSnoozed"}]'>Not now</button>
    <button class="btn-primary" id="pendo-button-6f7a8b9c" data-pendo-action='[{"action":"advanceGuide"}]'>Get Started</button>
  </div>
</div>

<script id="pendo-inline-script">
/*BEGIN PENDO PREVIEW STUBS*/
(function() {
  var toastCount = 0;
  function showToast(msg) {
    var t = document.createElement('div');
    var offset = 20 + (toastCount * 48);
    t.style.cssText = 'position:fixed;top:' + offset + 'px;right:20px;padding:12px 20px;border-radius:8px;background:#1a1a2e;color:#fff;font:14px system-ui,sans-serif;z-index:' + (99999 + toastCount) + ';opacity:0;transition:opacity 0.3s;pointer-events:none;';
    t.textContent = msg;
    document.body.appendChild(t);
    toastCount++;
    requestAnimationFrame(function() { t.style.opacity = '1'; });
    setTimeout(function() { t.style.opacity = '0'; setTimeout(function() { t.remove(); toastCount--; }, 300); }, 2500);
  }
  window.step = { advance: function() { showToast('→ step.advance()'); }, dismiss: function() { showToast('✕ step.dismiss()'); }, response: function(r) { showToast('✓ step.response(' + JSON.stringify(r) + ')'); }, eventRouter: { eventable: { trigger: function(name, evt) { if (evt && evt.action === 'openLink') { var url = evt.params && evt.params[0] && evt.params[0].value; showToast('🔗 openLink(' + url + ')'); } else { showToast('⚡ ' + (evt && evt.action || name)); } } } } };
  window.guide = { id: 'preview-guide', findStepById: function() { return window.step; } };
  window.pendo = window.pendo || {};
  window.pendo.onGuidePrevious = function() { showToast('← pendo.onGuidePrevious()'); };
  window.pendo.onGuideSnoozed = function(a, b, d) { showToast('⏸ pendo.onGuideSnoozed(' + d + 'ms)'); };
  window.pendo.findGuideById = function() { return window.guide; };
})();
/*END PENDO PREVIEW STUBS*/

/*BEGIN COMPONENT REGISTRATION*/
(function(){if(customElements.get('pendo-poll'))return;var B={NumberScale:'NumberScale',FreeForm:'FreeForm',SingleChoice:'FreeForm',MultiSelect:'FreeForm',Boolean:'NumberScale',Ranking:'FreeForm'};class PendoPoll extends HTMLElement{connectedCallback(){this.style.display='none';this._value=undefined}get pollId(){return this.getAttribute('poll-id')}get type(){return this.getAttribute('type')}get backendType(){return B[this.type]||'FreeForm'}setValue(v){this._value=v;this.dispatchEvent(new CustomEvent('pendo-poll-change',{detail:{pollId:this.pollId,value:v,type:this.type},bubbles:true}))}getValue(){return this._value}getSerializedValue(){var v=this._value;if(v===undefined||v===null)return undefined;switch(this.type){case'NumberScale':return typeof v==='number'?v:parseInt(v,10);case'Boolean':return v?1:0;case'MultiSelect':case'Ranking':return Array.isArray(v)?JSON.stringify(v):String(v);default:return String(v)}}hasValue(){if(this._value===undefined||this._value===null)return false;if(this.type==='MultiSelect'||this.type==='Ranking')return Array.isArray(this._value)&&this._value.length>0;return this._value!==''}}customElements.define('pendo-poll',PendoPoll)})();
/*END COMPONENT REGISTRATION*/

(function(step, guide, pendo) {
  var polls = document.querySelectorAll('pendo-poll');

  // Reports a guideActivity analytics event for `el`, deriving id/type/text from
  // the DOM element, then the caller performs the behavior. `el` is the clicked
  // element (pass `this` from the handler). Guarded so guides still work on older
  // agents (and in local preview) that lack step.trackAction.
  function track(el, acts) {
    if (!step.trackAction || !el) return;
    step.trackAction({ elementId: el.id, elementType: el.tagName, actions: acts });
  }

  var actions = {
    submit: function(el) {
      var responses = [];
      polls.forEach(function(p) {
        if (p.hasValue()) responses.push({ pollId: p.pollId, value: p.getSerializedValue() });
      });
      if (responses.length) step.response(responses);
      track(el, [{ action: 'submitPoll' }]);
      step.advance();
    },
    advance: function(el) { track(el, [{ action: 'advanceGuide' }]); step.advance(); },
    previous: function(el) { track(el, [{ action: 'previousStep' }]); pendo.onGuidePrevious(); },
    dismiss: function(el) { track(el, [{ action: 'dismissGuide' }]); step.dismiss(); },
    snooze: function(el, d) { d = d || 86400000; track(el, [{ action: 'guideSnoozed', duration: d, timeUnit: 'ms' }]); pendo.onGuideSnoozed(guide.id, step.id, d); },
    openLink: function(el, url, target) {
      target = target || '_blank';
      track(el, [{ action: 'openLink', url: url, target: target }]);
      step.eventRouter.eventable.trigger('pendoEvent', {
        action: 'openLink', step: step,
        params: [{ name: 'url', value: url }, { name: 'target', value: target }]
      });
    }
  };

  document.getElementById('pendo-button-5e6f7a8b').addEventListener('click', function() {
    actions.snooze(this, 86400000);
  });
  document.getElementById('pendo-button-6f7a8b9c').addEventListener('click', function() {
    actions.advance(this);
  });
})(step, guide, pendo);
</script>
```

**step-2.html** — Middle step (previous + advance):
```html
<style id="pendo-inline-css" type="text/css">
  .guide-container { font-family: system-ui, sans-serif; max-width: 480px; padding: 24px; border-radius: 8px; }
  .guide-container h2 { margin: 0 0 8px; font-size: 18px; color: #1a1a2e; }
  .guide-container p { margin: 0 0 20px; font-size: 14px; color: #555; line-height: 1.5; }
  .guide-progress { font-size: 12px; color: #999; margin-bottom: 12px; }
  .guide-buttons { display: flex; gap: 8px; justify-content: flex-end; }
  .btn-primary { padding: 10px 20px; border: none; border-radius: 8px; background: #1a1a2e; color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; }
  .btn-secondary { padding: 10px 20px; border: 1px solid #ccc; border-radius: 8px; background: transparent; font-size: 14px; cursor: pointer; }
</style>

<div class="guide-container">
  <p class="guide-progress">Step 2 of 3</p>
  <h2>Create Your First Report</h2>
  <p>Select any event from the sidebar to build a custom report. Try filtering by date range or segment.</p>
  <div class="guide-buttons">
    <button class="btn-secondary" id="pendo-button-7a8b9c0d" data-pendo-action='[{"action":"previousStep"}]'>Back</button>
    <button class="btn-primary" id="pendo-button-8b9c0d1e" data-pendo-action='[{"action":"advanceGuide"}]'>Next</button>
  </div>
</div>

<script id="pendo-inline-script">
/*BEGIN PENDO PREVIEW STUBS*/
(function() {
  var toastCount = 0;
  function showToast(msg) {
    var t = document.createElement('div');
    var offset = 20 + (toastCount * 48);
    t.style.cssText = 'position:fixed;top:' + offset + 'px;right:20px;padding:12px 20px;border-radius:8px;background:#1a1a2e;color:#fff;font:14px system-ui,sans-serif;z-index:' + (99999 + toastCount) + ';opacity:0;transition:opacity 0.3s;pointer-events:none;';
    t.textContent = msg;
    document.body.appendChild(t);
    toastCount++;
    requestAnimationFrame(function() { t.style.opacity = '1'; });
    setTimeout(function() { t.style.opacity = '0'; setTimeout(function() { t.remove(); toastCount--; }, 300); }, 2500);
  }
  window.step = { advance: function() { showToast('→ step.advance()'); }, dismiss: function() { showToast('✕ step.dismiss()'); }, response: function(r) { showToast('✓ step.response(' + JSON.stringify(r) + ')'); }, eventRouter: { eventable: { trigger: function(name, evt) { if (evt && evt.action === 'openLink') { var url = evt.params && evt.params[0] && evt.params[0].value; showToast('🔗 openLink(' + url + ')'); } else { showToast('⚡ ' + (evt && evt.action || name)); } } } } };
  window.guide = { id: 'preview-guide', findStepById: function() { return window.step; } };
  window.pendo = window.pendo || {};
  window.pendo.onGuidePrevious = function() { showToast('← pendo.onGuidePrevious()'); };
  window.pendo.onGuideSnoozed = function(a, b, d) { showToast('⏸ pendo.onGuideSnoozed(' + d + 'ms)'); };
  window.pendo.findGuideById = function() { return window.guide; };
})();
/*END PENDO PREVIEW STUBS*/

/*BEGIN COMPONENT REGISTRATION*/
(function(){if(customElements.get('pendo-poll'))return;var B={NumberScale:'NumberScale',FreeForm:'FreeForm',SingleChoice:'FreeForm',MultiSelect:'FreeForm',Boolean:'NumberScale',Ranking:'FreeForm'};class PendoPoll extends HTMLElement{connectedCallback(){this.style.display='none';this._value=undefined}get pollId(){return this.getAttribute('poll-id')}get type(){return this.getAttribute('type')}get backendType(){return B[this.type]||'FreeForm'}setValue(v){this._value=v;this.dispatchEvent(new CustomEvent('pendo-poll-change',{detail:{pollId:this.pollId,value:v,type:this.type},bubbles:true}))}getValue(){return this._value}getSerializedValue(){var v=this._value;if(v===undefined||v===null)return undefined;switch(this.type){case'NumberScale':return typeof v==='number'?v:parseInt(v,10);case'Boolean':return v?1:0;case'MultiSelect':case'Ranking':return Array.isArray(v)?JSON.stringify(v):String(v);default:return String(v)}}hasValue(){if(this._value===undefined||this._value===null)return false;if(this.type==='MultiSelect'||this.type==='Ranking')return Array.isArray(this._value)&&this._value.length>0;return this._value!==''}}customElements.define('pendo-poll',PendoPoll)})();
/*END COMPONENT REGISTRATION*/

(function(step, guide, pendo) {
  var polls = document.querySelectorAll('pendo-poll');

  // Reports a guideActivity analytics event for `el`, deriving id/type/text from
  // the DOM element, then the caller performs the behavior. `el` is the clicked
  // element (pass `this` from the handler). Guarded so guides still work on older
  // agents (and in local preview) that lack step.trackAction.
  function track(el, acts) {
    if (!step.trackAction || !el) return;
    step.trackAction({ elementId: el.id, elementType: el.tagName, actions: acts });
  }

  var actions = {
    submit: function(el) {
      var responses = [];
      polls.forEach(function(p) {
        if (p.hasValue()) responses.push({ pollId: p.pollId, value: p.getSerializedValue() });
      });
      if (responses.length) step.response(responses);
      track(el, [{ action: 'submitPoll' }]);
      step.advance();
    },
    advance: function(el) { track(el, [{ action: 'advanceGuide' }]); step.advance(); },
    previous: function(el) { track(el, [{ action: 'previousStep' }]); pendo.onGuidePrevious(); },
    dismiss: function(el) { track(el, [{ action: 'dismissGuide' }]); step.dismiss(); },
    snooze: function(el, d) { d = d || 86400000; track(el, [{ action: 'guideSnoozed', duration: d, timeUnit: 'ms' }]); pendo.onGuideSnoozed(guide.id, step.id, d); },
    openLink: function(el, url, target) {
      target = target || '_blank';
      track(el, [{ action: 'openLink', url: url, target: target }]);
      step.eventRouter.eventable.trigger('pendoEvent', {
        action: 'openLink', step: step,
        params: [{ name: 'url', value: url }, { name: 'target', value: target }]
      });
    }
  };

  document.getElementById('pendo-button-7a8b9c0d').addEventListener('click', function() {
    actions.previous(this);
  });
  document.getElementById('pendo-button-8b9c0d1e').addEventListener('click', function() {
    actions.advance(this);
  });
})(step, guide, pendo);
</script>
```

**step-3.html** — Final step (link + advance to close):
```html
<style id="pendo-inline-css" type="text/css">
  .guide-container { font-family: system-ui, sans-serif; max-width: 480px; padding: 24px; border-radius: 8px; }
  .guide-container h2 { margin: 0 0 8px; font-size: 18px; color: #1a1a2e; }
  .guide-container p { margin: 0 0 20px; font-size: 14px; color: #555; line-height: 1.5; }
  .guide-progress { font-size: 12px; color: #999; margin-bottom: 12px; }
  .guide-buttons { display: flex; gap: 8px; justify-content: flex-end; }
  .btn-primary { padding: 10px 20px; border: none; border-radius: 8px; background: #1a1a2e; color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; }
  .btn-link { padding: 10px 20px; border: 1px solid #1a1a2e; border-radius: 8px; background: transparent; color: #1a1a2e; font-size: 14px; font-weight: 600; cursor: pointer; text-decoration: none; }
</style>

<div class="guide-container">
  <p class="guide-progress">Step 3 of 3</p>
  <h2>You're All Set</h2>
  <p>Explore on your own or check out our docs for advanced tips.</p>
  <div class="guide-buttons">
    <a class="btn-link" id="pendo-button-9c0d1e2f" data-pendo-action='[{"action":"openLink"}]'>View docs</a>
    <button class="btn-primary" id="pendo-button-0d1e2f3a" data-pendo-action='[{"action":"advanceGuide"}]'>Done</button>
  </div>
</div>

<script id="pendo-inline-script">
/*BEGIN PENDO PREVIEW STUBS*/
(function() {
  var toastCount = 0;
  function showToast(msg) {
    var t = document.createElement('div');
    var offset = 20 + (toastCount * 48);
    t.style.cssText = 'position:fixed;top:' + offset + 'px;right:20px;padding:12px 20px;border-radius:8px;background:#1a1a2e;color:#fff;font:14px system-ui,sans-serif;z-index:' + (99999 + toastCount) + ';opacity:0;transition:opacity 0.3s;pointer-events:none;';
    t.textContent = msg;
    document.body.appendChild(t);
    toastCount++;
    requestAnimationFrame(function() { t.style.opacity = '1'; });
    setTimeout(function() { t.style.opacity = '0'; setTimeout(function() { t.remove(); toastCount--; }, 300); }, 2500);
  }
  window.step = { advance: function() { showToast('→ step.advance()'); }, dismiss: function() { showToast('✕ step.dismiss()'); }, response: function(r) { showToast('✓ step.response(' + JSON.stringify(r) + ')'); }, eventRouter: { eventable: { trigger: function(name, evt) { if (evt && evt.action === 'openLink') { var url = evt.params && evt.params[0] && evt.params[0].value; showToast('🔗 openLink(' + url + ')'); } else { showToast('⚡ ' + (evt && evt.action || name)); } } } } };
  window.guide = { id: 'preview-guide', findStepById: function() { return window.step; } };
  window.pendo = window.pendo || {};
  window.pendo.onGuidePrevious = function() { showToast('← pendo.onGuidePrevious()'); };
  window.pendo.onGuideSnoozed = function(a, b, d) { showToast('⏸ pendo.onGuideSnoozed(' + d + 'ms)'); };
  window.pendo.findGuideById = function() { return window.guide; };
})();
/*END PENDO PREVIEW STUBS*/

/*BEGIN COMPONENT REGISTRATION*/
(function(){if(customElements.get('pendo-poll'))return;var B={NumberScale:'NumberScale',FreeForm:'FreeForm',SingleChoice:'FreeForm',MultiSelect:'FreeForm',Boolean:'NumberScale',Ranking:'FreeForm'};class PendoPoll extends HTMLElement{connectedCallback(){this.style.display='none';this._value=undefined}get pollId(){return this.getAttribute('poll-id')}get type(){return this.getAttribute('type')}get backendType(){return B[this.type]||'FreeForm'}setValue(v){this._value=v;this.dispatchEvent(new CustomEvent('pendo-poll-change',{detail:{pollId:this.pollId,value:v,type:this.type},bubbles:true}))}getValue(){return this._value}getSerializedValue(){var v=this._value;if(v===undefined||v===null)return undefined;switch(this.type){case'NumberScale':return typeof v==='number'?v:parseInt(v,10);case'Boolean':return v?1:0;case'MultiSelect':case'Ranking':return Array.isArray(v)?JSON.stringify(v):String(v);default:return String(v)}}hasValue(){if(this._value===undefined||this._value===null)return false;if(this.type==='MultiSelect'||this.type==='Ranking')return Array.isArray(this._value)&&this._value.length>0;return this._value!==''}}customElements.define('pendo-poll',PendoPoll)})();
/*END COMPONENT REGISTRATION*/

(function(step, guide, pendo) {
  var polls = document.querySelectorAll('pendo-poll');

  // Reports a guideActivity analytics event for `el`, deriving id/type/text from
  // the DOM element, then the caller performs the behavior. `el` is the clicked
  // element (pass `this` from the handler). Guarded so guides still work on older
  // agents (and in local preview) that lack step.trackAction.
  function track(el, acts) {
    if (!step.trackAction || !el) return;
    step.trackAction({ elementId: el.id, elementType: el.tagName, actions: acts });
  }

  var actions = {
    submit: function(el) {
      var responses = [];
      polls.forEach(function(p) {
        if (p.hasValue()) responses.push({ pollId: p.pollId, value: p.getSerializedValue() });
      });
      if (responses.length) step.response(responses);
      track(el, [{ action: 'submitPoll' }]);
      step.advance();
    },
    advance: function(el) { track(el, [{ action: 'advanceGuide' }]); step.advance(); },
    previous: function(el) { track(el, [{ action: 'previousStep' }]); pendo.onGuidePrevious(); },
    dismiss: function(el) { track(el, [{ action: 'dismissGuide' }]); step.dismiss(); },
    snooze: function(el, d) { d = d || 86400000; track(el, [{ action: 'guideSnoozed', duration: d, timeUnit: 'ms' }]); pendo.onGuideSnoozed(guide.id, step.id, d); },
    openLink: function(el, url, target) {
      target = target || '_blank';
      track(el, [{ action: 'openLink', url: url, target: target }]);
      step.eventRouter.eventable.trigger('pendoEvent', {
        action: 'openLink', step: step,
        params: [{ name: 'url', value: url }, { name: 'target', value: target }]
      });
    }
  };

  document.getElementById('pendo-button-9c0d1e2f').addEventListener('click', function() {
    actions.openLink(this, 'https://docs.example.com/analytics', '_blank');
  });
  document.getElementById('pendo-button-0d1e2f3a').addEventListener('click', function() {
    actions.advance(this);
  });
})(step, guide, pendo);
</script>
```

### Styling defaults (if no org styles provided)
- Background: `#ffffff`
- Primary button: `#1a1a2e` (dark navy), white text
- Secondary button: transparent, border `#cccccc`
- Font: system-ui, sans-serif
- Border radius: `8px`
- Max width: `480px` for modals, full-width for banners

If org CSS or theme is provided, use those values instead. Embed the stylesheet inline in `<style>`.

---

## Rich & Creative Guides

Users may request guides that go beyond standard modal/tooltip layouts. **Never refuse or water down a
creative request** — embrace it and build it well. Guides are just HTML; anything that can be built in
a browser can be built in a guide.

Examples of unorthodox but totally valid requests:

- **Tabbed layouts** — multiple content tabs within a single guide step
- **Large centered CTAs** — oversized hero-style buttons as the main interaction
- **Text areas / input fields** — free-text feedback, name entry, or in-guide configuration
- **Checklists** — interactive checkbox lists users tick off before proceeding
- **Image carousels** — swipeable or clickable image sequences within a step
- **Video embeds** — inline Vimeo or YouTube video with play controls
- **Custom progress indicators** — rings, animated bars, or step dots instead of "Step X of Y"
- **Split layouts** — image on the left, copy on the right (or vice versa)
- **Icon grids** — visual feature menus or path selectors the user picks from
- **Rating scales / sliders** — NPS-style or satisfaction sliders
- **Countdown timers** — urgency elements for time-sensitive promotions
- **Accordion sections** — expandable FAQ or detail sections within a guide
- **Confetti / celebration animations** — for onboarding completion or milestone moments
- **Anything else the user describes** — if it can be built in HTML/CSS/JS, build it

### Rules for rich guides
- Use semantic HTML — `<input>`, `<textarea>`, `<select>`, `<ul>`, `<canvas>`, `<details>`, etc. as needed.
- All interactivity lives in the same `<script>` block. No external dependencies unless the user asks for them.
- Maintain copy and button text guidelines even in rich layouts.
- If a creative request conflicts with a guide type rule (e.g. multi-step Announcement), briefly note it
  and suggest a path forward — but if the user wants to break convention anyway, go with it without friction.
- Match the visual ambition of the request: a polished checklist, not a bolted-on afterthought.
