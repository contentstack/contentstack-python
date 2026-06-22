"""
Endpoint — Contentstack region-to-URL resolver.

Resolves Contentstack service endpoint URLs for any supported region.
Region data is loaded from contentstack/assets/regions.json (bundled) and
cached in-memory for the lifetime of the process. When the bundled file is
absent the class attempts a live download from the Contentstack CDN so the
SDK continues to work even when the file was not created during installation.
"""

import json
import os
import re

REGIONS_URL = 'https://artifacts.contentstack.com/regions.json'


class Endpoint:
    """
    Resolves Contentstack service endpoint URLs for any supported region.

    Usage::

        from contentstack.endpoint import Endpoint

        # Single service URL
        url = Endpoint.get_contentstack_endpoint('eu', 'contentDelivery')
        # 'https://eu-cdn.contentstack.com'

        # All services for a region
        endpoints = Endpoint.get_contentstack_endpoint('azure-na')
        # {'contentDelivery': 'https://...', 'contentManagement': 'https://...', ...}

        # Strip scheme (useful when setting host directly)
        host = Endpoint.get_contentstack_endpoint('gcp-eu', 'contentDelivery', omit_https=True)
        # 'gcp-eu-cdn.contentstack.com'
    """

    _regions_data = None  # in-memory cache — shared across all instances

    @staticmethod
    def get_contentstack_endpoint(region='us', service='', omit_https=False):
        """
        Resolve a Contentstack service endpoint URL for a given region.

        :param region: Region ID or alias ('us', 'eu', 'azure-na', 'gcp-eu', etc.).
                       Defaults to 'us' (AWS North America).
        :param service: Service key ('contentDelivery', 'contentManagement', ...).
                        When empty, returns a dict of all endpoints for the region.
        :param omit_https: When True, strips 'https://' prefix from returned URL(s).
        :returns: str when service is provided, dict[str,str] otherwise.
        :raises ValueError: When region is empty, unknown, or service is not found.
        :raises RuntimeError: When regions.json cannot be read or parsed.
        """
        if not region:
            raise ValueError('Empty region provided. Please put valid region.')

        data = Endpoint._load_regions()
        normalized = region.strip().lower()
        region_row = Endpoint._find_region(data['regions'], normalized)

        if region_row is None:
            raise ValueError(f'Invalid region: {region}')

        if service:
            if service not in region_row['endpoints']:
                raise ValueError(
                    f'Service "{service}" not found for region "{region_row["id"]}"'
                )
            url = region_row['endpoints'][service]
            return Endpoint._strip_https(url) if omit_https else url

        endpoints = region_row['endpoints']
        if omit_https:
            return {k: Endpoint._strip_https(v) for k, v in endpoints.items()}
        return dict(endpoints)

    @staticmethod
    def _load_regions():
        """
        Load and cache regions.json.

        Resolution order:
          1. In-memory static cache (zero I/O after first call)
          2. contentstack/assets/regions.json on disk (written by download script)
          3. Live download from artifacts.contentstack.com (fallback)
        """
        if Endpoint._regions_data is not None:
            return Endpoint._regions_data

        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        path = os.path.join(assets_dir, 'regions.json')

        if not os.path.exists(path):
            Endpoint._download_and_save(path)

        if not os.path.exists(path):
            raise RuntimeError(
                'contentstack: regions.json not found and could not be downloaded. '
                'Run "python scripts/download_regions.py" and ensure network access.'
            )

        try:
            with open(path, 'r', encoding='utf-8') as f:
                decoded = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                f'contentstack: Could not read or parse regions.json: {exc}. '
                'Run "python scripts/download_regions.py" to re-download it.'
            ) from exc

        if not isinstance(decoded, dict) or 'regions' not in decoded:
            raise RuntimeError(
                'contentstack: regions.json is corrupt. '
                'Run "python scripts/download_regions.py" to re-download it.'
            )

        Endpoint._regions_data = decoded
        return Endpoint._regions_data

    @staticmethod
    def _download_and_save(dest):
        """
        Download regions.json from the Contentstack CDN and save to disk.
        Uses the requests library (already an SDK dependency).
        Silent on failure — the caller decides whether a missing file is fatal.

        :param dest: Absolute path to write the file to.
        """
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        try:
            import requests
            response = requests.get(REGIONS_URL, timeout=30)
            response.raise_for_status()
            data = response.text
        except Exception:  # noqa: BLE001
            return

        try:
            decoded = json.loads(data)
        except json.JSONDecodeError:
            return

        if isinstance(decoded, dict) and 'regions' in decoded:
            try:
                with open(dest, 'w', encoding='utf-8') as f:
                    f.write(data)
            except OSError:
                pass

    @staticmethod
    def _find_region(regions, input_str):
        """
        Find a region entry by its id or any alias (case-insensitive).

        Two-pass: exact id match first, then alias[] scan — mirrors PHP implementation.

        :param regions: list of region dicts from regions.json
        :param input_str: already-lowercased input
        :returns: region dict or None
        """
        for row in regions:
            if row['id'] == input_str:
                return row
        for row in regions:
            for alias in row.get('alias', []):
                if alias.lower() == input_str:
                    return row
        return None

    @staticmethod
    def _strip_https(url):
        """Strip the https:// (or http://) scheme from a URL string."""
        return re.sub(r'^https?://', '', url)

    @staticmethod
    def reset_cache():
        """Reset the internal region cache. Intended for testing only."""
        Endpoint._regions_data = None
