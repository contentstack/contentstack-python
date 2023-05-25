import logging
import unittest
import config
import contentstack
from contentstack.basequery import QueryOperation
from contentstack.query import QueryType

API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST

class TestQuery(unittest.TestCase):

    def setUp(self):
        self.const_value = 'Apple Inc.'
        self.stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)
        self.query = self.stack.content_type('room').query()
        self.query1 = self.stack.content_type('product').query()
        self.query2 = self.stack.content_type('app_theme').query()
        self.query3 = self.stack.content_type('product').query()

    def test_01_functional_or_in_query_type_common_in_query(self):
        query1 = self.query1.where(
            "price", QueryOperation.IS_LESS_THAN, fields=90)
        query2 = self.query2.where(
            "discount", QueryOperation.INCLUDES, fields=[20, 45])
        query = self.query.query_operator(QueryType.OR, query1, query2)
        logging.info(query.query_params)
        self.assertEqual({'query': '{"$or": [{"price": {"$lt": 90}}, {"discount": {"$in": [20, 45]}}]}'},
                         query.query_params)

    def test_02_functional_tag_function_in_query(self):
        query = self.query.tags('title', 'location', 'room', 'description')
        logging.info(query.query_params)
        self.assertEqual({'tags': 'title,location,room,description'},
                         query.query_params)

    def test_03_functional_search_function_in_query(self):
        query = self.query.search('searching_tag')
        logging.info(query.query_params)
        self.assertEqual({'typeahead': 'searching_tag'},
                         query.query_params)

    def test_04_functional_search_function_where_in_query(self):
        query1 = self.query.where("title", QueryOperation.EQUALS, "Apple Inc")
        self.query.where_in("brand", query1)
        self.assertEqual({'query': {'brand': {'$in_query': {'title': 'Apple Inc'}}}},
                         self.query.query_params)

    def test_05_functional_tags_function_query(self):
        tags = self.query.tags('black', 'gold', 'silver')
        logging.info(tags.query_params)
        self.assertEqual({'tags': 'black,gold,silver'}, tags.query_params)

    def test_06_functional_search_function_query(self):
        params = self.query.search('search_contents').locale('en-us')
        logging.info(params.query_params)
        self.assertEqual({'typeahead': 'search_contents'}, params.query_params)

    def test_07_functional_where_in_function_query_limit(self):
        query_limit = self.query3.where(
            'title', QueryOperation.EQUALS, fields=self.const_value)
        self.query.where_in('brand', query_limit)
        logging.info(self.query.query_params)
        self.assertEqual({'query': {'brand': {'$in_query': {
            'title': self.const_value}}}}, self.query.query_params)

    def test_08_functional_where_not_in_function_query(self):
        query_limit = self.query3.where(
            'title', QueryOperation.EQUALS, fields=self.const_value)
        self.query.where_not_in('brand', query_limit)
        logging.info(self.query.query_params)
        self.assertEqual({'query': {'brand': {'$nin_query': {
            'title': self.const_value}}}}, self.query.query_params)

    def test_09_base_query_include_count(self):
        query = self.query3.include_count()
        logging.info(query.base_url)
        self.assertEqual('true', query.query_params['include_count'])

    def test_10_base_query_skip(self):
        query = self.query3.skip(3)
        logging.info(query.base_url)
        self.assertEqual('3', query.query_params['skip'])

    def test_11_base_query_limit(self):
        query = self.query3.limit(3)
        logging.info(query.base_url)
        self.assertEqual('3', query.query_params['limit'])

    def test_12_base_query_order_by_ascending(self):
        query = self.query3.order_by_ascending('title')
        logging.info(query.base_url)
        self.assertEqual('title', query.query_params['asc'])

    def test_13_base_query_order_by_descending(self):
        query = self.query3.order_by_descending('title')
        logging.info(query.base_url)
        self.assertEqual('title', query.query_params['desc'])

    def test_14_base_query_param(self):
        query = self.query3.param("keyOne", 'valueOne')
        logging.info(query.base_url)
        self.assertEqual('valueOne', query.query_params['keyOne'])

    def test_15_base_query_add_params(self):
        query = self.query3.add_params(
            {'keyOne': 'valueOne', 'keyTwo': 'valueTwo'})
        logging.info(query.base_url)
        self.assertEqual(2, len(query.query_params))

    def test_16_base_query(self):
        query = self.query3.query('keyOne', 'valueOne')
        logging.info(query.base_url)
        self.assertEqual('valueOne', query.parameters['keyOne'])

    def test_17_base_remove_param(self):
        query = self.query3.remove_param("keyOne")
        logging.info(query.base_url)

    def test_18_support_include_fallback(self):
        query = self.query3.include_fallback()
        logging.info(query.base_url)
        self.assertEqual('true', query.query_params['include_fallback'])

    def test_18_support_include_fallback_url(self):
        query = self.query3.include_fallback()
        logging.info(query.base_url)
        self.assertEqual({'include_fallback': 'true'}, query.query_params)

    def test_19_default_find_without_fallback(self):
        entry = self.query.locale('en-gb').find()
        self.assertEqual(1, len(entry))

    def test_20_default_find_with_fallback(self):
        entry = self.query.locale('en-gb').include_fallback().find()
        entries = entry['entries']
        self.assertEqual(0, len(entries))

    def test_21_include_metadata(self):
        entry = self.query.locale('en-gb').include_metadata().find()
        entries = entry['entries']
        self.assertEqual(0, len(entries))
