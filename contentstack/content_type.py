"""
ContentType
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""


class ContentType:

    """
    Content type defines the structure or schema of a page or a section of your web or mobile property. To create
    content for your application, you are required to first create a content type, and then create entries using the
    content type.
    Read more about Content Types[https://www.contentstack.com/docs/guide/content-types].
    """

    def __init__(self, content_type_uid: str):

        """
        :param content_type_uid: This is the uid of the content_type
        :type content_type_uid: str
        ==============================
        [Example:]
        >>> content_type: ContentType = stack.content_type('product')
        ==============================
        """

        self.__config = None
        self.__stack_instance = None
        self.__http_request = None
        self.__stack_headers = {}
        if content_type_uid is not None and isinstance(content_type_uid, str):
            self.__content_type_uid = content_type_uid
        else:
            raise ValueError('Kindly Provide ContentType')

    def _instance(self, stack_instance):

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

        """
        List of headers, used to verify stack (these are stack credentials)
        :return: stack_headers
        :rtype: dict
        ==============================
        [Example:]
        >>> content_type:ContentType = stack.content_type('product')
        >>> headers: dict = content_type.add_header
        ==============================
        """

        return self.__stack_headers

    def add_header(self, key, value):

        """
        This method used to add key value pair to the stack headers
        :param key: key of the header
        :type key: str
        :param value: value against of the key
        :type value: str
        :return: self
        :rtype: ContentType
        ==============================
        [Example:]
        >>> content_type: ContentType = stack.content_type('product')
        >>> content_type.add_header('api_key', 'bltsomething')
        ==============================
        """

        if key is not None and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self.__stack_headers[key] = value
            else:
                raise ValueError('Kindly provide a valid key')
        else:
            raise ValueError('Kindly provide a valid key value pair')

        return self

    def remove_header(self, key):

        """
        It Deletes the header against specified key
        :param key: The key of the header has to delete
        :type key: str
        :return: self
        :rtype: ContentType
        ==============================
        [Example:]
        >>> content_type: ContentType =  stack.content_type('product')
        >>> content_type.remove_header('api_key')
        ==============================
        """

        if key is not None and isinstance(key, str):
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)
            else:
                raise ValueError('Key provide by you, does not exits')
        else:
            raise ValueError('Kindly provide a valid key')

        return self

    def entry(self, uid):

        """
        An entry is the actual piece of content created using one of the defined content types.
        Read more about Entries. [ https://www.contentstack.com/docs/apis/content-delivery-api/#entries ]
        :param uid: This is the uid of entry
        :type uid: str
        :return: entry
        :rtype: <content_type.Entry>

        ==============================
        [Example:]
        >>> content_type ContentType = stack.content_type('product')
        >>> entry = content_type.entry('blt87409832174')
        ==============================
        """

        from contentstack import Entry
        if self.__http_request is None:
            raise ValueError("Invalid HTTP Request")
        entry: Entry = Entry(content_type_id=self.__content_type_uid)
        entry._instance(self.__stack_instance)
        if uid is not None:
            if isinstance(uid, str):
                entry.set_uid(uid)
            else:
                raise ValueError('Kindly provide valid entry uid')
        return entry

    def query(self):

        """
        You can add queries to extend the functionality of this API call.
        Under the URI Parameters section, insert a parameter named query
        and provide a query in JSON format as the value. To learn more about the queries, refer to the Queries section.
        :return: Query

        ==============================
        [Example:]
        >>> content_type ContentType = stack.content_type('product')
        >>> query = content_type.query()
        ==============================
        """

        from contentstack.query import Query
        query = Query(self.__content_type_uid)
        query._instance(self.__stack_instance)
        return query

    def fetch(self):

        """
        This method is useful to fetch ContentType of the of the stack.
        :return: response returns Json
        :rtype: ContentType
        """
        endpoint = self.__config.endpoint
        url = '{}/content_types'.format(endpoint)
        content_type_url = '{0}/{1}'.format(url, self.__content_type_uid)
        result = self.__http_request.get_result(content_type_url, {}, self.__stack_headers)
        return result
