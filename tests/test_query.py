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

    # ========== Combination Tests for BaseQuery Methods ==========

    def test_22_where_with_include_count_and_pagination(self):
        """Test combination of where, include_count, skip, and limit"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields=self.const_value)
                 .include_count()
                 .skip(5)
                 .limit(10))
        self.assertEqual({"title": self.const_value}, query.parameters)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_23_where_with_order_by_and_pagination(self):
        """Test combination of where, order_by, skip, and limit"""
        query = (self.query3
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=100)
                 .order_by_ascending("price")
                 .skip(0)
                 .limit(20))
        self.assertEqual({"price": {"$gt": 100}}, query.parameters)
        self.assertEqual("price", query.query_params["asc"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])

    def test_24_multiple_where_conditions_with_all_base_methods(self):
        """Test multiple where conditions combined with all BaseQuery methods"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields=self.const_value)
                 .where("price", QueryOperation.IS_LESS_THAN, fields=1000)
                 .where("tags", QueryOperation.INCLUDES, fields=["tag1", "tag2"])
                 .include_count()
                 .skip(10)
                 .limit(50)
                 .order_by_descending("created_at")
                 .param("locale", "en-us"))
        
        # Verify parameters
        self.assertEqual(3, len(query.parameters))
        self.assertEqual(self.const_value, query.parameters["title"])
        self.assertEqual({"$lt": 1000}, query.parameters["price"])
        self.assertEqual({"$in": ["tag1", "tag2"]}, query.parameters["tags"])
        
        # Verify query_params
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("50", query.query_params["limit"])
        self.assertEqual("created_at", query.query_params["desc"])
        self.assertEqual("en-us", query.query_params["locale"])

    def test_25_where_with_all_query_operations_combined(self):
        """Test where with all QueryOperation types combined"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields="Test")
                 .where("price", QueryOperation.NOT_EQUALS, fields=0)
                 .where("tags", QueryOperation.INCLUDES, fields=["tag1"])
                 .where("excluded", QueryOperation.EXCLUDES, fields=["tag2"])
                 .where("min_price", QueryOperation.IS_GREATER_THAN, fields=10)
                 .where("max_price", QueryOperation.IS_LESS_THAN, fields=1000)
                 .where("age", QueryOperation.IS_GREATER_THAN_OR_EQUAL, fields=18)
                 .where("score", QueryOperation.IS_LESS_THAN_OR_EQUAL, fields=100)
                 .where("exists", QueryOperation.EXISTS, fields=True)
                 .where("pattern", QueryOperation.MATCHES, fields="regex.*"))
        
        self.assertEqual(10, len(query.parameters))
        self.assertEqual("Test", query.parameters["title"])
        self.assertEqual({"$ne": 0}, query.parameters["price"])
        self.assertEqual({"$in": ["tag1"]}, query.parameters["tags"])
        self.assertEqual({"$nin": ["tag2"]}, query.parameters["excluded"])
        self.assertEqual({"$gt": 10}, query.parameters["min_price"])
        self.assertEqual({"$lt": 1000}, query.parameters["max_price"])
        self.assertEqual({"$gte": 18}, query.parameters["age"])
        self.assertEqual({"$lte": 100}, query.parameters["score"])
        self.assertEqual({"$exists": True}, query.parameters["exists"])
        self.assertEqual({"$regex": "regex.*"}, query.parameters["pattern"])

    def test_26_tags_with_where_and_pagination(self):
        """Test combination of tags, where, and pagination"""
        query = (self.query
                 .tags('black', 'gold', 'silver')
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=50)
                 .skip(5)
                 .limit(15))
        self.assertEqual("black,gold,silver", query.query_params["tags"])
        self.assertEqual({"price": {"$gt": 50}}, query.parameters)
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("15", query.query_params["limit"])

    def test_27_search_with_where_and_base_methods(self):
        """Test combination of search, where, and BaseQuery methods"""
        query = (self.query
                 .search('search_keyword')
                 .where("status", QueryOperation.EQUALS, fields="active")
                 .include_count()
                 .order_by_ascending("title"))
        self.assertEqual("search_keyword", query.query_params["typeahead"])
        self.assertEqual({"status": "active"}, query.parameters)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("title", query.query_params["asc"])

    def test_28_where_in_with_base_query_methods(self):
        """Test where_in combined with BaseQuery methods"""
        query1 = self.query3.where("title", QueryOperation.EQUALS, fields=self.const_value)
        query = (self.query
                 .where_in("brand", query1)
                 .include_count()
                 .skip(0)
                 .limit(10)
                 .order_by_descending("created_at"))
        
        self.assertEqual({"brand": {"$in_query": {"title": self.const_value}}}, 
                        query.query_params["query"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])
        self.assertEqual("created_at", query.query_params["desc"])

    def test_29_where_not_in_with_base_query_methods(self):
        """Test where_not_in combined with BaseQuery methods"""
        query1 = self.query3.where("title", QueryOperation.EQUALS, fields=self.const_value)
        query = (self.query
                 .where_not_in("brand", query1)
                 .include_count()
                 .skip(5)
                 .limit(20)
                 .order_by_ascending("title"))
        
        self.assertEqual({"brand": {"$nin_query": {"title": self.const_value}}}, 
                        query.query_params["query"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])
        self.assertEqual("title", query.query_params["asc"])

    def test_30_query_operator_with_base_query_methods(self):
        """Test query_operator (OR/AND) combined with BaseQuery methods"""
        query1 = self.query1.where("price", QueryOperation.IS_LESS_THAN, fields=90)
        query2 = self.query2.where("discount", QueryOperation.INCLUDES, fields=[20, 45])
        query = (self.query
                 .query_operator(QueryType.OR, query1, query2)
                 .include_count()
                 .skip(10)
                 .limit(25)
                 .order_by_descending("price"))
        
        self.assertIn("query", query.query_params)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("25", query.query_params["limit"])
        self.assertEqual("price", query.query_params["desc"])

    def test_31_complex_combination_all_methods(self):
        """Test complex combination of all Query and BaseQuery methods"""
        query1 = self.query1.where("price", QueryOperation.IS_LESS_THAN, fields=90)
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Test")
                 .where("status", QueryOperation.INCLUDES, fields=["active", "published"])
                 .tags('tag1', 'tag2', 'tag3')
                 .where_in("category", query1)
                 .include_count()
                 .skip(15)
                 .limit(30)
                 .order_by_ascending("created_at")
                 .param("locale", "en-us")
                 .include_fallback()
                 .include_metadata())
        
        # Verify parameters
        self.assertEqual("Test", query.parameters["title"])
        self.assertEqual({"$in": ["active", "published"]}, query.parameters["status"])
        
        # Verify query_params
        self.assertEqual("tag1,tag2,tag3", query.query_params["tags"])
        self.assertIn("query", query.query_params)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("15", query.query_params["skip"])
        self.assertEqual("30", query.query_params["limit"])
        self.assertEqual("created_at", query.query_params["asc"])
        self.assertEqual("en-us", query.query_params["locale"])
        self.assertEqual("true", query.query_params["include_fallback"])
        self.assertEqual("true", query.query_params["include_metadata"])

    def test_32_locale_with_where_and_pagination(self):
        """Test locale combined with where and pagination"""
        query = (self.query
                 .locale('en-us')
                 .where("title", QueryOperation.EQUALS, fields="Test")
                 .include_count()
                 .skip(0)
                 .limit(10))
        
        # locale is stored in entry_queryable_param, not query_params
        self.assertEqual("en-us", query.entry_queryable_param["locale"])
        self.assertEqual({"title": "Test"}, query.parameters)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_33_include_fallback_with_where_and_base_methods(self):
        """Test include_fallback combined with where and BaseQuery methods"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields=self.const_value)
                 .include_fallback()
                 .include_count()
                 .skip(5)
                 .limit(15)
                 .order_by_ascending("title"))
        
        self.assertEqual({"title": self.const_value}, query.parameters)
        self.assertEqual("true", query.query_params["include_fallback"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("15", query.query_params["limit"])
        self.assertEqual("title", query.query_params["asc"])

    def test_34_include_metadata_with_where_and_base_methods(self):
        """Test include_metadata combined with where and BaseQuery methods"""
        query = (self.query3
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=100)
                 .include_metadata()
                 .include_count()
                 .skip(10)
                 .limit(20)
                 .order_by_descending("price"))
        
        self.assertEqual({"price": {"$gt": 100}}, query.parameters)
        self.assertEqual("true", query.query_params["include_metadata"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])
        self.assertEqual("price", query.query_params["desc"])

    def test_35_add_params_with_where_and_other_methods(self):
        """Test add_params combined with where and other methods"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields=self.const_value)
                 .add_params({"locale": "en-us", "include_count": "true"})
                 .skip(5)
                 .limit(10))
        
        self.assertEqual({"title": self.const_value}, query.parameters)
        self.assertEqual("en-us", query.query_params["locale"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_36_remove_param_after_combination(self):
        """Test remove_param after building a complex query"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields=self.const_value)
                 .include_count()
                 .skip(10)
                 .limit(20)
                 .param("key1", "value1")
                 .param("key2", "value2")
                 .remove_param("key1"))
        
        self.assertEqual({"title": self.const_value}, query.parameters)
        self.assertNotIn("key1", query.query_params)
        self.assertEqual("value2", query.query_params["key2"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])

    def test_37_order_by_ascending_then_descending_coexist(self):
        """Test that order_by_ascending and order_by_descending can coexist"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields=self.const_value)
                 .order_by_ascending("title")
                 .order_by_descending("price"))
        
        self.assertEqual({"title": self.const_value}, query.parameters)
        # Both asc and desc can coexist (they use different keys)
        self.assertEqual("title", query.query_params["asc"])
        self.assertEqual("price", query.query_params["desc"])

    def test_38_multiple_where_conditions_with_complex_operations(self):
        """Test multiple where conditions with complex operations and all BaseQuery methods"""
        query = (self.query3
                 .where("title", QueryOperation.EQUALS, fields="Product")
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=50)
                 .where("price", QueryOperation.IS_LESS_THAN, fields=500)
                 .where("tags", QueryOperation.INCLUDES, fields=["electronics", "sale"])
                 .where("excluded_tags", QueryOperation.EXCLUDES, fields=["discontinued"])
                 .include_count()
                 .skip(0)
                 .limit(100)
                 .order_by_descending("price")
                 .param("locale", "en-us")
                 .include_fallback())
        
        # Verify all where conditions are present
        self.assertEqual("Product", query.parameters["title"])
        # Note: price is overwritten by the second where call - last call wins
        self.assertEqual({"$lt": 500}, query.parameters["price"])
        self.assertEqual({"$in": ["electronics", "sale"]}, query.parameters["tags"])
        self.assertEqual({"$nin": ["discontinued"]}, query.parameters["excluded_tags"])
        
        # Verify all query_params
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("100", query.query_params["limit"])
        self.assertEqual("price", query.query_params["desc"])
        self.assertEqual("en-us", query.query_params["locale"])
        self.assertEqual("true", query.query_params["include_fallback"])
