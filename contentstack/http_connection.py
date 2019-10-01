"""
HttpConnection
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

"""

import logging
import requests
from urllib import parse
from contentstack import Error
from json import JSONDecodeError
from requests.exceptions import Timeout, HTTPError


class HTTPConnection(object):

    def __init__(self, url: str, query: dict, stack_headers: dict):

        """
        Initialises the HTTPConnection to make Http Request
        :param url: url for the request to made
        :param query: It will be executed to retrieve entries. This query should be in key value format.
        :param stack_headers: It contains like API key of your stack, access token and others.
        """
        if None not in (url, query, stack_headers):
            self.__url = url
            self.__query_params = query
            self.__stack_headers = stack_headers
            self.__stack_headers.update(self.__user_agents())

    def get_result(self, url: str, query: dict, headers: dict):
        if None not in (url, query, headers):
            if len(url) > 0 and len(self.__stack_headers) > 0:
                self.__url = url
                self.__query_params = query
                self.__stack_headers.update(headers)
            else:
                raise ValueError('Kindly provide a valid input')

        # Headers from locale
        if 'environment' in self.__stack_headers:
            environment = self.__stack_headers['environment']
            self.__query_params['environment'] = environment
        logging.info('Query Parameters ={}'.format(self.__query_params))
        logging.info('Headers ={}'.format(self.__stack_headers))
        payload = parse.urlencode(query=self.__query_params, encoding='UTF-8')
        try:
            response = requests.get(self.__url, verify=True, timeout=(10, 8), params=payload,
                                    headers=self.__stack_headers)
            if response.status_code == 200:
                if response.raise_for_status() is None:
                    return self.__parse_dict(response)
            else:
                err = response.json()
                if err is not None:
                    return Error()._config(err)
        except Timeout:
            raise TimeoutError('The request timed out')
        except ConnectionError:
            raise ConnectionError('Connection error occurred')
        except JSONDecodeError:
            raise JSONDecodeError('Invalid JSON in request')
        except HTTPError:
            raise HTTPError('Http Error Occurred')

    def __parse_dict(self, response):
        from contentstack.stack import SyncResult
        result = response.json()
        logging.info('\n\nrequest url => {}\nresponse={}'.format(response.url, result))

        if 'stack' in result:
            return result['stack']
        # If result contains entry, return Entry
        if 'entry' in result:
            dict_entry = result['entry']
            return self.__parse_entries(dict_entry)
        # If result contains entries, return list[Entry]
        if 'entries' in result:
            entry_list = result['entries']
            return self.__parse_entries(entry_list)
        # If result contains asset, return Asset
        if 'asset' in result:
            dict_asset = result['asset']
            return self.__parse_assets(dict_asset)
        # If result contains assets, return list[Asset]
        if 'assets' in result:
            asset_list = result['assets']
            return self.__parse_assets(asset_list)
        # If result contains content_type,return content_type json
        if 'content_type' in result:
            return result['content_type']
        # If result contains content_types,return content_types json
        if 'content_types' in result:
            return result['content_types']
        # If result contains items, return SyncResult json
        if 'items' in result:
            sync_result = SyncResult()._configure(result)
            return sync_result

        return None

    @staticmethod
    def __parse_entries(result):
        from contentstack import Entry
        entries: list[Entry] = []
        entry = Entry()
        # if 'count' in result:
        # entry.count = result['count']
        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return entry._configure(result)
            if isinstance(result, list):
                for entry_obj in result:
                    each_entry = Entry()._configure(entry_obj)
                    entries.append(each_entry)
                return entries

    @staticmethod
    def __parse_assets(result):
        from contentstack import Asset
        assets: list[Asset] = []
        asset = Asset()

        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return asset._configure(result)
            if isinstance(result, list):
                for asset_obj in result:
                    itr_asset = asset._configure(asset_obj)
                    assets.append(itr_asset)

                return assets

    @staticmethod
    def __user_agents() -> dict:
        import contentstack
        import platform

        """
        Contentstack-User-Agent.
        """
        header = {'sdk': dict(name=contentstack.__package__, version=contentstack.__version__)}
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

        local_headers = {'User-Agent': str(header),
                         "Content-Type": 'application/json',
                         "X-User-Agent": "contentstack-python, {}".format(contentstack.__version__)
                         }
        return local_headers

    def __is_valid_json(response):

        import json
        try:
            json.loads(response)
            return True
        except ValueError as e:
            return False
