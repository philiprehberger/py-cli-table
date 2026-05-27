# Changelog

## 0.3.0 (2026-05-26)

- Numeric columns now auto-right-align when no explicit `align` is provided — detected from int/float values and numeric strings. Pass `align={"col": "left"}` to override.
- Add package-card image to README

## 0.2.0 (2026-04-29)

- Add `footer` parameter to `format_table()` and `table()` for totals/summary rows; accepts either a list of cell values or a dict keyed by header
- Footer columns auto-widen to fit and are rendered below a divider for `simple` and `markdown` styles

## 0.1.10 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.9 (2026-03-22)

- Add badges to README

## 0.1.8 (2026-03-21)

- Add pytest and mypy tool configuration to pyproject.toml

## 0.1.7 (2026-03-19)

- Trim keywords to match pyproject template guide

## 0.1.3 (2026-03-16)

- Add Development section to README

## 0.1.1 (2026-03-15)

- Fix column alignment for CJK and wide Unicode characters

## 0.1.0 (2026-03-13)

- Initial release
- `format_table()` for string output
- `table()` for quick printing
- Dict list and headers+rows input modes
- Column alignment (left, right, center)
- Cell truncation with max_width
- Border styles: simple, markdown, none
