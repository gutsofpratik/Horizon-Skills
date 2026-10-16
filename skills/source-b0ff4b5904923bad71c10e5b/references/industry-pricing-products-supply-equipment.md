---
title: Industry-Aware Pricing: Products, Supply, and Equipment
description: Detailed pricing architectures, subtypes, inputs, evidence use, scenarios, sensitivities, and failure modes for products, manufacturing, supply, equipment, distribution, repair, and logistics.
---

# Industry-Aware Pricing: Products, Supply, and Equipment

Use alongside the matching pricing workflow after the economic model clearly resolves to this primary lane.

## Pricing architecture

Build the model at the source-required unit. A generic unit build may include:

`acquisition/manufacturing cost`
`+ inbound freight and receiving`
`+ inspection, testing, traceability, and quality`
`+ preservation, packaging, packing, marking, and hazardous handling`
`+ outbound freight, fuel, accessorials, and delivery`
`+ installation, commissioning, training, documentation, and spares`
`+ warranty/returns/field-service reserve`
`+ financing, inventory, obsolescence, and lead-time exposure`
`+ allocated indirect cost`
`+ fee/profit`

Do not use this list as a fixed formula. Include only source-relevant and company-approved cost pools, and avoid double counting.

## Resolve the subtype

### Commodity/COTS/catalog

Pricing drivers:

- manufacturer/distributor cost, quantity break, catalog/list price, discount, minimum order, pack quantity, freight, tax, warranty, and price validity
- competition, equivalent products, channel structure, cooperative/vehicle discounts, and buyer volume

Evidence:

- strong state/local line items when unit/quantity/product/context match
- current supplier/catalog quote supplied externally
- same-item award history as a value signal

### Controlled-source/OEM/NSN/part-number

Pricing drivers:

- exact item/revision, approved source, scarcity, source approval, production lot, tooling, first article, test, traceability, counterfeit controls, minimum buy, shelf life, and lead time
- single/limited-source leverage and obsolete/long-lead risk

Evidence:

- exact identifier and current quote are far stronger than broad category averages
- federal award totals are not unit prices
- do not assume an incumbent's price reflects current source or quantity conditions

### Manufacturing/fabrication/kitting

Pricing drivers:

- bill of material, yield/scrap, setup/tooling, machine/labor cycle, production rate, lot size, quality/testing, special processes, packaging, and nonrecurring engineering
- capacity, make/buy, supplier risk, configuration changes, learning curve, and schedule

Required external inputs:

- BOM/quotes, routings, labor standards, yield, tooling, equipment, QA/test, and company indirects

GovTribe can provide buyer/award context but not a defensible manufacturing cost estimate without these inputs.

### Equipment/capital asset/vehicle

Pricing drivers:

- base configuration, options/accessories, delivery, installation, site preparation, commissioning, training, manuals, spares, warranty, preventive maintenance, uptime, software/licenses, telematics, and lifecycle support
- purchase vs lease, residual, financing, replacement cycle, and service network

Normalize total cost of ownership separately from acquisition price when the source evaluates lifecycle cost.

### Repair/overhaul/calibration/MRO

Pricing drivers:

- incoming condition, inspection/teardown, repair category, parts, labor, test, calibration, no-fault-found, beyond-economical-repair, exchange pool, turnaround, warranty, and shipping
- fixed price by repair level, time-and-materials, not-to-exceed, or catalog schedule

Use condition scenarios if the source does not define the mix.

### Distribution/warehousing/transportation

Pricing drivers:

- receipts, storage positions/cube, pick/pack, orders/lines, throughput, inventory accuracy, facilities, systems, labor, fuel, freight, accessorials, routes, stops, distance, weight/volume, claims, and surge
- pass-through vs at-risk transportation, minimum volume, and fixed-facility recovery

## Source-confirmed inputs to extract

- exact description/part/model/NSN/specification/revision
- quantity, UOM, estimated/min/max volume, pack size, options, destination, and schedule
- source approval/equivalent rules, quality/test/inspection, traceability, packaging, origin, and warranty
- freight terms, FOB point, installation/site, service/training, acceptance, and payment
- price schedule, quantity breaks, catalog/discount formula, escalation/EPA, options, and quote validity

## Evidence use

- Use `Search_Line_Items` for awarded state/local item/unit evidence only.
- Require matching UOM and inspect quantity and parent award context.
- Use exact item identifiers in award searches, but describe federal award values as award-level analogs unless unit detail is independently available.
- Use BLS/GSA/SCI only for material service components such as installation, repair labor, warehousing, help desk, or field support—not as the product price.

## Scenarios and sensitivities

Test:

- quantity/volume band
- supplier cost and quote expiration
- freight/fuel/accessorials
- lead time and expedited delivery
- packaging/quality/first-article burden
- warranty/returns
- inventory financing and payment timing
- option-year escalation
- foreign exchange/tariff/origin risk when applicable

## Failure modes

- Dividing total award value by an estimated quantity without source support.
- Comparing different pack sizes or units.
- Ignoring freight, packaging, inspection, warranty, or installation.
- Using a stale catalog or distributor quote without validity and availability.
- Treating zero inventory or unknown lead time as a price of zero.
- Applying labor-rate benchmarks to a product-only CLIN.
