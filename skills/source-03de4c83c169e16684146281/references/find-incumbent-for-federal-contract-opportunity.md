---
title: Find Incumbent for a Federal Contract Opportunity
description: Recover the exact incumbent contract or strongest defensible incumbent for a federal opportunity using direct procurement lineage before constrained fallback evidence.
---

# Find Incumbent for a Federal Contract Opportunity

Use this reference when the user asks who currently performs the work, asks for the exact incumbent contract or delivery order, or supplies incumbent-research rules that prohibit title-only matching. This is a lineage workflow, not a generic likely-bidder ranking.

## Goal
- Resolve the target opportunity and identify the current performing contract or strongest defensible incumbent using four ordered tiers:
  1. direct notice-thread and linked-record evidence
  2. current child-order recovery
  3. predecessor recovery
  4. tightly constrained fallback
- Return the actual award, task order, delivery order, or other child instrument whenever the evidence supports one.
- Keep lineage explicit. Do not overstate a parent vehicle, generic same-agency award, or solicitation-title similarity as order-level proof.

## Non-negotiable research rules
- Do not rely solely on solicitation title, description similarity, NAICS/PSC overlap, or a vendor's general agency footprint.
- Operate the relevant GovTribe tools when the user asks for exact incumbent tracing; do not answer with an ungrounded hypothesis when searchable records are available.
- Prefer contract, task-order, delivery-order, IDV, opportunity-thread, office, program, site, platform, and period-of-performance identifiers over loose keyword resemblance.
- Distinguish `Confirmed Incumbent`, `Likely Incumbent`, and `Supporting Predecessor Evidence`.
- Preserve the active opportunity context across follow-ups instead of making the user restate the target.

## Workflow

### 1. Resolve the target opportunity exactly
- Use `Search_Federal_Contract_Opportunities` with exact lookup first.
- Reuse `federal_meta_opportunity_id`, notice-chain relationships, agency, awarding office, program, classification, vehicle, site, and scope text.
- Recover attached government-file text when identifiers, incumbent language, transition facts, or predecessor references may be present in the solicitation package.
- If the target does not resolve cleanly enough to one opportunity, ask for the minimum missing detail and stop.

### 2. Tier 1: direct thread evidence
- Use direct dataset linkage first.
- If `federal_meta_opportunity_id` is present, query `Search_Federal_Contract_Awards` with it before broader searches.
- The opportunity row does not expose linked awards or IDVs. Recover them with a second call: `Search_Federal_Contract_Awards` with `federal_contract_opportunity_ids` set to the opportunity `govtribe_id`, and `Search_Federal_Contract_IDVs` with the same value when a parent instrument may be involved. Page through both.
- Reuse predecessor, vehicle, and notice-chain relationships already exposed on the opportunity.
- Inspect exact contract numbers, task-order numbers, delivery-order numbers, incumbent names, and transition statements surfaced in files or records.
- Use a narrow aggregation-only verification pass only when direct thread concentration materially clarifies whether one performer dominates the thread.
- If a linked vehicle or IDV materially clarifies the thread, run one targeted parent lookup, but do not treat parent-instrument context alone as incumbent proof.

### 3. Tier 2: current child-order recovery
- If direct thread evidence does not confirm the incumbent, recover the most defensible current child order or award.
- Build exact quoted office, program, site, platform, system, requirement phrase, and scope variants from the opportunity and source files.
- Run the recovery sequence in order:
  - exact contract/order identifiers and direct lineage fields
  - exact quoted platform, system, office, program, site, or requirement terms
  - the same terms with the strongest same-agency, office, NAICS, PSC, vehicle, set-aside, place, and period-of-performance filters
  - one narrow semantic retry only if the exact and keyword sweeps remain too broad or too thin
- Mine returned award text for exact identifiers and rerun exact lookups immediately when a contract number, IDV number, task-order number, delivery-order number, or child-award reference appears.
- If a candidate award references a parent IDV, expand that lineage before inclusion or exclusion.
- Use the current exact-scope child order or award as the incumbent record when its period of performance and scope support current performance.

### 4. Tier 3: predecessor recovery
- Only after Tier 1 and Tier 2 fail, search for older same-office, same-program, same-site, or same-functional-scope work.
- Prioritize exact office, site, program, branded system, requirement phrase, and contract lineage matches over generic same-agency similarity.
- Use `Search_Federal_Contract_Awards` as the primary predecessor surface and `Search_Federal_Contract_IDVs` when the opportunity language or recovered awards imply a parent instrument.
- If an IDV, parent award, or surfaced identifier is found, expand lineage before reaching a conclusion.
- Treat older exact-scope work as supporting predecessor evidence unless it is still current enough to satisfy Tier 2.

### 5. Tier 4: constrained fallback
- Only after the first three tiers fail, use `similar_filter` from the resolved opportunity with strict same-agency or office, same NAICS or PSC, same vehicle or IDV, same set-aside, place, scope, and recent-window filters.
- Use `search_mode: "semantic"` only inside this fallback tier when the exact and filter-first pass remains too thin.
- Use `Likely Incumbent` only for strong constrained fallback matches.
- Do not widen into open-ended likely-bidder logic.

### 6. Verification and stop conditions
- Exclude keyword-adjacent awards, wrong-scope same-agency work, wrong-office work, wrong-vehicle work, expired unrelated orders, parent-only lineage, and entity-mismatched vendor results.
- Before returning `No Defensible Incumbent`, expand every plausible Tier 2 or Tier 3 lineage lead or explicitly reject it with a reason.
- If the answer depends on Tier 2, Tier 3, or Tier 4 instead of direct thread evidence, say so explicitly.
- If the resolved incumbent is a candidate teaming partner rather than a head-on competitor, use `references/team-on-an-opportunity.md` to coordinate a teaming interest on the recompete.
- If the user asks for a full record dossier after the incumbent is resolved, hand the exact award/order/IDV target to the `govtribe-deep-dive` skill.

## Output contract
- Start with the resolved opportunity and the incumbent call.
- Name the exact current contract/order when supported, including identifier, vendor, parent instrument, scope, period of performance, and evidence tier.
- Then return ordered sections for direct evidence, current child-order recovery, predecessor evidence, supporting lineage, fallback, exclusions, risks, and confidence.
- Use compact markdown tables for each populated evidence section.
- Keep evidence labels explicit:
  - `Confirmed Incumbent`
  - `Likely Incumbent`
  - `Supporting Predecessor Evidence`
  - `Supporting Lineage`
  - `No Defensible Incumbent`
- If order-level incumbency remains unconfirmed, say so clearly instead of centering a parent IDV or vehicle.
