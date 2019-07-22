"""
MIT License
Copyright (c) 2012 - 2019 Contentstack
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 
"""
import logging
from contentstack import errors as err, HTTPConnection
from contentstack import Config

log = logging.getLogger(__name__)


class Stack:

    """
    contentstack.stack
    ~~~~~~~~~~~~~~~~~~
    A stack is a space that stores the content of a project (a web or mobile property).
    Within a stack, you can create content structures, content entries, users, etc.
    related to the project. Read more about Stacks

    API Reference: [https://www.contentstack.com/docs/guide/stack]
    """

    def __init__(self, **kwargs):

        """
        A stack is a space that stores the content of a project (a web or mobile property).
        Within a stack, you can create content structures, content entries, users, etc.
        related to the project. Read more about Stacks

        API Reference: [https://www.contentstack.com/docs/guide/stack]
        """

        # declare stack class variables
        self.__query_params = dict()
        self.__stack_headers = dict()
        # set class variables to initialise image transformation.
        self.__image_transform_url = None
        self.__image_params = dict
        # set sync variables
        self.__sync_query = dict()
        # it accepts api_key as str, access_token as str, and environment as str
        for key, value in kwargs.items():
            self.__stack_headers[key] = value
            log.debug("%s == %s" % (key, value))
        self.__initialise_stack()

        url = Config().endpoint('stacks')
        self.http_request = HTTPConnection(url, self.__query_params, self.__stack_headers)

    def __initialise_stack(self):

        if len(self.__stack_headers) > 0:
            if 'api_key' not in self.__stack_headers:
                raise err.StackException('Kindly provide api_key')
            if 'access_token' not in self.__stack_headers:
                raise err.StackException('Kindly provide access token')
            if 'environment' not in self.__stack_headers:
                raise err.StackException('Kindly provide environment')
        else:
            raise err.StackException('Kindly provide valid Arguments')

    def content_type(self, content_type_id: str):

        """

        Content type defines the structure or schema of a page or a section of your web or mobile property.
        To create content for your application, you are required to first create a content type.
        and then create entries using the content type. Read more about Content Types.

        API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#content-types

        :param content_type_id: The id of the Content Type.
        :return ContentType

        [Example]
        >>> content_type:ContentType = stack.content_type('product')
        """
        from contentstack import ContentType
        if content_type_id is not None and len(content_type_id) > 0 and isinstance(content_type_id, str):
            content_type = ContentType(self.http_request, content_type_id)
            content_type.headers = self.__stack_headers
        else:
            raise KeyError('Kindly provide a valid content_type')

        return content_type

    def get_content_types(self):

        """
        Fetches all Content Types from the Stack. This call returns comprehensive information
        of all the content types available in a particular stack in your account.
        API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#content-types

        :return: ContentTypes response

        [Usage]:
        >>>> content_types = stack.get_content_types()
        """
        ct_query: dict = {'include_count': 'true'}
        from contentstack import Config
        ct_url = Config().endpoint('content_types')
        result = self.http_request.get_result(ct_url, ct_query, self.__stack_headers)
        return result

    def asset(self, uid: str = None):

        """
        Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use. These files can be
        attached and used in multiple entries. Learn more about Assets.
        API Reference : https://www.contentstack.com/docs/guide/content-management#working-with-assets
        :param uid: asset uid
        :return: asset


        [All Assets]
        This call fetches the list of all the assets of a particular stack.
        It also returns the content of each asset in JSON format. You can also specify the environment of
        which you wish to get the assets.You can apply queries to
        filter assets/entries. Refer to the Queries [https://www.contentstack.com/docs/apis/content-delivery-api/#queries] section for more details.

        [Single Asset]
        This call fetches the latest version of a specific asset of a particular stack.

        [Usage]:
        >>>> asset = stack.asset('uid')

        """

        from contentstack import Asset
        assets = Asset(asset_uid=uid)
        assets.headers(self.__stack_headers)
        if uid is not None:
            assets.set_uid(asset_uid=uid)
        return assets

    def asset_library(self):

        """
        [AssetLibrary]
        This call fetches the list of all the assets on query
        :return: asset_library

        [Usage]:
        >>>> asset_lib: AssetLibrary = stack.asset_library()

        """
        from contentstack import AssetLibrary
        asset_library = AssetLibrary()
        asset_library.headers(self.__stack_headers)
        return asset_library

    @property
    def application_key(self):

        """
        :return: application_key as str

        [Usage]:
        >>>> api_key: str = stack.application_key

        """

        if 'api_key' in self.__stack_headers:
            app_key = self.__stack_headers['api_key']
            return app_key
        else:
            return None

    @property
    def access_token(self):

        """
        :return:str access token of the stack

        [Usage]:
        >>>> access_token: str = stack.access_token

        """
        if 'access_token' in self.__stack_headers:
            access_token = self.__stack_headers['access_token']
            return access_token
        else:
            return None

    def image_transform(self, image_url: str, **kwargs):

        """
        The Image Delivery API is used to retrieve, manipulate and/or convert image
        files of your Contentstack account and deliver it to your web or mobile properties.

        It is an second parameter in which we want to place different manipulation
        key and value in array form
        ImageTransform function is define for image manipulation with different
        transform_params in second parameter in array form

        :param image_url:str endpoint
        :param kwargs: query arguments
        :return: url:str

        [Usage]:
        >>>> image_url: str = stack.image_transform('endpoint', query_key='query_value', query_key1='query_value', query_key2='query_value')

        """
        self.__image_transform_url = image_url
        self.__image_params = kwargs
        args = ['{0}={1}'.format(k, v) for k, v in kwargs.items()]
        if args:
            self.__image_transform_url += '?{0}'.format('&'.join(args))
        return self.__image_transform_url

    def collaborators(self):

        """
        collaborators with whom the stacks are shared.
        A detailed information about each collaborator is returned.
        :returns list of stack collaborators in response

        [Usage]:
        >>>> stack = stack.collaborators()

        """

        self.__query_params['include_collaborators'] = 'true'
        return self

    def include_stack_variables(self):

        """
        Stack variables are extra information about the stack,
        such as the description, format of date,
        format of time, and so on. Users can include or exclude stack variables in the response.
        :returns stack_variables
        [Usage]:
        >>>> stack = stack.include_stack_variables()
        """

        self.__query_params['include_stack_variables'] = 'true'

        return self

    def include_discrete_variables(self):

        """
        :returns discrete variables of the stack
        [Usage]:
        >>>> stack = stack.include_discrete_variables()

        """
        self.__query_params['include_discrete_variables'] = 'true'

        return self

    def include_count(self):

        """
        :returns Total Count of stack response
        [Usage]:
        >>>> stack = stack.include_count()
        """
        self.__query_params['include_count'] = "true"

        return self

    def pagination(self, pagination_token: str):

        """
        If the result of the initial sync (or subsequent sync) contains more than 100 records,
        the response would be paginated. It provides pagination token in the response. However,
        you do not have to use the pagination token manually to get the next batch,
        the SDK does that automatically until the sync is complete.
        Pagination token can be used in case you want to fetch only selected batches.
        It is especially useful if the sync process is interrupted midway (due to network issues, etc.).
        In such cases, this token can be used to restart the sync process from where it was interrupted.

        :param pagination_token:
        :return: list[SyncResult]
        """

        self.__sync_query = {'pagination_token': pagination_token}

        return self.__sync_request()

    def sync_token(self, sync_token):

        """
        You can use the sync token (that you receive after initial sync)
        to get the updated content next time.
        The sync token fetches only the content that was added after your last sync,
        and the details of the content that was deleted or updated.

        :param sync_token:
        :return: SyncStack
        """

        self.__sync_query = {'sync_token': sync_token}

        return self.__sync_request()

    def sync(self, **kwargs):

        """
        [content_type_uid] --> You can also initialize sync with entries of
        only specific content_type. To do this, use syncContentType and specify
        the content type uid as its value. However, if you do this,
        the subsequent syncs will only include the entries of the specified content_type.

        [from_date] --> You can also initialize sync with entries published
        after a specific date. To do this, use from_date
        and specify the start date as its value.

        [locale] --> You can also initialize sync with entries of only specific locales.
        To do this, use syncLocale and specify the locale code as its value.
        However, if you do this, the subsequent syncs will only include
        the entries of the specified locales.

        [publish_type] --> Use the type parameter to get a specific type of content.
        You can pass one of the following values:

        asset_published, entry_published, asset_unpublished,
        asset_deleted, entry_unpublished, entry_deleted,
        content_type_deleted.

        If you do not specify any value, it will bring all published entries and published assets.

        """

        self.__sync_query["init"] = 'true'
        for key, value in kwargs.items():
            self.__sync_query[key] = value

        if self.__stack_headers is not None and len(self.__stack_headers) > 0:
            if 'environment' in self.__stack_headers:
                env = self.__stack_headers['environment']
                self.__sync_query['environment'] = env
        else:
            raise KeyError("Kindly provide stack headers")

        return self.__sync_request()

    @property
    def environment(self) -> str:
        if 'environment' in self.__stack_headers:
            return self.__stack_headers['environment']
        else:
            return 'environment not found'

    @environment.setter
    def environment(self, env: str):

        """
        :param env:str environment

        Example:
        stack = stack.environment = 'product'

        """
        if env is not None and isinstance(env, str):
            self.__stack_headers['environment'] = env
        else:
            raise KeyError('Kindly provide valid Argument')

    @property
    def headers(self):

        """
        :return:dict headers

        [Uses]
        >>>> headers:dict = stack.headers

        """
        return self.__stack_headers

    def __sync_request(self) -> tuple:
        sync_url = Config().endpoint('sync')
        result = self.http_request.get_result(sync_url, self.__sync_query, self.__stack_headers)
        return result

    def fetch(self) -> tuple:
        from contentstack import Config
        stack_url = Config().endpoint('stacks')
        result = self.http_request.get_result(stack_url, self.__query_params, self.__stack_headers)
        return result


class SyncResult:

    def __init__(self):
        self.__resp: dict = {}
        self.__items: list = []
        self.__skip = int
        self.__limit = int
        self.__total_count = int
        self.__sync_token = str
        self.__pagination_token = str

    def configure(self, result: dict):

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
        return self.__resp

    @property
    def items(self):
        return self.__items

    @property
    def skip(self):
        return self.__skip

    @property
    def limit(self):
        return self.__limit

    @property
    def count(self):
        return self.__total_count

    @property
    def sync_token(self):
        return self.__sync_token

    @property
    def pagination_token(self):
        return self.__pagination_token
