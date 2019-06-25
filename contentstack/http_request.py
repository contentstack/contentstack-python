import requests
from urllib3.util import timeout
from contentstack import config
import urllib.parse
import logging


class HTTPRequestConnection(object):

    def __init__(self, url_path, query=dict, local_headers=dict):
        self.url_path = url_path
        self._query_prams = query
        self._local_headers = local_headers
        self.url_path = config.Config().get_endpoint(self.url_path)
        if 'environment' in self._local_headers:
            self._query_prams['environment'] = self._local_headers['environment']

    def http_request(self) -> dict:
        self._local_headers['X-User-Agent'] = self._contentstack_user_agent()
        self._local_headers['Content-Type'] = 'application/json'
        response = requests.get(self.url_path, params=self._query_prams, headers=self._local_headers)

        print('request url:: ', response.url)
        if response.ok:
            json_response = response.json()
            if 'stack' in json_response:
                logging.info('stack response')
                return json_response['stack']
            if 'content_types' in json_response:
                logging.info('contenttypes response')
                return json_response['content_types']
            if 'items' in json_response:
                logging.info('sync response')
                return json_response['items']
            if 'content_type' in json_response:
                logging.info('content type response')
                return json_response['content_type']
            if 'entry' in json_response:
                logging.info('entry response')
                return json_response['entry']
            if 'entries' in json_response:
                logging.info('entries response')
                return json_response['entries']

        else:
            error_response = response.json()
            # error_message = error_response["error_message"]
            # error_code = error_response["error_code"]
            # error_code = error_response["errors"]
            return error_response

    @staticmethod
    def _contentstack_user_agent() -> str:
        """
        X-Contentstack-User-Agent header.
        """
        header = {}
        from . import __version__
        header['sdk'] = {
            'name': 'contentstack.python',
            'version': __version__
        }

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