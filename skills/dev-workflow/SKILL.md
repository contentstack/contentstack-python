---
name: dev-workflow
description: Branches, install, tests, and versioning for contentstack-python.
---

# Development workflow — Contentstack Python CDA SDK

## Before a PR

1. **Install** — `pip install -r requirements.txt` and editable package as needed: `pip install -e .`
2. **Tests** — `pytest tests/` (or `python -m pytest tests/`) from the repo root; **`tests/pytest.ini`** applies.
3. **Integration tests** use **`config.py`** at repo root for **HOST**, **APIKEY**, **DELIVERYTOKEN**, **ENVIRONMENT**, etc. Use local credentials only; **never commit** real tokens—prefer a gitignored local **`config.py`** or environment-based loading if you refactor tests.

## Versioning

- Bump **`contentstack/__init__.py`** **`__version__`** and **`setup.py`**-driven releases per semver for user-visible SDK changes.

## References

- [`AGENTS.md`](../../AGENTS.md) · [`contentstack-utils/SKILL.md`](../contentstack-utils/SKILL.md)
