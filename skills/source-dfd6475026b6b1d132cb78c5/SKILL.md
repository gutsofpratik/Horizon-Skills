---
name: lead-lists
description: Creates and organizes Hunter leads lists — build a list from contacts or a search, populate it, merge lists, favorite them, and group them into folders. Use when the user wants to build a lead list, save search results to Hunter, organize contacts into lists, or tidy up their lists and folders.
user-invocable: true
argument-hint: Create a list of marketing leads from SaaS companies
---

# Lead Lists

Create leads lists, populate them with contacts, and organize them into folders.

## Examples

- `/hunter:lead-lists Create a list of marketing leads from SaaS companies`
- `"Save these contacts to a new list called Q2 Outreach"`
- `"Build a list from the domain search results"`
- `"Merge my two fintech lists"`
- `"Favorite my Q2 Outreach list"`

## Workflow

### Step 1: Determine the source

- **From a previous search** — use contacts already found via Domain Search. (Discover returns companies/counts, not contacts with emails, so route Discover results through Domain Search first to get saveable contacts.)
- **From specific emails/contacts** — the user provides addresses directly.
- **From a new search** — run the discover / domain-search skills first, then save results.

### Step 2: Create or pick the list

To reuse an existing list, `List-Leads-Lists` to browse and `Get-Leads-List` to read one. For a new list, call `Create-Leads-List` with a descriptive name. If the user gives none, suggest one from context (e.g., "Fintech CTOs - France - 2026-07-16").

Present the deep-link: "List created: https://hunter.io/leads?leads_list_id={id}"

### Step 3: Add leads

For each contact, call `Create-Lead-If-Missing` with the contact's data and the new `leads_list_id` — it adds new leads but never overwrites an existing lead's fields, so sparse search data can't clobber contacts the user already maintains. Note: for an email that is **already** a lead, `Create-Lead-If-Missing` returns the existing record unchanged and does **not** add it to the new list — report those as already-existing / not added rather than counting them as added. (`Create-Or-Update-Lead` *would* add them to the list but overwrites their fields; use it only when the user explicitly wants that.) `Lead-Exists` checks first if unsure. Include all available fields (`email`, `first_name`, `last_name`, `position`, `company`, `linkedin_url`). Report progress ("Adding lead 5 of 20…").

### Step 4: Organize

- **Merge** two lists → `Merge-Leads-Lists` (destructive — it moves all leads to the destination and permanently deletes the source list; confirm first, see Guardrails). Both lists must be **static** and the source non-empty — dynamic/saved lists are rejected.
- **Favorite / unfavorite** → `Favorite-Leads-List` / `Unfavorite-Leads-List`.
- **Folders** → `List-Leads-List-Folders`, `Create-Leads-List-Folder`, `Update-Leads-List-Folder` (create and rename folders). Note: the API has no way to move an existing list into a folder — that's a Hunter-dashboard action.
- **Rename** a list → `Update-Leads-List` (accepts the list `id` and a new `name` only).

### Step 5: Present summary

```
# List Created: [List Name]

**Leads added:** [count] | **Duplicates skipped:** [count]

View in Hunter: https://hunter.io/leads?leads_list_id={id}

## Next Steps
1. Add more leads to this list
2. Add these leads to a sequence (build-sequences skill)
3. Push the list to your CRM (push-to-crm skill)
4. Search for more contacts (discover / domain-search skills)
```

## Guardrails

Confirm before destructive actions — state what will be affected, then wait for a "yes":

- `Delete-Leads-List` — "This deletes the '[name]' list (the leads themselves stay in your account); if it's a static list that a dynamic/saved list depends on, those dependent lists are deleted too. Confirm?"
- `Merge-Leads-Lists` — moving leads permanently deletes the source list and can't be undone: "This merges '[source]' into '[dest]' and deletes '[source]'. Confirm?"
- `Delete-Leads-List-Folder` — clarify whether lists inside move out or are affected, and confirm.

## Credit Cost

Free — `Create-Leads-List`, `Create-Lead-If-Missing`, merges, and folder operations do not consume credits. Only the initial search (Domain Search, Email Finder) uses credits if leads come from a new search.

## Important Notes

- Use `Create-Lead-If-Missing` when saving search results so you never overwrite an existing lead; reserve `Create-Or-Update-Lead` for when the user intends to update existing leads.
- Lists can be merged later with `Merge-Leads-Lists` — but the merge deletes the source list, so confirm first.
- `List-Leads` returns up to 100 leads per page — use `offset` to paginate through larger lists.
