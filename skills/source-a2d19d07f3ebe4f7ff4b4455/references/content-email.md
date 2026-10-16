# Email content (Orchestrate journeys)

**Validation:** `updateOrchestrateEmailContent` tool description, parameter schema, and error messages.
**This file:** workflow, copy craft, and worked example — not the full validation contract.

Use when the user asks to **write, draft, add, or update** email content. Run
`references/identify-journey.md` first when editing an existing journey.

---

## Workflow

1. Identify journey if needed — `references/identify-journey.md`.
2. `getOrchestrateJourneySteps` — list Email steps; each step's `messageId` is the `emailId` on
   `updateOrchestrateEmailContent`.
3. **Before drafting or saving** — for each email step you will update, call `getOrchestrateEmail` with that
   `messageId` (for `emailType` and status). Follow `updateOrchestrateEmailContent`'s `WithWorkflow` before calling
   the write tool.
4. Draft HTML; iterate with the user; call `updateOrchestrateEmailContent` per approved email. After a successful
   save, tell the user what the tool returned (`resultSummary`, `emailUrl`); do not claim the email was previewed
   in the UI unless the user did.

**Multi-email journeys:** one save per email, in journey order; label drafts by step **name**.

**Conditional splits:** each branch email has its own `messageId`.

---

## Generating HTML (craft, not enforcement)

Match Orchestrate **Edit email** intent — table-based layout, inline styles, simple structure. The save
path sanitizes HTML the same way as the UI; unsafe tags and `javascript:` URLs are stripped automatically.

Before drafting, skim
[Create and send an HTML email](https://support.pendo.io/hc/en-us/articles/52945752520731-Create-and-send-an-HTML-email):
table layout, no scripts, visible unsubscribe link for marketing.

**Personalization tokens** — use **single-brace** only (same as typing in Edit email):
`{visitor.agent.field/}`, `{field|default/}`. Call `visitorMetadataSchema` / `accountMetadataSchema`
before using a field — do not invent field paths in examples or drafts.

**Double-brace `{{...}}` in HTML** — only `{{ UnsubscribeURI }}` is valid. Do not author other
`{{...}}` tokens (e.g. `{{visitor.name}}`, `{{unsubscribe}}`); use single-brace for personalization.
Read the tool error and parameter schema on failure.

**Marketing unsubscribe** — required for marketing emails and when `emailType` is unset (same default as
`updateOrchestrateEmailContent`):

- If you already know `emailType` from create, use that.
- Otherwise use `emailType` from `getOrchestrateEmail` (step 3 above).
- **`transactional`** — omit the unsubscribe block below.
- **`marketing`**, or **`emailType` absent or unknown** — include `{{ UnsubscribeURI }}` in the draft (unset is
  treated as marketing at save).

- Use a **visible** link — do not hide the unsubscribe with CSS.
- Wrap the token in an anchor. The `href` must contain the **exact** platform token — copy it literally:

```html
<a href="{{ UnsubscribeURI }}">Unsubscribe</a>
```

- **`{{ UnsubscribeURI }}` is a safeword** — do not rename, rephrase, or encode it (no `UnsubscribeUrl`,
  `{{unsubscribe}}`, URL-encoding the braces, or extra characters inside the token). Pendo replaces this
  exact string at send time. You may change the visible link text if it still clearly means unsubscribe
  (e.g. `Unsubscribe`, `Opt out`) — do not use labels like `Manage preferences` that imply a preference center;
  this link only unsubscribes.
- Keep the `href` clean — no stray characters merged into the token (e.g. `{{ UnsubscribeURI }}#`). A broken
  `href` may still save but fail on test send.

**Outlook-friendly CTAs** — use table-based buttons. Put **button text color on an inner `<span>`**, not on the
`<a>` — Outlook often ignores `color` on block-level anchors.

**Lists** — prefer manual bullets (`•` or a styled table row) over `<ul>` / `<li>` for broader client support.

**No MSO / VML** — Orchestrate does not preserve pasted Outlook conditional comments or VML. HTML comments are
stripped on save. Do not rely on `<!--[if mso]>` blocks or VML round buttons; use simple table layouts instead.
Rounded button corners may not render in Outlook desktop — that is expected.

**Do not include:** polls, guide building blocks, or interactive widgets.

---

## Worked example — minimal email HTML

Starting template for a welcome or onboarding step. Layout and CTA patterns apply to both email types.
Example below is **marketing** (includes the unsub block from above); omit the last `<p>` for transactional.

Uses plain greeting text — add single-brace personalization only after `visitorMetadataSchema` confirms a
field exists.

```html
<!DOCTYPE html>
<html>
<head>
  <title>Welcome</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4;">
  <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f4f4;">
    <tr>
      <td align="center" style="padding: 24px 16px;">
        <table role="presentation" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff;">
          <tr>
            <td style="padding: 32px 24px; font-family: Arial, Helvetica, sans-serif; font-size: 16px; line-height: 24px; color: #333333;">
              <p style="margin: 0 0 16px;">Hi there,</p>
              <p style="margin: 0 0 16px;">Thanks for signing up. Here is one quick win to try in your first week.</p>
              <p style="margin: 0 0 24px;">
                <a href="https://app.example.com/getting-started" target="_blank" style="display: inline-block; padding: 12px 24px; background-color: #128297; text-decoration: none; border-radius: 4px;">
                  <span style="color: #ffffff;">Get started</span>
                </a>
              </p>
              <p style="margin: 0; font-size: 14px; color: #666666;">
                <a href="{{ UnsubscribeURI }}" style="color: #666666; text-decoration: underline;">Unsubscribe</a>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

**Save via MCP** (after `getOrchestrateJourneySteps`): call `updateOrchestrateEmailContent` using the tool's
input schema — do not guess parameter names or shape. **`emailId` is the step's `messageId`** (not
`journeyId` or `stepId`).

---

## Copy and tone

- Match the user's brand voice when described; otherwise clear, professional lifecycle tone.
- Lead with value; one primary CTA per email.
- Keep subject lines out of the HTML body.
- On revision, regenerate full HTML for affected emails and re-call the tool — do not ask the user to patch fragments.

On save failure, read the **tool error message** first, then adjust and retry once.
