---
name: company-lists
description: Saves companies and organizes them into Hunter company lists — save a company, add/remove companies to lists, create and manage lists and folders, and bulk copy/move/delete companies. Use when the user wants to save companies from a search, build a target-account list, or organize companies into lists and folders.
user-invocable: true
argument-hint: Save these fintech companies to a "Target Accounts" list
---

# Company Lists

Save companies and organize them into lists and folders — the account-level counterpart to lead-lists.

## Examples

- `/hunter:company-lists Save these fintech companies to a "Target Accounts" list`
- `"Save stripe.com to my prospects"`
- `"Add these Discover results to a new list"`
- `"Move the EU accounts into a Europe folder"`
- `"Copy these companies to my Q3 list"`

## Workflow

### Step 1: Save companies

- Save a single company → `Save-Company` (from a domain or a Discover / enrichment result).
- Companies typically come from the discover skill (`Find-Companies`) or company-enrichment.

### Step 2: Create or pick a list

- New list → `Create-Company-List` with a descriptive name.
- Existing → `List-Company-Lists` to browse, then use its ID.

### Step 3: Populate

- Add saved companies → `Add-Company-To-List`.
- Remove → `Remove-Company-From-List`.
- Move / copy in bulk across lists → `Bulk-Move-Companies` / `Bulk-Copy-Companies`.
- Note: list membership and bulk **move**/**delete** require static lists; bulk **copy** requires only the *destination* static (its source may be dynamic). Dynamic (auto-filter) lists can't be the target of these ops — pick a static target when the user chooses from `List-Company-Lists`.

### Step 4: Organize

- **Favorite / unfavorite** → `Favorite-Company-List` / `Unfavorite-Company-List`.
- **Folders** → `List-Company-List-Folders`, `Create-Company-List-Folder` (requires both a `name` **and** a `color` — ask the user or pick one; unlike leads-list folders, Hunter won't default it), `Update-Company-List-Folder` (renames/recolors a folder). To **file a list into a folder**, call `Update-Company-List` with the target `company_list_folder_id` — the folder tool only edits folder metadata, not membership.
- **Rename** → `Update-Company-List`; **read** → `Get-Company-List`.

### Step 5: Present summary

```
# Company List: Target Accounts

**Companies:** [count]

## Next Actions
1. Find contacts at these companies (domain-search skill)
2. Save decision-makers as leads (manage-leads / lead-lists skills)
3. Run a full prospecting pass on the list (prospecting skill)
```

## Guardrails

Confirm before destructive, irreversible, or bulk actions — state the operation, the count, and the target, then wait for a "yes" (adding a single company to a list is additive and needs no gate):

- `Delete-Company-List` — deleting a static list can also delete companies left orphaned by it (and any dependent dynamic lists): "This deletes the '[name]' list; companies only in this list may be removed too. Confirm?"
- `Bulk-Delete-Companies` — "This permanently deletes [N] companies. Confirm?"
- `Bulk-Move-Companies` — echo how many companies and the destination.
- `Bulk-Copy-Companies` — the tool is confirmation-gated: the first call reports the affected count without copying, so echo that count and destination, then re-run confirmed.
- `Delete-Company-List-Folder` — clarify what happens to the lists inside, and confirm.

## Credit Cost

Free — saving companies and managing lists and folders does not consume credits.

## Important Notes

- Company lists organize companies (accounts); use the lead-lists skill for contacts.
- Bulk copy/move act on many companies at once — confirm the count before running.
