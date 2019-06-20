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
import urllib
import logging
import contentstack
from contentstack import errors as err
from contentstack import config
from contentstack import content_type
import requests
import requests
import platform
from re import sub

"""
contentstack.stack
~~~~~~~~~~~~~~~~~~
A stack is a space that stores the content of a project (a web or mobile property).
Within a stack, you can create content structures, content entries, users, etc.
related to the project. Read more about Stacks

API Reference: [https://www.contentstack.com/docs/guide/stack]
"""


class Stack(object):
    """
    >>> import contentstack
    >>> stack = contentstack.Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development')

    """

    def __init__(self, api_key: str, access_token: str, environment: str, configs: config.Config = None):
        """
        A stack is a space that stores the content of a project (a web or mobile property).
        Within a stack, you can create content structures, content entries, users, etc.
        related to the project. Read more about Stacks
        API Reference: [https://www.contentstack.com/docs/guide/stack]
        :param api_key:
        :param access_token:
        :param environment:
        :param configs:
        """
        logging.debug('stack initialisation attempted with: ', api_key, access_token, environment)

        self._api_key = api_key
        self._access_token = access_token
        self._environment = environment

        if configs is not None:
            self._configs = configs
            self.set_config(config)

        self._initialise_stack()
        # declare stack class variables
        self._stack_query = dict()
        self._local_headers = dict()
        self._setup_stack()
        # set class variables to initialise image transformation.
        self._image_transform_url = None
        self._image_params = dict
        # set sync variables
        self._sync_query = dict()

    def _initialise_stack(self):
        if not self._api_key:
            raise err.StackException(
                'Please enter the API key of stack of which you wish to retrieve the content types.'
            )
        if not self._access_token:
            raise err.StackException(
                'Enter the access token of your stack.'
            )
        if not self._environment:
            raise err.StackException(
                'Environment can not be Empty.'
            )

    def set_config(self, configs: config.Config) -> config.Config:
        """
        :type configs: object
        :param configs:
        :return:
        """
        self._configs = configs
        if self._environment is not None:
            self._configs.set_environment(self._environment)
            self.set_environment(self._environment)
        return self._configs

    def stack(self, api_key):
        self._local_headers['api_key'] = api_key
        return self

    def _get_url(self, url: str) -> object:
        api_version: str = self._configs.get_version()
        host_url = self._configs.get_host()
        http_protocol = self._configs.get_http_protocol()
        return "/{0}/{1}/{2}/{3}".format(http_protocol, host_url, api_version, url)

    @staticmethod
    def content_type(content_type_id):
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
        return content_type.ContentType(content_type_id)

    def content_types(self):
        """Fetches all Content Types from the Stack.

        This call returns comprehensive information of all the content types available in a particular stack in your account.
        API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#content-types

        :param query: (optional) Dict with API options.
        :return: List of :class:`ContentType <contentful.content_type.ContentType>` objects.
        :rtype: List of contentful.content_type.ContentType

        Usage:
            >>> stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development')
            >>> content_types = stack.content_types()
        """
        return self._get_url('content_types?include_count=true')

    def get_application_key(self):

        """
        get_application_key() returns stack API_Key
        return self
        """
        if 'api_key' in self._local_headers:
            app_key = self._local_headers['api_key']
            return app_key

    def get_access_token(self):

        """
        get_access_token() method returns access token for the current stack
        :return self:
        """
        if 'access_token' in self._local_headers:
            access_token = self._local_headers['access_token']
            return access_token

    def remove_header(self, header_key):
        """
        remove_header() method removes existing header by key
        """
        if header_key in self._local_headers:
            del self._local_headers[header_key]
            return self

    def set_header(self, header_key, header_value):
        """
        set_header() mrthod sets additinal headers to the stack
        :returns _local_headers
        """
        self._local_headers[header_key] = header_value
        return self._local_headers

    def image_transform(self, image_url: str, transform_params=dict):

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
        self._image_transform_url = image_url
        self._image_params = transform_params
        return self._get_image_url()

    def _get_image_url(self):
        image_param_counter = len(self._image_params)
        if image_param_counter > 0:
            _url = urllib.parse.urlencode(self._image_params)
            return self._get_url(_url)
        else:
            return self._image_transform_url

    def get_collaborators(self):
        """
        collaborators with whom the stacks are shared.
        A detailed information about each collaborator is returned.
        """
        self._stack_query['include_collaborators'] = True
        return self

    def get_included_stack_variables(self):
        """
        Stack variables are extra information about the stack,
        such as the description, format of date,
        format of time, and so on. Users can include or exclude stack variables in the response.
        """
        self._stack_query['include_stack_variables'] = True
        return self

    def get_included_descrete_variables(self):
        """
        view the access token of your stack.
        """
        self._stack_query['include_discrete_variables'] = True
        return self

    def include_count(self):
        """
        the total count of entries available in a content type.
        """
        self._stack_query['include_count'] = True
        return self

    def sync_pagination(self, pagination_token: str):
        """
        If the result of the initial sync (or subsequent sync) contains more than 100 records,
        the response would be paginated. It provides pagination token in the response. However,
        you do not have to use the pagination token manually to get the next batch,
        the SDK does that automatically until the sync is complete.
        Pagination token can be used in case you want to fetch only selected batches.
        It is especially useful if the sync process is interrupted midway (due to network issues, etc.).
        In such cases, this token can be used to restart the sync process from where it was interrupted.
        """
        self._sync_query = {'init': True, 'pagination_token': pagination_token}
        return self._sync_query

    def sync_token(self, sync_token):
        """
        You can use the sync token (that you receive after initial sync)
        to get the updated content next time.
        The sync token fetches only the content that was added after your last sync,
        and the details of the content that was deleted or updated.
        """
        self._sync_query = {'init': True, 'sync_token': sync_token}
        return self._sync_query

    def sync(self, from_date=None, content_type_uid=None, publish_type=None, language_code='en-us'):

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

        self._sync_query['init'] = True
        if from_date is not None:
            self._sync_query["start_from"] = from_date
        if content_type_uid is not None:
            self._sync_query["content_type_uid"] = content_type_uid
        if publish_type is not None:
            self._sync_query["type"] = publish_type
        if language_code is not None:
            self._sync_query["locale"] = language_code

        return self._sync_query

    def get_stack_query(self):
        return self._stack_query

    def get_sync_query(self):
        return self._sync_query

    def local_headers(self):
        # Sets the default Request Headers.
        self._local_headers['X-User-Agent'] = self._contentful_user_agent()
        self._local_headers['Content-Type'] = 'application/contentstack.v{0}+json'.format(self._configs.SDK_VERSION)
        self._local_headers['Accept-Encoding'] = 'accept-encoding'
        return self._local_headers

    def get_environment(self):
        return self._local_headers['environment']

    def set_environment(self, environment):
        if environment in self._local_headers:
            self._local_headers['environment'] = environment
        return self

    def _setup_stack(self):
        self._local_headers['api_key'] = self._api_key
        self._local_headers['access_token'] = self._access_token
        self._local_headers['environment'] = self._environment
        # setup environment
        # null pointer checked already
        # self._configs.set_environment(self._environment)
