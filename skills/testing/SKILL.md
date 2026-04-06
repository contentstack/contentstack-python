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

## References

- `.cursor/rules/testing.mdc`
