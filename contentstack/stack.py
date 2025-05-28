import enum
import logging
from urllib import parse
from urllib3.util import Retry

from contentstack.asset import Asset
from contentstack.assetquery import AssetQuery
from contentstack.contenttype import ContentType
from contentstack.globalfields import GlobalField
from contentstack.https_connection import HTTPSConnection
from contentstack.image_transform import ImageTransform

DEFAULT_HOST = 'cdn.contentstack.io'


class ContentstackRegion(enum.Enum):
    """
    Sets region for the contentstack
    """
    US = 'us'
    EU = 'eu'
    AZURE_NA = 'azure-na'
    AZURE_EU = 'azure-eu'
    GCP_NA = 'gcp-na'


class Stack:
    """
    A stack can be defined as a pool of data or a container that holds all
    the content/assets related to a site. It is a collaboration space where multiple users can work
    together to create, edit, approve, and publish content.
    (API Reference)[https://www.contentstack.com/docs/developers/apis/content-delivery-api/#stack]:
    """

    def __init__(self, api_key: str, delivery_token: str, environment: str,
                 host=DEFAULT_HOST,
                 version='v3',
                 region=ContentstackRegion.US,
                 timeout=30,
                 retry_strategy=Retry(
                     total=5, backoff_factor=0, status_forcelist=[408, 429]),
                 live_preview=None,
                 branch=None,
                 early_access = None,
                 logger=None,
                 ):
        """
        # Class that wraps the credentials of the authenticated user. Think of
        this as a container that holds authentication related data.

        param api_key: api_key of the stack
        :param delivery_token: delivery_token of the stack
        :param environment: environment of the stack
        :param host: (optional) host of the stack default is cdm.contentstack.io
        :param branch: branch of the stack
        :param version: (optional) apiVersion of the stack default is v3
        :param region: (optional) region support of the stack default is ContentstackRegion.US
        :param live_preview: (optional) accepts type dictionary that enables
        live_preview option for request,
        takes input as dictionary object. containing one/multiple key value pair like below.

        ```python
    live_preview = {
            'enable': True,
            'host': 'api.contentstack.io',
            'authorization': 'your_management_token',
            'include_edit_tags': True,
            'edit_tags_type': object | str,
            }
        ```
        :param retry_strategy: (optional) custom retry_strategy can be set.
        Method to create retry_strategy: create object of Retry() and provide the
        required parameters like below
        **Example:**

        >>> _strategy = Retry(total=5, backoff_factor=1, status_forcelist=[408, 429])
        >>> import contentstack
        >>> stack = contentstack.Stack("api_key", "delivery_token", "environment",
                live_preview={enable=True, authorization='your auth token'}, retry_strategy= _strategy)
        ```
        """
        self.logger = logger or logging.getLogger(__name__)
        self.headers = {}
        self._query_params = {}
        self.sync_param = {}
        self.endpoint = None
        self.http_instance = None
        self.api_key = api_key
        self.delivery_token = delivery_token
        self.environment = environment
        self.host = host
        self.version = version
        self.region = region
        self.timeout = timeout
        self.branch = branch
        self.retry_strategy = retry_strategy
        self.live_preview = live_preview
        self.early_access = early_access
        self._validate_stack()
        self._setup_headers()
        self._setup_live_preview()
        self.http_instance = HTTPSConnection(
            endpoint=self.endpoint,
            headers=self.headers,
            timeout=self.timeout,
            retry_strategy=self.retry_strategy,
            live_preview=self.live_preview
        )

    def _validate_stack(self):
        if self.api_key is None or self.api_key == '':
            raise PermissionError(
                'You are not permitted to the stack without valid APIKey'
            )
        if self.delivery_token is None or self.delivery_token == "":
            raise PermissionError(
                'You are not permitted to the stack without valid Delivery Token'
            )
        if self.environment is None or self.environment == "":
            raise PermissionError(
                'You are not permitted to the stack without valid Environment'
            )

        if self.region.value == 'eu' and self.host == DEFAULT_HOST:
            self.host = 'eu-cdn.contentstack.com'
        elif self.region.value == 'azure-na' and self.host == DEFAULT_HOST:
            self.host = 'azure-na-cdn.contentstack.com'
        elif self.region.value == 'azure-eu' and self.host == DEFAULT_HOST:
            self.host = 'azure-eu-cdn.contentstack.com'
        elif self.region.value == 'gcp-na' and self.host == DEFAULT_HOST:
            self.host = 'gcp-na-cdn.contentstack.com'
        elif self.region.value != 'us':
            self.host = f'{self.region.value}-{DEFAULT_HOST}'
        self.endpoint = f'https://{self.host}/{self.version}'

    def _setup_headers(self):
        self.headers = {
            'api_key': self.api_key,
            'access_token': self.delivery_token,
            'environment': self.environment
        }
        if self.early_access is not None:
            early_access_str = ', '.join(self.early_access)
            self.headers['x-header-ea'] = early_access_str
 
        if self.branch is not None:
            self.headers['branch'] = self.branch
   
    @property
    def get_api_key(self):
        """
        :return: api_key of the stack
        """
        return self.api_key
    
    @property
    def get_early_access(self):
        """
        :return: early access
        """
        return self.early_access

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
    def get_branch(self):
        """
        :return: branch of the stack
        """
        return self.branch

    @property
    def get_headers(self):
        """
        :return: validating credentials http header of the stack
        """
        return self.headers

    @property
    def get_live_preview(self):
        """
        :return: live preview dictionary
        """
        return self.live_preview

    def content_type(self, content_type_uid=None):
        """
        Content type defines the structure or schema of a page or a section
        of your web or mobile property.
        param content_type_uid:
        :return: ContentType
        """
        return ContentType(self.http_instance, content_type_uid)
    
    def global_field(self, global_field_uid=None):
        """
        Global field defines the structure or schema of a page or a section
        of your web or mobile property.
        param global_field_uid:
        :return: GlobalField
        """
        return GlobalField(self.http_instance, global_field_uid)

    def asset(self, uid):
        """
        Assets refer to all the media files (images, videos, PDFs, audio files, and so on)
        uploaded in your Contentstack repository for future use.
        param uid: asset_uid of the Asset
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

    def sync_init(self, content_type_uid=None, start_from=None, locale=None, publish_type=None):
        """
        Set init to ‘true’ if you want to sync all the published entries and assets.
        This is usually used when the app does not have any content, and you want to
        get all the content for the first time.\n

        :param content_type_uid: (optional) content type UID. e.g., products
                    This retrieves published entries of specified content type
        :param start_from: (optional) The start date. e.g., 2018-08-14T00:00:00.000Z
                    This retrieves published entries starting from a specific date
        :param locale: (optional) locale code. e.g., en-us, This retrieves published
        entries of specific locale.
        :param publish_type: (optional) If you do not specify any value,
                    it will bring all published
                    entries and published assets. You can pass multiple types
                    as comma-separated values,
                    for example, entry_published,entry_unpublished,asset_published
        :return: list of sync items
        -------------------------------

        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.sync_init(content_type_uid='content_type_uid',
                         start_from='date', locale='en-us', publish_type='asset_published')
        -------------------------------
        """
        self.sync_param['init'] = 'true'
        if content_type_uid is not None and isinstance(content_type_uid, str):
            self.sync_param['content_type_uid'] = content_type_uid
        if start_from is not None and isinstance(start_from, str):
            self.sync_param['start_from'] = start_from
        if locale is not None and isinstance(locale, str):
            self.sync_param['locale'] = locale
        if publish_type is not None and isinstance(publish_type, str):
            self.sync_param['type'] = publish_type
        return self.__sync_request()

    def pagination(self, pagination_token: str):
        """
        If the result of the initial sync (or subsequent sync)
        contains more than 100 records, the response would be
        paginated. It provides pagination token in the response.
        However, you do not have to use the pagination token
        manually to get the next batch.
        param pagination_token:
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
        param sync_token: sync_token
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
        param url is URL for :class:`Request` object.
        in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        base_url = f'{self.http_instance.endpoint}/stacks/sync'
        self.sync_param['environment'] = self.http_instance.headers['environment']
        query = parse.urlencode(self.sync_param)
        return self.http_instance.get(f'{base_url}?{query}')

    def image_transform(self, image_url, **kwargs):
        """
        This document is a detailed reference to Contentstack’s Image Delivery
        API and covers the parameters that you can add to the URL to retrieve,
        manipulate (or convert) image files and display it to your web or
        mobile properties.\n

        :param image_url: base url on which queries to apply
        :param kwargs: to append queries to the asset URL.
        :return: instance of ImageTransform
        """
        if image_url is None or image_url == '':
            raise PermissionError(
                'image_url required for the image_transformation')
        return ImageTransform(self.http_instance, image_url, **kwargs)
    
    def _setup_live_preview(self):
        if self.live_preview and self.live_preview.get("enable"):
            region_prefix = "" if self.region.value == "us" else f"{self.region.value}-"
            self.live_preview["host"] = f"{region_prefix}rest-preview.contentstack.com"

            if self.live_preview.get("preview_token"):
                self.headers["preview_token"] = self.live_preview["preview_token"]


    def live_preview_query(self, **kwargs):
        """
        live_preview_query accepts key value pair objects to the query
        hash, content_type_uid and entry_uid
        Example:
            # def live_preview_query(**kwargs):
            # kwargs is a dict of the keyword args passed to the function
            for key, value in kwargs.iteritems():
                print "%s = %s" % (key, value)
            Uses:=>
        live_preview_query = (
                'enable': True,
                'live_preview': '#*#*#*#*#',
                'host': 'your_host',
                'content_type_uid': 'product',
                'entry_uid': 'your_entry_uid',
                'authorization': 'management_token'
                )
        """
        if self.live_preview and self.live_preview.get("enable") and "live_preview_query" in kwargs:
            query = kwargs["live_preview_query"]
            if isinstance(query, dict):
                self.live_preview.update(query)
                self.live_preview["live_preview"] = query.get("live_preview", "init")
                if "content_type_uid" in query:
                    self.live_preview["content_type_uid"] = query["content_type_uid"]
                if "entry_uid" in query:
                    self.live_preview["entry_uid"] = query["entry_uid"]

                for key in ["release_id", "preview_timestamp"]:
                    if key in query:
                        self.http_instance.headers[key] = query[key]
                    else:
                        self.http_instance.headers.pop(key, None)

                self._cal_url()
        return self

    def _cal_url(self):
        host = self.live_preview.get("host", DEFAULT_HOST)
        content_type = self.live_preview.get("content_type_uid", "default_content_type")
        url = f"https://{host}/v3/content_types/{content_type}/entries"
        entry_uid = self.live_preview.get("entry_uid")
        live_preview = self.live_preview.get("live_preview", "init")
        if entry_uid:
            url = f"{url}/{entry_uid}?live_preview={live_preview}"
        self.live_preview["url"] = url
