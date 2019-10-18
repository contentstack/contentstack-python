
"""

Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

contentstack.content_type
~~~~~~~~~~~~~~~~~~

API Reference: https://www.contentstack.com/docs/guide/content-types

"""


class ContentType:

    """Content type defines the structure or schema of a page or a section of your web or mobile property. To create
    content for your application, you are required to first create a content type, and then create entries using the
    content type.

    Read more about Content Types[https://www.contentstack.com/docs/guide/content-types].

    """

    def __init__(self, content_type_uid: str):

        """

        Arguments:
            content_type_uid {str} -- [This is the uid of the content_type]
        
        Raises:
            ValueError: [description]

        ==============================
        
        [Example:]
        
            >>> from stack import Stack
            >>> content_type = Stack.content_type('product')
        
        ==============================

        """

        self.__config = None
        self.__stack_instance = None
        self.__http_request = None
        self.__stack_headers = {}

        if content_type_uid is not None:
            raise KeyError('content_type_uid can not be None')
        elif isinstance(content_type_uid, str):
            self.__content_type_uid = content_type_uid
        else:
            raise ValueError('content_type_uid should be str type')

    def _instance(self, stack_instance):
        # _instance is the protected member of the asset, So outsiders can not access this file.
        from contentstack.stack import Stack
        from contentstack.errors import StackException
        
        if stack_instance is None:
            raise StackException('Kindly initialise stack first')
        self.__stack_instance: Stack = stack_instance
        self.__config = self.__stack_instance.config
        self.__stack_headers.update(self.__stack_instance.headers)
        self.__http_request = self.__stack_instance.get_http_instance


    @property
    def header(self):

        """header property is useful to get header of the the content_type
        
        Returns:
            dict -- It returns stack_headers

        ==============================
        
        [Example:]

            >>> content_type = stack.content_type('product')
            >>> content_type.header
        
        ==============================

        """

        return self.__stack_headers

    def add_header(self, key, value):

        """
        Adds header in content_type as key value pair
        
        Arguments:
            key {str} -- key of the header
            value {object} -- value of the respected key in header
        
        Raises:
            KeyError: key and value should not be None
            KeyError: key and value both should be str type
        
        Returns:
            ContentType -- ContentType, So we can chain the call

        ==============================
        
        [Example:]

            >>> content_type.add_header('key', 'value')
        
        ==============================
        """
        if None in (key, value):
            raise KeyError('Kindly provide a valid key and value')
        elif isinstance(key, str) and isinstance(value, str):
                self.__stack_headers[key] = value
        else:
            raise KeyError('Key and value should be str type')

        return self

    def remove_header(self, key):

        """It deletes the header against specified key
        
        Arguments:
            key {str} -- existing key that has to delete from header
    
        Raises:
            KeyError: If Key is None, Empty or not str type
        
        Returns:
            ContentType -- ContentType class object so we can chain more functions
        
        ==============================
        
        [Example:]

            >>> content_type.remove_header('key')
        
        ==============================

        """

        if key is None:
            raise KeyError('key should not be None')
        elif isinstance(key, str):
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)

        return self

    def entry(self, uid):

        """An entry is the actual piece of content created using one of the defined content types.
        
        Read more about Entries. 
        [https://www.contentstack.com/docs/apis/content-delivery-api/#entries]

        Arguments:
            uid {str} -- uid of the entry
        
        Raises:
            EnvironmentError: http instance is not found (invalid http request)
            KeyError: entru uid should be str type
        
        Returns:
            Entry -- Returns the Entry class object so we can chain the entry functions

        ==============================
        
        [Example:]

            >>> entry: Entry = content_type.entry('uid')
        
        ==============================

        """

        from contentstack import Entry
        if self.__http_request is None:
            raise EnvironmentError("Invalid http request")
        entry: Entry = Entry(content_type_id=self.__content_type_uid)
        entry._instance(self.__stack_instance)
        if uid is not None:
            if isinstance(uid, str):
                entry.set_uid(uid)
            else:
                raise KeyError('entry uid should be str type')
        return entry

    def query(self):

        """
        It returns query class object so we can query on entry of specified ContentType
        
        Returns:
            Query -- query object instance, so we can chain the query functions to it.
        
        ==============================
        
        [Example:]

            >>> query: Query = content_type.Query
        
        ==============================

        """

        from contentstack.query import Query
        query = Query(self.__content_type_uid)
        query._instance(self.__stack_instance)
        return query

    def fetch(self):

        """This method is useful to fetch ContentType of the of the stack.
        :return: response returns Json
        :rtype: ContentType
        
        Returns:
            dict -- Returns dictionary response
        
        ==============================

        Example:
            >>> content_type.add_header('key', 'someheader')
            >>> response = content_type.fetch()

        ==============================

        """
        endpoint = self.__config.endpoint
        url = '{}/content_types'.format(endpoint)
        content_type_url = '{0}/{1}'.format(url, self.__content_type_uid)
        result = self.__http_request.get_result(content_type_url, {}, self.__stack_headers)
        return result
