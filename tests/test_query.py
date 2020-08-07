import logging
import unittest

from HtmlTestRunner import HTMLTestRunner

import contentstack
from contentstack.basequery import QueryOperation
from contentstack.query import QueryType
from contentstack.utility import config_logging
from tests import credentials


class TestQuery(unittest.TestCase):

    def setUp(self):
        config_logging(logging.WARNING)
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.query = stack.content_type('room').query()
        self.query1 = stack.content_type('product').query()
        self.query2 = stack.content_type('app_theme').query()
        self.query3 = stack.content_type('product').query()

    def test_01_functional_or_in_query_type_common_in_query(self):
        query1 = self.query1.where("price", QueryOperation.IS_LESS_THAN, fields=90)
        query2 = self.query2.where("discount", QueryOperation.INCLUDES, fields=[20, 45])
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
        query_limit = self.query3.where('title', QueryOperation.EQUALS, fields='Apple Inc.')
        self.query.where_in('brand', query_limit)
        logging.info(self.query.query_params)
        self.assertEqual({'query': {'brand': {'$in_query': {'title': 'Apple Inc.'}}}}, self.query.query_params)

    def test_08_functional_where_not_in_function_query(self):
        query_limit = self.query3.where('title', QueryOperation.EQUALS, fields='Apple Inc.')
        self.query.where_not_in('brand', query_limit)
        logging.info(self.query.query_params)
        self.assertEqual({'query': {'brand': {'$nin_query': {'title': 'Apple Inc.'}}}}, self.query.query_params)


suite = unittest.TestLoader().loadTestsFromTestCase(TestQuery)
runner = HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)
