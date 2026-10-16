# Bid / No-Bid Decision Brief: {{opportunity_title}}

## Executive decision
| Decision point | Current call |
|---|---|
| Recommendation | `{{recommendation}}` |
| Pursuit path | {{selected_path}} |
| P(win given bid) | {{pwin}} |
| Expected value | {{expected_value}} |
| Confidence | {{confidence}} |
| Primary action | {{primary_action}} |

## Why this is the call
{{rationale_summary}}

## Pursuit context
| Field | Value |
|---|---|
| Buyer / office | {{buyer_office}} |
| Opportunity / timing | {{opportunity_timing}} |
| Value basis | {{value_basis}} |
| Access path | {{set_aside_vehicle}} |
| Key gate requirements | {{required_credentials}} |

## Gate calls
| Scenario | Call | Decision implication |
|---|---|---|
{{gate_rows}}

## Selected factor readout
Use this compact table for the decision-moving factors. Keep full factor evidence, flags, row-level scores, and scenario details in JSON/CSV companion artifacts.

| Factor | Posture | Score / confidence | Decision implication |
|---|---|---:|---|
{{factor_rows}}

## Scenario options
| Path | Call | P(win) / EV | What it means |
|---|---|---:|---|
{{scenario_rows}}

## Economics and win view
{{economics_summary}}

## Risks to close
{{missing_data_and_risks}}

## Recommended next actions
{{recommended_actions}}

## Companion artifacts
Full details: {{companion_artifacts}}
