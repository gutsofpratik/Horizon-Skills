---
title: Price-to-Win Analysis
description: Build an evidence-backed PTW range and pricing posture for one opportunity, including terse context-dependent requests such as “ptw.”
---

# Price-to-Win Analysis

Use this reference when the user asks for price to win, PTW, a target bid range, proposed-price posture, recompete pricing, competitor-pricing inference, or pricing evidence for one opportunity, delivery order, task order, or solicitation.

## Context recovery

A terse prompt such as `ptw` is actionable when the conversation already contains an opportunity, pursuit, delivery order, solicitation, attached pricing files, or a proposed price.

- Recover and preserve the selected record, its identifier and established type, and the supplied files and pricing context before asking a question. Do not repeat resolution or retrieval when that context already supports the analysis.
- Reuse previously resolved buyer, office, vehicle, incumbent, contract type, period of performance, CLINs, and likely competitors.
- Ask one bounded clarification only when multiple active targets exist or the missing choice materially changes the analysis, such as quick sanity check versus full PTW model.
- Do not respond with a generic definition of PTW when target context is available.

## Goal

Produce a defensible range rather than a single unsupported number, explain the evidence and confidence, compare any proposed price, and identify the pricing actions needed next.

Pricing Data owns the primary range, rate, staffing, FTE, wrap, and comparable-price analysis. Hand the result to the bundled `govtribe-capture-workflows` skill when the user needs bid/no-bid, P(win), teaming, or pursuit-posture implications.

## Inputs to resolve

Use the request, active record, and source files to resolve as many of these as possible:

- opportunity, solicitation, task order, or delivery order identifier
- buyer and office
- vehicle and parent contract
- incumbent or predecessor
- contract type and evaluation method
- period of performance and option structure
- scope, CLINs, quantities, labor mix, locations, and service levels
- set-aside and vehicle-access constraints
- historical obligations and value basis
- proposed price, margin floor, or staffing plan
- likely competitors and visible public pricing signals

Proceed with a bounded analysis when some inputs are missing; state what the missing inputs do to confidence.

## Evidence sequence

### 1. Source-package and direct pricing evidence

Inspect the solicitation, pricing sheets, CLIN structure, amendments, Q&A, wage determinations, staffing exhibits, and evaluation language when available. Preserve the value basis of every price signal.

Use the selected record and supplied source package first. When additional resolution is needed, choose the tool for the established target type:

- Federal opportunity: `Search_Federal_Contract_Opportunities`.
- State/local opportunity: `Search_State_And_Local_Contract_Opportunities`.
- Award, order, or IDV: use the matching federal or state/local operations in step 2.
- Pursuit with an unresolved linked target: use `Search_Pursuits` to recover that target, then follow its established record type. Preserve the pursuit context and do not create or change a pursuit to perform pricing analysis.
- Record type still unresolved: use `Search_GovTribe` to establish the type, then switch to the matching typed operation if further lookup is needed. Do not replace a selected target merely because another result is easier to retrieve.

Find missing government attachments with `Search_Government_Files` using the selected record's supported filters; use `Search_User_Files` only when needed workspace source files are not already supplied. Use `Documentation` for current schemas and supported relationships rather than assuming identical filters across record types. If a required tool is unavailable, preserve the selected target, use supplied evidence for a bounded analysis, and state the gap; do not redirect a state/local target into federal datasets.

When full source text is still needed, stage the smallest useful supported package with `Add_To_Vector_Store`, wait until the requested files are ready, review skipped and failed files, and use focused `Search_Vector_Store` queries for pricing instructions, CLINs, evaluation rules, wage determinations, staffing, and amendments. Cite returned source metadata through the external host's native citation format. If a material spreadsheet or unsupported attachment is skipped, use the host's attachment or spreadsheet capability; if none exists, disclose the gap and request a supported export only when it changes the PTW conclusion.

### 2. Direct lineage and historical performance

For a delivery order or task order, follow a parent IDV or vehicle relationship only when supported by the selected record or source documents. Gather historical obligations or other reported amounts, period of performance, modifications, incumbent, and related orders when available, preserving the source's value basis and relationship limits.

When existing context is insufficient and additional lookup is needed:

- For federal targets, use `Search_Federal_Contract_Awards` for the award, order, or related order comparables and `Search_Federal_Contract_IDVs` for an established parent instrument. Use `Search_Federal_Transactions` only for a federal target when modification or obligation movement matters.
- For state/local targets, use `Search_State_And_Local_Contract_Awards` for awards or orders represented in that dataset and `Search_State_And_Local_Contract_IDVs` for established parent instruments. Follow actual reported parent/vehicle relationships and source files for history; do not assume federal-style order lineage or invent a state/local transaction tool. Treat missing relationships or history as evidence gaps.

Use the bundled federal record-structure and award-value references only for federal targets. For state/local targets, retain the semantics of the retrieved record and controlling source. Call `Documentation` before relying on freshness-sensitive fields, filters, or relationships for the chosen operations. Preserve the selected target and use the bounded supplied-evidence fallback above when a needed operation is unavailable.

Do not treat parent ceiling, maximum value, or total IDIQ obligations as the likely price for one order.

### 3. Comparable awards and line items

Prefer comparables in this order:

1. direct predecessor or prior iteration
2. same office and same vehicle
3. same buyer and tightly similar scope
4. same labor/quantity pattern and geography
5. broader market evidence only when direct comparables are thin

Use awarded state/local line items when unit, quantity, or equipment evidence is relevant. Keep included and excluded comparables visible.

### 4. Labor, staffing, and rate evidence

Use the appropriate bundled pricing guides:

- [Staffing, Wage, and Labor-Category Workflow](./staffing-wage-and-labor-category-workflow.md)
- [BLS Occupational Wage Data MCP Tool](./bls-occupational-wage-data-mcp-tool.md)
- [Search GSA Labor Rates MCP Tool](./search-gsa-labor-rates-mcp-tool.md)
- [Search Service Contract Inventory MCP Tool](./search-service-contract-inventory-mcp-tool.md)

Use staffing and FTE reasonableness checks when the proposed headcount materially drives price. Separate wage, fully burdened cost, bill rate, and ceiling rate.

### 5. Public benchmark versus proprietary actuals

For wrap-rate questions, indirect-rate questions, or competitor pricing:

- clearly state that actual company indirect rates, bid rates, and negotiated margins are generally proprietary unless directly provided or publicly disclosed
- provide planning benchmarks, observed rate relationships, or scenario assumptions instead of presenting a public-data estimate as an actual company rate
- show the assumed fringe, overhead, G&A, fee, or composite multiplier when using a modeled wrap
- distinguish a MAS ceiling rate from a likely task-order rate

## Reconcile the PTW range

Build both views when the evidence supports them:

- top-down market view from predecessor prices, awards, obligations, line items, public rate evidence, buyer behavior, and likely competition
- bottom-up execution view from labor, staffing, quantities, materials, escalation, transition, travel, risk, and fee assumptions

If the views diverge, show the gap and its likely cause. Do not hide it inside one midpoint.

Provide at least three scenarios:

- aggressive / low
- competitive midpoint
- premium / value-supported

For each scenario, state the range, assumptions, likely use case, realism risk, and evidence strength.

## Output contract

For a quick PTW request, return:

- recommended range or target
- proposed-price posture when available
- confidence
- top evidence and assumptions
- one immediate next action

For a fuller analysis, include:

1. target and pricing basis
2. evidence ledger with value basis
3. comparable universe and exclusions
4. top-down range
5. bottom-up range
6. reconciled PTW scenarios
7. proposed-price comparison
8. confidence and missing evidence
9. pricing actions
10. optional capture implications clearly labeled as a handoff

## Normal chained workflows

- If the follow-up is “write the submission email,” “draft the pricing cover note,” or another outbound proposal artifact, hand off to the bundled `govtribe-proposal-workflows` skill while preserving the chosen price, assumptions, caveats, and active opportunity. Use the host's document capability or return a complete Markdown draft when that capability is unavailable. Drafting does not authorize sending.
- If the follow-up asks whether to bid, how PTW affects P(win), or whether a teammate changes the economics, hand off to the bundled `govtribe-capture-workflows` skill, preserve the pricing result, and clearly separate the new strategic judgment from the pricing evidence.
- These handoffs are expected workflow progression, not routing failures.

## Guardrails

- Use a range, not a magic number.
- Keep facts, assumptions, and inferred competitor posture separate.
- Never imply access to proprietary competitor indirect rates or bid prices without evidence.
- Label ceiling, obligated amount, total potential value, evaluated price, hourly rate, and unit price correctly.
- Do not force external tools when the user supplied enough contract and staffing detail for a useful bounded reasonableness analysis.
- State when evidence is too thin to support more than a directional range.
