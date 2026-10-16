---
name: prospecting
description: Runs end-to-end B2B prospecting by chaining company discovery, contact search, email verification, and enrichment. Use when the user wants to build a prospect list, find and qualify leads, or run a full prospecting pipeline.
user-invocable: true
argument-hint: Find CTOs at fintech startups in Europe
---

# Prospecting

Chain Hunter tools into a complete prospecting workflow. Discover companies, find contacts, verify emails, and enrich -- all in one go.

## Examples

- `/hunter:prospecting Find CTOs at fintech startups in France`
- `/hunter:prospecting decision-makers at Stripe, Notion, and Figma`
- `"Build me a list of marketing leads at SaaS companies in Germany"`
- `"I need 20 VPs of Sales at mid-size tech companies"`
- `"Find people to reach out to at companies using Salesforce in healthcare"`

## Workflow

For a quick starting point, you can call `Plan-Prospecting-Flow` with the user's goal to get a suggested end-to-end plan, then execute the steps below (or a refinement of it).

### Step 1: Identify Companies

Parse the user's request to determine the starting point:

- **Specific companies provided** (e.g., "Stripe, Notion, Figma") -- skip to Step 2.
- **Criteria provided** (e.g., "fintech startups in France") -- call `Find-Companies` with the criteria as the `query` parameter. If the user is targeting people by role (e.g. "CTOs at fintech startups"), still start from `Find-Companies`, then use `Domain-Search`'s seniority/department filters in Step 2 to pull just those people. (`Find-People` only counts contacts per company -- use it to size the batch, not to list people.)

Whenever more than one company will be searched, present the list and get approval before running Domain-Search, because each `Domain-Search` spends credits (1 per 10 results) and single-company calls have no built-in batch-consent gate:

> "I found [N] companies matching your criteria. Here are the results. Which should I search for contacts? Select specific companies or say 'proceed with all' — each Domain Search uses 1 credit per 10 results returned."

For long lists (>10), show the top results rather than all of them.

### Step 2: Find Contacts

For each company, call `Domain-Search` with the company's `domain`. Use server-side filters:
- "CTOs" or "engineering leaders" -> `department: "it"`, `seniority: "executive"`
- "marketing team" -> `department: "marketing"`
- "executives" or "C-suite" -> `seniority: "executive"`
- "senior people" -> `seniority: "senior,executive"`

Report progress for multi-company searches: "Searching stripe.com... found 15 contacts. Moving to notion.so..."

### Step 3: Verify Emails (Optional)

> Before verifying, confirm credit usage: "I found [N] contacts across [M] companies. Verifying all emails will use [N] verification credits. Proceed?"

Only verify after the user confirms. Call `Email-Verifier` for each contact's `email`.

If the user says "skip verification," present unverified results instead.

### Step 4: Enrich (Optional)

If the user asks for more company context, call `Company-Enrichment` for each company's `domain`. Only run this step if requested -- do not run by default.

### Step 5: Save to Hunter Leads

After presenting results, offer to save contacts:

> "Would you like me to save these contacts to your Hunter leads? I can create a new list for them."

If the user confirms:
1. Call `Create-Leads-List` with a descriptive name (e.g., "Fintech CTOs - France - 2026-04-08").
2. For each contact, call `Create-Lead-If-Missing` with the contact's data and the new `leads_list_id` — it adds new leads without overwriting existing ones. Note: an email that is already a lead is returned unchanged and is **not** added to the new list, so report those contacts as already-existing / not added rather than implying the whole set is in the list.
3. Present the deep-link: "View your leads list: https://hunter.io/leads?leads_list_id={id}"

### Step 6: Present Results

Present a consolidated table grouped by company:

```
# Prospect List: [Description]

**Companies:** [count] | **Contacts:** [count] | **Verified:** [deliverable] deliverable, [risky] risky

## [Company Name] (domain.com)
**Industry** | **Size** | **Location**

| Name | Position | Email | Verified |
|------|----------|-------|----------|
| ... | ... | ... | valid / accept_all / invalid / unknown |

## Next Steps
1. Save contacts to a Hunter leads list (Create-Lead-If-Missing)
2. Add contacts to a sequence (build-sequences skill)
3. Verify the risky addresses again later
4. Search for more companies with different criteria
```

## Credit Costs

- `Find-Companies` / `Find-People` — Free (no credits)
- `Domain-Search` — 1 search credit per 10 emails returned (rounded up)
- `Email-Verifier` — 1 verification credit per email
- `Company-Enrichment` — 1 enrichment credit per domain
- `Create-Lead-If-Missing`, `Create-Leads-List`, `Save-Company` — Free (no credits)

## Important Notes

- Always confirm before running verification on large batches
- If a company returns zero contacts, skip it and note it in the output
- If the user interrupts mid-workflow, present partial results gathered so far
- Prefer `Create-Lead-If-Missing` when saving found contacts so existing leads aren't overwritten
