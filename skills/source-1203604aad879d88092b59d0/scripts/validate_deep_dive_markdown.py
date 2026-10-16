#!/usr/bin/env python3
"""Validate a GovTribe Deep Dive Markdown dossier structure."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "target_metadata": ("target metadata",),
    "decision_snapshot": ("decision snapshot",),
    "executive_takeaway": ("executive takeaway",),
    "source_backed_target_profile": ("source backed target profile", "source-backed target profile"),
    "lifecycle_and_user_intent": ("lifecycle and user intent",),
    "bd_and_capture_implications": ("bd and capture implications", "bd capture implications"),
    "consultant_scoring": ("consultant scoring",),
    "recommended_actions": ("recommended actions",),
    "risks_unknowns_and_evidence_gaps": (
        "risks unknowns and evidence gaps",
        "risks, unknowns, and evidence gaps",
        "risks and evidence gaps",
    ),
    "evidence_ledger": ("evidence ledger",),
}

PROFILE_MODULES: dict[str, tuple[str, ...]] = {
    "live_pursuit": ("live pursuit module",),
    "market_research_shaping": ("market research and rfq shaping module",),
    "recompete_planning": ("recompete planning module",),
    "account_market": ("account and market module",),
    "competitor_partner_stakeholder": ("competitor partner and stakeholder module",),
    "funding_eligibility": ("funding and eligibility module",),
    "vehicle_idv_award": ("vehicle idv and award module",),
    "state_local_market": ("state and local market module",),
}

TARGET_TYPE_PROFILE_HINTS: dict[str, tuple[tuple[str, ...], ...]] = {
    "federal_contract_opportunity": (
        ("live_pursuit",),
        ("market_research_shaping",),
        ("recompete_planning",),
    ),
    "federal_forecast": (("live_pursuit",), ("recompete_planning",)),
    "federal_contract_award": (("vehicle_idv_award",), ("recompete_planning",)),
    "federal_contract_idv": (("vehicle_idv_award",), ("recompete_planning",)),
    "federal_contract_vehicle": (("vehicle_idv_award",), ("account_market",)),
    "vendor": (("competitor_partner_stakeholder",),),
    "contact": (("competitor_partner_stakeholder",),),
    "federal_agency": (("account_market",),),
    "major_defense_program": (("account_market",),),
    "federal_grant_opportunity": (("funding_eligibility",), ("live_pursuit",)),
    "federal_grant_program": (("funding_eligibility",), ("account_market",)),
    "federal_grant_award": (("funding_eligibility",),),
    "jurisdiction": (("state_local_market",), ("account_market",)),
    "state": (("state_local_market",), ("account_market",)),
    "state_local_contract_opportunity": (("state_local_market",), ("live_pursuit",)),
    "state_local_contract_award": (("state_local_market",), ("recompete_planning",)),
    "state_local_contract_idv": (("state_local_market",), ("vehicle_idv_award",)),
    "state_local_contract_vehicle": (("state_local_market",), ("vehicle_idv_award",)),
}

EVIDENCE_ID_PATTERN = re.compile(
    r"(?<![A-Za-z0-9-])(?:SRC|FILE|OPP|AWD|IDV|VEH|VND|CNT|GRANT|NEWS|USER|MEM|GAP)-[A-Za-z0-9._-]+\b"
)
CONFIDENCE_PATTERN = re.compile(r"\b(high|moderate|medium|low|unknown)\b|\b\d{1,3}%\b", re.I)
GENERIC_ACTION_PATTERN = re.compile(
    r"\b(research more|do more research|follow up|monitor closely|keep watching|circle back)\b",
    re.I,
)


def normalize_heading_text(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s/-]", "", value)
    value = value.replace("/", " ")
    value = re.sub(r"[-_]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def extract_heading_positions(text: str) -> list[tuple[int, int, str]]:
    headings: list[tuple[int, int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        heading = normalize_heading_text(match.group(2))
        headings.append((line_number, level, heading))
    return headings


def heading_set(positions: list[tuple[int, int, str]]) -> set[str]:
    return {heading for _, _, heading in positions}


def has_alias(headings: set[str], aliases: tuple[str, ...]) -> bool:
    normalized_aliases = {normalize_heading_text(alias) for alias in aliases}
    return bool(headings & normalized_aliases)


def missing_sections(headings: set[str]) -> list[str]:
    return [
        section
        for section, aliases in SECTION_ALIASES.items()
        if not has_alias(headings, aliases)
    ]


def profiles_from_arg(raw_profile: str | None) -> tuple[list[str], list[str]]:
    if not raw_profile:
        return [], []

    profiles = [item.strip() for item in raw_profile.split(",") if item.strip()]
    unknown = [profile for profile in profiles if profile not in PROFILE_MODULES]
    return profiles, unknown


def detected_profiles(headings: set[str]) -> list[str]:
    detected: list[str] = []
    for profile, aliases in PROFILE_MODULES.items():
        if has_alias(headings, aliases):
            detected.append(profile)
    return detected


def section_text(
    text: str,
    positions: list[tuple[int, int, str]],
    aliases: tuple[str, ...],
) -> str:
    lines = text.splitlines()
    normalized_aliases = {normalize_heading_text(alias) for alias in aliases}

    start_index: int | None = None
    start_level = 0
    for index, (_, level, heading) in enumerate(positions):
        if heading not in normalized_aliases:
            continue
        start_index = positions[index][0]
        start_level = level
        break

    if start_index is None:
        return ""

    end_line = len(lines) + 1
    for line_number, level, _ in positions:
        if line_number <= start_index:
            continue
        if level <= start_level:
            end_line = line_number
            break

    return "\n".join(lines[start_index : end_line - 1]).strip()


def table_diagnostics(text: str) -> tuple[int, int]:
    max_columns = 0
    long_cell_count = 0

    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        max_columns = max(max_columns, len(cells))
        long_cell_count += sum(1 for cell in cells if len(cell) > 140)

    return max_columns, long_cell_count


def validate(
    path: Path,
    target_type: str | None = None,
    profile_arg: str | None = None,
) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()
    positions = extract_heading_positions(text)
    headings = heading_set(positions)
    evidence_ledger = section_text(text, positions, SECTION_ALIASES["evidence_ledger"])
    recommended_actions = section_text(text, positions, SECTION_ALIASES["recommended_actions"])
    body_before_ledger = text.split("## Evidence ledger", 1)[0]

    used_evidence_ids = sorted(set(EVIDENCE_ID_PATTERN.findall(body_before_ledger)))
    ledger_evidence_ids = sorted(set(EVIDENCE_ID_PATTERN.findall(evidence_ledger)))
    all_evidence_ids = sorted(set(EVIDENCE_ID_PATTERN.findall(text)))
    max_columns, long_cell_count = table_diagnostics(text)
    requested_profiles, unknown_profiles = profiles_from_arg(profile_arg)
    found_profiles = detected_profiles(headings)

    errors: list[str] = []
    warnings: list[str] = []

    for section in missing_sections(headings):
        errors.append(f"missing required deep-dive section: {section}")

    for profile in unknown_profiles:
        errors.append(f"unknown output profile: {profile}")

    if not found_profiles:
        errors.append("dossier must include at least one recognized module heading.")

    for profile in requested_profiles:
        if profile not in found_profiles:
            errors.append(f"missing module for requested profile: {profile}")

    if target_type:
        normalized_target_type = target_type.strip()
        allowed_profile_groups = TARGET_TYPE_PROFILE_HINTS.get(normalized_target_type)
        if allowed_profile_groups is None:
            warnings.append(f"no target-type profile hint is configured for: {normalized_target_type}")
        elif not any(set(group) & set(found_profiles) for group in allowed_profile_groups):
            expected = sorted({profile for group in allowed_profile_groups for profile in group})
            errors.append(
                "target type does not include an expected module: "
                + normalized_target_type
                + " expects one of "
                + ", ".join(expected)
            )

    if len(used_evidence_ids) < 5:
        errors.append("dossier must cite at least five evidence IDs before the evidence ledger.")

    if len(ledger_evidence_ids) < 5:
        errors.append("evidence ledger must include at least five evidence IDs.")

    missing_from_ledger = sorted(set(used_evidence_ids) - set(ledger_evidence_ids))
    if missing_from_ledger:
        errors.append("cited evidence IDs missing from evidence ledger: " + ", ".join(missing_from_ledger))

    if "confidence" not in lower_text:
        errors.append("dossier must include confidence language.")
    elif not CONFIDENCE_PATTERN.search(text):
        warnings.append("confidence language should include high/moderate/low or a numeric confidence value.")

    if not any(term in lower_text for term in ("gap", "unknown", "risk", "limitation", "missing")):
        errors.append("dossier must explicitly discuss risks, unknowns, limitations, or evidence gaps.")

    if recommended_actions and not EVIDENCE_ID_PATTERN.search(recommended_actions):
        warnings.append("recommended actions should cite evidence IDs.")

    if GENERIC_ACTION_PATTERN.search(recommended_actions) and not EVIDENCE_ID_PATTERN.search(recommended_actions):
        warnings.append("generic recommended actions should be tied to evidence IDs or rewritten as specific actions.")

    if ("USER-" in text or "MEM-" in text) and "personalized inference" not in lower_text:
        warnings.append("personalization evidence is cited; label personalized inference separately from source-backed facts.")

    if max_columns > 5:
        warnings.append(f"widest markdown table has {max_columns} columns; keep rendered tables to five columns or fewer.")

    if long_cell_count:
        warnings.append(f"{long_cell_count} table cell(s) exceed 140 characters; move long analysis into prose or bullets.")

    return {
        "path": str(path),
        "targetType": target_type,
        "requestedProfiles": requested_profiles,
        "detectedProfiles": found_profiles,
        "headingCount": len(headings),
        "usedEvidenceIdCount": len(used_evidence_ids),
        "ledgerEvidenceIdCount": len(ledger_evidence_ids),
        "allEvidenceIds": all_evidence_ids,
        "maxTableColumns": max_columns,
        "longTableCellCount": long_cell_count,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GovTribe Deep Dive Markdown dossier.")
    parser.add_argument("markdown", type=Path, help="Path to the generated deep-dive Markdown file.")
    parser.add_argument("--target-type", help="Optional GovTribe target type, such as federal_contract_opportunity.")
    parser.add_argument("--profile", help="Optional comma-separated output profiles to require.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    if not args.markdown.exists():
        print(f"error: markdown file not found: {args.markdown}", file=sys.stderr)
        return 2

    result = validate(args.markdown, target_type=args.target_type, profile_arg=args.profile)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
