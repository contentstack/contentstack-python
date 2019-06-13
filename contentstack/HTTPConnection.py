import logging
import requests
from requests.auth import HTTPDigestAuth
import json
import config
import urllib.parse


class HTTPConnection:

    def __init__(self, local_headers, query):
        self.__local_headers = {}
        self.__query = {}
        self.__local_headers = local_headers
        self.__query = query


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
        
        __config = config.Config()
        encoded_query = urllib.parse.urlencode(self.__query)
        self.__local_headers.update({'Content-Type': 'application/json',
                                     'X-User-Agent': __config.SDK_VERSION })
        response = requests.post(
            __config.get_host(), encoded_query, self.__local_headers)
        
        print(response.json)


