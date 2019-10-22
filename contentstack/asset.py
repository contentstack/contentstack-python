"""

Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

contentstack.asset
~~~~~~~~~~~~~~~~~~

API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets

"""


class Asset:

    """Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded
    in your Contentstack repository for future use.
    These files can be attached and used in multiple entries.
    contentstack.asset
    ==============================

    This module implements the Asset class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#assets
        
    [Example]:

        >>> import stack
        >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
        >>> asset = stack.asset()

    ==============================

    """

    def __init__(self, uid=None):
        if uid is not None and isinstance(uid, str):
            self.__uid = uid
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
        # _instance is the protected member of the asset, So outsiders can not access this file.
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
        # _configure is the protected member of the asset, So outsiders can not access this file.
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
    def uid(self):

        """uid property helps to set uid of the asset
        
        Returns:
            str -- uid of the asset

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> uid = asset.uid

        ==============================
        """
        return self.__uid

    @property
    def count(self):

        """count property helps to get the Size of asset objects.
        
        Returns:
            int -- count of asset object

        ==============================
        
        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset()
            >>> count = asset.count

        ==============================

        """

        return self.__count

    @property
    def filetype(self):

        """This function returns type of the asset file

        Returns:
            str -- type of file

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> file = asset.filetype

        ==============================

        """
        return self.__file_type

    @property
    def filesize(self):

        """Returns size of asset file
        
        Returns:
            int -- size of asset file

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> size = asset.filesize

        ==============================

        """

        return self.__file_size

    @property
    def filename(self):

        """This property returns the filename asset file.
        
        Returns:
            str -- filename of asset

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> filename = asset.filename

        ==============================

        """

        return self.__file_name

    @property
    def url(self):

        """This property returns the url of the Asset
        
        Returns:
            str -- asset url

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> file_url = asset.url

        ==============================

        """

        return self.__file_url

    @property
    def json(self):

        """
        This property returns response in json
        
        Returns:
            str -- Json response of Asset

        ==============================

        [Example]:


            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> response = asset.json

        ==============================
        """

        return self.__response

    @property
    def created_at(self):

        """
        This property returns the time when Asset is created.
        
        Returns:
            str -- Time when Asset is created

        ==============================

        [Example]:


            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> response = asset.created_at

        ==============================
        """

        return self.__created_at

    @property
    def created_by(self):

        """This property created_by returns the owner of the Asset
        
        Returns:
            str -- Owner of the Asset

        ===============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> response = asset.created_by
        
        ================================

        """

        return self.__created_by

    @property
    def updated_at(self):

        """This property updated_at returns the time the Asset was updated.
        
        Returns:
            str -- Time the Asset was updated

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> response = asset.updated_at

        ==============================

        """

        return self.__updated_at

    @property
    def updated_by(self):

        """
        This function returns the time of Asset was updated
        
        Returns:
            str --  Asset was updated by whome

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> response = asset.updated_by

        ==============================

        """

        return self.__updated_by

    @property
    def tags(self):

        """This property returns the list of tag str
        
        Returns:
            list -- list of tags

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> tags = asset.tags

        ==============================

        """

        return self.__tags

    @property
    def version(self):

        """This property returns the version of asset
        
        Returns:
            int -- version of the asset

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> tags = asset.get_version

        ==============================

        """

        return self.__version

    @property
    def dimension(self):

        """This property returns the dimension of the Asset
        
        Returns:
            dict -- Dimension of the Asset

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> tags = asset.dimension

        ==============================

        """

        return self.__dimension

    def add_header(self, key, value):

        """
        add_header is the funtion helps to pass additional header to the asset class
        
        Arguments:
            key {str} -- key of the header
            value {str} -- value of the header
        
        Raises:
            ValueError: Kindly provide valid KEY and Value
            ValueError: key and value should be str type
        
        Returns:
            Asset -- Asset, So we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.add_header('key', 'value')

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
        
        Arguments:
            environment {str} -- the name of the environment

        Returns:
            Asset -- Asset, So we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.environment('production')

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
        add_param is helpful to pass addtional parameters to the asset class

        Arguments:
            key {str} -- key of the query parameter
            value {str} -- value of the query parameter
        
        Raises:
            KeyError: if key is None or type of key is not str
            ValueError: if value is None
        
        Returns:
            Asset -- [Returns Asset object So we can chain the call]

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.add_params('key', 'value')

        ==============================
        """

        if None in (key, value):
            raise KeyError('Kindly provide valid params')
        elif isinstance(key, str):
            self.__query_params[key] = value
        else:
            raise ValueError('Kindly provide str type KEY')

        return self

    def relative_urls(self):

        """
        Include the relative URLs of the assets in the response.
        
        Returns:
            Asset -- Asset, so we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.relative_urls()

        ==============================

        """

        self.__query_params['relative_urls'] = 'true'

        return self

    def include_dimension(self):

        """
        Include the dimensions (height and width) of the image in the response.
        Supported image types: JPG, GIF, PNG, WebP, BMP, TIFF, SVG, and PSD.

        Returns:
            Asset -- Asset, so we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.include_dimension()

        ==============================
        
        """

        self.__query_params['include_dimension'] = "true"

        return self

    def remove_header(self, key):

        """
        remove_header function helps to delete the existing key from the header.
        
        Arguments:
            key {str} -- existing key of the header parameter
        
        Raises:
            ValueError: If key is None
        
        Returns:
            Asset -- Asset, So we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
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
        
        Arguments:
            asset_uid {str} -- asset_uid is unique ID of the asset of which you wish to retrieve the details
        
        Raises:
            KeyError: If asset_uid is None
            KeyError: If type of asset_uid is str
        
        Returns:
            Asset -- Asset, so we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.set_uid('uid')

        ==============================

        """

        if asset_uid is None:
            raise KeyError('Invalid asset_uid')
        elif isinstance(asset_uid, str):
            self.__uid = asset_uid
        else:
            raise KeyError('Kindly provide str type of asset_uid')

        return self

    def include_count(self):

        """
        include_count is used to return total asset count

        Returns:
            Asset -- Asset, so we can chain the call

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
            >>> asset = asset.set_uid('uid')
        
        ==============================

        """
        self.__query_params['include_count'] = 'true'

        return self

    def sort(self, key, order_by):

        """
        Request asset by sort by key, It caould be sorted to ASCENDING and DESCENDING order
        param key: provides the key on which ASC/DESC need to apply.
        :param key: key that to be constrained
        :param order_by: object option either "asc" or "desc"
        :return self , instance of AssetLibrary
        
        Arguments:
            key {str} -- field uid
            order_by {OrderType} -- type of oerder ASC or DES
        
        Raises:
            ValueError: If key and OrderType is None

        Returns:
            Asset -- Asset instance, So call will be chainable.

        ==============================

        [Example]:

            >>> import stack
            >>> stack = stack.Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> asset = stack.asset('uid')
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

        return self

    def fetch_all(self):

        """Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use. These files can be
        attached and used in multiple entries.
        Learn more about Assets 
        [https://www.contentstack.com/docs/guide/content-management#working-with-assets].

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
        if self.__uid is not None and len(self.__uid) > 0:
            endpoint = self.__config.endpoint
            url = '{}/assets/{}'.format(endpoint, self.__uid)
        else:
            raise Exception("Kindly Provide Asset UID")
        return self.__http_request.get_result(url, self.__query_params, self.__stack_headers)


class OrderType(object):
    """OrderType is used to choose one of the ascending or descending"""

    ASC, DESC = range(0, 2)
