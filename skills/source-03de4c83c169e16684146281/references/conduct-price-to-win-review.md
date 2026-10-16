# Conduct Price-to-Win Review

## Overview
- Use this workflow for price-to-win analysis, pricing posture review, recompete pricing, competitor-pricing inference, or a sanity check against a proposed price for one opportunity.
- Prefer this workflow when the output should drive a capture or pricing decision, not just return one benchmark source.
- Goal: produce an evidence-backed PTW range, explain confidence, and recommend concrete pricing and capture actions.

## Default output
- For a standard or deep PTW review, prefer the structure in `assets/price-to-win-brief-template.md` from the skill root.
- Open the brief with a decision snapshot: recommended target, proposed-price posture, confidence, and the primary pricing action.
- Keep rendered Markdown/PDF briefs readable: use compact scenario, evidence, and competitor tables in the document.
- Put the full comparable universe, detailed rate rows, and detailed normalization model in CSV/JSON companions when they would make the document table too wide or dense.
- Before delivering a customer-facing brief or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).
- For a quick check, return only:
  - recommended range or posture,
  - confidence,
  - top evidence points,
  - next action.
- If structured company inputs are needed, use `assets/price-to-win-intake.json` from the skill root as the preferred intake shape.

## Inputs to resolve
Resolve as many of these as are available from the request, opportunity context, and source files. Do not block if some are missing.
- Opportunity or solicitation identifier
- Buying office, agency, vehicle, and competition context
- Solicitation, amendments, Q&A, pricing sheets, CLIN structure, and evaluation method
- Predecessor or incumbent signals
- Proposed total price, labor mix, rates, or target margin if available
- Known company differentiators, vehicle position, teaming notes, or likely competitors
- Prior pricing notes, BOE templates, proposal pricing assumptions, or reusable pricing workbooks only when the user asks to reuse or compare against them. Read [Prior User File Context](./prior-user-file-context.md) before searching for prior files.

If pricing documents or direct comparables are missing, still produce a bounded PTW hypothesis and label the confidence accordingly.

## Read-on-demand references
- Read [Price-to-Win Method](./price-to-win-method.md) before building scenarios or reconciling market and execution views.
- Read [Price-to-Win Data Playbook](./price-to-win-data-playbook.md) before gathering awards, incumbent, competitor, and rate evidence.
- Read [Price-to-Win Quality Checks](./price-to-win-quality-checks.md) before finalizing.

## Procedure

### 1) Resolve the decision question first
Identify whether the request is for:
- a quick PTW sanity check,
- a standard PTW brief,
- a proposed-price comparison,
- a recompete pricing posture review,
- or a deeper pricing and capture strategy readout.

Do not force a deep PTW brief when the request only needs a directional answer.

### 2) Build the opportunity and evidence set
Use [Price-to-Win Data Playbook](./price-to-win-data-playbook.md).
At minimum, resolve:
- the opportunity and buying office,
- solicitation and pricing basis,
- contract type and period of performance,
- evaluation method,
- incumbent or predecessor signals,
- direct pricing artifacts or their absence.

If the request depends on exact solicitation wording for price evaluation, pricing instructions, or CLIN structure, follow the bundled [vector-store retrieval guide](./govtribe-docs-vector-store-content-retrieval.md): resolve the files, call `Add_To_Vector_Store`, then call `Search_Vector_Store` and cite returned source metadata through the host's native citation format.

### 3) Build the comparable universe
- Prefer direct predecessor, same office, same vehicle, and same-scope comparables before widening.
- Keep included and excluded comparables visible.
- Label value basis carefully: obligated amount, total potential value, ceiling, evaluated price, hourly rate, or unit price.

### 4) Analyze incumbent and competitor posture
- Identify likely bidders, incumbent advantage, vehicle access, and visible pricing posture.
- Distinguish observed evidence from inferred pricing behavior.
- If likely-bidder recovery or incumbent determination is still unresolved, use the related capture workflow first and then return to PTW.

### 5) Normalize pricing signals
- Normalize for scope, option structure, contract type, location, labor mix, units, and escalation where the evidence supports it.
- Use the `govtribe-pricing-data` skill when PTW needs staffing or wage model support, labor-category mapping, BLS/GSA rate comparisons, labor-rate benchmarks, MAS ceiling-rate evidence, awarded state/local line-item pricing support, or Service Contract Inventory context for service-labor footprint, FTEs, contractor reliance, workshare, and derived hourly-rate checks.
- Flag outliers and explain why they were excluded or down-weighted.

### 6) Reconcile market view and execution view
Use [Price-to-Win Method](./price-to-win-method.md).
- Build the top-down market view from awards, rates, and buyer history.
- Build the bottom-up execution view from CLINs, labor, deliverables, and realism constraints when enough inputs exist.
- If the two views diverge materially, surface the gap and explain the likely capture or staffing implications instead of hiding it inside one midpoint number.
- In the rendered brief, include a visible market/execution reconciliation table with top-down range, bottom-up range, reconciled PTW range, and confidence notes.

### 7) Produce the PTW scenarios
Provide:
- aggressive / low,
- competitive midpoint,
- premium / value-based.

For each scenario, explain:
- the range,
- when to use it,
- the main risk,
- and which scenario best matches the opportunity and company position.

If a proposed price is available, compare it directly to the range and label the posture clearly.

### 8) Keep rendered evidence tables compact
- In the Markdown brief, summarize comparable evidence with a narrow table focused on `Signal`, `Value basis`, `PTW implication`, and `Source`.
- Keep document evidence tables to 6 rows or fewer by default. Prioritize the direct predecessor, strongest same-office/same-vehicle comparables, major exclusions, and rate signals that materially change the recommendation.
- Keep likely-competitor coverage compact. Prefer concise response notes when a competitor table would wrap heavily or split across pages.
- If the comparable universe has more than 6 rows, state that the full evidence set is delivered in a CSV/JSON companion.
- If the user explicitly asks for every comparable in the rendered document, split evidence by tier or value basis rather than forcing one wide table.

### 9) Recommend actions and validate
- Recommend specific capture and pricing next steps: questions to resolve, evidence to pull, labor mix checks, vehicle-rate checks, teaming decisions, or bid / no-bid implications.
- Run the checklist in [Price-to-Win Quality Checks](./price-to-win-quality-checks.md).
- If a structured PTW JSON output is created, run `python3 scripts/validate_price_to_win_output.py path/to/ptw.json` before final delivery.
- Correct weak value-basis labels, unsupported assumptions, or missing confidence statements before finalizing.

## Output rules
- Use a range, not a single unsupported magic number.
- Separate facts, assumptions, and inferred competitor posture.
- Keep evidence traceable to GovTribe records, solicitation text, or clearly labeled company-provided inputs.
- Tie pricing posture to the actual evaluation method and solicitation structure.
- Flag low-confidence conditions and missing pricing documents directly.
- Do not use non-public competitor pricing or other impermissible inputs.

## Common failure modes to avoid
- Treating PTW as only a labor-rate benchmark
- Treating IDIQ ceiling values as likely award values
- Ignoring evaluation method, option years, or contract type
- Recommending a premium without clear evaluation support
- Producing a market overview without a usable pricing posture recommendation
- Hiding sparse evidence behind confident language
- Burying the top-down versus bottom-up reconciliation in prose or an appendix
- Delivering a rendered brief that feels like a raw table dump instead of a pricing decision memo
