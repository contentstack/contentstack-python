"""
Query
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""

import os
import sys

sys.path.insert(0, os.path.abspath('.'))


class Query:
    """
    Contentstack provides certain queries that you can use to fetch filtered results.
    You can use queries for Entries and Assets API requests.
    [API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#queries]
    """

    def __init__(self, content_type_uid):

        self.__config = None
        self.__entry_url = None
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
        # _instance is protected and it is accessible with in package only.
        self.__stack_instance = stack_instance
        self.__config = self.__stack_instance.config
        endpoint = self.__config.endpoint
        self.__entry_url = '{}/content_types/{}/entries'.format(endpoint, self.__content_type_id)
        self.__http_request = self.__stack_instance.get_http_instance

        return self

    @property
    def content_type(self):

        """
        :return content_type: It returns the content type of the entry.
        :rtype: str

        ==============================
        [Example]:

        >>> query = query.content_type
        ==============================
        """

        return self.__content_type_id

    @content_type.setter
    def content_type(self, content_type_id):

        """
        The unique ID of the content type of which you wish to retrieve the details. The uid is generated based on
        the title of the content type and it is unique across a stack
        :param content_type_id: unique ID of the content type of which you wish to retrieve information
        :type content_type_id: str
        
        ==============================
        [Example]:

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

        """
        :return: Additional header dict for Query.
        :rtype: dict
        
        ==============================

        [Example]:

        >>> query = query.headers

        ==============================
        """

        return self.__headers

    def remove_header(self, key):

        """
        :param key: It removes header from the Query headers by key.
        :type key: str
        :return: self
        :rtype: Query, so you can chain this call.
        
        ==============================

        [Example]:

        >>> query = query.remove_header('header_key')
        ==============================
        """

        if key is None or len(key.strip()) == 0:
            raise ValueError('Kindly provide valid header key')
        if isinstance(key, str) and key in self.__headers:
            self.__headers.pop(key, None)

        return self

    def add_header(self, key, value):

        """
        :param key: It adds header in the Query headers by key and value.
        :type key: str
        :param value:  Respective value of header key
        :type value: str
        :return: self
        :rtype: Query, so you can chain this call.
        
        ==============================

        [Example]:

        >>> query = query.add_header('key', value)

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

        """
        :param locale: Enter the language code of which the entries needs to be included.
        Only the entries published in this locale will be displayed.
        :type locale: str
        :return: self
        :rtype: Query, so you can chain this call.

        ==============================

        [Example]:

        >>> query = query.locale('en-us')

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

        """
        :param key: Get entries containing the field values matching the condition in the query.
        :type key: str
        :param value: provide value as object
        :type value: object
        :return: self
        :rtype: Query, so you can chain this call.
        
        ==============================

        [Example]:

        >>> query.where("uid", "bltsomething123")

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide a valid key and value')
        if isinstance(key, str):
            self.__query_dict[key] = value
        else:
            raise ValueError('key and value should be str')

        return self

    def add_query(self, key, value):

        """
        Add a custom query against specified key.
        :param key: key
        :type key: str
        :param value: value
        :type value: str
        :return: self
        :rtype: Query object, so you can chain this call
        
        ==============================

        [Example]:

        >>> query.add_query("query_param_key", "query_param_value")
        >>> query.find()

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
        :param key: Query key to remove.
        :type key: str
        :return: self
        :rtype:  Query object, so you can chain this call.
        
        ==============================

        [Example]:

        >>> query.remove_query("query_key")
        >>> query.find()

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
        :param query_objects: *query_objects for variable number of arguments of type Query Object
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        Example: Let’s say you want to retrieve entries in which the Title field is set to 'Redmi Note 3' and the Color
        field is 'Gold'. The query to be used for such a case would be:
        The response will contain the entries where the values for Title is 'Redmi Note 3' and Color is 'Gold'
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#and-operator]

        >>> query1.where("title", "Redmi Note 3")
        >>> query2.where("color", "Gold")
        >>> base_query.and_query(query1, query2)
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
        :param query_objects: list of queries
        :type query_objects: Query
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        [Example]: Let’s say you want to retrieve entries in which either the value for the
        Color field is 'Gold' or 'Black'. The query to be used for such a case would be:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#or-operator]

        >>> query1.where("color", "Black")
        >>> query2.where("color", "Gold")
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
        :param key: the key to be constrained.
        :type key: str
        :param value: value the value that provides an upper bound.
        :type value: object
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        [Example]: Let’s say you want to retrieve all the entries that have value of the 
        Price in USD field set to a value that is less than but not equal to 600. 
        You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#less-than]

        >>> query.less_than('price_in_usd', 600)
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
        :param key: The key to be constrained
        :param value: The value that must be equalled.
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        Example: Let’s say you want to retrieve all the entries that have value of the Price in USD field
        set to a value that is less than or equal to 146. To achieve this, send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#less-than-or-equal-to]

        >>> query.less_than_or_equal_to('price_in_usd', 146)
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
        Get entries in which the value for a field is greater than the value provided in the condition.
        :param key: The key to be constrained.
        :param value: The value that provides an lower bound.
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        Example: Let’s say you want to retrieve all the entries that have value of the Price in USD field set to a value
        that is greater than but not equal to 146. You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#greater-than]

        >>> query.greater_than('price_in_usd', 146)
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

        """
        Add a constraint to the query that requires a particular key entry to be greater than or equal to
        the provided value.
        :param key: The key to be constrained.
        :param value: The value that provides an lower bound.
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        Example: Let’s say you want to retrieve all the entries that have value of the Price in USD field set to a value
        that is greater than or equal to 146. You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#greater-than-or-equal-to]

        >>> query.greater_than_or_equal_to('price_in_usd', 146)
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
        Add a constraint to the query that requires a particular key&#39;s
        entry to be not equal to the provided value.
        :param key: The key to be constrained.
        :param value: value The object that must not be equaled
        :return: self
        :rtype: Query object, so you can chain this call.
        
        ==============================

        Example: In the Product content type, you have a field named Price in USD. Now,
        you need to retrieve all entries where the value of this field not equal to '146'
        for this field. The parameter can be used as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#not-equals-operator]

        >>> query.not_equal_to('price_in_usd', 146)
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
        :param key The key to be constrained.
        :param contained_in The possible values for the key's object.
        :return  Query object, so you can chain this call.
        
        ==============================

        Example: In the Product content type, you have a field named Price in USD. Now,
        you need to retrieve all the entries where value of this field is one among the given set of values.
        The query fired using the '$in' parameter is given below:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#array-equals-operator]

        >>> query.contained_in('price_in_usd', 101, 749)
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

        """
        Get all entries in which the value of a field does not match to any of the given values.
        This parameter will compare field values of entries to that of the values provided in the condition,
        and the query will retrieve entries that have field values that does not match to any of the values provided.
        :param key: The key to be constrained.
        :param not_contained_in: The possible comma separated values for the key's object.
        :return: Query object, so you can chain this call.
        
        ==============================
        Example: In the Product content type, you have a field named Price in USD. Now, you need to retrieve the entries
        where the field value does not fall in the given set. You can send the parameter as:
        for more: [https://www.contentstack.com/docs/apis/content-delivery-api/#array-not-equals-operator]

        >>> query.not_contained_in('price_in_usd', 101, 749)
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
        :param key: field_UID
        :return: Query object, so you can chain this call.
        
        ==============================

        In the Product content type, we have a field named Price in USD. Now, you want to retrieve all the entries in
        the content type in which the field exists
        for more: https://www.contentstack.com/docs/apis/content-delivery-api/#exists

        >>> query.exists('price_in_usd')
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
        :param key: field_UID that has to be constrained.
        :return: Query object, so you can chain this call.
        
        ==============================

        In the Product content type, we have a field named Price in USD. Now, you want 
        to retrieve all the entries in the content type in which the field does not exists

        >>> query.not_exists('price_in_usd')
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
        along with the content of the specified entry.
        :param key: field_UID that to be constrained.
        :return: Query object, so you can chain this call.
        
        ==============================

        Example: If you wish to fetch the content of the entry that is included in the
        reference field, you need to use the include[] parameter, and specify the UID of the reference field as
        value. This informs Contentstack that the request also includes fetching the entry used in the specified
        reference field
        for more: https://www.contentstack.com/docs/apis/content-delivery-api/#include-reference

        >>> query.include_reference('categories')
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
        :param tags: Comma separated list of tags with which to search entries.
        :return self. Query object, so you can chain this call.
        
        ==============================

        Example:

        >>> query.tags('black', 'gold', 'silver')
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
        :param key:  field_UID that to be constrained.
        :return self. Query object, so you can
        chain this call.
        
        ==============================
        
        Example: In the Product content type, if you wish to sort the entries with respect to their prices,
        the parameter can be used as:

        >>> query.ascending('price_in_usd')
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

        """
        When fetching entries, you can sort them in the descending order with respect to the value of a
        specific field in the response body.
        :key: field_UID that to be constrained.
        :return self. Query object, so you can chain this call.
        
        ==============================
        
        Example: In the Product content type, if you wish to sort the entries
        with respect to their prices, the parameter can be used as:

        >>> query.descending('price_in_usd')
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
        :field_uid  comma separated uid  which get excluded from the response.
        :return  Query object, so you can chain this call.
        
        ==============================
        
        Example: In the Product content type, if you wish to sort the entries
        with respect to their prices, the parameter can be used as:

        >>> except_field = Query('content_type_uid').except_field_uid('field_uid1', 'field_uid2')
        >>> result = except_field.find()
        ==============================
        """

        if field_uid is None:
            raise ValueError('Kindly provide valid field_uid')
        if len(field_uid) > 0:
            for uid in field_uid:
                self.__uid_except.append(uid)

        return self

    def only(self, *field_uid):

        """
        Specifies an list of field_uid keys in BASE object that would be included in the response.

        :field_uid: comma separated uid of the only reference keys to be included in response.
        :return:  Query object, so you can chain this call.
        
        ==============================
        
        Example: In the Product content type, if you wish to sort the entries
        with respect to their prices, the parameter can be used as:

        >>> query.only('price_in_usd', 'color')
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

        """
        Specifies an array of only keys that would be included in the response.
        :param reference_field_uid: reference_field_uid Key who has reference to some other class object.
        :param field_uid: field_uid list of the only reference keys to be included in response.
        :return: Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> query.only_with_reference_uid('reference_field_uid', 'field_uid 1', 'field_uid 2')
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

        """
        Specifies an array of except keys that would be excluded in the response.
        :param field_uid Array of the except reference keys to be excluded in response.
        :param reference_field_uid Key who has reference to some other class object.
        :return  Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> query.except_with_reference_uid('price_in_usd', 'field_uid 1', 'field_uid 2')
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

        """
        Retrieve count and data of objects in result
        :return  Query object, so you can chain this call.
        
        ==============================
        
        [Example:]
        
        >>> query.include_count()
        >>> result = query.find()
        
        ==============================
        """

        self.__query_params["include_count"] = 'true'

        return self

    def include_content_type(self):

        """
        Include Content Type of all returned objects along with objects themselves.
        :return  Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> query.include_content_type()
        >>> result = query.find()
        
        ==============================
        """

        self.__query_params["include_content_type"] = 'true'

        return self

    def skip(self, number):

        """
        :param number: The number of objects to skip before returning any.
        :return: Query object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> query.skip(3)
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
        :param number: Number of objects to limit.
        :return: Query object, so you can chain this call.
        
        ==============================
        
        [Example]

        >>> query.limit(3)
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
        :param key: The key to be constrained.
        :param regex: The regular expression pattern to match
        :param modifiers (Optional): Any of the following supported Regular expression modifiers.
        :return: Query object, so you can chain this call.

        [Note:] Some useful values for $options are m for making dot match newlines and x for ignoring
        whitespace in regex.
        
        ==============================
        
        [Example:]

        query.regex("name", "browser")
        result= query.find()
        
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
        :param value: used to match or compare
        :return: Query object, so you can chain this call.
        
        ==============================
        
        [Example]

        query.search("value")
        
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
        :param key:  The key as string which needs to be added to the Query
        :param value: The value as string which needs to be added to the Query
        :return: Query object, so you can chain this call.
        
        ==============================
        
        [Example]

        query.param("key", "value")
        result= query.find()
        
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
        :return: Query object, so you can chain this call.

        ==============================

        [Example]

        query.include_reference_content_type_uid()
        result = query.find()

        ==============================
        """

        self.__query_params['include_reference_content_type_uid'] = 'true'

        return self

    def where_in(self, key):

        """
        Get entries having values based on referenced fields. This query retrieves all entries that satisfy the query
        conditions made on referenced fields.
        :param key: The key to be constrained
        :return: Query object, so you can chain this call.

        ==============================
        
        [Example]

        query.where_in("brand")
        result = query.find()
        
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

        """
        Get entries having values based on referenced fields. This query works the opposite of $in_query and
        retrieves all entries that does not satisfy query conditions made on referenced fields.
        :param key: The key to be constrained
        :return: Query object, so you can chain this call.

        ==============================
        
        [Example]

        query.where_not_in("brand")
        result = query.find()
        
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

        """
        It fetches the query result.
        :return: list of Entry Objects.

        ==============================
        
        [Example]:

        result = query.find()
        
        ==============================
        """

        if self.__content_type_id is None:
            raise ValueError('Kindly provide a valid content_type_id')
        elif isinstance(self.__content_type_id, str) and len(self.__content_type_id) > 0:
            return self.__execute_query()
        else:
            raise ValueError('Invalid content_type_id')

    def find_one(self):

        """
        It returns only one result.
        :return: Query result

        ==============================
        
        [Example]:

        result = query.find_one()
        
        ==============================
        """
        self.__query_params["limit"] = 1

        return self.__execute_query()

    def __execute_query(self):
        self.__setup_queries()
        query = self.__query_params.__str__().replace('\'', '\"')
        result = self.__http_request.get_result(self.__entry_url, query, self.__headers)
        return result
