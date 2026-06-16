---
name: python-style
description: Use for Python package layout, setup.py conventions, and style in contentstack-python.
---

# Python style – Contentstack CDA SDK

## When to use

- Editing any Python under `contentstack/`, `setup.py`, or `requirements.txt`.
- Adding modules or changing how the public package surface is exported.

## Instructions

### Layout

| Path | Role |
|------|------|
| `contentstack/stack.py` | `Stack`, `ContentstackRegion` |
| `contentstack/query.py`, `basequery.py` | Query building |
| `contentstack/entry.py`, `asset.py`, `contenttype.py` | Domain objects |
| `contentstack/taxonomy.py`, `globalfields.py`, `variants.py` | Advanced features |
| `contentstack/https_connection.py`, `controller.py` | HTTP session + request dispatch |
| `contentstack/error_messages.py`, `utility.py` | Shared helpers |
| `contentstack/__init__.py` | Public exports (`Stack`, `Entry`, `Asset`, …), `__version__` |

### Style

- Match existing patterns (typing on `Stack`, `unittest`-style tests in `tests/`).
- Prefer clear public APIs over internal churn; keep module boundaries similar to neighboring files.

### Dependencies

- `requests`, `python-dateutil`, `urllib3` (Retry) — see `setup.py` `install_requires`.
- Do not add new runtime dependencies without updating `setup.py` and `requirements.txt`.

### Security

- Do not log `delivery_token`, `preview_token`, `api_key`, or `management_token`; follow existing logging in `Stack`.
