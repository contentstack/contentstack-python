"""
The Get a single entry request fetches a particular entry of a content type.
API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#single-entry
"""
#min-similarity-lines=10
import logging
from urllib import parse

from contentstack.deep_merge_lp import DeepMergeMixin
from contentstack.entryqueryable import EntryQueryable
from contentstack.variants import Variants

class Entry(EntryQueryable):
    """
    An entry is the actual piece of content that you want to publish.
    Entries can be created for one of the available content types.

    Entry works with
    version={version_number}
    environment={environment_name}
    locale={locale_code}
    """

    def __init__(self, http_instance, content_type_uid, entry_uid, logger=None):
        super().__init__()
        EntryQueryable.__init__(self)
        self.entry_param = {}
        self.http_instance = http_instance
        self.content_type_id = content_type_uid
        self.entry_uid = entry_uid
        self.base_url = self.__get_base_url()
        self.logger = logger or logging.getLogger(__name__)

    def environment(self, environment):
        """
        Enter the name of the environment of which the entries need to be included
        Example: production
        :param environment: {str} name of the environment of which the entries need to be included.
        :return: Entry, so you can chain this call.
        ------------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry.environment('production')
            >>> result = entry.fetch()
        ------------------------------
        """
        if environment is None:
            raise KeyError('Kindly provide a valid environment')
        self.http_instance.headers['environment'] = environment
        return self

    def version(self, version):
        """When no version is specified, it returns the latest version
        To retrieve a specific version, specify the version number under this parameter.
        In such a case, DO NOT specify any environment. Example: 4

        :param version: {int} -- version
        :return: Entry, so you can chain this call.
        ------------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry.version(4)
            >>> result = entry.fetch()
        ------------------------------
        """
        if version is None:
            raise KeyError('Kindly provide a valid version')
        self.entry_param['version'] = version
        return self

    def param(self, key, value):
        """
        This method is useful to add additional Query parameters to the entry
        :param key: {str} -- key The key as string which needs to be added to an Entry
        :param value: {object} -- value The value as string which needs to be added to an Entry
        :return: @Entry, so you can chain this call.
        -----------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry = entry.param('key', 'value')
            >>> result = entry.fetch()
        -----------------------------
        """
        if None in (key, value) and not isinstance(key, str):
            raise ValueError('Kindly provide valid key and value arguments')
        self.entry_param[key] = value
        return self

    def include_fallback(self):
        """Retrieve the published content of the fallback locale if an entry is
        not localized in specified locale.
        :return: Entry, so we can chain the call
        ----------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry = entry.include_fallback()
            >>> result = entry.fetch()
        ----------------------------
        """
        print('Requesting fallback....')
        self.entry_param['include_fallback'] = 'true'
        return self

    def include_branch(self):
        """Retrieve the published pranch in the entry response
        :return: Entry, so we can chain the call
        ----------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry = entry.include_branch()
            >>> result = entry.fetch()
        ----------------------------
        """
        self.entry_param['include_branch'] = 'true'
        return self

    def include_embedded_items(self):
        """include_embedded_items instance of Entry
        include_embedded_objects (Entries and Assets) along with entry/entries details.
        :return: Entry, so we can chain the call

        ----------------------------
        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry = entry.include_embedded_items()
            >>> result = entry.fetch()
        ----------------------------
        """
        self.entry_param['include_embedded_items[]'] = "BASE"
        return self

    def __get_base_url(self, endpoint=''):
        if endpoint is not None and endpoint.strip(): # .strip() removes leading/trailing whitespace
            self.http_instance.endpoint = endpoint
        if None in (self.http_instance, self.content_type_id, self.entry_uid):
            raise KeyError(
                'Provide valid http_instance, content_type_uid or entry_uid')
        url = f'{self.http_instance.endpoint}/content_types/{self.content_type_id}/entries/{self.entry_uid}'
        return url

    def fetch(self):
        """
        Fetches the latest version of the entries from stack
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> result = entry.fetch()
        -------------------------------
        """
        if 'environment' in self.http_instance.headers:
            self.entry_param['environment'] = self.http_instance.headers['environment']
        if len(self.entry_queryable_param) > 0:
            self.entry_param.update(self.entry_queryable_param)
        encoded_str = parse.urlencode(self.entry_param, doseq=True)
        url = f'{self.base_url}?{encoded_str}'
        self._impl_live_preview()
        response = self.http_instance.get(url)
        if self.http_instance.live_preview is not None and not 'errors' in response:
            self.http_instance.live_preview['entry_response'] = response['entry']
            return self._merged_response()
        return response

    def _impl_live_preview(self):
        lv = self.http_instance.live_preview
        if lv is not None and lv['enable'] and 'content_type_uid' in lv and lv[
            'content_type_uid'] == self.content_type_id:
            url = lv['url']
            if lv.get('management_token'):
                self.http_instance.headers['authorization'] = lv['management_token']
            else:
                self.http_instance.headers['preview_token'] = lv['preview_token']
            lp_resp = self.http_instance.get(url)
            if lp_resp is not None and not 'error_code' in lp_resp:
                self.http_instance.live_preview['lp_response'] = lp_resp
            return None
        return None

    def _merged_response(self):
        if 'entry_response' in self.http_instance.live_preview and 'lp_response' in self.http_instance.live_preview:
            entry_response = self.http_instance.live_preview['entry_response']
            # Ensure lp_entry exists
            if 'entry' in self.http_instance.live_preview.get('lp_response', {}):
                lp_entry = self.http_instance.live_preview['lp_response']['entry']
            else:
                lp_entry = {} 
            if not isinstance(entry_response, list):
                entry_response = [entry_response]
            if not isinstance(lp_entry, list):
                lp_entry = [lp_entry]  # Wrap in a list if it's a dict
            if not all(isinstance(item, dict) for item in entry_response):
                raise TypeError(f"entry_response must be a list of dictionaries. Got: {entry_response}")
            if not all(isinstance(item, dict) for item in lp_entry):
                raise TypeError(f"lp_entry must be a list of dictionaries. Got: {lp_entry}")
            merged_response = DeepMergeMixin(entry_response, lp_entry).to_dict()  # Convert to dictionary
            return merged_response  # Now correctly returns a dictionary
        raise ValueError("Missing required keys in live_preview data")
    
    def variants(self, variant_uid: str | list[str], params: dict = None):
        """
        Fetches the variants of the entry
        :param variant_uid: {str} -- variant_uid
        :return: Entry, so you can chain this call.
        """
        return Variants(
            http_instance=self.http_instance,
            content_type_uid=self.content_type_id,
            entry_uid=self.entry_uid,
            variant_uid=variant_uid,
            params=params,
            logger=self.logger
        )





