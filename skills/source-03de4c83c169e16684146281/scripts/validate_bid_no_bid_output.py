#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ALLOWED_RECOMMENDATIONS = {
    "BID",
    "BID_WITH_PARTNER",
    "SUB_ONLY",
    "MONITOR_AND_SHAPE",
    "NO_BID",
}

REQUIRED_SCENARIOS = {
    "prime_solo",
    "prime_with_teammate",
    "sub_only",
    "monitor_and_shape",
}

REQUIRED_FACTORS = {
    "customer_fit",
    "capability_fit",
    "past_performance",
    "price_fit",
    "competition",
    "delivery",
    "strategy",
    "readiness",
}


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and not math.isnan(value)


def require_number(
    errors: list[str],
    payload: dict[str, Any],
    key: str,
    path: str,
    low: float | None = None,
    high: float | None = None,
) -> None:
    value = payload.get(key)
    if not is_number(value):
        errors.append(f"{path}.{key} must be numeric.")
        return

    if low is not None and value < low:
        errors.append(f"{path}.{key} must be >= {low}.")
    if high is not None and value > high:
        errors.append(f"{path}.{key} must be <= {high}.")


def require_string(errors: list[str], payload: dict[str, Any], key: str, path: str) -> None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key} must be a non-empty string.")


def validate_factor(errors: list[str], warnings: list[str], factor: dict[str, Any], path: str) -> None:
    require_string(errors, factor, "name", path)
    require_number(errors, factor, "score", path, low=0.0, high=100.0)
    require_number(errors, factor, "confidence", path, low=0.0, high=1.0)
    require_string(errors, factor, "rationale", path)

    if not isinstance(factor.get("evidence"), list):
        errors.append(f"{path}.evidence must be a list.")
    if not isinstance(factor.get("flags"), list):
        errors.append(f"{path}.flags must be a list.")

    if factor.get("name") in {"price_fit", "past_performance", "competition"} and not factor.get("evidence"):
        warnings.append(f"{path} has no evidence entries for a high-value factor.")


def validate_scenario(errors: list[str], warnings: list[str], scenario: dict[str, Any], path: str) -> None:
    require_string(errors, scenario, "scenarioKey", path)
    require_string(errors, scenario, "scenarioDisplayName", path)
    require_number(errors, scenario, "weightedScore", path, low=0.0, high=100.0)
    require_number(errors, scenario, "pwin", path, low=0.0, high=1.0)
    require_number(errors, scenario, "expectedValue", path)
    require_number(errors, scenario, "confidence", path, low=0.0, high=1.0)

    recommendation = scenario.get("recommendation")
    if recommendation not in ALLOWED_RECOMMENDATIONS:
        errors.append(f"{path}.recommendation must be one of {sorted(ALLOWED_RECOMMENDATIONS)}.")

    gate_failures = scenario.get("gateFailures")
    if not isinstance(gate_failures, list):
        errors.append(f"{path}.gateFailures must be a list.")
        gate_failures = []

    if gate_failures and recommendation in {"BID", "BID_WITH_PARTNER"}:
        errors.append(f"{path} recommends {recommendation} despite gate failures.")
    if gate_failures and recommendation == "SUB_ONLY":
        warnings.append(f"{path} recommends SUB_ONLY with gate failures; confirm they do not block a sub role.")

    next_actions = scenario.get("nextActions")
    if not isinstance(next_actions, list):
        errors.append(f"{path}.nextActions must be a list.")

    factors = scenario.get("factorResults")
    if not isinstance(factors, list):
        errors.append(f"{path}.factorResults must be a list.")
        return

    factor_names = {factor.get("name") for factor in factors if isinstance(factor, dict)}
    if factor_names != REQUIRED_FACTORS:
        errors.append(f"{path}.factorResults must contain exactly {sorted(REQUIRED_FACTORS)}.")

    for index, factor in enumerate(factors):
        if not isinstance(factor, dict):
            errors.append(f"{path}.factorResults[{index}] must be an object.")
            continue
        validate_factor(errors, warnings, factor, f"{path}.factorResults[{index}]")


def validate_output(
    payload: dict[str, Any],
    expect_recommendation: str | None = None,
    expect_selected_scenario: str | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    recommendation = payload.get("recommendation")
    if recommendation not in ALLOWED_RECOMMENDATIONS:
        errors.append(f"recommendation must be one of {sorted(ALLOWED_RECOMMENDATIONS)}.")

    if expect_recommendation and recommendation != expect_recommendation:
        errors.append(f"Expected recommendation {expect_recommendation}, got {recommendation}.")

    require_string(errors, payload, "selectedScenarioKey", "$")
    require_string(errors, payload, "selectedScenarioDisplayName", "$")
    require_number(errors, payload, "pwin", "$", low=0.0, high=1.0)
    require_number(errors, payload, "expectedValue", "$")
    require_number(errors, payload, "confidence", "$", low=0.0, high=1.0)

    if not isinstance(payload.get("missingDataWarnings"), list):
        errors.append("missingDataWarnings must be a list.")

    scenarios = payload.get("scenarios")
    if not isinstance(scenarios, list):
        errors.append("scenarios must be a list.")
        return errors, warnings

    scenario_keys = {scenario.get("scenarioKey") for scenario in scenarios if isinstance(scenario, dict)}
    if scenario_keys != REQUIRED_SCENARIOS:
        errors.append(f"scenarios must contain exactly {sorted(REQUIRED_SCENARIOS)}.")

    selected_key = payload.get("selectedScenarioKey")
    if expect_selected_scenario and selected_key != expect_selected_scenario:
        errors.append(f"Expected selected scenario {expect_selected_scenario}, got {selected_key}.")

    selected: dict[str, Any] | None = None
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"scenarios[{index}] must be an object.")
            continue
        if scenario.get("scenarioKey") == selected_key:
            selected = scenario
        validate_scenario(errors, warnings, scenario, f"scenarios[{index}]")

    if selected is None:
        errors.append("selectedScenarioKey does not match a scenario.")
    else:
        if selected.get("recommendation") != recommendation:
            errors.append("selected scenario recommendation must match top-level recommendation.")
        for key in ["pwin", "expectedValue", "confidence"]:
            top_value = payload.get(key)
            selected_value = selected.get(key)
            if is_number(top_value) and is_number(selected_value) and abs(float(top_value) - float(selected_value)) > 0.01:
                errors.append(f"top-level {key} must match the selected scenario.")
        if selected.get("gateFailures") and selected.get("recommendation") in {"BID", "BID_WITH_PARTNER"}:
            errors.append("selected bid scenario has gate failures.")

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate GovTribe bid/no-bid engine JSON output.",
    )
    parser.add_argument("output_path", help="Path to bid_no_bid_engine.py JSON output.")
    parser.add_argument("--expect-recommendation", choices=sorted(ALLOWED_RECOMMENDATIONS))
    parser.add_argument("--expect-selected-scenario", choices=sorted(REQUIRED_SCENARIOS))
    parser.add_argument("--pretty", action="store_true", help="Print a JSON validation summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        payload = json.loads(Path(args.output_path).read_text())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"errors": [f"Could not read JSON: {exc}"], "warnings": []}), file=sys.stderr)
        return 1

    errors, warnings = validate_output(
        payload,
        expect_recommendation=args.expect_recommendation,
        expect_selected_scenario=args.expect_selected_scenario,
    )

    summary = {
        "recommendation": payload.get("recommendation"),
        "selectedScenarioKey": payload.get("selectedScenarioKey"),
        "scenarioCount": len(payload.get("scenarios", [])) if isinstance(payload.get("scenarios"), list) else 0,
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
