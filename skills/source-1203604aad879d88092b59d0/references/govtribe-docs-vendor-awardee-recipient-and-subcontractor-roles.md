<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Vendor, awardee, recipient, and subcontractor roles

- Canonical GovTribe Docs page: [https://govtribe.com/docs/data-model/guides/vendor-awardee-recipient-and-subcontractor-roles](https://govtribe.com/docs/data-model/guides/vendor-awardee-recipient-and-subcontractor-roles)

GovTribe uses [Vendor data type](https://govtribe.com/docs/data-model/data-types/vendor) records for organizations that appear in government-market data. The field name tells you the organization's role on a specific record.

## Quick model

| Role | Meaning | Use when asking |
| --- | --- | --- |
| Vendor | The organization profile GovTribe stores. | What organization is this? |
| Awardee or recipient | The organization directly awarded a prime contract, IDV, grant, or assistance record. | Who won or received the prime award? |
| Prime contractor or prime grantee | The upstream prime organization on a reported sub-award. | Which prime reported or passed through the work? |
| Subcontractor or sub-grantee | The downstream organization on a reported sub-award. | Who received downstream work or pass-through funding? |
| Parent of awardee | Corporate or parent organization context tied to the awardee. | What larger organization is associated with the awardee? |
| Primary consortium member | A vendor role used when source context identifies a leading member of a consortium. | Which consortium member should I treat as the primary participant? |

## Which field should I use?

| Question | Use | Why |
| --- | --- | --- |
| Who won this contract award, IDV, or grant award? | `awardee` or `awardee_name` | This is the direct award party on prime award-style records. |
| Who received a grant or assistance award? | `awardee` on grant award records. | GovTribe uses the shared vendor relationship for grant recipients as well as contract awardees. |
| Who is the prime on a reported subcontract? | `prime_contractor` | This is the upstream prime contractor on federal contract sub-awards. |
| Who is the subcontractor? | `sub_contractor` | This is the downstream subcontractor on federal contract sub-awards. |
| Who is the prime recipient on a grant sub-award? | `prime_grantee` | This is the upstream grant recipient or pass-through entity. |
| Who is the subrecipient? | `sub_grantee` | This is the downstream recipient on federal grant sub-awards. |
| What vendor profile should I join to? | The linked [Vendor data type](https://govtribe.com/docs/data-model/data-types/vendor) record, often by `govtribe_id` or `uei` when available. | The role field explains the relationship, while the vendor record stores organization identity and enrichment. |

## GovTribe field mapping

| GovTribe field | Appears on | Role |
| --- | --- | --- |
| `awardee` | Federal contract awards, federal contract IDVs, federal grant awards, federal transactions. | Direct awardee or recipient. |
| `awardee_name` | State and local contract awards and IDVs. | Source-provided awardee relationship. |
| `parent_of_awardee` | Federal contract awards, IDVs, and grant awards. | Parent organization context for the direct awardee. |
| `primary_consortia_member` | Federal contract awards and IDVs. | Primary consortium participant when available. |
| `prime_contractor` | Federal contract sub-awards. | Prime contractor reporting or associated with downstream subcontracting. |
| `sub_contractor` | Federal contract sub-awards. | Downstream subcontractor. |
| `prime_grantee` | Federal grant sub-awards. | Prime grant recipient or pass-through entity. |
| `sub_grantee` | Federal grant sub-awards. | Downstream grant subrecipient. |

## Official source notes

- [USAspending Federal Spending Guide](https://www.usaspending.gov/data/Federal-Spending-Guide.pdf) distinguishes prime awards from sub-awards and explains recipient and award-spending concepts.
- [SAM.gov entity registration and UEI](https://sam.gov/entity-registration) explains entity registration, Unique Entity IDs, and when an organization may need only a UEI.
- [GSA Unique Entity ID guidance](https://www.gsa.gov/about-us/organization/federal-acquisition-service/fas-initiatives/integrated-award-environment/iae-systems-information-kit/unique-entity-id-is-here) identifies UEI as the federal award identifier of record across IAE systems.
- [SAM.gov Contracting](https://sam.gov/contracting) covers contract opportunities, awards, and subcontract reports in SAM.gov.

## Related articles

- [Vendor data type](https://govtribe.com/docs/data-model/data-types/vendor): Review the organization record used for vendors, awardees, recipients, and suppliers.
- [Vendor attribute](https://govtribe.com/docs/data-model/attributes/vendor-attribute): Review the shared relationship attribute used by organization role fields.
- [Federal contract sub-award](https://govtribe.com/docs/data-model/data-types/federal-contract-sub-award): Review reported subcontracting records.
- [Federal grant sub-award](https://govtribe.com/docs/data-model/data-types/federal-grant-sub-award): Review reported pass-through assistance records.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
