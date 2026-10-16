#!/usr/bin/env python3
"""Validate a GovTribe annotated proposal outline intermediate JSON file.

Expected shape is documented in assets/annotated-proposal-outline-schema.json.
The script has no external dependencies so it can run in constrained agent sandboxes.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

MANDATORY_PRIORITIES = {"mandatory", "evaluated", "contractual"}
RECOMMENDED_REQ_FIELDS = {"id", "source", "text", "type", "priority", "mapped_to"}
RECOMMENDED_OUTLINE_FIELDS = {"id", "volume", "title", "requirements"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a GovTribe annotated proposal outline JSON file.",
        epilog=(
            "Example: python3 scripts/validate_annotated_outline.py "
            "path/to/outline.json"
        ),
    )
    parser.add_argument(
        "outline_json",
        type=Path,
        help="Path to the intermediate annotated-outline JSON file.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(
            f"ERROR: outline JSON file not found: {path}. "
            "Pass the path generated from the annotated-outline schema."
        )
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"ERROR: invalid JSON in {path} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )
    if not isinstance(data, dict):
        raise SystemExit(
            "ERROR: top-level JSON value must be an object with "
            "source_inventory, requirements, and outline arrays."
        )
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def contains_source_id(source_text: str, source_id: str) -> bool:
    return re.search(
        rf"(?<![A-Za-z0-9_-]){re.escape(source_id)}(?![A-Za-z0-9_-])",
        source_text,
    ) is not None


def validate(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in ("source_inventory", "requirements", "outline"):
        if key not in data:
            errors.append(f"Missing top-level key: {key}")
        elif not isinstance(data[key], list):
            errors.append(f"Top-level key must be a list: {key}")

    requirements = data.get("requirements", []) if isinstance(data.get("requirements"), list) else []
    outline = data.get("outline", []) if isinstance(data.get("outline"), list) else []
    sources = data.get("source_inventory", []) if isinstance(data.get("source_inventory"), list) else []

    source_ids = [source.get("id") for source in sources if isinstance(source, dict)]
    source_id_counts = Counter(source_ids)
    for source_id, count in source_id_counts.items():
        if not source_id:
            errors.append("A source inventory item is missing an id")
        elif count > 1:
            errors.append(f"Duplicate source inventory id: {source_id}")
    source_id_set = {str(value) for value in source_ids if value}

    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            errors.append(f"source_inventory[{index}] must be an object")
            continue
        if not source.get("title"):
            errors.append(f"Source inventory item {source.get('id', index)} missing title")

    requirement_ids = [requirement.get("id") for requirement in requirements if isinstance(requirement, dict)]
    requirement_id_counts = Counter(requirement_ids)
    for requirement_id, count in requirement_id_counts.items():
        if not requirement_id:
            errors.append("A requirement is missing an id")
        elif count > 1:
            errors.append(f"Duplicate requirement id: {requirement_id}")

    outline_ids = [section.get("id") for section in outline if isinstance(section, dict)]
    outline_id_counts = Counter(outline_ids)
    for outline_id, count in outline_id_counts.items():
        if not outline_id:
            errors.append("An outline section is missing an id")
        elif count > 1:
            errors.append(f"Duplicate outline section id: {outline_id}")

    outline_id_set = {value for value in outline_ids if value}
    requirement_id_set = {value for value in requirement_ids if value}

    for index, requirement in enumerate(requirements, start=1):
        if not isinstance(requirement, dict):
            errors.append(f"requirements[{index}] must be an object")
            continue
        missing = RECOMMENDED_REQ_FIELDS - set(requirement)
        if missing:
            errors.append(
                f"Requirement {requirement.get('id', index)} missing fields: "
                + ", ".join(sorted(missing))
            )
        requirement_id = requirement.get("id", f"requirements[{index}]")
        source_text = str(requirement.get("source", "")).strip()
        if not source_text:
            errors.append(f"{requirement_id} is missing a source citation")
        elif source_id_set and not any(
            contains_source_id(source_text, source_id) for source_id in source_id_set
        ):
            errors.append(
                f"{requirement_id} source does not reference a known "
                f"source inventory id: {source_text}"
            )
        priority = str(requirement.get("priority", "")).strip().lower()
        mapped_to = [
            str(value).strip()
            for value in as_list(requirement.get("mapped_to"))
            if str(value).strip()
        ]
        status = str(requirement.get("status", "")).strip().lower()
        if (
            priority in MANDATORY_PRIORITIES
            and not mapped_to
            and status not in {"gap", "unmapped"}
        ):
            errors.append(
                f"{requirement_id} has priority '{priority}' but no mapped_to "
                "section and is not marked gap/unmapped"
            )
        if priority in MANDATORY_PRIORITIES and status in {"", "unknown", "todo"}:
            warnings.append(
                f"{requirement_id} has priority '{priority}' but weak/missing status"
            )
        for target in mapped_to:
            if target not in outline_id_set:
                warnings.append(
                    f"{requirement_id} maps to unknown outline section id: {target}"
                )
        if (
            priority == "inferred"
            and "inferred" not in str(requirement.get("type", "")).lower()
            and "inferred" not in str(requirement.get("notes", "")).lower()
        ):
            warnings.append(
                f"{requirement_id} priority is inferred but the requirement is "
                "not clearly labeled as inferred in type/notes"
            )

    outline_reference_counts: Counter[str] = Counter()
    volume_pages: defaultdict[str, float] = defaultdict(float)
    for index, section in enumerate(outline, start=1):
        if not isinstance(section, dict):
            errors.append(f"outline[{index}] must be an object")
            continue
        missing = RECOMMENDED_OUTLINE_FIELDS - set(section)
        if missing:
            errors.append(
                f"Outline section {section.get('id', index)} missing fields: "
                + ", ".join(sorted(missing))
            )
        section_id = section.get("id", f"outline[{index}]")
        linked_requirements = [
            str(value).strip()
            for value in as_list(section.get("requirements"))
            if str(value).strip()
        ]
        if not linked_requirements:
            warnings.append(f"Outline section {section_id} has no linked requirements")
        for requirement_id in linked_requirements:
            outline_reference_counts[requirement_id] += 1
            if requirement_id not in requirement_id_set:
                warnings.append(
                    f"Outline section {section_id} references unknown "
                    f"requirement id: {requirement_id}"
                )
        page_budget = section.get("page_budget")
        if page_budget is not None:
            try:
                volume_pages[str(section.get("volume", "Unspecified"))] += float(page_budget)
            except (TypeError, ValueError):
                warnings.append(
                    f"Outline section {section_id} has non-numeric "
                    f"page_budget: {page_budget!r}"
                )

    mandatory_total = 0
    mandatory_mapped = 0
    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        priority = str(requirement.get("priority", "")).strip().lower()
        if priority in MANDATORY_PRIORITIES:
            mandatory_total += 1
            if [
                value
                for value in as_list(requirement.get("mapped_to"))
                if str(value).strip()
            ]:
                mandatory_mapped += 1

    return {
        "source_count": len(sources),
        "requirement_count": len(requirements),
        "outline_section_count": len(outline),
        "mandatory_or_scored_requirements": mandatory_total,
        "mandatory_or_scored_mapped": mandatory_mapped,
        "mandatory_or_scored_coverage_pct": (
            round(mandatory_mapped / mandatory_total * 100, 1)
            if mandatory_total
            else None
        ),
        "page_budget_by_volume": dict(volume_pages),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    data = load_json(args.outline_json)
    summary = validate(data)
    print(json.dumps(summary, indent=2))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
