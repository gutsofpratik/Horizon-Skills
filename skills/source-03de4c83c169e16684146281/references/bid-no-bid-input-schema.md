---
title: Bid / No-Bid Input Schema
description: Canonical JSON payload for the deterministic bid / no-bid engine.
---

# Bid / No-Bid Input Schema

Use this reference with `scripts/bid_no_bid_engine.py` when the workflow needs deterministic scoring, scenario comparison, and JSON-safe output.

## Top-level payload

```json
{
  "opportunity": {},
  "buyer_history": {},
  "contractor_profile": {},
  "teammates": [],
  "settings": {}
}
```

## Required minimum fields

### `opportunity`
- `buyer`
- `office`
- `description`

### `contractor_profile`
- `name`

The engine will run with a thin payload, but the output degrades quickly without pricing, past performance, and readiness inputs.

## High-value optional fields

### `opportunity`
- `opportunity_id`
- `naics`
- `psc`
- `contract_type`
- `estimated_value`
- `realistic_order_value`
- `set_aside`
- `vehicle_required`
- `due_date`
- `phase`
- `required_capabilities`
- `required_clearances`
- `required_certifications`
- `evaluation_weights`
- `small_business_participation_material`
- `far_5222246_included`
- `incumbent_vendor`
- `transition_complexity`
- `recruiting_difficulty`
- `key_personnel_coverage_score`

### `buyer_history`
- `comparable_awards`
- `price_band.low`
- `price_band.median`
- `price_band.high`
- `price_band.comparable_count`
- `concentration`
- `switching_rate`
- `competitors`

### `contractor_profile`
- `capabilities`
- `clearances`
- `certifications`
- `vehicles`
- `socio_statuses`
- `awards`
- `available_fte`
- `margin_floor`
- `bid_cost`
- `opportunity_cost`
- `proposal_assets_score`
- `strategic_priority_score`
- `expected_margin_at_market_price`
- `expected_margin_at_low_price`
- `expected_margin_at_high_price`
- `differentiators`

### `teammates`
- Same shape as `contractor_profile`
- Used to test the `prime with best-fit teammate` scenario

### `settings`
- `weights`
- `pwin_floor_bid`
- `pwin_floor_partner`
- `readiness_floor_bid`
- `sub_only_share_estimate`
- `monitor_shaping_cost`
- `strategic_floor_monitor`

## Example payload

```json
{
  "opportunity": {
    "opportunity_id": "opp-001",
    "buyer": "Department of the Air Force",
    "office": "AFLCMC/HB",
    "description": "Provide cyber operations support, cleared engineering staff, and transition services for a recompete.",
    "contract_type": "FFP",
    "estimated_value": 18000000,
    "realistic_order_value": 15000000,
    "set_aside": "8(a)",
    "vehicle_required": "GSA OASIS SB",
    "due_date": "2026-05-15",
    "phase": "solicitation",
    "required_capabilities": ["cyber operations", "program management", "systems engineering"],
    "required_clearances": ["Secret"],
    "required_certifications": ["ISO 27001"],
    "small_business_participation_material": true,
    "far_5222246_included": true,
    "incumbent_vendor": "Incumbent Systems LLC",
    "transition_complexity": 60,
    "recruiting_difficulty": 55,
    "key_personnel_coverage_score": 70
  },
  "buyer_history": {
    "price_band": {
      "low": 13500000,
      "median": 15200000,
      "high": 16800000,
      "comparable_count": 14
    },
    "concentration": 0.42,
    "switching_rate": 0.35,
    "competitors": [
      {"name": "Incumbent Systems LLC", "is_incumbent": true, "strength_score": 85},
      {"name": "Vector Mission Partners", "strength_score": 72}
    ],
    "comparable_awards": [
      {
        "award_id": "awd-001",
        "buyer": "Department of the Air Force",
        "office": "AFLCMC/HB",
        "description": "Cyber operations and cleared program support services.",
        "contract_type": "FFP",
        "value": 14800000,
        "award_date": "2024-02-01",
        "is_prime": true
      }
    ]
  },
  "contractor_profile": {
    "name": "Blue Forge Federal",
    "capabilities": ["cyber operations", "systems engineering", "program management"],
    "clearances": ["Secret", "Top Secret"],
    "certifications": ["ISO 27001"],
    "vehicles": ["GSA OASIS SB"],
    "socio_statuses": ["8(a)"],
    "available_fte": 10,
    "margin_floor": 0.12,
    "bid_cost": 180000,
    "opportunity_cost": 40000,
    "proposal_assets_score": 78,
    "strategic_priority_score": 82,
    "expected_margin_at_market_price": 0.15,
    "differentiators": ["same-office cyber ops delivery", "cleared surge staffing"],
    "awards": [
      {
        "award_id": "pp-001",
        "buyer": "Department of the Air Force",
        "office": "AFLCMC/HB",
        "description": "Delivered cleared cyber operations support and systems engineering services.",
        "contract_type": "FFP",
        "value": 13900000,
        "award_date": "2025-01-10",
        "is_prime": true
      }
    ]
  },
  "teammates": [
    {
      "name": "Signal Ridge Partners",
      "capabilities": ["cyber operations", "intel support"],
      "clearances": ["Secret"],
      "certifications": ["ISO 27001"],
      "vehicles": ["GSA OASIS SB", "8(a) STARS III"],
      "socio_statuses": ["8(a)"],
      "available_fte": 6,
      "bid_cost": 40000,
      "opportunity_cost": 15000,
      "proposal_assets_score": 70,
      "strategic_priority_score": 72,
      "expected_margin_at_market_price": 0.13
    }
  ],
  "settings": {
    "sub_only_share_estimate": 0.3
  }
}
```

## Example usage

```bash
python3 scripts/bid_no_bid_engine.py payload.json --pretty
```
