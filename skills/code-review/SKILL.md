---
name: code-review
description: Use when reviewing PRs for the Python CDA SDK — public API, Stack, HTTP layer, tests, secrets.
---

# Code review – Contentstack Python CDA SDK

## When to use

- Reviewing a PR, self-review before submit, or running an automated review pass.

## Instructions

### Checklist

- [ ] **API:** New or changed `Stack` / content-type / query / entry methods documented; `contentstack/__init__.py` exports updated if needed.
- [ ] **Version:** `__version__` in `contentstack/__init__.py` aligned with release strategy for breaking changes.
- [ ] **HTTP:** `https_connection.py` / `controller.py` changes keep retry and timeout behavior predictable.
- [ ] **Tests:** `pytest tests/` passes; extend `tests/` when CDA behavior changes.
- [ ] **Secrets:** No tokens in repo; `config.py` remains local-only when it holds real credentials.

### Public API

- Exported `Stack`, `ContentType`, `Query`, asset/entry helpers match `README` and consumer expectations; `contentstack/__init__.py` `__all__` stays accurate when exports change.
- Docstrings on `Stack` and key public methods when behavior or options change.

### Compatibility

- Avoid breaking `Stack.__init__` signatures or method chains without a semver strategy; document migration for breaking changes in `setup.py` / `__version__`.

### HTTP / dependencies

- Changes to `requests`, retry behavior, or `HTTPSConnection` should stay consistent with `contentstack/controller.py` and `urllib3.Retry` usage in `stack.py`.

### Security

- No hardcoded tokens in source or docs; no logging of `api_key`, `delivery_token`, `preview_token`, or `management_token`.

### Severity (optional)

| Level | Examples |
|-------|----------|
| **Blocker** | Breaking public API without approval; security issue; no tests for new logic |
| **Major** | Inconsistent HTTP/retry behavior; README examples that don't match code |
| **Minor** | Style; minor docs |
