---
title: Federal Contract Opportunity Deep Dive
description: Resolve one federal contract opportunity through lifecycle, notice-chain, source-file, exact-linkage, predecessor, vehicle, and shaping context without overstating weak relationships.
---

# Federal Contract Opportunity Deep Dive

Use this reference when the user wants more than the target opportunity row and the answer depends on notice history, attached files, exact award-side linkage, predecessor evidence, vehicle context, or follow-on shaping.

## Goal

- Resolve the exact opportunity and its current lifecycle posture.
- Recover the most relevant notice-chain and source-file context.
- Prefer exact relationships before semantic expansion.
- Distinguish current actionability, market-research shaping, predecessor evidence, analog evidence, and unresolved gaps.
- Stop when the answer is decision-useful rather than returning a raw data dump.

Read [Federal Contract Opportunity Lifecycle and Linkage Caveats](federal-contract-opportunity-lifecycle-and-linkage-caveats.md) whenever the target is a past-deadline RFI/Sources Sought notice or exact opportunity-to-award linkage returns no records.

## 1. Read and lock the target

Capture the fields needed to resolve identity, lifecycle, scope, and direct relationships:

- `govtribe_id`, `govtribe_url`, `solicitation_number`, `name`
- `opportunity_type`, `opportunity_state`, `part_of_mas`
- `posted_date`, `due_date`, `award_date`, `updated_at`
- `set_aside_type`, `descriptions`, `place_of_performance`
- `federal_meta_opportunity_id`
- `federal_agency`, `federal_contract_vehicle`
- `naics_category`, `psc_category`
- `government_files`, `points_of_contact`

If the target is not already in context, fetch it by exact GovTribe ID, exact solicitation number, or exact GovTribe URL. If more than one defensible target remains, ask one bounded clarification.

## 2. Classify lifecycle before analysis

Use current date, notice type, status, due date, award date, and later notice-chain events.

### Active response or pursuit

Use a live-pursuit posture when the response window or current action window is still open.

### Past-deadline market research

If the target is an RFI, Sources Sought, Request for Capabilities, draft PWS, or market-research Special Notice whose response deadline has passed and no award or active solicitation supersedes it:

- classify the primary profile as `market_research_shaping`
- state that the response window has passed
- explain what the government appeared to be testing
- identify acquisition-path, set-aside, vehicle, and vendor-pool unknowns
- recommend RFQ watch and pre-solicitation shaping actions rather than late submission activity

A past deadline alone does not prove cancellation, award, or abandonment.

### Recompete or predecessor planning

Use recompete-planning posture when award, incumbent, predecessor, expiring vehicle, or follow-on evidence materially supports it. Do not force a full recompete narrative onto a market-research notice with no predecessor evidence.

## 3. Load notice-chain context

When `part_of_mas` is not true and `federal_meta_opportunity_id` is present:

- fetch the oldest notice for original scope and attachments
- fetch the newest viable notice for current status
- compare due dates, notice types, set-aside, scope, vehicle references, attachments, and amendments

Useful viable notice types include Solicitation, Pre-Solicitation, Sources Sought, Special Notice, and other source-confirmed follow-on notice types relevant to the thread.

### MAS caveat

For MAS opportunities, do not treat `federal_meta_opportunity_id` as an opportunity-specific thread key. A MAS-level key can pull unrelated notices, awards, and files. Prefer direct target relationships, exact vehicle context, attached files, identifiers, and bounded searches.

If `federal_meta_opportunity_id` is absent, skip exact-thread chaining and rely on direct target fields plus bounded recovery.

## 4. Reuse direct relationships before fan-out

Use direct nested or related fields before broader searches:

- agency and office context
- vehicle
- NAICS and PSC
- place of performance
- contacts
- files

The opportunity row does not carry linked awards or IDVs. Retrieve them with a second call to `Search_Federal_Contract_Awards` or `Search_Federal_Contract_IDVs` using `federal_contract_opportunity_ids`, and page through the results.

Direct relationships outrank semantic similarity for lineage claims.

## 5. Read source files when they change the answer

If attached government files exist and the question depends on solicitation detail:

1. Follow the bundled [Vector-store content retrieval](govtribe-docs-vector-store-content-retrieval.md) guidance; call `Documentation` when current schemas or response fields matter.
2. Stage the smallest useful source set with `Add_To_Vector_Store`.
3. Wait until the requested files are ready.
4. Use `Search_Vector_Store` with focused questions and cite returned source metadata using the external host's native citation format.
5. If a material spreadsheet or unsupported attachment is skipped, use the host's ordinary attachment or spreadsheet capability. If none is available, disclose the gap and return a labeled partial result or request a supported export when the missing evidence could change the answer.

Prioritize focused questions about:

- scope and SOW/PWS/SOO requirements
- RFI or Sources Sought questions
- Section L and Section M
- CLINs and pricing instructions
- amendments and deadline changes
- security, cyber, clearance, facility, or compliance requirements
- submission method, forms, page limits, and format rules
- acquisition strategy, vehicle, set-aside, and market-research purpose

Do not stage files when metadata or existing snippets already answer the question.

## 6. Run exact award-side linkage first

When `part_of_mas` is not true and the exact `federal_meta_opportunity_id` is valid, use it before semantic recovery on:

- `Search_Federal_Contract_Awards`
- `Search_Federal_Contract_IDVs`
- `Search_Federal_Contract_Vehicles` when supported and material

Keep fields and result counts bounded. Use this pass to test:

- exact predecessor or incumbent award linkage
- exact parent IDV linkage
- exact vehicle linkage
- current or prior performer evidence

Retrieve the target's awards and IDVs with `federal_contract_opportunity_ids` before falling back to semantic or notice-chain searches. This exact-linkage call also works for MAS opportunities, where `federal_meta_opportunity_id` is not a clean opportunity-specific key.

### When exact linkage returns zero

Use this language or its equivalent:

> No exact linked awards or IDVs were returned for the opportunity's federal meta opportunity ID. Treat this as no defensible predecessor evidence from the exact notice thread, not proof that no related work exists elsewhere in the agency or market.

Then label the exact-linkage result separately from any broader same-office, same-program, same-vehicle, or semantic evidence.

## 7. Recover predecessor and analog context carefully

Only after direct and exact linkage:

1. search exact contract, order, program, platform, site, office, vehicle, and requirement identifiers found in the target or files
2. constrain by agency/office, NAICS/PSC, vehicle, set-aside, place, and period of performance
3. expand candidate parent-child lineage before accepting or rejecting it
4. use one bounded semantic or `similar_filter` pass when exact and filter-first recovery remains thin

Classify results as:

- `Exact linked predecessor`
- `Likely predecessor`
- `Supporting predecessor evidence`
- `Related analog`
- `Likely-bidder or vendor-pool signal`
- `Excluded candidate`

Do not use title similarity, general agency footprint, or a parent vehicle alone as order-level predecessor proof.

## 8. Add vehicle, vendor, contact, and pricing branches only when material

- Expand a vehicle or IDV when it changes access, ordering mechanics, holder ecosystem, predecessor lineage, or recompete posture.
- Expand vendors when incumbent, likely bidder, partner, or vendor-pool context is requested.
- Expand contacts when buyer access, RFI follow-up, or shaping actions are requested.
- Use `govtribe-pricing-data` when the question becomes broader staffing, rate, FTE, wrap, line-item, SCI, or PTW analysis.
- Use `govtribe-capture-workflows` when the user asks for company fit, past performance, competitors, partners, or pursuit posture.

## Output contract

Return a concise, evidence-led package:

1. **Target and current lifecycle** - exact record, notice type, status, dates, and whether the posture is live pursuit, market-research shaping, or recompete planning.
2. **Notice-chain read** - oldest, target, newest controlling or viable notice, and material changes.
3. **Source-file findings** - only the requirements, questions, or constraints that change the decision.
4. **Exact linkage** - linked awards, IDVs, vehicles, or an explicit zero-result caveat.
5. **Predecessor and analog evidence** - clearly labeled confidence and exclusions.
6. **Buyer, vehicle, vendor, and stakeholder implications** - only when material.
7. **Recommended actions and watch triggers** - aligned to the lifecycle posture.
8. **Risks, unknowns, and evidence gaps**.

For past-deadline market research, include what the government was testing, response-gap areas, likely follow-on path, vehicle implications, probable vendor pool, shaping themes, and RFQ watch triggers.

## Stop conditions

Stop expanding when:

- the opportunity and lifecycle are resolved
- the controlling notice and material files are understood
- exact linkage has been tested
- the strongest predecessor or analog evidence is labeled
- remaining branches are weak, duplicative, or do not change the recommendation

## Failure modes

- Treating a past RFI or Sources Sought response deadline as an active submission deadline.
- Treating no exact linked award as proof no related work exists.
- Using MAS-level FMO linkage as an exact opportunity thread.
- Presenting semantic analogs as exact predecessors.
- Using a parent IDV or vehicle as order-level incumbent proof.
- Repeating broad agency history that does not change the target-specific answer.
- Exposing raw internal source labels instead of human-readable evidence IDs and proper chat citations.
