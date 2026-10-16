---
name: email-finder
description: Finds a professional email address from a person's name and company domain. Use when the user asks to find someone's email, look up a contact's email address, or needs to reach a specific person at a company.
user-invocable: true
argument-hint: Jane Smith at stripe.com
---

# Email Finder

Find the most likely email address for a person at a company using their name and domain.

## Examples

- `/hunter:email-finder Jane Smith at stripe.com`
- `/hunter:email-finder the CEO of notion.so`
- `"What's John Doe's email at acme.com?"`
- `"Find the email for Sarah Chen at Figma"`
- `"How can I reach Marc Benioff at Salesforce?"`

## Steps

1. **Parse the input.** Extract the person's `full_name` and the company `domain`.
   - "Jane Smith at Stripe" -> `full_name`: "Jane Smith", `domain`: "stripe.com"
   - If the user provides a company name instead of a domain, infer the likely domain (e.g., "Stripe" -> "stripe.com")
   - If only a role is given (e.g., "the CTO of Notion"), note that `Email-Finder` requires a name. Suggest using `Domain-Search` on the domain first to find the person's name, then come back to find their email.

2. **Call `Email-Finder`** with `full_name` and `domain`.

3. **Present the result:**

```
# Email Found: Jane Smith @ Stripe

| Field | Value |
|-------|-------|
| **Email** | jane.smith@stripe.com |
| **Score** | 92 |
| **Domain** | stripe.com |
| **Verification** | valid |

## Sources
- stripe.com/team (last seen: 2026-02-15)
- LinkedIn profile (last seen: 2026-01-20)

## Next Actions
1. Verify this email address (Email-Verifier)
2. Save as a lead (Create-Lead-If-Missing — adds without overwriting an existing lead)
3. Enrich this contact with more details (Person-Enrichment)
4. Find more contacts at stripe.com (Domain-Search)
```

4. **If no email is found,** suggest alternatives:
   - "I couldn't find an email for [name] at [domain]. Would you like me to search all contacts at [domain] instead? That might help find the right person."
   - Suggest checking the spelling of the name or trying a different domain variation.

## Credit Cost

Costs 1 search credit — only charged if an email is found.

## Success Criteria

Email address returned with score and at least one source.
