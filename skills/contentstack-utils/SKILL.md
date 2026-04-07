---
name: contentstack-utils
description: Contentstack Python CDA SDK — Stack, queries, entries, assets, live preview, taxonomy, HTTP session.
---

# Contentstack Python Delivery SDK (`contentstack/`)

## Stack entry

- **`Stack`** in **`contentstack/stack.py`**: validates **api_key**, **delivery_token**, **environment**; resolves **region → host** via **`ContentstackRegion`**; builds **`endpoint`**; wires **`HTTPSConnection`** with **headers**, **timeout**, **`urllib3.Retry`**, and optional **`live_preview`** / **`branch`** / **`early_access`**.

## Features

- **Content types & entries** — **`contenttype.py`**, **`entry.py`**, **`entryqueryable.py`**.
- **Queries** — **`basequery.py`**, **`query.py`**; chain methods align with CDA query parameters.
- **Assets** — **`asset.py`**, **`assetquery.py`**.
- **Taxonomy, global fields, variants, image transform** — **`taxonomy.py`**, **`globalfields.py`**, **`variants.py`**, **`image_transform.py`**.
- **Sync** — **`Stack.sync_init`**, **`pagination`**, **`sync_token`** → **`/stacks/sync`** via **`__sync_request`**.

## Live preview

- **`live_preview`** dict (**enable**, **host**, **authorization**, etc.) merged in **`deep_merge_lp.py`** / stack setup; keep behavior aligned with **`tests/test_live_preview.py`**.

## HTTP layer

- **`https_connection.py`** — **`requests.Session`**, **`HTTPAdapter`**, **`get_request`** from **`controller.py`**; user-agent uses **`contentstack.__title__`** / **`__version__`**.

## Extending

- Add query or stack methods consistent with [CDA query parameters](https://www.contentstack.com/docs/developers/apis/content-delivery-api/).
- Keep transport logic in **`HTTPSConnection`** / **`controller`** rather than duplicating **`requests`** setup.

## Dependencies

- **`requests`**, **`urllib3`** (**Retry**), **`python-dateutil`**

## Related skills

- [`framework/SKILL.md`](../framework/SKILL.md) — retries, **`HTTPAdapter`**, timeouts

## Docs

- [Content Delivery API](https://www.contentstack.com/docs/developers/apis/content-delivery-api/)
