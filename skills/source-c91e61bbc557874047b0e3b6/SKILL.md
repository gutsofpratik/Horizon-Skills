---
name: push-to-crm
description: Pushes Hunter leads to a connected CRM (e.g. HubSpot, Salesforce, Pipedrive). Use when the user wants to sync leads to their CRM, export contacts to HubSpot/Salesforce, or send a list to their connected sales tool.
user-invocable: true
argument-hint: Push my Q2 leads to HubSpot
---

# Push to CRM

Send leads from Hunter to a connected CRM.

## Examples

- `/hunter:push-to-crm Push my Q2 leads to HubSpot`
- `"Send these contacts to Salesforce"`
- `"Sync the fintech list to my CRM"`
- `"Which CRMs do I have connected?"`

## Workflow

### Step 1: Identify the target CRM

- `List-Connected-Apps` to show the user's connected integrations; `Get-Connected-App` for details on one.
- If nothing is connected, tell the user to connect a CRM in Hunter first (Settings → Integrations) — this skill can't create the connection.

### Step 2: Identify the leads

Determine which leads to push. `Push-Leads-To-CRM` accepts only saved `lead_ids` or a `leads_list_id` — so if the "current selection" is unsaved Domain Search / finder results, first save them as leads (with the user's OK, via `Create-Lead-If-Missing`) and push those IDs. You can't push unsaved rows. `lead_ids` is capped at 100: for larger selections, save them to a leads list and push the `leads_list_id` instead (or batch the IDs in groups of 100 after confirming the total). Note: `Create-Lead-If-Missing` leaves an already-existing lead out of the new list, so pushing that new `leads_list_id` would skip those contacts — collect the full set of `lead_ids` (existing + new, via `Lead-Exists` / `List-Leads`) and push those IDs. Don't reach for `Create-Or-Update-Lead` just to force list membership — it overwrites the existing lead's fields; use it only if the user explicitly wants to update them.

### Step 3: Confirm, then push

State the target app and how many records will be sent, and wait for explicit confirmation, because this writes data into an external system:

> "This will push 40 leads to **HubSpot**. Confirm?"

Only after a "yes", call `Push-Leads-To-CRM` with the leads and the target app.

### Step 4: Report the queued push

`Push-Leads-To-CRM` is asynchronous — it returns a `queued` status and the lead count, not per-record results. Report that; do not invent created/updated/skipped numbers.

```
# Push queued → HubSpot

**Leads queued:** 40 | **Status:** queued

The sync runs in the background — check HubSpot in a few moments to confirm the records.

## Next Actions
1. Push another list
2. Review the leads in HubSpot shortly
```

## Guardrails

`Push-Leads-To-CRM` commits data to an external system — always confirm the **target app** and the **record count** before executing. Never push silently or by default. The call only queues the sync (it returns `queued` + count, not per-record results), so report it as queued and point the user to the CRM to verify the outcome.

## Credit Cost

Free — pushing leads to a connected CRM does not consume credits.

## Important Notes

- The CRM connection must already exist in Hunter — this skill uses it, it doesn't create it.
- Confirm the destination every time; pushing to the wrong CRM is hard to undo.
