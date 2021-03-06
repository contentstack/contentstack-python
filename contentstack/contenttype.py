"""
Content type defines the structure or schema of a page or a section of your web
or mobile property. To create content for your application, you are required
to first create a content type, and then create entries using the
content type.
"""

# ************* Module ContentType **************
# Your code has been rated at 10.00/10 by pylint

import logging
from urllib import parse

from contentstack.entry import Entry
from contentstack.query import Query

log = logging.getLogger(__name__)

class ContentType:
    """
    Content type defines the structure or schema of a page or a
    section of your web or mobile property. To create
    content for your application, you are required to
    first create a content type, and then create entries using the
    content type.
    """

    def __init__(self, http_instance, content_type_uid):
        self.http_instance = http_instance
        self.__content_type_uid = content_type_uid
        self.local_param = {}

    def entry(self, entry_uid: str):
        r"""
        An entry is the actual piece of content created using one of the defined content types.
        :param entry_uid: {str} -- unique ID of the entry that you wish to fetch
        :return: Entry -- Returns the Entry class object so we can chain the entry functions

        --------------------------------

        [Example:]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
        --------------------------------
        """
        if self.__content_type_uid is None:
            raise PermissionError('Please provide valid content_type_uid')
        if entry_uid is None:
            raise PermissionError('Please provide valid entry uid')
        entry = Entry(self.http_instance, self.__content_type_uid, entry_uid=entry_uid)
        return entry

    def query(self):
        """
        It returns query class object so we can query on entry of specified ContentType
        :return: Query -- query object instance, so we can chain the query functions to it.
        ------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
        ------------------------------
        """
        if self.__content_type_uid is None:
            raise PermissionError('Kindly provide content_type_uid')
        return Query(self.http_instance, self.__content_type_uid)

    def fetch(self):
        """
        This method is useful to fetch ContentType of the of the stack.
        :return:dict -- contentType response
        ------------------------------
        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> some_dict = {'abc':'something'}
            >>> response = content_type.fetch(some_dict)
        ------------------------------
        """
        if self.__content_type_uid is None:
            raise KeyError('content_type_uid can not be None to fetch contenttype')
        self.local_param['environment'] = self.http_instance.headers['environment']
        uri = '{}/content_types/{}'.format(self.http_instance.endpoint, self.__content_type_uid)
        encoded_params = parse.urlencode(self.local_param)
        url = '{}?{}'.format(uri, encoded_params)
        result = self.http_instance.get(url)
        return result

    def find(self, params=None):
        """
        This method is useful to fetch ContentType of the of the stack.
        :param params: dictionary of params
        :return:dict -- contenttype response
        ------------------------------
        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type()
            >>> some_dict = {'abc':'something'}
            >>> response = content_type.find(param=some_dict)
        ------------------------------
        """
        self.local_param['environment'] = self.http_instance.headers['environment']
        if params is not None:
            self.local_param.update(params)
        encoded_params = parse.urlencode(self.local_param)
        url = '{}?{}'.format('{}/content_types'.format(self.http_instance.endpoint), encoded_params)
        result = self.http_instance.get(url)
        return result
