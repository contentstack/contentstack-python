"""
The Get a single entry request fetches a particular entry of a content type.
API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#single-entry
"""

import logging
from urllib import parse

from contentstack.entryqueryable import EntryQueryable

# ************* Module Entry **************
# Your code has been rated at 10/10 by pylint


log = logging.getLogger(__name__)


class Entry(EntryQueryable):
    """
    An entry is the actual piece of content that you want to publish.
    Entries can be created for one of the available content types.

    Entry works with
    version={version_number}
    environment={environment_name}
    locale={locale_code}
    """

    def __init__(self, http_instance, content_type_uid, entry_uid):
        super().__init__()
        EntryQueryable.__init__(self)
        self.entry_param = {}
        self.http_instance = http_instance
        self.content_type_id = content_type_uid
        self.entry_uid = entry_uid
        self.base_url = self.__get_base_url()

    def environment(self, environment):
        """
        Enter the name of the environment of which the entries needs to be included
        Example: production
        :param environment: {str} name of the environment of which the entries needs to be included.
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
        :return: Entry, so you can chain this call.
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

    def __get_base_url(self):
        if None in (self.http_instance, self.content_type_id, self.entry_uid):
            raise KeyError('Provide valid http_instance, content_type_uid or entry_uid')
        url = '{}/content_types/{}/entries/{}' \
            .format(self.http_instance.endpoint, self.content_type_id, self.entry_uid)
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
        encoded_string = parse.urlencode(self.entry_param, doseq=True)
        url = '{}?{}'.format(self.base_url, encoded_string)
        return self.http_instance.get(url)
