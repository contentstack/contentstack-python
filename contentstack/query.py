"""
 * MIT License
 *
 * Copyright (c) 2012 - 2019 Contentstack
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 """


class Query:

    """
    Contentstack provides certain queries that you can use to fetch filtered results.
    You can use queries for Entries and Assets API requests.
    [API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#queries]
    """

    def __init__(self, content_type_id: str):

        import contentstack
        if content_type_id is not None and len(content_type_id) > 0:
            self.__content_type_id = content_type_id
            self.__entry_url = contentstack.config.Config().endpoint('entries')
            self.__entry_url = '{}/{}/entries'.format(self.__entry_url, self.__content_type_id)
        else:
            ValueError('Invalid content_type_id, content_type_id could not be None or empty')

        self.__stack_headers = {}
        self.__query_params = {}

        self.__uid_include: list = []
        self.__uid_except: list = []
        self.__uid_only: list = []

        self.__query_value = {}
        self.__only_json = {}
        self.__query_dict = {}
        self.__except_Json = {}
        self.__main_json = {}

    @property
    def content_type(self):
        return self.__content_type_id

    @content_type.setter
    def content_type(self, content_type_id):
        if content_type_id is not None and len(content_type_id) > 0:
            self.__content_type_id = content_type_id
        else:
            ValueError('Invalid content_type_id, '
                       'content_type_id could not be None or empty')

    @property
    def headers(self):
        return self.__stack_headers

    @headers.setter
    def headers(self, headers: dict):
        if headers is not None and isinstance(headers, dict):
            self.__stack_headers = headers
            if 'environment' in headers:
                env_value = self.__stack_headers['environment']
                self.__query_params['environment'] = env_value

    def remove_header(self, key):
        if key in self.__stack_headers:
            self.__stack_headers.pop(key)
        return self.__stack_headers

    def add_header(self, key, value):
        if key is not None and value is not None:
            self.__stack_headers[key] = value
        return self.__stack_headers

    def locale(self, locale_code='en-us'):
        self.__query_params["locale"] = locale_code
        return self

    def where(self, key: str, value):

        """
        :param key: field_UID
        :param value: provide value as str
        :return: self

        [Equals Operator]
        Get entries containing the field values matching the condition in the query.
        Example: In the Products content type, you have a field named Title ("uid":"title") field.
        If, for instance, you want to retrieve all the entries in which the value for
        the Title field is 'Redmi 3S', you can set the parameters as:

        [Example]
        query = stack.contentType("content_type_id").query();
        query.where('title', 'Redmi 3S')
        result, error = query.find()

        """

        if key is not None and value is not None and len(key) > 0 and len(value) > 0:
            self.__query_dict[key] = value
        else:
            raise TypeError('Kindly provide valid parameters')
        return self

    def add_query(self, key: str, value):

        """
        :param value value:
        :param key key:
        :returns Query object, so you can chain this call.

        [Uses]:
        query = stack.contentType("content_type_id").query()
        query.add_query("query_param_key", "query_param_value")
        result, error = query.find()
        if error is None:
            print(result)
        """

        if key is not None and value is not None:
            self.__query_params[key] = value
        else:
            raise TypeError('Kindly provide valid parameters')
        return self

    def remove_query(self, key: str):

        """
        Remove provided query key from custom query if exist.
        :param key Query name to remove.
        :return: Query object, so you can chain this call.

        [Uses]:
        query = stack.contentType("content_type_id").query();
        projectQuery.remove_query("query_key")
        result, error = query.find()
        if error is None:
            print(result)
        """

        if key is not None and key in self.__query_params:
            self.__query_params.pop(key)
        else:
            raise TypeError('Kindly provide valid parameters')
        return self

    def and_query(self, queries: list):

        """
        Combines all the queries together using AND operator
        :param queries: list of Query instances on which AND query executes.
        :return: self

        [Uses]:
        query = stack.content_type("content_type_id").query()

        query = content_type.query()
        query.where("title", "Redmi Note 3")

        sub_query = content_type.query()
        sub_query.where("color", "Gold")

        list_array = [query, sub_query]
        base_query.and_query(list_array)
        result, error = query.find()
        if error is None:
            print(result)

        """

        if queries is not None and len(queries) > 0 and isinstance(queries, list):
            query_list: list = []
            for query in queries:
                query_list.append(query.__query_dict)
            self.__query_dict["$and"] = query_list
        else:
            raise TypeError('Kindly provide valid parameters')

        return self

    def or_query(self, queries: list):

        """
        :param queries: list
        :return: self

        Get all entries that satisfy at least one
        of the given conditions provided in the '$or' query.

        [Example]: Let’s say you want to retrieve
        entries in which either the value for the
        Color field is 'Gold' or 'Black'.
        The query to be used for such a case would be:

        cs_query = stack.content_type("content_type_id").query()

        query1 = content_type.query()
        query1.where("color", "Black")

        query2 = content_type.query()
        query2.where("color", "Gold")

        list_array = [query1, query2]

        cs_query.or_query(list_array)
        result, error = cs_query.find()

        """

        if queries is not None and len(queries) > 0:
            query_list: list = []
            for query in queries:
                query_list.append(query.__query_dict)
            self.__query_dict["$or"] = query_list
        else:
            raise TypeError('Kindly provide valid parameters')

        return self

    def less_than(self, key: str, value):

        """
        Get entries in which the value of a field is lesser
        than the value provided in the condition.

        [Example]: Let’s say you want to retrieve all the
        entries that have value of the Price in USD
        field set to a value that is less than but not
        equal to 600. You can send the parameter as:

        :param key the key to be constrained.
        :param value the value that provides an upper bound.
        :returns  Query object, so you can chain this call.

        [Example :]
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than('price_in_usd', 600)
        result, error = query.find()
        """

        if key is not None and value is not None:
            self.__query_value["$lt"] = value
            self.__query_dict[key] = self.__query_value

        return self

    def less_than_or_equal_to(self, key: str, value):

        """
        Get entries in which the value of a field is
        lesser than or equal to the value
        provided in the condition.

        Example: Let’s say you want to retrieve
        all the entries that have value of the Price in USD field set to a value that
        is less than or equal to 146. To achieve this, send the parameter as:

        :param key The key to be constrained
        :param value The value that must be equalled.
        :returns Query object, so you can chain this call.

        [ Example :]
        cs_query = stack.content_type("content_type_id").query();
        query.less_than_or_equal_to('price_in_usd', 146)
        result, error = query.find()

        """

        if key is not None and value is not None:
            self.__query_value["$lte"] = value
            self.__query_dict[key] = self.__query_value

        return self

    def greater_than(self, key: str, value):

        """
        Add a constraint to the query that requires a particular key entry to be greater than the provided value.
        :param key The key to be constrained.

        :param value The value that provides an lower bound.
        :return  Query object, so you can chain this call.

        [ Example :]
        cs_query = stack.content_type("content_type_id").query();
        query.greater_than('price_in_usd', 146)
        result, error = query.find()

        """

        if key is not None and value is not None:
            self.__query_value["$gt"] = value
            self.__query_dict[key] = self.__query_value

        return self

    def greater_than_or_equal_to(self, key: str, value):

        """
        Add a constraint to the query that requires a particular key entry to be greater than or equal to the provided value.
        :param key The key to be constrained.

        :param value The value that provides an lower bound.
        :return  Query object, so you can chain this call.

        [ Example :]
        cs_query = stack.content_type("content_type_id").query();
        query.greater_than_or_equal_to('price_in_usd', 146)
        result, error = query.find()

        """

        if key is not None and value is not None:
            self.__query_value["$gte"] = value
            self.__query_dict[key] = self.__query_value

        return self

    def not_equal_to(self, key: str, value):

        """
        Add a constraint to the query that requires a particular key&#39;s
        entry to be not equal to the provided value.

        :param  key The key to be constrained.
        :param value: value The object that must not be equaled
        :return: Query object, so you can chain this call.

        [ Example :]
        cs_query = stack.content_type("content_type_id").query();
        query.not_equal_to('price_in_usd', 146)
        result, error = query.find()
        """

        if key is not None and value is not None:
            self.__query_value["$ne"] = value
            self.__query_dict[key] = self.__query_value

        return self

    def contained_in(self, key: str, values: list):

        """
        Add a constraint to the query that requires a particular key&#39;s entry to be contained
        in the provided array.

        :param key The key to be constrained.
        :param values The possible values for the key&#39;s object.
        :return  Query object, so you can chain this call.

        [ Example :]
        query = content_type.query()
        query.locale('en-us')
        in_list = [101, 749]
        query.contained_in('price_in_usd', in_list)
        result, error = query.find()

        """
        if key is not None and values is not None:
            if isinstance(values, list):
                self.__query_value["$in"] = values
            self.__query_dict[key] = self.__query_value

        return self

    def not_contained_in(self, key: str, values: list):

        """
        Add a constraint to the query that requires a particular key entry&#39;s
        value not be contained in the provided array.

        :param key The key to be constrained.
        :param values The possible values for the key&#39;s object.
        :return  Query object, so you can chain this call.

        [ Example :]
        query = content_type.query()
        query.locale('en-us')
        in_list = [101, 749]
        query.not_contained_in('price_in_usd', in_list)
        result, error = query.find()

        """

        if key is not None and values is not None:

            if isinstance(values, list):
                values_array: list = []
                for val in values:
                    values_array.append(val)
            self.__query_value["$nin"] = values_array
            self.__query_dict[key] = self.__query_value

        return self

    def exists(self, key: str):

        """

        Add a constraint that requires, a specified key exists in response.
        :param key: key The key to be constrained.
        :return: Query object, so you can chain this call.

        [ Example :]
        query = content_type.query()
        query.exists('price_in_usd')
        result, error = query.find()
        """
        if key is not None:
            self.__query_value["$exists"] = 'true'
            self.__query_dict[key] = self.__query_value

        return self

    def not_exists(self, key: str):

        """

        Add a constraint that requires, a specified key does not exists in response.
        :param key: key The key to be constrained.
        :return: Query object, so you can chain this call.

        [ Example :]
        query = content_type.query()
        query.not_exists('price_in_usd')
        result, error = query.find()

        """
        if key is not None:
            self.__query_value["$exists"] = "false"
            self.__query_dict[key] = self.__query_value

        return self

    def include_reference(self, key: str):

        """
        When you fetch an entry of a content type that has a reference field,
        by default, the content of the referred entry is not fetched. It only
        fetches the UID of the referred entry, along with the content of the
        specified entry.

        :param key: str key that to be constrained.
        :return: self
        """
        if key is not None and isinstance(key, str):
            self.__uid_include.append(key)

        return self

    def tags(self, tags: list):

        """
        Include tags with which to search entries.
        :param tags Comma separated array of tags with which to search entries.
        :return {@link Query} object, so you can chain this call.
        [Example :]
        # 'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query();
        cs_query.tags(;"tag1","tag2"]);
        :param tags:
        :return: Query
        """
        tagalog: str = ''
        if tags is not None and len(tags) > 0:
            for tag in tags:
                tagalog += ",{0}".format(tag)
            self.__query_params["tags"] = tagalog

        return self

    def ascending(self, key: str):

        """
        Sort the results in ascending order with the given key.
        Sort the returned entries in ascending order of the provided key.
        :param key The key to order by.
        :return  Query object, so you can chain this call.
        ~~~~~~~~~~Example :~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        # stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # cs_query = stack.content_type("contentType_name").query();
        # cs_query.ascending("name");

        :return: Query

        """
        if key is not None:
            self.__query_params["asc"] = key
        return self

    def descending(self, key):

        """
        Sort the results in descending order with the given key..
        Sort the returned entries in ascending order of the provided key.
        :param key The key to order by.
        :return  Query object, so you can chain this call.
        ~~~~~~~~~~Example :~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        # stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # cs_query = stack.content_type("contentType_name").query();
        # cs_query.descending("name");

        :return: Query

        """
        if key is not None:
            self.__query_params["desc"] = key
        return self

    def except_field_uid(self, field_uid: list):

        """
        Specifies list of field uids that would be &#39;excluded&#39; from the response.
        :param field_uid field uid  which get &#39;excluded&#39; from the response.
        :return  Query object, so you can chain this call.
        ~~~~~~~~~~~~Example :~~~~~~~~~~~~~~~~~
        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query()
        array.add("name")
        array.add("description")>
        cs_query.except(array)
        """
        if field_uid is not None and len(field_uid) > 0:
            for uid in field_uid:
                self.__uid_except.append(uid)
        return self

    def only_field_uid(self, field_uid: list):

        """
        Specifies an list of only_field_uid keys in BASE object that would be &#39;included&#39; in the response.
        :param field_uid list of the &#39;only&#39; reference keys to be included in response.
        :return  Query object, so you can chain this call.
        ~~~~~~~~~~~~~~~Example :~~~~~~~~~~~~~
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        # stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # cs_query = stack.contentType("contentType_name").query()
        # cs_query.only(["name", "company", ""user])

        """
        if field_uid is not None and len(field_uid) > 0:
            for uid in field_uid:
                self.__uid_only.append(uid)

        return self

    def only_with_reference_uid(self, field_uid: list, reference_field_uid: str):

        """
        Specifies an array of &#39;only&#39; keys that would be &#39;included&#39; in the response.
        :param field_uid: field_uid list of the &#39;only&#39; reference keys to be included in response.
        :param reference_field_uid: reference_field_uid Key who has reference to some other class object.
        :return: Query object, so you can chain this call.

        ~~~~~~~Example :~~~~~~~~~~~

        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        list.add("description")
        list.add("name")
        cs_query.only_with_reference_uid(list, "for_bug")

        """
        if field_uid is not None and reference_field_uid is not None:
            field_value_container: list = []
            for uid in field_uid:
                field_value_container.append(uid)
            self.__only_json[reference_field_uid] = field_value_container
            self.__uid_include.append(reference_field_uid)

        return self

    def except_with_reference_uid(self, field_uid: list, reference_field_uid: str):

        """
        Specifies an array of &#39;except&#39; keys that would be &#39;excluded&#39; in the response.
        :param field_uid Array of the &#39;except&#39; reference keys to be excluded in response.
        :param reference_field_uid Key who has reference to some other class object.
        :return  Query object, so you can chain this call.
        ~~~~~~~~~Example :~~~~~~~~~~~~~~~
        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query()
        list.add("description")
        list.add("name")
        cs_query.exceptWithReferenceUid(list, "for_bug");

        """
        if field_uid is not None and reference_field_uid is not None:
            field_value_container: list = []
            for uid in field_uid:
                field_value_container.append(uid)
            self.__except_Json[reference_field_uid] = field_value_container
            self.__uid_include.append(reference_field_uid)

        return self

    def count(self):
        """
        Retrieve only count of entries in result.
        :return  Query object, so you can chain this call.
        ~~~~~~~ Note ~~~~~~~~~~~
        Call {@link QueryResult#getCount()} method in the success to get count of objects.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.count()

        """
        self.__query_params["count"] = "true"
        return self

    def include_count(self):
        """
        Retrieve count and data of objects in result
        :return  Query object, so you can chain this call.
        ~~~~~~~ Note ~~~~~~~~~~~
        Call {@link QueryResult#getCount()} method in the success to get count of objects.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        csQuery.include_count();

        """
        self.__query_params["include_count"] = "true"
        return self

    def include_content_type(self):
        """
        Include Content Type of all returned objects along with objects themselves.
        :return  Query object, so you can chain this call.
        ~~~~~~~ Note ~~~~~~~~~~~
        Call {@link QueryResult#getCount()} method in the success to get count of objects.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.include_content_type()

        """
        if "include_schema" in self.__query_params:
            self.__query_params.pop("include_count")
        self.__query_params["include_content_type"] = "true"

        return self

    def include_owner(self):

        """
        Include Content Type of all returned objects along with objects themselves.
        :return  Query object, so you can chain this call.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.include_owner()

        """
        self.__query_params["include_owner"] = "true"
        return self

    def before_uid(self, uid: str):

        """
        Fetches all the objects before specified uid.
        @param uid  uid before which objects should be returned.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.before_uid()

        """
        if uid is not None:
            self.__query_params["before_uid"] = uid
        return self

    def after_uid(self, uid: str):

        """
        Fetches all the objects after specified uid.
        @param uid  uid before which objects should be returned.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.after_uid()

        """
        if uid is not None:
            self.__query_params["after_uid"] = uid
        return self

    def skip(self, number: int):

        """
        the number of objects to skip before returning any.
        :param number:
        :param No of objects to skip from returned objects.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.limit(2)

        """
        if number is not None and isinstance(number, int):
            self.__query_params["skip"] = number
        return self

    def limit(self, number: int):

        """
        A limit on the number of objects to return.
        :param number No of objects to limit.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.limit(2)

        """
        if number is not None and isinstance(number, int):
            self.__query_params["limit"] = number
        return self

    def regex(self, key: str, regex: str, modifiers: str = None):

        """
        Add a regular expression constraint for finding string values that match the provided regular expression.
        This may be slow for large data sets.
        :param modifiers: Optional
        Any of the following supported Regular expression modifiers.
        <p>use <b> i </b> for case-insensitive matching.</p>
        <p>use <b> m </b> for making dot match newlines.</p>
        <p>use <b> x </b> for ignoring whitespace in regex</p>

        :param key The key to be constrained.
        :param regex The regular expression pattern to match.
        :return Query object, so you can chain this call.
        ~~~~~~~~Example :~~~~~~~~~~`
        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.regex("name", "^browser");

        """
        if key is not None and regex is not None:
            if len(self.__query_value) > 0:
                self.__query_value.clear()
            self.__query_value["$regex"] = regex
            if modifiers is not None:
                self.__query_value["$options"] = modifiers
            self.__query_dict[key] = self.__query_value

        return self

    def set_locale(self, locale_code: str):
        """

        :param locale_code: Language code value
        :return: Query instance

        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.set_locale("en_eu");
        """
        if locale_code is not None:
            self.__query_params["locale"] = locale_code
        return self

    def search(self, value: str):
        if value is not None:
            self.__query_params["typeahead"] = value
        return self

    def add_param(self, key: str, value: str):
        if key is not None and value is not None:
            self.__query_params[key] = value
        return self

    def __setup_queries(self):

        if self.__query_dict is not None and len(self.__query_dict) > 0:
            self.__query_params["query"] = self.__query_dict.__str__().replace("\'", "\"")

        if self.__uid_except is not None and len(self.__uid_except) > 0:
            self.__query_params["except[BASE][]"] = self.__uid_except.__str__().replace("\'", "\"")
            self.__uid_except = None

        if self.__uid_only is not None and len(self.__uid_only) > 0:
            self.__query_params["only[BASE][]"] = self.__uid_only.__str__().replace("\'", "\"")
            self.__uid_only = None

        if self.__only_json is not None and len(self.__only_json) > 0:
            self.__query_params["only"] = self.__only_json.__str__().replace("\'", "\"")
            self.__only_json = None

        if self.__except_Json is not None and len(self.__except_Json) > 0:
            self.__query_params["except"] = self.__except_Json.__str__().replace("\'", "\"")
            self.__except_Json = None

        if self.__uid_include is not None and len(self.__uid_include) > 0:
            var = ', '.join(self.__uid_include)
            self.__query_params["include[]"] = var.replace("\'", "\"")
            self.__uid_include = None

        return self

    def find(self):
        if self.__content_type_id is not None and len(self.__content_type_id) > 0:
            return self.__execute_query()
        else:
            raise KeyError('Invalid content_type id ')

    def find_one(self):
        limit = -1
        if self.__content_type_id is not None and len(self.__content_type_id) > 0:
            if self.__query_params is not None and "limit" in self.__query_params:
                limit = self.__query_params["limit"]
            self.__query_params["limit"] = 1
            self.__execute_query()
            if limit != -1:
                self.__query_params["limit"] = limit
        else:
            raise KeyError('Invalid content_type id ')

        pass

    def __execute_query(self) -> tuple:

        import requests
        from urllib import parse
        from requests import Response
        from contentstack import Entry
        error = None

        self.__setup_queries()
        self.__stack_headers.update(self.header_agents())
        payload = parse.urlencode(query=self.__query_params, encoding='UTF-8')

        try:
            response: Response = requests.get(self.__entry_url, params=payload, headers=self.__stack_headers)
            entries: list[Entry] = []

            if response.ok:

                response: dict = response.json()['entries']
                for entry_obj in response:
                    entry = Entry()
                    entry.configure(entry_obj)
                    entries.append(entry)
            else:
                error = response.json()

            return entries, error

        except requests.exceptions.RequestException as e:
            raise ConnectionError(e.response)
            pass

    @classmethod
    def header_agents(cls) -> dict:

        import contentstack
        import platform

        """
        Contentstack-User-Agent header.
        """
        header = {'sdk': dict(name=contentstack.__package__, version=contentstack.__version__)}
        os_name = platform.system()

        if os_name == 'Darwin':
            os_name = 'macOS'

        elif not os_name or os_name == 'Java':
            os_name = None

        elif os_name and os_name not in ['macOS', 'Windows']:
            os_name = 'Linux'

        header['os'] = {
            'name': os_name,
            'version': platform.release()
        }

        local_headers = {'X-User-Agent': str(header), "Content-Type": 'application/json'}
        return local_headers
