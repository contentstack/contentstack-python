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
from contentstack import errors as err, Config
from contentstack import http_request

log = logging.getLogger(__name__)


class Stack(object):
    """
    contentstack.stack
    ~~~~~~~~~~~~~~~~~~
    A stack is a space that stores the content of a project (a web or mobile property).
    Within a stack, you can create content structures, content entries, users, etc.
    related to the project. Read more about Stacks
    API Reference: [https://www.contentstack.com/docs/guide/stack]

    """

    from contentstack import Config

    def __init__(self, api_key: str, access_token: str, environment: str, config: Config = None):

        """
        A stack is a space that stores the content of a project (a web or mobile property).
        Within a stack, you can create content structures, content entries, users, etc.
        related to the project. Read more about Stacks
        API Reference: [https://www.contentstack.com/docs/guide/stack]
        :type config: Config
        :param api_key:
        :param access_token:
        :param environment:
        :param config:

        """

        self.__api_key = api_key
        self.__access_token = access_token
        self.__environment = environment

        if config is not None and isinstance(config, Config):
            self.__configs = config
        else:
            self.__configs = Config()

        self.__initialise_stack()
        # declare stack class variables
        self.__query_params = dict()
        self.__stack_headers = dict()
        self.__setup_stack()
        # set class variables to initialise image transformation.
        self.__image_transform_url = None
        self.__image_params = dict
        # set sync variables
        self.__sync_query = dict()

    def __initialise_stack(self):

        if not self.__api_key:
            raise err.StackException(
                'Please enter the API key of stack of which you wish to retrieve the content types.'
            )
        if not self.__access_token:
            raise err.StackException(
                'Enter the access token of your stack.'
            )
        if not self.__environment:
            raise err.StackException(
                'Environment can not be Empty.'
            )

    @property
    def config(self):
        return self.__configs

    @config.setter
    def config(self, configs_instance):
        from contentstack import Config
        """
        :type configs: object
        :param configs:
        :return:
        """
        if isinstance(configs_instance, Config):
            self.__configs = configs_instance

    def content_type(self, content_type_id: str):

        """
        Fetches a Content Type by content_type_id.
        Content type defines the structure or schema of a page or a section of your web or mobile property.
        To create content for your application, you are required to first create a content type.
        and then create entries using the content type. Read more about Content Types.
        API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#content-types
        :param content_type_id: The id of the Content Type.
        :return: :class:`ContentType <contentstack.content_type.ContentType>` object.
        :return type: contentstack.content_type.ContentType
        """
        from contentstack import ContentType
        if content_type_id is not None and len(content_type_id) > 0 and isinstance(content_type_id, str):
            content_type = ContentType(content_type_id)
            content_type.headers = self.__stack_headers
        else:
            raise KeyError('Please provide a valid content_type')

        return content_type

    def get_content_types(self):

        """
        Fetches all Content Types from the Stack. This call returns comprehensive information
        of all the content types available in a particular stack in your account.
        API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#content-types

        :return: List of ContentType objects.
        :rtype: List of ContentType

        Usage:
        # >>> stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development')
        # >>> content_types = stack.content_types()
        """
        content_types_query: dict = {'include_count': 'true'}
        https_request = http_request.HTTPRequestConnection('content_types', content_types_query, self.__stack_headers)
        return https_request.http_request()

    def asset(self, uid: str = None):

        """
        Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use. These files can be
        attached and used in multiple entries. Learn more about Assets.
        API Reference : https://www.contentstack.com/docs/guide/content-management#working-with-assets
        :param uid:
        :return: asset


        [All Assets]

        This call fetches the list of all the assets of a particular stack.
        It also returns the content of each asset in JSON format. You can also specify the environment of
        which you wish to get the assets.You can apply queries to
        filter assets/entries. Refer to the Queries [https://www.contentstack.com/docs/apis/content-delivery-api/#queries] section for more details.

        [Single Asset]

        This call fetches the latest version of a specific asset of a particular stack.
        """
        from contentstack import Asset
        assets = Asset(asset_uid=uid)
        assets.set_header(self.__stack_headers)
        if uid is not None:
            assets.set_uid(asset_uid=uid)
        return assets

    def asset_library(self):
        from contentstack import AssetLibrary
        asset_library = AssetLibrary()
        asset_library.headers(self.__stack_headers)
        return asset_library

    @property
    def application_key(self):
        """ :returns API_key: str """
        if 'api_key' in self.__stack_headers:
            app_key = self.__stack_headers['api_key']
            return app_key

    @property
    def access_token(self):

        """
        get_access_token() method returns access token for the current stack
        :return self:
        """
        if 'access_token' in self.__stack_headers:
            access_token = self.__stack_headers['access_token']
            return access_token

    def remove_header(self, header_key):

        """
        remove_header() method removes existing header by key
        """
        if header_key in self.__stack_headers:
            self.__stack_headers.pop(header_key, None)
        return self

    def image_transform(self, image_url: str, **kwargs):

        """
        @contentstack is a headless, API-first content management system (CMS)
        that provides everything you need to power your web or mobile properties.
        To learn more about Contentstack, visit our website or refer to our
        documentation site to understand what we do.
        This document is a detailed reference to Contentstack Image Delivery API
        and covers the parameters that you can add to the URL to retrieve images.
        The Image Delivery API is used to retrieve, manipulate and/or convert image
        files of your Contentstack account and deliver it to your web or mobile properties.

        It is an second parameter in which we want to place different manipulation key and value in array form
        ImageTransform function is define for image manipulation with different
        transform_params in second parameter in array form

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

        """
        self.__query_params['include_collaborators'] = 'true'
        return self

    def include_stack_variables(self):

        """
        Stack variables are extra information about the stack,
        such as the description, format of date,
        format of time, and so on. Users can include or exclude stack variables in the response.
        """
        self.__query_params['include_stack_variables'] = 'true'
        return self

    def include_discrete_variables(self):

        """
        view the access token of your stack.
        """
        self.__query_params['include_discrete_variables'] = 'true'
        return self

    def include_count(self):

        """
        the total count of entries available in a content type.
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
        :return: list[SyncStack]
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

        self.__sync_query = {'init': 'true', 'sync_token': sync_token}
        return self.__sync_request()

    def sync(self, from_date=None, content_type_uid=None, publish_type=None, locale=None):

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
        asset_published, entry_published, asset_unpublished, asset_deleted, entry_unpublished, entry_deleted,  content_type_deleted.
        If you do not specify any value, it will bring all published entries and published assets.
        """

        self.__sync_query["init"] = 'true'
        if from_date is not None:
            self.__sync_query["start_from"] = from_date
        if content_type_uid is not None:
            self.__sync_query["content_type_uid"] = content_type_uid
        if publish_type is not None:
            self.__sync_query["type"] = publish_type
        if locale is not None:
            self.__sync_query["locale"] = locale

        if self.__stack_headers is not None and len(self.__stack_headers) > 0:
            if 'environment' in self.__stack_headers:
                env = self.__stack_headers['environment']
                self.__sync_query['environment'] = env
        else:
            raise KeyError("Kindly provide stack headers")

        return self.__sync_request()

    @property
    def environment(self):
        if 'environment' in self.__stack_headers:
            return self.__stack_headers['environment']

    @environment.setter
    def environment(self, environment):
        if environment in self.__stack_headers:
            self.__stack_headers['environment'] = environment

    @property
    def headers(self):
        return self.__stack_headers

    def set_header(self, key, value):
        """
        set_header() method sets additional headers to the stack
        :returns _local_headers
        """
        self.__stack_headers[key] = value

    def __setup_stack(self):

        self.__stack_headers['api_key'] = self.__api_key
        self.__stack_headers['access_token'] = self.__access_token
        self.__stack_headers['environment'] = self.__environment

    def __sync_request(self) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack import Config
        error = None

        sync_url = Config().endpoint('sync')
        self.__stack_headers.update(self.header_agents())
        payload = parse.urlencode(query=self.__sync_query, encoding='UTF-8')

        try:
            response: Response = requests.get(sync_url, params=payload, headers=self.__stack_headers)

            if response.ok:
                response: dict = response.json()
                response: SyncStack = SyncStack(response)

            else:
                error = response.json()

            return response, error

        except requests.exceptions.RequestException as e:
            raise ConnectionError(e.response)
            pass

    def fetch(self) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack import Config
        error = None

        stack_url = Config().endpoint('stacks')
        self.__stack_headers.update(self.header_agents())
        payload = parse.urlencode(query=self.__query_params, encoding='UTF-8')

        try:
            response: Response = requests.get(stack_url, params=payload, headers=self.__stack_headers)

            if response.ok:
                result = response.json()
                if 'stack' in result:
                    response = result['stack']
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


class SyncStack:

    def __init__(self, json_dict: dict):

        self.__sync_dict = json_dict

        if self.__sync_dict is not None:

            if "items" in self.__sync_dict:
                self.__items = self.__sync_dict['items']
            if "skip" in self.__sync_dict:
                self.__skip = self.__sync_dict['skip']
            if "limit" in self.__sync_dict:
                self.__limit = self.__sync_dict['limit']
            if "total_count" in self.__sync_dict:
                self.__total_count = self.__sync_dict['total_count']
            if "sync_token" in self.__sync_dict:
                self.__sync_token = self.__sync_dict['sync_token']
            if "pagination_token" in self.__sync_dict:
                self.__pagination_token = self.__sync_dict['pagination_token']

    @property
    def json(self):
        return self.__sync_dict

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
