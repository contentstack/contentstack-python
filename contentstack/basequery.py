"""
Missing docstring
Common Query for Entry and Assets
"""
import enum
import logging

log = logging.getLogger(__name__)


# ************* Module basequery.py **************
# Your code has been rated at 10.00/10

class QueryOperation(enum.Enum):
    """
    QueryOperation is enum that Provides Options to perform operation to query the result.

    Available Options for QueryOperation are below.
    EQUALS, NOT_EQUALS, INCLUDES, EXCLUDES, IS_LESS_THAN, IS_LESS_THAN_OR_EQUAL
    IS_GREATER_THAN, IS_GREATER_THAN_OR_EQUAL, EXISTS, MATCHES

    Arguments:
        enum {QueryOperation} -- Type of operation to perform
    """
    EQUALS = ""
    NOT_EQUALS = '$ne'
    INCLUDES = '$in'
    EXCLUDES = '$nin'
    IS_LESS_THAN = '$lt'
    IS_LESS_THAN_OR_EQUAL = '$lte'
    IS_GREATER_THAN = '$gt'
    IS_GREATER_THAN_OR_EQUAL = '$gte'
    EXISTS = '$exists'
    MATCHES = '$regex'


def _get_operation_value(fields):
    value = fields[0] if isinstance(fields, list) and len(fields) == 1 else fields
    return value


class BaseQuery:
    """
    Common Query class works for Query As well as Asset
    """

    def __init__(self):
        self.parameters = {}
        self.query_params = {}

    def where(self, field_uid: str, query_operation: QueryOperation, fields=None):
        """
        Get entries containing the field values matching the condition in the query.
        Arguments:
            field_uid {str} -- [accept field uid for the operation]
            query_operation {QueryOperation} -- Type of operation to perform
            fields {list} - list of string
        """
        if None not in (field_uid, query_operation):
            result = _get_operation_value(fields) if query_operation.name == "EQUALS" \
                else {query_operation.value: fields}
            self.parameters[field_uid] = result
        return self

    def include_count(self):
        """Retrieve count and data of objects in result
        Returns:
            [Query] -- Query object, so you can chain this call.
        ==============================
        [Example:]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'access_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.include_count()
            >>> result = query.find()
        ==============================
        """
        self.query_params["include_count"] = 'true'
        return self

    def skip(self, skip_count: int):
        """
        The number of objects to skip before returning any.
        skip_count No of objects to skip from returned objects
        :param skip_count:
        :return: self
        """
        self.query_params["skip"] = str(skip_count)
        return self

    def limit(self, limit_count: int):
        """
        A limit on the number of objects to return.
        :param limit_count:
        :return: self
        """
        self.query_params["limit"] = str(limit_count)
        return self

    def order_by_ascending(self, key: str):
        """
        you can sort them in the ascending order with respect to the
        value of a specific field in the response body.

        :param key:  key on which ascending order to be implemented
        :return: self
        """
        self.query_params["asc"] = str(key)
        return self

    def order_by_descending(self, key: str):
        """
        you can sort them in the descending order with respect to the value
        of a specific field in the response body.
        :param key:  key on which descending order to be implemented
        :return: self - Class instance, So that method chaining can be performed
        """
        self.query_params["desc"] = str(key)
        return self

    def param(self, key: str, value):
        """
        Adds Parameters to the to the request

        Arguments:
            key {str} -- Key of the parameter
            value {[any]} -- Value of the parameter

        Raises:
            KeyError: When None found in key or value

        Returns:
            [self] -- instance of the class

        -----------------------------------

        [Example]
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'access_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.param("key", "value")
            >>> result = query.find()

        -----------------------------------
        """
        if None in (key, value):
            raise KeyError('Invalid key or value')
        self.query_params[key] = str(value)
        return self

    def add_params(self, param: dict):
        """
        Adds Parameters to the to the request
        Arguments:
            param {dict} --  parameters
        Returns:
            [self] -- Class instance, So that method chaining can be performed
        """
        self.query_params.update(param)
        return self

    def query(self, key: str, value):
        """
        Adds key value pairs to the to the query parameters
        Arguments:
            key {str} -- key of the query param
            value {any} -- value of query param
        Raises:
            `KeyError`: when key or value found None
        Returns:
            self-- Class instance, So that method chaining can be performed
        """
        if None in (key, value):
            raise KeyError('Invalid key or value')
        self.parameters[key] = str(value)
        return self

    def remove_param(self, key: str):
        """
        Remove provided query key from custom query if exist.
        :param key {str} -- The key to be constrained
        :return: self -- So that method chaining can be performed

        ----------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> content_type = stack.content_type('content_type_uid')
            >>> query = content_type.query()
            >>> query = query.remove_query("query_key")
            >>> result = query.find()
        ----------------------------------
        """
        if key is None:
            raise ValueError('Kindly provide valid key')
        if key in self.query_params:
            self.query_params.pop(key, None)
        return self
