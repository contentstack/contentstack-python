---
name: framework
description: Use for HTTPSConnection, requests session, urllib3 retries, and timeouts in contentstack-python.
---

# Framework / HTTP – Contentstack Python CDA SDK

## When to use

- Editing `contentstack/https_connection.py` or `contentstack/controller.py`.
- Changing retry policy, timeouts, or `requests` session configuration.
- Debugging connection or retry failures.

## Instructions

### Integration point

- `contentstack/stack.py` constructs `HTTPSConnection` with `endpoint`, `headers`, `timeout`, `retry_strategy` (`urllib3.Retry`), and `live_preview`.
- `contentstack/https_connection.py` mounts `HTTPAdapter(max_retries=...)` and calls `get_request` from `contentstack/controller.py`.

### When to change

- **Retry / timeout behavior:** align `Stack` defaults with `HTTPSConnection` and `HTTPAdapter` usage; avoid breaking existing `Retry` constructor expectations.
- **Headers / user-agent:** `user_agents()` in `https_connection.py` uses `contentstack.__title__` and `__version__`.

### Testing

- **Integration** — full stack via `tests/` and `config`; unit-style assertions on URL building and headers where tests exist.
