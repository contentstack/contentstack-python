---
name: contentstack-delivery-python
description: Contentstack Python CDA SDK — Stack, queries, entries, assets, live preview, taxonomy.
---

# Contentstack Python Delivery SDK skill

## Entry

- **`contentstack.Stack(api_key, delivery_token, environment, ...)`** — **`contentstack/stack.py`**: validates credentials, sets **region** / **host**, builds **`endpoint`**, instantiates **`HTTPSConnection`** with **retry_strategy** and **live_preview**.

## Structure

- **`Stack`** — content types, entries, assets, sync helpers as implemented on the class.
- **Queries** — **`BaseQuery`**, **`Query`**, **`AssetQuery`**, **`EntryQueryable`**, etc.
- **Live preview** — **`live_preview`** dict and **`deep_merge_lp`** behavior.
- **Sync** — **`sync_init`**, **`pagination`**, **`sync_token`** on **`Stack`**.

## Extending

- Add query or stack methods consistent with [CDA query parameters](https://www.contentstack.com/docs/developers/apis/content-delivery-api/).
- Keep transport logic in **`HTTPSConnection`** / **`controller`** rather than duplicating **`requests`** setup.

## Dependencies

- **`requests`**, **`urllib3`** (**Retry**), **`python-dateutil`**

## Docs

- [Content Delivery API](https://www.contentstack.com/docs/developers/apis/content-delivery-api/)

## Rule shortcut

- `.cursor/rules/contentstack-delivery-python.mdc`
