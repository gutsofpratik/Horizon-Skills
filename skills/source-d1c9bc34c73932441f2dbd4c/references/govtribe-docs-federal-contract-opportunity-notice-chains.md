<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Federal contract opportunity notice chains

- Canonical GovTribe Docs page: [https://govtribe.com/docs/data-model/guides/federal-contract-opportunity-notice-chains](https://govtribe.com/docs/data-model/guides/federal-contract-opportunity-notice-chains)

Use this guide when you need to move between a federal contract opportunity, related notices in the same procurement thread, and downstream federal contract awards, IDVs, or vehicles. The key idea is that a single acquisition can appear in SAM.gov as several notice records, and GovTribe may connect those records with a GovTribe-generated notice-chain identifier.

## Quick model

| Concept | Where it appears | How to use it |
| --- | --- | --- |
| `federal_meta_opportunity_id` | Federal contract opportunity records. | Use it to retrieve other opportunity notices in the same GovTribe notice chain. |
| `originating_federal_meta_opportunity_id` | Federal contract awards, federal contract IDVs, and federal contract vehicles. | Use it to move from an awarded or vehicle record back to the related opportunity notice chain. |
| `originating_federal_contract_opportunity` | Federal contract awards, IDVs, and vehicles when GovTribe can resolve a rich relationship. | Use it as the best already-returned source-notice anchor, then use the scalar chain ID when you need the whole chain. |
| Original or oldest notice | The earliest federal contract opportunity GovTribe can connect in the chain. | Use it for early scope, source context, first-posted timing, and original attachments. |
| Newest viable notice | The newest connected notice with opportunity type `Solicitation`, `Pre-Solicitation`, or `Special Notice`. | Use it for the most current actionable notice context when the target is not already the newest viable record. |

`federal_meta_opportunity_id` and `originating_federal_meta_opportunity_id` are GovTribe linking IDs. They are not SAM.gov notice numbers, solicitation numbers, contract numbers, PIIDs, or UEIs.

## Why notice chains exist

SAM.gov can publish related acquisition information as separate opportunity records. Sources-sought notices, pre-solicitations, solicitations, amendments, special notices, award notices, and attached files may not always arrive as one clean parent-child thread from the source.

GovTribe groups related federal contract opportunity notices into a notice chain when source relationships, procurement identifiers, or related source context support that connection. The chain can also connect to downstream awarded records when GovTribe can match the pre-award notice context to federal contract awards, IDVs, or vehicles.

Treat a notice chain as a strong retrieval path, not as a guarantee that every record in the chain has the same scope, status, attachments, or response deadline. Always compare the specific notices that matter for the task.

## How GovTribe maintains the chain

GovTribe builds and refreshes notice chains from source identifiers and related opportunity context. When a federal contract opportunity has a usable federal solicitation number or other procurement identifier, GovTribe can use that identifier to find or create the notice chain. When SAM.gov-related opportunity IDs point to records that were previously separated, GovTribe can merge the chains and update related records to use the surviving chain.

After a chain is updated, GovTribe can also update downstream records that match the same procurement or spend identifiers. That is how an award, IDV, or vehicle can receive `originating_federal_meta_opportunity_id` and later expose `originating_federal_contract_opportunity`.

This means notice-chain links can improve over time as new notices, awards, IDVs, vehicles, or backfilled source records arrive. If an older report or copied answer contains a chain ID, refresh the current GovTribe record before treating that ID as complete.

## Retrieval rules

Use exact chain and relationship fields before semantic search. Semantic similarity is useful after direct identifiers are missing or exhausted, but it should not be treated as proof of lineage.

When using MCP tools, use [Search Federal Contract Opportunities](https://govtribe.com/docs/govtribe-for-agents/tools/search-federal-contract-opportunities-mcp-tool) for the examples below.

| Starting record | First retrieval path | What to inspect next |
| --- | --- | --- |
| Federal contract opportunity | Use `federal_meta_opportunity_id` with `Search_Federal_Contract_Opportunities` to retrieve the notice chain. | Compare the target, original or oldest notice, newest viable notice, files, direct awards, direct IDVs, and vehicle context. |
| Federal contract award | Use `originating_federal_meta_opportunity_id` with `Search_Federal_Contract_Opportunities`. | Review `originating_federal_contract_opportunity`, then retrieve original and newest viable notices if the chain ID is available. |
| Federal contract IDV | Use `originating_federal_meta_opportunity_id` with `Search_Federal_Contract_Opportunities`. | Review source solicitation context, then inspect task orders, child IDVs, parent vehicle, and price-list files when relevant. |
| Federal contract vehicle | Use `originating_federal_meta_opportunity_id` with `Search_Federal_Contract_Opportunities`. | Review source vehicle solicitation context, then inspect child IDVs, downstream awards, holders, and vehicle subcategories. |
| Pursuit | Inspect linked federal contract opportunities first. | For each linked opportunity, retrieve its chain and de-duplicate original and newest viable notices across all linked opportunities. |

When the target already includes nested relationships such as `federal_contract_vehicle` or `originating_federal_contract_opportunity`, use those direct relationships before launching broader searches.

Award-side outcomes are not nested on the opportunity. Retrieve them with a second call: use `Search_Federal_Contract_Awards` or `Search_Federal_Contract_IDVs` with `federal_contract_opportunity_ids` set to the opportunity `govtribe_id` for that one notice, or with `federal_meta_opportunity_ids` when the question covers the whole notice chain.

  When a federal contract opportunity has `part_of_mas` set to `true`, do not treat `federal_meta_opportunity_id` as a clean opportunity-specific notice-chain key. MAS opportunities can share schedule-level context. Prefer direct vehicle context, attached files, and bounded follow-up searches. To keep award-side results tied to the one notice rather than the whole schedule, filter with `federal_contract_opportunity_ids` instead of `federal_meta_opportunity_ids`.

## Federal contract opportunity targets

Start by reading the exact opportunity record. Inspect these fields when they are available:

- `govtribe_id`
- `govtribe_url`
- `solicitation_number`
- `name`
- `opportunity_type`
- `opportunity_state`
- `part_of_mas`
- `posted_date`
- `due_date`
- `descriptions`
- `federal_meta_opportunity_id`
- `federal_contract_vehicle`
- `federal_agency`
- `government_files`

The opportunity record does not carry its awards or IDVs. Retrieve them with a second call to `Search_Federal_Contract_Awards` or `Search_Federal_Contract_IDVs` using `federal_contract_opportunity_ids`.

If `part_of_mas` is not true and `federal_meta_opportunity_id` is present, use that ID to retrieve other federal contract opportunities in the same chain. Sort or compare by `posted_date` to identify the oldest notice and the newest viable notice.

Use the oldest notice to recover early scope and first-posted context. Use the newest viable notice to understand the most current actionable notice in the thread. Use the target notice when the user's question is specifically about the page or record they selected, even if a newer viable notice exists.

Do not assume the latest notice contains every useful detail. Critical attachments, contacts, requirements, or agency language can appear only on an earlier notice.

## Award, IDV, and vehicle targets

Federal contract awards, IDVs, and vehicles can point back to a source notice chain through `originating_federal_meta_opportunity_id`. They can also expose `originating_federal_contract_opportunity` as a nested relationship when GovTribe can resolve a useful federal contract opportunity from the chain.

When starting from an award, IDV, or vehicle:

1. Read the target record and keep its direct relationships in context.
2. If `originating_federal_contract_opportunity` is present, inspect it before making another search call.
3. If `originating_federal_meta_opportunity_id` is present, use it with `Search_Federal_Contract_Opportunities` to retrieve the broader notice chain.
4. Compare the target's award-side facts against the original and newest viable opportunity notices.
5. Use files, descriptions, dates, agency context, vendors, vehicle context, and contract numbers to explain gaps or changes.

Use the originating opportunity to understand solicitation context, not to replace the award, IDV, or vehicle record. The downstream record remains the source for awarded value, awardee or holder, contract number, ordering window, transactions, and parent contract structure.

## Pursuit targets

A pursuit can be linked to one or more federal contract opportunities. When a pursuit is the target, retrieve notice-chain context from the linked opportunities rather than assuming the pursuit itself is the source record.

For each linked federal contract opportunity:

1. Read the linked opportunity's `federal_meta_opportunity_id` and `part_of_mas`.
2. Skip MAS-style chain expansion unless direct opportunity context clearly supports it.
3. Retrieve the original or oldest and newest viable notices for non-MAS chains.
4. De-duplicate notices across linked opportunities by GovTribe ID.
5. Preserve the pursuit as capture context, but use the opportunity records for source notice facts.

This pattern helps avoid over-weighting one stale linked notice when the pursuit also points to a newer solicitation or a richer original notice.

## When exact linkage is missing

Missing notice-chain fields are not negative evidence. They usually mean GovTribe does not have enough source context to expose that exact link on the record you are holding.

If `federal_meta_opportunity_id` or `originating_federal_meta_opportunity_id` is missing:

- Use exact GovTribe IDs, solicitation numbers, contract numbers, and source URLs first.
- Inspect direct relationships and visible related tabs before broad search.
- Use attached government files when source text matters.
- Use `similar_filter` only after exact identifiers and direct relationships are unavailable or insufficient.
- Label similar records as comparable or possible context, not confirmed members of the same notice chain.

## What to compare across notices

When multiple notices exist in the same chain, compare the fields that can materially change the procurement interpretation:

| Compare | Why it matters |
| --- | --- |
| `opportunity_type` | Sources-sought, pre-solicitation, solicitation, special notice, and award notice types answer different workflow questions. |
| `posted_date`, `due_date`, and `award_date` | Timing can move as the opportunity is amended or awarded. |
| `descriptions` | Scope, submission instructions, and amendment notes can differ between notices. |
| `government_files` | Attachments may be added, replaced, or left behind on an earlier notice. |
| `set_aside_type` | Competition posture can change or be clearer on a later notice. |
| `federal_agency` | Office or agency context can clarify the buyer or posting source. |
| `federal_contract_vehicle` | Vehicle context can determine whether the notice is open-market, schedule-related, or tied to another buying channel. |
| `federal_contract_awards` and `federal_contract_idvs` | Direct links can confirm award-side outcomes without a broader search. |

When records disagree, cite the specific notice or downstream record that supports the fact. Do not collapse the chain into one blended record unless the answer is explicitly summarizing the whole procurement thread.

## Common mistakes to avoid

- Do not use `federal_meta_opportunity_id` as a public source identifier.
- Do not assume a solicitation number should appear directly on every downstream award.
- Do not treat `similar_filter` results as confirmed notice-chain members.
- Do not use a MAS-level chain as exact opportunity lineage when `part_of_mas` is true.
- Do not stop at `originating_federal_contract_opportunity` when the task needs the original notice, newest viable notice, or files from another notice in the chain.
- Do not ignore older notices. The first useful scope description or attachment can be older than the current target.

## Related articles

- [Federal meta opportunity ID attribute](https://govtribe.com/docs/data-model/attributes/federal-meta-opportunity-id-attribute): Review the GovTribe notice-chain identifier on federal contract opportunities.
- [Originating federal meta opportunity ID attribute](https://govtribe.com/docs/data-model/attributes/originating-federal-meta-opportunity-id-attribute): Review the downstream bridge from awards, IDVs, and vehicles back to opportunity chains.
- [Originating federal contract opportunity attribute](https://govtribe.com/docs/data-model/attributes/originating-federal-contract-opportunity-attribute): Review the nested relationship that can return source notice context on award-side records.
- [Source identifiers and record matching](https://govtribe.com/docs/data-model/guides/source-identifiers-and-record-matching): Choose between GovTribe IDs, source identifiers, UEIs, source URLs, and originating-record links.
- [Federal contract record structure](https://govtribe.com/docs/data-model/guides/federal-contract-record-structure): Choose between opportunities, vehicles, IDVs, awards, transactions, and sub-awards.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
