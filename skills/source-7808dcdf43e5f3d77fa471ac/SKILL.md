---
name: company-enrichment
description: Retrieves detailed company information including industry, size, location, and description from a domain name. Use when the user asks about a company, wants company details, or says "tell me about [company]".
user-invocable: true
argument-hint: stripe.com
---

# Company Enrichment

Get a detailed profile of any company from its domain name.

## Examples

- `/hunter:company-enrichment stripe.com`
- `"Tell me about acme.com"`
- `"What does notion.so do?"`
- `"Company info for figma.com"`
- `"Look up HubSpot"`

## Steps

1. **Parse the input.** Extract the `domain`.
   - "stripe.com" -> use directly
   - "Stripe" -> infer domain as "stripe.com"

2. **Call `Company-Enrichment`** with the `domain`. To retrieve both a company profile and a contact's details for an email in one call, use `Combined-Enrichment` instead.

3. **Present the company profile:**

```
# Company: Stripe (stripe.com)

| Field | Value |
|-------|-------|
| **Industry** | Financial Technology |
| **Size** | 5,000-10,000 employees |
| **Founded** | 2010 |
| **Headquarters** | San Francisco, CA |
| **Type** | Private |

## Description
Stripe builds economic infrastructure for the internet, enabling businesses to accept payments and manage their businesses online.

## Social Profiles
- LinkedIn: linkedin.com/company/stripe
- Twitter: @stripe

## Next Actions
1. Find contacts at stripe.com (Domain-Search)
2. Search for similar companies with Find-Companies
3. Find a specific person's email at Stripe (Email-Finder)
4. Save this company to your leads (Save-Company)
```

4. **If the domain is unknown,** respond: "No company data available for [domain]. Try checking the spelling, or use Find-Companies to search for companies by name."

## Credit Cost

Costs 1–2 enrichment credits (plan-dependent — 1 on two-bucket plans, 2 on single-credit-bucket plans) — only charged if data is found.

## Success Criteria

Company name, industry, and size returned.
