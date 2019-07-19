"""
 * MIT License
 *
 * Copyright (c) 2012 - 2019 Contentstack
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 """


class AssetLibrary:

    """
    contentstack.asset_library
    ~~~~~~~~~~~~~~~~~~
    This module implements the AssetLibrary class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

    """

    def __init__(self):
        self.count = 0
        self.__local_headers = {}
        self.__query_params = {}

    def set_header(self, key: str, value):
        if key is not None and value is not None:
            self.__local_headers[key] = value
            return self

    def headers(self, headers: dict):
        if headers is not None and len(headers) > 0 and isinstance(headers, dict):
            self.__local_headers = headers
            if 'environment' in self.__local_headers:
                env_value = self.__local_headers['environment']
                self.__query_params["environment"] = env_value
        return self

    def remove_header(self, key):
        if key is not None:
            if key in self.__local_headers:
                self.__local_headers.pop(key)
        return self

    def include_count(self):
        self.__query_params['include_count'] = 'true'
        return self

    def include_relative_url(self):
        self.__query_params['relative_urls'] = 'true'
        return self

    def get_count(self) -> int:
        return self.count

    # Color = enumerate(RED="ASCENDING", GREEN='DESCENDING')
    # [PENDING], Need to add
    # order_by = Enum('ORDER_BY', 'ASCENDING DESCENDING')
    #   def sort(self, key: str, order_by):
    #  if ORDER_.ASCENDING:
    #      self.__post_params['asc'] = key
    #   if ORDER_BY.DESCENDING:
    #       self.__post_params['desc'] = key
    #   return self.__post_params

    def fetch_all(self) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack import Config
        from contentstack import Error
        from contentstack import Asset

        error = None
        asset_url = Config().endpoint('assets')
        self.__local_headers.update(self.header_agents())
        payload = parse.urlencode(query=self.__query_params, encoding='UTF-8')

        try:
            response: Response = requests.get(asset_url, params=payload, headers=self.__local_headers)
            list_asset: list[Asset] = []

            if response.ok:

                response: dict = response.json()['assets']

                for asset in response:
                    asset_instance = Asset()
                    asset_resp: Asset = asset_instance.configure(response=asset)
                    list_asset.append(asset_resp)
            else:

                error_dict = response.json()
                Error().error(error_dict)

            return list_asset, error

        except requests.exceptions.RequestException as e:
            raise ConnectionError(e.response)
            pass

    @classmethod
    def header_agents(cls) -> dict:

        import contentstack
        import platform

        """
        Contentstack-User-Agent header.
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
