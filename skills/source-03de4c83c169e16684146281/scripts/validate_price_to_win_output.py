#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

REQUIRED_OUTPUT_KEYS = {
    "opportunity_title",
    "executive_decision",
    "executive_takeaway",
    "ptw_range",
    "reconciliation",
    "customer_price_position",
    "evidence_digest",
    "likely_competitors",
    "pricing_levers",
    "data_gaps",
    "recommended_actions",
}

REQUIRED_DECISION_KEYS = {
    "target_range",
    "proposed_price_posture",
    "confidence",
    "primary_pricing_action",
}

REQUIRED_SCENARIOS = {
    "aggressive",
    "competitive_midpoint",
    "premium_value",
}

REQUIRED_RECONCILIATION_VIEWS = {
    "top_down",
    "bottom_up",
    "reconciled",
}

CONFIDENCE_VALUES = {
    "high",
    "moderate-high",
    "moderate",
    "medium",
    "moderate-low",
    "low",
}


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and not math.isnan(value)


def require_object(errors: list[str], payload: dict[str, Any], key: str, path: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        errors.append(f"{path}.{key} must be an object.")
        return {}

    return value


def require_list(errors: list[str], payload: dict[str, Any], key: str, path: str, min_count: int = 0) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        errors.append(f"{path}.{key} must be a list.")
        return []

    if len(value) < min_count:
        errors.append(f"{path}.{key} must contain at least {min_count} item(s).")

    return value


def require_string(errors: list[str], payload: dict[str, Any], key: str, path: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key} must be a non-empty string.")
        return ""

    return value.strip()


def require_number(
    errors: list[str],
    payload: dict[str, Any],
    key: str,
    path: str,
    low: float | None = None,
    high: float | None = None,
) -> float | None:
    value = payload.get(key)
    if not is_number(value):
        errors.append(f"{path}.{key} must be numeric.")
        return None

    numeric = float(value)
    if low is not None and numeric < low:
        errors.append(f"{path}.{key} must be >= {low}.")
    if high is not None and numeric > high:
        errors.append(f"{path}.{key} must be <= {high}.")

    return numeric


def validate_executive_decision(
    errors: list[str],
    warnings: list[str],
    payload: dict[str, Any],
    expect_confidence: str | None,
) -> None:
    decision = require_object(errors, payload, "executive_decision", "$")
    if not decision:
        return

    missing = REQUIRED_DECISION_KEYS - set(decision)
    if missing:
        errors.append(f"$.executive_decision missing keys: {sorted(missing)}.")

    target_range = require_string(errors, decision, "target_range", "$.executive_decision")
    require_string(errors, decision, "proposed_price_posture", "$.executive_decision")
    confidence = require_string(errors, decision, "confidence", "$.executive_decision").lower()
    require_string(errors, decision, "primary_pricing_action", "$.executive_decision")

    if expect_confidence and confidence != expect_confidence:
        errors.append(f"Expected confidence {expect_confidence}, got {confidence}.")
    if confidence and confidence not in CONFIDENCE_VALUES:
        warnings.append("$.executive_decision.confidence should use a standard confidence label.")
    if target_range and not any(char.isdigit() for char in target_range):
        warnings.append("$.executive_decision.target_range should include a numeric range or target.")


def validate_scenarios(errors: list[str], warnings: list[str], payload: dict[str, Any]) -> None:
    scenarios = require_object(errors, payload, "ptw_range", "$")
    if not scenarios:
        return

    scenario_keys = set(scenarios)
    missing = REQUIRED_SCENARIOS - scenario_keys
    if missing:
        errors.append(f"$.ptw_range missing scenarios: {sorted(missing)}.")

    if not scenario_keys <= REQUIRED_SCENARIOS:
        warnings.append(f"$.ptw_range contains non-standard scenarios: {sorted(scenario_keys - REQUIRED_SCENARIOS)}.")

    high_values: dict[str, float] = {}
    low_values: dict[str, float] = {}

    for scenario_key in sorted(REQUIRED_SCENARIOS):
        scenario = scenarios.get(scenario_key)
        path = f"$.ptw_range.{scenario_key}"
        if not isinstance(scenario, dict):
            if scenario_key in scenarios:
                errors.append(f"{path} must be an object.")
            continue

        require_string(errors, scenario, "label", path)
        low = require_number(errors, scenario, "low", path, low=0.0)
        high = require_number(errors, scenario, "high", path, low=0.0)
        require_string(errors, scenario, "when_to_use", path)
        require_string(errors, scenario, "main_risk", path)

        if low is not None and high is not None:
            low_values[scenario_key] = low
            high_values[scenario_key] = high
            if low > high:
                errors.append(f"{path}.low must be <= {path}.high.")

    if {"aggressive", "competitive_midpoint", "premium_value"} <= set(low_values):
        if low_values["aggressive"] > low_values["competitive_midpoint"]:
            warnings.append("aggressive scenario starts above the competitive midpoint scenario.")
        if low_values["competitive_midpoint"] > low_values["premium_value"]:
            warnings.append("competitive midpoint scenario starts above the premium scenario.")


def validate_reconciliation(errors: list[str], payload: dict[str, Any]) -> None:
    reconciliation = require_object(errors, payload, "reconciliation", "$")
    if not reconciliation:
        return

    missing = REQUIRED_RECONCILIATION_VIEWS - set(reconciliation)
    if missing:
        errors.append(f"$.reconciliation missing views: {sorted(missing)}.")

    for view_key in sorted(REQUIRED_RECONCILIATION_VIEWS):
        view = reconciliation.get(view_key)
        path = f"$.reconciliation.{view_key}"
        if not isinstance(view, dict):
            if view_key in reconciliation:
                errors.append(f"{path} must be an object.")
            continue

        require_string(errors, view, "range", path)
        require_string(errors, view, "signal", path)
        require_string(errors, view, "decision_implication", path)


def validate_evidence_digest(errors: list[str], warnings: list[str], payload: dict[str, Any]) -> None:
    digest = require_list(errors, payload, "evidence_digest", "$", min_count=1)
    if len(digest) > 6:
        warnings.append("$.evidence_digest has more than 6 rows; use companion artifacts for full evidence.")

    seen_sources: set[str] = set()
    for index, item in enumerate(digest):
        path = f"$.evidence_digest[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object.")
            continue

        require_string(errors, item, "signal", path)
        value_basis = require_string(errors, item, "value_basis", path)
        require_string(errors, item, "ptw_implication", path)
        source = require_string(errors, item, "source", path)
        if source:
            seen_sources.add(source)
        if value_basis and "ceiling" in value_basis.lower() and "only" not in value_basis.lower():
            warnings.append(f"{path}.value_basis mentions a ceiling; confirm it is labeled correctly.")

    if len(seen_sources) < 2 and len(digest) > 1:
        warnings.append("$.evidence_digest should normally cite more than one source.")


def validate_competitors(errors: list[str], warnings: list[str], payload: dict[str, Any]) -> None:
    competitors = require_list(errors, payload, "likely_competitors", "$", min_count=1)

    for index, competitor in enumerate(competitors):
        path = f"$.likely_competitors[{index}]"
        if not isinstance(competitor, dict):
            errors.append(f"{path} must be an object.")
            continue

        require_string(errors, competitor, "name", path)
        require_string(errors, competitor, "observed_evidence", path)
        pricing_posture = require_string(errors, competitor, "inferred_pricing_posture", path)
        require_string(errors, competitor, "recommended_response", path)

        if pricing_posture and not pricing_posture.lower().startswith(("inferred", "observed")):
            warnings.append(f"{path}.inferred_pricing_posture should label whether the posture is inferred or observed.")


def validate_non_empty_string_list(
    errors: list[str],
    payload: dict[str, Any],
    key: str,
    min_count: int,
) -> None:
    items = require_list(errors, payload, key, "$", min_count=min_count)
    for index, item in enumerate(items):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"$.{key}[{index}] must be a non-empty string.")


def validate_output(
    payload: dict[str, Any],
    expect_confidence: str | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = REQUIRED_OUTPUT_KEYS - set(payload)
    if missing:
        errors.append(f"Missing output keys: {sorted(missing)}.")

    require_string(errors, payload, "opportunity_title", "$")
    require_string(errors, payload, "executive_takeaway", "$")
    require_string(errors, payload, "customer_price_position", "$")

    proposed_price = payload.get("proposed_price_millions")
    if proposed_price is not None and not is_number(proposed_price):
        errors.append("$.proposed_price_millions must be numeric when present.")
    elif is_number(proposed_price) and float(proposed_price) <= 0:
        errors.append("$.proposed_price_millions must be greater than 0 when present.")

    validate_executive_decision(errors, warnings, payload, expect_confidence)
    validate_scenarios(errors, warnings, payload)
    validate_reconciliation(errors, payload)
    validate_evidence_digest(errors, warnings, payload)
    validate_competitors(errors, warnings, payload)
    validate_non_empty_string_list(errors, payload, "pricing_levers", min_count=1)
    validate_non_empty_string_list(errors, payload, "data_gaps", min_count=1)
    validate_non_empty_string_list(errors, payload, "recommended_actions", min_count=1)

    if payload.get("comparable_universe_count") is not None:
        comparable_count = require_number(errors, payload, "comparable_universe_count", "$", low=0.0)
        if comparable_count is not None and comparable_count > len(payload.get("evidence_digest", [])):
            if not payload.get("full_evidence_artifact"):
                warnings.append("comparable_universe_count exceeds evidence digest count; full_evidence_artifact should be named.")

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate GovTribe price-to-win structured JSON output.",
    )
    parser.add_argument("output_path", help="Path to structured price-to-win JSON output.")
    parser.add_argument("--expect-confidence", choices=sorted(CONFIDENCE_VALUES))
    parser.add_argument("--pretty", action="store_true", help="Print a formatted validation summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        payload = json.loads(Path(args.output_path).read_text())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"errors": [f"Could not read JSON: {exc}"], "warnings": []}), file=sys.stderr)
        return 1

    errors, warnings = validate_output(payload, expect_confidence=args.expect_confidence)
    decision = payload.get("executive_decision", {}) if isinstance(payload.get("executive_decision"), dict) else {}

    summary = {
        "opportunityTitle": payload.get("opportunity_title"),
        "recommendedTarget": decision.get("target_range"),
        "confidence": decision.get("confidence"),
        "evidenceDigestCount": len(payload.get("evidence_digest", [])) if isinstance(payload.get("evidence_digest"), list) else 0,
        "competitorCount": len(payload.get("likely_competitors", [])) if isinstance(payload.get("likely_competitors"), list) else 0,
        "errors": errors,
        "warnings": warnings,
    }

    if args.pretty:
        print(json.dumps(summary, indent=2))
    else:
        print(json.dumps(summary))

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
