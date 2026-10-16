---
title: Conduct Black Hat Review
description: How to run a mock source-selection review for one specific opportunity.
---

# Conduct Black Hat Review

Use this reference when the user wants a rigorous black hat review of one opportunity built around the buyer's likely source-selection logic.

## Goal
- Reconstruct the government's evaluation model, identify the serious bidder field, score likely offers against the stated factors and the buyer's recent behavior, and turn that view into concrete counter-moves.
- Keep the review evidence-backed and decision-oriented. The point is to improve win probability, not to produce free-form competitor brainstorming.
- For a document-style deliverable, prefer the structure in `assets/black-hat-brief-template.md` from the skill root.
- Before delivering a customer-facing brief or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).

## Minimum input contract
- Required: one specific opportunity or resolvable procurement target.
- Strongly preferred: our company or team context.
- Helpful: likely bidders, incumbent hypothesis, solicitation files, amendments, Q&A, and pricing context.
- If the likely bidder field is missing, build it first with `references/likely-bidders.md`.
- If our side is missing, still review the field, but label our-position judgments as lower-confidence.

## Workflow

### 1. Reconstruct the evaluation model first
- Resolve the opportunity on the correct market surface and recover the solicitation, attachments, amendments, Q&A, evaluation criteria, contract type, vehicle rules, CLIN logic, and compliance thresholds.
- Build one `evaluation_model` before scoring anyone. It should carry at least:
  - evaluation method such as `tradeoff`, `lpta`, or `unknown`
  - factors and subfactors
  - relative importance
  - contract type
  - minimum acceptability thresholds
  - vehicle, labor, security, and eligibility constraints
  - atomic requirement statements that can be scored directly
- Federal contracts should use the full Part 15 source-selection framing.
- Federal grants and state/local work can still use this model, but adapt the factor language to the awarding program, jurisdiction, or buyer-specific evaluation structure instead of forcing a federal tradeoff frame.
- Use the bundled [federal contract](./govtribe-docs-federal-contract-data-model.md), [federal grant](./govtribe-docs-federal-grant-data-model.md), and [state and local contract](./govtribe-docs-state-and-local-contract-data-model.md) references for stable data-model guidance. Call `Documentation` when the current tool schema or freshness-sensitive behavior matters.

### 2. Build the bidder universe and bid-propensity view
- Start from the incumbent, vehicle holders, same-buyer winners, same-lane vendors, known teammates, adjacent-market firms, and any user-supplied likely bidders.
- Model the bidder field as a top set, not one guessed rival.
- Score bid propensity using the strongest available combination of:
  - incumbent status
  - vehicle eligibility
  - scope similarity to prior awards
  - customer or agency adjacency
  - contract-size fit
  - place-of-performance fit
  - clearance and readiness fit
  - socio-economic eligibility
  - teammate connectivity
  - momentum or engagement signals when they exist
- Keep scenario branches visible when incumbent-plus-challenger teaming looks plausible.

### 3. Score requirement coverage at the atomic requirement level
- Break the requirement into atomic statements and score each bidder from evidence upward, not narrative downward.
- Use the strongest evidence for each requirement from capabilities, awards, files, and other retrieved material.
- A good default requirement-coverage frame is:
  - `0.55 * semantic_match`
  - `0.15 * keyword_overlap`
  - `0.10 * size_fit`
  - `0.10 * recency`
  - `0.10 * customer_fit`
- Roll coverage up by requirement weight rather than averaging raw narratives.
- Keep an explicit evidence trail for which source best supported each requirement-level score.

### 4. Score past performance separately from generic capability
- Do not let past performance disappear into capability marketing.
- Prefer official source signals when available, then use cross-source corroboration to strengthen or weaken the view.
- Score past performance in two layers:
  - relevance: scope, customer, contract or assistance structure, size, recency, and place or security fit
  - credibility: source quality, cross-source agreement, recency, and data completeness
- Use a neutral fallback when relevant past performance data is genuinely absent instead of treating no evidence as either a strength or a failure.
- Use `references/past-performance-match.md` when the competitor past-performance picture needs a deeper evidence pass.

### 5. Model price-to-win and realism separately
- Do not reduce pricing to a hand-wavy “probably low” judgment.
- Build a market price band from comparable awards, rate structures, labor categories, geography, contract type, and buyer history.
- Produce bidder-specific price posture such as aggressive, mid-pack, or premium.
- Keep a realism view distinct from simple price posture when the contract type or evaluation method makes realism material.
- Pressure-test any countermeasure against our own margin floor before recommending it.
- Use the `govtribe-pricing-data` skill only when price-band evidence or realism materially changes the review.

### 6. Emulate the evaluator, not just the competitor
- Run the review through the `evaluation_model`, not through free-form prose.
- For each serious bidder, produce two views:
  - evaluator view: likely standing by factor, with probable strengths, weaknesses, deficiencies, significant weaknesses, and risks where the method supports those distinctions
  - competitor view: likely win themes, likely attack themes against us, likely teaming move, and likely price posture
- Use `references/gao-bid-protest-evidence.md` when protest history, prior GAO decision text, or agency protest outcomes materially sharpen bidder attack themes, evaluator vulnerabilities, or risk mitigation.
- In `tradeoff` buys, keep discriminator-oriented factor scorecards.
- In `lpta` buys, switch non-price scoring to acceptability and price to low-price ranking. Do not pretend tradeoff logic applies when it does not.

### 7. Turn the review into counterstrategy optimization
- Do not stop at “competitor X looks dangerous.”
- Recommend concrete moves such as:
  - add or replace a teammate
  - swap in a stronger past-performance example
  - sharpen transition or risk-mitigation language
  - add a key person or SME
  - reduce price inside a real margin floor
  - restructure staffing to improve realism
  - shift win themes toward stronger discriminators
- Score each move on:
  - expected score lift
  - expected `P(win)` lift
  - proposal effort
  - margin impact
- Use `references/conduct-bid-no-bid-review.md` only when a countermeasure needs to be checked against our own economic posture or pursuit posture.

### 8. Keep uncertainty and evidence first-class
- Every major claim should carry:
  - evidence IDs
  - support score
  - confidence
  - missing-data flags
  - scenario dependencies
- Use a confidence frame like:
  - `0.40 * data_completeness`
  - `0.30 * source_agreement`
  - `0.20 * model_stability`
  - `0.10 * human_override`
- If a claim depends on weak evidence or a fragile scenario branch, make that visible instead of hiding it in narrative confidence.

## Output contract
- Return:
  - `evaluation_model`
  - `predicted_bidders`
  - `competitor_assessments`
  - `our_position`
  - `price_to_win`
  - `recommended_actions`
  - `confidence_summary`
  - `evidence_ledger`
- Use compact markdown tables when they materially improve readability.
- Open rendered briefs with a decision snapshot: likely leader, our standing, main exposure, primary counter-move, and confidence.
- Use concise threat cards instead of wide competitor tables when bidder strengths, risks, and counterstrategy notes would wrap heavily.
- Keep evaluator comparison focused on likely leader versus our team in the document; put full factor scorecards in a CSV/JSON companion.
- Use concise counter-move bullets instead of wide action tables when lift, effort, and margin fields would split across pages.
- Keep the tone candid and unsentimental. Do not assume our side is the best choice without evidence.
- If the evidence is thin, say so clearly and keep the uncertainty visible.

## Deterministic asset
- From the skill root, use `scripts/black_hat_engine.py` with `references/black-hat-input-schema.md` when the workflow needs reproducible bidder ranking, factor scorecards, countermove scoring, or UI-safe JSON output.
- When engine output is produced, validate it before final delivery:

```bash
python3 scripts/validate_black_hat_output.py path/to/black_hat_output.json
```
