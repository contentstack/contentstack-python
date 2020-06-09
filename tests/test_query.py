import logging
import HtmlTestRunner
from contentstack.utility import config_logging
import unittest
import contentstack
from contentstack.basequery import QueryOperation
from contentstack.query import QueryType
from tests import credentials


class TestQuery(unittest.TestCase):

    def setUp(self):
        config_logging(logging.WARNING)
        self.api_key = credentials.keys['api_key']
        self.access_token = credentials.keys['access_token']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.query = stack.content_type('room').query()
        self.query1 = stack.content_type('product').query()
        self.query2 = stack.content_type('app_theme').query()

    # def test_functional_and_in_query(self):
    #     query1 = self.query1.where("price", QueryOperation.IS_LESS_THAN, fields=90)
    #     query2 = self.query2.where("discount", QueryOperation.INCLUDES, fields=[20, 45])
    #     query = self.query.and_query(query1, query2)
    #     logging.info(query.query_params)
    #     self.assertEqual({'query': '{"$and": [{"price": {"$lt": 90}}, {"discount": {"$in": [20, 45]}}]}'},
    #                      query.query_params)
    #
    # def test_functional_or_in_query(self):
    #     query1 = self.query.where("price", QueryOperation.IS_LESS_THAN, fields=90)
    #     query2 = self.query.where("discount", QueryOperation.INCLUDES, fields=[20, 45])
    #     query = self.query.or_query(query1, query2)
    #     logging.info(query.query_params)
    #     self.assertEqual({'query': '{"$or": [{"price": {"$lt": 90}, "discount": {"$in": [20, 45]}}]}'},
    #                      query.query_params)
    #
    # def test_functional_or_in_query_type_common_in_query(self):
    #     query1 = self.query.where("price", QueryOperation.IS_LESS_THAN, fields=90)
    #     query2 = self.query.where("discount", QueryOperation.INCLUDES, fields=[20, 45])
    #     query = self.query.query_operator(QueryType.OR, query1, query2)
    #     logging.info(query.query_params)
    #     self.assertEqual({'query': '{"$or": [{"price": {"$lt": 90}, "discount": {"$in": [20, 45]}}]}'},
    #                      query.query_params)
    #
    # def test_functional_and_in_query_type_common_in_query(self):
    #     query1 = self.query.where("price", QueryOperation.IS_LESS_THAN, fields=90)
    #     query2 = self.query.where("discount", QueryOperation.INCLUDES, fields=[20, 45])
    #     query = self.query.query_operator(QueryType.AND, query1, query2)
    #     logging.info(query.query_params)
    #     self.assertEqual({'query': '{"$and": [{"price": {"$lt": 90}, "discount": {"$in": [20, 45]}}]}'},
    #                      query.query_params)
    #
    # def test_functional_tag_function_in_query(self):
    #     query = self.query.tags('title', 'location', 'room', 'description')
    #     logging.info(query.query_params)
    #     self.assertEqual({'tags': 'title,location,room,description'},
    #                      query.query_params)
    #
    def test_functional_search_function_in_query(self):
        query = self.query.search('searching_tag')
        logging.info(query.query_params)
        self.assertEqual({'typeahead': 'searching_tag'},
                         query.query_params)
    #
    # def test_functional_search_function_where_in_query(self):
    #     query1 = self.query.where("title", QueryOperation.EQUALS, "Apple Inc")
    #     logging.info(self.query.query_params)
    #     self.query.where_in("brand", query1)
    #     self.assertEqual({'typeahead': 'searching_tag'},
    #                      self.query.query_params)
    #
    # def test_functional_tags_function_query(self):
    #     result = self.query.tags('black', 'gold', 'silver').find()
    #     logging.info(self.query.query_params)
    #     self.assertEqual({'typeahead': 'searching_tag'}, self.query.query_params)
    #
    # def test_functional_search_function_query(self):
    #     result = self.query.search('search_contents').locale('en-us').find()
    #     logging.info(self.query.query_params)
    #     self.assertEqual({'typeahead': 'searching_tag'}, self.query.query_params)
    #
    # def test_functional_where_in_function_query(self):
    #     query_limit = self.query.limit(4)
    #     result = self.query.where_in('title', query_limit).find()
    #     logging.info(self.query.query_params)
    #     self.assertEqual({'typeahead': 'searching_tag'}, self.query.query_params)
    #
    # def test_functional_where_not_in_function_query(self):
    #     query_limit = self.query.limit(4)
    #     self.query.where_not_in('title', query_limit).find()
    #     logging.info(self.query.query_params)
    #     self.assertEqual({'typeahead': 'searching_tag'}, self.query.query_params)


suite = unittest.TestLoader().loadTestsFromTestCase(TestQuery)
outfile = open("test_report_query.html", "w")
runner = HtmlTestRunner.HTMLTestRunner(
                stream=outfile,
                # title='Stack Test Report',
                # description='This demonstrates the report output by Contentstack Python.'
                )
runner.run(suite)
