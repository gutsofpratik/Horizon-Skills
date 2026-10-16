#!/usr/bin/env python3
"""Validate a Past Performance Match memo for defensible document structure."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "reference_decision": (
        "reference decision",
        "match decision",
        "decision",
    ),
    "requirement_basis": (
        "requirement basis",
        "requirement summary",
        "requirement proof",
    ),
    "recommended_reference_set": (
        "recommended reference set",
        "recommended references",
        "reference set",
    ),
    "anchor_reference_profile": (
        "anchor reference profile",
        "lead reference profile",
        "anchor reference",
    ),
    "supporting_references": (
        "supporting references",
        "support references",
        "secondary references",
    ),
    "gap_and_risk_assessment": (
        "gap and risk assessment",
        "gap and risk notes",
        "gaps and risks",
        "risk assessment",
    ),
    "evidence_traceability": (
        "evidence traceability",
        "evidence basis",
        "evidence ledger",
    ),
    "confidence": (
        "confidence",
        "confidence and limitations",
    ),
}

POSTURE_PATTERN = re.compile(r"\b(strong|defensible|conditional|weak|not defensible)\b", re.I)
USE_PATTERN = re.compile(r"\b(lead reference|anchor reference|supporting reference|support reference|reserve|do not use)\b", re.I)
EVIDENCE_ID_PATTERN = re.compile(r"\b(?:REQ|PP|AWD|FILE|SRC)-[A-Za-z0-9._-]+\b")
CONFIDENCE_PATTERN = re.compile(r"\b(high|moderate|medium|low)\b|\b\d{1,3}%\b", re.I)


def normalized_heading(line: str) -> str | None:
    match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
    if not match:
        return None

    heading = match.group(1).strip().lower()
    heading = re.sub(r"[^\w\s/-]", "", heading)
    heading = re.sub(r"\s+", " ", heading)
    return heading


def extract_headings(text: str) -> set[str]:
    headings: set[str] = set()
    for line in text.splitlines():
        heading = normalized_heading(line)
        if heading:
            headings.add(heading)
    return headings


def find_missing_sections(headings: set[str]) -> list[str]:
    missing: list[str] = []
    for key, aliases in SECTION_ALIASES.items():
        if not any(alias in headings for alias in aliases):
            missing.append(key)
    return missing


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
        long_cell_count += sum(1 for cell in cells if len(cell) > 130)

    return max_columns, long_cell_count


def validate(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()
    headings = extract_headings(text)
    evidence_ids = sorted(set(EVIDENCE_ID_PATTERN.findall(text)))
    max_columns, long_cell_count = table_diagnostics(text)

    errors: list[str] = []
    warnings: list[str] = []

    missing_sections = find_missing_sections(headings)
    for section in missing_sections:
        errors.append(f"missing required memo section: {section}")

    if not POSTURE_PATTERN.search(text):
        errors.append("memo must state a match posture such as strong, defensible, conditional, weak, or not defensible.")

    if not USE_PATTERN.search(text):
        errors.append("memo must state how to use the reference set, such as lead reference, support reference, reserve, or do not use.")

    if len(evidence_ids) < 4:
        errors.append("memo must cite at least four evidence IDs across requirement and past-performance evidence.")

    if not any(term in lower_text for term in ("gap", "risk", "limitation", "not found", "no direct")):
        errors.append("memo must explicitly discuss gaps, risks, limitations, or missing evidence.")

    if "confidence" in lower_text and not CONFIDENCE_PATTERN.search(text):
        warnings.append("confidence section should include high/moderate/low confidence or a numeric confidence value.")

    if max_columns > 5:
        warnings.append(f"widest markdown table has {max_columns} columns; keep memo tables to five columns or fewer for document rendering.")

    if long_cell_count:
        warnings.append(f"{long_cell_count} table cell(s) exceed 130 characters; move analysis into memo prose instead of wide table cells.")

    return {
        "path": str(path),
        "headingCount": len(headings),
        "evidenceIdCount": len(evidence_ids),
        "maxTableColumns": max_columns,
        "longTableCellCount": long_cell_count,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Past Performance Match memo.")
    parser.add_argument("memo", type=Path, help="Path to the generated markdown memo.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    if not args.memo.exists():
        print(f"error: memo not found: {args.memo}", file=sys.stderr)
        return 2

    result = validate(args.memo)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
