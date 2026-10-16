---
name: fiftyone-app-playwright
description: >
  Use when driving the FiftyOne App via the Playwright MCP — plugin/operator verification,
  demo or screencast recording, or any end-to-end UI automation against `fo.launch_app(...)`.
  Covers the critical "do not navigate after reload_dataset" crash, launcher patterns
  (remote=True, trigger-file IPC), MUI-specific input/dropdown gotchas, sidebar tag filtering,
  `data-cy` selectors, dialog scrolling, session refresh strategies, and cleanup. Trigger on
  mentions of "Playwright + FiftyOne", "automate FiftyOne App", "operator demo", "browser_navigate
  crash", "reload_dataset", or any FiftyOne session that silently dies after a UI action.
compatibility: Requires the Playwright MCP server and a Python environment with `fiftyone` installed (drives a live `fo.launch_app(...)` session).
---

# FiftyOne + Playwright Automation

Session notes for driving the FiftyOne App via the Playwright MCP. The App is a React/MUI SPA backed by a Python `session` over a WebSocket — most pitfalls come from that lifecycle.

---

## 1. The #1 Rule: Never `browser_navigate` or `location.reload()` after an operator that calls `ctx.ops.reload_dataset()`

**Symptom.** The FiftyOne server dies silently (`curl localhost:5151` → HTTP 000; `ps` shows no PID). Dataset on disk is fine — the crash is session-layer. `nohup`/`disown` do NOT prevent it; the trigger is inside FiftyOne's own loop.

**Cause.** The navigate closes the active WebSocket while the remote session is mid-reload; `session.wait()` exits.

**Fixes — ranked by cost.**

### A. `session.refresh()` via trigger-file IPC (best)

Neither `session.refresh()` nor `dataset.reload()` closes the WebSocket. They require a live handle, so replace `session.wait()` with a watcher loop. The bundled [`scripts/launch_app.py`](scripts/launch_app.py) implements exactly this — clone a source dataset, launch `remote=True`, then poll a trigger file and `reload()` + `refresh()` whenever it appears:

```bash
nohup python scripts/launch_app.py \
  --source quickstart --clone verify_clone --port 5151 \
  > /tmp/fo_app.log 2>&1 &
```

The crux of the loop (see the script for the full version, including a guard that refuses to overwrite a *persistent* dataset sharing the clone name):

```python
while True:
    if os.path.exists(TRIGGER):
        os.remove(TRIGGER)
        clone.reload()      # refresh this process's view of MongoDB
        session.refresh()   # push refresh event over existing WebSocket
    time.sleep(0.5)
```

Automation side: `touch /tmp/fo_refresh.trigger` (the script's default `--trigger` path). Refresh lands in ~0.5 s, no UI round-trip. Extend `watch()` in the script for other side effects (mutate samples, create views, etc.). More robust IPC variants: Unix socket / named pipe, Jupyter kernel, or `python -i` with the session kept in a background shell.

### B. "Reload the dataset" built-in operator via the backtick palette (no launcher changes)

```javascript
// 1. Open palette
await page.keyboard.press('`');
// 2. Search (use the React-controlled-input pattern below)
const sb = document.querySelector('input[placeholder="Search operations by name..."]');
setter.call(sb, 'reload the dataset');
sb.dispatchEvent(new Event('input', { bubbles: true }));
// 3. browser_click the "Reload the dataset" result
```

Slower (~2 s) but zero Python-side plumbing. Note: `Reload samples from the dataset` is a **different, weaker** operator — it does NOT refresh the sidebar tag index.

### Why not a sibling-process `dataset.reload()`?

`python -c "fo.load_dataset('clone').reload()"` only refreshes *that process's* copy. The launcher's `session` and the browser WebSocket are untouched. You still need `session.refresh()` on the launcher — back to option A.

---

## 2. Launcher patterns

- **Always `remote=True`.** Prevents a duplicate OS-browser tab on every navigate; launch Playwright and connect to `http://localhost:5151` separately.
- **Non-persistent clones with a pre-delete guard** (the bundled launcher does this). They do NOT auto-delete on ungraceful crash — they linger in MongoDB until the next run's guard removes them.
- Run detached: `nohup python scripts/launch_app.py --source <dataset> --clone <clone-name> --port 5151 > /tmp/fo_app.log 2>&1 &`. (`nohup` doesn't prevent the rule-1 crash; it just insulates from shell signal noise.)
- **Health check between phases:** `curl -s -o /dev/null -w "%{http_code}" localhost:5151` + `ps -p $PID` — detect silent crashes early.
- **Always `remote=True`**: Prevents a duplicate OS-browser tab on every navigate; drive the App through the Playwright MCP browser at `http://localhost:5151`.
- **If no window opens by itself tell the user where to watch**: After the health check passes, report the App URL so the user can open it in their own browser as a passive viewer (watch, don't click, while automation is running). Whether the Playwright MCP browser itself is visible is fixed at MCP-server startup (`@playwright/mcp` is headed unless started with `--headless`, default configuration is for 'headed' mode) — the skill works either way; don't attempt to change it mid-session.

---

## 3. MUI / React gotchas

### React-controlled inputs

`input.value = "foo"` does **not** update React state. The UI shows it briefly then reverts; `dynamic=True` forms won't re-evaluate. Use the native prototype setter:

```javascript
const setter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'value'
).set;
setter.call(inputEl, newValue);
inputEl.dispatchEvent(new Event('input', { bubbles: true }));
```

Applies to every text / number / textbox field in operator forms.

### MUI dropdowns (combobox, not `<select>`)

FiftyOne uses `<div role="combobox">`. `browser_select_option` fails with "Element is not a `<select>`". Options only exist in the DOM while the listbox is open.

```
1. browser_click on the combobox (ref from a FRESH snapshot)
2. Wait ~1s for the listbox to mount
3. browser_evaluate:
   Array.from(document.querySelectorAll('[role="option"]'))
     .find(o => o.textContent.includes('Target label'))
     .click()
```

Use real `browser_click` (not a synthesized `.click()`) to OPEN the popover — MUI's state machine doesn't always accept synthesized events for that.

### Synthesized clicks

Most elements respond to `.click()`. For **SVG icons, MUI chip close buttons, some option rows**, dispatch a real MouseEvent:

```javascript
el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
// Or for chips / drag handles: mousedown → mouseup → click
```

### Scrolling inside MUI dialogs

The dialog's outer container doesn't scroll — an inner div does, and `scrollIntoView()` on children is a no-op. Walk up to the scrollable ancestor and set `scrollTop`:

```javascript
() => {
  const target = document.querySelector('img[src*="/media?filepath"]');
  let el = target.parentElement;
  while (el) {
    const s = getComputedStyle(el);
    if ((s.overflowY === 'auto' || s.overflowY === 'scroll')
        && el.scrollHeight > el.clientHeight) {
      const t = target.getBoundingClientRect();
      const e = el.getBoundingClientRect();
      el.scrollTop += t.top - e.top - 60;  // 60px top margin
      return 'scrolled';
    }
    el = el.parentElement;
  }
}
```

---

## 4. Finding elements

### Prefer `data-cy` attributes

FiftyOne ships extensive `data-cy` hooks for its own Cypress tests — stable across versions.

| `data-cy` | Element |
|---|---|
| `sidebar-field-container-tags` | "sample tags" sidebar row |
| `sidebar-field-arrow-enabled-tags` | Expand caret on that row |
| `checkbox-tags` | Group visibility toggle (NOT a filter) |
| `categorical-filter-tags` | Expanded filter area |
| `selector-sidebar-search-tags` | "+ filter by sample tag" input |
| `flashlight-section` | Main grid renderer |
| `looker` | Each sample card in the grid |

Grep the installed FiftyOne app bundle for more — locate it with `python -c "import os, fiftyone; print(os.path.join(os.path.dirname(fiftyone.__file__), 'app'))"`.

### Text-content matching — filter to leaves

Ancestor `<div>`s contain every descendant string. Filter:

```javascript
Array.from(document.querySelectorAll('*'))
  .find(el => el.textContent.trim() === 'reviewed' && el.children.length === 0)
```

---

## 5. Sidebar tag filtering (non-obvious UX)

To filter the grid by a sample-tag value:

1. Expand "sample tags" via the **caret** (`sidebar-field-arrow-enabled-tags`) — NOT the checkbox (that toggles the whole group).
2. Click the filter input (`selector-sidebar-search-tags`, placeholder "+ filter by sample tag") to open its autocomplete.
3. Click the desired tag row. It becomes a chip; grid filters; click the chip again to clear.

Tag rows are a dynamic autocomplete — not pre-rendered checkboxes.

---

## 6. Stale UI state after an operator mutation

After an Execute that adds samples/tags: the grid count lags and the sidebar tag index is stale. Fix with the `reload_dataset` built-in (rule 1). `reload_samples` is NOT enough — it doesn't refresh the tag index.

---

## 7. Modal viewer navigation

- Click the "Click to expand" ref on a card (real `browser_click`, not a synthesized click on the canvas — that tends not to open the modal).
- `ArrowRight` / `ArrowLeft` cycle the view; `Escape` closes. URL gets `?id=<sample_id>`.

---

## 8. Pacing

- 1–2 s wait after any dialog closes (state-sync debounce).
- ~300–500 ms after input on `dynamic=True` forms before checking for Warnings/Notices.
- 1–2 s between `ArrowRight` presses for recording-grade pacing.

---

## 9. Recording tips

- **Split long demos at crash-prone boundaries.** Record pre-Execute and post-Done clips separately; splice in editor — cheaper than fighting session lifecycle.
- Use the **same operator params** across takes so clips stitch. Unseeded RNG varies per-sample but overall style stays consistent at matched intensities.
- Pre-configure deterministic state (clone, saved views, defaults) in the launcher so on-camera time is all creative action.
- Viewport: `browser_resize(width=2560, height=1440)` **before** `browser_navigate` — default 1440×900 is coarse on Retina.

---

## 10. Cleanup (run between attempts)

```bash
# Kill stale launcher (match the script you launched)
pgrep -f launch_app.py | xargs -r kill; sleep 1
# Drop the non-persistent clone (no-op if already gone). $CLONE = your clone name.
python -c "import sys, fiftyone as fo; fo.dataset_exists(sys.argv[1]) and fo.delete_dataset(sys.argv[1])" "$CLONE"
# Remove ONLY recent orphan output files this run produced — NEVER a broad name glob alone.
# $OUTPUT_GLOB  = a pattern unique to YOUR outputs (e.g. "*_processed_*").
# $PREVIEW_FILE = any sidecar preview the operator wrote (e.g. ".fo_preview.jpg").
find "$MEDIA_DIR" -name "$OUTPUT_GLOB" -type f -mmin -30 -delete
find "$MEDIA_DIR" -name "$PREVIEW_FILE" -mmin -30 -delete
# Playwright snapshot scratch files
rm -f ./*-snap.md ./snap-*.md ./target-*.md ./sv-*.md 2>/dev/null
```

**Cleanup safety:** a bare `find -name "$OUTPUT_GLOB"` will match files from unrelated sessions you shouldn't touch. Always filter by `-mmin` or a session-specific prefix.

---

## Pre-flight checklist

- [ ] Launcher uses `remote=True` + trigger-file watcher (or `session.wait()` if rule 1 is acceptable)
- [ ] Clone is non-persistent, deterministic name, pre-delete guard
- [ ] Deterministic saved views / tags created by the launcher, not at demo time
- [ ] Viewport ≥ 2560×1440 before first navigate
- [ ] Never `browser_navigate` / `location.reload()` after an operator Execute
- [ ] Post-Execute refresh via `touch <trigger-file>` OR `reload_dataset` via backtick palette
- [ ] `data-cy` selectors first; leaf-text match as fallback
- [ ] MUI dropdowns: real click to open, JS click on `[role="option"]` to select
- [ ] React inputs: prototype setter + `input` event
- [ ] Dialog scrolling: walk to scrollable ancestor, set `scrollTop`
- [ ] Cleanup script scoped by `-mmin` / prefix, never bare name globs
- [ ] Health check (`curl` + `ps`) between phases
