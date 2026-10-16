---
title: Federal Contract Opportunity Lifecycle and Linkage Caveats
description: Apply market-research shaping posture to past-deadline RFIs and use precise language when exact opportunity-to-award or IDV linkage returns no records.
---

# Federal Contract Opportunity Lifecycle and Linkage Caveats

Read this alongside [Federal Contract Opportunity Deep Dive](federal-contract-opportunity-deep-dive.md) when lifecycle or exact-linkage interpretation could materially change the answer.

## Past-deadline market-research notices

If the target is an RFI, Sources Sought, Request for Capabilities, draft PWS, or market-research Special Notice whose response deadline has passed and no award or active solicitation supersedes it:

- Do not frame it as an immediate live submission.
- Classify the primary output profile as `market_research_shaping`.
- State that the response window has passed.
- Explain what the government appeared to be testing: capability, capacity, set-aside strategy, vehicle access, commercial availability, pricing structure, acquisition method, or requirement maturity.
- Identify acquisition-path unknowns, likely follow-on notice types, vehicle-access implications, probable vendor pool, and RFQ watch triggers.
- Recommend pre-RFQ shaping actions rather than late response actions.
- Add compact `recompete_planning` or `competitor_partner_stakeholder` modules only when predecessor, vendor-pool, or teaming evidence materially improves the answer.

A past deadline alone does not prove the requirement was canceled, awarded, or abandoned.

## Exact-linkage zero-result language

When an exact `federal_meta_opportunity_id` award or IDV search is valid for the target and returns no records, use language such as:

> No exact linked awards or IDVs were returned for the opportunity's federal meta opportunity ID. Treat this as no defensible predecessor evidence from the exact notice thread, not proof that no related work exists elsewhere in the agency or market.

Then:

- distinguish `no exact linked predecessor` from `no related work`
- state whether the target was MAS-like or otherwise unsuitable for exact FMO-ID linkage
- review direct nested relationships before widening
- use bounded same-office, program, vehicle, site, platform, scope, and period filters before semantic recovery
- label broader results as analogs, likely-bidder signals, or predecessor hypotheses rather than exact linkage
- preserve exclusions and explain why a candidate was not accepted as the predecessor

## File retrieval with MCP

When attached files matter, follow [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md). After `Add_To_Vector_Store` reports the files ready, use `Search_Vector_Store` and cite returned source metadata with the external host's native citation format. If a material spreadsheet or unsupported attachment is skipped, use the host's ordinary attachment or spreadsheet capability; when none is available, disclose the gap and return a labeled partial result or request a supported export if the missing evidence could change the answer.

## Output implications

Keep these statements separate:

- current notice and response status
- exact linked predecessor evidence
- broader related-work evidence
- supported acquisition-path inference
- unresolved gaps and watch triggers

Do not convert the absence of exact linkage into a confident claim that no incumbent, predecessor, vehicle, or related agency work exists.
