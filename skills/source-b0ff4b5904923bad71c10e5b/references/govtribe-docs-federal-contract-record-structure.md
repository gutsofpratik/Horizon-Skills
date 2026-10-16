<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Federal contract record structure

- Canonical GovTribe Docs page: [https://govtribe.com/docs/data-model/guides/federal-contract-record-structure](https://govtribe.com/docs/data-model/guides/federal-contract-record-structure)

Federal contract records answer different questions depending on where they sit in the procurement lifecycle. Use this guide when a search result, export, or MCP response includes several federal contract data types that look related but are not interchangeable.

## Quick model

| Data type | Role | Use when asking |
| --- | --- | --- |
| [Federal forecast](https://govtribe.com/docs/data-model/data-types/federal-forecast) | Early planning signal. | What might an agency buy later? |
| [Federal contract opportunity](https://govtribe.com/docs/data-model/data-types/federal-contract-opportunity) | Public procurement notice. | What is currently planned, solicited, amended, or announced? |
| [Federal contract vehicle opportunity](https://govtribe.com/docs/data-model/data-types/federal-contract-vehicle-opportunity) | Opportunity under vehicle context. | What demand is being competed through a vehicle, pool, SIN, or lane? |
| [Federal contract vehicle data type](https://govtribe.com/docs/data-model/data-types/federal-contract-vehicle) | Broad contract family or buying lane. | What program, schedule, GWAC, or master vehicle organizes this market? |
| [Federal contract IDV data type](https://govtribe.com/docs/data-model/data-types/federal-contract-idv) | Parent ordering instrument. | What parent contract or agreement can issue orders? |
| [Federal contract award](https://govtribe.com/docs/data-model/data-types/federal-contract-award) | Awarded contract, order, purchase order, or BPA call. | Who won and what work was awarded? |
| [Federal transaction](https://govtribe.com/docs/data-model/data-types/federal-transaction) | Action-level spending or modification event. | What changed or obligated value over time? |
| [Federal contract sub-award data type](https://govtribe.com/docs/data-model/data-types/federal-contract-sub-award) | Reported downstream subcontract. | Which subcontractors were reported under prime award activity? |

## How to choose the right record type

| Question | Start with | Why |
| --- | --- | --- |
| I want current or upcoming demand. | Federal forecast or federal contract opportunity. | These records are pre-award signals. |
| I want demand tied to a known vehicle. | Federal contract vehicle opportunity. | Vehicle opportunities preserve vehicle or subcategory context. |
| I want the broad market lane. | Federal contract vehicle. | Vehicles group related IDVs, opportunities, holders, and categories. |
| I want a vendor's parent contract. | Federal contract IDV. | IDVs are parent instruments used for future orders. |
| I want historical awarded work. | Federal contract award. | Awards are the main prime awarded-work records. |
| I want modification or obligation history. | Federal transaction. | Transactions are action-level records beneath awards or IDVs. |
| I want downstream subcontracting. | Federal contract sub-award. | Sub-awards are reported subcontracting activity beneath prime awards. |

## How records connect

Not every record has every relationship. A contract opportunity may connect to an award when source identifiers support it. An award may connect to a parent IDV. An IDV may connect to a vehicle. An award may also connect to transactions and reported sub-awards. When direct relationships are missing, compare records through identifiers, agency roles, vendor roles, categories, dates, source URLs, and file context.

## GovTribe relationship mapping

| Relationship field | Meaning | Related article |
| --- | --- | --- |
| `federal_contract_vehicle` | Vehicle or broad contract family connected to an opportunity, award, or IDV. | [Federal contract vehicle attribute](https://govtribe.com/docs/data-model/attributes/federal-contract-vehicle-attribute) |
| `federal_contract_idv` | Parent IDV connected to a federal contract award. | [Federal contract IDV attribute](https://govtribe.com/docs/data-model/attributes/federal-contract-idv-attribute) |
| `federal_meta_opportunity_id` | Notice-chain identifier connected to a federal contract opportunity. | [Federal contract opportunity notice chains](https://govtribe.com/docs/data-model/guides/federal-contract-opportunity-notice-chains) |
| `originating_federal_contract_opportunity` | Upstream opportunity connected to an awarded or vehicle record. | [Originating federal contract opportunity attribute](https://govtribe.com/docs/data-model/attributes/originating-federal-contract-opportunity-attribute) |
| `task_orders` | Child task orders connected to an IDV. | [Task orders attribute](https://govtribe.com/docs/data-model/attributes/task-orders-attribute) |
| `sub_contracts` | Reported contract sub-awards connected to a prime award. | [Federal contract sub-award attribute](https://govtribe.com/docs/data-model/attributes/federal-contract-sub-award-attribute) |

## Official source notes

- [SAM.gov Contract Award Data](https://sam.gov/contract-data) includes award, IDV, and other transaction contract data and identifies common filters such as PIID, referenced IDV PIID, solicitation ID, NAICS, PSC, date signed, and competition fields.
- [SAM.gov Opportunity Management API](https://open.gsa.gov/api/opportunities-api/) lists contract opportunity notice types such as solicitation, presolicitation, sources sought, award notice, and special notice.
- [FAR 4.601](https://www.acquisition.gov/far/4.601) defines contract action reports, definitive contracts, and indefinite delivery vehicles for FPDS reporting context.
- [USAspending Federal Spending Guide](https://www.usaspending.gov/data/Federal-Spending-Guide.pdf) explains IDVs, prime award transactions, prime award summaries, and the relationship between awards and transactions.

## Related articles

- [Federal contract data model](https://govtribe.com/docs/data-model/guides/federal-contract-data-model): Review the broader federal contract hierarchy.
- [Federal contract opportunity notice chains](https://govtribe.com/docs/data-model/guides/federal-contract-opportunity-notice-chains): Use notice-chain fields to connect federal opportunities to related awards, IDVs, and vehicles.
- [Federal award values and transactions](https://govtribe.com/docs/data-model/guides/federal-award-values-and-transactions): Distinguish award summaries, transaction events, obligations, and potential values.
- [Source identifiers and record matching](https://govtribe.com/docs/data-model/guides/source-identifiers-and-record-matching): Use identifiers and originating links to compare related records.
- [Contracting and funding federal agencies](https://govtribe.com/docs/data-model/guides/contracting-and-funding-federal-agencies): Choose the right agency role on federal contract awards and IDVs.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
