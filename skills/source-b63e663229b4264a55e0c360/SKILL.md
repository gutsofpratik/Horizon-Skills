---
name: domain-search
description: Finds all publicly available email addresses and contacts at a company domain. Use when the user asks who works at a company, wants to find contacts at a domain, or needs email addresses for an organization.
user-invocable: true
argument-hint: stripe.com
---

# Domain Search

Find all contacts and email addresses associated with a company domain.

## Examples

- `/hunter:domain-search stripe.com`
- `/hunter:domain-search Notion`
- `"Who works at figma.com?"`
- `"Find me contacts at Salesforce"`
- `"Show me the marketing team at hubspot.com"`
- `"List executives at acme.com"`

## Steps

1. **Parse the input.** Extract the `domain`.
   - "stripe.com" -> use directly
   - "Stripe" or "stripe" -> infer domain as "stripe.com"
   - If unsure about the domain, ask the user to confirm.

   **Free pre-check first (optional).** If the user wants to size how many **contacts/emails** Hunter has for a domain before paying, call `Email-Count` *before* `Domain-Search`. It's free and takes a `domain` plus an optional `personal`/`generic` `type`. It returns email totals only — not company headcount (use company-enrichment for employee counts) — and can't filter the count by role or department (only the paid `Domain-Search` filters by seniority/department).

2. **Call `Domain-Search`** with the `domain`. Use server-side filters when the user specifies criteria:
   - `type`: `personal` or `generic`
   - `seniority`: comma-separated from `junior`, `senior`, `executive`
   - `department`: comma-separated from `executive`, `it`, `finance`, `management`, `sales`, `legal`, `support`, `hr`, `marketing`, `communication`, `education`, `design`, `health`, `operations`, `product`, `research`, `consulting`, `administrative`, `procurement`
   - `required_field`: `full_name`, `position`, or `phone_number` — only return results where this field has a value
   - `limit`: 1-100 (default 10)
   - `offset`: for pagination

   **Mapping user requests to filters:**
   - "marketing team" -> `department: "marketing"`
   - "executives" / "C-suite" / "leadership" -> `seniority: "executive"`
   - "engineering" / "developers" -> `department: "it"`
   - "senior people" -> `seniority: "senior,executive"`
   - No filter specified -> show the top contacts by confidence score

4. **Present the results:**

```
# Contacts at Stripe (stripe.com)

**Found:** 247 contacts | **Showing:** 10

| Name | Position | Email | Confidence |
|------|----------|-------|------------|
| Patrick Collison | CEO | patrick@stripe.com | 97% |
| John Collison | President | john@stripe.com | 95% |
| David Singleton | CTO | david.singleton@stripe.com | 88% |
| ... | ... | ... | ... |

## Next Actions
1. Show more contacts (use offset to paginate)
2. Filter by department (e.g., "show me the marketing team")
3. Verify email addresses (1 verification credit each)
4. Save contacts as leads (Create-Lead-If-Missing — adds without overwriting existing leads)
5. Enrich Stripe with company details (Company-Enrichment)
```

5. **If the user asks for more,** present the next batch of results.

6. **If zero results,** suggest:
   - Check the domain spelling
   - The company may be too new or too small for our database
   - Try `Find-Companies` to find similar companies

## Credit Cost

Costs 1 search credit per 10 emails returned (rounded up) — only charged if emails are found.

## Success Criteria

At least one contact returned with name, email, and confidence score.
