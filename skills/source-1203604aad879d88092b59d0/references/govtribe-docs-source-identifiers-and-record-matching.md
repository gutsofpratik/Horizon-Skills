<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Source identifiers and record matching

- Canonical GovTribe Docs page: [https://govtribe.com/docs/data-model/guides/source-identifiers-and-record-matching](https://govtribe.com/docs/data-model/guides/source-identifiers-and-record-matching)

Identifiers answer different matching questions. Some identify a GovTribe record, some identify a source record, some identify an organization, and some link one procurement lifecycle stage to another.

## Quick model

| Identifier | Meaning | Use when asking |
| --- | --- | --- |
| `govtribe_id` | GovTribe's stable record identifier. | Which exact GovTribe record is this? |
| `search_results_id` | A temporary GovTribe search state returned by a replayable search tool. | Which recent search should be saved, reopened, or used to replace saved-search criteria? |
| `contract_number` | Source-reported contract, award, IDV, or state and local contract number. | What source contract or award number should I compare? |
| `solicitation_number` | Source-reported notice or solicitation identifier. | Which opportunity or notice is this? |
| `grant_number` | Source-reported grant or assistance award identifier. | Which grant award is this? |
| `uei` | SAM.gov Unique Entity ID for an organization. | Which registered entity is this? |
| `source_url` | Original source location when available. | Where did this record come from? |
| `originating_*` fields | Upstream notice or opportunity context. | Which pre-award record is linked to this awarded record? |

## GovTribe ID formats

`govtribe_id` identifies a GovTribe record for links, exports, MCP responses, Zapier data, copied URLs, and follow-on workflows. Use it with `govtribe_type` when a workflow needs to know both the record and the kind of record being referenced.

The visible value format can vary by data type. Treat the returned `govtribe_id` as the public GovTribe record identifier for that `govtribe_type`, not as a promise that the value is the original source identifier.

| Data types | Typical public `govtribe_id` format | Matching note |
| --- | --- | --- |
| Many GovTribe-managed data types | Internal GovTribe key, often a 24-character ID. | Use the exact value with `govtribe_type` when reopening the record, adding it to a workflow, or passing it to another GovTribe tool. |
| Vendor | Current SAM-backed vendor records often use the vendor's UEI; older records can have a legacy GovTribe vendor ID. | Use `uei` when matching organizations to federal source systems. Use `govtribe_id` when referencing the GovTribe vendor record. |
| Federal agency | Agency code or agency hierarchy code. | Use the returned `govtribe_id` for GovTribe agency filters. Use source agency codes and office context when reconciling to source data. |
| Federal contract opportunity | SAM opportunity ID or parent opportunity ID. | Use `solicitation_number` when comparing notice labels or source solicitation values. |
| Federal contract award and federal contract IDV | PIID or referenced-IDV style identifier. | Awards and IDVs are not identified by solicitation number alone. Keep `contract_number`, referenced IDV context, and originating-opportunity fields nearby. |
| Federal grant opportunity, award, program, and sub-award | Grants.gov opportunity ID, FAIN, Assistance Listing number, or sub-award report number, depending on the data type. | Use `grant_number` and program numbers when comparing to Grants.gov, SAM.gov, or USAspending source data. |
| Federal contract vehicle, DOD acquisition program, GSA labor rate, and government file | Source-aligned or GovTribe-derived keys. | Use `govtribe_id` for GovTribe workflows. Use source fields, contract context, and files when auditing the original record. |
| NAICS, PSC, NIGP, and UNSPSC category | Classification code. | Category data types use their classification code as the public GovTribe ID in MCP and search responses. |

Use `govtribe_id` for GovTribe workflows. Use source identifiers, such as `uei`, `contract_number`, `solicitation_number`, or `grant_number`, when matching to external systems.

## Which identifier should I use?

| Question | Use | Why |
| --- | --- | --- |
| I need to link back to a GovTribe record. | `govtribe_id` or `govtribe_url` | These identify GovTribe records and pages, not necessarily the original source object. |
| I need to preserve or reuse a recent GovTribe search. | `search_results_id` | This identifies the replayable search state, not an individual result row. |
| I need to compare federal contract awards or IDVs to source contract data. | `contract_number`, referenced IDV context, and `originating_federal_meta_opportunity_id` when available. | Federal contract records often need both award identifiers and upstream notice identifiers. |
| I need to match a pre-award notice to an awarded record. | `solicitation_number`, `federal_meta_opportunity_id`, and `originating_federal_contract_opportunity`. | These fields preserve opportunity and originating-notice context when GovTribe has it. |
| I need to identify an organization across federal award systems. | `uei` on the linked vendor. | UEI is the current federal entity identifier of record. |
| I need to reference a specific GovTribe vendor record. | `govtribe_id` with `govtribe_type`, and keep `uei` nearby when available. | The GovTribe vendor record and the federal organization identifier are related, but they are not always the same value. |
| I need to audit or inspect the original source. | `source_url` and attached government files. | Source links and files are the closest customer-facing trail back to the original notice or document. |

## When a solicitation number does not find an award

A solicitation number usually identifies a pre-award opportunity or notice. Award records often use a PIID, contract number, referenced IDV, transaction identifier, or originating-opportunity field instead of the solicitation number as the primary award identifier.

If a solicitation number does not find an award, search the opportunity record first, then use related records, originating fields, source files, agency, vendor, title, dates, and referenced IDV context to look for the awarded record. When available, open the opportunity's related awards, IDVs, vehicles, or source files instead of assuming the solicitation number must appear directly on the award record.

## GovTribe field mapping

| GovTribe field | Identifies | Related attribute |
| --- | --- | --- |
| `govtribe_id` | GovTribe record. | [GovTribe ID](https://govtribe.com/docs/data-model/attributes/govtribe-id-attribute) |
| `govtribe_url` | GovTribe web page. | [GovTribe URL](https://govtribe.com/docs/data-model/attributes/govtribe-url-attribute) |
| `search_results_id` | Replayable search state. | [Search results ID](https://govtribe.com/docs/data-model/attributes/search-results-id-attribute) |
| `contract_number` | Contract, award, IDV, or state and local contract source identifier. | [Contract number](https://govtribe.com/docs/data-model/attributes/contract-number-attribute) |
| `solicitation_number` | Opportunity or notice identifier. | [Solicitation number](https://govtribe.com/docs/data-model/attributes/solicitation-number-attribute) |
| `grant_number` | Federal grant award identifier. | [Grant number](https://govtribe.com/docs/data-model/attributes/grant-number-attribute) |
| `uei` | Vendor or entity identifier from SAM.gov. | [UEI](https://govtribe.com/docs/data-model/attributes/uei-attribute) |
| `source_url` | Original source URL. | [Source URL](https://govtribe.com/docs/data-model/attributes/source-url-attribute) |
| `federal_meta_opportunity_id` | GovTribe's federal opportunity source identifier context. | [Federal meta opportunity ID](https://govtribe.com/docs/data-model/attributes/federal-meta-opportunity-id-attribute) |
| `originating_federal_meta_opportunity_id` | Upstream federal opportunity identifier on an awarded or vehicle record. | [Originating federal meta opportunity ID](https://govtribe.com/docs/data-model/attributes/originating-federal-meta-opportunity-id-attribute) |
| `originating_federal_contract_opportunity` | Linked upstream federal contract opportunity. | [Originating federal contract opportunity](https://govtribe.com/docs/data-model/attributes/originating-federal-contract-opportunity-attribute) |

## Matching rules of thumb

- Use `govtribe_id` when matching inside GovTribe exports, MCP responses, Zapier data, or copied URLs.
- Use source identifiers when comparing to SAM.gov, USAspending, Grants.gov, state and local source portals, or customer-owned spreadsheets.
- Use `uei` to match organizations, not awards or opportunities.
- Use originating fields as strong relationship signals, but expect gaps because not every source record connects cleanly across the procurement lifecycle.
- Use [Federal contract opportunity notice chains](https://govtribe.com/docs/data-model/guides/federal-contract-opportunity-notice-chains) when you need to retrieve original, newest viable, or originating federal contract opportunity records from chain fields.
- When identifiers are incomplete, compare multiple signals together: agency, vendor, title, dates, contract number, solicitation number, category, place of performance, and source files.

## Official source notes

- [FAR 4.605](https://www.acquisition.gov/far/4.605) requires governmentwide-unique PIIDs for FPDS reporting and requires reporting the successful offeror's Unique Entity ID.
- [SAM.gov Contract Award Data](https://sam.gov/contract-data) exposes contract identification filters such as PIID, referenced IDV PIID, solicitation ID, and document type.
- [USAspending Federal Spending Guide](https://www.usaspending.gov/data/Federal-Spending-Guide.pdf) explains award unique keys, contract award unique keys, assistance award unique keys, and the use of identifiers for joining award summaries and transactions.
- [GSA Unique Entity ID guidance](https://www.gsa.gov/about-us/organization/federal-acquisition-service/fas-initiatives/integrated-award-environment/iae-systems-information-kit/unique-entity-id-is-here) identifies UEI as the federal award identifier of record for entities.

## Related articles

- [Federal contract record structure](https://govtribe.com/docs/data-model/guides/federal-contract-record-structure): Choose the right federal contract record type before matching records.
- [Federal contract opportunity notice chains](https://govtribe.com/docs/data-model/guides/federal-contract-opportunity-notice-chains): Retrieve related notices and originating opportunity context from GovTribe notice-chain fields.
- [Federal award values and transactions](https://govtribe.com/docs/data-model/guides/federal-award-values-and-transactions): Avoid mixing award summaries and transaction rows while joining data.
- [GovTribe ID attribute](https://govtribe.com/docs/data-model/attributes/govtribe-id-attribute): Review the shared GovTribe record identifier.
- [UEI attribute](https://govtribe.com/docs/data-model/attributes/uei-attribute): Review the SAM.gov entity identifier used on vendor records.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
