import logging
import requests
from requests.auth import HTTPDigestAuth
import json
import urllib.parse
from contentstack import config


class HTTPConnection:

    def __init__(self,  query=None):
        self._query = query

    def get_query_request(self):
        return self.__http_request()

    def get_entry_request(self):
        return self.__http_request()

    def get_stack_request(self):
        return self.__http_request()

    def get_content_type_req(self):
        return self.__http_request()

    def get_group_request(self):
        return self.__http_request()

    def __http_request(self):
        encoded_query = urllib.parse.urlencode(self.__query)
        self._local_headers['Content-Type'] ='application/json'.format()
        self._local_headers['X-User-Agent'] = config.Config.SDK_VERSION
        response = requests.post(config.Config.get_host(), encoded_query, self.__local_headers)

        print(response.json)


connection: HTTPConnection = HTTPConnection(local_headers={'dwd','wdq'},query={'dwwd':'dwdwq'})
connection.get_entry_request()
