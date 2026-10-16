---
title: Contact Deep Dive
description: How to exhaustively gather context for a contact using exact-person resolution, role and organization confirmation, recent award and opportunity activity, forward-looking pipeline, and selective agency, vendor, or state/local expansion.
---

# Contact Deep Dive

Use this reference when the user wants a deep dive on a single contact and the answer depends on more than the target row alone.

## Goal
- Contacts are person records by default. Exhaustive context means locking the exact contact identity first, then using that exact contact ID to understand role, organizational affiliation, recent award and opportunity activity, forward pipeline, and the strongest surrounding agency, vendor, or jurisdiction context.
- Prefer exact `contact_ids` filters across awards, opportunities, forecasts, and state/local surfaces before semantic expansion.
- Treat the contact as the primary anchor, not the organization. Only widen into agency, vendor, state, or jurisdiction context when the contact's own activity makes that necessary.
- If the target, organizational affiliation, recent awards, or near-term pipeline are already present in context, reuse them instead of refetching the same records.
- Stop once you can explain who the contact is, where they sit, how they appear in procurement activity, what near-term items they are tied to, and what the most relevant unresolved questions are.

## Workflow

### 1. Read the target first
- Harvest the target fields before doing any fan-out:
  - `govtribe_id`
  - `govtribe_url`
  - `types`
  - `name`
  - `email`
  - `phone`
  - `title`
  - `role`
  - `organization`
  - `govtribe_ai_summary`
  - `updated_at`
  - `parent_organization_details`
- If the target is not already in context, fetch it by exact GovTribe ID, exact quoted email, or exact quoted name.

### 2. Lock exact identity before widening
- Treat the resolved contact as the exact person first.
- Do not silently merge same-name contacts, nearby organization matches, or possible aliases into one person.
- Use `types`, `email`, `title`, `role`, `organization`, and `govtribe_ai_summary` to decide whether the target looks like:
  - a named individual
  - a functional mailbox or team inbox
  - a contact record with mixed or thin identity signals
- Only treat the record as mailbox-like when `types` explicitly includes `Mailbox` or the email/title pattern makes that conclusion unusually strong.
- If the record is clearly mailbox-like or a routing alias, say that explicitly. Do not narrate mailbox behavior as if it were one individual's buying history.
- Use `govtribe_ai_summary` early because it can surface buying-profile context that the raw title or role fields do not.

### 3. Confirm organizational affiliation before cross-surface fan-out
- Use `parent_organization_details` first when present.
- The parent can resolve to:
  - a federal agency
  - a vendor
  - a jurisdiction
  - a state
- If `parent_organization_details` is missing or ambiguous, resolve the affiliation conservatively using the safest available exact clue:
  - `Search_Federal_Agencies` for quoted agency or office names
  - `Search_Vendors` for quoted vendor names
  - `Search_Jurisdictions` or `Search_States` for state/local organizations
- Use this pass to answer:
  - whether the contact is primarily federal, vendor-side, or state/local
  - whether the organizational label is trustworthy enough to support a wider account-level narrative
  - whether the contact appears to be a named person, with mailbox-like behavior only as an explicit edge case

### 4. Build the federal awarding-behavior branch when the contact is federal or clearly appears on federal awards
- Use `Search_Federal_Contract_Awards` with exact `contact_ids=[target.govtribe_id]`.
- Start with an aggregation-first pass, then pull representative recent rows.
- Use the award branch to answer:
  - whether the contact appears mainly on awards, opportunities, or both
  - how much federal contract activity is associated with the contact
  - which vendors, NAICS, PSCs, and vehicles recur
  - whether the contact seems tied to one lane or many
- If federal award history is sparse, say that clearly and rely more heavily on opportunity, forecast, and organization context.

### 5. Surface the near-term federal pipeline early
- Use `Search_Federal_Contract_Opportunities` with exact `contact_ids=[target.govtribe_id]` for current and upcoming opportunities.
- Use `Search_Federal_Forecasts` with the same exact contact ID for planned requirements.
- If the contact appears to operate in grant space or the organization suggests it, use `Search_Federal_Grant_Opportunities` with the same exact contact ID.
- Keep these passes bounded with near-term windows:
  - federal opportunities: usually `due_date_range` over the next 60 to 180 days
  - forecasts: usually `estimated_solicitation_release_date_range` over the next 180 days
  - grant opportunities: usually `due_date_range` over the next 120 days
- Use this pipeline branch to answer:
  - what is on deck for this contact
  - whether upcoming work aligns with their recent award behavior
  - whether there are due-soon items that materially change what matters about the contact

### 6. Add the state and local branch only when the contact's affiliation or activity supports it
- If `parent_organization_details` indicates a jurisdiction or state, or the contact clearly appears in state/local procurement activity, use the state/local surfaces.
- Use `Search_State_And_Local_Contract_Awards` with exact `contact_ids=[target.govtribe_id]` for recent award-side activity.
- Use `Search_State_And_Local_Contract_Opportunities` with exact `contact_ids=[target.govtribe_id]` for near-term opportunity context.
- Keep the state/local branch bounded with realistic windows and location clues when available.
- Use this branch to answer:
  - whether the contact is active in state/local buying
  - which jurisdictions, entities, and category lanes recur
  - whether the contact appears mostly pre-award, post-award, or both

### 7. Use referenced-record evidence when the contact set or role signal is noisy
- If the contact's role is broad, the record is thin, or you need to prove how the contact is actually appearing in workflow records, use `Search_Contacts` with:
  - exact `contact_ids=[target.govtribe_id]`, and
  - `referenced_govtribe_ids` from the most representative awards, opportunities, forecasts, or files you already found
- Narrow `reference_types` when helpful:
  - `pointOfContact`
  - `transactionContact`
  - `externalFile`
  - `description`
- Use this pass to answer:
  - whether the contact is attached as an award administrator, opportunity POC, file-surfaced contact, or broader descriptive mention
  - whether the same contact recurs across multiple records in the same lane
  - whether a mailbox-like record or generic role is functioning as the real public-facing point of entry

### 8. Widen into organization context only when it materially helps answer the question
- If the user really needs account-level context rather than person-level context, widen after the exact contact branch is clear.
- Good widening paths are:
  - the contact's federal agency, using exact `federal_agency_ids`
  - the contact's vendor, using exact `vendor_ids`
  - the contact's state or jurisdiction, using the corresponding exact IDs
- Use the organization branch to answer:
  - whether the contact sits inside a bigger buying lane that matters to the user
  - whether the contact's behavior is representative of a broader office or organization
  - whether a mailbox-like edge case should be interpreted through its parent organization rather than as one person's history
- Do not default to a full agency or vendor deep dive unless the user actually needs that wider context.

### 9. Use file retrieval selectively and only from representative opportunities
- Do not default to file retrieval at the contact level.
- Only review files when a representative contract or grant opportunity tied to the contact appears central and the attached files are likely to contain requirement, compliance, or submission details that materially affect the answer.
- Preview exact `government_file_ids` with `Search_Government_Files` and use `content_snippet` first.
- If the snippet only suggests relevance, or the task depends on exact wording, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): call `Add_To_Vector_Store`, wait until ready, and call `Search_Vector_Store`. Cite returned source metadata with the external host's native citation format; for a material skipped file, use the host's attachment or spreadsheet capability or disclose the gap.

### 10. Use semantic expansion only after the exact-person passes, then stop with a context package
- If exact award, opportunity, forecast, and organization context is still too thin, use bounded semantic expansion.
- Good semantic targets are:
  - related opportunities
  - related forecasts
  - related contacts only when the user wants office-level or team-level context
- Treat semantic results as adjacency signals, not proof that two contacts are the same person or role.
- Good stopping points usually include:
  - the target contact and exact identity decision
  - the clearest role and organization takeaways
  - the strongest recent award signals
  - the most relevant upcoming opportunities, forecasts, or grant opportunities
  - any defensible state/local activity
  - any material file-derived findings from central notices
  - a short list of unresolved gaps
- Do not keep expanding if new records are only weakly related, duplicative, or organization-level noise that does not improve the answer.

## Examples

Fetch the exact target if it is not already in context:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "types",
    "name",
    "email",
    "phone",
    "title",
    "role",
    "organization",
    "govtribe_ai_summary",
    "updated_at",
    "parent_organization_details"
  ],
  "per_page": 1
}
```

Resolve a contact by exact quoted email when only the email is known:
Tool: `Search_Contacts`
```json
{
  "query": "\"<CONTACT_EMAIL>\"",
  "search_mode": "keyword",
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "email",
    "title",
    "organization",
    "parent_organization_details"
  ],
  "per_page": 5
}
```

Build a federal awarding-behavior rollup for the exact contact:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "award_date_range": {
    "from": "now-5Y/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_awardees_by_dollars_obligated",
    "top_naics_codes_by_dollars_obligated",
    "top_psc_codes_by_dollars_obligated",
    "top_federal_contract_vehicles_by_dollars_obligated",
    "top_set_aside_types_by_dollars_obligated",
    "top_transaction_points_of_contact_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Pull representative recent federal awards tied to the exact contact:
Tool: `Search_Federal_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "award_date_range": {
    "from": "now-5Y/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "contract_number",
    "award_date",
    "dollars_obligated",
    "awardee",
    "contracting_federal_agency",
    "funding_federal_agency",
    "naics_category",
    "psc_category",
    "federal_contract_vehicle",
    "transaction_contacts",
    "originating_federal_meta_opportunity_id",
    "originating_federal_contract_opportunity"
  ],
  "sort": {
    "key": "awardDate",
    "direction": "desc"
  },
  "per_page": 15
}
```

Surface upcoming federal contract opportunities for the exact contact:
Tool: `Search_Federal_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+90d/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "opportunity_type",
    "set_aside_type",
    "posted_date",
    "due_date",
    "descriptions",
    "federal_agency",
    "naics_category",
    "psc_category",
    "government_files",
    "points_of_contact"
  ],
  "sort": {
    "key": "dueDate",
    "direction": "asc"
  },
  "per_page": 15
}
```

Surface upcoming federal forecasts for the exact contact:
Tool: `Search_Federal_Forecasts`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "estimated_solicitation_release_date_range": {
    "from": "now/d",
    "to": "now+180d/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "forecast_type",
    "set_aside",
    "estimated_solicitation_release_date",
    "estimated_award_start_date",
    "estimated_award_value",
    "descriptions",
    "federal_agency",
    "points_of_contact"
  ],
  "sort": {
    "key": "estimated_solicitation_release_date",
    "direction": "asc"
  },
  "per_page": 15
}
```

Surface federal grant opportunities tied to the exact contact when grant activity matters:
Tool: `Search_Federal_Grant_Opportunities`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+120d/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "funding_instruments",
    "funding_activity_categories",
    "posted_date",
    "due_date",
    "description",
    "federal_agency",
    "federal_grant_programs",
    "government_files",
    "points_of_contact"
  ],
  "sort": {
    "key": "dueDate",
    "direction": "asc"
  },
  "per_page": 15
}
```

Build a state and local award rollup for the exact contact when the contact is state/local:
Tool: `Search_State_And_Local_Contract_Awards`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "award_date_range": {
    "from": "now-3Y/d",
    "to": "now/d"
  },
  "aggregations": [
    "dollars_obligated_stats",
    "top_contract_entities_by_dollars_obligated",
    "top_nigp_codes_by_dollars_obligated",
    "top_unspsc_codes_by_dollars_obligated",
    "top_states_by_dollars_obligated"
  ],
  "per_page": 0
}
```

Surface upcoming state and local opportunities for the exact contact:
Tool: `Search_State_And_Local_Contract_Opportunities`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "due_date_range": {
    "from": "now/d",
    "to": "now+90d/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "solicitation_number",
    "name",
    "posted_date",
    "due_date",
    "jurisdictions",
    "state",
    "government_files",
    "unspsc_categories",
    "nigp_categories",
    "points_of_contact"
  ],
  "sort": {
    "key": "dueDate",
    "direction": "asc"
  },
  "per_page": 15
}
```

Confirm how the exact contact appears across representative anchor records:
Tool: `Search_Contacts`
```json
{
  "search_mode": "keyword",
  "contact_ids": [
    "<CONTACT_ID>"
  ],
  "referenced_govtribe_ids": [
    "<ANCHOR_RECORD_ID_1>",
    "<ANCHOR_RECORD_ID_2>",
    "<ANCHOR_RECORD_ID_3>"
  ],
  "reference_types": [
    "pointOfContact",
    "transactionContact",
    "externalFile"
  ],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "email",
    "phone",
    "title",
    "role",
    "organization",
    "parent_organization_details",
    "govtribe_ai_summary"
  ],
  "per_page": 5
}
```
