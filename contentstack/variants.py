import logging
from urllib import parse

from contentstack.entryqueryable import EntryQueryable

class Variants(EntryQueryable):
    """
    An entry is the actual piece of content that you want to publish.
    Entries can be created for one of the available content types.

    Entry works with
    version={version_number}
    environment={environment_name}
    locale={locale_code}
    """

    def __init__(self,
        http_instance=None,
        content_type_uid=None,
        entry_uid=None,
        variant_uid=None,
        params=None,
        logger=None):
        
        super().__init__()
        EntryQueryable.__init__(self)
        self.entry_param = {}
        self.http_instance = http_instance
        self.content_type_id = content_type_uid
        self.entry_uid = entry_uid
        self.variant_uid = variant_uid
        self.logger = logger or logging.getLogger(__name__)
        self.entry_param = params or {}

    def find(self, params=None):
        """
        find the variants of the entry of a particular content type
        :param self.variant_uid: {str} -- self.variant_uid
        :return: Entry, so you can chain this call.
        """
        headers = self.http_instance.headers.copy()  # Create a local copy of headers
        if isinstance(self.variant_uid, str):
            headers['x-cs-variant-uid'] = self.variant_uid
        elif isinstance(self.variant_uid, list):
            headers['x-cs-variant-uid'] = ','.join(self.variant_uid)
        
        if params is not None:
            self.entry_param.update(params)
        encoded_params = parse.urlencode(self.entry_param)
        endpoint = self.http_instance.endpoint
        url = f'{endpoint}/content_types/{self.content_type_id}/entries?{encoded_params}'
        self.http_instance.headers.update(headers)
        result = self.http_instance.get(url)
        self.http_instance.headers.pop('x-cs-variant-uid', None)
        return result
    
    def fetch(self, params=None):
        """
        This method is useful to fetch variant entries of a particular content type and entries of the of the stack.
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
        """
        Fetches the variants of the entry
        :param self.variant_uid: {str} -- self.variant_uid
        :return: Entry, so you can chain this call.
        """
        if self.entry_uid is None:
            raise ValueError("entry_uid is required")
        else:
            headers = self.http_instance.headers.copy()  # Create a local copy of headers
            if isinstance(self.variant_uid, str):
                headers['x-cs-variant-uid'] = self.variant_uid
            elif isinstance(self.variant_uid, list):
                headers['x-cs-variant-uid'] = ','.join(self.variant_uid)
            
            if params is not None:
                self.entry_param.update(params)
            encoded_params = parse.urlencode(self.entry_param)
            endpoint = self.http_instance.endpoint
            url = f'{endpoint}/content_types/{self.content_type_id}/entries/{self.entry_uid}?{encoded_params}'
            self.http_instance.headers.update(headers)
            result = self.http_instance.get(url)
            self.http_instance.headers.pop('x-cs-variant-uid', None)
            return result