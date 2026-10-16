---
title: Industry-Aware Capture Workflows
description: Progressive-disclosure router for adding industry-specific gates, evidence fields, risks, and capture questions to task-specific capture workflows.
---

# Industry-Aware Capture Workflows

Use this reference alongside the matching capture workflow when the opportunity, pursuit, source package, buyer context, or user request clearly points to an industry. Industry context sharpens capture questions; retrieved records, source files, and user-confirmed company facts decide what actually applies.

## Progressive-disclosure rule

1. Load the task-specific capture workflow first.
2. Select one primary industry lane below.
3. Load a mission-domain modifier only when it materially changes the pursuit.
4. Do not load every industry reference.

For mixed procurements, choose the lane that drives the hardest gate, largest share of value, or central evaluation logic. Add one secondary lane only when it materially changes eligibility, execution, competition, pricing, or past-performance relevance.

## Select the primary lane

- [Products, Supply, and Equipment](./industry-capture-products-supply-equipment.md): manufacturing, commodities, COTS, source-controlled items, equipment, repair/overhaul, distribution, logistics, and fleet support.
- [Digital, IT, Cyber, and Data](./industry-capture-digital-it-cyber.md): SaaS, cloud, software, modernization, cyber, managed IT, data/AI, telecom, and digital infrastructure.
- [Professional and Mission-Support Services](./industry-capture-professional-services.md): advisory, PMO, human capital, training, staff augmentation, contact center, case processing, and labor-led mission support.
- [Construction, AEC, and Facilities](./industry-capture-construction-aec-facilities.md): construction, architect-engineer, design-build, facilities O&M, infrastructure, public works, energy, and real-property services.
- [Mission-Domain Modifiers](./industry-capture-mission-domain-modifiers.md): healthcare/life sciences; R&D/scientific; environmental/energy; transportation/aviation/maritime; public safety/emergency response.

A mission modifier supplements the primary lane. It never replaces it.

## Classification record

Before applying industry rules, resolve the smallest useful context:

- primary lane and subtype
- material secondary lane
- federal or state/local market and jurisdiction
- acquisition method and access path
- economic model and unit of competition
- performance environment and regulated object

Treat agency, geography, contract type, compliance regime, and asset type as overlays rather than standalone industries.

## Evidence and gate semantics

Keep these states separate:

- `confirmed`: directly supported by the controlling source or user-confirmed company data
- `supported_inference`: reasonable synthesis from retrieved evidence
- `unknown`: material fact not established
- `conflicting`: sources disagree or amendment control is unclear
- `not_applicable`: sourced scope shows the check does not apply

Classify decision-moving conditions as sourced hard gates, operational hard gates, partner-remediable gates, conditional gates, competitive factors, or informational checks. An unknown is not a failure.

## Base-workflow preservation

- Use industry context to add sharper evidence fields, gates, risks, competitor archetypes, past-performance dimensions, and validation actions.
- Preserve the base workflow's bid/no-bid, incumbent, likely-bidder, black-hat, past-performance, PTW, pipeline, and output procedures.
- Do not create unsupported requirements, capabilities, licenses, certifications, inventory, capacity, authorization status, quotes, or performance claims.
- For non-labor-led pursuits, treat the deterministic bid/no-bid engine as a services-weighted indicator and add a supplemental industry gate/economics table rather than inventing FTE inputs.
- Hand primary pricing evidence to `govtribe-pricing-data`; use Capture for P(win), teaming, bid posture, and next actions.
- Use `govtribe-proposal-workflows` when the task becomes a response artifact or proposal-control deliverable.

## Current-rule verification

The solicitation, amendments, incorporated clauses, current regulations, official registries, and jurisdiction-specific rules control. Verify current versions at execution time rather than treating static industry guidance as source-confirmed fact.
