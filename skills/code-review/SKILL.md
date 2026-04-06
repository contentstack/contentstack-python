---
name: code-review
description: PR review for Contentstack Python CDA SDK — public API, Stack, HTTP layer, tests.
---

# Code review — Contentstack Python CDA SDK

## Checklist

- [ ] **API:** New or changed **`Stack`** / content-type / query / entry methods documented; **`contentstack/__init__.py`** exports updated if needed.
- [ ] **Version:** **`__version__`** in **`contentstack/__init__.py`** aligned with release strategy for breaking changes.
- [ ] **HTTP:** **`https_connection.py`** / **`controller.py`** changes keep retry and timeout behavior predictable.
- [ ] **Tests:** **`pytest tests/`** passes; extend **`tests/`** when CDA behavior changes.
- [ ] **Secrets:** No tokens in repo; **`config.py`** remains local-only when it holds real credentials.

## References

- `.cursor/rules/code-review.mdc`
- `.cursor/rules/dev-workflow.md`
