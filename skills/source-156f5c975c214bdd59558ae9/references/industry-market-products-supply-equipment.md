---
title: Industry-Aware Market Intelligence: Products, Supply, and Equipment
description: Detailed segmentation, identifier hierarchy, federal and state/local lanes, competitor archetypes, signals, recompete logic, monitor triggers, and contamination controls for product and supply markets.
---

# Industry-Aware Market Intelligence: Products, Supply, and Equipment

Use alongside the matching market-intelligence workflow after the market clearly resolves to this primary lane.

## Market segmentation

Do not treat all “supplies” as one market. Separate at least:

- catalog commodity or consumable
- source-controlled/OEM/approved-source item
- custom manufactured or fabricated item
- capital equipment or vehicle
- medical/laboratory/specialized regulated equipment
- repairable, MRO, calibration, overhaul, or depot support
- distribution, warehousing, kitting, fulfillment, or transportation
- equipment plus installation, training, warranty, and maintenance

## Identifier hierarchy

Prefer the most discriminating identifiers available:

1. exact NSN, part number, model, manufacturer, item number, drawing, specification, contract number, or solicitation number
2. item family, platform, vehicle/equipment family, system, end item, or installed base
3. buyer-specific nomenclature and functional description
4. PSC/FSC, NAICS, NIGP, UNSPSC, commodity code, or catalog category
5. broad product keywords

Use codes to expand recall, not to prove exact product identity. Validate with descriptions, line items, files, specifications, or summaries.

## Federal market lanes

Search separately where relevant:

- DLA and DoD supply/repair activity by NSN, part, weapon/platform, source, depot, and sustainment language
- GSA/Schedule and other catalog or channel-based buying
- VA and civilian medical, laboratory, facilities, fleet, and commodity buying
- agency-specific equipment programs and installed-base support
- maintenance, repair, overhaul, calibration, and field service as distinct from new equipment
- warehousing, distribution, freight, and logistics services as distinct from the item itself

Market questions:

- Is demand recurring replenishment, episodic replacement, project-based acquisition, or lifecycle sustainment?
- Is the market open to distributors/resellers, limited to manufacturers/approved sources, or dependent on technical data?
- Does the buyer aggregate demand through an IDV/vehicle or issue repeated standalone awards?
- Are quantities and delivery locations concentrated or dispersed?
- Do historic awards bundle installation, training, warranty, maintenance, spares, or logistics?
- Is the real competitor field manufacturers, authorized channels, broadline distributors, small-business resellers, repair providers, or integrators?

## State and local market lanes

Common structures include:

- statewide term contracts and catalogs
- cooperative contracts and piggyback purchasing
- school, higher-education, healthcare, corrections, public-safety, fleet, transit, utility, and public-works buying
- local bid schedules, annual requirements, blanket orders, and spot buys
- equipment replacement programs funded through operating budgets, capital plans, bonds, or grants
- dealer/reseller networks and geographic service territories

Use `Search_Line_Items` when comparable awarded state/local line items exist. Preserve UOM, quantity, brand/model, bundle, geography, term, and parent context.

## Competitor archetypes

Classify candidates as:

- OEM/manufacturer
- approved/qualified source
- authorized distributor/reseller/dealer
- broadline commodity distributor
- specialty product supplier
- custom manufacturer/fabricator
- repair/MRO/calibration provider
- logistics/fulfillment integrator
- equipment-plus-service integrator
- incumbent with installed-base or warranty advantage

Do not assign an archetype without evidence. A vendor winning a product award is not automatically the OEM or authorized source.

## Early signals

Prioritize:

- forecast or notice language tied to exact item/platform/equipment family
- installed-base sustainment, obsolescence, end-of-life, replacement, refresh, recall, or safety notice
- capital budget, fleet replacement plan, bond, grant award, facility opening, or program expansion
- RFI/source-approval/qualification activity
- expiring catalog, statewide, cooperative, IDV, maintenance, or warranty arrangement
- recurring annual/seasonal buying cadence
- inventory replenishment, surge, disaster stockpile, or supply-chain resilience initiative
- repair backlog, depot workload, maintenance cycle, calibration interval, or fleet mileage/age trigger

## Recompete and renewal signals

Strong signals include:

- repeated buys of the same item family from the same buyer
- expiring requirement or ordering period with continuing installed base
- service/warranty/calibration term ending while equipment remains in use
- successor model, obsolescence, or manufacturer end-of-support
- vehicle or catalog refresh
- recurring school/fiscal-year, seasonal, fleet, or stock replenishment
- phased facility, transit, public-safety, or medical-equipment replacement

Reduce confidence when:

- the item was a one-time project component
- the asset/program was retired
- the record is a final closeout or disposal
- the source is controlled and no alternate path is visible
- the buyer shifted to a mandatory statewide/cooperative channel

## Monitor triggers

- exact NSN/part/model/item-family notice
- buyer plus item-family award or solicitation
- approved-source, qualification, source-sought, or technical-data notice
- vehicle/catalog renewal or vendor addition
- line-item price/quantity change for a comparable item
- fleet/equipment replacement plan or budget action
- new facility/program creating equipment demand
- warranty, maintenance, repair, calibration, or overhaul term approaching end
- OEM acquisition, channel change, discontinuation, recall, or end-of-life evidence from an authoritative source

## Common contamination and failure modes

- searching a generic item word that also appears incidentally in construction or service contracts
- mixing new product sales with repair, lease, rental, and maintenance
- treating a part-family match as exact interchangeability
- mixing each/case/box/kit/lot units
- treating a catalog or vehicle ceiling as product demand
- inferring source approval or channel authorization from an award name
- assuming an awardee manufactured the product
- treating a capital purchase as recurring annual demand
- using state/local line items as federal unit-price evidence
