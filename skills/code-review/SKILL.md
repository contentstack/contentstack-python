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

## Public API

- **Exported** **`Stack`**, **ContentType**, **Query**, asset/entry helpers match **README** and consumer expectations; **`contentstack/__init__.py`** **`__all__`** stays accurate when exports change.
- **Docstrings** on **`Stack`** and key public methods when behavior or options change.

## Compatibility

- Avoid breaking **`Stack.__init__`** signatures or method chains without a semver strategy; document migration for breaking changes (**`setup.py`** / **`__version__`**).

## HTTP / dependencies

- Changes to **`requests`**, **retry** behavior, or **`HTTPSConnection`** should stay consistent with **`contentstack/controller.py`** and **`urllib3`** **`Retry`** usage in **`stack.py`**.

## Tests

- **Tests** hit the live CDA when using **`config`** credentials; extend **`tests/`** when request/response behavior changes. Do not commit new secrets.

## Security

- No hardcoded tokens in source or docs; no logging of **api keys**, **delivery tokens**, **preview**, or **management** tokens.

## References

- [`dev-workflow/SKILL.md`](../dev-workflow/SKILL.md)
- [`python-style/SKILL.md`](../python-style/SKILL.md)
