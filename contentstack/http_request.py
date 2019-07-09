import platform
import urllib.parse
from urllib import parse

import requests
from requests import Response

from contentstack import config


class HTTPRequestConnection(object):

    def __init__(self, url_path, query=dict, local_headers=dict):
        self.result = None
        self.error = None
        self.url_path = url_path
        self._query_prams = query
        self._local_headers = local_headers
        self._local_headers['X-User-Agent'] = self._contentstack_user_agent()
        self._local_headers['Content-Type'] = 'application/json'
        self.url_path = config.Config().endpoint(self.url_path)
        if 'environment' in self._local_headers:
            self._query_prams['environment'] = self._local_headers['environment']

    def http_request(self) -> tuple:
        print("prams", self._query_prams.__str__())
        payload = parse.urlencode(query=self._query_prams, encoding='UTF-8')
        print("encoded prams", payload)
        response: Response = requests.get(self.url_path, params=payload, headers=self._local_headers)
        var_url = response.url
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
        os_name = platform.system()
        if os_name == 'Darwin':
            os_name = 'macOS'
        elif not os_name or os_name == 'Java':
            os_name = None
        elif os_name and os_name not in ['macOS', 'Windows']:
            os_name = 'Linux'
        header['os'] = {
            'name': os_name,
            'version': platform.release()
        }
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