"""
Contentstack provides certain queries that you can use to fetch filtered results
"""
import json
from contentstack.basequery import BaseQuery
from contentstack.entryqueryable import EntryQueryable
from urllib import parse
import enum


class QueryType(enum.Enum):
    AND = "$and"
    OR = '$or'


class Query(BaseQuery, EntryQueryable):
    """
    Contentstack provides certain queries that you can use to fetch filtered results.
    You can use queries for Entries API requests.
    [API Reference]:https://www.contentstack.com/docs/developers/apis/content-delivery-api/#queries]

    ---------------------------------------
    Example:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> query = stack.content_type('content_type_uid').query()
            >>> result = query.locale('locale-code').excepts('field_uid').limit(4).skip(5).find()
    """

    def __init__(self, http_instance, content_type_uid):
        super().__init__()
        self.content_type_uid = content_type_uid
        self.http_instance = http_instance
        if self.content_type_uid is None:
            raise PermissionError('You are not allowed here without content_type_uid')
        self.base_url = '{}/content_types/{}/entries' \
            .format(self.http_instance.endpoint, self.content_type_uid)

    def query(self, query_type: QueryType, *query_objects):
        """
        Get entries that satisfy all the conditions provided in the '$and' query.
        Arguments:
            query_objects {Query} -- query_objects for variable number
            of arguments of type Query Object.
        Raises:
            ValueError: If query_objects is None
        Returns:
            Query -- Query object, so you can chain this call.
        ---------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> query = stack.content_type('content_type_uid').query()
            >>> query_one = query.where('field_uid',
                                    QueryOperation.EQUALS, fields=['field1', 'field2', 'field3'])
            >>> query_two = query.where('field_uid',
                                    QueryOperation.INCLUDE, fields=['field1', 'field2', 'field3'])
            >>> result = query.and_query(query_one, query_two).find()
        ---------------------------------
        """
        self.query_params["query"] = json.dumps({query_type.value: [self.parameters]})
        if len(self.parameters):
            self.parameters.clear()
        return self

    def and_query(self, *query_objects):
        """
        Get entries that satisfy all the conditions provided in the '$and' query.
        Arguments:
            query_objects {Query} -- query_objects for variable number
            of arguments of type Query Object.
        Raises:
            ValueError: If query_objects is None
        Returns:
            Query -- Query object, so you can chain this call.
        ---------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> query = stack.content_type('content_type_uid').query()
            >>> query_one = query.where('field_uid',
                                    QueryOperation.EQUALS, fields=['field1', 'field2', 'field3'])
            >>> query_two = query.where('field_uid',
                                    QueryOperation.EQUALS, fields=['field1', 'field2', 'field3'])
            >>> result = query.and_query(query_one, query_two).find()
        ---------------------------------
        """
        self.query_params["query"] = json.dumps({"$and": [self.parameters]})
        if len(self.parameters):
            self.parameters.clear()
        return self

    def or_query(self, *query_objects):
        """
        Get all entries that satisfy at least
        one of the given conditions provided in the '$or' query.
        Arguments:
            query_objects {object} -- query_objects for variable
            number of arguments of type Query Object.
        Raises:
            ValueError: If query_objects is None
        Returns:
            Query -- Query object, so you can chain this call.
        ----------------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> query = stack.content_type('content_type_uid').query()
            >>> query_one = query.where('field_uid',
                                QueryOperation.EQUALS, fields=['field1', 'field2', 'field3'])
            >>> query_two = query.where('field_uid',
                                QueryOperation.EQUALS, fields=['field1', 'field2', 'field3'])
            >>> result = query.or_query(query_one, query_two).find()
        ----------------------------------
        """
        self.query_params["query"] = json.dumps({"$or": [self.parameters]})
        if len(self.parameters):
            self.parameters.clear()
        return self

    def tags(self, *tags):
        """
        Include tags with which to search entries.
        Arguments:
            tags {list of str} -- tags Comma separated objects with which to search entries.
        Returns:
            [Query] -- Query object, so you can chain this call.

        ----------------------------------
        Example:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.tags('black', 'gold', 'silver')
            >>> result = query.find()
        ----------------------------------
        """
        if tags is not None:
            self.query_params["tags"] = ",".join(tags)
        return self

    def search(self, value: str):
        """
        This method provides only the entries matching
        the specified value.
        Arguments:
            value {str} -- value used to match or compare
        Raises:
            ValueError: If value is None
            ValueError: If type od value is not str
        Returns:
            [Query] -- Query object, so you can chain this call.
        -------------------------------------
        [Example]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.search("search_keyword")
            >>> result = query.find()
        -------------------------------------
        """
        if value is not None:
            self.query_params["typeahead"] = value
        return self

    def where_in(self, key: str, query_object):
        """Get entries having values based on referenced fields.
        This query retrieves all entries that satisfy the query
        conditions made on referenced fields.
        Arguments:
            key {str} -- The key to be constrained
        Raises:
            ValueError: If key is None
            ValueError: If key is not str type
        Returns:
            [Query] -- Query object, so you can chain this call.
        -------------------------------------
        [Example]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.where_in("brand")
            >>> result = query.find()
        -------------------------------------
        :param key:
        :type query_object: object
        """
        if isinstance(key, str):
            query_dict = {key: {'$in_query': self.parameters}}
            self.query_params['query'] = query_dict
        else:
            raise ValueError('key should be str type')
        return self

    def where_not_in(self, key, query_object):
        """Get entries having values based on referenced fields.
        This query works the opposite of $in_query and
        retrieves all entries that does not satisfy query
        conditions made on referenced fields.
        Arguments:
            key {str} -- The key to be constrained
        Raises:
            ValueError: If key is None
            ValueError: If key is not str type
        Returns:
            [Query] -- Query object, so you can chain this call.
        -------------------------------------
        [Example]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.where_not_in("brand")
            >>> result = query.find()
        -------------------------------------
        """
        # pylint: disable=W0212
        if isinstance(key, str):
            if isinstance(query_object, Query):
                _query = query_object.__query_dict
                self.__query_dict = {key: {'$nin_query': _query}}
                return self
            raise ValueError('query_object should be Query type')
        raise ValueError('key should be str type')

    def find(self):
        """It fetches the query result.
        List of :class:`Entry <contentstack.entry.Entry>` objects.
        Raises:
            ValueError: If content_type_id is None
            ValueError: If content_type_id is empty or not str type
        Returns:
            list[Entry] -- List of <contentstack.entry.Entry>
        -------------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> result = query.find()
        -------------------------------------
        """
        # if len(self.entry_queryable_param) > 0:
        #     self.query_params.update(self.entry_queryable_param)
        if len(self.parameters) > 0:
            self.query_params["query"] = json.dumps(self.parameters)
        if 'environment' in self.http_instance.headers:
            self.query_params['environment'] = self.http_instance.headers['environment']
        encoded_string = parse.urlencode(self.query_params, doseq=True)
        url = '{}?{}'.format(self.base_url, encoded_string)
        return self.http_instance.get(url)

    def find_one(self):
        """It returns only one result.
        Returns:
            list[Entry] -- List of <contentstack.entry.Entry>
        -------------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> result = query.find_one()
        -------------------------------------
        """
        self.query_params["limit"] = 1
        return self.__execute_query()
