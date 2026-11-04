import json
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, range_boundaries


def color_value(color):
    if not color:
        return None
    if color.type == "rgb" and color.rgb:
        return color.rgb[-6:]
    if color.type == "indexed" and color.indexed is not None:
        return f"indexed:{color.indexed}"
    if color.type == "theme" and color.theme is not None:
        return f"theme:{color.theme}"
    return None


def serializable(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def style_payload(cell):
    border = {}
    for side_name in ("top", "right", "bottom", "left"):
        side = getattr(cell.border, side_name)
        if side.style:
            border[side_name] = {
                "style": side.style,
                "color": color_value(side.color),
            }
    return {
        "font": {
            "name": cell.font.name,
            "size": cell.font.sz,
            "bold": bool(cell.font.bold),
            "italic": bool(cell.font.italic),
            "underline": cell.font.underline,
            "color": color_value(cell.font.color),
        },
        "fill": color_value(cell.fill.fgColor) if cell.fill.fill_type else None,
        "alignment": {
            "horizontal": cell.alignment.horizontal,
            "vertical": cell.alignment.vertical,
            "wrap": bool(cell.alignment.wrap_text),
            "rotation": cell.alignment.text_rotation,
        },
        "border": border,
        "numberFormat": cell.number_format,
    }


def main():
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else "115年防護 (修改test)"
    values_wb = load_workbook(source, data_only=True)
    formula_wb = load_workbook(source, data_only=False)
    ws = values_wb[sheet_name]
    formula_ws = formula_wb[sheet_name]

    styles = []
    style_ids = {}
    cells = {}
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            formula_cell = formula_ws[cell.coordinate]
            style = style_payload(formula_cell)
            style_key = json.dumps(style, sort_keys=True, ensure_ascii=False)
            if style_key not in style_ids:
                style_ids[style_key] = len(styles)
                styles.append(style)
            value = serializable(cell.value)
            formula = formula_cell.value if isinstance(formula_cell.value, str) and formula_cell.value.startswith("=") else None
            if value is not None or formula is not None or formula_cell.style_id:
                cells[cell.coordinate] = {
                    "value": value,
                    "formula": formula,
                    "style": style_ids[style_key],
                }

    merges = []
    for merged in ws.merged_cells.ranges:
        min_col, min_row, max_col, max_row = range_boundaries(str(merged))
        merges.append({
            "range": str(merged),
            "start": f"{get_column_letter(min_col)}{min_row}",
            "rowspan": max_row - min_row + 1,
            "colspan": max_col - min_col + 1,
            "minRow": min_row,
            "maxRow": max_row,
            "minCol": min_col,
            "maxCol": max_col,
        })

    detail_rows = []
    for row_number in range(42, 271):
        description = ws.cell(row_number, 3).value
        amount = sum(
            float(ws.cell(row_number, col).value or 0)
            for col in range(4, 36)
            if isinstance(ws.cell(row_number, col).value, (int, float))
        )
        if description and amount:
            detail_rows.append(row_number)

    payload = {
        "source": source.name,
        "sheetName": sheet_name,
        "maxRow": ws.max_row,
        "maxCol": ws.max_column,
        "columnWidths": [
            ws.column_dimensions[get_column_letter(col)].width or 8.43
            for col in range(1, ws.max_column + 1)
        ],
        "rowHeights": [
            ws.row_dimensions[row].height or 15
            for row in range(1, ws.max_row + 1)
        ],
        "hiddenRows": [row for row in range(1, ws.max_row + 1) if ws.row_dimensions[row].hidden],
        "merges": merges,
        "styles": styles,
        "cells": cells,
        "detailRows": detail_rows,
        "summary": {
            "approved": ws["U5"].value,
            "executed": ws["U6"].value,
            "remaining": ws["U7"].value,
            "reimbursed": ws["AJ271"].value,
            "borrowed": ws["Z1"].value,
            "unposted": ws["Z2"].value,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
