# philiprehberger-cli-table

[![Tests](https://github.com/philiprehberger/py-cli-table/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-cli-table/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-cli-table.svg)](https://pypi.org/project/philiprehberger-cli-table/)
[![License](https://img.shields.io/github/license/philiprehberger/py-cli-table)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Format Python data as aligned terminal tables with no dependencies.

## Installation

```bash
pip install philiprehberger-cli-table
```

## Usage

### Dict list mode

```python
from philiprehberger_cli_table import table

data = [
    {"name": "Alice", "age": 30, "city": "Berlin"},
    {"name": "Bob", "age": 25, "city": "Vienna"},
    {"name": "Charlie", "age": 35, "city": "Zurich"},
]

table(data)
# name     age  city
# -------  ---  ------
# Alice    30   Berlin
# Bob      25   Vienna
# Charlie  35   Zurich
```

### Headers + rows mode

```python
from philiprehberger_cli_table import table

table(
    headers=["Product", "Price", "Stock"],
    rows=[
        ["Widget", "9.99", "142"],
        ["Gadget", "24.99", "38"],
    ],
)
# Product  Price  Stock
# -------  -----  -----
# Widget   9.99   142
# Gadget   24.99  38
```

### Column alignment

```python
from philiprehberger_cli_table import table

table(
    data=[
        {"item": "Coffee", "qty": 3, "price": "4.50"},
        {"item": "Tea", "qty": 12, "price": "2.00"},
    ],
    align={"qty": "right", "price": "right"},
)
# item    qty  price
# ------  ---  -----
# Coffee    3   4.50
# Tea      12   2.00
```

### Styles

```python
from philiprehberger_cli_table import format_table

# Markdown style
print(format_table(
    headers=["Name", "Score"],
    rows=[["Alice", "95"], ["Bob", "87"]],
    style="markdown",
))
# | Name  | Score |
# | ----- | ----- |
# | Alice | 95    |
# | Bob   | 87    |

# No borders
print(format_table(
    headers=["Name", "Score"],
    rows=[["Alice", "95"], ["Bob", "87"]],
    style="none",
))
# Name   Score
# Alice  95
# Bob    87
```

### Cell truncation

```python
from philiprehberger_cli_table import table

table(
    data=[{"description": "A very long description that goes on and on"}],
    max_width=20,
)
```

## Wide character support

Supports CJK and other wide Unicode characters with correct column alignment.

## API

| Function | Description |
| --- | --- |
| `format_table(headers, rows, *, data, align, max_width, style)` | Returns a formatted table as a string |
| `table(data, headers, rows, **kwargs)` | Prints a formatted table to stdout |

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `headers` | `list[str] \| None` | `None` | Column header names |
| `rows` | `list[list[Any]] \| None` | `None` | List of row value lists |
| `data` | `list[dict[str, Any]] \| None` | `None` | List of dicts (keys become headers) |
| `align` | `dict[str, Align] \| None` | `None` | Per-column alignment: `"left"`, `"right"`, `"center"` |
| `max_width` | `int \| None` | `None` | Truncate cell values to this width |
| `style` | `Style` | `"simple"` | Border style: `"simple"`, `"markdown"`, `"none"` |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
