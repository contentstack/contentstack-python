---
name: python-style
description: Python layout, packaging, and conventions for the Contentstack CDA SDK package.
---

# Python style — Contentstack CDA SDK

## Layout

- **`contentstack/stack.py`** — **`Stack`**, **`ContentstackRegion`**.
- **`contentstack/query.py`**, **`basequery.py`** — query building.
- **`contentstack/entry.py`**, **`asset.py`**, **`contenttype.py`**, **`taxonomy.py`**, **`globalfields.py`** — domain objects.
- **`contentstack/https_connection.py`**, **`controller.py`** — HTTP.
- **`contentstack/error_messages.py`**, **`utility.py`** — shared helpers.

## Style

- Match existing patterns (typing on **`Stack`**, **unittest**-style tests in **`tests/`**).
- Prefer clear public APIs over internal churn; keep module boundaries similar to neighboring files.

## Dependencies

- **`requests`**, **`python-dateutil`**, **`urllib3`** (Retry) — see **`setup.py`** **`install_requires`**.

## Security

- Do not log **delivery tokens**, **preview tokens**, **api keys**, or **management** tokens; follow existing logging on **`Stack`**.
