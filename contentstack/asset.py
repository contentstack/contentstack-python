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
# FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Asset:

    """
    Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded
    in your Contentstack repository for future use.
    These files can be attached and used in multiple entries.
    contentstack.asset
    ~~~~~~~~~~~~~~~~~~
    This module implements the Asset class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

    """

    def __init__(self, asset_uid: str = None):

        self.__asset_uid = asset_uid
        self.__stack_instance = None
        self.__response = None
        self.__http_request = None
        self.__query_params = {}
        self.__stack_headers = {}

        self.__file_name = None
        self.__file_size = None
        self.__file_type = None
        self.__file_url = None
        self.__created_at = None
        self.__created_by = None
        self.__updated_at = None
        self.__updated_by = None
        self.__version = None
        self.__dimension = None
        self.__uid = None
        self.__tags = None

    def instance(self, stack_instance):
        self.__stack_instance = stack_instance
        self.__stack_headers.update(self.__stack_instance.headers)
        self.__http_request = self.__stack_instance.http_request

    def configure(self, response: dict):
        # response is dictionary that check None and length
        if response is not None and len(response) > 0:
            # if response dictionary is Not None
            self.__response = response
            if 'filename' in self.__response:
                self.__file_name = self.__response['filename']
            if 'file_size' in self.__response:
                self.__file_size = self.__response['file_size']
            if 'content_type' in self.__response:
                self.__file_type = self.__response['content_type']
            if 'url' in self.__response:
                self.__file_url = self.__response['url']
            if 'uid' in self.__response:
                self.__uid = self.__response['uid']
            if 'tags' in self.__response:
                self.__tags = self.__response['tags']
            if 'created_at' in self.__response:
                self.__created_at = self.__response['created_at']
            if 'created_by' in self.__response:
                self.__created_by = self.__response['created_by']
            if 'updated_at' in self.__response:
                self.__updated_at = self.__response['updated_at']
            if 'updated_by' in self.__response:
                self.__updated_by = self.__response['updated_by']
            if '_version' in self.__response:
                self.__version = self.__response['_version']
            if 'dimension' in self.__response:
                self.__dimension = self.__response['dimension']
        return self

    @property
    def asset_uid(self):

        """
        [Example]
        uid = asset.asset_uid
        :return: str of asset_uid
        """
        return self.__uid

    @property
    def filetype(self):

        """
        [Example]
        file = asset.filetype
        :return: str of filetype
        """
        return self.__file_type

    @property
    def filesize(self):

        """
        [Example]
        size = asset.file_size
        :return: file_size
        """
        return self.__file_size

    @property
    def filename(self):

        """
        [Example]
        filename = asset.filename
        :return: filename
        """
        return self.__file_name

    @property
    def url(self):

        """
        [Example]
        file_url = asset.file_url
        :return: file_url
        """
        return self.__file_url

    @property
    def to_json(self):

        """
        [Example]
        response = asset.to_json
        :return: dict response
        """
        return self.__response

    @property
    def create_at(self):

        """
        [Example]
        created_at = asset.created_at
        :return: str created_at
        """
        return self.__created_at

    @property
    def create_by(self):

        """
        [Example]
        created_by = asset.created_by
        :return: str created_by
        """
        return self.__created_by

    @property
    def update_at(self):

        """
        [Example]
        updated_at = asset.updated_at
        :return: str updated_at
        """
        return self.__updated_at

    @property
    def update_by(self):

        """
        [Example]
        updated_by = asset.updated_by
        :return: str updated_by
        """
        return self.__updated_by

    @property
    def tags(self):

        """
        [Example]
        tags = asset.tags
        :return: list tags
        """
        return self.__tags

    @property
    def get_version(self):

        """
        [Example]
        tags = asset.tags
        :return: list tags
        """
        return self.__version

    @property
    def dimension(self) -> tuple:

        """
        [Example]
        dimension = asset.dimension
        :return: tuple (height, width)
        """
        global width, height
        if self.__dimension is not None and isinstance(self.__dimension, dict):
            dim: dict = self.__dimension
            height, width = dim.values()
        return height, width

    def headers(self, http_request, headers: dict):

        """
        [Example]
        headers = asset.headers(dict)
        :return: self, that help to chaining the request.

        """
        if http_request is not None:
            self.__http_request = http_request
        else:
            raise Exception("Error! We Don't Have HTTP Instance")

        if isinstance(headers, dict) and len(headers) > 0:
            self.__stack_headers = headers.copy()
            if 'environment' in self.__stack_headers:
                env = self.__stack_headers['environment']
                self.__query_params["environment"] = env
                self.__stack_headers.pop('environment', None)
            else:
                raise Exception("Environment Can't Be None")

        return self

    def params(self, params: dict):

        """
        add param method allows to add query param dictionary to the asset
        :param params:
        :return: self
        """
        if params is not None and isinstance(params, dict) and len(params) > 0:
            self.__query_params.update(params)
        return self

    def relative_urls(self):
        self.__query_params['relative_urls'] = "true"
        return self

    def version(self, version):
        if version is not None:
            self.__query_params['version'] = version
        return self

    def include_dimension(self):
        self.__query_params['include_dimension'] = "true"
        return self

    def remove_header(self, key):
        if key is not None:
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)
        return self

    def set_uid(self, asset_uid: str):
        if asset_uid is not None:
            self.__asset_uid = asset_uid

    def fetch_all(self):
        from contentstack import Config
        asset_url = Config().endpoint('assets')
        return self.__http_request.get_result(asset_url, self.__query_params, self.__stack_headers)

    def fetch(self):
        from contentstack import Config
        if self.__asset_uid is not None and len(self.__asset_uid) > 0:
            asset_url = '{}/{}'.format(Config().endpoint('assets'), self.__asset_uid)
            return self.__http_request.get_result(asset_url, self.__query_params, self.__stack_headers)
        else:
            raise Exception("Kindly Provide Asset UID")
