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

from contentstack import http_request

"""
contentstack.asset_library
~~~~~~~~~~~~~~~~~~
This module implements the AssetLibrary class.
API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

"""



class AssetLibrary():

    def __init__(self):
        self.count = 0
        self.__local_header: dict = {}
        self.__post_params: dict = {}

    def set_header(self, key: str, value):
        if key is not None and value is not None:
            self.__local_header[key] = value
            return self

    def set_headers(self, **headers):
        if headers is not None:
            self.__local_header = headers
            for key, value in self.__local_header.items():
                self.__local_header[key] = value
        return self

    def remove_header(self, key):
        if key is not None:
            if key in self.__local_header:
                self.__local_header.pop(key)
        return self

    def include_count(self):
        self.__post_params['include_count'] = 'true'
        return self

    def include_relative_url(self):
        self.__post_params['relative_urls'] = 'true'
        return self

    def get_count(self) -> int:
        return self.count

    # [PENDING], Need to add
    # order_by = Enum('ORDER_BY', 'ASCENDING DESCENDING')
    #   def sort(self, key: str, order_by):
    #  if ORDER_.ASCENDING:
    #      self.__post_params['asc'] = key
    #   if ORDER_BY.DESCENDING:
    #       self.__post_params['desc'] = key
    #   return self.__post_params

    def fetch(self) -> tuple:
        print('__params  ::', self.__post_params)
        print('__headers ::', self.__local_header)
        asset_request = http_request.HTTPRequestConnection('assets', self.__post_params, self.__local_header)
        (response, error) = asset_request.http_request()
        if error is None:
            print(response)
            self.__set_response(response['assets'])
            return response, error
        else:
            return response, error

    def __set_response(self, param):

        pass
