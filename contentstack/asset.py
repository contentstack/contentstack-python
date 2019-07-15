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


"""
contentstack.asset
~~~~~~~~~~~~~~~~~~
This module implements the Asset class.
API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

"""


class Asset:
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
    """

    def __init__(self, asset_uid: str = None):

        self.__asset_uid = asset_uid
        self.__response = None
        self.__local_params = {}
        self.__local_headers = {}

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

    def set_stack_instance(self, stack):
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
            self.__version = self.__response['_version']
            if 'dimension' in self.__response:
                self.__dimension = self.__response['dimension']

        return self

    @property
    def asset_uid(self):

        """
        uid = asset.asset_uid
        :return: str of asset_uid
        """
        return self.__uid

    @property
    def filetype(self):

        """
        file = asset.filetype
        :return: str of filetype
        """
        return self.__file_type

    @property
    def filesize(self):

        """
        size = asset.file_size
        :return: file_size
        """
        return self.__file_size

    @property
    def filename(self):

        """
        filename = asset.filename
        :return: filename
        """
        return self.__file_name

    @property
    def url(self):

        """
        file_url = asset.file_url
        :return: file_url
        """
        return self.__file_url

    @property
    def to_json(self):

        """
        response = asset.to_json
        :return: dict response
        """
        return self.__response

    @property
    def create_at(self):

        """
        created_at = asset.created_at
        :return: str created_at
        """
        return self.__created_at

    @property
    def create_by(self):

        """
        created_by = asset.created_by
        :return: str created_by
        """
        return self.__created_by

    @property
    def update_at(self):

        """
        updated_at = asset.updated_at
        :return: str updated_at
        """
        return self.__updated_at

    @property
    def update_by(self):

        """
        updated_by = asset.updated_by
        :return: str updated_by
        """
        return self.__updated_by

    @property
    def tags(self):

        """
        tags = asset.tags
        :return: list tags
        """
        return self.__tags

    @property
    def get_version(self):

        """
        tags = asset.tags
        :return: list tags
        """
        return self.__version

    @property
    def dimension(self) -> tuple:

        """
        tags = asset.tags
        :return: list tags
        """
        global width, height
        if self.__dimension is not None and isinstance(self.__dimension, dict):
            dim: dict = self.__dimension
            height, width = dim.values()
        return height, width

    def set_header(self, headers: dict):
        if headers is not None and isinstance(headers, dict):
            self.__local_headers = headers
            for key, value in self.__local_headers.items():
                if key == 'environment':
                    self.__local_params["environment"] = value
                self.__local_headers[key] = value
        return self

    def add_params(self, params: dict):
        if params is not None:
            self.__local_params = params
            for key, value in self.__local_params.items():
                self.__local_params[key] = value
        return self

    def relative_urls(self):
        self.__local_params['relative_urls'] = "true"
        return self

    def version(self, version):
        if version is not None:
            self.__local_params['version'] = version
        return self

    def include_dimension(self):
        self.__local_params['include_dimension'] = "true"
        return self

    def remove_header(self, key):
        if key is not None:
            if key in self.__local_headers:
                self.__local_headers.pop(key)
        return self

    def set_uid(self, asset_uid: str):
        if asset_uid is not None:
            self.__asset_uid = asset_uid

    def fetch_all(self) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack import Config
        from contentstack import Error

        error = None
        asset_url = Config().endpoint('assets')
        self.__local_headers.update(self.header_agents())
        payload = parse.urlencode(query=self.__local_params, encoding='UTF-8')

        try:
            response: Response = requests.get(asset_url, params=payload, headers=self.__local_headers)
            list_asset: list[Asset] = []

            if response.ok:

                response: dict = response.json()['assets']
                print(response)
                for asset in response:
                    asset_resp: Asset = self.configure(asset)
                    list_asset.append(asset_resp)
            else:

                error_dict = response.json()
                Error().error(error_dict)

            return list_asset, error

        except requests.exceptions.RequestException as e:
            raise ConnectionError(e.response)
            pass

    def fetch(self) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack import Config
        error = None

        asset_url = '{}/{}'.format(Config().endpoint('assets'), self.__asset_uid)

        if self.__asset_uid is None or len(self.__asset_uid) == 0:
            raise KeyError('Please provide asset uid to process to fetch response')

        self.__local_headers.update(self.header_agents())
        payload = parse.urlencode(query=self.__local_params, encoding='UTF-8')

        try:
            response: Response = requests.get(asset_url, params=payload, headers=self.__local_headers)

            if response.ok:
                response: dict = response.json()['asset']
                self.configure(response)

            else:

                error = response.json()

            return response, error

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
