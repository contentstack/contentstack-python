# AGENTS.md — AI / automation context

## Project

| | |
|---|---|
| **Name** | **Contentstack** (PyPI) — **Python Content Delivery SDK** |
| **Purpose** | Python client for the **Content Delivery API (CDA)**: **Stack**, content types, entries, assets, queries, live preview, taxonomy, variants. Uses **`requests`** + **`urllib3.Retry`** via **`HTTPSConnection`**. |
| **Repository** | [contentstack/contentstack-python](https://github.com/contentstack/contentstack-python.git) |

## Tech stack

| Area | Details |
|------|---------|
| **Language** | **Python** (see **`setup.py`** `python_requires`, classifiers) |
| **HTTP** | **`requests`**, **`urllib3`** |
| **Tests** | **pytest** + **`unittest.TestCase`** under **`tests/`** |
| **Packaging** | **`setuptools`** / **`setup.py`**, package **`contentstack`** |

## Source layout

| Path | Role |
|------|------|
| `contentstack/stack.py` | **`Stack`**, **`ContentstackRegion`**, endpoint and **HTTPSConnection** wiring |
| `contentstack/https_connection.py`, `contentstack/controller.py` | Session, retries, **`get_request`** |
| `contentstack/query.py`, `contentstack/basequery.py` | Queries |
| `contentstack/entry.py`, `asset.py`, `contenttype.py`, … | Domain modules |
| `contentstack/__init__.py` | Public exports (**`Stack`**, **`Entry`**, **`Asset`**, …), **`__version__`** |
| `config.py` (repo root) | Test credentials and UIDs — **must not commit secrets** |
| `tests/*.py` | Integration-style tests importing **`config`** |

## Common commands

```bash
pip install -r requirements.txt
pip install -e .
pytest tests/
```

## Environment / test configuration

Tests load stack settings from root **`config.py`** (e.g. **HOST**, **APIKEY**, **DELIVERYTOKEN**, **ENVIRONMENT**). Use a local, gitignored file or sanitized values for CI. Do not commit secrets.

## Further guidance

- **Cursor rules:** [`.cursor/rules/README.md`](.cursor/rules/README.md)
- **Skills:** [`skills/README.md`](skills/README.md)

Product docs: [Content Delivery API](https://www.contentstack.com/docs/developers/apis/content-delivery-api/).
