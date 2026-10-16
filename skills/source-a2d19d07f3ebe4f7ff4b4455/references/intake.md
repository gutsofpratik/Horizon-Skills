# Intake and create

Use when the user wants a **new** journey.

---

## Confirm new journey vs edit existing

Duplicate journey names are allowed. Resolve **`subId` and `appId` first** when either is missing
(`references/identify-journey.md` — Subscription and application) — `listOrchestrateJourneys` requires `subId`.

Before create, confirm the user wants a **new** journey — not to edit one that already exists.

- **Clear create intent** ("create", "build", "new journey") — proceed to intake. If they also name a journey
  that already exists, call `listOrchestrateJourneys` (with resolved `subId`) and briefly note matches exist;
  confirm they still want a **new** one (do not block create on name alone).
- **Clear edit intent** ("update", "edit", "change my journey") — run `references/identify-journey.md` instead;
  do not call a create tool.
- **Ambiguous** — if they name a journey without create vs edit language, after `subId` / `appId` are resolved,
  call `listOrchestrateJourneys` and ask: edit an existing match, or create a new journey (same name is fine)?

---

## Progressive intake

Work through **two rounds** when Round 1 is not already complete. Ask each round together, wait for answers,
then continue. Do not collapse rounds into one message.

Acknowledge what the user already shared, then ask what is still missing.

### One-shot (Round 1 already complete)

When the user already gave **journey name**, **application**, and **what to build** (Round 1):

One-shot skips **Round 1 and Round 2 questions** only. First run **Confirm new journey vs edit existing**
above (resolve `subId` / `appId`, `listOrchestrateJourneys` when needed, create vs edit) — do not jump
straight to approval.

1. Acknowledge what they shared — do not re-ask Round 1.
2. Briefly note any Round 2 topics they skipped (audience, schedule, goal, email content) and that those can
   wait until after create unless they specified them.
3. **Confirm and proceed** — summarize the create tool and graph you will use, then ask for approval to create.
   Do not invent filler questions to satisfy two rounds.

After they approve (or Round 2 finishes), resolve any remaining `subId` / `appId` gaps via
`references/identify-journey.md`, then create.

### Round 1 — Required

1. **Journey name** — Shown in the Orchestrate UI (e.g. "Q1 onboarding").
2. **Application** — Which Pendo application this journey belongs to.
3. **What to build** — In plain language: how many emails, wait days between them, and any branching.
   Infer the create tool from this — do not ask the user to pick a technical template category.
   For common shapes, see the use-case table in `references/journey-graph-patterns.md`.

### Round 2 — Optional (ask every time; user may skip)

4. **Audience** — Segment name or rules. Can attach after create (`references/configuration.md`).
   For re-engagement journeys, ask how they define inactive visitors (e.g. no login in 30 days).
5. **Schedule** — When should the journey start? (date and time in subscription timezone; required before
   activation — set now or in configuration after create).
6. **Conversion goal** — Page, feature, or track event (if any).
7. **Email content** — Body for email steps (optional now; `references/content-email.md` after create when
   the user wants content).

After Round 2 (or skips), resolve `subId` and `appId` via `references/identify-journey.md` if still unknown,
then create.

---

## Choose the create tool

Pick the tool from **graph shape** (see table). Set `emailType` (marketing or transactional) in each
email node's `messageData` when using `createOrchestrateJourneyFromJson`. The built-in template is one
marketing email step.

| User need | Tool |
|-----------|------|
| One email step, built-in graph (marketing) | `createOrchestrateJourneyFromTemplate` with `templateId` `mcpSingleEmailJourneyTemplate` |
| Multiple emails, wait days, a conditional split, transactional email, or any custom graph | `createOrchestrateJourneyFromJson` with `templateJson` |

**Do not** use ids from `listOrchestrateJourneyTemplates` as create inputs (see
`references/troubleshooting.md`).

For custom graphs: read the **`templateJson` JSON Schema**, then `references/journey-graph-patterns.md` if
the layout is not obvious.

---

## Create and verify

Read the chosen create tool's **input schema** before calling it. Both create tools require `subId`, `appId`, and
`name`; also pass `templateId` (template create) or `templateJson` (custom graph create).

1. Call the create tool with all required parameters.
2. Share `journeyUrl` from the response — create tools return it on success.
3. Call `getOrchestrateJourneySteps` and confirm step names and wait days match what the user asked for.
4. On validation failure, read the tool error and JSON Schema; retry once before asking the user for help.

Then continue to `references/configuration.md` and/or `references/content-email.md` for anything the user
asked for in intake.

---

## Assistant tone (create path)

- Be friendly and concise — explain choices briefly.
- Share the journey link prominently after create (`journeyUrl` in the create response).
- Summarize what was set vs what remains (use the capability boundary rule in `SKILL.md`).
- Do not open with "Here's the journey:" — describe what you built and why.
- Invite changes: segment, timing, extra emails, conditional split structure, or email content.
