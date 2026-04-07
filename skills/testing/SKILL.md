---
name: testing
description: pytest and unittest tests for contentstack-python — tests/ and config.py.
---

# Testing — Contentstack Python CDA SDK

## Commands

| Goal | Command |
|------|---------|
| Full test tree | `pytest tests/` |
| Single file | `pytest tests/test_stack.py` |

## Environment

- Root **`config.py`**: **HOST**, **APIKEY**, **DELIVERYTOKEN**, **ENVIRONMENT**, optional **PREVIEW_TOKEN**, content UIDs for specific suites.
- Use a **local** **`config.py`** or sanitized values; never commit live secrets.

## Conventions

- Tests subclass **`unittest.TestCase`**; **`tests/pytest.ini`** applies warning filters.

## Scope by module

| Area | Example tests |
|------|----------------|
| Stack / region | **`tests/test_stack.py`** |
| Queries | **`tests/test_query.py`**, **`tests/test_basequery.py`** |
| Entries / assets | **`tests/test_entry.py`**, **`tests/test_assets.py`** |
| Taxonomy / global fields / live preview | **`tests/test_taxonomies.py`**, **`tests/test_global_fields.py`**, **`tests/test_live_preview.py`** |
| Early access | **`tests/test_early_find.py`**, **`tests/test_early_fetch.py`** |

## Hygiene

- No committed **`pytest.mark.skip`** without reason; avoid **`@unittest.skip`** unless environment is genuinely unavailable in CI.

## References

- [`dev-workflow/SKILL.md`](../dev-workflow/SKILL.md)
