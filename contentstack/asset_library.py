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


class OrderType(object):

    """
    OrderType is used to choose one of the ascending and descending
    It returns either ascending or descending
    """
    ASC, DESC = range(0, 2)

    pass


class AssetLibrary:

    """
    contentstack.asset_library
    ~~~~~~~~~~~~~~~~~~
    This module implements the AssetLibrary class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

    """

    def __init__(self):

        self.__count = 0
        self.__stack_instance = None
        self.__http_request = None
        self.__stack_headers = {}
        self.__query_params = {}

    def instance(self, stack_instance):

        self.__stack_instance = stack_instance
        self.__stack_headers.update(self.__stack_instance.headers)
        self.__http_request = self.__stack_instance.http_request

    def set_header(self, key: str, value):

        if key is not None and value is not None:
            self.__stack_headers[key] = value
            return self

    def headers(self, headers: dict):

        if headers is not None and len(headers) > 0 and isinstance(headers, dict):
            self.__stack_headers = headers
            if 'environment' in self.__stack_headers:
                env_value = self.__stack_headers['environment']
                self.__query_params["environment"] = env_value
        return self

    def remove_header(self, key):

        if key is not None:
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)
        return self

    def include_count(self):
        self.__query_params['include_count'] = 'true'
        return self

    def include_relative_url(self):
        self.__query_params['relative_urls'] = 'true'
        return self

    def get_count(self) -> int:
        """
        get_count returns the total size of content
        :return: count of content
        :rtype: int
        """
        return self.__count

    def sort(self, key: str, order_by: OrderType):

        """
        :param key: provides key on which ASC/DESC need to apply.
        :param order_by: object option either "asc" or "desc"
        :return self , instance of AssetLibrary
        """
        if order_by == 1:
            self.__query_params['asc'] = key
        else:
            self.__query_params['desc'] = key

        return self.__query_params

    def fetch_all(self):
        from contentstack import Config
        asset_url = Config().endpoint('assets')
        return self.__http_request.get_result(asset_url, self.__query_params, self.__stack_headers)



