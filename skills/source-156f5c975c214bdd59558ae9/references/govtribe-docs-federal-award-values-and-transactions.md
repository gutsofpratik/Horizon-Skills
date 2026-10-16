<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Federal award values and transactions

- Canonical GovTribe Docs page: [https://govtribe.com/docs/data-model/guides/federal-award-values-and-transactions](https://govtribe.com/docs/data-model/guides/federal-award-values-and-transactions)

Use value fields differently depending on whether the question is about an award-level record, a transaction-level event, or a potential contract limit. This guide applies to GovTribe federal contract awards, federal contract IDVs, federal grant awards, federal transactions, and federal sub-award records.

## Quick model

| Concept | Meaning | Use when asking |
| --- | --- | --- |
| Award summary | A rolled-up record for an award, IDV, or grant award. | What is the overall award or parent record? |
| Transaction | An action-level event beneath a federal award or IDV. | What changed, obligated, corrected, or modified value over time? |
| Obligation | Money the government has committed or de-obligated. | How much has been committed so far? |
| Potential value | A ceiling, base-and-options amount, or estimated limit. | How large could this contract or vehicle become? |
| Transaction value split | Federal and non-federal portions of a transaction value. | What part of this transaction is federal versus non-federal? |

## Which field or type should I use?

| Question | Start with | Why |
| --- | --- | --- |
| How much has the government committed on an award or grant? | `dollars_obligated` on award-level records. | This is the summarized obligation signal GovTribe exposes on award records when available. |
| What happened on a specific modification or spending action? | [Federal transaction](https://govtribe.com/docs/data-model/data-types/federal-transaction) records. | Transactions are action-level records and can show dates, modification numbers, reasons, and value splits. |
| What is the maximum potential size of a federal contract award or IDV? | `ceiling_value` on federal contract award or IDV records. | Ceiling value is a potential or maximum value, not the same as dollars obligated. |
| What is the total value reported on one transaction row? | `total_value` on federal transaction records. | This is transaction-level value, not an award-level ceiling. |
| How much of a transaction value is federal versus non-federal? | `federal_value` and `non_federal_value` on federal transaction records. | These split transaction value into federal and non-federal portions when the source reports them. |

## GovTribe field mapping

| GovTribe field or data type | Meaning | Related attribute or data type |
| --- | --- | --- |
| `dollars_obligated` | Reported obligation amount on federal award-style records. | [Dollars obligated](https://govtribe.com/docs/data-model/attributes/dollars-obligated-attribute) |
| `ceiling_value` | Potential maximum value on federal contract award and IDV records. | [Ceiling value](https://govtribe.com/docs/data-model/attributes/ceiling-value-attribute) |
| `total_value` | Transaction-level total value. | [Total value](https://govtribe.com/docs/data-model/attributes/total-value-attribute) |
| `federal_value` | Federal portion of a transaction value. | [Federal value](https://govtribe.com/docs/data-model/attributes/federal-value-attribute) |
| `non_federal_value` | Non-federal portion of a transaction value. | [Non-federal value](https://govtribe.com/docs/data-model/attributes/non-federal-value-attribute) |
| Federal transaction | Action-level contract or assistance transaction. | [Federal transaction](https://govtribe.com/docs/data-model/data-types/federal-transaction) |

## Transaction search amount and date basis

[Search federal transactions](https://govtribe.com/docs/govtribe-for-agents/tools/search-federal-transactions-mcp-tool) includes five families. Its statistics and dollar leaderboards sum signed `total_value` in USD; dollar sorting uses `federalValue`. `total_value` combines the reported federal and non-federal portions. It is not necessarily federal-only spending.

| Family | Amount basis | Date basis in current source processing |
| --- | --- | --- |
| Contract award | Signed action obligation plus reported non-government dollars. | Source date signed. |
| Contract IDV | Signed IDV action obligation plus reported non-government dollars; ceiling values are separate. | Source date signed. |
| Assistance award | Federal action obligation plus reported non-federal funding. | Source action date. |
| Contract subaward | Reported subaward amount. | Source subaward date. |
| Assistance subaward | Reported subaward amount. | Source subaward date. |

Historical stored transaction and effective dates can differ. Search uses the stored transaction date for `transaction_date_range`, the stored effective date for `transaction_effective_date_range`, and the immediate parent's award date for `award_date_range`. A 2022 award's 2025 modification belongs to the 2025 transaction period, not the 2025 award-date cohort. Missing dates cannot match the corresponding range.

Select `contract_award` and `contract_idv` for prime contract activity. The `transactions_by_type` aggregation keeps family counts and amount sums separate. Positive and negative statistics preserve signed values: +$100 and −$20 yield positive $100, negative −$20, and net $80. Zero and absent values enter neither sign group. Net statistics include actual zeros but exclude absent amounts from count and average. Already stored zeros do not reveal whether a source amount was absent.

## How to avoid double counting

- Use award records when the question is about current award-level history or a standard search result.
- Use transaction records when the question requires a time series, modification history, action date, reason for modification, or obligation movement.
- Do not add award-level `dollars_obligated` to transaction-level values for the same award unless you have deliberately designed a reconciliation workflow.
- Treat `ceiling_value` as potential value. It can be much larger than obligated dollars and should not be used as committed spending.
- Treat sub-awards as separately reported downstream activity, not as another transaction layer on the prime award.

## Official source notes

- [USAspending Federal Spending Guide](https://www.usaspending.gov/data/Federal-Spending-Guide.pdf) distinguishes prime awards, sub-awards, prime award transactions, prime award summaries, obligations, and outlays.
- [SAM.gov Contract Award Data](https://sam.gov/contract-data) is the federal contract award source GovTribe uses for contract award and IDV records.
- [FAR 4.601](https://www.acquisition.gov/far/4.601) defines contract actions and contract action reports for FPDS reporting context.
- [FAR 4.605](https://www.acquisition.gov/far/4.605) covers FPDS reporting identifiers and award reporting procedures.

## Related articles

- [Federal contract data model](https://govtribe.com/docs/data-model/guides/federal-contract-data-model): Understand how awards, IDVs, vehicles, transactions, and sub-awards fit together.
- [Federal grant data model](https://govtribe.com/docs/data-model/guides/federal-grant-data-model): Understand how grant opportunities, programs, awards, transactions, and sub-awards fit together.
- [Federal transaction](https://govtribe.com/docs/data-model/data-types/federal-transaction): Review action-level transaction records.
- [Dollars obligated attribute](https://govtribe.com/docs/data-model/attributes/dollars-obligated-attribute): Review the shared obligation value attribute.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
