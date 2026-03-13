"""Format Python data as aligned terminal tables with no dependencies."""

from __future__ import annotations

import sys
from typing import Any, Literal

__all__ = ["table", "format_table"]

Align = Literal["left", "right", "center"]
Style = Literal["simple", "markdown", "none"]


def format_table(
    headers: list[str] | None = None,
    rows: list[list[Any]] | None = None,
    *,
    data: list[dict[str, Any]] | None = None,
    align: dict[str, Align] | None = None,
    max_width: int | None = None,
    style: Style = "simple",
) -> str:
    """Format data as an aligned table string.

    Provide either `data` (list of dicts) or `headers` + `rows`.

    Args:
        headers: Column header names.
        rows: List of row value lists.
        data: List of dicts (keys become headers).
        align: Per-column alignment overrides.
        max_width: Truncate cell values to this width.
        style: Border style — "simple", "markdown", or "none".
    """
    if data is not None:
        if not data:
            return ""
        headers = list(data[0].keys())
        rows = [[row.get(h, "") for h in headers] for row in data]
    elif headers is None or rows is None:
        return ""

    if not headers:
        return ""

    align = align or {}
    str_rows = [[_truncate(str(v), max_width) for v in row] for row in rows]

    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(cell))
            else:
                col_widths.append(len(cell))

    lines: list[str] = []

    header_cells = [
        _align_cell(h, col_widths[i], align.get(h, "left")) for i, h in enumerate(headers)
    ]

    if style == "simple":
        lines.append("  ".join(header_cells))
        lines.append("  ".join("-" * w for w in col_widths))
    elif style == "markdown":
        lines.append("| " + " | ".join(header_cells) + " |")
        sep_parts = []
        for i, h in enumerate(headers):
            a = align.get(h, "left")
            w = col_widths[i]
            if a == "right":
                sep_parts.append("-" * (w - 1) + ":")
            elif a == "center":
                sep_parts.append(":" + "-" * (w - 2) + ":")
            else:
                sep_parts.append("-" * w)
        lines.append("| " + " | ".join(sep_parts) + " |")
    elif style == "none":
        lines.append("  ".join(header_cells))

    for row in str_rows:
        cells = []
        for i, h in enumerate(headers):
            value = row[i] if i < len(row) else ""
            cells.append(_align_cell(value, col_widths[i], align.get(h, "left")))
        if style == "markdown":
            lines.append("| " + " | ".join(cells) + " |")
        else:
            lines.append("  ".join(cells))

    return "\n".join(lines)


def table(
    data: list[dict[str, Any]] | None = None,
    headers: list[str] | None = None,
    rows: list[list[Any]] | None = None,
    **kwargs: Any,
) -> None:
    """Print a formatted table to stdout."""
    output = format_table(headers=headers, rows=rows, data=data, **kwargs)
    if output:
        print(output, file=sys.stdout)


def _truncate(value: str, max_width: int | None) -> str:
    if max_width is not None and len(value) > max_width:
        return value[: max_width - 1] + "\u2026"
    return value


def _align_cell(value: str, width: int, alignment: Align) -> str:
    if alignment == "right":
        return value.rjust(width)
    if alignment == "center":
        return value.center(width)
    return value.ljust(width)
