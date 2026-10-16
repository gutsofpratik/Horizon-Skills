---
title: Federal Contract Award Deep Dive
description: Resolve one federal contract award through its parent instrument, transactions, vendor, buyer, originating opportunity, and recompete implications.
---

# Federal Contract Award Deep Dive

Use this reference for one resolved federal contract award when the answer needs more than the award row.

## Default procedure

1. **Lock the award.** Resolve the exact GovTribe ID or contract/order number and capture award type, dates, value fields, description, buyer, awardee, place of performance, NAICS/PSC, and direct relationships.
2. **Classify the value basis.** Keep obligated amount, current value, potential value, and parent ceiling separate.
3. **Follow the instrument chain.** Expand the parent IDV and vehicle when they change ordering mechanics, access, ceiling interpretation, or recompete posture.
4. **Read transactions.** Use transactions to explain obligation timing, modifications, option exercise, deobligations, and funding cadence. Do not sum fields that represent the same action twice.
5. **Resolve the performer.** Use the direct awardee relationship first. Expand parent/child vendor scope only when the user requests family-level analysis.
6. **Recover the originating opportunity.** Prefer exact linked notices and direct identifiers. Treat similar opportunities as analogs, not proof of lineage.
7. **Read files only when material.** Follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md): preview with `Search_Government_Files`, then use `Add_To_Vector_Store` and `Search_Vector_Store` when exact scope, CLIN, amendment, or ordering language changes the answer. Cite returned source metadata with the host's native citation format and disclose any unsupported-file gap.
8. **Add bounded context.** Expand related orders, subawards, competitors, pricing, or news only to close a named decision gap.

## Evidence priorities

- Exact award and transaction records
- Direct parent IDV or vehicle relationships
- Exact linked opportunity or solicitation identifiers
- Awardee and agency relationships
- Source files tied to the award family
- Constrained same-office, same-vehicle, or same-scope analogs

## Output contract

Return:

- award identity, scope, status, period, buyer, performer, and value basis
- parent IDV/vehicle lineage and ordering implications
- obligation and modification timeline
- originating-notice evidence and confidence
- incumbent, recompete, pricing, or teaming implications requested by the user
- material unknowns and the next evidence to retrieve

## Gotchas

- A parent ceiling is not the value of this award or order.
- Obligations are not revenue, backlog, or total contract value.
- The current awardee is not automatically the future incumbent if scope or ordering structure changed.
- A related title or same-agency award is not exact predecessor evidence.
- Stop when added records no longer change the award interpretation or recommendation.
