---
name: person-enrichment
description: Retrieves detailed information about a person from their email address, including name, position, company, and social profiles. Use when the user asks about a person, wants to enrich a contact, or needs more details about someone whose email they have.
user-invocable: true
argument-hint: jane@stripe.com
---

# Person Enrichment

Get a detailed profile of a person from their email address.

## Examples

- `/hunter:person-enrichment jane@stripe.com`
- `"What do you know about john@acme.com?"`
- `"Who is sarah@notion.so?"`
- `"Enrich this contact: marc@salesforce.com"`
- `"Get me details on hello@figma.com"`

## Steps

1. **Parse the input.** Extract the `email` address.

2. **Call `Person-Enrichment`** with the `email`. To retrieve both the person and their company in a single call, use `Combined-Enrichment` instead.

3. **Present the person profile:**

```
# Person: Jane Smith (jane@stripe.com)

| Field | Value |
|-------|-------|
| **Name** | Jane Smith |
| **Position** | VP of Engineering |
| **Company** | Stripe |
| **Location** | San Francisco, CA |
| **LinkedIn** | linkedin.com/in/janesmith |
| **Twitter** | @janesmith |

## Next Actions
1. Verify this email address (`Email-Verifier`)
2. Save as a lead (`Create-Lead-If-Missing` — adds without overwriting an existing lead)
3. Find more contacts at stripe.com (`Domain-Search`)
4. Enrich Stripe with company details (`Company-Enrichment`)
```

4. **If no data is found,** respond: "No data available for [email]. Try enriching their company domain instead, or use Domain Search to find other contacts at this company."

## Credit Cost

Costs 1–2 enrichment credits (plan-dependent — 1 on two-bucket plans, 2 on single-credit-bucket plans) — only charged if data is found.

## Success Criteria

Person's name and position returned from the email address.
