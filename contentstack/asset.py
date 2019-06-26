# Asset.py
# Contentstack
# Created by Shailesh on 22/06/19.
# Copyright (c) 2012 - 2019 Contentstack. All rights reserved.

# [MIT License] :: Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from contentstack import http_request


class Asset:

    def __init__(self, asset_uid: str = None):
        """ :type asset_uid: str """

        self.__asset_url: str = "assets"
        self.__response = dict
        self.__file_name = str
        self.__file_size = str
        self.__file_type = str
        self.__file_url = str
        self.__uid = str
        self.__tags = list
        self.__created_at = str
        self.__created_by = str
        self.__updated_at = str
        self.__updated_by = str

        self.__local_params = {}
        self.__local_headers = {}
        if asset_uid is not None and len(asset_uid) > 0:
            self.__asset_uid = asset_uid
            asset_url = "assets/{0}"
            self.__asset_url = asset_url.format(self.__asset_uid)

    def __configure(self, response: dict):
        self.__response = response
        self.__file_name = self.__response['filename']
        self.__file_size = self.__response['file_size']
        self.__file_type = self.__response['content_type']
        self.__file_url = self.__response['url']
        self.__uid = self.__response['uid']
        self.__tags = self.__response['tags']
        self.__created_at = self.__response['created_at']
        self.__created_by = self.__response['created_by']
        self.__updated_at = self.__response['updated_at']
        self.__updated_by = self.__response['updated_by']
        return self

    def set_header(self, **headers):
        if headers is not None:
            self.__local_headers = headers
            for key, value in self.__local_headers.items():
                self.__local_headers[key] = value
        return self

    def add_param(self, **params):
        if params is not None:
            self.__local_params = params
            for key, value in self.__local_params.items():
                self.__local_params[key] = value
        return self

    def remove_header(self, key):
        if key is not None:
            if key in self.__local_headers:
                self.__local_headers.pop(key)
        return self

    def fetch(self) -> tuple:
        print('__asset_url ::', self.__asset_url)
        print('__params    ::', self.__local_params)
        print('__headers   ::', self.__local_headers)
        asset_request = http_request.HTTPRequestConnection(self.__asset_url, self.__local_params, self.__local_headers)
        (response, error) = asset_request.http_request()
        if error is None:
            print(response)
            self.__configure(response['asset'])
            return response, error
        else:
            return response, error


asset = Asset('blt782397846923')
kwargs = {"kwarg_1": "Val bol", "kwarg_2": "Harper mod", "kwarg_3": " ways from extremist"}
result: Asset = asset.add_param(**kwargs)
result.fetch()
