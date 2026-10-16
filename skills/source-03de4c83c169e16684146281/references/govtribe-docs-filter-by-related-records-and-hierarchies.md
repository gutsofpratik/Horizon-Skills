<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Filter by related records and hierarchies

- Canonical GovTribe Docs page: [https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies](https://govtribe.com/docs/govtribe-for-agents/guides/filter-by-related-records-and-hierarchies)

Use this guide when a GovTribe MCP filter seems to include records beyond the exact value supplied. Some filters match a direct field, while others follow a relationship such as a parent agency, category family, awarded vendor role, contact, jurisdiction, IDV, vehicle, file, pursuit, or sub-award connection.

## How relationship filters work

GovTribe MCP search filters use structured record relationships. When a request supplies a known agency, vendor, category, contact, jurisdiction, parent record, or workflow record ID, GovTribe searches the relationship named by the filter.

The filter name controls the question being asked. For example, `vendor_ids`, `sub_vendor_ids`, `primary_consortia_member_ids`, `contracting_federal_agency_ids`, `funding_federal_agency_ids`, `federal_agency_ids`, `contact_ids`, and `jurisdiction_ids` can point to different relationships even when they all involve familiar organizations or people.

Use the most specific filter available on the selected tool. Use `query` when the important part is wording in a title, summary, description, file, or source text.

## Resolve values before filtering

Prefer GovTribe IDs from earlier search results when a filter expects entities. Several schema-valid ID filters also accept exact source identifiers or names and resolve them to canonical GovTribe records before the search runs.

| Need | Accepted exact values or common resolver |
| --- | --- |
| Agency IDs | A GovTribe ID; agency code; canonical or alternate name; acronym; or configured matching key. Use `Search_Federal_Agencies` when the value is unclear. |
| Vendor IDs | `Search_Vendors` |
| NAICS, PSC, NIGP, or UNSPSC IDs | The matching category `Search_*` tool |
| State IDs | A GovTribe ID, case-insensitive USPS code, or full state or territory name. Use `Search_States` when the value is unclear. |
| Jurisdiction IDs | `Search_Jurisdictions` or FIPS codes when accepted by the selected tool |
| Saved search, pursuit, pipeline, stage, task, or file IDs | The matching workspace or file search tool |

Exact values tolerate harmless case, punctuation, and whitespace differences. Each array element must resolve to one existing GovTribe record. An ambiguous or unknown value returns an indexed validation error instead of disappearing from the filter or broadening the search.

Agency resolution preserves the role named by the filter. An exact value supplied to `contracting_federal_agency_ids` remains a contracting-agency constraint, while the same value supplied to `funding_federal_agency_ids` remains a funding-agency constraint. When an exact match identifies a non-displayable agency office, GovTribe uses its configured displayable parent; if more than one displayable agency remains equally valid, the tool asks for a more specific value.

Use [Source identifiers and record matching](https://govtribe.com/docs/data-model/guides/source-identifiers-and-record-matching) when you need to decide whether a value is a GovTribe ID, source identifier, code, or display label.

## Hierarchies and parent values

Some filters use hierarchy context so a broader value can find narrower records beneath it.

- Agency filters may include records tied to child offices, bureaus, commands, or related organization levels depending on the selected filter and search tool.
- Category filters may use parent or child NAICS, PSC, NIGP, or UNSPSC context.
- State and jurisdiction filters can separate broad state scope from county, city, school district, and other local-government geography.
- Vehicle, IDV, and subcategory filters can include records connected through a broader buying lane or parent instrument.

When a parent value is selected, results may include child agencies, child categories, or records tied to narrower related values. Request the relationship fields needed to verify the exact child value.

## Organization and role filters

Organization filters are role-specific. The same organization can appear in different roles across records.

| Filter pattern | Typical meaning |
| --- | --- |
| `vendor_ids` on award and parent-instrument tools | The organization won, received, or holds the award or parent instrument. |
| `sub_vendor_ids` or subcontractor fields | The organization appears in a subcontractor or downstream recipient role. |
| `primary_consortia_member_ids` | The organization appears as a primary consortia member where the selected tool exposes that relationship. |
| `vendor_ids` | The selected tool's vendor relationship, which can differ by record type. |
| `contracting_federal_agency_ids` | The agency that awarded, issued, executed, or administers the contract action. |
| `funding_federal_agency_ids` | The agency whose mission, program, or budget funded the record. |
| `federal_agency_ids` | The general agency relationship exposed by the selected tool. |
| `contact_ids` | A person or point of contact connected to the record. |

If a result is connected to the organization but the role feels wrong, check the filter name before changing the `query`.

## Parent and connected records

Some filters match through a parent, container, or connected record rather than a field that appears prominently in the returned row.

- `federal_contract_idv_ids`, `federal_contract_vehicle_ids`, and vehicle subcategory filters can find records tied to ordering instruments, schedules, pools, lanes, SINs, or buying channels.
- `federal_contract_opportunity_ids` on `Search_Federal_Contract_Awards` and `Search_Federal_Contract_IDVs` finds the awards or IDVs tied to one specific opportunity notice. Use `federal_meta_opportunity_ids` instead when the question covers the opportunity's whole notice chain. GovTribe stores at most 500 opportunity IDs per award or IDV, so a record linked to more opportunities than that, such as a Multiple Award Schedule award, may not match every opportunity it belongs to. Treat an empty result as inconclusive for MAS and other very high-volume schedules rather than as proof that no linked records exist.
- State and local IDV or vehicle filters can find records connected to state and local parent contract structures.
- Government file and user file filters can use parent record, source record, workspace, pursuit, or file-bearing entity context.
- Workspace filters can narrow by pursuit, pipeline, stage, task, owner, creator, saved search, or workflow state when the selected tool exposes those filters.

Use these filters when the question is about the relationship around a record. Use record-specific tools or returned relationship fields when the agent needs to verify the exact parent, child, source, or downstream connection.

### Inspect a federal transaction's immediate parent

On [Search federal transactions MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-federal-transactions-mcp-tool), select `transaction_type` and `parent_record` when the answer needs family or lineage context. The parent is the record that owns the transaction. A contract subaward transaction points to its contract subaward; an assistance subaward transaction points to its assistance subaward. Neither substitutes the upstream prime award.

Tool: `Search_Federal_Transactions`

```json
{
  "govtribe_ids": ["<transaction_govtribe_id>"],
  "fields_to_return": ["govtribe_id", "transaction_type", "parent_record"]
}
```

A resolved `parent_record` includes `status: "resolved"`, the parent's `govtribe_id`, `govtribe_type`, and name, with a URL or source contract/grant identifier when available. Use the returned type to choose the matching parent search tool and its GovTribe ID to retrieve the parent. Source contract or grant identifiers describe the parent; they are not its GovTribe ID.

If the parent cannot be resolved, `status: "unavailable"` preserves the stored parent ID and any recognized type. An unrecognized parent class has a null `govtribe_type`. Keep the transaction in the answer, state that the parent is unavailable, and do not infer a parent name, URL, or upstream award. See [Parent record](https://govtribe.com/docs/data-model/attributes/parent-record-attribute) for the returned field shape.

## Pursuit discussion and comment workflow

Pursuit responses do not include nested discussion or comment arrays. Retrieve those records through the discussion and comment search tools so the agent can keep payloads focused.

1. Resolve the pursuit with [Search pursuits MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-pursuits-mcp-tool) or another tool that returns a pursuit `govtribe_id`.
2. Pass that ID to [Search pursuit discussions MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-pursuit-discussions-mcp-tool) using `pursuit_ids`.
3. Pass returned discussion IDs to [Search pursuit comments MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-pursuit-comments-mcp-tool) using `discussion_ids`.

## Example

This request asks for awards connected to a contracting-agency role, not just awards whose text mentions the agency name.

Tool: `Search_Federal_Contract_Awards`

```json
{
  "contracting_federal_agency_ids": ["Department of Defense"],
  "award_date_range": {
    "from": "now-12M/d",
    "to": "now/d"
  },
  "fields_to_return": [
    "govtribe_id",
    "name",
    "contracting_federal_agency",
    "funding_federal_agency",
    "awardee",
    "dollars_obligated"
  ],
  "per_page": 10
}
```

## When results look broader than expected

Start by checking the exact filter names and selected values.

- If the request used a parent agency or parent category, results may include child offices, child categories, or records classified under narrower values.
- If the request used an organization ID, confirm whether the filter is for awarded vendor, vendor, contracting agency, funding agency, recipient, subcontractor, or another role.
- If the request used an IDV, vehicle, subcategory, file, pursuit, contact, jurisdiction, or state value, confirm whether the result is connected through a parent or related record.
- If the result set is still too broad, use a more specific child value, add a date or status filter, request fewer result rows, or remove one relationship filter at a time.

## Related articles

- [Manage search context](https://govtribe.com/docs/govtribe-for-agents/guides/manage-search-context): Shape `fields_to_return` and retrieve child records with a second search call.
- [Choose a search mode and write queries](https://govtribe.com/docs/govtribe-for-agents/guides/choose-a-search-mode-and-write-queries): Choose keyword or semantic search and shape the `query` value.
- [Location filtering](https://govtribe.com/docs/govtribe-for-agents/guides/location-filtering): Resolve location text, compound location values, state names, and USPS codes without broadening the search.
- [Troubleshoot search results](https://govtribe.com/docs/govtribe-for-agents/guides/troubleshoot-search-results): Adjust a search call when results are too broad, too narrow, or missing expected records.
- [Search pursuit discussions MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-pursuit-discussions-mcp-tool): Retrieve discussion records attached to pursuits.
- [Search pursuit comments MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-pursuit-comments-mcp-tool): Retrieve comments inside pursuit discussions.
- [Contracting and funding federal agencies](https://govtribe.com/docs/data-model/guides/contracting-and-funding-federal-agencies): Choose the right federal agency role when filtering or reviewing federal records.
- [Vendor, awardee, recipient, and subcontractor roles](https://govtribe.com/docs/data-model/guides/vendor-awardee-recipient-and-subcontractor-roles): Distinguish awardee, recipient, prime, parent, and subcontractor relationships.
- [Choosing category systems](https://govtribe.com/docs/data-model/guides/choosing-category-systems): Choose between NAICS, PSC, NIGP, UNSPSC, and Assistance Listings.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
