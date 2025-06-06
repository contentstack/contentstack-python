"""
Global field defines the structure or schema of a page or a section of your web
or mobile property. To create content for your application, you are required
to first create a Global field, and then create entries using the
Global field.
"""

import logging
from urllib import parse

class GlobalField:
    """
    Global field defines the structure or schema of a page or a
    section of your web or mobile property. To create
    content for your application, you are required to
    first create a Global field, and then create entries using the
    Global field.
    """

    def __init__(self, http_instance, global_field_uid, logger=None):
        self.http_instance = http_instance
        self.__global_field_uid = global_field_uid
        self.local_param = {}
        self.logger = logger or logging.getLogger(__name__)


    def fetch(self):
        """
        This method is useful to fetch GlobalField of the of the stack.
        :return:dict -- GlobalField response
        ------------------------------
        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> global_field = stack.global_field('global_field_uid')
            >>> some_dict = {'abc':'something'}
            >>> response = global_field.fetch(some_dict)
        ------------------------------
        """
        if self.__global_field_uid is None:
            raise KeyError(
                'global_field_uid can not be None to fetch GlobalField')
        self.local_param['environment'] = self.http_instance.headers['environment']
        uri = f'{self.http_instance.endpoint}/global_fields/{self.__global_field_uid}'
        encoded_params = parse.urlencode(self.local_param)
        url = f'{uri}?{encoded_params}'
        result = self.http_instance.get(url)
        return result

    def find(self, params=None):
        """
        This method is useful to fetch GlobalField of the of the stack.
        :param params: dictionary of params
        :return:dict -- GlobalField response
        ------------------------------
        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> global_field = stack.global_field()
            >>> some_dict = {'abc':'something'}
            >>> response = global_field.find(param=some_dict)
        ------------------------------
        """
        self.local_param['environment'] = self.http_instance.headers['environment']
        if params is not None:
            self.local_param.update(params)
        encoded_params = parse.urlencode(self.local_param)
        endpoint = self.http_instance.endpoint
        url = f'{endpoint}/global_fields?{encoded_params}'
        result = self.http_instance.get(url)
        return result
