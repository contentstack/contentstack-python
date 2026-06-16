---
name: testing
description: Use for pytest setup, test layout, config.py credentials, and hygiene in contentstack-python.
---

# Testing – Contentstack Python CDA SDK

## When to use

- Adding or changing tests under `tests/`.
- Debugging test failures or understanding how credentials are loaded.
- Improving test coverage for a new feature.

## Instructions

### Commands

| Goal | Command |
|------|---------|
| Full test tree | `pytest tests/` |
| Single file | `pytest tests/test_stack.py` |
| With coverage | `pytest --cov=contentstack tests/` |

### Environment

- Root `config.py`: `HOST`, `APIKEY`, `DELIVERYTOKEN`, `ENVIRONMENT`, optional `PREVIEW_TOKEN`, content UIDs for specific suites.
- Use a **local** `config.py` or sanitized values; never commit live secrets.

### Conventions

- Tests subclass `unittest.TestCase`; `tests/pytest.ini` applies warning filters.

### Scope by module

| Area | Test files |
|------|------------|
| Stack / region | `tests/test_stack.py` |
| Queries | `tests/test_query.py`, `tests/test_basequery.py` |
| Entries / assets | `tests/test_entry.py`, `tests/test_assets.py` |
| Taxonomy / global fields / live preview | `tests/test_taxonomies.py`, `tests/test_global_fields.py`, `tests/test_live_preview.py` |
| Early access | `tests/test_early_find.py`, `tests/test_early_fetch.py` |

### Hygiene

- No committed `pytest.mark.skip` without reason; avoid `@unittest.skip` unless environment is genuinely unavailable in CI.
- Do not commit real API keys, delivery tokens, or preview tokens.
