"""
This module implements the Requests API.
"""

import logging
import platform
import requests
from requests.adapters import HTTPAdapter
import contentstack
from contentstack.controller import get_request

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
    header = {'sdk': dict(name=contentstack.__package__,
                          version=contentstack.__version__
                          ), 'os': __get_os_platform(), 'Content-Type': 'application/json'}
    package = f"{contentstack.__title__}/{contentstack.__version__}"
    return {'User-Agent': str(header), "X-User-Agent": package}


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

    def get(self, url):
        self.headers.update(user_agents())
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.session.mount('https://', adapter)
        return get_request(self.session, url, headers=self.headers, timeout=self.timeout)
