"""
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
contentstack.entry
~~~~~~~~~~~~~~~~~~
The Get a single entry request fetches a particular entry of a content type.
API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#entries
"""


# ************* Module stack **************
# Your code has been rated at 9.89/10 by pylint


class Entry:
    """
    An entry is the actual piece of content that you want to publish.
    Entries can be created for one of the available content types.
    In this section, we will understand how to add, edit, publish,
    unpublish, and localize an entry.

    - Before we start working with entries,
    it is important to ensure that the required content types are in place
    """

    def __init__(self, http_instance, content_type_uid, entry_uid):
        self.local_param = {}
        self.except_field = {}
        self.http_instance = http_instance
        self.content_type_id = content_type_uid
        self.entry_uid = entry_uid

        self.__only_dict = {}
        self.__uid_for_except = {}
        self.__except_field = []
        self.__uid_for_only = []

    def locale(self, locale):
        """
        - Locale is optional
        - When no locale is specified, it returns the entry from the master locale
        - Specify a locale to get entry/entries of only a particular locale
          Example: 'en-us'
        :param locale: {str} -- language code
        :return: Entry, so you can chain this call.
        ------------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry.locale('en-us')
            >>> result = entry.fetch()
        ------------------------------
        """
        if locale is None or not isinstance(locale, str):
            raise KeyError('Kindly provide a valid locale')
        self.local_param["locale"] = locale
        return self

    def environment(self, environment):
        """
        Enter the name of the environment of which the entries needs to be included
        Example: production
        :param environment: {str} environment of which the entries needs to be included
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
        if environment is None or not isinstance(environment, str):
            raise KeyError('Kindly provide a valid environment')
        self.local_param['environment'] = environment
        return self

    def version(self, version):
        """
        - Version is optional
        - When no version is specified, it returns the latest version
        - To retrieve a specific version, specify the version number under this parameter.
          In such a case, DO NOT specify any environment.
          Example: 4
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
        self.local_param['version'] = version
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
        self.local_param[key] = value
        return self

    def excepts(self, *field_uid):
        """
        Specifies list of field field_uid that would be excluded from the response.
        :param field_uid: list of field field_uid
        :return: Entry, so you can chain this call.
        ------------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry.excepts(['field_uid1', 'field_uid2', 'field_uid3'])
            >>> result = entry.fetch()
        -------------------------------
        """
        if field_uid is None:
            raise ValueError('Kindly provide a valid argument')
        self.except_field = list(field_uid)
        return self

    def except_with_reference_uid(self, reference_field_uid, *field_uid):
        """
        The except will exclude the data of the specified fields for
        each entry and will include the data of the rest of the fields.
        :param reference_field_uid: {str} -- Key who has reference to some other class object.
        :param field_uid: {str}: field_uid for variable number of arguments
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='asset_uid')
            >>> entry = entry.except_with_reference_uid('reference_field_uid',
                        ["field1", 'field2', 'field3'])
            >>> result = entry.fetch()
        -------------------------------
        """
        if (reference_field_uid, field_uid) is None and not isinstance(reference_field_uid, str):
            raise ValueError('Kindly provide valid arguments')
        self.__uid_for_except[reference_field_uid] = list(field_uid)
        self.include_reference(reference_field_uid)
        return self

    def include_reference(self, *reference_uid):
        """
        If you wish to fetch the content of the entry that is included in the reference field,
        :param reference_uid: reference field of Entry
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.include_reference(['uid1', 'uid2', 'uid3'])
            >>> result = entry.fetch()
        -------------------------------
        """
        if reference_uid is None:
            raise ValueError('Kindly provide a valid argument')
        self.local_param["include[]"] = list(reference_uid)
        return self

    def only(self, *field_uid):
        """
        Specifies an array of only keys in BASE object that would be included in the response.
        :param field_uid: field_uid for variable number of arguments to be included in response.
        field_uid for variable number of arguments
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.only(['field_uid1', 'field_uid2', 'field_uid3'])
            >>> result = entry.fetch()
        -------------------------------
        """
        if field_uid is None:
            raise KeyError('field_uid can not be None')
        for uid in field_uid:
            self.__uid_for_only.append(uid)
        return self

    def only_with_reference_uid(self, reference_field_uid, *field_uid):
        """
        Specifies an array of only keys that would be included in the response.
        :param reference_field_uid: {str} - Key who has reference to some other class object.
        :param field_uid: list of field_uid
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.only_with_reference_uid('reference_uid', ['uid1', 'uid2', 'uid3'])
            >>> result = entry.fetch()
        -------------------------------
        """
        field_value_list = []
        for field in field_uid:
            field_value_list.append(field)
        if reference_field_uid is not None and isinstance(reference_field_uid, str):
            self.__only_dict[reference_field_uid] = field_value_list
            self.include_reference(reference_field_uid)
        return self

    def include_reference_content_type_uid(self):
        """
        This method also includes the content type UIDs
        of the referenced entries returned in the response.
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.include_reference_content_type_uid()
            >>> result = entry.fetch()
        -------------------------------
        """
        self.local_param['include_reference_content_type_uid'] = 'true'
        return self

    def include_content_type(self):
        """
        This method also includes the ContentType in the entry
        :return: Entry, so you can chain this call.
        -------------------------------
        [Example:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.include_content_type()
            >>> result = entry.fetch()
        -------------------------------
        """
        include_content_type = {'include_content_type': 'true',
                                'include_global_field_schema': 'true'}
        self.local_param.update(include_content_type)
        return self

    def __set_include_json(self):
        if self.__uid_for_only is not None and len(self.__uid_for_only) > 0:
            self.local_param["only[BASE][]"] = self.__uid_for_only
            self.__uid_for_only = None
        if self.__except_field is not None and len(self.__except_field) > 0:
            self.local_param["except[BASE][]"] = self.__except_field
            self.__except_field = None
        if self.__uid_for_except is not None and len(self.__uid_for_except) > 0:
            self.local_param["except"] = self.__uid_for_except
            self.__uid_for_except = None
        if self.__only_dict is not None and len(self.__only_dict) > 0:
            self.local_param["only"] = self.__only_dict
            self.__only_dict = None

        return self

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
        if isinstance(self.entry_uid, str):
            self.__set_include_json()
        # self.__local_params, self.__entry_headers
        url = '{}/content_types/{}/entries/{}'.format(self.http_instance.endpoint,
                                                      self.content_type_id, self.entry_uid)
        result = self.http_instance.get(url)
        return result
