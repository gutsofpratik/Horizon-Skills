# Handoff and activation

Use when the user wants to **go live**, **activate**, or ask what is left before sending.

Run `references/identify-journey.md` first when the journey was not just created in this conversation.

Activation and capability boundaries — see **Capability boundary** in `SKILL.md`.

---

## Pre-activation checklist (user-driven)

1. Revisit what the user asked for — do not audit items they did not ask about.
2. For each item they care about:
   - Confirm what you can via get tools and prior write responses in this conversation.
   - Route gaps to `references/configuration.md` or `references/content-email.md` when an MCP tool covers them.
   - For email content and split conditions — not readable via get tools; if they care, ask them to verify in
     Orchestrate UI.
   - If no MCP tool covers the item — say so; do not guess about the UI.
3. Close with what you confirmed via MCP, what you could not verify (and why), and that activation is their
   step in Orchestrate UI.

---

## Customer KB (optional pointers)

- [Create and customize a journey](https://support.pendo.io/hc/en-us/articles/28029722249115-Create-and-customize-a-journey) — goals, segments, throttling, templates
- [Monitor journey results](https://support.pendo.io/hc/en-us/articles/28064439051547-Monitor-journey-results) — after activation
