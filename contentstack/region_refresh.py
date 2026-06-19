"""
Utility to pull the latest regions.json from the Contentstack CDN and
overwrite the bundled copy at contentstack/assets/regions.json.

Exposed as a package-level function so tooling and CI pipelines can call it
programmatically instead of invoking the script directly:

    from contentstack import refresh_regions
    refresh_regions()
"""

import json
import os
import sys
import urllib.request

_REGIONS_URL = "https://artifacts.contentstack.com/regions.json"
_ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets", "regions.json")


def refresh_regions(
    url: str = _REGIONS_URL,
    dest: str = _ASSET_PATH,
    *,
    timeout: int = 30,
    silent: bool = False,
) -> dict:
    """
    Download the latest regions manifest from the Contentstack CDN and write
    it to the bundled assets file so all consumers get the update.

    @param url     - URL to fetch regions.json from (defaults to Contentstack CDN)
    @param dest    - Destination file path (defaults to contentstack/assets/regions.json)
    @param timeout - HTTP request timeout in seconds
    @param silent  - Suppress progress output when True
    @returns The parsed regions dict on success
    @raises RuntimeError on download failure, invalid JSON, or unexpected schema
    """
    dest = os.path.normpath(dest)

    if not silent:
        print(f"Fetching {url} ...")

    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
    except Exception as exc:
        raise RuntimeError(f"Could not download regions.json: {exc}") from exc

    try:
        decoded = json.loads(data)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Downloaded content is not valid JSON: {exc}") from exc

    if not isinstance(decoded, dict) or "regions" not in decoded:
        raise RuntimeError("Downloaded JSON does not contain a 'regions' key.")

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(decoded, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    region_count = len(decoded["regions"])
    if not silent:
        print(f"OK: Wrote {region_count} regions to {dest}")

    return decoded


def _cli_main() -> int:
    """Entry point kept for backward compatibility with the scripts/ invocation."""
    try:
        refresh_regions()
        return 0
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(_cli_main())
