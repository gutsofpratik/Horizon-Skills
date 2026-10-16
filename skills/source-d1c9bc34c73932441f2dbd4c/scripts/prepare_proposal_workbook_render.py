#!/usr/bin/env python3
"""Prepare a GovTribe proposal control workbook for PDF rendering.

The bundled workbook is optimized for editing. Before visual QA or PDF delivery,
set print areas to populated ranges, fit wide sheets to one page, and expand
rows that contain long wrapped text so LibreOffice does not clip content.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

SHEET_COLUMNS = {
    "Start Here": 7,
    "Opportunity Setup": 9,
    "Dashboard": 11,
    "Requirement Matrix": 21,
    "Evaluation Crosswalk": 12,
    "Submission Checklist": 11,
    "Pricing & Deliverables": 10,
    "Questions-Risks": 11,
    "Amendment Log": 10,
    "Sources": 5,
    "Lists": 18,
}

load_workbook = None
get_column_letter = None
PageMargins = None
PageSetupProperties = None


def load_openpyxl() -> int:
    global load_workbook, get_column_letter, PageMargins, PageSetupProperties

    try:
        from openpyxl import load_workbook as openpyxl_load_workbook
        from openpyxl.utils import get_column_letter as openpyxl_get_column_letter
        from openpyxl.worksheet.page import PageMargins as OpenPyxlPageMargins
        from openpyxl.worksheet.properties import (
            PageSetupProperties as OpenPyxlPageSetupProperties,
        )
    except ModuleNotFoundError:
        print(
            "DEGRADED: openpyxl is unavailable. Use the external host's spreadsheet "
            "rendering capability and manually verify print areas, fit-to-width, and "
            "wrapped row heights. Deliver Markdown or CSV control views if rendering "
            "is unavailable.",
            file=sys.stderr,
        )
        return 2

    load_workbook = openpyxl_load_workbook
    get_column_letter = openpyxl_get_column_letter
    PageMargins = OpenPyxlPageMargins
    PageSetupProperties = OpenPyxlPageSetupProperties

    return 0


MIN_PRINT_ROWS = {
    "Start Here": 31,
    "Opportunity Setup": 14,
    "Dashboard": 34,
    "Requirement Matrix": 8,
    "Evaluation Crosswalk": 8,
    "Submission Checklist": 7,
    "Pricing & Deliverables": 7,
    "Questions-Risks": 7,
    "Amendment Log": 7,
    "Sources": 8,
    "Lists": 16,
}

LONG_TEXT_SHEETS = {
    "Requirement Matrix",
    "Evaluation Crosswalk",
    "Submission Checklist",
    "Pricing & Deliverables",
    "Questions-Risks",
    "Amendment Log",
    "Sources",
}

ROW_ID_PRINT_SHEETS = {
    "Requirement Matrix",
    "Evaluation Crosswalk",
    "Submission Checklist",
    "Pricing & Deliverables",
    "Questions-Risks",
    "Amendment Log",
}


def is_populated(value: object) -> bool:
    return value is not None and str(value).strip() != ""


def last_populated_row(ws, max_col: int) -> int:
    last_row = 1
    if ws.title in ROW_ID_PRINT_SHEETS:
        for row_idx in range(1, ws.max_row + 1):
            if is_populated(ws.cell(row=row_idx, column=1).value):
                last_row = row_idx

        return max(last_row, MIN_PRINT_ROWS.get(ws.title, last_row))

    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=max_col):
        if any(is_populated(cell.value) for cell in row):
            last_row = row[0].row

    return max(last_row, MIN_PRINT_ROWS.get(ws.title, last_row))


def effective_column_width(ws, column: int) -> float:
    width = ws.column_dimensions[get_column_letter(column)].width

    return float(width or 10)


def estimated_lines(value: object, width: float) -> int:
    if not is_populated(value):
        return 1

    text = str(value)
    explicit_lines = text.count("\n") + 1
    wrapped_lines = math.ceil(len(text) / max(width * 1.1, 8))

    return max(explicit_lines, wrapped_lines, 1)


def adjust_row_heights(ws, max_col: int, max_row: int) -> None:
    if ws.title not in LONG_TEXT_SHEETS:
        return

    for row_idx in range(1, max_row + 1):
        max_lines = 1
        for col_idx in range(1, max_col + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            max_lines = max(
                max_lines,
                estimated_lines(cell.value, effective_column_width(ws, col_idx)),
            )

        if max_lines > 1:
            ws.row_dimensions[row_idx].height = min(max(18, max_lines * 15), 120)


def prepare_sheet(ws, contract_mode: bool = False) -> None:
    if contract_mode:
        if str(ws.print_area or "").strip():
            return
        populated = [cell for row in ws for cell in row if is_populated(cell.value)]
        if not populated:
            return
        max_col = max(cell.column for cell in populated)
        max_row = max(cell.row for cell in populated)
        for merged in ws.merged_cells.ranges:
            if is_populated(ws.cell(merged.min_row, merged.min_col).value):
                max_col = max(max_col, merged.max_col)
                max_row = max(max_row, merged.max_row)
        ws.print_area = f"A1:{get_column_letter(max_col)}{max_row}"
        return
    max_col = SHEET_COLUMNS.get(ws.title, ws.max_column)
    for row in ws.iter_rows():
        for cell in row:
            if is_populated(cell.value):
                max_col = max(max_col, cell.column)
    for merged in ws.merged_cells.ranges:
        if is_populated(ws.cell(merged.min_row, merged.min_col).value):
            max_col = max(max_col, merged.max_col)
    max_row = last_populated_row(ws, max_col)
    last_col = get_column_letter(max_col)

    ws.print_area = f"A1:{last_col}{max_row}"
    ws.print_options.horizontalCentered = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.scale = None
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_margins = PageMargins(
        left=0.25, right=0.25, top=0.4, bottom=0.4, header=0.2, footer=0.2
    )

    adjust_row_heights(ws, max_col, max_row)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare a GovTribe proposal workbook for visual rendering."
    )
    parser.add_argument("workbook", type=Path, help="Input .xlsx workbook")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output .xlsx path. Defaults to overwriting with --in-place.",
    )
    parser.add_argument(
        "--in-place", action="store_true", help="Overwrite the input workbook"
    )
    parser.add_argument(
        "--profile", choices=("eleven-sheet", "contract"), default="eleven-sheet"
    )
    parser.add_argument("--contract", type=Path)
    args = parser.parse_args()
    if args.profile == "contract":
        from proposal_contract import read_contract

        try:
            if args.contract is None:
                raise ValueError("Contract profile requires --contract")
            read_contract(args.contract)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    if not args.workbook.exists():
        print(f"ERROR: workbook not found: {args.workbook}")
        return 1

    if not args.in_place and args.output is None:
        print("ERROR: provide --output or --in-place")
        return 2

    if exit_code := load_openpyxl():
        return exit_code

    output = args.workbook if args.in_place else args.output
    wb = load_workbook(args.workbook)

    if args.profile == "eleven-sheet" and set(wb.sheetnames) != set(SHEET_COLUMNS):
        print(
            "ERROR: Non-template layout requires --profile contract --contract contract.json",
            file=sys.stderr,
        )
        return 1

    prepared = []
    for ws in wb.worksheets:
        prepare_sheet(ws, contract_mode=args.profile == "contract")
        prepared.append(ws.title)

    wb.save(output)
    print(f"Prepared workbook render layout: {output}")
    print(f"Sheets prepared: {', '.join(prepared)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
