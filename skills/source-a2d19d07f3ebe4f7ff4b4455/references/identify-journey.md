# Identify subscription and target journey

Run before any mutation on an **existing** journey, and before create when `subId` / `appId` are unknown.

---

## Subscription and application

Resolve **`subId` and `appId` together** before `listOrchestrateJourneys`
name matching or before create. For set/write on an already-identified journey,
`subId` plus the journey or email id is enough.
Application ids are **not unique across subscriptions** — a wrong pair silently retargets every downstream mutation.
Do not guess ids from journey names.

**If the user gave both `subId` and `appId`** — use them.

**If either is missing** — call `listAllApplications` (works without `subId`). Narrow rows using subscription or
application names or ids the user gave.

1. **Zero matching rows** — stop and ask which subscription and application to use (names or ids).
2. **One matching row** — use that row's `subscriptionId` as `subId` and `applicationId` as `appId`.
3. **Two or more matching rows** — stop; list each candidate (`subscriptionId`, `subscriptionName`,
   `applicationId`, `applicationName`) and ask which subscription and application to use. Do not call any
   Orchestrate set/write tool until the user picks one row.

When the user names only a subscription and that subscription has multiple applications, treat the narrowed set
as **two or more** — list apps under that subscription and ask which `applicationId` to use.

---

## Existing journey by URL, id, or name

**If the user pasted an Orchestrate journey URL** — parse from the URL:

- **Journey** — path `.../s/{subscriptionId}/journeys/{journeyId}` (optional query such as `?view=map`). When
  `subscriptionId` is present, use it as `subId`. Call `getOrchestrateJourney` with `journeyId`. Resolve `appId`
  from the response or from the user if you still need it for other calls.
- **Email step (when present)** — query `messageId={campaignId}` on the map URL, or path
  `.../journeys/{journeyId}/messages/{campaignId}`. That value is the step **`messageId`** / **`emailId`** for
  `references/content-email.md`; keep it — do not re-derive through `getOrchestrateJourneySteps` unless it does
  not match any Email step.

**If the user gave a journey id (no URL)** — call `getOrchestrateJourney`. Confirm `name` and `appId` match what
they meant.

**If the user gave a name (no id or URL):**

1. Resolve **`subId` and `appId`** via **Subscription and application** above if either is still unknown. Do
   not pick a journey from a different application.
2. Call `listOrchestrateJourneys` with `subId` (`limit` up to 500; paginate with `offset` if needed).
3. Match by name in the results — there is no server-side name filter — then **keep only rows whose `appId`
   equals the resolved `appId`**. Ignore same-name journeys on other applications in the subscription.
4. **Zero matches** after that filter — for **edit** intent, tell the user and ask for a different name or
   the journey id. For **create** intent, zero matches is expected — return to `references/intake.md`.
5. **One match** — call `getOrchestrateJourney` with that `id`. Confirm `name` and `appId` match what they
   meant.
6. **Two or more matches** — stop; list each candidate (`id`, `name`, `status`, `appId`) and ask which
   journey to edit. Do not call any set/write tool until the user picks one.

Never mutate using a display name alone — you need a single `journeyId` first.
