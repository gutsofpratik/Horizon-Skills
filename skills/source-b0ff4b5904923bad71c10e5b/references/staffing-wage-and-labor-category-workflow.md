---
name: staffing-wage-and-labor-category-workflow
description: Staffing, FTE reasonableness, wage, labor-category, and public wrap-rate benchmarking workflow for combining user-supplied contract facts, BLS wage baselines, GSA labor-rate benchmarks, awarded-price evidence, and SCI service-labor context without mixing source semantics.
---

# Staffing, Wage, and Labor-Category Workflow

Use this guide when the user asks for a staffing model, FTE reasonableness assessment, wage model, labor-category mapping, BLS/GSA rate comparison, burden or escalation assumptions, public wrap-rate planning benchmark, service-labor pricing evidence, or a quick rate sanity check.

Do not use this guide when the request is only capture qualification, proposal compliance extraction, document extraction of a stated FTE number, or a generic award search with no staffing, wage, labor category, rate, or pricing-evidence question.

Before delivering a staffing workbook, rate-support table, pricing assumptions exhibit, or narrative, read [Pricing Output Quality Checks](./pricing-output-quality-checks.md).

## Inputs to Resolve

Resolve as many of these as the request and GovTribe context allow. Do not block on every input, but label missing assumptions.

- Target opportunity, buyer lane, award, delivery order, IDV, vehicle, vendor, or market context
- User-supplied contract description, estimated FTEs, hours, workload, service levels, labor mix, and performance constraints
- Place of performance, worksite, remote/on-site assumption, and geography level
- Roles, labor categories, seniority, quantities, hours, FTEs, or draft staffing plan
- Contract type, period of performance, option years, and escalation need
- Certifications, clearances, education, experience, or worksite constraints
- SCA, DBA, wage determination, union, or locality concerns when raised by the user or source material
- Target GSA vendor, contract, SIN, category, or schedule lane when relevant
- Requested benchmark type: wage, bill rate, FTE reasonableness, public wrap/multiplier planning range, awarded price, or full pricing model
- Requested output format: quick benchmark, staffing model, price-to-win support, proposal-pricing support, or assumptions table
- Prior pricing notes, BOE templates, labor-category mappings, rate assumptions, or reusable pricing workbook formats only when the user asks to reuse, compare, or continue from them. Read [Prior User File Context](./prior-user-file-context.md) before searching prior files.

A complete pasted fact pattern can be sufficient for a bounded reasonableness assessment. Do not force a tool call when it would not materially improve the answer.

## Source Semantics

Keep these meanings separate in the answer.

- `BLS_Occupational_Wage_Data`: wage baseline, geography, occupation proxy, percentile, and escalation input. It is not a bill rate, not fully burdened cost, and not awarded pricing.
- `Search_GSA_Labor_Rates`: GSA Schedule ceiling-rate benchmark and visible labor-category market context. It is not necessarily a task-order winning price and not a wage table.
- `Search_Line_Items`: awarded state/local unit-price evidence when quantity, unit, description, and parent context are comparable enough. It is not normalized labor-category market data by default.
- `Search_Service_Contract_Inventory`: service-labor footprint, FTE/hour intensity, incumbent workshare, subcontractor reliance, and derived hourly context. It is not a complete pricing benchmark by itself.
- User-provided staffing, rates, workload, and wrap assumptions: decision inputs supplied by the user. They are not independently verified source evidence unless corroborated.
- Public wrap-rate or multiplier benchmarks: planning ranges assembled from transparent assumptions and public market evidence. They are not a named contractor's actual proprietary indirect-rate structure.

## Procedure

### 1) Classify the Pricing Question

Choose the narrowest useful path:

- **Wage baseline**: start with BLS and explain geography, occupation proxy, percentile, and escalation.
- **Labor-category benchmark**: start with GSA labor rates and compare category/rate rows by vendor, SIN, contract, education, experience, worksite, clearance, and contract year.
- **FTE reasonableness**: independently estimate a plausible staffing range from workload, hours, service levels, coverage, labor mix, and performance constraints, then classify the supplied estimate as reasonable, underestimated, or overestimated.
- **Public wrap-rate benchmark**: build a transparent planning multiplier or range and state what fringe, overhead, G&A, fee, escalation, and other elements it includes or excludes.
- **Full staffing model**: combine BLS wage baseline, burden assumptions, GSA labor-rate benchmark, comparable award or line-item evidence, SCI where service-labor footprint matters, and user-provided assumptions.
- **Exact pricing-evidence review**: resolve the award, order, parent contract, obligations, source-file pricing instructions, and comparable evidence before drawing conclusions.
- **PTW support**: use this guide for staffing and rate evidence, then use the bundled `govtribe-capture-workflows` skill when the task becomes bid posture or target-price strategy, preserving the evidence, selected range, assumptions, and confidence.
- **Proposal pricing support**: use this guide for rate and assumption evidence, then use the bundled `govtribe-proposal-workflows` skill and the host's document or spreadsheet capability when the task becomes a proposal artifact; return a complete Markdown or CSV fallback when that capability is unavailable.
- **Sanity check**: return a small evidence table, confidence, caveats, and next data needed.

### 2) Normalize Roles

Map customer wording into both wage and rate concepts:

- Preserve the original user role or labor category.
- Map to the closest defensible BLS occupation or SOC proxy.
- Map to likely GSA labor-category search terms.
- Record confidence and caveats when the match is approximate.
- Do not average unrelated labor categories just because the wording overlaps.

### 3) Resolve Geography

Use the most specific geography that the evidence supports:

- MSA or locality when place of performance is known and supported by wage rows.
- State when the MSA is unknown or too narrow.
- National only when no better location is available or the user requests a national benchmark.
- Separate remote, on-site, cleared, travel, and locality assumptions from source-backed facts.

### 4) Pull the Wage Baseline

Use `BLS_Occupational_Wage_Data` for wage evidence.

- Select occupation proxies deliberately and explain the mapping.
- Use median wages for a baseline unless the role level implies otherwise.
- Use lower percentiles for junior roles and upper percentiles for senior, cleared, specialized, or hard-to-fill work.
- Apply escalation only when the model needs future-year pricing.
- Treat fringe, overhead, G&A, fee, productivity, and labor mix as explicit assumptions, not BLS facts.

### 5) Benchmark the Bill-Rate Market

Use `Search_GSA_Labor_Rates` when GSA Schedule market context is relevant.

- Search by precise labor-category terms before using broad role words.
- Narrow by vendor, contract, SIN, category, education, years of experience, worksite, clearance, and contract year when available.
- Compare BLS-derived burdened ranges to GSA ceiling-rate ranges only after labeling both value bases.
- Do not describe GSA ceiling rates as likely winning task-order rates unless additional awarded-price evidence supports that conclusion.

### 6) Find Awarded Comparables

Use `Search_Line_Items` only when the evidence is comparable enough.

- Prefer rows with clear quantity, unit of measure, description, parent award or IDV context, and similar service or product scope.
- Use line-item evidence to support or challenge rate assumptions, not to replace wage or labor-category mapping.
- If units or descriptions do not align, state that the evidence is directional or exclude it.

For federal delivery-order evidence, resolve the exact order and parent instrument, then distinguish obligations, potential value, ceiling, and inferred labor context.

### 7) Pressure-Test Staffing Realism With SCI

Use `Search_Service_Contract_Inventory` when labor-heavy federal services depend on incumbent footprint or service-labor intensity.

- Prefer prime records for row-level dollars, total hours, total FTEs, subcontractor count, subcontractor-hour share, and derived hourly context.
- Use subcontractor rows for workshare and FTE/hour distribution, not per-subcontractor pricing.
- Treat `derived_hourly_rate` as context based on reported dollars and hours, not a loaded labor-category rate.
- Use SCI to challenge staffing volume, incumbent labor intensity, prime/sub workshare, and recompete realism before narrowing the recommended range.

### 8) Assess FTE Reasonableness Independently

When the user provides an estimated headcount:

- Reconstruct annual productive hours and coverage requirements rather than accepting the estimate as the baseline.
- Translate workload, shifts, service levels, locations, deliverables, management span, surge, leave, training, and nonproductive time into a low/base/high staffing range.
- Compare the supplied FTE count to the independent range and classify it as `Reasonable`, `Underestimated`, `Slightly Underestimated`, `Slightly Overestimated`, or `Overestimated`.
- Identify the assumptions most likely to move the answer.
- State when the estimate is based only on supplied facts and when GovTribe evidence materially corroborates it.

### 9) Build a Public Wrap-Rate Planning Benchmark

When the user asks for typical wrap rates or multipliers:

- Define the value basis before giving a range: direct labor to cost, direct labor to loaded cost, or direct labor to bill rate.
- Show a transparent illustrative stack for fringe, overhead, G&A, fee, and any other included elements.
- Use public wage, GSA, award, and market evidence only as directional support.
- Present a planning range and sensitivity drivers rather than claiming one universal rate.
- State explicitly that named-company actual indirect rates, pools, allocation bases, negotiated rates, and margins are proprietary unless the user supplies them.

### 10) Build Assumptions

Show the chain from wage evidence to staffing assumptions:

`wage baseline -> burdened cost assumption -> bill-rate range -> awarded or market comparables -> pricing caveats`

Make fringe, overhead, G&A, fee, escalation, productivity, labor mix, hours, FTEs, and place of performance visible. If the user provided values, label them as user-provided assumptions.

### 11) Hand Off Only When the Task Changes Domains

- Stay in this guide while the answer is mainly staffing, FTE, wage, labor-category, wrap, rate, or source-semantics work.
- Use [Pricing Model Workflow](./pricing-model-workflow.md) when the user needs a broader combined pricing model beyond staffing and rate evidence.
- When the user needs bid/no-bid, pursuit posture, competitor posture, or PTW strategy, use the bundled `govtribe-capture-workflows` skill and preserve the pricing result.
- When the user needs a pricing-volume artifact, compliance matrix, workbook, annotated outline, or submission email, use the bundled `govtribe-proposal-workflows` skill, preserve the model inputs, and use the host's document or spreadsheet capability; if unavailable, return the corresponding Markdown or CSV source artifact.

## Output Contract

For a full answer, use the applicable portions of this structure:

1. **Pricing question resolved**: wage baseline, labor-category benchmark, FTE reasonableness, public wrap benchmark, exact pricing-evidence review, full staffing model, PTW support, proposal-pricing support, or sanity check.
2. **Independent call**: recommended range or classification, confidence, and the primary assumptions driving it.
3. **Role mapping table**: user role, BLS proxy, GSA category terms, confidence, and caveats.
4. **Wage baseline table**: geography, percentile, wage, source, and use in the model.
5. **Bill-rate benchmark table**: vendor, category, SIN, contract, representative rates or low/median/high, and caveats.
6. **Comparable award, order, line-item, or SCI evidence**: include only if comparable enough.
7. **Staffing or wrap assumptions**: labor mix, hours, FTEs, fringe, overhead, G&A, fee, escalation, productivity, and sensitivity drivers.
8. **Risks and missing data**: SCA/DBA, wage determination, clearances, union/locality, remote/on-site, incumbent unknowns, incomplete categories, proprietary-rate limits, or thin comparables.

For a quick benchmark, return only the independent call, best source-backed benchmark or supplied-data calculation, caveats, and next data needed.

## Failure Modes

- Do not call a BLS wage a fully burdened price.
- Do not call a GSA ceiling rate a likely winning task-order price without caveat.
- Do not call a public planning multiplier a named contractor's actual wrap rate.
- Do not simply accept the user's FTE estimate; build an independent bounded check.
- Do not average unrelated labor categories.
- Do not infer wage determination, SCA, DBA, union, or locality compliance unless the relevant source is retrieved.
- Do not use SCI derived hourly context as a standalone market rate.
- Do not hide user-provided burden, fee, escalation, productivity, or labor-mix assumptions inside source-backed evidence.
- Do not refuse a bounded advisory answer solely because the user supplied the relevant contract facts instead of a searchable GovTribe record.
