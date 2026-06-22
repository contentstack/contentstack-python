# CHANGELOG

## _v2.6.0_

### **Date: 22-June-2026**

- Dynamic endpoint resolution via new `Endpoint` class.
- Region-to-URL mapping is now loaded from a bundled `regions.json` (sourced from `artifacts.contentstack.com`) instead of hardcoded `if/elif` chains.
- Added `Endpoint.get_contentstack_endpoint(region, service, omit_https)` — resolves any supported region to its `contentDelivery`, `contentManagement`, or other service URL.
- Added `contentstack.get_contentstack_endpoint()` module-level proxy.
- `Stack` now auto-resolves `host` and `live_preview` management host via `Endpoint` on initialization.
- Bundled `contentstack/assets/regions.json` included in `package_data` — always present after `pip install`.
- `setup.py` auto-refreshes `regions.json` at build time via a custom `BuildPyWithRegions` command; network failures warn but never block the build.
- Runtime fallback: if `regions.json` is absent, the SDK downloads it live on the first `Endpoint` call.
- Added `refresh_regions()` utility to programmatically download the latest regions manifest from the Contentstack CDN and overwrite the bundled `assets/regions.json` (`from contentstack import refresh_regions`).
- Added `python3 -m contentstack.region_refresh` CLI command for refreshing the registry after `pip install` (source-tree script `scripts/download_regions.py` is for contributors only).

## _v2.5.1_

### **Date: 15-April-2026**

- Fixed security issues.

## _v2.5.0_

### **Date: 02-March-2026**

- Assets fields(DAM 2.0) support added
## _v2.4.1_

### **Date: 10-November-2025**

- Improved Error messages. 

## _v2.4.0_

### **Date: 01-September-2025**

- AWS AU and GCP EU region support added.

## _v2.3.0_

### **Date: 21-July-2025**

- Taxonomy Support Added.

## _v2.2.0_

### **Date: 14-July-2025**

- Variants Support Added.

## _v2.1.1_

### **Date: 07-July-2025**

- Fixed sanity testcases and removed hardcoded secrets.

## _v2.1.0_

### **Date: 02-June-2025**

- Global fields support added.

## _v2.0.1_

### **Date: 12-MAY-2025**

- Setuptools package version bump

## _v2.0.0_

### **Date: 28-APRIL-2025**

- Custom logger support

## _v1.11.2_

### **Date: 21-APRIL-2025**

- Version bump and security fixes.

## _v1.11.1_

### **Date: 26-MARCH-2025**

- Updated the dependencies

## _v1.11.0_

### **Date: 17-MARCH-2025**

- Added Livepreview 2.0 and Timeline support

## _v1.10.0_

### **Date: 03-SEPTEMBER-2024**

- Fetch asset by any other field than UID

## _v1.9.0_

### **Date: 14-MAY-2024**

- Added GCP NA Support

---
## _v1.8.2_

### **Date: 05-DECEMBER-2023**

- Empty package removed and added python 3.11 support

---

## _v1.8.1_

### **Date: 29-NOVEMBER-2023**

- SNYK issues fixed 
- General code improvement clean up

---

## _v1.8.0_

### **Date: 26-MAY-2023**

- AZURE_EU, Region support added
- Include Metadata support added to asset, entry and query
- General code improvement clean up
- Updated code for Live Preview

---

## _v1.7.0_

### **Date: 8-APR-2022**

Region support added.

- AZURE_NA support added
- General code clean up

---

## _v1.6.0_

### **Date: 11-Aug-2021**

Live Preview support added.

- Stack.live_preview_query function added in Stack
- live preview funtions added in config

---

## _v1.5.1_

### **Date: 1-Aug-2021**

Issue #17 resolved.
Stack.sync_init uses wrong parameter names

---

## _v1.5.0_

### **Date: 22-Jul-2021**

contentstack-utils updated to v1.1.0

---

## _v1.4.0_

### **Date: 05-Apr-2021**

Entry - include_embedded_objects support added
Query - include_embedded_objects support added

---

## _v1.3.0_

Date: 26-Feb-2021

- Retry policy and timeout support included
- Set default timeout 30 sec

---

## _v1.2.0_

Date: 08-Dec-2020

- include_fallback Support Added
- Timeout support included

- Entry
    - added support for include_fallback.
- Asset
    - added support for include_fallback.
- AssetQueryable
    - added support for include_fallback.
- Query
    - added support for include_fallback.

---

## _v1.1.0_

Date: 10-Aug-2020 - include_reference issue fixed

EntryQueryable

- updated include_reference function.

---

## _v1.0.0_

Date: 17-Jun-2020 - initial release

Stack

- Initialisation of stack has been modified
- External config support moved to stack initialisation optional paramters
- Added support for whereIn(String key) and whereNotIn(String key) methods in Query

Assets

- Changes incorporated in Asset class.

Entry

- Changes incorporated in the entry class.

Query

- Changes incorporated in the Query class.

---

## _v0.1.0_

November-18, 2019 -beta release

Initial release for the contentstack-python-sdk for Content Delivery API

---
