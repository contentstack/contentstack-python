

#  Asset
#  contentstack
#
#  Created by Shailesh Mishra on 22/06/19.
#  Copyright © 2019 Contentstack. All rights reserved.


class OrderType(object):

    """
    OrderType is used to choose one of the ascending or descending

    """
    ASC, DESC = range(0, 2)

    pass


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

    def __init__(self, uid=None):

        """
        :param uid: accepts asset_uid (optional) -> it is URI parameter required for fetch() Asset
        :type : str

        """
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
        self.__uid = None
        self.__tags = None

    def instance(self, stack_instance):

        """
        :param stack_instance: contains stack information like config, headers and http_instance
        :type stack_instance: contentstack.stack.Stack
        :return: self
        :rtype: Asset
        """

        from contentstack.stack import Stack
        from contentstack.errors import StackException
        if stack_instance is None:
            raise StackException('Kindly initialise stack first')
        self.__stack_instance: Stack = stack_instance
        self.__config = self.__stack_instance.config
        self.__stack_headers.update(self.__stack_instance.headers)
        self.__http_request = self.__stack_instance.get_http_instance

        return self

    def configure(self, response):

        """
        :param response: response is Asset result
        :type response: dict
        :return: self
        :rtype: Asset

        """
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
    def asset_uid(self):

        """
        :return: asset_uid function returns asset_uid of the asset
        :rtype: str

        [Example]
        uid = asset.asset_uid
        """

        return self.__uid

    @property
    def count(self):

        """
        :return: count function returns list of assets.
        :rtype: int

        [Example]
        count = asset.count
        """

        return self.__uid

    @property
    def filetype(self):

        """
        :return: This function returns type of the asset file
        :rtype: str

        [Example]
        file = asset.filetype

        """

        return self.__file_type

    @property
    def filesize(self):

        """
        :return: returns size of asset file
        :rtype: str

        [Example]
        size = asset.file_size

        """
        return self.__file_size

    @property
    def filename(self):

        """
        :return: this function returns the name of the asset file.
        :rtype: str

        [Example]
        filename = asset.filename

        """

        return self.__file_name

    @property
    def url(self):

        """
        :return: this function returns the url of the Asset
        :rtype: str

        [Example]
        file_url = asset.file_url

        """
        return self.__file_url

    @property
    def to_json(self):

        """
        :return: this function returns json response of Asset
        :rtype: dict

        [Example]
        response = asset.to_json

        """
        return self.__response

    @property
    def create_at(self):

        """
        :return: this function returns the time when Asset is created.
        :rtype:  str

        [Example]
        created_at = asset.created_at

        """
        return self.__created_at

    @property
    def created_by(self):

        """
        :return: this function returns the owner of the Asset
        :rtype: str

        [Example]
        created_by = asset.created_by

        """
        return self.__created_by

    @property
    def update_at(self):

        """
        :return: this method returns the time the Asset was updated.
        :rtype: str

        [Example]
        updated_at = asset.updated_at
        :return: str updated_at

        """
        return self.__updated_at

    @property
    def updated_by(self):

        """
        :return: this function returns the time of Asset was updated
        :rtype: str

        [Example]
        updated_by = asset.updated_by

        """
        return self.__updated_by

    @property
    def tags(self):

        """
        :return: this function returns the list of str
        :rtype: list

        [Example]
        tags = asset.tags

        """
        return self.__tags

    @property
    def get_version(self):

        """
        :return: this returns the version of the asset
        :rtype: int

        [Example]
        version = asset.get_version

        """
        return self.__version

    @property
    def dimension(self):

        """
        :return: this function returns the dimension of the Asset
        :rtype: dict

        [Example]

        dimension = asset.dimension

        """
        return self.__dimension

    def headers(self, headers):

        """
        :param headers: headers is the stack headers for the stack authentication
        :type headers: dict
        :return: self
        :rtype: Asset

        [Example]

        asset_dict = {'api_key':'bltsomething', 'access_token':'someacceesstoken', 'environment':'development'}
        asset = asset.headers(asset_dict)

        """
        if headers is not None and isinstance(headers, dict) and len(headers) > 0:
            self.__stack_headers = headers.copy()
            if 'environment' in self.__stack_headers:
                env = self.__stack_headers['environment']
                self.__query_params['environment'] = env
                self.__stack_headers.pop('environment', None)
            else:
                raise ValueError("Environment Can't Be None")
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def environment(self, environment):

        """
        provide the name of the environment if you wish to retrieve the assets published in a particular environment.
        Example: production

        :param environment: the name of the environment
        :type environment: str
        :return: self
        :rtype: Asset

        """

        if environment is not None and isinstance(environment, str):
            self.__query_params['environment'] = environment

        return self

    def params(self, params):

        """
        :param params: param function allows to add/update asset query param dictionary.
        :type params: dict
        :return: instance of asset self
        :rtype: Asset

        [Example]

        asset_param = {'key1':'paramOne', 'key2':'paramTwo', 'key3':'paramThree'}
        asset = asset.params(asset_param)

        """
        if params is not None and isinstance(params, dict) and len(params) > 0:
            self.__query_params.update(params)

        return self

    def relative_urls(self):

        """
        include the relative URLs of the assets in the response.
        :return: instance of asset self
        :rtype: Asset

        [Example]
        asset = asset.relative_urls()

        """
        self.__query_params['relative_urls'] = 'true'

        return self

    def version(self, version):

        """
        Note: If no version is mentioned, this request will retrieve the latest published version of the asset.
        To retrieve a specific version, make use of the version parameter and keep the environment parameter blank.

        Specify the version number of the asset that you wish to retrieve.
        If the version is not specified, the details of the latest version will be retrieved.
        To retrieve a specific version, keep the environment parameter blank.
        Example: 1

        :param version: retrieves asset of a specific version
        :type version: int
        :return: instance of asset self
        :rtype: Asset

        [Example]

        asset = asset.version(1)

        """
        if version is not None:
            self.__query_params['version'] = version

        return self

    def include_dimension(self):

        """
        include the dimensions (height and width) of the image in the response.
        Supported image types: JPG, GIF, PNG, WebP, BMP, TIFF, SVG, and PSD.

        :return: instance of asset
        :rtype: Asset

        [Example]
        asset = asset.include_dimension()

        """
        self.__query_params['include_dimension'] = "true"
        return self

    def remove_header(self, key):

        """
        :param key: remove_header function takes key of header developer wants to remove.
        :type key:
        :return: instance of asset
        :rtype: Asset

        [Example]
        asset = asset.remove_header('header_key')

        """
        if key is not None and key in self.__stack_headers:
            self.__stack_headers.pop(key)
        else:
            raise Exception('Kindly provide valid input')

        return self

    def set_uid(self, asset_uid):

        """
        Enter the unique ID of the asset of which you wish to retrieve the details.
        Example: blt91af1e5af9c3639f

        :param asset_uid:  asset_uid is unique ID of the asset of which you wish to retrieve the details
        :type asset_uid:
        :return: instance of asset
        :rtype: Asset
        """
        if asset_uid is not None and isinstance(asset_uid, str):
            self.__asset_uid = asset_uid
        else:
            raise Exception('Kindly provide valid asset_uid')

        return self

    def include_count(self):

        """
        :return: include_count is used to include number of assets, used for fetch_all()
        :rtype: Asset

        """
        self.__query_params['include_count'] = 'true'

        return self

    def sort(self, key: str, order_by):

        """
        :param key: provides key on which ASC/DESC need to apply.
        :param order_by: object option either "asc" or "desc"
        :return self , instance of AssetLibrary

        [Example]:
        asset = asset.sort(OrderType.ASC)

        """

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
