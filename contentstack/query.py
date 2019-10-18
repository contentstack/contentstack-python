
"""

Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

contentstack.query
~~~~~~~~~~~~~~~~~~

API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#queries

"""


class Query(object):

    """
    Contentstack provides certain queries that you can use to fetch filtered results.
    You can use queries for Entries and Assets API requests.

    [API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#queries]

    """

    def __init__(self, content_type_uid):

        self.__config = None
        self.__query_url = None
        self.__stack_instance = None
        self.__http_request = None

        self.__uid_include = []
        self.__uid_except = []
        self.__uid_only = []

        self.__headers = {}
        self.__query_params = {}
        self.__query_value = {}
        self.__only_json = {}
        self.__query_dict = {}
        self.__except_Json = {}
        self.__main_json = {}

        if content_type_uid is None or len(content_type_uid.strip()) == 0:
            raise ValueError('Kindly provide content_type_uid as URI Parameters')
        if isinstance(content_type_uid, str):
            self.__content_type_id = content_type_uid

    def _instance(self, stack_instance):

        # _instance is protected and it is not accessible out side of package.
        self.__stack_instance = stack_instance
        self.__config = self.__stack_instance.config
        endpoint = self.__config.endpoint
        self.__query_url = '{}/content_types/{}/entries'.format(endpoint, self.__content_type_id)
        self.__http_request = self.__stack_instance.get_http_instance

        return self

    @property
    def content_type(self):

        """It returns the content type of the entry.
        
        Returns:
            str -- It returns the content type of the entry.

        ==============================

        [Example]:
            >>> from stack import Stack
            >>> query = stack.content_type('product').query()
            >>> content_type = query.content_type

        ==============================

        """

        return self.__content_type_id

    @content_type.setter
    def content_type(self, content_type_id):

        """The unique ID of the content type of which you wish to retrieve the details. 
        The uid is generated based on the title of the content type and it is unique across a stack

        Arguments:
            content_type_id {str} -- unique ID of the content type of which you wish to retrieve information
        
        Raises:
            ValueError: If content_type_id is None
            ValueError: If content_type_id is not str type

        ==============================

        [Example]:
            >>> query = stack.content_type('product').query()
            >>> query.content_type = 'content_type_id'

        ==============================

        """

        if content_type_id is None or len(content_type_id.strip()) == 0:
            raise ValueError('Kindly provide valid content_type_id')
        if isinstance(content_type_id, str):
            self.__content_type_id = content_type_id
        else:
            raise ValueError('content_type_id should be str')

    @property
    def headers(self):

        """Additional header dict for Query.
        
        Returns:
            dict -- additional header dict for Query
        
        ==============================

        [Example]:
            >>> query = stack.content_type('product').query() 
            >>> query = query.headers

        ==============================

        """

        return self.__headers

    def remove_header(self, key):

        """It removes header from the Query headers by key.
        
        Raises:
            ValueError: If key is None or empty
        
        Returns:
            Query -- Query, so you can chain this call.

        ==============================

        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> query = query.remove_header('key')
            >>> result = query.find()

        ==============================

        """

        if key is None or len(key.strip()) == 0:
            raise ValueError('Kindly provide valid header key')
        if isinstance(key, str) and key in self.__headers:
            self.__headers.pop(key, None)

        return self

    def add_header(self, key, value):

        """It adds header in the Query headers by key and value.
        
        Arguments:
            key {str} -- header's key
            value {object} -- value of the respective key

        Raises:
            ValueError: If key or value will be None
            ValueError: If type of key should be str
        
        Returns:
            Query -- Query, so you can chain this call.

        ==============================

        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> query = query.add_header('key', value)
            >>> result = query.find()

        ==============================
        """

        if key and value is None:
            raise ValueError('Kindly provide valid header key and value')
        if isinstance(key, str):
            self.__headers[key] = value
        else:
            raise ValueError('Kindly provide a valid arguments')

        return self

    def locale(self, locale):

        """Enter the language code of which the entries needs to be included.
        Only the entries published in this locale will be displayed.
        
        Arguments:
            locale {str} -- locale is langauge code

        Raises:
            ValueError: If locale is None
            ValueError: If locale is not type of str
        
        Returns:
            Query -- Query, so you can chain this call.

        ==============================

        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> query = query.locale('en-us')
            >>> result = query.find()

        ==============================

        """

        if locale is None:
            raise ValueError('Kindly provide a valid locale-code')
        if isinstance(locale, str):
            self.__query_params['locale'] = locale
        else:
            raise ValueError('locale-code should be str')

        return self

    def where(self, key, value):

        """Add a constraint to fetch all entries that contains given value against specified  key
        
        Arguments:
            key {str} -- The key to be constrained.
            value {object} -- field value which get included from the response.
        
        Raises:
            ValueError: If key or value is None
            ValueError: If key type is not str
        
        Returns:
            Query -- Query, so you can chain this call
        
        ==============================

        [Example]:

            >>> query = stack.content_type('product').query()
            >>> query = query.where("uid", "bltsomething123")
            >>> result = query.find()

        ==============================

        """

        if None in (key, value):
            raise ValueError('Kindly provide a valid key and value')
        if isinstance(key, str):
            self.__query_dict[key] = value
        else:
            raise ValueError('key and value should be str')

        return self

    def add_query(self, key, value):

        """Add a custom query against specified key.
        
        Arguments:
            key {str} -- key of query param
            value {str} -- value of the query
    
        
        Raises:
            ValueError: If key or value is None
            ValueError: if the type of key is not str 
        
        Returns:
            Query -- Query object, so you can chain this call

        ==============================

        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> query = query.add_query("query_param_key", "query_param_value")
            >>> result = query.find()

        ==============================
        
        """

        if key and value is None:
            raise ValueError('Kindly provide a valid key and value')
        if isinstance(key, str):
            self.__query_params[key] = value
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def remove_query(self, key):
        
        """
        Remove provided query key from custom query if exist.
        
        Arguments:
            key {str} -- The key to be constrained.
        
        Raises:
            ValueError: If key is None
        
        Returns:
            Query -- Query object, so you can chain this call.

        ==============================

        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> query = query.remove_query("query_key")
            >>> result = query.find()

        ==============================

        """
        if key is None:
            raise ValueError('Kindly provide valid key')
        if key in self.__query_params and isinstance(key, str):
            self.__query_params.pop(key, None)
        return self

    def and_query(self, *query_objects):

        """
        Get entries that satisfy all the conditions provided in the '$and' query.
        
        Arguments:
            query_objects {object} -- query_objects for variable number of arguments of type Query Object.
        
        Raises:
            ValueError: If query_objects is None
        
        Returns:
            Query -- Query object, so you can chain this call.

        ==============================

        [Example]: 
        
        Let’s say you want to retrieve entries in which the Title field is set to 'Redmi Note 3' and the Color
        field is 'Gold'. The query to be used for such a case would be:
        The response will contain the entries where the values for Title is 'Redmi Note 3' and Color is 'Gold'
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#and-operator]

            >>> query = stack.content_type('product').query() 
            >>> query1 = query.where("title", "Redmi Note 3")
            >>> query2 = query.where("color", "Gold")
            >>> query.and_query(query1, query2)
            >>> result = query.find()

        ==============================

        """

        if query_objects is None:
            raise ValueError('Kindly provide a valid KEYs')
        if len(query_objects) > 0:
            query_list = []
            for query in query_objects:
                query_list.append(query.__query_dict)
            self.__query_dict["$and"] = query_list

        return self

    def or_query(self, *query_objects):

        """
        Get all entries that satisfy at least one of the given conditions provided in the '$or' query.
        
        Arguments:
            query_objects {object} -- query_objects for variable number of arguments of type Query Object.

        Raises:
            ValueError: If query_objects is None
        
        Returns:
            Query -- Query object, so you can chain this call.

        ==============================

        [Example]: 
        
        Let’s say you want to retrieve entries in which either the value for the
        Color field is 'Gold' or 'Black'. The query to be used for such a case would be:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#or-operator]

            >>> query  = stack.content_type('product').query() 
            >>> query1 = query.where("color", "Black")
            >>> query2 = query.where("price", "price_in_usd")
            >>> query.or_query(query1, query2)
            >>> result = query.find()

        ==============================

        """

        if query_objects is None:
            raise ValueError('Kindly provide a valid KEYs')
        query_list: list = []
        for query in query_objects:
            query_list.append(query.__query_dict)
        self.__query_dict["$or"] = query_list

        return self

    def less_than(self, key, value):

        """
        Get entries in which the value of a field is lesser than the value provided in the condition.
        
        Arguments:
            key {str} -- The key to be constrained
            value {object} -- value The value that must be less than.
                
        Raises:
            ValueError: If key or value is None
            ValueError: If type of key is not str
        
        Returns:
            Query -- Query object, so you can chain this call.

        ==============================

        [Example]: 
        
        Let’s say you want to retrieve all the entries that have value of the 
        Price in USD field set to a value that is less than but not equal to 600. 
        You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#less-than]

            >>> query = stack.content_type('product').query() 
            >>> query = query.less_than('price_in_usd', 600)
            >>> result = query.find()

        ==============================
        """

        if key and value is None:
            raise ValueError('Kindly provide valid key and value')
        self.__query_value["$lt"] = value
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def less_than_or_equal_to(self, key, value):
        
        """
        Get entries in which the value of a field is lesser than or equal to the value
        provided in the condition.
        
        Arguments:
            key {str} -- The key to be constrained
            value {object} -- value The value that must be equalled.
        
        Raises:
            ValueError: If key or value is None
            ValueError: If key is not str type
        
        Returns:
            Query -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        Let’s say you want to retrieve all the entries that have value of the Price in USD field
        set to a value that is less than or equal to 146. To achieve this, send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#less-than-or-equal-to]

            >>> query = stack.content_type('product').query() 
            >>> query = query.less_than_or_equal_to('price_in_usd', 146)
            >>> result = query.find()

        ==============================

        """
        if key and value is None:
            raise ValueError('Kindly provide valid key and value')
        self.__query_value["$lte"] = value
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def greater_than(self, key, value):

        """
        Add a constraint to the query that requires a particular key entry to be greater than the provided value
    
        Arguments:
            key {str} -- The key to be constrained.
            value {object} -- value The value that provides an lower bound
                
        Raises:
            ValueError: If key or value is None
            ValueError: If key is not str type
        
        Returns:
            Query -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        Let’s say you want to retrieve all the entries that have value of the Price in USD field set to a value
        that is greater than but not equal to 146. You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#greater-than]

            >>> query = stack.content_type('product').query() 
            >>> query = query.greater_than('price_in_usd', 146)
            >>> result = query.find()

        ==============================
        """

        if key and value is None:
            raise ValueError('Kindly provide valid key and value')
        self.__query_value["$gt"] = value
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def greater_than_or_equal_to(self, key, value):

        """Add a constraint to the query that requires a particular key entry to be greater than or equal to
        the provided value.

        Arguments:
            key {str} -- The key to be constrained.
            value {object} -- value The value that provides an lower bound.
        
        Raises:
            ValueError: If key or value is None
            ValueError: If key is not str type
        
        Returns:
            Query -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        Let’s say you want to retrieve all the entries that have value of the Price in USD field set to a value
        that is greater than or equal to 146. You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#greater-than-or-equal-to]

            >>> query = stack.content_type('product').query() 
            >>> query = query.greater_than_or_equal_to('price_in_usd', 146)
            >>> result = query.find()

        ==============================

        """

        if key and value is None:
            raise ValueError('Kindly provide valid key and value')
        self.__query_value["$gte"] = value
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def not_equal_to(self, key, value):

        """
        Add a constraint to the query that requires a particular key's
        entry to be not equal to the provided value.
        
        Arguments:
            key {str} -- The key to be constrained.
            value {object} -- The object that must not be equaled.
        
        Raises:
            ValueError: If key or value is None
            ValueError: If key is not str type
        
        Returns:
            Query -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        In the Product content type, you have a field named Price in USD. Now,
        you need to retrieve all entries where the value of this field not equal to '146'
        for this field. The parameter can be used as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#not-equals-operator]

            >>> query = stack.content_type('product').query() 
            >>> query = query.not_equal_to('price_in_usd', 146)
            >>> result = query.find()

        ==============================
        """

        if key and value is None:
            raise ValueError('Kindly provide valid key and value')
        self.__query_value["$ne"] = value
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def contained_in(self, key, *contained_in):
        
        """
        Add a constraint to the query that requires a particular key&#39;s entry to be contained
        in the provided array.
        
        Arguments:
            key {str} -- The key to be constrained.
            contained_in -- The possible values for the key's object
    
        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        In the Product content type, you have a field named Price in USD. Now,
        you need to retrieve all the entries where value of this field is one among the given set of values.
        The query fired using the '$in' parameter is given below:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#array-equals-operator]

            >>> query = stack.content_type('product').query()
            >>> query = query.contained_in('price_in_usd', 101, 749)
            >>> result = query.find()

        ==============================

        """

        if key is None:
            raise ValueError('Kindly provide valid key')
        self.__query_value["$in"] = list(contained_in)
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def not_contained_in(self, key, *not_contained_in):

        """Get all entries in which the value of a field does not match to any of the given values.
        This parameter will compare field values of entries to that of the values provided in the condition,
        and the query will retrieve entries that have field values that does not match to any of the values provided.
        
        Arguments:
            key {str} -- The key to be constrained.
            not_contained_in -- The possible values for the key's object

        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        In the Product content type, you have a field named Price in USD. Now, you need to retrieve the entries
        where the field value does not fall in the given set. You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#array-not-equals-operator]

            >>> query = stack.content_type('product').query()
            >>> query = query.not_contained_in('price_in_usd', 101, 749)
            >>> result = query.find()

        ==============================

        """

        if key is None:
            raise ValueError('Kindly provide valid key')
        self.__query_value["$nin"] = list(not_contained_in)
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def exists(self, key):

        """
        Get entries if value of the field, mentioned in the condition, exists.

        Arguments:
            key {str} -- The key to be constrained.
        
        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        Example:
        
        In the Product content type, we have a field named Price in USD. Now, you want to retrieve all the entries in
        the content type in which the field exists
        for more: https://www.contentstack.com/docs/apis/content-delivery-api/#exists

            >>> query = stack.content_type('product').query()
            >>> query = query.exists('price_in_usd')
            >>> result = query.find()

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide valid key')
        self.__query_value["$exists"] = True
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def not_exists(self, key):

        """
        Add a constraint that requires, a specified key does not exists in response.

        Arguments:
            key {str} -- The key to be constrained.
        
        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        Example:
        
        In the Product content type, we have a field named Price in USD. Now, you want 
        to retrieve all the entries in the content type in which the field does not exists

        for more: https://www.contentstack.com/docs/apis/content-delivery-api/#not_exists

            >>> query = stack.content_type('product').query()
            >>> query = query.not_exists('price_in_usd')
            >>> result = query.find()

        ==============================

        """

        if key is None:
            raise ValueError('Kindly provide valid key')
        self.__query_value["$exists"] = False
        if isinstance(key, str):
            self.__query_dict[key] = self.__query_value
        else:
            raise ValueError('key should be str type')

        return self

    def include_reference(self, key):

        """
        When you fetch an entry of a content type that has a reference field, by default,
        the content of the referred entry is not fetched. It only fetches the UID of the referred entry,
        
        Arguments:
            key {str} -- The key to be constrained.

        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        Example: 
        
        If you wish to fetch the content of the entry that is included in the
        reference field, you need to use the include[] parameter, and specify the UID of the reference field as
        value. This informs Contentstack that the request also includes fetching the entry used in the specified
        reference field
        for more: https://www.contentstack.com/docs/apis/content-delivery-api/#include-reference

            >>> query = stack.content_type('product').query() 
            >>> query = query.include_reference('categories')
            >>> result = query.find()

        ==============================

       """

        if key is None:
            raise ValueError('Kindly provide valid key')
        if isinstance(key, str):
            self.__uid_include.append(key)
        else:
            raise ValueError('key should be str type')

        return self

    def tags(self, *tags):

        """
        Include tags with which to search entries.

        Arguments:
            tags {object} -- tags Comma separated objects with which to search entries.
        
        Raises:
            ValueError: If key is None
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        Example:

            >>> query = stack.content_type('product').query() 
            >>> query = query.tags('black', 'gold', 'silver')
            >>> result = query.find()

        ==============================
        """

        if tags is None:
            raise ValueError('Kindly provide valid key')
        tag_string = ",".join(tags)
        self.__query_params["tags"] = tag_string

        return self

    def ascending(self, key):

        """
        When fetching entries, you can sort them in the ascending order with respect to the value of a specific field
        in the response body.

        Arguments:
            key {str} -- The key to order by.
        
        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        Example: 
        
        In the Product content type, if you wish to sort the entries with respect to their prices,
        the parameter can be used as:

            >>> query = stack.content_type('product').query() 
            >>> query = query.ascending('price_in_usd')
            >>> result = query.find()

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide valid key')
        elif isinstance(key, str):
            self.__query_params["asc"] = key
        else:
            raise ValueError('key type should be str')

        return self

    def descending(self, key):

        """When fetching entries, you can sort them in the descending order with respect to the value of a
        specific field in the response body.
        
        Arguments:
            key {str} -- The key to order by
        
        Raises:
            ValueError: If key is None
            ValueError: key should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        Example: 
        
        In the Product content type, if you wish to sort the entries
        with respect to their prices, the parameter can be used as:

            >>> query = stack.content_type('product').query() 
            >>> query = query.descending('price_in_usd')
            >>> result = query.find()

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide valid key')
        elif isinstance(key, str):
            self.__query_params["desc"] = key
        else:
            raise ValueError('Kindly provide str type key')

        return self

    def except_field_uid(self, *field_uid):

        """
        Specifies list of field uids that would be excluded from the response.
        
        Arguments:
            *field_uid {object} -- comma separated uid objects which get excluded from the response.
        
        Raises:
            ValueError: If field_uid is None
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        Example: 
        
        In the Product content type, if you wish to sort the entries
        with respect to their prices, the parameter can be used as:

            >>> query = stack.content_type('product').query() 
            >>> except_field = query.except_field_uid('field_uid1', 'field_uid2')
            >>> result = query.find()

        ==============================

        """

        if field_uid is None:
            raise ValueError('Kindly provide valid field_uid')
        if len(field_uid) > 0:
            for uid in field_uid:
                self.__uid_except.append(uid)

        return self

    def only(self, *field_uid):

        """Specifies an list of field_uid keys in BASE object that would be included in the response.

        Arguments:
            *field_uid {object} -- comma seprated objects of the only reference keys to be included in response.

        Raises:
            ValueError: If field_uid is None
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        Example: 
        
        In the Product content type, if you wish to sort the entries
        with respect to their prices, the parameter can be used as:

            >>> query = stack.content_type('product').query() 
            >>> query = query.only('price_in_usd', 'color')
            >>> result = query.find()

        ==============================

        """

        if field_uid is None:
            raise ValueError('Kindly provide valid field_uid')
        if len(field_uid) > 0:
            for uid in field_uid:
                self.__uid_only.append(uid)

        return self

    def only_with_reference_uid(self, reference_field_uid, *field_uid):
        
        """Specifies an array of only keys that would be included in the response.
        
        Arguments:
            reference_field_uid {[str]} -- reference_field_uid Key who has reference to some other class object.
            *field_uid {object} -- comma separated uid objects which get excluded from the response.
        
        Raises:
            ValueError: If reference_field_uid is None
            ValueError: reference_field_uid should be str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> query = stack.content_type('product').query() 
            >>> query = query.only_with_reference_uid('reference_field_uid', 'field_uid 1', 'field_uid 2')
            >>> result = query.find()

        ==============================
        """

        if field_uid and reference_field_uid is None:
            raise ValueError('Kindly provide valid fields')
        if isinstance(reference_field_uid, str):
            self.__only_json[reference_field_uid] = list(field_uid)
            self.__uid_include.append(reference_field_uid)
        else:
            raise ValueError('reference_field_uid should be str type')

        return self

    def except_with_reference_uid(self, reference_field_uid, *field_uid):

        """Specifies an array of except keys that would be excluded in the response.
        
        Arguments:
            reference_field_uid {str} -- who has reference to some other class object
            *field_uid {object} -- comma separated uid objects which get excluded from the response.

        Raises:
            ValueError: If reference_field_uid is None or not str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> query = stack.content_type('product').query() 
            >>> query = query.except_with_reference_uid('price_in_usd', 'field_uid 1', 'field_uid 2')
            >>> result = query.find()

        ==============================
        """

        field_value_container = []
        for field in field_uid:
            field_value_container.append(field)
        if reference_field_uid is not None and isinstance(reference_field_uid, str):
            self.__except_Json[reference_field_uid] = field_value_container
            self.__uid_except.append(reference_field_uid)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def include_count(self):

        """Retrieve count and data of objects in result    
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> query = stack.content_type('product').query() 
            >>> query = query.include_count()
            >>> result = query.find()

        ==============================

        """

        self.__query_params["include_count"] = 'true'

        return self

    def include_content_type(self):

        """
        Include Content Type of all returned objects along with objects themselves.
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> query = stack.content_type('product').query() 
            >>> query = query.include_content_type()
            >>> result = query.find()

        ==============================
        """

        self.__query_params["include_content_type"] = 'true'

        return self

    def skip(self, number):
        
        """[summary]
        
        Arguments:
            number {int} -- The number of objects to skip
        
        
        Raises:
            ValueError: If number is None
            ValueError: If type of number is not int
        
        Returns:
            Query -- Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> query = stack.content_type('product').query() 
            >>> query = query.skip(3)
            >>> result = query.find()

        ==============================
        
        """

        if number is None:
            raise ValueError('Kindly provide valid number')
        elif isinstance(number, int):
            self.__query_params["skip"] = number
        else:
            raise ValueError('number should be int type')

        return self

    def limit(self, number):

        """
        Arguments:
            number {int} -- number of objects to limit
        
        Raises:
            ValueError: If number is None
            ValueError: If number is not int type
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================
        
        [Example]

            >>> query = stack.content_type('product').query() 
            >>> query = query.limit(3)
            >>> result = query.find()

        ==============================

        """

        if number is None:
            raise ValueError('Kindly provide valid number')
        elif isinstance(number, int):
            self.__query_params["limit"] = number
        else:
            raise ValueError('number should be int type')

        return self

    def regex(self, key, regex, modifiers=None):

        """
        Add a regular expression constraint for finding string values that match the provided 
        regular expression. This may be slow for large data sets.
        
        Arguments:
            key {str} -- The key to be constrained.
            regex {str} -- The regular expression pattern to match
            modifiers {str} -- (optional) modifiers Any of the following supported Regular expression modifiers.
            
            <p>use <b> i </b> for case-insensitive matching.</p>
            <p>use <b> m </b> for making dot match newlines.</p>
            <p>use <b> x </b> for ignoring whitespace in regex</p>
        
        Keyword Arguments:
            modifiers {[type]} -- [description] (default: {None})
        
        Raises:
            ValueError: If key, regex is None
        
        Returns:
            [Query] -- Query object, so you can chain this call
        
        ==============================
        
        [Example:]

            >>> query = stack.content_type('product').query() 
            >>> query = query.regex("name", "browser")
            >>> result = query.find()

        ==============================

        """
        if None in (key, regex):
            raise ValueError('Kindly provide valid key and regex params')
        elif isinstance(key, str) and isinstance(regex, str):
            self.__query_value.clear()
            self.__query_value["$regex"] = regex
            if modifiers is not None and isinstance(modifiers, str):
                self.__query_value["$options"] = modifiers
            self.__query_dict[key] = self.__query_value

        return self

    def search(self, value):

        """
        This method provides only the entries matching the specified value.
        
        Arguments:
            value {str} -- value used to match or compare    
        
        Raises:
            ValueError: If value is None
            ValueError: If type od value is not str
        
        Returns:
            [Query] -- Query object, so you can chain this call.

        ==============================
        
        [Example]

            >>> query = stack.content_type('product').query() 
            >>> query = query.search("search_keyword")
            >>> result = query.find()
        
        ==============================

        """
        if value is None:
            raise ValueError('Kindly provide a valid value')
        elif isinstance(value, str):
            self.__query_params["typeahead"] = value
        else:
            raise ValueError('value should be str type')

        return self

    def param(self, key, value):

        """
        This method adds key and value to an Entry.
        
        Arguments:
            key {str} -- The key as string which needs to be added to the Query
            value {object} -- The value as string which needs to be added to the Query

        Raises:
            ValueError: If key and value is None
            ValueError: If key is not str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.

        ==============================
        
        [Example]

            >>> query = stack.content_type('product').query() 
            >>> query = query.param("key", "value")
            >>> result = query.find()
        
        ==============================

        """
        if None in (key, value):
            raise ValueError('Kindly provide valid key and value')
        elif isinstance(key, str):
            self.__query_params[key] = value
        else:
            raise ValueError('key and value should be str type')

        return self

    def include_reference_content_type_uid(self):

        """
        This method also includes the content type UIDs of the referenced entries returned in the response
        
        Returns:
            [Query] -- Query object, so you can chain this call.
        
        ==============================

        [Example]

            >>> query = stack.content_type('product').query() 
            >>> query = query.include_reference_content_type_uid()
            >>> result = query.find()

        ==============================
        
        """

        self.__query_params['include_reference_content_type_uid'] = 'true'

        return self

    def where_in(self, key):

        """
        Get entries having values based on referenced fields. This query retrieves all entries that satisfy the query
        conditions made on referenced fields.

        Arguments:
            key {str} -- The key to be constrained
        
        Raises:
            ValueError: If key is None
            ValueError: If key is not str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.

        ==============================
        
        [Example]

            >>> query = stack.content_type('product').query() 
            >>> query = query.where_in("brand")
            >>> result = query.find()

        ==============================

        """

        if key is None:
            raise ValueError('Kindly provide a valid key')
        elif isinstance(key, str):
            self.__query_dict = {key: {'$in_query': self.__query_dict}}
        else:
            raise ValueError('key should be str type')

        return self

    def where_not_in(self, key):

        """Get entries having values based on referenced fields. This query works the opposite of $in_query and
        retrieves all entries that does not satisfy query conditions made on referenced fields.
        
        Arguments:
            key {str} -- The key to be constrained
        
        Raises:
            ValueError: If key is None
            ValueError: If key is not str type
        
        Returns:
            [Query] -- Query object, so you can chain this call.

        ==============================
        
        [Example]

            >>> query = stack.content_type('product').query() 
            >>> query = query.where_not_in("brand")
            >>> result = query.find()

        ==============================

        """

        if key is None:
            raise ValueError('Kindly provide a valid key')
        elif isinstance(key, str):
            self.__query_dict = {key: {'$nin_query': self.__query_dict}}
        else:
            raise ValueError('key should be str type')

        return self

    def __setup_queries(self):

        if self.__query_dict is not None and len(self.__query_dict) > 0:
            self.__query_params["query"] = self.__query_dict
        if self.__uid_except is not None and len(self.__uid_except) > 0:
            self.__query_params["except[BASE][]"] = self.__uid_except
            self.__uid_except = None
        if self.__uid_only is not None and len(self.__uid_only) > 0:
            self.__query_params["only[BASE][]"] = self.__uid_only
            self.__uid_only = None
        if self.__only_json is not None and len(self.__only_json) > 0:
            self.__query_params["only"] = self.__only_json
            self.__only_json = None
        if self.__except_Json is not None and len(self.__except_Json) > 0:
            self.__query_params["except"] = self.__except_Json
            self.__except_Json = None
        if self.__uid_include is not None and len(self.__uid_include) > 0:
            self.__query_params["include[]"] = self.__uid_include
            self.__uid_include = None

        return self

    def find(self):

        """It fetches the query result.
        
        List of :class:`Entry <contentstack.entry.Entry>` objects.

        Raises:
            ValueError: If content_type_id is None
            ValueError: If content_type_id is empty or not str type
        
        Returns:
            list[Entry] -- List of <contentstack.entry.Entry>
        
        ==============================
        
        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> result = query.find()
        
        ==============================
        

        """

        if self.__content_type_id is None:
            raise ValueError('Kindly provide a valid content_type_id')
        elif isinstance(self.__content_type_id, str) and len(self.__content_type_id) > 0:
            return self.__execute_query()
        else:
            raise ValueError('Invalid content_type_id')

    def find_one(self):

        """ It returns only one result.

        Returns:
            list[Entry] -- List of <contentstack.entry.Entry>

        ==============================
        
        [Example]:

            >>> query = stack.content_type('product').query() 
            >>> result = query.find_one()
        
        ==============================
        """
        self.__query_params["limit"] = 1
        return self.__execute_query()

    def __execute_query(self):
        self.__setup_queries()
        result = self.__http_request.get_result(self.__query_url, self.__query_params, self.__headers)
        return result
