---
name: manage-leads
description: Manages individual leads in Hunter — create, look up, update, or delete leads, tag them, and set custom attributes. Use when the user wants to add or edit a lead, tag contacts, organize leads with custom fields, or clean up their lead database.
user-invocable: true
argument-hint: Add jane@stripe.com as a lead and tag her "priority"
---

# Manage Leads

Create, update, tag, and organize the leads in a Hunter account.

## Examples

- `/hunter:manage-leads Add jane@stripe.com as a lead and tag her "priority"`
- `"Update John's position to VP of Sales"`
- `"Tag all these contacts as 'Q2 campaign'"`
- `"Add a custom attribute 'deal size' to my leads"`
- `"Delete the leads I imported by mistake"`
- `"Do I already have marc@acme.com as a lead?"`

## Workflow

### Create or update leads

- **Add a lead** → `Create-Lead-If-Missing` to add without touching an existing lead's data, or `Create-Or-Update-Lead` when the user intends to update in place (it overwrites existing fields). `Create-Lead` forces a new record.
- **Check first** → `Lead-Exists` to test whether an email is already a lead; `Get-Lead` / `List-Leads` to read.
- **Edit** → `Update-Lead` with the lead ID and the fields to change.

Include all available built-in fields when creating (`email`, `first_name`, `last_name`, `position`, `company`, `linkedin_url`, `phone_number`). Custom-attribute *values* can't be set through the lead tools (see Custom attributes below) — only the built-in fields are accepted.

### Tags

- Manage the tag vocabulary → `List-Lead-Tags`, `Create-Lead-Tag`, `Update-Lead-Tag`, `Delete-Lead-Tag`.
- Apply/remove on a lead → `Add-Tag-To-Lead`, `Remove-Tag-From-Lead`.
- If the user references a tag that doesn't exist yet, offer to create it before applying.

### Custom attributes

- Manage the definitions: `List-Custom-Attributes` to see them, `Create-Custom-Attribute` to add one (a **label** only — there is no type parameter), and `Get-Custom-Attribute` / `Update-Custom-Attribute` / `Delete-Custom-Attribute` to manage.
- Note: the lead write tools expose only the built-in fields (email, name, position, company, …). There is currently **no API to set a custom attribute's value on a lead**, so this skill manages attribute *definitions*, not their per-lead values.

### Present a summary

```
# Lead Updated: Jane Smith (jane@stripe.com)

| Field | Value |
|-------|-------|
| **Position** | VP of Engineering |
| **Company** | Stripe |
| **Tags** | priority, Q2 campaign |

## Next Actions
1. Add her to a leads list (lead-lists skill)
2. Add her to an outreach sequence (build-sequences skill)
3. Push to your CRM (push-to-crm skill)
```

## Guardrails

Confirm before any destructive action — state the operation, the affected count, and the target, then wait for an explicit "yes":

- `Delete-Lead` — name the lead being deleted.
- `Bulk-Delete-Leads` — takes explicit `lead_ids` or a `leads_list_id` (not free-form criteria), max 100 ids per call: resolve the target ids first (e.g. via `List-Leads`), then confirm "This permanently deletes [N] leads." and batch in groups of 100.
- `Bulk-Move-Leads` — echo how many leads and the destination list; both source and destination must be **static** lists (dynamic/saved lists are rejected).
- `Delete-Lead-Tag`, `Delete-Custom-Attribute` — these affect every lead using them; say so.
- `Update-Lead-Tag`, `Update-Custom-Attribute` — renaming a tag or attribute label changes it across every lead that uses it and can't be undone; confirm before a global rename.

Never run a delete or bulk operation without explicit confirmation.

## Credit Cost

Free — creating, updating, tagging, and organizing leads does not consume credits. (Finding or verifying the underlying emails does.)

## Important Notes

- `Create-Lead-If-Missing` adds without overwriting; `Create-Or-Update-Lead` updates in place (overwrites existing fields). Both avoid duplicates — pick by whether you want to overwrite.
- Deleting a tag or custom attribute affects all leads that use it — confirm scope first.
- `List-Leads` returns up to 100 leads per page — use `offset` to paginate through large accounts.
