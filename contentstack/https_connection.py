"""
This module implements the Requests API.
"""

# ************* Module https_connection.py **************
# Your code has been rated at 10.00/10  by pylint

import logging
import platform
from json import JSONDecodeError
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

    def __init__(self, endpoint, headers, timeout, retry_strategy):
        if None not in (endpoint, headers):
            self.payload = None
            self.endpoint = endpoint
            self.headers = headers
            self.timeout = timeout  # default timeout (period=30) seconds
            self.retry_strategy = retry_strategy

    def get(self, url):

        import requests
        from requests.adapters import HTTPAdapter
        from requests.exceptions import HTTPError, Timeout

        """
        Here we create a response object, `response` which will store the request-response.
        We use requests.get method since we are sending a GET request.
        The four arguments we pass are url, verify(ssl), timeout, headers
        """
        try:
            self.headers.update(user_agents())
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            # log.info('url: %s', url)
            response = session.get(url, verify=True, headers=self.headers, timeout=self.timeout)
            if response.encoding is None:
                response.encoding = 'utf-8'
            if response is not None:
                return response.json()
            else:
                return {"error": "error details not found", "error_code": 422, "error_message": "unknown error"}
        except Timeout:
            raise TimeoutError('The request timed out')
        except ConnectionError:
            raise ConnectionError('Connection error occurred')
        except JSONDecodeError:
            raise TypeError('Invalid JSON in request')
        except HTTPError:
            raise HTTPError('Http Error Occurred')
