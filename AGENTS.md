# Contentstack Python CDA SDK – Agent guide

**Universal entry point** for contributors and AI agents. Detailed conventions live in **`skills/*/SKILL.md`**.

## What this repo is

| Field | Detail |
|--------|--------|
| **Name:** | [contentstack/contentstack-python](https://github.com/contentstack/contentstack-python) |
| **Purpose:** | Python client for the **Content Delivery API (CDA)**: stacks, content types, entries, assets, queries, live preview, taxonomy, and variants. Uses **`requests`** + **`urllib3.Retry`** via **`HTTPSConnection`**. |
| **Out of scope:** | Content management (create / update / delete) — use `contentstack-management-python` for CMA operations. |

## Tech stack (at a glance)

| Area | Details |
|------|---------|
| Language | Python ≥ 3.6 (`setup.py` `python_requires`) |
| Build | `setuptools` / `setup.py`; package `contentstack` |
| Tests | `pytest` — `tests/test_*.py`; config in `tests/pytest.ini` |
| Lint / coverage | `ruff`, `flake8`, `black`, `isort`; `pytest-cov` for coverage |
| HTTP | `requests`, `urllib3` |

## Commands (quick reference)

| Command Type | Command |
|---|---|
| Build | `pip install -e .` |
| Install deps | `pip install -r requirements.txt` |
| Test | `pytest tests/` |
| Coverage | `pytest --cov=contentstack tests/` |
| Lint | `ruff check contentstack/` |

CI: [`.github/workflows/python-publish.yml`](.github/workflows/python-publish.yml) · [`.github/workflows/check-branch.yml`](.github/workflows/check-branch.yml)

## Where the documentation lives: skills

| Skill | Path | What it covers |
|---|---|---|
| Development workflow | [`skills/dev-workflow/SKILL.md`](skills/dev-workflow/SKILL.md) | Install, tests, `config.py`, versioning, PR baseline |
| Contentstack CDA SDK | [`skills/contentstack-utils/SKILL.md`](skills/contentstack-utils/SKILL.md) | `Stack`, queries, entries, assets, live preview, taxonomy, HTTP session |
| Python style & repo layout | [`skills/python-style/SKILL.md`](skills/python-style/SKILL.md) | Package layout, `setup.py`, naming conventions, no secret logging |
| Testing | [`skills/testing/SKILL.md`](skills/testing/SKILL.md) | `pytest`, `tests/`, `config.py`, credential hygiene |
| Code review | [`skills/code-review/SKILL.md`](skills/code-review/SKILL.md) | PR checklist, public API, `Stack`, HTTP layer, secrets |
| Framework / HTTP | [`skills/framework/SKILL.md`](skills/framework/SKILL.md) | `requests`, `HTTPSConnection`, `urllib3` retries, timeouts |

An index with "when to use" hints is in [`skills/README.md`](skills/README.md).

## Using Cursor (optional)

If you use **Cursor**, [`.cursor/rules/README.md`](.cursor/rules/README.md) only points to **`AGENTS.md`**—same docs as everyone else.
