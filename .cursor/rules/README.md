# Cursor Rules — Contentstack Python CDA SDK

Rules for **contentstack-python**: Python **Content Delivery API (CDA)** SDK (`pip` package **Contentstack**).

## Rules overview

| Rule | Role |
|------|------|
| [`dev-workflow.md`](dev-workflow.md) | Branch/PR, install, tests |
| [`python.mdc`](python.mdc) | Python layout, `contentstack/`, `setup.py` |
| [`contentstack-delivery-python.mdc`](contentstack-delivery-python.mdc) | **Stack**, queries, live preview, **HTTPSConnection** / **requests** |
| [`testing.mdc`](testing.mdc) | **pytest** + **unittest** under `tests/` |
| [`code-review.mdc`](code-review.mdc) | PR checklist (**always applied**) |

## Rule application

| Context | Typical rules |
|---------|----------------|
| **Every session** | `code-review.mdc` |
| **Most files** | `dev-workflow.md` |
| **`contentstack/`** | `python.mdc` + `contentstack-delivery-python.mdc` |
| **`tests/**`** | `testing.mdc` |
| **Packaging** | `python.mdc` |

## Quick reference

| File | `alwaysApply` | Globs (summary) |
|------|---------------|-----------------|
| `dev-workflow.md` | no | `**/*.py`, `requirements.txt`, `setup.py`, `tests/pytest.ini` |
| `python.mdc` | no | `contentstack/**/*.py`, `setup.py` |
| `contentstack-delivery-python.mdc` | no | `contentstack/**/*.py` |
| `testing.mdc` | no | `tests/**/*.py`, `tests/pytest.ini` |
| `code-review.mdc` | **yes** | — |

## Skills

- [`skills/README.md`](../../skills/README.md) · [`AGENTS.md`](../../AGENTS.md)
