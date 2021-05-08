"""
Class that wraps the credentials of the authenticated user. Think of
this as a container that holds authentication related data.
"""

# ************* Module stack **************
# Your code has been rated at 10.00/10

import enum
import logging
from urllib import parse
from contentstack.asset import Asset
from contentstack.assetquery import AssetQuery
from contentstack.contenttype import ContentType
from contentstack.https_connection import HTTPSConnection
from contentstack.image_transform import ImageTransform

log = logging.getLogger(__name__)


class ContentstackRegion(enum.Enum):
    """
    Sets region for the contentstack
    """
    US = 'us'
    EU = 'eu'


class Stack:
    from urllib3.util import Retry
    """
    A stack can be defined as a pool of data or a container that holds all
    the content/assets related to a site. It is a collaboration space where multiple users can work
    together to create, edit, approve, and publish content.
    (API Reference)[https://www.contentstack.com/docs/developers/apis/content-delivery-api/#stack]:
    """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(self, api_key, delivery_token, environment,
                 host='cdn.contentstack.io',
                 branch='',
                 version='v3', region=ContentstackRegion.US, timeout=30,
                 retry_strategy=Retry(total=5, backoff_factor=0, status_forcelist=[408, 429])):
        """
        Class that wraps the credentials of the authenticated user. Think of
        this as a container that holds authentication related data.
        :param api_key: api_key of the stack
        :param delivery_token: delivery_token of the stack
        :param environment: environment of the stack
        :param host: (optional) host of the stack default is cdm.contentstack.io
        :param branch: (optional) branch of the stack default is empty
        :param version: (optional) apiVersion of the stack default is v3
        :param region: (optional) region support of the stack default is ContentstackRegion.US
        :param retry_strategy (optional) custom retry_strategy can be set.
        ```
        # Method to create retry_strategy: create object of Retry() and provide the
        # required parameters like below
        **Example:**
        >>> retry_strategy = Retry(total=5, backoff_factor=1, status_forcelist=[408, 429])
        >>> stack = contentstack.Stack("APIKey", "deliveryToken", "environment", retry_strategy= retry_strategy)
        ```
        """
        logging.basicConfig(level=logging.DEBUG)
        self.headers = {}
        self.__query_params = {}
        self.sync_param = {}
        self.endpoint = None
        self.http_instance = None
        self.api_key = api_key
        self.delivery_token = delivery_token
        self.environment = environment
        self.host = host
        self.branch = branch
        self.version = version
        self.region = region
        self.timeout = timeout
        self.retry_strategy = retry_strategy
        self.__validate_stack()

    def __validate_stack(self):
        if self.api_key is None or self.api_key == '':
            raise PermissionError('You are not permitted to the stack without valid Api Key')
        if self.delivery_token is None or self.delivery_token == "":
            raise PermissionError('You are not permitted to the stack without valid Delivery Token')
        if self.environment is None or self.environment == "":
            raise PermissionError('You are not permitted to the stack without valid Environment')
        # prepare endpoint for the url:
        if self.region.value != 'us' and self.host == 'cdn.contentstack.io':
            self.host = 'eu-cdn.contentstack.com'
        self.endpoint = 'https://{}/{}'.format(self.host, self.version)
        # prepare Headers:`
        self.headers = {'api_key': self.api_key, 'access_token': self.delivery_token,
                        'environment': self.environment}
        if len(self.branch) is not 0:
            self.headers['branch'] = self.branch
        self.http_instance = HTTPSConnection(endpoint=self.endpoint,
                                             headers=self.headers, timeout=self.timeout,
                                             retry_strategy=self.retry_strategy)
        # call httpRequest instance & pass the endpoint and headers

    @property
    def get_api_key(self):
        """
        :return: api_key of the stack
        """
        return self.api_key

    @property
    def get_delivery_token(self):
        """
        :return: delivery_token of the stack
        """
        return self.delivery_token

    @property
    def get_environment(self):
        """
        :return: environment of the stack
        """
        return self.environment

    @property
    def get_headers(self):
        """
        :return: validating credentials http header of the stack
        """
        return self.headers

    def content_type(self, content_type_uid=None):
        """
        Content type defines the structure or schema of a page or a section
        of your web or mobile property.
        :param content_type_uid:
        :return: ContentType
        """
        return ContentType(self.http_instance, content_type_uid)

    def asset(self, uid):
        """
        Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use.
        :param uid: asset_uid of the Asset
        :return: Asset

        -----------------------------
        Example: provide asset_uid to fetch single asset:
            >>> import contentstack
            >>> stack = Stack('api_key', 'delivery_token', 'environment')
            >>> asset_instance = stack.asset(uid='asset_uid')
            >>> result = asset_instance.fetch()
        -----------------------------
        """
        if uid is None or not isinstance(uid, str):
            raise KeyError('Please provide a valid uid')
        return Asset(self.http_instance, uid=uid)

    def asset_query(self):
        """
        Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use.
        :return: Asset Instance
        -----------------------------
        Example: [All Assets]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset_query = stack.asset_query()
            >>> assets = asset_query.find()
        -----------------------------
        """
        return AssetQuery(self.http_instance)

    def sync_init(self, content_type_uid=None, from_date=None, locale=None, publish_type=None):
        """
        Constructs and initialises sync if no params provided else below mentioned params
        can be provided to get the response accordingly
        :param content_type_uid: subsequent syncs will only include the entries
                                 of the specified content_type.
        :param from_date: use from_date and specify the start date as its value.
        :param locale: specify the locale code as its value. However, if you do this,
                       the subsequent syncs will only include the entries of the specified locales.
        :param publish_type: Use the type parameter to get a specific
                             type of content. pass as follows:
        ``asset_published``, ``entry_published``,
        ``asset_unpublished``, ``asset_deleted``,
        ``entry_unpublished``, ``entry_deleted``, or ``content_type_deleted``.
        :return: list of sync items
        -------------------------------
        Example:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.sync_init(content_type_uid='content_type_uid',
                         from_date='date', locale='en-us', publish_type='asset_published')
        -------------------------------
        """
        self.sync_param['init'] = 'true'
        if content_type_uid is not None and isinstance(content_type_uid, str):
            self.sync_param['content_type_uid'] = content_type_uid
        if from_date is not None and isinstance(from_date, str):
            self.sync_param['from_date'] = from_date
        if locale is not None and isinstance(locale, str):
            self.sync_param['locale'] = locale
        if publish_type is not None and isinstance(publish_type, str):
            self.sync_param['publish_type'] = publish_type
        return self.__sync_request()

    def pagination(self, pagination_token: str):
        """
        If the result of the initial sync (or subsequent sync)
        contains more than 100 records, the response would be
        paginated. It provides pagination token in the response.
        However, you do not have to use the pagination token
        manually to get the next batch.
        :param pagination_token:
        :return: list of sync items
        ------------------------------
        Example:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.pagination('pagination_token')
        ------------------------------
        """
        if isinstance(pagination_token, str):
            self.sync_param = {'pagination_token': pagination_token}
        return self.__sync_request()

    def sync_token(self, sync_token):
        """You can use the sync token (that you receive after initial sync)
        to get the updated content next time. The sync token fetches
        only the content that was added
        after your last sync, and the details of the content that was deleted or updated.
        :param sync_token: sync_token
        :return: list of Sync Result
        ------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.sync_token('sync_token')
        -------------------------------
        """
        if isinstance(sync_token, str):
            self.sync_param = {'sync_token': sync_token}
        return self.__sync_request()

    def __sync_request(self):
        r"""Sends a GET request.
        :param url URL for :class:`Request` object.
        in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        base_url = '{}/stacks/sync'.format(self.http_instance.endpoint)
        self.sync_param['environment'] = self.http_instance.headers['environment']
        encoded_query = parse.urlencode(self.sync_param)
        url = '{}?{}'.format(base_url, encoded_query)
        result = self.http_instance.get(url)
        return result

    def image_transform(self, image_url, **kwargs):
        """
        This document is a detailed reference to Contentstack’s Image Delivery
        API and covers the parameters that you can add to the URL to retrieve,
        manipulate (or convert) image files and display
        it to your web or mobile properties.
        :param image_url: base url on which queries to apply
        :param kwargs: append queries to the asset URL.
        :return: instance of ImageTransform
        """
        if image_url is None or image_url == '':
            raise PermissionError('image_url required for the image_transformation')
        return ImageTransform(self.http_instance, image_url, **kwargs)
