#  HttpConnection
#  contentstack
#
#  Created by Shailesh Mishra on 22/06/19.
#  Copyright © 2019 Contentstack. All rights reserved.

import logging
import requests
from urllib import parse
from contentstack import Error
from json import JSONDecodeError
from requests.exceptions import Timeout, HTTPError


class HTTPConnection(object):

    def __init__(self, url: str, query: dict, headers: dict):
        if None not in (url, query, headers):
            self.url = url
            self.query = query
            self.headers = headers
        else:
            raise ValueError('Kindly provide valid Arguments')

    def get_result(self, url: str, query: dict, headers: dict):

        """
        get Results is helpful to make HTTP request
        :param url: Request url
        :param query: query parameters
        :param headers: headers parameters
        :return: response

        """

        if None not in (url, query, headers):
            if len(url) > 0 and len(headers) > 0:
                self.url = url
                self.query = query
                self.headers = headers
            else:
                raise ValueError('Kindly provide a valid input')

        # Headers from locale
        self.headers.update(self.__user_agents())
        payload = parse.urlencode(query=self.query, encoding='UTF-8')
        try:
            response = requests.get(self.url, verify=True, timeout=(2, 5), params=payload, headers=self.headers)
            if response.status_code == 200:
                # Check if json dictionary is valid decode and parse the dictionary
                if response.raise_for_status() is None:
                    return self.__parse_dict(response)
            else:
                # It helps to set Error object to return with Error Message and Error Code
                err = response.json()
                if err is not None:
                    return Error().config(err)
        except Timeout:
            # If a request times out, a Timeout exception will be raised.
            raise TimeoutError('The request timed out')
        except ConnectionError:
            # If there is a network problem like a DNS failure, or refused connection the Requests library will raise
            # a ConnectionError exception.
            raise ConnectionError('Connection error occurred')
        except JSONDecodeError:
            # Invalid json format response received
            raise JSONDecodeError('Invalid JSON in request')
        except HTTPError:
            # With invalid HTTP responses, Requests will also raise an HTTPError exception, but these are rare.
            raise HTTPError('Http Error Occurred')

    def __parse_dict(self, response):
        # This is the private method to parse the response to their respective type
        from contentstack.stack import SyncResult
        # Decode byte response to json
        result = response.json()
        logging.info('url={}\nresponse={}'.format(response.url, result))

        # If result contains stack, return json response
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
            sync_result = SyncResult().configure(result)
            return sync_result

        return None

    @staticmethod
    def __parse_entries(result):
        from contentstack import Entry
        entries: list[Entry] = []
        entry = Entry()

        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return entry.configure(result)
            if isinstance(result, list):
                for entry_obj in result:
                    each_entry = Entry().configure(entry_obj)
                    entries.append(each_entry)
                return entries

    @staticmethod
    def __parse_assets(result):
        from contentstack import Asset
        assets: list[Asset] = []
        asset = Asset()

        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return asset.configure(result)
            if isinstance(result, list):
                for asset_obj in result:
                    itr_asset = asset.configure(asset_obj)
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

        local_headers = {'X-User-Agent': str(header), "Content-Type": 'application/json'}
        return local_headers

    import json

    @staticmethod
    def is_valid_json(json_string):
        import json
        try:
            json_object = json.loads(json_string)
        except ValueError as e:
            return False
        return True
