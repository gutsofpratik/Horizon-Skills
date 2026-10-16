---
name: discover
description: Finds companies matching criteria (industry, size, location, technologies), estimates how many contacts exist across them, and manages saved searches. Use when the user wants to find companies, build a target-account list, or size a prospecting batch before spending credits. Browsing is free.
user-invocable: true
argument-hint: fintech startups in France with 50-200 employees
---

# Discover

Find companies matching any criteria and size how many contacts they hold — all free, no credits consumed. To turn companies into named, verified contacts you then use Domain Search (which consumes credits); for the full "find people by role" pipeline, use the **prospecting** skill.

## Examples

- `/hunter:discover fintech startups in France`
- `/hunter:discover SaaS companies using Salesforce`
- `"Find healthcare companies in Germany with 100+ employees"`
- `"How many contacts could I get across these fintech companies?"`
- `"Series B startups in Europe"`
- `"Save this search as 'French fintech'"`
- `"Run my saved search"`

## Steps

1. **Find companies.** Pass the user's query directly to `Find-Companies` as the `query` parameter — it accepts natural language and handles parsing.

2. **Present the results:**

```
# Discover: Fintech Startups in France

**Found:** 43 companies | **Showing:** 10

| Company | Domain | Industry | Size | Location |
|---------|--------|----------|------|----------|
| Qonto | qonto.com | Fintech | 150 | Paris, FR |
| Pennylane | pennylane.com | Fintech | 120 | Paris, FR |
| Swan | swan.io | Fintech | 95 | Paris, FR |
| ... | ... | ... | ... | ... |

## Next Actions
1. Narrow or refine the criteria to surface different results (Find-Companies / Find-People have no offset paging)
2. Find the actual contacts at one of these (Domain-Search — consumes credits)
3. Estimate how many contacts these companies hold, free (see "Sizing a batch" below)
4. Save companies to a list (company-lists skill)
5. Run the full people pipeline on these (prospecting skill)
6. Rerun one of your saved searches (List-Saved-Searches)
```

3. **If results are too broad** (hundreds of companies), suggest narrowing: "That's a broad search. Try adding filters like industry, size, location, or technology."

4. **If zero results,** suggest loosening criteria: "No companies matched. Try broadening — for example, widen the location or employee range."

5. **Remind users this is free:** "Discovering companies is free — refine as many times as you'd like. You only spend credits when you pull the actual contacts with Domain Search."

## Finding people by role

`Find-People` does **not** return individual people — it reports, for each matching company, how many email addresses Hunter's index holds (`emails_count.personal` for named people, `emails_count.generic` for role addresses like info@). Use it to **size a batch**, not to list contacts.

- **"How many contacts could I reach across these companies?"** → call `Find-People`. To size a specific selection, pass the exact `domains` of the displayed/selected companies — not the original `query`, which re-counts *every* company matching the search and overstates the budget. Present the totals so the user can budget credits before running Domain Search.
- **"Find the CTOs / VPs of Sales / marketing leaders"** (actual named people by role) → this is **not** a Find-People call. Run `Find-Companies` for the segment, then `Domain-Search` on each company's domain with the role mapped to server-side filters (`seniority: "executive"`, `department: "it"`, etc. — see the domain-search skill). For the end-to-end version, hand off to the **prospecting** skill.

## Saved Searches

- **Reuse an existing saved search** → `List-Saved-Searches` to show the user's saved searches, `Get-Saved-Search` to load one's stored `filters`. Find-Companies/Find-People can't re-apply the stored structured filters verbatim, so the natural-language `query` you reconstruct is approximate — present it to the user to confirm or refine *before* re-running `Find-Companies`, so a complex saved search doesn't return an unexpected scope.
- **Create a saved search** → `Create-Saved-Search` stores a **structured `filters` payload**. After a `Find-Companies` run, pass the `meta.filters` from that response to `Create-Saved-Search` to save the current search. (A bare natural-language string with no filters payload can't be saved this way.)
- **Delete a saved search** → confirm the name first, then `Delete-Saved-Search`.

## Credit Cost

- `Find-Companies`, `Find-People` (counts), and all saved-search operations — **Free** (no credits).
- Pulling the actual contacts (Domain Search) and verifying them consumes credits — confirm before doing it in bulk.

## Success Criteria

At least one company returned matching the user's criteria — with people-by-role requests correctly routed to Domain Search / prospecting rather than to Find-People.
