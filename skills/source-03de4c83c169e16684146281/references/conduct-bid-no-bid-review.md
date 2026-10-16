---
title: Conduct Bid / No-Bid Review
description: How to run a gated, evidence-weighted bid / no-bid or go/no-go review for one opportunity or pursuit.
---

# Conduct Bid / No-Bid Review

Use this reference when the user wants a disciplined bid / no-bid decision for one specific opportunity or pursuit. Treat "go/no-go" and "go no go" as customer-facing language for the same decision family unless the user defines a different gate.

## Goal
- Resolve the target pursuit, normalize the relevant market, buyer, and contractor context, and recommend the best pursuit posture using explicit gates, factor scoring, and an economic view.
- Keep the workflow evidence-backed and recommendation-first. The point is to decide whether and how to pursue, not to produce a generic opportunity summary.
- For a document-style deliverable, prefer the structure in `assets/bid-no-bid-brief-template.md` from the skill root.
- Before delivering a customer-facing brief or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).

## Minimum input contract
- Required: one specific opportunity or one pursuit that resolves to a specific opportunity or requirement.
- Required: our company, team, or teammate context.
- Helpful: incumbent hypothesis, likely bidder list, uploaded requirement files, proposal timing, bid-cost assumptions, margin floor, and strategic priorities.
- Helpful only when relevant: prior capability statements, past performance summaries, proposal outlines, debrief notes, or reusable company-context files. Read `references/prior-user-file-context.md` before searching for them.
- If the target opportunity or our side does not resolve cleanly enough to evaluate, ask for the minimum missing detail and stop.

## Workflow

### 1. Resolve the target pursuit on the right market surface
- If the user starts from a pursuit, recover the linked opportunity, requirement, or best available pursued work first.
- Federal contract path: resolve the opportunity and keep buyer, office, NAICS, PSC, contract type, vehicle, set-aside, estimated value, period of performance, due date, phase, and evaluation structure.
- Federal grant path: resolve the opportunity or program and keep awarding agency, program, assistance structure, recipient eligibility, timing, value, and evaluation structure.
- State and local path: resolve the opportunity with buyer, jurisdiction, category, vehicle, geography, value, timing, and evaluation structure.
- Use the bundled [federal contract](./govtribe-docs-federal-contract-data-model.md), [federal grant](./govtribe-docs-federal-grant-data-model.md), and [state and local contract](./govtribe-docs-state-and-local-contract-data-model.md) references for stable data-model guidance. Call `Documentation` when the current tool schema or freshness-sensitive behavior matters.

### 2. Normalize the review into one pursuit view
- Build one canonical pursuit view with three blocks:
  - opportunity block: target requirement, buyer, office or jurisdiction, work dimensions, contract or funding structure, timing, evaluation factors, and compliance gates
  - buyer-history block: comparable awards, incumbent behavior, switching rate, concentration, value bands, set-aside posture, and contract or funding preferences
  - contractor-profile block: capabilities, vehicles, clearances, certifications, socioeconomic status, relevant awards, prime versus sub history, customer footprint, staffing capacity, proposal readiness, margin floor, bid cost, and strategic priorities
- Collapse buyer names and office structures to stable identities before scoring.
- Separate base awards from modifications before using award history for buyer-behavior or pricing conclusions.
- Treat IDIQ ceiling as distinct from realistic order value or expected share. Do not let ceiling stand in for expected economics.
- Distinguish prime past performance from sub past performance instead of flattening them together.

### 3. Ground the buyer-history block with bounded comparable awards
- Run a same-buyer comparable-awards pass before over-weighting generic market evidence.
- Prefer the closest practical buyer scope: same office, program, buying lane, awarding office, or jurisdiction before broader agency-level history.
- Keep the comparable slice close to the work pattern using the strongest available combination of scope, NAICS, PSC, program, vehicle, IDV, set-aside posture, geography, contract type, and value band.
- Keep the window recent enough to matter, usually the last 24 to 36 months unless the buyer history is too thin.
- Use this pass to ground likely winning vendors, incumbent strength, switching behavior, contract-type preference, set-aside usage, and pricing pressure.
- Use the `govtribe-pricing-data` skill only when comparable-award pricing evidence materially sharpens the price-to-win and margin view.

### 4. Run hard gates before scoring
- Check hard gates first:
  - set-aside, eligibility, vehicle, or access-path fit
  - required clearances, certifications, labor constraints, and place-of-performance requirements
  - obvious OCI, responsibility, or execution blockers
  - credible ability to field labor, key personnel, transition, and delivery coverage
  - plausible path to the required relevant past performance examples
  - ability to price inside a competitive band without breaking margin floor or delivery reality
  - enough time, artifacts, and proposal readiness to submit a compliant response
- If a critical gate fails, do not bury it inside a blended score. Let it drive the recommendation toward "NO_BID", "BID_WITH_PARTNER", "SUB_ONLY", or "MONITOR_AND_SHAPE".
- Penalize missing data instead of filling it with optimism.

### 5. Score the opportunity the way the buyer is likely to evaluate it
- Mirror the solicitation's actual evaluation structure whenever the evaluation factors or Section M equivalent are available.
- When the final evaluation structure is not available, use this best-value services default and then override it when better evidence appears:
  - customer or buyer fit: `0.15`
  - capability or technical fit: `0.20`
  - past performance relevance: `0.15`
  - price-to-win or margin fit: `0.20`
  - competitive position: `0.10`
  - delivery or staffing risk: `0.10`
  - strategic value: `0.05`
  - proposal readiness: `0.05`
- Keep these factor families explicit:
  - customer or buyer fit
  - capability or technical fit
  - past performance relevance
  - price-to-win or margin fit
  - competitive position
  - delivery or staffing risk
  - strategic value
  - proposal readiness
- When the buyer or solicitation makes small-business participation material, keep it explicit instead of hiding it inside technical fit.
- For labor-heavy professional-services work, raise a compensation or realism flag when FAR `52.222-46` or equivalent compensation realism logic is materially in play.
- Weight readiness more heavily as the due date compresses.

### 6. Use explicit scoring logic for the highest-value factors
- Past performance relevance:
  - score examples on requirement similarity, recency, dollar-size fit, contract or assistance structure fit, buyer adjacency, and prime versus sub role
  - aggregate the top three examples, not the average of all examples
  - use `references/past-performance-match.md` when the comparable-reference question needs a deeper pass
- Price-to-win or margin fit:
  - build a comparable cohort from the strongest same-buyer and same-lane evidence
  - estimate low, median, and high likely winning bands
  - score high only when the contractor can land in the credible winning band and remain executable
- Competitive position:
  - penalize strong incumbency, concentrated buyers, and crowded serious-bidder fields
  - boost only when the contractor has a believable discriminator that maps to the buyer's likely evaluation story
  - use `references/gao-bid-protest-evidence.md` when protest history, agency outcomes, or a linked procurement dispute could materially change competitive risk
- If the competitive field is missing or too thin, build it first with `references/likely-bidders.md`.

### 7. Compute both decision posture and economic posture
- Convert the factor view into both:
  - `P(win | bid)`
  - expected value
- Use an expected-value frame like:
  - `EV = P(win) * expected_gross_profit - bid_cost - opportunity_cost - risk_reserve`
- Base expected gross profit on realistic order value, not IDIQ ceiling.
- Increase the risk reserve when staffing, transition, compliance, or pricing gaps remain material.
- Keep the arithmetic deterministic and evidence-backed. Let the model synthesize and explain; do not invent unsupported math.

### 8. Run scenario analysis before issuing the recommendation
- Score at least these scenarios:
  - prime solo
  - prime with best-fit teammate
  - sub only
  - monitor and shape
- Use teammate scenarios to test whether partner access closes hard gaps around vehicle, set-aside, past performance, staffing, or buyer position.
- If a partnered scenario is the most credible path, use `references/team-on-an-opportunity.md` to discover who has already created a teaming interest on the opportunity and coordinate matches.
- If the recommendation still looks ambiguous after the scenario pass, use `references/conduct-black-hat-review.md` to pressure-test the competitive posture before finalizing.

### 9. Adjudicate to a formal recommendation
- Use these formal outputs:
  - `BID`
  - "BID_WITH_PARTNER"
  - "SUB_ONLY"
  - "MONITOR_AND_SHAPE"
  - "NO_BID"
- Use these seed thresholds as starting guidance, then adjust when better internal history exists:
  - `BID`: hard gates pass, `P(win | bid)` is credibly high, expected value is positive, and readiness is adequate
  - "BID_WITH_PARTNER": solo path is weak, but the partnered path clears the key gates and decision thresholds
  - "SUB_ONLY": the work is worth pursuing, but the prime posture is not credible while a sub position is
  - "MONITOR_AND_SHAPE": the work is early, strategic, or influenceable, but current readiness, economics, or competitiveness do not justify a bid commitment yet
  - "NO_BID": hard gate failure, negative economics, or an unsupported win path
- If the evidence is too thin for a defensible bid recommendation, stop at missing-data warnings or "MONITOR_AND_SHAPE" instead of forcing a premature answer.

## Output contract
- Return:
  - recommendation
  - short rationale summary
  - gate failures or pass notes
  - factor breakdown with score posture, evidence, confidence, and flags
  - `P(win | bid)` view
  - expected-value view
  - missing-data warnings
  - recommended next actions
  - scenario results for prime solo, prime with teammate, sub only, and monitor and shape
- Use compact markdown tables where they materially improve readability.
- Make rendered briefs read like decision memos, not raw engine dumps. Open with an executive decision block that includes recommendation, pursuit path, `P(win | bid)`, expected value, confidence, and the primary action.
- Keep document tables readable in portrait Markdown/PDF output. Use compact tables for gate calls, scenario options, and selected factor posture.
- Keep the pursuit context table short enough to avoid page splits; combine opportunity/timing and access-path details instead of listing every field separately.
- In the brief, summarize scenario options with columns like `Path`, `Call`, `P(win) / EV`, and `What it means` instead of exposing every engine metric.
- In the brief, summarize only the decision-moving factor posture by default, using columns like `Factor`, `Posture`, `Score / confidence`, and `Decision implication`.
- Put row-level factor evidence, flags, next-action details, full weighted scores, and full scenario JSON in companion JSON or CSV artifacts instead of forcing every engine field into the rendered brief.
- If companion artifact links create a trailing blank page in a rendered PDF, omit them from the rendered brief and provide them in the final response instead.
- Keep the recommendation explicit, the evidence traceable, and the missing data visible.
- Do not mutate pursuits, move stages, or create pipeline records unless the user explicitly asks in a later step.

## Deterministic asset
- From the skill root, use `scripts/bid_no_bid_engine.py` with `references/bid-no-bid-input-schema.md` when the workflow needs reproducible scoring, scenario comparison, or UI-safe JSON output.
- When engine output is produced, validate it before final delivery:

```bash
python3 scripts/validate_bid_no_bid_output.py path/to/bid_no_bid_output.json
```
