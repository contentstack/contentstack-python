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

log = logging.getLogger(__name__)


def __get_os_platform():
    """ Returns client platform """
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
    header = {'sdk': dict(
        name=contentstack.__package__,
        version=contentstack.__version__
    ),
        'os': __get_os_platform,
        'Content-Type': 'application/json'}
    package = f"contentstack-python/{contentstack.__version__}"
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
    """Make Https Request to fetch the result as per requested url"""

    def __init__(self, endpoint, headers, timeout, retry_strategy, live_preview):
        if None not in (endpoint, headers):
            self.payload = None
            self.endpoint = endpoint
            self.headers = headers
            self.timeout = timeout  # default timeout (period=30) seconds
            self.retry_strategy = retry_strategy
            self.live_preview = live_preview

    def get(self, url):

        """
        Here we create a response object, `response` which will store the request-response.
        We use requests. Get method since we are sending a GET request.
        The four arguments we pass are url, verify(ssl), timeout, headers
        """
        try:
            self.headers.update(user_agents())
            session = requests.Session()
            adapter = HTTPAdapter(max_retries=self.retry_strategy)
            session.mount('https://', adapter)
            response = session.get(url, verify=True, headers=self.headers, timeout=self.timeout)
            response.encoding = "utf-8"
            # response.raise_for_status()
            session.close()
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except requests.exceptions.Timeout as timeout_error:
            print(f"Timeout error occurred: {timeout_error}")
        except requests.exceptions.ConnectionError as connection_error:
            print(f"Connection error occurred: {connection_error}")
        except requests.exceptions.RequestException as request_exception:
            print(f"An error occurred: {request_exception}")
        else:
            print("API request successful")
            return response.json()
        finally:
            print("API request complete")

        # if response.status_code == 200 and response.encoding is None:
        #     response.encoding = 'utf-8'
        #     return response.json()
        # else:
        #     return get_api_data(response)
