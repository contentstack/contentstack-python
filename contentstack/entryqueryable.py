import enum


class Include(enum.Enum):
    """
    Include is enum that Provides Options to perform operation to query the result.

    Available Options for QueryOperation are below.
    DEFAULT, ONLY, EXCEPT

    Arguments:
        enum {Include} -- Type of IncludeReference
    """
    EXCEPT = 'except'
    ONLY = 'only'
    DEFAULT = ''


class EntryQueryable:
    """
    This class is base class for the Entry and Query class that shares common functions
    """
    def __init__(self):
        self.entry_queryable_param = {}

    def locale(self, locale: str):
        """
        Language code of which the entries needs to be included.
        Only the entries published in this locale will be displayed

        Arguments:
            locale {str} -- locale_code of the language of which the entries needs to be included.
            Only the entries published in this locale will be displayed

        :return: self: so you can chain this call.

        Example (locale for Entry):
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry(uid='entry_uid')
            >>> entry.locale('en-us')
            >>> result = entry.fetch()

        Example (locale for Query):
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query.locale('en-us')
            >>> result = query.find()
        """
        self.entry_queryable_param['locale'] = locale
        return self

    def only(self, field_uid):
        """
        Specifies an array of only keys in BASE object that would be included in the response.
        It refers to the top-level fields of the schema
        :param field_uid: Array of the only reference keys to be included in response
        Returns:
            self -- so you can chain this call.
        """
        if field_uid is not None:
            self.entry_queryable_param['only[BASE][]'] = field_uid
            return self

    def excepts(self, field_uid):
        """
        Specifies list of field_uid that would be excluded from the response.
        It refers to the top-level fields of the schema
        :param field_uid: to be excluded from the response.
        :return: self -- so you can chain this call.
        """
        if field_uid is not None:
            self.entry_queryable_param['except[BASE][]'] = field_uid
            return self

    def include_reference(self, include_reference_type:  Include, reference_field_uid: str, field_uid=None):
        """
        **Include Reference:**
        When you fetch an entry of a content type that has a reference field,
        by default, the content of the referred entry is not fetched.
        It only fetches the UID of the referred entry, along with the content of
        the specified entry.

        Arguments:
        reference_field_uid {str} -- Key who has reference to some other class object.
        Array of the only reference keys to be included in response
        include_type {Include} -- Provides three options, none, only and except
        i.e accepts list of field_uid
        field_uid {list} -- list of field_uid on which include operation to perform

        Returns:
            self -- So you can chain this call.
        """
        container = {}
        if reference_field_uid is None:
            raise KeyError("reference_field_uid can't be None")
        if include_reference_type.name == 'DEFAULT':
            self.entry_queryable_param["include[]"] = reference_field_uid
        else:
            container[reference_field_uid] = field_uid
            self.entry_queryable_param["include[]"] = {include_reference_type.value: container}
        return self

    def include_content_type(self):
        """
        This method also includes the ContentType in the entry
        :return: self: so you can chain this call.

        -------------------------------

        [Example: for Entry]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.include_content_type()
            >>> result = entry.fetch()

        -------------------------------

        [Example: for Query:]

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query.include_content_type()
            >>> result = query.find()
        -------------------------------
        """
        self.entry_queryable_param['include_content_type'] = 'true'
        self.entry_queryable_param['include_global_field_schema'] = 'true'
        return self

    def include_reference_content_type_uid(self):
        """
        This method also includes the content type UIDs
        of the referenced entries returned in the response
        Returns:
            :return: self: so you can chain this call.

        [Example for Query]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.include_reference_content_type_uid()
            >>> result = query.find()

        [Example for Entry]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> entry = stack.content_type('content_type_uid').entry('entry_uid')
            >>> entry = entry.include_reference_content_type_uid()
            >>> result = entry.fetch()
        """
        self.entry_queryable_param['include_reference_content_type_uid'] = 'true'
        return self

    def add_param(self, key: str, value: str):
        """
        This method adds key and value to an Entry.
        :param key: The key as string which needs to be added to an Entry
        :param value: The value as string which needs to be added to an Entry
        :return: self: object, so you can chain this call.

        Example: Call from Query =>
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> query = stack.content_type('content_type_uid').query()
            >>> query = query.include_reference_content_type_uid()
            >>> result = query.find()

        Example: Call from Entry =>
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> entry = stack.content_type('content_type_uid').entry('entry_uid')
            >>> entry = entry.include_reference_content_type_uid()
            >>> result = entry.fetch()

        """
        if None not in (key, value):
            self.entry_queryable_param[key] = value
