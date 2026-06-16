---
name: dev-workflow
description: Use for install, pytest, versioning, pre-commit hooks, and PR baseline in contentstack-python.
---

# Development workflow – Contentstack Python CDA SDK

## When to use

- Setting up locally, opening a PR, or matching CI expectations.
- Answering "how do we run tests?" or "what runs in CI?"
- Bumping the SDK version for a release.

## Instructions

### Branches & releases

- **Flow:** feature / fix branches → `staging` → `master`. Direct PRs to `master` from feature branches are rejected by [`.github/workflows/check-branch.yml`](../../.github/workflows/check-branch.yml).
- **PyPI:** publish a **GitHub Release** to trigger [`.github/workflows/python-publish.yml`](../../.github/workflows/python-publish.yml).

### Before a PR

1. **Install** — `pip install -r requirements.txt` then `pip install -e .` for an editable install.
2. **Tests** — `pytest tests/` (or `python -m pytest tests/`) from the repo root; `tests/pytest.ini` applies.
3. **Integration tests** use `config.py` at repo root for `HOST`, `APIKEY`, `DELIVERYTOKEN`, `ENVIRONMENT`, etc. Use local credentials only; **never commit** real tokens.

### Versioning

- Bump `__version__` in `contentstack/__init__.py` per semver for any user-visible SDK change.

### Pre-commit hooks

- **Talisman** — scans for secrets before commit (`.talismanrc`).
- **Snyk** — dependency vulnerability check (`snyk test --all-projects --fail-on=all`).
- Both hooks are in `.husky/pre-commit`. Skip with `SKIP_HOOK=1` only when justified.
