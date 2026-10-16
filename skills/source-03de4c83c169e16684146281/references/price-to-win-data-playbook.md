# Price-to-Win Data Playbook

Use this reference when a PTW workflow needs grounded GovTribe retrieval. The exact helper combination may vary, but the data needs are stable.

## Required retrieval intents

### 1. Resolve the target opportunity

Use this when the request starts from a GovTribe URL, solicitation number, notice ID, title, or agency cue.

Retrieve:

- opportunity notice and canonical URL/record ID
- solicitation number and related notices
- agency, office, contacts if visible, dates, set-aside, NAICS, PSC
- attachments and amendments
- RFP/PWS/SOW/pricing schedules/Q&A
- related award or predecessor links if GovTribe has them

### 2. Read solicitation documents

Retrieve or summarize:

- evaluation criteria and price evaluation method
- basis of award
- pricing schedule and CLINs
- contract type and period of performance
- labor category tables or staffing requirements
- deliverables, SLAs, volume assumptions, and locations
- incumbent references or transition details

If attachments are unavailable, say so and lower confidence.

### 3. Find predecessor and incumbent awards

Search by:

- solicitation number and title variants
- program name/acronym
- agency office
- incumbent/vendor names mentioned in documents
- NAICS/PSC + office + scope keywords
- expiring contracts and follow-on references

Retrieve:

- award ID/PIID, parent IDV, task order, vendor, dates, obligated amount, base/all-options value, ceiling, competition type, set-aside, contract type, NAICS/PSC, place of performance, and description
- modifications and spending trend when available

### 4. Build the comparable universe

Search by:

- same office + scope keywords
- same agency + NAICS/PSC
- same vehicle + similar task descriptions
- same set-aside + scope keywords
- similar labor categories or product/service keywords

For each candidate, classify Tier 1/2/3 and include/exclude reason.

### 5. Analyze vendors and competitors

For likely competitors, retrieve:

- vendor profile
- agency footprint
- recent similar awards
- incumbent or vehicle-holder status
- socioeconomic status
- teaming/subcontracting hints if available
- related news or filings if available in GovTribe

Do not infer private competitor intentions. Phrase likely-bidder analysis as probability based on observable footprint.

### 6. Retrieve rate and pricing data

Use `govtribe-pricing-data` when rate or line-item evidence is needed. Retrieve:

- GSA MAS or other contract vehicle labor rates
- IDIQ/GWAC/BPA schedule rates
- awarded labor category tables
- product catalog rates or contract line item pricing
- historical unit prices
- Service Contract Inventory service-labor footprint, reported hours, FTEs, prime/subcontractor workshare, contractor-reliance, and derived hourly-rate context for labor-heavy federal service work
- FOIA, debrief, or company-uploaded rates only if the requesting company has a right to use them

Normalize all rates to fully burdened vs direct vs ceiling rate, if known.

Use SCI especially for recompetes, professional services, O&M, help desk, staff augmentation, and workforce-rebalancing contexts. Treat SCI-derived hourly rates as source-row context, not loaded labor-category rates; pair them with BLS, GSA labor-rate, line-item, award, and company-provided evidence before using them in a PTW range.

### 7. Use company context

If available, retrieve the company's:

- company name and UEI/CAGE
- existing vehicles and schedules
- NAICS/PSC focus
- socioeconomic status
- agency relationships
- past performance examples
- saved opportunities and pipelines
- known indirect-rate or margin assumptions if they were explicitly provided for AI use

Never invent private company cost structure. If not available, ask only if needed or list it as a data gap.

## Suggested search expansion order

1. Direct predecessor and incumbent evidence
2. Same office, same program, same vehicle
3. Same agency + same NAICS/PSC + same scope
4. Same vehicle + similar scope
5. Similar agency mission + similar scope
6. Broad market analogs

Stop when there is enough high-quality evidence. Do not bury the PTW brief in weak comparables.

## Citation and evidence style

Every evidence row should include a GovTribe source reference when available:

- GovTribe opportunity URL or record ID
- award/PIID/task-order number
- vendor name
- date and value basis
- attachment name/page if citing a document

Use these labels for value basis:

- `obligated amount`
- `base and exercised options`
- `total potential value`
- `IDIQ ceiling`
- `evaluated price`
- `hourly ceiling rate`
- `unit price`
- `company-provided estimate`
- `agent estimate`

## Data gaps to surface

- no pricing attachment available
- no direct predecessor found
- incumbent unclear
- only ceiling values available
- obligations incomplete or stale
- labor mix unknown
- evaluation method unclear
- product unit basis unknown
- customer proposed price unavailable
- customer indirect rates/margin unavailable
