---
name: pricing-model-workflow
description: Example-driven workflow for building a pricing model with `BLS_Occupational_Wage_Data`, `Search_GSA_Labor_Rates`, `Search_Line_Items`, and Service Contract Inventory context when service-labor footprint evidence is available.
---

# Pricing Model Workflow

Use this guide when the user is building an actual pricing model, not just asking for a one-off benchmark or a narrow tool query.

If the request is specifically about staffing models, wage baselines, labor-category mapping, BLS/GSA rate comparisons, burden assumptions, escalation, or staffing realism, read [Staffing, Wage, and Labor-Category Workflow](./staffing-wage-and-labor-category-workflow.md) first and return here only when the user needs the broader combined pricing model.

Before delivering a pricing workbook, rate-support exhibit, or pricing narrative, read [Pricing Output Quality Checks](./pricing-output-quality-checks.md).

When the user asks to reuse prior pricing notes, BOE templates, labor-category mappings, rate assumptions, or workbook formats, read [Prior User File Context](./prior-user-file-context.md) before searching prior files. Refresh current rate, wage, award, and solicitation facts before treating them as current.

## Workflow

### 1) Identify the pricing context

First determine which of these situations applies:

- **Non-MAS / general pricing model**
- **MAS bid or MAS benchmark**
- **Hybrid model** where the user wants both internal cost realism and external market comparison

If unclear, default to a **hybrid workflow**:

1. build from `BLS_Occupational_Wage_Data`
2. benchmark with `Search_GSA_Labor_Rates`
3. add `Search_Line_Items` if directly comparable awarded state/local line items exist
4. add `Search_Service_Contract_Inventory` when the context is service-heavy and staffing, workshare, FTEs, subcontractor reliance, or derived hourly-rate context affects the pricing decision

### 2) Normalize the labor mapping

Before calculating rates, map the user’s role to the cleanest comparable labor concept.

For `BLS_Occupational_Wage_Data`:
- map to an **occupation title** or **SOC code**
- choose the most comparable occupation, not the broadest keyword

For `Search_GSA_Labor_Rates`:
- map to the most precise **labor category title** possible
- avoid generic terms like `Administrator`, `Supervisor`, or `Analyst` when narrower titles exist

If a search term is too broad and results are noisy, refine the title before modeling.

### 3) Build the wage baseline with `BLS_Occupational_Wage_Data`

Use `BLS_Occupational_Wage_Data` as the wage baseline when the user needs an actual pricing model.

Recommended sequence:

1. choose occupation / SOC
2. choose geography:
   - MSA when place of performance is known
   - state if MSA is not practical
   - nationwide only when no better location is available
3. choose occupation level:
   - Junior -> 25th percentile
   - Journeyman -> 50th percentile
   - Senior -> 75th percentile
   - SME -> use guide-based logic above senior-level wages
4. choose escalation method:
   - 2-year, 5-year, 10-year average ECI, or custom
5. apply indirects:
   - fringe
   - overhead
   - G&A
   - fee/profit

Use this illustrative multiplicative formula only when its sequential allocation bases match the company-approved accounting treatment; otherwise use the supplied bases and avoid double counting. Label the result as a modeled rate including the stated fee, not a BLS wage or proprietary actual.

Use this formula for a burdened estimate:

`Burdened Rate = Wage x (1 + Fringe) x (1 + Overhead) x (1 + G&A) x (1 + Fee/Profit)`

Use this formula for a future-year burdened estimate:

`Escalated Burdened Rate = Escalated Wage x (1 + Fringe) x (1 + Overhead) x (1 + G&A) x (1 + Fee/Profit)`

### 4) Benchmark the result with `Search_GSA_Labor_Rates`

After building the BLS-based model, compare it against `Search_GSA_Labor_Rates` when relevant.

Use filters that improve comparability:

- education
- years of experience
- worksite
- business size
- security clearance
- SIN
- contract year
- category / subcategory

Then classify the result:

- **Below market-visible MAS range**
- **Within market-visible MAS range**
- **Above market-visible MAS range**
- **Not comparable enough to conclude**

### 5) Add awarded line-item evidence with `Search_Line_Items` when relevant

Use `Search_Line_Items` when the user has a comparable state/local procurement context or needs evidence from actual awarded line items.

Recommended sequence:

1. start from the known parent if possible:
   - `state_local_contract_award_ids`
   - `state_local_contract_idv_ids`
   - `state_local_contract_vehicle_ids`
2. if the parent is not known, search by product or service phrase and narrow with:
   - `state_ids`
   - `nigp_category_ids`
   - `unspsc_category_ids`
   - `unit_of_measurements`
   - `unit_price_range`
   - `quantity_range`
3. review `unit_of_measure` before comparing prices across rows
4. use `unit_price_stats`, `quantity_stats`, and top-category aggregations to summarize the evidence
5. keep the award / IDV / vehicle context in the final explanation so the user understands what those awarded prices actually represent

Use `Search_Line_Items` to strengthen the market evidence section of the model, not to replace wage logic when the user needs labor build-up analysis.

### 6) Add SCI service-labor footprint context when relevant

Use `Search_Service_Contract_Inventory` when the pricing model is for labor-heavy federal services and the decision depends on incumbent footprint, contractor reliance, FTEs, reported hours, prime/subcontractor workshare, or derived hourly-rate context.

Recommended sequence:

1. anchor the search to the known fiscal year, vendor, award, IDV, agency, PSC, NAICS, contract number, or place of performance when available
2. use `role: ["prime"]` for row-level dollar, total-hour, FTE, subcontractor-count, and derived-rate context
3. use `subcontractor_count_range.max = 0` when a cleaner prime-only derived hourly-rate proxy is more useful than a blended prime-plus-sub workshare signal
4. request `total_dollar_amount_invoiced`, `total_contractor_hours_invoiced`, `total_ftes`, `subcontractor_count`, `sub_hours_share`, `derived_hourly_rate`, `vendor`, and parent award or IDV fields
5. use stats and terms aggregations to summarize hours, FTEs, dollars invoiced, derived hourly rates, top vendors, agencies, PSCs, NAICS, and contract identifiers before pulling detailed rows

Use SCI to pressure-test staffing volume, incumbent labor intensity, and workshare assumptions. Do not treat `derived_hourly_rate` as a loaded labor-category rate, a wage benchmark, or a complete price. It is source-row context that should be paired with BLS, GSA labor-rate, line-item, award, and company-provided evidence.

### 7) Explain the difference between cost, market, and service-footprint context

Always distinguish:

- **cost-based estimate** from BLS + indirects
- **market-visible MAS benchmark** from `Search_GSA_Labor_Rates`
- **awarded transactional evidence** from `Search_Line_Items`
- **service-labor footprint context** from `Search_Service_Contract_Inventory`

These are not the same thing. A pricing model is stronger when it shows how the sources agree, diverge, or constrain one another.

## Examples

### Example: non-MAS staffing model
User asks:
> Build a labor pricing model for cybersecurity engineers supporting a DHS program in Northern Virginia.

Recommended approach:
- start with `BLS_Occupational_Wage_Data`
- map roles to the closest defensible occupation titles or SOC codes
- use the relevant MSA
- select occupation levels
- escalate only if future-year pricing is needed
- apply indirects explicitly
- optionally compare to `Search_GSA_Labor_Rates` as a market-facing benchmark

### Example: MAS rate sanity check
User asks:
> Are our proposed MAS labor rates for project managers and business analysts out of line?

Recommended approach:
- start with `Search_GSA_Labor_Rates`
- search precise labor categories
- filter for experience, education, worksite, business size, SIN, and security clearance as relevant
- compare proposed rates to the returned benchmark range and summary statistics
- use `BLS_Occupational_Wage_Data` only as a secondary explanation of labor-cost structure if helpful

### Example: awarded pricing evidence
User asks:
> Show me comparable awarded state/local line items for network switch maintenance so I can sanity-check my unit price.

Recommended approach:
- start with `Search_Line_Items`
- narrow by the best available parent contract context, state, NIGP, UNSPSC, and unit of measure
- compare only rows with comparable units
- use `unit_price_stats` and `quantity_stats` to summarize the awarded evidence
- optionally bring in `BLS_Occupational_Wage_Data` only if the user also needs a labor build-up explanation

### Example: hybrid pricing model
User asks:
> Help me assemble a price-to-win labor model for a professional services bid.

Recommended approach:
- build the wage baseline from `BLS_Occupational_Wage_Data`
- burden and escalate rates
- compare to `Search_GSA_Labor_Rates` if MAS comparables are relevant
- add `Search_Line_Items` if there are directly comparable awarded state/local line items
- add `Search_Service_Contract_Inventory` if the incumbent or agency has relevant service-contract inventory rows that show FTEs, reported hours, subcontractor workshare, or derived hourly-rate context
- explain where the estimate sits relative to visible market pricing
