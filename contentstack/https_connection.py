"""
This module implements the Requests API.
"""

# ************* Module https_connection.py **************
# Your code has been rated at 10.00/10  by pylint

import platform
from json import JSONDecodeError
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import requests
from requests.exceptions import Timeout, HTTPError
import logging
import contentstack

log = logging.getLogger(__name__)


def __get_os_platform():
    """ returns client platform """
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
    """User Agents for the Https"""
    header = {'sdk': dict(name=contentstack.__package__, version=contentstack.__version__),
              'os': __get_os_platform,
              'Content-Type': 'application/json'}
    package = "contentstack-python/{}".format(contentstack.__version__)
    return {'User-Agent': str(header), "X-User-Agent": package}


class HTTPSConnection:  # R0903: Too few public methods
    """Make Https Request to fetch the result as per requested url"""
    # BACKOFF_MAX = 120

    def __init__(self, endpoint, headers, timeout, retry_strategy):
        if None not in (endpoint, headers):
            self.payload = None
            self.endpoint = endpoint
            self.headers = headers
            self.timeout = timeout
            self.retry_strategy = retry_strategy  # default timeout (period=30) seconds

    def get(self, url):
        """
        Here we create a response object, `response` which will store the request-response.
        We use requests.get method since we are sending a GET request.
        The four arguments we pass are url, verify(ssl), timeout, headers
        """
        try:
            self.headers.update(user_agents())

            # Setting up custom retry adapter
            session = requests.Session()
            # retry on 429 rate limit exceeded
            # Diagnosing a 408 request timeout
            # backoff_factor works on algorithm {backoff factor} * (2 ** ({number of total retries} - 1))
            # This value is by default 0, meaning no exponential backoff will be set and
            # retries will immediately execute. Make sure to set this to 1 in to avoid hammering your servers!.
            # retries = Retry(total=5, backoff_factor=1, status_forcelist=[408, 429], allowed_methods=["GET"])

            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            log.info('url: %s', url)
            response = session.get(url, verify=True, headers=self.headers, timeout=self.timeout)
            if response.encoding is None:
                response.encoding = 'utf-8'

            if response is not None:
                return response.json()
            else:
                return {"error": "Unknown error", "error_code": 000, "error_message": "Unknown error"}

        except Timeout:
            raise TimeoutError('The request timed out')
        except ConnectionError:
            raise ConnectionError('Connection error occurred')
        except JSONDecodeError:
            raise TypeError('Invalid JSON in request')
        except HTTPError:
            raise HTTPError('Http Error Occurred')

