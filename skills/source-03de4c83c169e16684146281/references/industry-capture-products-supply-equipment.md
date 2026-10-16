---
title: Industry-Aware Capture: Products, Supply, and Equipment
description: Detailed capture gates, evidence fields, competitor logic, workflow adaptations, and failure modes for products, manufacturing, supply, equipment, and distribution pursuits.
---

# Industry-Aware Capture: Products, Supply, and Equipment

Use alongside the matching capture workflow after the pursuit clearly resolves to this primary lane.

## Activate this lane when

The buyer is primarily acquiring an item, asset, manufactured output, equipment system, replacement part, consumable, vehicle, kit, distribution outcome, or product-led maintenance package. Do not activate it merely because a services contract includes incidental materials.

## Source-confirmed facts to extract

- item description, manufacturer, OEM, brand-name-or-equal language, model, part number, NSN, stock number, drawing/specification, revision, salient characteristics, approved-source or source-control status
- quantity, unit of issue, unit of measure, minimum/maximum order, quantity breaks, substitutions, alternates, options, and estimated demand
- destination, delivery schedule, required delivery date, shipment terms, FOB point, routing, consignee, installation site, staging, and acceptance location
- inspection, acceptance, first article, testing, certificate of conformance, traceability, calibration, quality system, lot/date/serial controls, shelf life, warranty, and nonconformance obligations
- preservation, packaging, packing, marking, labeling, RFID/barcode, hazardous-material, export, temperature-control, and chain-of-custody requirements
- country-of-origin, domestic-preference, trade-agreement, specialty-material, prohibited-source, supply-chain security, and counterfeit-avoidance provisions that are actually incorporated
- installation, commissioning, training, manuals, spares, consumables, field service, maintenance, repair, overhaul, uptime, and service-network requirements
- set-aside, nonmanufacturer-rule, waiver, manufacturer/processor status, authorized channel, and workshare facts
- pricing structure, payment timing, inventory financing, progress or milestone payments, liquidated damages, warranty reserve, and contract term

## Gate table

| Check | Gate posture | Evidence needed |
|---|---|---|
| Exact item/source eligibility | Hard only when source controls the item or approved source | Solicitation/specification, approved-source evidence, OEM/channel documentation |
| Equivalent/substitute acceptability | Conditional | Brand-name-or-equal criteria, deviation/alternate process, technical comparison |
| Delivery feasibility | Hard when the date cannot be met | Inventory/production plan, supplier confirmation, freight path, inspection lead time |
| Technical data and revision access | Hard for build-to-print or controlled items | Current drawings/specs, license/data access, configuration control |
| Quality/test/traceability | Hard when contractually required | QA system, test facility/partner, traceability process, certificates |
| Domestic or prohibited-source compliance | Hard when incorporated | Bill of material/source map, country-of-origin evidence, supplier attestations |
| Small-business supply eligibility | Hard when set aside and applicable | Manufacturer/nonmanufacturer analysis, waiver status, source plan |
| Packaging/marking/hazmat | Conditional but often schedule-critical | Packaging code/spec, hazmat capability, labeling and shipping process |
| Working capital and price validity | Operational/competitive | Supplier payment terms, quote validity, inventory exposure, cash-cycle model |
| Warranty/field support | Conditional | Service footprint, response model, spares, warranty reserve |

## Fit and past-performance dimensions

Score relevance on the dimensions the requirement actually values:

- exact item, platform, equipment family, or technical specification
- OEM/authorized-channel relationship and source-control experience
- quantity, throughput, production complexity, delivery cadence, and surge
- inspection/test regime, traceability, quality escapes, on-time delivery, and warranty outcomes
- buyer, destination type, deployed environment, facility, fleet, or mission
- role as manufacturer, value-added reseller, distributor, integrator, repair provider, logistics provider, or subcontractor
- packaging, hazardous, cold-chain, secure-chain, or specialized transportation experience
- dollar scale, working-capital burden, contract structure, and geographic/service network

A broad NAICS match with no item, platform, delivery, or quality similarity is weak evidence.

## Competitor and incumbent analysis

Build the likely-bidder cohort in this order:

1. Exact NSN, part number, model, OEM, item description, or prior solicitation identifier.
2. Approved sources, manufacturers, authorized resellers, and known channel partners.
3. Vendors with recent same-buyer or same-equipment-family awards.
4. Distributors, integrators, repair stations, logistics firms, and local dealers that match the operating model.
5. Broader PSC/FSC, NAICS, NIGP, or UNSPSC peers only after exact lanes are exhausted.

Distinguish:

- OEM/manufacturer advantage
- exclusive or constrained distribution
- incumbent inventory and forecast knowledge
- local service or dealer footprint
- existing vehicle/cooperative access
- buyer preference for direct OEM, small distributor, or systems integrator
- fragmented incumbency across products, regions, depots, or task orders

## Workflow adaptations

- **Relevant opportunities:** rank on item/source match, delivery feasibility, quality burden, geography, access path, and working-capital fit. Available FTE should not drive product-only ranking.
- **Bid/no-bid:** make item/source eligibility, delivery, QA, domestic-source, nonmanufacturer, and cash exposure explicit. Use "BID_WITH_PARTNER" where an authorized supplier, manufacturer, test house, installer, or logistics partner closes the path lawfully.
- **Past performance:** select examples with item/platform and delivery/quality similarity, not generic revenue.
- **Likely bidders/black hat:** evaluate source control, price leverage, inventory, channel, quality record, and delivery certainty. For low-price responsive buys, do not invent a narrative-heavy tradeoff.
- **Incumbent:** search predecessor item awards and recurring orders; a prior equipment supplier may differ from the maintenance incumbent.
- **PTW handoff:** pass exact item identity, quantity/UOM, delivery terms, source restrictions, quote date, packaging, freight, warranty, and comparable-award context. Do not send a product buy to a labor-rate-only model.
- **Pipeline:** tag `commodity`, `controlled_part`, `manufacturing`, `equipment`, `MRO`, `distribution`, or another resolved subtype and record the decisive supply validation.

## State/local considerations

- Use `Search_Line_Items` only for awarded state/local line-item evidence and only when description, quantity, UOM, parent contract, geography, and delivery context are comparable.
- Check local/reciprocal product preferences, dealer or service-location requirements, mandatory statewide contracts, cooperative participation, recycled/sustainable product preferences, bidder registration, tax treatment, and public-works installation rules in the source jurisdiction.
- A cooperative master agreement does not prove that every entity can or will use it; verify participating addenda, eligible users, local competition requirements, and scope.

## Common failure modes

- Treating an award total as a unit price.
- Treating an OEM name in a description as proof of an approved source or reseller relationship.
- Assuming equal items are acceptable without matching every salient characteristic.
- Ignoring packaging, inspection, first-article, or delivery lead time in the margin model.
- Using zero FTE as a no-bid reason for an inventory- or manufacturing-led pursuit.
- Comparing line items with different UOMs, quantities, option content, freight terms, or service bundles.
