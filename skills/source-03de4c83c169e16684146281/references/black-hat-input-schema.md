---
title: Black Hat Input Schema
description: Canonical JSON payload for the deterministic black hat engine.
---

# Black Hat Input Schema

Use this reference with `scripts/black_hat_engine.py` when the workflow needs deterministic bidder ranking, factor scorecards, counter-move scoring, and JSON-safe output.

## Top-level payload

```json
{
  "evaluation_model": {},
  "opportunity": {},
  "bidders": [],
  "our_team_vendor_id": "vendor-123",
  "pricing": {},
  "settings": {}
}
```

## Required minimum fields

### `evaluation_model`
- `factors`
- `requirements`

### `opportunity`
- `id`
- `agency`
- `contract_type`

### `bidders`
- at least one bidder
- each bidder needs `vendor_id` and `name`

### `our_team_vendor_id`
- must match one bidder `vendor_id` when you want `our_position` to be populated

The engine will run with sparse inputs, but bidder ranking and counter-moves degrade quickly without price samples, award history, and usable atomic requirements.

## High-value optional fields

### `evaluation_model`
- `eval_method`
- `required_vehicle`
- `estimated_value`
- factor `weight`
- factor `minimum_acceptability`
- requirement `factor`
- requirement `weight`
- requirement `required_clearance`
- requirement `required_place`

### `opportunity`
- `buyer`
- `office`
- `description`
- `place_of_performance`
- `set_aside`
- `required_vehicle`
- `estimated_value`
- `due_date`

### `bidders[]`
- `capabilities_text`
- `vehicles`
- `clearances`
- `certifications`
- `socio_statuses`
- `places`
- `awards`
- `is_incumbent`
- `teammates`
- `momentum_score`
- `engagement_score`
- `likely_role`

### `pricing`
- `samples_by_vendor`
- `realism_risk_by_vendor`
- `our_margin_floor`
- `our_expected_margin`

### `settings`
- `bid_probability_weights`
- `overall_score_weights`
- `price_position_weight`
- `human_override`
- `top_bidder_count`
- `lpta_acceptability_threshold`

## Output contract

```json
{
  "evaluation_model": {},
  "predicted_bidders": [],
  "competitor_assessments": [],
  "our_position": {},
  "price_to_win": {},
  "recommended_actions": [],
  "confidence_summary": {},
  "evidence_ledger": []
}
```

## Example payload

```json
{
  "evaluation_model": {
    "eval_method": "tradeoff",
    "required_vehicle": "GSA OASIS SB",
    "estimated_value": 22000000,
    "factors": [
      {"id": "technical", "name": "Technical Approach", "weight": 0.4},
      {"id": "past_performance", "name": "Past Performance", "weight": 0.25},
      {"id": "management", "name": "Management and Staffing", "weight": 0.2},
      {"id": "price", "name": "Price", "weight": 0.15}
    ],
    "requirements": [
      {"id": "req-1", "factor": "technical", "text": "Provide cleared cyber operations support.", "weight": 1.0, "required_clearance": "Secret"},
      {"id": "req-2", "factor": "management", "text": "Demonstrate transition and staffing readiness.", "weight": 0.8}
    ]
  },
  "opportunity": {
    "id": "opp-001",
    "agency": "Department of the Air Force",
    "buyer": "Department of the Air Force",
    "office": "AFLCMC/HB",
    "description": "Cyber operations support recompete.",
    "contract_type": "FFP",
    "required_vehicle": "GSA OASIS SB",
    "estimated_value": 22000000,
    "place_of_performance": "CONUS",
    "set_aside": "8(a)"
  },
  "bidders": [
    {
      "vendor_id": "our-team",
      "name": "Blue Forge Federal",
      "capabilities_text": "Cyber operations, systems engineering, and transition support for mission programs.",
      "vehicles": ["GSA OASIS SB"],
      "clearances": ["Secret", "Top Secret"],
      "certifications": ["ISO 27001"],
      "socio_statuses": ["8(a)"],
      "places": ["CONUS"],
      "is_incumbent": false,
      "teammates": ["signal-ridge"],
      "momentum_score": 0.72,
      "engagement_score": 0.81,
      "awards": [
        {
          "award_id": "pp-001",
          "agency": "Department of the Air Force",
          "office": "AFLCMC/HB",
          "description": "Cleared cyber operations support services.",
          "value": 18000000,
          "contract_type": "FFP",
          "end_date": "2025-09-30",
          "cpars_rating": 4.4,
          "official_source": true,
          "cross_source_agreement": 0.8
        }
      ]
    },
    {
      "vendor_id": "incumbent",
      "name": "Incumbent Systems LLC",
      "capabilities_text": "Incumbent cyber operations and sustainment support for Air Force mission systems.",
      "vehicles": ["GSA OASIS SB"],
      "clearances": ["Secret"],
      "places": ["CONUS"],
      "is_incumbent": true,
      "momentum_score": 0.78,
      "engagement_score": 0.65,
      "awards": [
        {
          "award_id": "pp-010",
          "agency": "Department of the Air Force",
          "office": "AFLCMC/HB",
          "description": "Incumbent cyber operations support contract.",
          "value": 21000000,
          "contract_type": "FFP",
          "end_date": "2026-03-31",
          "cpars_rating": 4.7,
          "official_source": true,
          "cross_source_agreement": 0.9
        }
      ]
    }
  ],
  "our_team_vendor_id": "our-team",
  "pricing": {
    "samples_by_vendor": {
      "our-team": [20500000, 21400000, 21900000],
      "incumbent": [19800000, 20600000, 21100000]
    },
    "realism_risk_by_vendor": {
      "our-team": 0.25,
      "incumbent": 0.15
    },
    "our_margin_floor": 0.12,
    "our_expected_margin": 0.15
  },
  "settings": {
    "top_bidder_count": 5,
    "human_override": 0.0
  }
}
```

## Example usage

```bash
python3 scripts/black_hat_engine.py payload.json --pretty
```
