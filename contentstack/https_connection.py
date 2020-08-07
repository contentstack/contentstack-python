"""
This module implements the Requests API.
"""

# ************* Module https_connection.py **************
# Your code has been rated at 10.00/10  by pylint

import platform
from json import JSONDecodeError

import requests
from requests.exceptions import Timeout, HTTPError

import contentstack


def get_os_platform():
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
              'os': get_os_platform,
              'Content-Type': 'application/json'}
    package = "contentstack-python/{}".format(contentstack.__version__)
    return {'User-Agent': str(header), "X-User-Agent": package}


class HTTPSConnection:  # R0903: Too few public methods
    """Make Https Request to fetch the result as per requested url"""

    def __init__(self, endpoint, headers):
        if None not in (endpoint, headers):
            self.payload = None
            self.endpoint = endpoint
            self.headers = headers
            self.default_timeout = 10

    def get(self, url):
        """
        Here we create a response object ‘response’ which will store the request-response.
        We use requests.get method since we are sending a GET request.
        The four arguments we pass are url, verify(ssl), timeout, headers
        """
        try:
            self.headers.update(user_agents())
            response = requests.get(url, verify=True, headers=self.headers)
            response.encoding = 'utf-8'
            return response.json()
        except Timeout:
            raise TimeoutError('The request timed out')
        except ConnectionError:
            raise ConnectionError('Connection error occurred')
        except JSONDecodeError:
            raise TypeError('Invalid JSON in request')
        except HTTPError:
            raise HTTPError('Http Error Occurred')

    def update_connection_timeout(self, timeout: int):
        """Facilitate to update timeout for the https request"""
        self.default_timeout = timeout
