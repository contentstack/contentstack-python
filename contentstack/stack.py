"""
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
contentstack.stack
~~~~~~~~~~~~~~~~~~
API Reference:
https://www.contentstack.com/docs/developers/apis/content-delivery-api/#stack
"""

from contentstack import HTTPConnection
from contentstack import Config
from contentstack.errors import StackException
from contentstack import Asset
from contentstack import ContentType


class Stack:
    """A stack can be defined as a pool of data or a container
    that holds all the content/assets related to a site.
    It is a collaboration space where multiple users can work
    together to create, edit, approve, and publish content.
    This is the first page that will appear once you log in.
    Since Contentstack is capable of handling multiple stacks,
    you will see a list of stacks that you have access to. As a Developer,
    you can invite users to a stack.
    The invited users can then log in to the platform and start
    working with you on a stack with the rights and access
    you have assigned to them.
    ~~~~~~~~~~~~~~~~~~
    API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#stack
    Arguments:
        object {[api_key, delivery_token, environment]} -- [stack credentials]
    Raises:
        KeyError: [When invalid key is provided]
        StackException: [When invalid data is provided]
    Returns:
        [Stack] -- [Instance of stack object]
    """
    def __init__(self, **kwargs):
        """Argument kwargs is key-worded, variable-length argument list.
        To initialise stack following fields should be provided.
        api_key -> stack 'api_key' of your target stack, type of api_key should be str.
        access_token -> stack 'access_token' of your target stack,
                        type of access_token should be str.
        environment -> stack 'environment' of your target stack, type of environment should be str
        config: config = '<contentstack.config.Config>' (optional)
                      stack configuration to setup custom API.
        ==============================
        [Example]:
            >>> import contentstack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )

        To declare stack with custom configuration
            >>> config = Config()
            >>> config.host('cdn.contentstack.io')
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
        ==============================
        """
        # https://stackoverflow.com/questions/24434510/how-to-deal-with-pylints-too-many-instance-attributes-message?answertab=active#tab-top
        # pylint: disable=too-many-instance-attributes
        # Eight is reasonable in this case.
        self.config = None
        self.__http_request = None
        self.__query_params = dict()
        self.__stack_headers = dict()
        self.__headers = dict()
        self.__image_params = dict
        self.__sync_query = dict()
        for key, value in kwargs.items():
            self.__headers[key] = value
        self.__initialise_stack()

    @property
    def api_key(self):
        """Returns api_KEY of the stack
        Returns:
            str -- api_key of the stack
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> api_key = stack.api_key
        ==============================
        """
        if 'api_key' in self.__stack_headers:
            app_key = self.__stack_headers['api_key']
            return app_key
        return None

    @property
    def get_http_instance(self):
        """This method returns http_instance of the stack.
        Returns:
            str -- instance of the HttpRequest
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> http_instance = stack.get_http_instance
        ==============================
        """
        return self.__http_request

    @property
    def access_token(self):
        """access_token property returns access_token of the stack
        Returns:
            str -- access_token of the stack
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> access_token = stack.access_token
        ==============================
        """
        if 'access_token' in self.__stack_headers:
            access_token = self.__stack_headers['access_token']
            return access_token
        return None

    @property
    def environment(self):
        """environment property returns environment of the stack
        Returns:
            str -- environment of the stack
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> environment = stack.environment
        ==============================
        """
        if 'environment' in self.__stack_headers:
            return self.__stack_headers['environment']
        return None

    @environment.setter
    def environment(self, environment):
        """environment property helps to set environment of the stack
        Arguments:
            environment {str} -- environment of the stack
        Raises:
            KeyError: If environment is None, empty or not str type
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack.environment = 'product'
        ==============================
        """
        if environment is None:
            raise KeyError
        if isinstance(environment, str):
            self.__stack_headers['environment'] = environment
        else:
            raise KeyError('Argument environment should be str type')

    @property
    def headers(self):
        """dictionary of the stack headers
        Returns:
            dict -- dictionary of the headers
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> headers = stack.headers
        ==============================
        """
        return self.__stack_headers

    def __initialise_stack(self):
        self.config = Config()
        if len(self.__headers) > 0:
            if 'api_key' not in self.__headers:
                raise StackException('Kindly provide API_Key')
            if 'access_token' not in self.__headers:
                raise StackException('Kindly provide access token')
            if 'environment' not in self.__headers:
                raise StackException('Kindly provide environment')
            if 'config' in self.__headers:
                self.config = self.__headers['config']
                self.__headers.pop('config', None)

            self.__stack_headers['api_key'] = self.__headers['api_key']
            self.__stack_headers['access_token'] = self.__headers['access_token']
            self.__stack_headers['environment'] = self.__headers['environment']
            self.__http_request = HTTPConnection(
                self.config.endpoint,
                self.__query_params,
                self.__stack_headers
                )
    def content_type(self, content_type_id):
        """[Content type lets you define the structure or blueprint
        of a page or a section of your web or mobile property.]
        Read more about contenttypes
        API Reference:
        https://www.contentstack.com/docs/developers/create-content-types/about-content-types
        Arguments:
            content_type_id {[str]} -- [content_type_id of entry]
        Returns:
            [contentstack.content_type.ContentType] -- [Instance of the ContentType]
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> content_type = stack.content_type('product')
        ==============================
        """
        if content_type_id is not None \
                and isinstance(content_type_id, str) \
                and len(content_type_id) > 0:
            content_type = ContentType(content_type_id)
            content_type.instance(self)
            return content_type

        raise KeyError('Invalid key provided')

    def get_content_types(self, query_params):

        """
        Fetches all Content Types from the Stack. This call returns comprehensive information
        of all the content types available in a particular stack in your account.
        API Reference:
        https://www.contentstack.com/docs/developers/apis/content-delivery-api/#content-types
        Arguments:
            query_params {dict} -- query parameters for the content_types
        Raises:
            StackException: If stack instance is not found
        Returns:
            dict -- returns list of <contentstack.content_type.ContentType>
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> content_types = stack.get_content_types()
        ==============================
        """
        content_type_params = {}
        if self.config is None:
            raise StackException('Kindly initialise stack')
        endpoint = self.config.endpoint
        url = '{}/content_types'.format(endpoint)
        if query_params is not None and isinstance(query_params, dict):
            content_type_params = query_params.copy()
        result = self.__http_request.get_result(url, content_type_params, self.__stack_headers)
        return result

    def asset(self, uid=None):
        """Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use. These files can be
        attached and used in multiple entries. Learn more about Assets.
        Keep uid None to fetch list of all assets
        API Reference : https://www.contentstack.com/docs/content-managers/work-with-assets
        Keyword Arguments:
            uid {str} -- uid of the asset (default: {None})
        Returns:
            <contentstack.asset.Asset> -- class object of asset so we can chain the asset functions.
        ==============================
        [Example]: [Asset]
        This call fetches the latest version of a specific asset of a particular stack.
        provide asset_uid of the asset you have to find.
        Example: in case to fetch single asset, provide uid of the asset:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> asset_instance = stack.asset('bltputyourassetuid')
            >>> asset = asset_instance.fetch()
        ###############################
        [Example]: [All Assets]
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> asset_instance = stack.asset()
            >>> assets = asset_instance.fetch_all()
        ==============================
        """
        asset = Asset(uid=uid)
        asset.instance(self)
        return asset

    def image_transform(self, image_url, **kwargs):
        """The Image Delivery API is used to retrieve, manipulate and/or convert image
        files of your Contentstack account and deliver it to your web or mobile properties.
        It is an second parameter in which we want to place different manipulation key and
        value in array form ImageTransform method is define for image manipulation with
        different transform_params in second parameter in array form
        Arguments:
            image_url {str} -- On which we want to manipulate
            **kwargs {object} -- parameter in which we want to
            place different manipulation key-worded, variable-length
            argument list
            It is a query form that we want to place different manipulation key and value
        Returns:
            str -- Image transformation url
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack.image_transform('image_url', width=100, height=100)
        ==============================
        """
        image_transform_url = image_url
        self.__image_params = kwargs
        args = ['{0}={1}'.format(k, v) for k, v in kwargs.items()]
        if args:
            image_transform_url += '?{0}'.format('&'.join(args))
        return image_transform_url

    def collaborators(self):
        """A detailed information about collaborators with whome the stacks are shared.
        Returns:
            Stack -- Stack object so we can chain other functions.
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack = stack.collaborators()
            >>> result = stack.fetch()
        ==============================
        """
        self.__query_params['include_collaborators'] = 'true'
        return self

    def include_stack_variables(self):
        """Stack variables are extra information about the stack, such as the description,
        format of date, format of time, and so on. Users can include or exclude stack variables
        in the response
        Returns:
            Stack -- Stack object so we can chain other functions.
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack = stack.include_stack_variables()
            >>> result = stack.fetch()
        ==============================
        """
        self.__query_params['include_stack_variables'] = 'true'

        return self

    def include_discrete_variables(self):

        """Discrete variables of the stack

        Returns:
            Stack -- Stack object so we can chain other functions.

        ==============================

        [Example]:

            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack = stack.include_discrete_variables()
            >>> result = stack.fetch()

        ==============================
        """

        self.__query_params['include_discrete_variables'] = 'true'

        return self

    def include_count(self):
        """Includes count of stack response
        Returns:
            Stack -- Stack object so we can chain other functions.
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack = stack.include_count()
            >>> result = stack.fetch()
        ==============================
        """
        self.__query_params['include_count'] = 'true'
        return self

    def fetch(self):
        """[Fetches the stack reponse as per the functions applied]
        Returns:
            dict -- result is the reponse of the stack
        ==============================

        [Example]:

            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> stack = stack.include_count()
            >>> result = stack.fetch()

        ==============================

        """
        url = '{}/stacks'.format(self.config.endpoint)
        result = self.__http_request.get_result(url, self.__query_params, self.__stack_headers)
        return result

    def sync(self, **kwargs):
        """
        content_type_uid --> You can also initialize sync with entries of
        only specific content_type. To do this, use syncContentType and specify
        the content type uid as its value. However, if you do this,
        the subsequent syncs will only include the entries of the specified content_type.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        from_date --> You can also initialize sync with entries published
        after a specific date. To do this, use from_date
        and specify the start date as its value.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        locale --> You can also initialize sync with entries of only specific locales.
        To do this, use syncLocale and specify the locale code as its value.
        However, if you do this, the subsequent syncs will only include
        the entries of the specified locales.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        publish_type --> Use the type parameter to get a specific type of content.
        You can pass one of the following values:
        asset_published, entry_published, asset_unpublished,
        asset_deleted, entry_unpublished, entry_deleted,
        content_type_deleted.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        If you do not specify any value, it will bring all published entries and published assets.
        Raises:
            KeyError: If headers of the stack is None or empty
        Returns:
            list[SyncResult] -- returns list of SyncResult
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> result = stack.sync
            >>> (
            >>>    content_type_uid='content_type_uid',
            >>>    from_date='date',
            >>>    locale='en-us',
            >>>    publish_type='asset_published'
            >>> )
        ==============================

        """

        self.__sync_query["init"] = 'true'
        if kwargs is not None and len(kwargs) > 0:
            for key, value in kwargs.items():
                self.__sync_query[key] = value
        if self.__stack_headers is not None and len(self.__stack_headers) > 0:
            if 'environment' in self.__stack_headers:
                env = self.__stack_headers['environment']
                self.__sync_query['environment'] = env
        else:
            raise KeyError("Kindly provide stack headers")

        return self.__sync_request()

    def pagination(self, pagination_token):
        """ If the result of the initial sync (or subsequent sync) contains more than 100 records,
        the response would be paginated. It provides pagination token in the response.
        However, you do not have to use the pagination token manually to get the next batch,
        the SDK does that automatically until the sync is complete. Pagination token
        can be used in case you want to fetch only selected batches.
        It is especially useful if the sync process is interrupted
        midway (due to network issues, etc.)
        In such cases, this token can be used to restart
        the sync process from where it was interrupted.
        Arguments:
            pagination_token {str} -- pagination_token
        Raises:
            KeyError:  If pagination_token is None, empty or not str type
        Returns:
            list[SyncResult] -- list of SyncResult
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> result = stack.pagination('blt8347235938759')

        ==============================

        """

        if isinstance(pagination_token, str):
            self.__sync_query = {'pagination_token': pagination_token}
        else:
            raise KeyError('Kindly provide valid pagination_token')
        return self.__sync_request()

    def sync_token(self, sync_token):

        """
        You can use the sync token (that you receive after initial sync)
        to get the updated content next time.
        The sync token fetches only the content that was added after your last sync,
        and the details of the content that was deleted or updated.

        Arguments:
            sync_token {str} -- sync_token
        Raises:
            StackException: If sync_token is not str
        Returns:
            list[SyncResult] -- list of SyncResult object
        ==============================
        [Example]:
            >>> from contentstack import Stack
            >>> stack = Stack
            >>> (
            >>>  api_key='stack_api_key',
            >>>  access_token='stack_access_token',
            >>>  environment='env'
            >>>  )
            >>> result = stack.sync_token('bltsomekeytoput')
        ==============================
        """

        if isinstance(sync_token, str):
            self.__sync_query = {'sync_token': sync_token}
        else:
            raise StackException('Kindly provide valid sync_token')
        return self.__sync_request()

    def __sync_request(self):

        # This is useful to find sync_request for the stack
        url = '{}/stacks/sync'.format(self.config.endpoint)
        result = self.__http_request.get_result(url, self.__sync_query, self.__stack_headers)
        return result


class SyncResult:
    "SyncResult is model class that retuns Sync Response"
    def __init__(self):
        self.__resp = {}
        self.__items = []
        self.__skip = None
        self.__limit = None
        self.__total_count = None
        self.__sync_token = None
        self.__pagination_token = None

    def _configure(self, result):
        if result is not None and len(result) > 0:
            self.__resp = result
            if 'items' in self.__resp:
                self.__items = self.__resp['items']
            if 'skip' in self.__resp:
                self.__skip = self.__resp['skip']
            if 'limit' in self.__resp:
                self.__limit = self.__resp['limit']
            if 'total_count' in self.__resp:
                self.__total_count = self.__resp['total_count']
            if 'sync_token' in self.__resp:
                self.__sync_token = self.__resp['sync_token']
            if 'pagination_token' in self.__resp:
                self.__pagination_token = self.__resp['pagination_token']
        return self

    @property
    def json(self):
        """
        :return: Json response
        """
        return self.__resp

    @property
    def items(self):
        """
        :return: Total items
        """
        return self.__items

    @property
    def skip(self):
        """
        :return: skipped items
        """
        return self.__skip

    @property
    def limit(self):
        """[Returns limit from SyncResult]
        Returns:
            [int] -- [limit of sync_result]
        """
        return self.__limit

    @property
    def count(self):
        """[This property returns count]
        ==============================
        Example:
            >>> count = SyncResult.count
        ==============================
        Returns:
            [int] -- [count of total sync_result]
        """
        return self.__total_count

    @property
    def sync_token(self):
        """[This property returns sync_token]
        ==============================
        Example:
            >>> sync_token = SyncResult.sync_token
        ==============================
        Returns:
            [str] -- [sync token]
        """
        return self.__sync_token

    @property
    def pagination_token(self):
        """[This property returns pagination_token]
        Returns:
            [str] -- [pagination token for the sync_result]
        ==============================
        Example:
            >>> pagination_token = SyncResult.pagination_token
        ==============================
        """
        return self.__pagination_token
