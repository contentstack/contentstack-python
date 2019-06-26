import requests
from urllib3.util import timeout
from contentstack import config
import urllib.parse
import logging


class HTTPRequestConnection(object):

    def __init__(self, url_path, query=dict, local_headers=dict):
        self.result = None
        self.error = None
        self.url_path = url_path
        self._query_prams = query
        self._local_headers = local_headers
        self._local_headers['X-User-Agent'] = self._contentstack_user_agent()
        self._local_headers['Content-Type'] = 'application/json'
        self.url_path = config.Config().get_endpoint(self.url_path)
        if 'environment' in self._local_headers:
            self._query_prams['environment'] = self._local_headers['environment']

    def http_request(self) -> tuple:
        response = requests.get(self.url_path, params=self._query_prams, headers=self._local_headers)
        if response.ok:
            self.result = response.json()
        else:
            self.error = response.json()

        return self.result, self.error

    @staticmethod
    def _contentstack_user_agent() -> str:
        """
        X-Contentstack-User-Agent header.
        """
        header = {'sdk': {
            'name': 'contentstack.python',
            'version': "1.0.0"
        }}
        # from contentstack import __version__
        # from sys import platform as cs_plateforom
        # os_name = cs_plateforom.system()
        # if os_name == 'Darwin':
        #    os_name = 'macOS'
        # elif not os_name or os_name == 'Java':
        #    os_name = None
        # elif os_name and os_name not in ['macOS', 'Windows']:
        #    os_name = 'Linux'
        # header['os'] = {
        #    'name': os_name,
        #    'version': cs_plateforom.release()
        # }

        return header.__str__()

    def set_entry_model(self):
        pass

    def set_content_type_model(self):
        pass

    def set_query_model(self):
        pass

    def set_asset_model(self):
        pass

    def request_api(self, urls: str):
        try:
            r = requests.get(urls, timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        pass