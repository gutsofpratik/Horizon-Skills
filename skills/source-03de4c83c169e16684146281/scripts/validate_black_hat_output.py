#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

REQUIRED_OUTPUT_KEYS = {
    "evaluation_model",
    "predicted_bidders",
    "competitor_assessments",
    "our_position",
    "price_to_win",
    "recommended_actions",
    "confidence_summary",
    "evidence_ledger",
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

    return value


def require_number(errors: list[str], payload: dict[str, Any], key: str, path: str, low: float = 0.0, high: float = 1.0) -> None:
    value = payload.get(key)
    if not is_number(value):
        errors.append(f"{path}.{key} must be numeric.")
        return

    if value < low or value > high:
        errors.append(f"{path}.{key} must be between {low} and {high}.")


def validate_predicted_bidders(errors: list[str], payload: dict[str, Any]) -> None:
    bidders = require_list(errors, payload, "predicted_bidders", "$", min_count=1)
    previous: float | None = None
    for index, bidder in enumerate(bidders):
        path = f"$.predicted_bidders[{index}]"
        if not isinstance(bidder, dict):
            errors.append(f"{path} must be an object.")
            continue
        require_string(errors, bidder, "vendor_id", path)
        require_string(errors, bidder, "name", path)
        require_number(errors, bidder, "bid_probability", path)
        require_number(errors, bidder, "overall_score", path)
        require_string(errors, bidder, "likely_price_posture", path)
        sort_score = float(bidder.get("bid_probability", 0.0)) * float(bidder.get("overall_score", 0.0))
        if previous is not None and sort_score > previous:
            errors.append("$.predicted_bidders must be sorted by bid_probability * overall_score descending.")
        previous = sort_score


def validate_factor_scorecards(
    errors: list[str],
    cards: list[Any],
    required_factor_ids: set[str],
    path: str,
) -> None:
    if not isinstance(cards, list):
        errors.append(f"{path} must be a list.")
        return

    factor_ids = {card.get("factor_id") for card in cards if isinstance(card, dict)}
    if factor_ids != required_factor_ids:
        errors.append(f"{path} must include exactly the evaluation model factor IDs.")

    for index, card in enumerate(cards):
        card_path = f"{path}[{index}]"
        if not isinstance(card, dict):
            errors.append(f"{card_path} must be an object.")
            continue
        require_string(errors, card, "factor_id", card_path)
        require_string(errors, card, "factor_name", card_path)
        require_number(errors, card, "score", card_path)
        require_string(errors, card, "standing", card_path)


def validate_competitors(errors: list[str], payload: dict[str, Any], required_factor_ids: set[str], ledger_ids: set[str]) -> None:
    competitors = require_list(errors, payload, "competitor_assessments", "$", min_count=1)
    our_vendor_id = payload.get("our_position", {}).get("vendor_id") if isinstance(payload.get("our_position"), dict) else None
    for index, competitor in enumerate(competitors):
        path = f"$.competitor_assessments[{index}]"
        if not isinstance(competitor, dict):
            errors.append(f"{path} must be an object.")
            continue
        require_string(errors, competitor, "vendor_id", path)
        require_string(errors, competitor, "name", path)
        if our_vendor_id and competitor.get("vendor_id") == our_vendor_id:
            errors.append(f"{path} must not include our team.")
        for key in ["bid_probability", "coverage_score", "past_performance_score", "price_position_score", "overall_score", "confidence"]:
            require_number(errors, competitor, key, path)
        evaluator_view = require_object(errors, competitor, "evaluator_view", path)
        validate_factor_scorecards(errors, evaluator_view.get("factor_scorecards"), required_factor_ids, f"{path}.evaluator_view.factor_scorecards")
        competitor_view = require_object(errors, competitor, "competitor_view", path)
        require_string(errors, competitor_view, "likely_price_posture", f"{path}.competitor_view")
        for evidence_id in competitor.get("evidence_ids", []):
            if evidence_id not in ledger_ids:
                errors.append(f"{path}.evidence_ids contains missing ledger id {evidence_id}.")


def validate_our_position(errors: list[str], payload: dict[str, Any], required_factor_ids: set[str], ledger_ids: set[str]) -> None:
    our = require_object(errors, payload, "our_position", "$")
    if not our:
        return
    require_string(errors, our, "vendor_id", "$.our_position")
    require_string(errors, our, "name", "$.our_position")
    require_number(errors, our, "bid_probability", "$.our_position")
    require_number(errors, our, "overall_score", "$.our_position")
    require_number(errors, our, "confidence", "$.our_position")
    if not isinstance(our.get("rank"), int):
        errors.append("$.our_position.rank must be an integer.")
    require_string(errors, our, "likely_price_posture", "$.our_position")
    validate_factor_scorecards(errors, our.get("factor_scorecards"), required_factor_ids, "$.our_position.factor_scorecards")
    for evidence_id in our.get("evidence_ids", []):
        if evidence_id not in ledger_ids:
            errors.append(f"$.our_position.evidence_ids contains missing ledger id {evidence_id}.")


def validate_actions(errors: list[str], payload: dict[str, Any]) -> None:
    actions = require_list(errors, payload, "recommended_actions", "$", min_count=1)
    for index, action in enumerate(actions):
        path = f"$.recommended_actions[{index}]"
        if not isinstance(action, dict):
            errors.append(f"{path} must be an object.")
            continue
        require_string(errors, action, "action", path)
        require_number(errors, action, "expected_score_lift", path, low=0.0, high=1.0)
        require_number(errors, action, "expected_pwin_lift", path, low=0.0, high=1.0)
        require_string(errors, action, "proposal_effort", path)
        require_string(errors, action, "margin_impact", path)


def validate_output(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = REQUIRED_OUTPUT_KEYS - set(payload)
    if missing:
        errors.append(f"Missing output keys: {sorted(missing)}.")

    evaluation_model = require_object(errors, payload, "evaluation_model", "$")
    factors = require_list(errors, evaluation_model, "factors", "$.evaluation_model", min_count=1) if evaluation_model else []
    required_factor_ids = {factor.get("id") for factor in factors if isinstance(factor, dict)}
    if not required_factor_ids:
        errors.append("$.evaluation_model.factors must include factor IDs.")

    ledger = require_list(errors, payload, "evidence_ledger", "$", min_count=1)
    ledger_ids = {entry.get("evidence_id") for entry in ledger if isinstance(entry, dict)}

    validate_predicted_bidders(errors, payload)
    validate_our_position(errors, payload, required_factor_ids, ledger_ids)
    validate_competitors(errors, payload, required_factor_ids, ledger_ids)
    validate_actions(errors, payload)

    price_to_win = require_object(errors, payload, "price_to_win", "$")
    if price_to_win and price_to_win.get("market_band") is None:
        warnings.append("$.price_to_win.market_band is missing; price posture confidence should be low.")

    confidence = require_object(errors, payload, "confidence_summary", "$")
    for key in ["overall_confidence", "data_completeness", "source_agreement", "model_stability"]:
        if confidence:
            require_number(errors, confidence, key, "$.confidence_summary")

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate GovTribe black-hat engine JSON output.",
    )
    parser.add_argument("output_path", help="Path to black_hat_engine.py JSON output.")
    parser.add_argument("--pretty", action="store_true", help="Print a formatted validation summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(Path(args.output_path).read_text())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"errors": [f"Could not read JSON: {exc}"], "warnings": []}), file=sys.stderr)
        return 1

    errors, warnings = validate_output(payload)
    summary = {
        "predictedBidderCount": len(payload.get("predicted_bidders", [])) if isinstance(payload.get("predicted_bidders"), list) else 0,
        "competitorAssessmentCount": len(payload.get("competitor_assessments", [])) if isinstance(payload.get("competitor_assessments"), list) else 0,
        "ourRank": payload.get("our_position", {}).get("rank") if isinstance(payload.get("our_position"), dict) else None,
        "evidenceLedgerCount": len(payload.get("evidence_ledger", [])) if isinstance(payload.get("evidence_ledger"), list) else 0,
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
