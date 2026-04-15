---
name: framework
description: HTTP layer for the Python CDA SDK — requests Session, urllib3 retries, HTTPSConnection.
---

# Framework skill — requests + Contentstack Python SDK

## Integration point

- **`contentstack/stack.py`** constructs **`HTTPSConnection`** with **endpoint**, **headers**, **timeout**, **`retry_strategy`** (**`urllib3.Retry`**), and **live_preview**.
- **`contentstack/https_connection.py`** mounts **`HTTPAdapter(max_retries=...)`** and calls **`get_request`** from **`contentstack/controller.py`**.

## When to change

- **Retry / timeout** behavior: align **`Stack`** defaults with **`HTTPSConnection`** and **`HTTPAdapter`** usage; avoid breaking existing **`Retry`** constructor expectations.
- **Headers / user-agent** — **`user_agents()`** in **`https_connection.py`** uses **`contentstack.__title__`** and **`__version__`**.

## Testing

- **Integration** — full stack via **`tests/`** and **`config`**; **unit-style** assertions on URL building and headers where tests exist.

## Related skills

- [`contentstack-utils/SKILL.md`](../contentstack-utils/SKILL.md)
