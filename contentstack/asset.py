import os
import sys
sys.path.insert(0, os.path.abspath('.'))

"""
Asset
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""


class OrderType(object):

    """
    OrderType is used to choose one of the ascending or descending
    """
    ASC, DESC = range(0, 2)


class Asset:

    """
    Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded
    in your Contentstack repository for future use.
    These files can be attached and used in multiple entries.
    contentstack.asset
    ==============================
    [Example]:
    This module implements the Asset class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets
    >>> from stack import Stack as stack
    >>> asset = stack.asset()
    ==============================
    """

    def __init__(self, uid=None):
        if uid is not None and isinstance(uid, str):
            self.__asset_uid = uid
        
        self.__config = None
        self.__stack_instance = None
        self.__response = None
        self.__http_request = None
        self.__query_params = {}
        self.__stack_headers = {}
        self.__count = 0
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
        self.__tags = None

    def _instance(self, stack_instance):
        from contentstack.stack import Stack
        from contentstack.errors import StackException

        if stack_instance is None:
            raise StackException('Kindly initialise stack first')
        if isinstance(stack_instance, Stack):
            self.__stack_instance = stack_instance
            self.__config = self.__stack_instance.config
            self.__http_request = self.__stack_instance.get_http_instance
        else:
            raise ValueError('Invalid Stack type, Please provide Stack Instance')

        return self

    def _configure(self, response):
        
        if response is not None and isinstance(response, dict) and len(response) > 0:
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
                self.__asset_uid = self.__response['uid']
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
        asset_uid function returns asset_uid of the asset

        Returns:
        [type] -- str

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> uid = asset.asset_uid

        ==============================

        """

        return self.__asset_uid

    @property
    def count(self):

        """
        Size of asset objects in Asset list.
        
        Returns:
            [type] -- [int]

        ==============================
        
        [Example]:
        >>> asset = Asset()
        >>> count = asset.count

        ==============================
        """

        return self.__count

    @property
    def filetype(self):

        """
        This function returns type of the asset file

        Returns:
            [type] -- str

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> file = asset.filetype

        ==============================
        """

        return self.__file_type

    @property
    def filesize(self):

        """
        Returns size of asset file
        
        Returns:
            [type] -- str

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> size = asset.filesize

        ==============================
        """

        return self.__file_size

    @property
    def filename(self):

        """
        This function returns the name of the asset file.
        
        Returns:
            [type] -- [str]

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> filename = asset.filename

        ==============================
        """

        return self.__file_name

    @property
    def url(self):

        """
        This function returns the url of the Asset
        
        Returns:
            [type] -- [str]

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> file_url = asset.url

        ==============================
        """

        return self.__file_url

    @property
    def json(self):

        """
        This function returns json response of Asset
        
        Returns:
            [{str}] -- [json response of Asset]

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  response = asset.json

        ==============================
        """

        return self.__response

    @property
    def created_at(self):

        """
        This function returns the time when Asset is created.
        
        Returns:
            [str] -- Time when Asset is created

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  response = asset.created_at

        ==============================
        """

        return self.__created_at

    @property
    def created_by(self):

        """
        This function returns the owner of the Asset
        
        Returns:
            [str] -- Owner of the Asset

        [Example]:
        >>> asset = Asset()
        >>>  response = asset.created_by

        """

        return self.__created_by

    @property
    def updated_at(self):

        """
        This method returns the time the Asset was updated.
        
        Returns:
            [str] -- Time the Asset was updated

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  response = asset.updated_at

        ==============================
        """

        return self.__updated_at

    @property
    def updated_by(self):

        """
        This function returns the time of Asset was updated
        
        Returns:
            [str] --  Asset was updated by whome

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  response = asset.updated_by

        ==============================
        """

        return self.__updated_by

    @property
    def tags(self):

        """
        This function returns the list of str
        
        Returns:
            [list] -- list of tags

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  tags = asset.tags

        ==============================
        """

        return self.__tags

    @property
    def get_version(self):

        """
        This returns the version of the asset
        
        Returns:
            [int] -- Version of the asset

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> tags = asset.get_version

        ==============================
        """

        return self.__version

    @property
    def dimension(self):

        """
        This function returns the dimension of the Asset
        
        Returns:
            [dict] -- Dimension of the Asset

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> tags = asset.dimension

        ==============================
        """

        return self.__dimension

    def add_header(self, key, value):

        """
        Adds header params to the header of request
        
        Raises:

            ValueError: Kindly provide valid KEY and Value
            ValueError: key and value should be str type
        
        Returns:
            [Asset] -- Asset, So we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  asset = asset.add_header('key', 'value')

        ==============================
        
        """

        if None in (key, value):
            raise ValueError('Kindly provide valid KEY and Value')
        elif isinstance(key, str) and isinstance(value, str):
            self.__stack_headers[key] = value
        else:
            raise ValueError('KEY and Value should be str type')

        return self

    def environment(self, environment):

        """
        Provide the name of the environment if you wish to retrieve the assets published 
        in a particular environment.

        :param environment: the name of the environment
        :type environment: str
        :return: self
        :rtype: Asset, so we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  asset = asset.environment('production')

        ==============================
        """

        if environment is None:
            raise ValueError('Kindly provide valid environment')
        elif isinstance(environment, str):
            self.__query_params['environment'] = environment
        else:
            raise ValueError('Environment should be str type')

        return self

    def add_params(self, key, value):

        """
        :param key: query params key
        :param value: query params value
        :return: Asset, So we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  asset = asset.add_params('key', 'value')

        ==============================
        """

        if None in (key, value):
            raise ValueError('Kindly provide valid params')
        elif isinstance(key, str):
            self.__query_params[key] = value
        else:
            raise ValueError('Kindly provide str type KEY')

        return self

    def relative_urls(self):

        """
        include the relative URLs of the assets in the response.
        :return: self
        :rtype: Asset, so we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> asset = asset.relative_urls()

        ==============================
        """

        self.__query_params['relative_urls'] = 'true'

        return self

    def include_dimension(self):

        """
        include the dimensions (height and width) of the image in the response.
        Supported image types: JPG, GIF, PNG, WebP, BMP, TIFF, SVG, and PSD.
        :return: self
        :rtype: Asset

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> asset = asset.include_dimension()

        ==============================
        """

        self.__query_params['include_dimension'] = "true"

        return self

    def remove_header(self, key):

        """
        :param key: remove_header function takes key of header developer wants to remove.
        :type key: header of key
        :return: self
        :rtype: Asset, So we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> asset = asset.remove_header('some_key')

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide valid KEY')
        elif isinstance(key, str) and key in self.__stack_headers:
            self.__stack_headers.pop(key, None)

        return self

    def set_uid(self, asset_uid):

        """
        Enter the unique ID of the asset of which you wish to retrieve the details.
        :param asset_uid:  asset_uid is unique ID of the asset of which you wish to retrieve the details
        :type asset_uid:
        :return: self
        :rtype: Asset, So we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> asset = asset.set_uid('uid')

        ==============================
        """
        if asset_uid is None:
            raise ValueError('Invalid asset_uid')
        elif isinstance(asset_uid, str):
            self.__asset_uid = asset_uid
        else:
            raise Exception('Kindly provide str tyoe of asset_uid')

        return self

    def include_count(self):

        """
        :return: include_count is used to include number of assets, used for fetch_all()
        :rtype: Asset, So we can chain the call

        ==============================

        [Example]:
        >>> asset = Asset()
        >>>  asset = asset.set_uid('uid')
        
        ==============================

        """
        self.__query_params['include_count'] = 'true'

        return self

    def sort(self, key, order_by):

        """
        :param key: provides key on which ASC/DESC need to apply.
        :param order_by: object option either "asc" or "desc"
        :return self , instance of AssetLibrary

        ==============================

        [Example]:
        >>> asset = Asset()
        >>> asset = asset.sort('some_key', OrderType.ASC)
        
        ==============================
        """
        if None in (key, order_by):
            raise ValueError('Kindly provide valid arguments')
        elif isinstance(key, str) and isinstance(order_by, OrderType):
            if order_by is not None:
                if order_by == 0:
                    self.__query_params['asc'] = key
                else:
                    self.__query_params['desc'] = key
            else:
                raise Exception('Kindly provide a valid input')

        return self.__query_params

    def fetch_all(self):

        """
        Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use. These files can be
        attached and used in multiple entries.
        Learn more about Assets [https://www.contentstack.com/docs/guide/content-management#working-with-assets].

        :return: This call fetches the list of all the assets of a particular stack.
        It also returns the content of each asset in the form of list[Assets].
        :rtype: list[Asset]

        """

        endpoint = self.__config.endpoint
        url = '{}/assets'.format(endpoint)
        return self.__http_request.get_result(url, self.__query_params, self.__stack_headers)

    def fetch(self):

        """
        This call fetches the latest version of a specific asset of a particular stack.
        :return: It returns Asset on the basis of asset_uid
        :rtype: Asset

        """
        if self.__asset_uid is not None and len(self.__asset_uid) > 0:
            endpoint = self.__config.endpoint
            url = '{}/assets/{}'.format(endpoint, self.__asset_uid)
        else:
            raise Exception("Kindly Provide Asset UID")
        return self.__http_request.get_result(url, self.__query_params, self.__stack_headers)
