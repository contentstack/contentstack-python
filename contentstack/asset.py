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
import contentstack
from contentstack import http_request
from contentstack.stack import Stack

"""
contentstack.asset
~~~~~~~~~~~~~~~~~~
This module implements the Asset class.
API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

"""


class Asset(Stack):

    """
    Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded
    in your Contentstack repository for future use. These files can be attached and used in multiple entries.
    Learn more about Assets [https://www.contentstack.com/docs/guide/content-management#working-with-assets].

    [All Assets]

    This call fetches the list of all the assets of a particular stack.
    It also returns the content of each asset in JSON format.
    You can also specify the environment of which you wish to get the assets.
    You can apply queries to filter assets/entries. Refer to the Queries section for more details.

    [Single Asset]
    This call fetches the latest version of a specific asset of a particular stack.
    Uses:
    >>> stack = contentstack.Stack('api_key', 'access_token', 'environment')
    >>> asset = stack.asset('asset_uid')
    >>> result, error = asset.fetch()
    """

    def __init__(self, asset_uid: str = None):
        self.__response = None
        self.__asset_url_path: str = "assets"
        self.__stack = Stack
        self.__local_params = {}
        self.__local_headers = Stack.get_headers()

        self.__file_name = None
        self.__file_size = None
        self.__file_type = None
        self.__file_url = None
        self.__uid = None
        self.__tags = None
        self.__created_at = None
        self.__created_by = None
        self.__updated_at = None
        self.__updated_by = None

        if asset_uid is not None and len(asset_uid) > 0:
            self.__asset_uid = asset_uid
            asset_url = "assets/{0}"
            self.__asset_url_path = asset_url.format(self.__asset_uid)

    def set_stack_instance(self, stack):
        self.__stack = stack
        self.__local_headers = stack.local_headers
        self.__local_headers = stack.get_headers()

    def configure(self, response: dict):
        self.__response = response
        if self.__response is not None:
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

        def get_asset_uid(self):
            return self.__uid

        def get_file_type(self):
            return self.__file_type

        def get_file_size(self):
            return self.__file_size

        def get_filename(self):
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

    def relative_urls(self):
        self.__local_params["relative_urls"] = "true"
        return self

    def get_version(self, version):
        if version is not None:
            self.__local_params["environment"] = ''
            self.__local_params["version"] = version
        return self

    def include_dimension(self):
        self.__local_params["include_dimension"] = "true"
        return self

    def remove_header(self, key):
        if key is not None:
            if key in self.__local_headers:
                self.__local_headers.pop(key)
        return self

    def set_uid(self, asset_uid: str):
        if asset_uid is not None:
            self.__asset_uid = asset_uid

    def fetch(self) -> tuple:
        print('__asset_url ::', self.__asset_url_path)
        print('__params    ::', self.__local_params)
        print('__headers   ::', self.__local_headers)

        asset_request = http_request.HTTPRequestConnection(self.__asset_url_path, self.__local_params, self.__local_headers)
        (response, error) = asset_request.http_request()
        if error is None:
            response = response['asset']
            #response = AssetModel(response)
            return response, error
        else:
            return response, error
