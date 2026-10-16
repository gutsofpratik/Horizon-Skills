---
title: Federal Contract IDV Deep Dive
description: Resolve one federal IDV through its vehicle, holder, child awards, ordering activity, pricing files, originating opportunity, and recompete or access implications.
---

# Federal Contract IDV Deep Dive

Use this reference for one resolved federal IDV, schedule contract, BPA, BOA, or other indefinite-delivery instrument.

## Default procedure

1. **Lock the IDV.** Capture exact ID, contract number, holder, buyer, type, set-aside, award and ordering dates, value fields, categories, and direct relationships.
2. **Classify the instrument.** Explain whether it is a holder contract, BPA, GWAC/IDIQ child, schedule/FSS contract, or another structure using source fields rather than title alone.
3. **Follow the parent vehicle.** Expand the vehicle only when it changes holder eligibility, ordering scope, shared ceiling, on-ramp, or access interpretation.
4. **Analyze child awards.** Summarize order count, obligations, buyers, categories, timing, and representative orders without treating the parent ceiling as realized demand.
5. **Review the holder.** Keep exact legal-entity scope and distinguish prime holder status from downstream performance.
6. **Inspect pricing context when relevant.** Preview direct `price_lists`; use exact `Search_GSA_Labor_Rates` for MAS/FSS labor-rate questions. When exact file text is needed, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md) with `Add_To_Vector_Store` and `Search_Vector_Store`; use the host's attachment or spreadsheet capability for material skipped files, or disclose the gap.
7. **Recover the originating opportunity.** Prefer exact identifiers and direct relationships; label broader notices as analogs.
8. **Add only decision-relevant branches.** Expand transactions, buyers, competitors, or recompete signals when they affect access, pricing, teaming, or pipeline decisions.

## Output contract

Return:

- instrument identity, type, holder, buyer, dates, and value basis
- parent vehicle and ordering mechanics
- child-order portfolio and concentration
- pricing-file or labor-rate context when requested
- originating-notice evidence
- access, on-ramp, teaming, or recompete implications
- confidence, gaps, and watch triggers

## Gotchas

- Shared or IDV ceiling is not obligated spend or likely order value.
- Holding an IDV does not prove activity, category coverage, or eligibility for every order.
- MAS-level meta-opportunity linkage may be too broad for exact lineage.
- GSA ceiling rates are not task-order winning rates.
- Stop after the child-order and access picture is decision-useful.
