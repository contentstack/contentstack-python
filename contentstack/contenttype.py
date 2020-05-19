"""
Content type defines the structure or schema of a page or a section of your web
or mobile property. To create content for your application, you are required
to first create a content type, and then create entries using the
content type.
"""


# ************* Module asset **************
# Your code has been rated at 9.09/10 by pylint


class ContentType:
    """
    Content type defines the structure or schema of a page or a
    section of your web or mobile property. To create
    content for your application, you are required to
    first create a content type, and then create entries using the
    content type.
    """

    def __init__(self, http_instance, content_type_uid):
        self.__http_instance = http_instance
        self.__content_type_uid = content_type_uid

    def entry(self, uid):
        """
        An entry is the actual piece of content created using one of the defined content types.
        :param uid: {str} -- uid of the entry
        :return: Entry -- Returns the Entry class object so we can chain the entry functions
        --------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
        --------------------------------
        """
        from contentstack import Entry
        entry = Entry(self.__http_instance, self.__content_type_uid, entry_uid=uid)
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
        from contentstack.query import Query
        query = Query(self.__content_type_uid)
        return query

    def fetch(self, params=None):
        """
        This method is useful to fetch ContentType of the of the stack.
        :param params: dictionary of params
        :return:dict -- contentType response
        ------------------------------
        Example:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> content_type.add_header('key', 'someheader')
            >>> some_dict = {'abc':'something'}
            >>> response = content_type.fetch(some_dict)
        ------------------------------
        """
        if params is None:
            params = {}
        params_dict = {}
        url = '{}/content_types'.format(self.__http_instance.endpoint)
        content_type_url = '{0}/{1}'.format(url, self.__content_type_uid)
        if params is not None and isinstance(params, dict):
            params_dict.update(params)
        # params_dict, self.__stack_headers
        result = self.__http_instance.get(content_type_url)
        return result
