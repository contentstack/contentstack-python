import requests
from contentstack import config
import urllib.parse


class HTTPRequest(object):

    def __init__(self, url_path, query=dict, local_headers=dict):
        self.url_path = url_path
        self._query_prams = query
        self._local_headers = local_headers
        if 'environment' in self._local_headers:
            self._query_prams['environment'] = self._local_headers['environment']

        # self._query_prams = urllib.parse.quote_plus(self._query_prams)
        self._local_headers['X-User-Agent'] = self._contentstack_user_agent()
        self._local_headers['Content-Type'] = 'application/json'
        # http request based on url_path and respected query
        self.url_path = config.Config().get_endpoint(self.url_path)
        self._http_request()

    def _http_request(self):
        response = requests.get(
            self.url_path,
            params=self._query_prams,
            headers=self._local_headers,
        )

        json_response = response.json()
        stack = json_response['stack']
        collaborators = stack['collaborators']
        print(collaborators, collaborators)

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

# connection = HTTPRequest(url_path='sync', query=None)
# connection._http_request()
