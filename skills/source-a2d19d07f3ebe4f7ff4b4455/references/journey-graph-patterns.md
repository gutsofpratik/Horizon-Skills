# Journey graph patterns

**Authoritative:** `templateJson` JSON Schema on `createOrchestrateJourneyFromJson` (fields, enums, wait
days, conditional split topology).

**This file:** topology only — how steps connect. Adjust names, ids, and wait days to match the user.
Audience, segments, schedule, and email content live in other reference files — not here.

---

## Use case → pattern

| User intent (plain language) | Pattern |
|------------------------------|---------|
| Single email, built-in graph (marketing) | Built-in template — see `references/intake.md` for `createOrchestrateJourneyFromTemplate` |
| Welcome or onboarding sequence (2 emails) | Pattern 1 |
| Re-engage inactive users, retention emails, win-back | Pattern 2 |
| Different follow-ups by behavior (after intro email) | Pattern 3 |

All custom graphs use `createOrchestrateJourneyFromJson` — see `references/intake.md`.

---

## Pattern 1 — Two-email journey (welcome / onboarding)

```
Start -> [Welcome email] -> [Getting started tips] -> Exit
         wait: 3 days        wait: 1 day
```

Linear sequence. Wait before the gap goes on the **first** email (see schema for `durationInDays`).

---

## Pattern 2 — Three-email re-engagement / retention journey

Default topology when the user asks for a **retention journey**, **re-engagement**, or **win-back** emails
for inactive visitors.

```
Start -> [We miss you] -> [Here's what's new] -> [Last chance] -> Exit
         wait: 2 days      wait: 5 days         wait: 1 day
```

Linear sequence. Tune wait days and step names to match the user's request.

---

## Pattern 3 — Conditional split

Use when one intro email should branch to different follow-ups (e.g. engaged vs not engaged).

```
Start -> [Introduction] -> (conditional split) --Yes--> [Power-user tips] -> Exit
         wait: 1 day              |  (immediate)
                                  --No--> [Getting started guide] -> Exit
```

Split has **no wait**. Split **topology** is set at create; the Yes/No **condition** is configured in
Orchestrate UI — see create tool descriptions and **Capability boundary** in `SKILL.md`.
