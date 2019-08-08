import logging
import unittest
from contentstack.stack import Stack


class TestQuery(unittest.TestCase):
    log = logging.getLogger(__name__)

    def setUp(self):
        api_key: str = 'blt20962a819b57e233'
        access_token: str = 'blt01638c90cc28fb6f'
        env_prod: str = 'production'
        self.stack_query = Stack(api_key=api_key, access_token=access_token, environment=env_prod)

    def test_query_content_type(self):
        query = self.stack_query.content_type('product').query()
        self.assertEqual('product', query.content_type)

    def test_query_headers(self):
        query = self.stack_query.content_type('product').query()
        headers = query.headers
        self.assertEqual(3, len(headers))

    def test_query_remove_headers(self):
        query = self.stack_query.content_type('product').query()
        headers = query.remove_header('environment')
        self.assertEqual(2, len(headers))

    def test_query_add_headers(self):
        query = self.stack_query.content_type('product').query()
        headers = query.add_header('env', 'mishra')
        self.assertEqual(4, len(headers))

    def test_query_where(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us').where("title", "Redmi 3S")
        result, error = query.find()
        if error is None:
            self.assertEqual(1, len(result))

    def test_query_add_query(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.add_query("limit", "8")
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_remove_query(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.add_query("limit", "3")
        query.remove_query('limit')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_and_query(self):

        content_type = self.stack_query.content_type('product')
        base_query = content_type.query()
        base_query.locale('en-us')
        # query where title is equals to Redmi Note 3
        query = content_type.query()
        query.where("title", "Redmi Note 3")
        # query where color is equals to Gold
        sub_query = content_type.query()
        sub_query.where("color", "Gold")
        # adding query in list
        list_array = [query, sub_query]
        # passing query list in and_query
        base_query.and_query(list_array)
        result, error = base_query.find()
        if error is None:
            self.assertEqual(1, len(result))

    def test_query_or_query(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        # query where title is equals to Redmi Note 3
        query1 = content_type.query()
        query1.where("color", "Black")
        # query where color is equals to Gold
        query2 = content_type.query()
        query2.where("color", "Gold")
        # adding query in list
        list_array = [query1, query2]
        # passing query list in and_query
        query.or_query(list_array)
        result, error = query.find()
        if error is None:
            self.assertEqual(5, len(result))

    def test_query_less_than(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than('price_in_usd', 600)
        result, error = query.find()
        if error is None:
            self.assertEqual(5, len(result))

    def test_query_less_than_or_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than_or_equal_to('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(4, len(result))

    def test_query_greater_than(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.greater_than('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(3, len(result))

    def test_query_greater_than_or_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.greater_than_or_equal_to('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(4, len(result))

    def test_query_not_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.not_equal_to('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(6, len(result))

    def test_query_contained_in(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        in_list = [101, 749]
        query.contained_in('price_in_usd', in_list)
        result, error = query.find()
        if error is None:
            self.assertEqual(2, len(result))

    def test_query_not_contained_in(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        in_list = [101, 749]
        query.not_contained_in('price_in_usd', in_list)
        result, error = query.find()
        if error is None:
            self.assertEqual(5, len(result))

    def test_query_exists(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.exists('price_in_usd')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_not_exists(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.not_exists('price_in_usd')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_include_reference(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.include_reference('categories')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_tags(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        taglist = ['Black', 'Gold', 'Silver']
        query.tags(taglist)
        result, error = query.find()
        if error is None:
            self.assertEqual(0, len(result))

    def test_query_ascending(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.ascending('price_in_usd')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_descending(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.descending('price_in_usd')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_except_field_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        listfield = {'gold', 'silver'}
        query.except_field_uid(listfield)
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_only_field_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        listfield = {'gold', 'silver'}
        query.only_field_uid(listfield)
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_only_with_reference_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        fields = ['gold', 'silver']
        query.only_with_reference_uid(fields, 'reference_field_uid')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))
        else:
            self.assertEqual(141, error['error_code'])

    def test_query_except_with_reference_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        listfield = ['gold', 'silver']
        query.except_with_reference_uid(listfield, 'reference_field_uid')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    # def test_query_count(self):

    #    content_type = self.stack_query.content_type('product')
    #    query = content_type.query()
    #    query.locale('en-us')
    #    query.count()
    #    result, error = query.find()
    #    if error is None:
    #        self.assertEqual(7, result)

    def test_query_include_count(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.include_count()
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_include_content_type(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.include_content_type()
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_include_owner(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.include_owner()
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_before_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.before_uid('')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_after_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.after_uid('')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_skip(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.skip(3)
        result, error = query.find()
        if error is None:
            self.assertEqual(4, len(result))

    def test_query_limit(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.limit(3)
        result, error = query.find()
        if error is None:
            self.assertEqual(3, len(result))

    def test_query_regex(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.regex('key', 'regex', 'modifiers')
        result, error = query.find()
        if error is None:
            self.assertEqual(0, len(result))

    def test_query_search(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.search('somekey')
        result, error = query.find()
        if error is None:
            self.assertEqual(0, len(result))

    def test_query_param(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.param('somekey', 'somevalue')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))
