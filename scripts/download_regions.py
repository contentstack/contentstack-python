"""
Downloads the Contentstack regions registry from the official source and
saves it to contentstack/assets/regions.json.

Run manually:
    python scripts/download_regions.py

Can also be wired into setup.py post-install hooks or tox envsetup if needed.
"""

import json
import os
import sys
import requests

REGIONS_URL = 'https://artifacts.contentstack.com/regions.json'

DEST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'contentstack', 'assets', 'regions.json'
)


def download():
    dest_dir = os.path.dirname(DEST)
    os.makedirs(dest_dir, exist_ok=True)

    print(f'contentstack: Downloading regions.json from {REGIONS_URL} ...')

    try:
        response = requests.get(REGIONS_URL, timeout=30)
        response.raise_for_status()
        data = response.text
    except Exception as exc:
        sys.stderr.write(
            f'contentstack: Warning — could not download regions.json: {exc}. '
            'The SDK will attempt to download it at runtime on first use.\n'
        )
        sys.exit(0)  # non-fatal

    try:
        decoded = json.loads(data)
    except json.JSONDecodeError:
        sys.stderr.write(
            'contentstack: Warning — downloaded data is not valid JSON.\n'
        )
        sys.exit(0)

    if not isinstance(decoded, dict) or 'regions' not in decoded or \
            not isinstance(decoded['regions'], list):
        sys.stderr.write(
            'contentstack: Warning — downloaded data is not a valid regions.json.\n'
        )
        sys.exit(0)

    try:
        with open(DEST, 'w', encoding='utf-8') as f:
            f.write(data)
    except OSError as exc:
        sys.stderr.write(
            f'contentstack: Warning — could not write regions.json to {DEST}: {exc}\n'
        )
        sys.exit(0)

    region_count = len(decoded['regions'])
    print(f'contentstack: regions.json downloaded ({region_count} regions) → {DEST}')


if __name__ == '__main__':
    download()
