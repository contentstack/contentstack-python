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
from contentstack.stack import Stack


class Asset(Stack):

    def __init__(self, asset_uid: str = None):
        """ :type asset_uid: str """

        self.__asset_url_path: str = "assets"
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

        self.__stack = Stack
        self.__local_params = {}
        self.__local_headers = {}
        if asset_uid is not None and len(asset_uid) > 0:
            self.__asset_uid = asset_uid
            asset_url = "assets/{0}"
            self.__asset_url_path = asset_url.format(self.__asset_uid)

    def set_stack_instance(self, stack):
        self.__stack = stack
        self.__local_headers = stack.local_headers
        self.__local_headers = stack.get_headers()

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

    def add_params(self, **params):
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

    def set_uid(self, asset_uid: str):
        if asset_uid is not None:
            self.__asset_uid = asset_uid

    def get_asset_uid(self):
        return self.__asset_uid

    def get_file_type(self):
        return self.__file_type

    def get_file_size(self):
        return self.__file_size

    def get_file_name(self):
        return self.__file_name

    def get_url(self):
        return self.__file_url

    def to_json(self):
        return self.__response

    def get_create_at(self):
        return self.__created_at

    def get_create_by(self):
        return self.__created_by

    def get_update_at(self):
        return self.__updated_at

    def get_update_by(self):
        return self.__updated_by

    def get_tags(self):
        return self.__tags

    def fetch(self) -> tuple:
        print('__asset_url ::', self.__asset_url_path)
        print('__params    ::', self.__local_params)
        print('__headers   ::', self.__local_headers)
        asset_request = http_request.HTTPRequestConnection(self.__asset_url_path, self.__local_params,
                                                           self.__local_headers)
        (response, error) = asset_request.http_request()
        if error is None:
            print(response)
            self.__configure(response['asset'])
            return response, error
        else:
            return response, error

# asset: Asset = Asset('blt78356332423')
# head = {'api_key': 'blt347894985', 'access_token': '734328976236', 'environment': 'dev'}
# params = {'param1': 'Yes iam in', 'param2 ': 'Yes in', 'param3': 'Oh Yes in'}
# asset.set_header(**head)
# asset.add_params(**params)
# result, err = asset.fetch()
# if err is None:
#    print(result)
# else:
#    print(err['error_message'])
