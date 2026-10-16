---
title: Industry-Aware Pricing
description: Progressive-disclosure router for selecting the right economic model, evidence sources, normalization rules, and industry-specific cost drivers in GovTribe pricing workflows.
---

# Industry-Aware Pricing

Use this reference alongside the matching pricing workflow when the opportunity, award, order, source file, pricing context, line-item evidence, or buyer clearly points to an industry. Industry context helps select the economic model and assumptions; evidence determines what is supportable.

## Progressive-disclosure rule

1. Load the task-specific pricing workflow first.
2. Select one primary economic lane below.
3. Load a mission-domain modifier only when it materially changes the cost model.
4. Do not load every industry reference.

For mixed scopes, allocate major cost components to the lane that owns their unit and risk. Do not force one evidence model across the entire procurement.

## Select the primary economic lane

- [Products, Supply, and Equipment](./industry-pricing-products-supply-equipment.md): commodity/COTS, source-controlled items, manufacturing, equipment, MRO, distribution, warehousing, transportation, and logistics pricing.
- [Digital, IT, Cyber, and Data](./industry-pricing-digital-it-cyber.md): SaaS/licensing, cloud consumption, custom software, modernization, managed IT, cyber, data/AI, telecom, and digital pricing units.
- [Professional and Mission-Support Services](./industry-pricing-professional-services.md): labor chains, staffing, productive hours, wages/rates, SCI, staff augmentation, managed services, advisory deliverables, contact centers, and training.
- [Construction, AEC, and Facilities](./industry-pricing-construction-aec-facilities.md): construction, A-E, design-build, facilities O&M, energy projects, unit-price normalization, wages/trades, quotes, materials, schedule, and site risk.
- [Mission-Domain Modifiers](./industry-pricing-mission-domain-modifiers.md): healthcare/life sciences; R&D/scientific; environmental/energy; transportation/aviation/maritime; public safety/emergency response.

A mission modifier supplements the primary economic model. It never replaces it.

## Economic-model classification

Resolve the dominant unit of competition:

- item/unit/lot
- subscription/license/user/transaction
- cloud consumption or usage
- labor-hour/FTE/team
- fixed deliverable or outcome
- construction quantity/takeoff/schedule
- A-E effort/fee
- availability/performance/energy savings
- hybrid allocation across multiple units

## Evidence and normalization discipline

- Separate source-confirmed drivers, user-provided assumptions, modeled assumptions, and checks to verify.
- Label evidence as wage, labor-rate ceiling, awarded line item, SCI footprint, award history, quote, takeoff, or user assumption.
- Normalize unit, scope, quantity, fixed-cost recovery, time, escalation, geography, delivery environment, contract terms, risk, and competition before comparison.
- Label every value basis: wage, cost, bill rate, ceiling rate, unit price, evaluated price, obligation, potential value, or parent ceiling.
- Do not force BLS/GSA labor logic onto a supply buy or line-item logic onto a labor-centric service.
- Keep public planning benchmarks distinct from proprietary indirect rates, supplier quotes, and competitor bid prices.

## Base-workflow preservation

- Preserve the base staffing, PTW, BLS, GSA, line-item, SCI, and pricing-model procedures.
- Use industry context to sharpen cost drivers, evidence preferences, scenario variables, sensitivities, and failure modes.
- When a source is unavailable, state the limitation and use transparent assumptions rather than fabricated precision.
- Hand pursuit implications to `govtribe-capture-workflows` and proposal artifacts to `govtribe-proposal-workflows` while preserving the selected range and assumptions. Use the host's document or spreadsheet capability for the requested artifact, with a complete Markdown or CSV fallback when unavailable.

## Current-rule verification

The solicitation, current wage decision, pricing schedule, quotes, company accounting data, and jurisdiction-specific requirements control. Verify current versions at execution time.
