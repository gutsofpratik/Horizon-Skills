# Troubleshooting

Proactive guardrails and recovery when something fails, ids are wrong, or behavior does not match
expectations.

---

## Agent behavior — avoid these (not API rules)

- Creating on the first message without intake (`references/intake.md`).
- Mutating an existing journey without `references/identify-journey.md` (duplicate names, wrong app).
- Ignoring a tool's `WithWorkflow` (guessing ids, auto-picking first segment/goal match).
- Using `journeyId` or `stepId` as `emailId` (use `messageId` from `getOrchestrateJourneySteps`).
- Reading `emailType` from `getOrchestrateJourneySteps` (use `getOrchestrateEmail` or what you set in
  `templateJson` at create).
- Claiming readiness or email content state — see **Do not infer unobservable state** in `SKILL.md`.
- Referencing `journeyUrl` from get/list — only create/write responses return it on success.
- Hardcoding UI-only capabilities instead of checking the tool list.
- Confusing journey **metrics** with journey **building**.
- Calling a **create** tool when the user meant to edit an existing journey (confirm new vs edit in
  `references/intake.md`).
- Calling **create** again to add steps or change waits on an existing journey — check the MCP tool list for a
  graph-update tool first (see dispatch table in `SKILL.md`).

API validation errors come from the tool — read the error and schema.

---

## Symptom → cause → action

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Create validation error | Invalid `templateJson` graph or fields | Read tool error + `templateJson` JSON Schema; fix and retry once |
| Create timed out or transport error | Outcome unknown — journey may exist | `listOrchestrateJourneys` with pagination; disambiguate by name; do not duplicate create |
| Multiple journeys same name | Skipped identify step | Re-run `references/identify-journey.md`; user picks `journeyId` |
| `field_not_editable` on set | Journey status blocks that field | Read tool description; tell user |
| "Unknown template id" | Used UI template id from `listOrchestrateJourneyTemplates` | Use built-in template create or `createOrchestrateJourneyFromJson` — see create tool descriptions |
| Email content save fails | Validation error from write tool | Read tool error + parameter schema; see `references/content-email.md` |
| User request you cannot fulfill | No MCP tool for that action | Say you have no MCP tool; user verifies in Orchestrate UI or KB |
