from __future__ import annotations

import pytest

from philiprehberger_cli_table import format_table, table
from philiprehberger_cli_table import _display_width


class TestDictListMode:
    def test_dict_list_produces_expected_output(self) -> None:
        data = [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]
        result = format_table(data=data)
        lines = result.split("\n")
        assert len(lines) == 4
        assert "name" in lines[0]
        assert "age" in lines[0]
        assert "Alice" in lines[2]
        assert "Bob" in lines[3]

    def test_empty_data_returns_empty_string(self) -> None:
        assert format_table(data=[]) == ""

    def test_single_row(self) -> None:
        data = [{"x": "1"}]
        result = format_table(data=data)
        lines = result.split("\n")
        assert len(lines) == 3
        assert "1" in lines[2]


class TestHeadersRowsMode:
    def test_headers_rows_works(self) -> None:
        result = format_table(
            headers=["Name", "Score"],
            rows=[["Alice", "95"], ["Bob", "87"]],
        )
        lines = result.split("\n")
        assert len(lines) == 4
        assert "Name" in lines[0]
        assert "Alice" in lines[2]

    def test_no_headers_returns_empty_string(self) -> None:
        assert format_table(headers=[], rows=[["a"]]) == ""

    def test_no_headers_or_rows_returns_empty_string(self) -> None:
        assert format_table() == ""

    def test_missing_values_in_rows_padded(self) -> None:
        result = format_table(
            headers=["A", "B", "C"],
            rows=[["1"]],
        )
        lines = result.split("\n")
        assert len(lines) == 3


class TestAlignment:
    def test_right_alignment(self) -> None:
        result = format_table(
            headers=["Name", "Num"],
            rows=[["Alice", "1"], ["Bob", "200"]],
            align={"Num": "right"},
        )
        lines = result.split("\n")
        # "200" should be right-aligned — check it ends at the right edge
        num_col_line = lines[2]
        assert "  1" in num_col_line or num_col_line.endswith("1")

    def test_center_alignment(self) -> None:
        result = format_table(
            headers=["Name", "Val"],
            rows=[["A", "X"]],
            align={"Val": "center"},
        )
        assert "Val" in result
        assert "X" in result


class TestTruncation:
    def test_truncation_with_max_width(self) -> None:
        result = format_table(
            headers=["Text"],
            rows=[["This is a very long string that should be truncated"]],
            max_width=10,
        )
        lines = result.split("\n")
        # The data row should have a truncated value with ellipsis
        assert "\u2026" in lines[2]
        # The visible cell content (excluding padding) should not exceed max_width
        cell_text = lines[2].strip()
        assert len(cell_text) <= 10


class TestStyles:
    def test_simple_style_default(self) -> None:
        result = format_table(
            headers=["A"],
            rows=[["1"]],
        )
        lines = result.split("\n")
        assert len(lines) == 3
        assert "-" in lines[1]
        assert "|" not in lines[0]

    def test_markdown_style(self) -> None:
        result = format_table(
            headers=["A", "B"],
            rows=[["1", "2"]],
            style="markdown",
        )
        lines = result.split("\n")
        assert lines[0].startswith("|")
        assert lines[0].endswith("|")
        assert lines[1].startswith("|")
        assert "---" in lines[1] or "- |" in lines[1]

    def test_none_style(self) -> None:
        result = format_table(
            headers=["A", "B"],
            rows=[["1", "2"]],
            style="none",
        )
        lines = result.split("\n")
        assert len(lines) == 2  # header + 1 row, no separator
        assert "-" not in lines[0]


class TestUnicode:
    def test_unicode_characters_in_cells(self) -> None:
        result = format_table(
            headers=["Name", "City"],
            rows=[
                ["\u00c9milie", "Z\u00fcrich"],
                ["\u00d6zlem", "Malm\u00f6"],
            ],
        )
        assert "\u00c9milie" in result
        assert "Z\u00fcrich" in result
        assert "\u00d6zlem" in result
        assert "Malm\u00f6" in result


class TestFormatTableReturnsString:
    def test_format_table_returns_string(self) -> None:
        result = format_table(data=[{"a": "1"}])
        assert isinstance(result, str)


class TestWideCharacters:
    def test_cjk_columns_align_correctly(self) -> None:
        result = format_table(
            headers=["Name"],
            rows=[["名前"], ["ab"]],
        )
        lines = result.split("\n")
        # "名前" has display width 4, "ab" has display width 2
        # Both rows should be padded to the same display width (4)
        header_line = lines[0]
        data_line_cjk = lines[2]
        data_line_ascii = lines[3]
        assert _display_width(header_line) == _display_width(data_line_cjk)
        assert _display_width(data_line_cjk) == _display_width(data_line_ascii)

    def test_truncation_of_wide_chars(self) -> None:
        result = format_table(
            headers=["Text"],
            rows=[["漢字漢字漢字"]],
            max_width=5,
        )
        lines = result.split("\n")
        cell_text = lines[2].strip()
        assert "\u2026" in cell_text
        assert _display_width(cell_text) <= 5


class TestTablePrintsToStdout:
    def test_table_prints_to_stdout(self, capsys: pytest.CaptureFixture[str]) -> None:
        table(data=[{"x": "1", "y": "2"}])
        captured = capsys.readouterr()
        assert "x" in captured.out
        assert "y" in captured.out
        assert "1" in captured.out
        assert "2" in captured.out
