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
from contentstack import http_request


class Query:

    """
    Contentstack provides certain queries that you can use to fetch filtered results.
    You can use queries for Entries and Assets API requests.
    [API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#queries]

    """

    def __init__(self, content_type_id: str):

        self._stack_headers = {}
        self._objectUidForInclude: list = []
        self._objectUidForExcept: list = []
        self._objectUidForOnly: list = []

        self._urlQueries = {}
        self._queryValue = {}
        self._onlyJsonObject = {}
        self._queryValueJSON = {}
        self._exceptJsonObject = {}
        self._mainJSON = {}

        self._content_type_id = content_type_id
        self._entry_url = None

    def set_content_type(self, content_type):
        self._content_type_id = content_type

    def _headers(self, local_headers: dict):
        if local_headers is not None:
            self._stack_headers = local_headers.copy()

    def header(self, key, value):
        self._stack_headers[key] = value

    def remove_header(self, key):
        if key in self._stack_headers:
            self._stack_headers.pop(key)

    def set_locale(self, locale_code):
        if locale_code is not None:
            self._urlQueries["locale"] = locale_code
        return self

    def get_content_type(self):
        return self._content_type_id

    def where(self, key: str, value):
        """
        Equals Operator
        Get entries containing the field values matching the condition in the query.
        Example: In the Products content type, you have a field named Title ("uid":"title") field.
        If, for instance, you want to retrieve all the entries in which the value for
        the Title field is 'Redmi 3S', you can set the parameters as:

        {kay = "title": value= "Redmi 3S"}

        Let’s consider another example. You want to retrieve all the entries that have their
        start date as 8th December, 2017. Now, you need to set this parameter with the date
        in the ISO Date format as below:

        { kay = "start_date": value = "2017-12-08T00:00:00.000Z"  }

        This will give you all the entries where the start date is 8th December, 2017.
        :return: self

        """
        if key is not None and value is not None:
            self._queryValueJSON[key] = value

        return self

    def add_query(self, key: str, value):

        """
        [Uses]:

        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag");
        query = stack.contentType("contentType_name").query();
        query.addQuery("query_param_key", "query_param_value");

        :param value value:
        :param key key:
        :returns Query object, so you can chain this call.

        """
        if key is not None and value is not None:
            self._urlQueries[key] = value

        return self

    def remove_query(self, key: str):
        """
        Remove provided query key from custom query if exist.
        :param key Query name to remove.
        :return: Query object, so you can chain this call.

        projectQuery.removeQuery("query_key");
        """

        if key is not None and key in self._urlQueries:
            self._urlQueries.pop(key)

        return self

    def and_query(self, query_objects: list):

        """
        Combines all the queries together using AND operator
        :param query_objects: list of Query instances on which AND query executes.
        :return: Query

        # blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.
        Stack stack = contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()

        query = project_class.query()
        query.where('username','something')

        Query sub_query = project_class.query()
        subQuery.where('email_address','something@email.com')

        list of Query if this is named array
        array.add(query)
        array.add(subQuery)
        project_query.and(array)

        """

        if query_objects is not None and len(query_objects) > 0:
            or_value_json: list = []
            for query in query_objects:
                or_value_json.append(query)
            self._queryValueJSON["$and"] = or_value_json

        return self

    def or_query(self, query_objects: list):
        """
        Add a constraint to fetch all entries which satisfy <b> any </b> queries.
        :param query_objects list of Query instances on which OR query executes.
        :returns Query object, so you can chain this call.

       [Example :]

        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()

        query = project_class.query();
        query.where('username','something')

        aub_query = project_class.query()
        subQuery.where('email_address','something@email.com')

        list of Query class instances
        array.add(query);
        array.add(subQuery)
        csQuery.or(array)

        :param query_objects:
        :return:
        """

        if query_objects is not None and len(query_objects) > 0:
            or_value_json: list = []
            for query in query_objects:
                or_value_json.append(query)
            self._queryValueJSON["$or"] = or_value_json

        return self

    def less_than(self, key: str, value):
        """

        Add a constraint to the query that requires a particular key entry to be less than the provided value.
        :param key the key to be constrained.
        :param value the value that provides an upper bound.
        :returns  Query object, so you can chain this call.

        [Example :]

        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query()
        csQuery.lessThan("due_date", "2013-06-25T00:00:00+05:30")

        """
        if key is not None and value is not None:
            self._queryValue["$lt"] = value
            self._queryValueJSON[key] = self._queryValue

        return self

    def less_than_or_equal_to(self, key: str, value):

        """
        Add a constraint to the query that requires a particular key entry to be less than or equal to the provided value.
        :param key The key to be constrained
        :param value The value that must be equalled.
        :returns Query object, so you can chain this call.

        [ Example :]
        # blt5d4sample2633b' is a dummy Stack API key
        # blt6d0240b5sample254090d' is dummy access token.
        # stack = Contentstack.stack(context, "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag", false);
        # cs_query = stack.contentType("contentType_name").query();
        # cs_query.lessThanOrEqualTo("due_date", "2013-06-25T00:00:00+05:30");

        """

        if key is not None and value is not None:
            self._queryValue["$lte"] = value
            self._queryValueJSON[key] = self._queryValue

        return self

    def greater_than(self, key: str, value):

        """
        Add a constraint to the query that requires a particular key entry to be greater than the provided value.
        :param key The key to be constrained.
        :param value The value that provides an lower bound.
        :return  Query object, so you can chain this call.

        [Example :]
        //'blt5d4sample2633b' is a dummy Stack API key
        //'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack(context, "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query()
        cs_query.greater_than("due_date", "2013-06-25T00:00:00+05:30")

        """

        if key is not None and value is not None:
            self._queryValue["$gt"] = value
            self._queryValueJSON[key] = self._queryValue

        return self

    def greater_than_or_equal_to(self, key: str, value):

        """
        Add a constraint to the query that requires a particular key entry to be greater than or equal to the provided value.
        :param key The key to be constrained.
        :param value The value that provides an lower bound.
        :return  Query object, so you can chain this call.

        [Example :]
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        # stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # cs_query = stack.content_type("contentType_name").query()
        # cs_query.greaterThanOrEqualTo("due_date", "2013-06-25T00:00:00+05:30")

        """

        if key is not None and value is not None:
            self._queryValue["$gte"] = value
            self._queryValueJSON[key] = self._queryValue

        return self

    def not_equal_to(self, key: str, value):

        """

        [USES]

        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query()
        cs_query.notEqualTo("due_date", "2013-06-25T00:00:00+05:30");


        Add a constraint to the query that requires a particular key&#39;s
        entry to be not equal to the provided value.

        :param  key The key to be constrained.
        :param value: value The object that must not be equaled
        :return: Query object, so you can chain this call.

        """

        if key is not None and value is not None:
            self._queryValue["$ne"] = value
            self._queryValueJSON[key] = self._queryValue

        return self

    def contained_in(self, key: str, values: list):

        """
        [Example :]
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.contained_in("severity", ["Show Stopper", "Critical"])

        Add a constraint to the query that requires a particular key&#39;s entry to be contained
        in the provided array.
        :param key The key to be constrained.
        :param values The possible values for the key&#39;s object.
        :return  Query object, so you can chain this call.

        """
        if key is not None and values is not None:

            if isinstance(values, list):
                values_array = ','.join(map(str, values))
                self._queryValue["$in"] = values_array
            self._queryValueJSON[key] = self._queryValue

        return self

    def not_contained_in(self, key: str, values: list):

        """
        [Example :]
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.contentType("contentType_name").query()
        cs_query.contained_in("severity", ["Show Stopper", "Critical"])

        Add a constraint to the query that requires a particular key entry&#39;s
        value not be contained in the provided array.
        :param key The key to be constrained.
        :param values The possible values for the key&#39;s object.
        :return  Query object, so you can chain this call.

        """

        if key is not None and values is not None:

            if isinstance(values, list):
                values_array: list = []
                for val in values:
                    values_array.append(val)
            self._queryValue["$nin"] = values_array
            self._queryValueJSON[key] = self._queryValue

        return self

    def exists(self, key: str):

        """
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        # stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # cs_query = stack.content_type("contentType_name").query()
        cs_query.exists("status");

        Add a constraint that requires, a specified key exists in response.
        :param key: key The key to be constrained.
        :return: Query object, so you can chain this call.
        """
        if key is not None:
            self._queryValue["$exists"] = 'true'
            self._queryValueJSON[key] = self._queryValue

        return self

    def not_exists(self, key: str):

        """
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.
        stack = Contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query()
        cs_query.not_exists("status")

        Add a constraint that requires, a specified key does not exists in response.
        :param key: key The key to be constrained.
        :return: Query object, so you can chain this call.

        """
        if key is not None:
            self._queryValue["$exists"] = 'false'
            self._queryValueJSON[key] = self._queryValue

        return self

    def include_reference(self, key: str):

        """
        # //'blt5d4sample2633b' is a dummy Stack API key
        # //'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.Stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        cs_query = stack.content_type("contentType_name").query();
        cs_query.include_reference("for_bug");

        Add a constraint that requires a particular reference key details.
        :param key: key key that to be constrained.
        :return: Query object, so you can chain this call.
        """
        if key is not None:
            self._objectUidForInclude.append(key)

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
        tagalog: str = None
        if tags is not None and len(tags) > 0:
            for tag in tags:
                tagalog += ",{0}".format(tag)
            self._urlQueries["tags"] = tagalog

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
            self._urlQueries["asc"] = key
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
            self._urlQueries["desc"] = key
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
                self._objectUidForExcept.append(uid)
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
                self._objectUidForOnly.append(uid)

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
            self._onlyJsonObject[reference_field_uid] = field_value_container
            self._objectUidForInclude.append(reference_field_uid)

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
            self._exceptJsonObject[reference_field_uid] = field_value_container
            self._objectUidForInclude.append(reference_field_uid)

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
        self._urlQueries["count"] = "true"
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
        self._urlQueries["include_count"] = "true"
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
        if "include_schema" in self._urlQueries:
            self._urlQueries.pop("include_count")
        self._urlQueries["include_content_type"] = "true"

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
        self._urlQueries["include_owner"] = "true"
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
            self._urlQueries["before_uid"] = uid
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
            self._urlQueries["after_uid"] = uid
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
            self._urlQueries["skip"] = number
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
            self._urlQueries["limit"] = number
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
            if len(self._queryValue) > 0:
                self._queryValue.clear()
            self._queryValue["$regex"] = regex
            if modifiers is not None:
                self._queryValue["$options"] = modifiers
            self._queryValueJSON[key] = self._queryValue

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
            self._urlQueries["locale"] = locale_code
        return self

    def search(self, value: str):
        if value is not None:
            self._urlQueries["typeahead"] = value
        return self

    def add_param(self, key: str, value: str):
        if key is not None and value is not None:
            self._urlQueries[key] = value
        return self

    def __setup_queries(self):

        if self._queryValueJSON is not None and len(self._queryValueJSON) > 0:
            self._urlQueries["query"] = self._queryValueJSON
        if self._objectUidForExcept is not None and len(self._objectUidForExcept) > 0:
            self._urlQueries["except[BASE][]"] = self._objectUidForExcept
            self._objectUidForExcept = None
        if self._objectUidForOnly is not None and len(self._objectUidForOnly) > 0:
            self._urlQueries["only[BASE][]"] = self._objectUidForOnly
            self._objectUidForOnly = None
        if self._onlyJsonObject is not None and len(self._onlyJsonObject) > 0:
            self._urlQueries["only"] = self._onlyJsonObject
            self._onlyJsonObject = None
        if self._exceptJsonObject is not None and len(self._exceptJsonObject) > 0:
            self._urlQueries["except"] = self._exceptJsonObject
            self._exceptJsonObject = None
        if self._objectUidForInclude is not None and len(self._objectUidForInclude) > 0:
            self._urlQueries["include[]"] = self._objectUidForInclude
            self._objectUidForInclude = None
        return self

    def find(self):
        if self._content_type_id is not None and len(self._content_type_id) > 0:
            self.__execute_query()

    def find_one(self):
        limit = -1
        if self._content_type_id is not None and len(self._content_type_id) > 0:
            if self._urlQueries is not None and "limit" in self._urlQueries:
                limit = self._urlQueries["limit"]
            self._urlQueries["limit"] = 1
            self.__execute_query()
            if limit != -1:
                self._urlQueries["limit"] = limit
        pass

    def __execute_query(self):
        if self._content_type_id is not None:
            self._entry_url = "content_types/{0}/entries".format(self._content_type_id)
            self.__setup_queries()
        else:
            raise Exception("content_type_id is not found, "
                            " HELP: ContentTypeID can be set by calling method [query.set_content_type('your_content_type')]")
        if len(self._stack_headers) < 1:
            raise Exception("You must called contentstack.Stack() first")
        payload = {"query", self._urlQueries}
        https_request = http_request.HTTPRequestConnection(self._entry_url, payload, self._stack_headers)
        resp, err = https_request.http_request()
        if err is None:
            resp = resp['entries']
            print(resp, len(resp))
        return resp, err
        pass


query_cs = Query('product')
query_cs.set_header('api_key', 'blt20962a819b57e233')
query_cs.set_header('access_token', 'blt01638c90cc28fb6f')
query_cs.set_header('environment', 'production')
query_cs.set_locale("en-us")
query_cs.contained_in('contain', ["shailesh", "Ramesh", "Suresh"])
