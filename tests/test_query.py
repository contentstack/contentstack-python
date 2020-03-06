import logging
import unittest
from contentstack import Stack


class TestQuery(unittest.TestCase):

    def setUp(self):

        from tests.creds import query_keys
        self.credentials = query_keys()
        api_key = self.credentials['api_key']
        access_token = self.credentials['access_token']
        environment = self.credentials['environment']
        self.stack_query = Stack(api_key=api_key, access_token=access_token, environment=environment)

    def test_query_content_type(self):
        query = self.stack_query.content_type('product').query()
        self.assertEqual('product', query.content_type)

    def test_query_remove_headers(self):
        query = self.stack_query.content_type('product').query()
        query.add_header('environment', 'production')
        query.add_header('environment2', 'production2')
        query.add_header('environment3', 'production3')
        query_obj = query.remove_header('environment3')
        self.assertEqual(2, len(query_obj.headers))

    def test_query_check_additional_params_in_add_headers(self):
        # functional testing
        query = self.stack_query.content_type('product').query()
        query.add_header('header1', 'header_value1')
        query.add_header('header2', 'header_value2')
        query.add_header('contentstack_header', 'contentstack')
        self.assertEqual(3, len(query.headers))

    # ==================================
    def test_query_is_equal_where_condition(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.where("color", "Gold")
        result = query.find()
        if result is not None:
            self.assertEqual(2, len(result))

    def test_query_add_query(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.add_query("limit", "8")
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result))

    def test_query_remove_query(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.add_query("limit", "3")
        query.remove_query('limit')
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result))

    def test_query_check_locale(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        result = query.find()
        if result is not None:
            if isinstance(result, list):
                entry_locale = result[0].locale
                self.assertEqual('en-us', entry_locale)
            else:
                self.assertFalse(True)

    # ==================================
    def test_query_where_condition_check(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.where('title', 'Galaxy Note')
        result = query.find()
        if result is not None:
            if isinstance(result, list):
                for value in result:
                    entry_title = value.title
                    self.assertEqual('Galaxy Note', entry_title)
            else:
                self.assertFalse(True)

    def test_query_adding_locale_param_for_add_query(self):
        query = self.stack_query.content_type('product').query()
        query.add_query('locale', 'en-us')
        result = query.find()
        if result is not None:
            if isinstance(result, list):
                for value in result:
                    entry_locale = value.locale
                    self.assertEqual('en-us', entry_locale)
            else:
                self.assertFalse(True)

    def test_query_and_query(self):

        content_type = self.stack_query.content_type('product')
        base_query = content_type.query()
        query = content_type.query()
        query.where("title", "Galaxy Note")
        sub_query = content_type.query()
        sub_query.where("color", "Gold")
        base_query.and_query(query, sub_query)
        result = base_query.find()
        if result is not None:
            for entry in result:
                check_title = entry.title
                check_color = entry.get_string('color')
                self.assertTrue(True)
                logging.info('\n\ncheck_title = {}\ncheck_color={}'.format(check_title, check_color))
        else:
            self.assertFalse(True)

    # ==================================
    def test_query_or_query(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query1 = content_type.query()
        query1.where("color", "Black")
        query2 = content_type.query()
        query2.where("color", "Gold")
        query.or_query(query1, query2)
        result = query.find()
        if result is not None:
            for entry in result:
                check_color = entry.get_string('color')
                if check_color == 'Gold' or check_color == 'Black':
                    self.assertTrue(True)
                else:
                    self.assertFalse(True)
        else:
            self.assertFalse(True)

    # ==================================
    def test_query_less_than(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than('price_in_usd', 600)
        result = query.find()
        if result is not None:
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd < 600:
                    self.assertTrue(True)
                else:
                    self.assertFalse(True)
        else:
            self.assertFalse(True)

    # ==================================
    def test_query_less_than_or_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than_or_equal_to('price_in_usd', 146)
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd <= 146:
                    self.assertTrue(True)
                else:
                    self.assertFalse(True)
        else:
            self.assertFalse(True)

    # ==================================
    def test_query_greater_than(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.greater_than('price_in_usd', 146)
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd > 146:
                    self.assertTrue(True)
                else:
                    self.assertFalse(True)
        else:
            self.assertFalse(True)

    # ==================================
    def test_query_greater_than_or_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.greater_than_or_equal_to('price_in_usd', 146)
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd >= 146:
                    self.assertTrue(True)
                else:
                    self.assertFalse(True)
        else:
            self.assertFalse(True)

    # ==================================
    def test_query_not_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.not_equal_to('price_in_usd', 146)
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd == 146:
                    self.assertFalse(True)
        else:
            self.assertFalse(True)

    def test_query_contained_in(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.contained_in('price_in_usd', 101, 749)
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd == 101 or 749:
                    self.assertTrue(True)
        else:
            self.assertFalse(True)

    def test_query_not_contained_in(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.not_contained_in('price_in_usd', 101, 749)
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                if price_in_usd != 101 or 749:
                    self.assertTrue(True)
        else:
            self.assertFalse(True)

    def test_query_exists(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.exists('price_in_usd')
        result = query.find()
        counter = 0
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                print('price_in_usd {}'.format(price_in_usd))
                counter = counter + 1
        self.assertEqual(7, counter)

    def test_query_not_exists(self):
        # this test need to check
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.not_exists('price_in_usd')
        result = query.find()
        counter = 0
        if isinstance(result, list):
            for entry in result:
                price_in_usd = entry.get('price_in_usd')
                print('price_in_usd {}'.format(price_in_usd))
                counter = counter + 1
        self.assertEqual(7, counter)

    def test_query_include_reference(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.include_reference('categories')
        result = query.find()
        if isinstance(result, list):
            for entry in result:
                categories = entry.get('categories')
                print('categories {} '.format(categories))
        self.assertEqual(7, len(result))

    # ============================================================
    # ============================================================
    def test_query_tags(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.tags('Black', 'Gold')
        result = query.find()
        if result is not None:
            if isinstance(result, list):
                for entry in result:
                    color = entry.get('color')
            self.assertEqual(7, len(result))
        else:
            self.assertEqual(None, result)

    def test_query_ascending(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.ascending('price_in_usd')
        result = query.find()
        if result is not None:
            previous = 0
            if isinstance(result, list):
                for entry in result:
                    price_in_usd = entry.get('price_in_usd')
                    if previous < price_in_usd:
                        self.assertTrue(True)
                    else:
                        self.assertTrue(False)
                    previous = price_in_usd

    def test_query_descending(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.descending('price_in_usd')
        result = query.find()
        if isinstance(result, list):
            for index in range(len(result) - 1):
                current_price = result[index].get('price_in_usd')
                next_price = result[index + 1].get('price_in_usd')
                # Descending Order. Numbers are said to be in descending order when they are arranged from the
                # largest to the smallest number.
                if current_price > next_price:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)

    def test_query_except_field_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.except_field_uid("color")
        result = query.find()
        if result is not None and isinstance(result, list):
            for index in range(len(result)):
                color = result[index].get('color')
                if color is None:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)

    def test_query_only_with_field_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.only('price_in_usd', 'color')
        result = query.find()
        if result is not None:
            if len(result) > 0:
                self.assertEqual(7, len(result))
            else:
                self.assertTrue(False)

    def test_query_only_with_reference_uid(self):
        from contentstack import Error
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.only_with_reference_uid('categories', 'gold', 'silver')
        result = query.find()
        if result is not None:
            if isinstance(result, list):
                self.assertEqual(7, len(result))
            if isinstance(result, Error):
                self.assertEqual(141, result.error_code)

    def test_query_except_with_reference_uid(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.except_with_reference_uid('categories', 'gold', 'silver')
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result))

    def test_query_include_count(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.include_count()
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result))

    def test_query_include_content_type(self):
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.include_content_type()
        result = query.find()
        if result is not None:
            for entry in result:
                brand = entry.json['brand']
                #content_type_uid = brand[0]['_content_type_uid']
                if len(brand) == 1:
                    self.assertTrue(True)
                else:
                    self.assertFalse(True)

    def test_query_skip(self):
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        result = query.find()
        if result is not None:
            counter = len(result)
            query.skip(3)
            result = query.find()
            if result is not None:
                skip_counter = len(result)
                if counter - skip_counter == 3:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)

    def test_query_limit(self):
        LIMIT = 3
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.limit(LIMIT)
        result = query.find()
        if result is not None:
            self.assertEqual(LIMIT, len(result))

    # ==================================
    def test_query_regex(self):
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.regex('color', '^Bla')
        result = query.find()
        if result is not None:
            self.assertEqual(3, len(result))

    # ==================================
    def test_query_regex_with_option(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.regex('color', '^Bla', 'i')
        result = query.find()
        if result is not None:
            self.assertEqual(3, len(result))

    def test_query_search(self):
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.search('somekey')
        result = query.find()
        if result is not None:
            self.assertEqual(0, len(result))

    def test_query_param(self):
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.param('somekey', 'somevalue')
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result))

    def test_query_include_reference_content_type_uid(self):
        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.include_reference_content_type_uid()
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result))

    # ==================================
    def test_query_in_query_reference(self):
        stack = Stack(api_key='blt02f7b45378b008ee', access_token='bltb327f978f247e1c8', environment='production')
        content_type = stack.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.where('title', 'Apple Inc.')
        query.where_in('brand', query)
        result = query.find()
        if result is not None:
            self.assertEqual(2, len(result))
        else:
            self.assertTrue(False)

    # ==================================
    def test_query_not_in_query_reference(self):
        stack = Stack(api_key='blt02f7b45378b008ee', access_token='bltb327f978f247e1c8', environment='production')
        content_type = stack.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.where('title', 'Apple Inc.')
        query.where_not_in('brand', query)
        result = query.find()
        if result is not None:
            self.assertEqual(5, len(result))
        else:
            self.assertTrue(False)
