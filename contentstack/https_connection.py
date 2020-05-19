import logging
from json import JSONDecodeError
from urllib.parse import urlencode
import requests
from requests.exceptions import Timeout, HTTPError
from contentstack import Error
import contentstack
import logging
import platform


def get_os_platform():
    """ returns client platform """
    os = platform.system()
    if os == 'Darwin':
        os = 'macOS'
    elif not os or os == 'Java':
        os = None
    elif os and os not in ['macOS', 'Windows']:
        os = 'Linux'
    os_platform = {'name': os, 'version': platform.release()}
    return os_platform


def user_agents():
    """User Agents for the Https"""
    header = {'sdk': dict(name=contentstack.__package__, version=contentstack.__version__), 'os': get_os_platform,
              'Content-Type': 'application/json'}
    package = "contentstack-python, - {}".format(contentstack.__version__)
    return {'User-Agent': str(header), "X-User-Agent": package}


# R0903: Too few public methods (1/2) (too-few-public-methods)
# "pylint doesn't know what's best" - use your own judgement but as a rule.
class HTTPConnection(object):

    def __init__(self, url, query, stack_headers):
        if None not in (url, query, stack_headers):
            self.__payload = None
            self.__base_url = url
            self.__query_params = query
            self.__headers = stack_headers
            self.__headers.update(user_agents())

            if 'environment' in self.__headers:
                environment = self.__headers['environment']
                self.__query_params['environment'] = environment

    def get_result(self, url, query, headers):
        if None not in (url, query, headers):
            if len(url) > 0 and len(self.__headers) > 0:
                self.__base_url = url
                if len(headers) > 0:
                    self.__headers.update(headers)
                self.__query_params.update(query)
                # Case: If UIR Parameter contains entries
                if 'entries' in self.__base_url:
                    self.__payload = self.__execute_entry()
                else:
                    url_param = ''
                    for (key, value) in self.__query_params.items():
                        url_param = '{}&{}={}'.format(url_param, key, value)
                    self.__payload = url_param
        try:
            if self.__payload.startswith("&"):
                self.__payload = self.__payload[1:]

            _url = '{}?{}'.format(self.__base_url, self.__payload)
            logging.info('{}?{}'.format(self.__base_url, self.__payload))
            response = requests.get(_url, verify=True, timeout=(10, 8), headers=self.__headers)

            if response.status_code == 200:
                if response.raise_for_status() is None:
                    return self.__parse_dict(response)
            else:
                err = response.json()
                if err is not None:
                    error = Error()
                    error._config(err)
                    return error

            logging.info('\n\nrequest url => {}\nresponse={}'.format(response.url, response))

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
        if 'stack' in result:
            return result['stack']
        if 'entry' in result:
            dict_entry = result['entry']
            return self.__parse_entries(dict_entry)
        if 'entries' in result:
            entry_list = result['entries']
            return self.__parse_entries(entry_list)
        if 'asset' in result:
            dict_asset = result['asset']
            return self.__parse_assets(dict_asset, 1)
        if 'assets' in result:
            asset_list = result['assets']
            asset_count = 0
            if 'count' in result:
                asset_count = result['count']
            return self.__parse_assets(asset_list, asset_count)
        if 'content_type' in result:
            return result['content_type']
        if 'content_types' in result:
            return result['content_types']
        if 'items' in result:
            sync_result = SyncResult()
            sync_result._configure(result)
            return sync_result

        return None

    @staticmethod
    def __parse_entries(result):
        from contentstack import Entry
        entries = []
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
    def __parse_assets(result, asset_count):
        from contentstack import Asset
        assets = []
        asset = Asset()

        if result is not None and len(result) > 0:
            if isinstance(result, dict):
                return asset._configure(result)
            if isinstance(result, list):
                for asset_obj in result:
                    itr_asset = asset._configure(asset_obj)
                    assets.append(itr_asset)
                asset._count(asset_count)
                return assets

    def __execute_entry(self):
        url_param = ''
        for (key, value) in self.__query_params.items():
            if key == 'include[]':
                if isinstance(value, list):
                    url_param = '{}&{}'.format(url_param, urlencode({key: value}, doseq=True))
            elif key == 'only[BASE][]':
                if isinstance(value, list):
                    url_param = '{}&{}'.format(url_param, urlencode({key: value}, doseq=True))
            elif key == 'except[BASE][]':
                if isinstance(value, list):
                    url_param = '{}&{}'.format(url_param, urlencode({key: value}, doseq=True))
            elif key == 'only':
                for uid in value:
                    inner_list = value[uid]
                    inner_key = 'only[{}][]'.format(uid)
                    if isinstance(inner_list, list):
                        url_param = '{}&{}'.format(url_param, urlencode({inner_key: inner_list}, doseq=True))
            elif key == 'except':
                for uid in value:
                    inner_list = value[uid]
                    inner_key = 'except[{}][]'.format(uid)
                    if isinstance(inner_list, list):
                        url_param = '{}&{}'.format(url_param, urlencode({inner_key: inner_list}, doseq=True))
            elif key == 'query':
                url_param = '{}&{}={}'.format(url_param, key, value.__str__().replace("\'", "\""))
                print(url_param)
            else:
                url_param = '{}&{}={}'.format(url_param, key, value)

        return url_param
