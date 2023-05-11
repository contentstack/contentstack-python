"""
This module implements the Requests API.
"""

# ************* Module https_connection.py **************
# Your code has been rated at 10.00/10  by pylint

import logging
import platform
import requests
from requests.adapters import HTTPAdapter
import contentstack
from contentstack.controller import get_request

log = logging.getLogger(__name__)


def __get_os_platform():
    os_platform = platform.system()
    if os_platform == 'Darwin':
        os_platform = 'macOS'
    elif not os_platform or os_platform == 'Java':
        os_platform = None
    elif os_platform and os_platform not in ['macOS', 'Windows']:
        os_platform = 'Linux'
    os_platform = {'name': os_platform, 'version': platform.release()}
    return os_platform


def user_agents():
    """Default User Agents for the Https"""
    header = {'sdk': dict(
        name=contentstack.__package__,
        version=contentstack.__version__
    ),
        'os': __get_os_platform,
        'Content-Type': 'application/json'}
    package = f"{contentstack.__title__}/{contentstack.__version__}"
    return {'User-Agent': str(header), "X-User-Agent": package}


def get_api_data(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(f"Error: {error}")
        return None
    else:
        return response.json()


class HTTPSConnection:  # R0903: Too few public methods
    def __init__(self, endpoint, headers, timeout, retry_strategy, live_preview):
        if None not in (endpoint, headers):
            self.session = requests.Session()
            self.payload = None
            self.endpoint = endpoint
            self.headers = headers
            self.timeout = timeout
            self.retry_strategy = retry_strategy
            self.live_preview = live_preview

    def impl_live_preview(self):
        if self.live_preview['enable']:
            print(self.live_preview)
            # Get all the params from live preview and make a request,
            # get the data and merger it to the base response
        pass

    def get(self, url):
        self.headers.update(user_agents())
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.session.mount('https://', adapter)
        self.impl_live_preview()
        return get_request(self.session, url, headers=self.headers, timeout=self.timeout)
