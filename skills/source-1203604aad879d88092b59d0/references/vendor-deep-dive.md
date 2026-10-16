---
title: Vendor Deep Dive
description: Resolve one vendor through exact entity scope, federal and state/local awards, vehicles, pricing context, subcontract posture, grant activity, opportunity fit, and current signals.
---

# Vendor Deep Dive

Use this reference for one resolved company, nonprofit, institution, or other vendor/recipient entity.

## Default procedure

1. **Lock exact entity scope.** Resolve GovTribe ID, UEI/CAGE where available, legal name, DBA/division, address, registration, certifications, and parent/child context. Do not silently roll up affiliates.
2. **Reuse direct relationships.** Start with nested awards, IDVs, vehicles, subawards, grants, categories, and parent links.
3. **Build the federal prime footprint.** Use exact `vendor_ids` for awards and IDVs; summarize obligations, buyers, categories, set-asides, timing, and representative work.
4. **Review vehicles and pricing only when material.** For MAS/FSS instruments, preview direct price lists and use exact `Search_GSA_Labor_Rates` when rate context is requested. When exact file text is necessary, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md) with `Add_To_Vector_Store` and `Search_Vector_Store`; use the host's attachment or spreadsheet capability for material skipped files, or disclose the gap.
5. **Build subcontract and grant views separately.** Do not merge prime awards, subawards, grants, and grant subawards into one performance total.
6. **Add state/local evidence carefully.** Use exact name and geography controls and state when entity matching is less certain.
7. **Assess near-term fit only when requested.** Constrain opportunity/forecast discovery by verified capabilities, buyers, categories, vehicles, geography, and timing.
8. **Use current news selectively.** Prefer government-related events that affect ownership, leadership, protests, vehicles, performance, partnerships, or market access.

## Output contract

Return:

- exact entity scope, registration, certifications, and ownership context
- federal prime, subcontract, grant, and state/local footprints kept separate
- top buyers, categories, vehicles, and representative awards
- pricing or labor-rate context when requested
- requested opportunity fit, recompete, teaming and current-news implications
- confidence, identity or coverage gaps, and the next evidence to retrieve
