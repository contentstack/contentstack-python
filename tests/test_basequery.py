"""
Comprehensive unit tests for BaseQuery class with combination tests
"""
import unittest
import logging
from contentstack.basequery import BaseQuery, QueryOperation


class TestBaseQuery(unittest.TestCase):
    """Test cases for BaseQuery class"""

    def setUp(self):
        """Set up test fixtures"""
        self.query = BaseQuery()

    # ========== Individual Method Tests ==========

    def test_01_where_equals_single_value(self):
        """Test where method with EQUALS operation and single value"""
        query = self.query.where("title", QueryOperation.EQUALS, fields="Apple")
        self.assertEqual({"title": "Apple"}, query.parameters)

    def test_02_where_equals_list_single_item(self):
        """Test where method with EQUALS operation and list with single item"""
        query = self.query.where("title", QueryOperation.EQUALS, fields=["Apple"])
        self.assertEqual({"title": "Apple"}, query.parameters)

    def test_03_where_not_equals(self):
        """Test where method with NOT_EQUALS operation"""
        query = self.query.where("price", QueryOperation.NOT_EQUALS, fields=100)
        self.assertEqual({"price": {"$ne": 100}}, query.parameters)

    def test_04_where_includes(self):
        """Test where method with INCLUDES operation"""
        query = self.query.where("tags", QueryOperation.INCLUDES, fields=["tag1", "tag2"])
        self.assertEqual({"tags": {"$in": ["tag1", "tag2"]}}, query.parameters)

    def test_05_where_excludes(self):
        """Test where method with EXCLUDES operation"""
        query = self.query.where("tags", QueryOperation.EXCLUDES, fields=["tag1", "tag2"])
        self.assertEqual({"tags": {"$nin": ["tag1", "tag2"]}}, query.parameters)

    def test_06_where_is_less_than(self):
        """Test where method with IS_LESS_THAN operation"""
        query = self.query.where("price", QueryOperation.IS_LESS_THAN, fields=100)
        self.assertEqual({"price": {"$lt": 100}}, query.parameters)

    def test_07_where_is_less_than_or_equal(self):
        """Test where method with IS_LESS_THAN_OR_EQUAL operation"""
        query = self.query.where("price", QueryOperation.IS_LESS_THAN_OR_EQUAL, fields=100)
        self.assertEqual({"price": {"$lte": 100}}, query.parameters)

    def test_08_where_is_greater_than(self):
        """Test where method with IS_GREATER_THAN operation"""
        query = self.query.where("price", QueryOperation.IS_GREATER_THAN, fields=100)
        self.assertEqual({"price": {"$gt": 100}}, query.parameters)

    def test_09_where_is_greater_than_or_equal(self):
        """Test where method with IS_GREATER_THAN_OR_EQUAL operation"""
        query = self.query.where("price", QueryOperation.IS_GREATER_THAN_OR_EQUAL, fields=100)
        self.assertEqual({"price": {"$gte": 100}}, query.parameters)

    def test_10_where_exists(self):
        """Test where method with EXISTS operation"""
        query = self.query.where("field", QueryOperation.EXISTS, fields=True)
        self.assertEqual({"field": {"$exists": True}}, query.parameters)

    def test_11_where_matches(self):
        """Test where method with MATCHES operation"""
        query = self.query.where("title", QueryOperation.MATCHES, fields="pattern")
        self.assertEqual({"title": {"$regex": "pattern"}}, query.parameters)

    def test_12_where_multiple_conditions(self):
        """Test multiple where conditions"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=100))
        self.assertEqual({"title": "Apple", "price": {"$gt": 100}}, query.parameters)

    def test_13_include_count(self):
        """Test include_count method"""
        query = self.query.include_count()
        self.assertEqual("true", query.query_params["include_count"])

    def test_14_skip(self):
        """Test skip method"""
        query = self.query.skip(10)
        self.assertEqual("10", query.query_params["skip"])

    def test_15_limit(self):
        """Test limit method"""
        query = self.query.limit(20)
        self.assertEqual("20", query.query_params["limit"])

    def test_16_order_by_ascending(self):
        """Test order_by_ascending method"""
        query = self.query.order_by_ascending("title")
        self.assertEqual("title", query.query_params["asc"])

    def test_17_order_by_descending(self):
        """Test order_by_descending method"""
        query = self.query.order_by_descending("price")
        self.assertEqual("price", query.query_params["desc"])

    def test_18_param(self):
        """Test param method"""
        query = self.query.param("key1", "value1")
        self.assertEqual("value1", query.query_params["key1"])

    def test_19_add_params(self):
        """Test add_params method"""
        query = self.query.add_params({"key1": "value1", "key2": "value2"})
        self.assertEqual("value1", query.query_params["key1"])
        self.assertEqual("value2", query.query_params["key2"])

    def test_20_query(self):
        """Test query method"""
        query = self.query.query("field1", "value1")
        self.assertEqual("value1", query.parameters["field1"])

    def test_21_remove_param(self):
        """Test remove_param method"""
        query = self.query.param("key1", "value1").remove_param("key1")
        self.assertNotIn("key1", query.query_params)

    def test_22_remove_param_nonexistent(self):
        """Test remove_param with non-existent key"""
        query = self.query.remove_param("nonexistent")
        self.assertEqual({}, query.query_params)

    # ========== Combination Tests ==========

    def test_23_where_with_include_count(self):
        """Test combination of where and include_count"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .include_count())
        self.assertEqual({"title": "Apple"}, query.parameters)
        self.assertEqual("true", query.query_params["include_count"])

    def test_24_where_with_skip_and_limit(self):
        """Test combination of where, skip, and limit"""
        query = (self.query
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=100)
                 .skip(5)
                 .limit(10))
        self.assertEqual({"price": {"$gt": 100}}, query.parameters)
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_25_where_with_order_by_ascending(self):
        """Test combination of where and order_by_ascending"""
        query = (self.query
                 .where("category", QueryOperation.INCLUDES, fields=["electronics"])
                 .order_by_ascending("price"))
        self.assertEqual({"category": {"$in": ["electronics"]}}, query.parameters)
        self.assertEqual("price", query.query_params["asc"])

    def test_26_where_with_order_by_descending(self):
        """Test combination of where and order_by_descending"""
        query = (self.query
                 .where("status", QueryOperation.EQUALS, fields="active")
                 .order_by_descending("created_at"))
        self.assertEqual({"status": "active"}, query.parameters)
        self.assertEqual("created_at", query.query_params["desc"])

    def test_27_include_count_with_skip_limit(self):
        """Test combination of include_count, skip, and limit"""
        query = (self.query
                 .include_count()
                 .skip(10)
                 .limit(25))
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("25", query.query_params["limit"])

    def test_28_where_with_param(self):
        """Test combination of where and param"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .param("locale", "en-us"))
        self.assertEqual({"title": "Apple"}, query.parameters)
        self.assertEqual("en-us", query.query_params["locale"])

    def test_29_where_with_add_params(self):
        """Test combination of where and add_params"""
        query = (self.query
                 .where("price", QueryOperation.IS_LESS_THAN, fields=1000)
                 .add_params({"locale": "en-us", "include_count": "true"}))
        self.assertEqual({"price": {"$lt": 1000}}, query.parameters)
        self.assertEqual("en-us", query.query_params["locale"])
        self.assertEqual("true", query.query_params["include_count"])

    def test_30_where_with_query_method(self):
        """Test combination of where and query"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .query("field1", "value1"))
        self.assertEqual({"title": "Apple", "field1": "value1"}, query.parameters)

    def test_31_complex_combination_all_methods(self):
        """Test complex combination of all BaseQuery methods"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=100)
                 .include_count()
                 .skip(5)
                 .limit(20)
                 .order_by_ascending("price")
                 .param("locale", "en-us")
                 .query("category", "electronics"))
        
        # Verify parameters
        self.assertEqual({"title": "Apple", "price": {"$gt": 100}, "category": "electronics"}, 
                        query.parameters)
        
        # Verify query_params
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])
        self.assertEqual("price", query.query_params["asc"])
        self.assertEqual("en-us", query.query_params["locale"])

    def test_32_multiple_where_conditions_all_operations(self):
        """Test multiple where conditions with all query operations"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .where("price", QueryOperation.NOT_EQUALS, fields=0)
                 .where("tags", QueryOperation.INCLUDES, fields=["tag1", "tag2"])
                 .where("excluded_tags", QueryOperation.EXCLUDES, fields=["tag3"])
                 .where("min_price", QueryOperation.IS_GREATER_THAN, fields=10)
                 .where("max_price", QueryOperation.IS_LESS_THAN, fields=1000)
                 .where("age", QueryOperation.IS_GREATER_THAN_OR_EQUAL, fields=18)
                 .where("score", QueryOperation.IS_LESS_THAN_OR_EQUAL, fields=100)
                 .where("field_exists", QueryOperation.EXISTS, fields=True)
                 .where("pattern", QueryOperation.MATCHES, fields="regex.*"))
        
        expected_params = {
            "title": "Apple",
            "price": {"$ne": 0},
            "tags": {"$in": ["tag1", "tag2"]},
            "excluded_tags": {"$nin": ["tag3"]},
            "min_price": {"$gt": 10},
            "max_price": {"$lt": 1000},
            "age": {"$gte": 18},
            "score": {"$lte": 100},
            "field_exists": {"$exists": True},
            "pattern": {"$regex": "regex.*"}
        }
        self.assertEqual(expected_params, query.parameters)

    def test_33_remove_param_after_combination(self):
        """Test remove_param after building a complex query"""
        query = (self.query
                 .include_count()
                 .skip(10)
                 .limit(20)
                 .param("key1", "value1")
                 .param("key2", "value2")
                 .remove_param("key1"))
        
        self.assertNotIn("key1", query.query_params)
        self.assertEqual("value2", query.query_params["key2"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])

    def test_34_order_by_ascending_and_descending_coexist(self):
        """Test that order_by_ascending and order_by_descending can coexist"""
        query = (self.query
                 .order_by_ascending("title")
                 .order_by_descending("price"))
        
        # Both asc and desc can coexist (they use different keys)
        self.assertEqual("title", query.query_params["asc"])
        self.assertEqual("price", query.query_params["desc"])

    def test_35_multiple_params_and_add_params(self):
        """Test combination of param and add_params"""
        query = (self.query
                 .param("key1", "value1")
                 .param("key2", "value2")
                 .add_params({"key3": "value3", "key4": "value4"}))
        
        self.assertEqual("value1", query.query_params["key1"])
        self.assertEqual("value2", query.query_params["key2"])
        self.assertEqual("value3", query.query_params["key3"])
        self.assertEqual("value4", query.query_params["key4"])

    def test_36_where_with_all_query_operations_and_pagination(self):
        """Test where with all operations combined with pagination"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Test")
                 .where("price", QueryOperation.IS_GREATER_THAN, fields=50)
                 .where("tags", QueryOperation.INCLUDES, fields=["tag1"])
                 .include_count()
                 .skip(0)
                 .limit(50)
                 .order_by_descending("created_at"))
        
        self.assertEqual(3, len(query.parameters))
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("50", query.query_params["limit"])
        self.assertEqual("created_at", query.query_params["desc"])

    # ========== Edge Cases and Error Handling ==========

    def test_37_where_with_none_field_uid(self):
        """Test where with None field_uid (should not add to parameters)"""
        query = self.query.where(None, QueryOperation.EQUALS, fields="value")
        self.assertEqual({}, query.parameters)

    def test_38_where_with_none_operation(self):
        """Test where with None operation (should not add to parameters)"""
        query = self.query.where("field", None, fields="value")
        self.assertEqual({}, query.parameters)

    def test_39_param_with_none_key_raises_error(self):
        """Test param with None key raises KeyError"""
        with self.assertRaises(KeyError):
            self.query.param(None, "value")

    def test_40_param_with_none_value_raises_error(self):
        """Test param with None value raises KeyError"""
        with self.assertRaises(KeyError):
            self.query.param("key", None)

    def test_41_query_with_none_key_raises_error(self):
        """Test query with None key raises KeyError"""
        with self.assertRaises(KeyError):
            self.query.query(None, "value")

    def test_42_query_with_none_value_raises_error(self):
        """Test query with None value raises KeyError"""
        with self.assertRaises(KeyError):
            self.query.query("key", None)

    def test_43_remove_param_with_none_raises_error(self):
        """Test remove_param with None key raises ValueError"""
        with self.assertRaises(ValueError):
            self.query.remove_param(None)

    def test_44_where_equals_with_empty_list(self):
        """Test where EQUALS with empty list"""
        query = self.query.where("field", QueryOperation.EQUALS, fields=[])
        self.assertEqual({"field": []}, query.parameters)

    def test_45_where_equals_with_list_multiple_items(self):
        """Test where EQUALS with list containing multiple items"""
        query = self.query.where("field", QueryOperation.EQUALS, fields=["item1", "item2"])
        self.assertEqual({"field": ["item1", "item2"]}, query.parameters)

    def test_46_skip_with_zero(self):
        """Test skip with zero value"""
        query = self.query.skip(0)
        self.assertEqual("0", query.query_params["skip"])

    def test_47_limit_with_zero(self):
        """Test limit with zero value"""
        query = self.query.limit(0)
        self.assertEqual("0", query.query_params["limit"])

    def test_48_limit_with_large_number(self):
        """Test limit with large number"""
        query = self.query.limit(10000)
        self.assertEqual("10000", query.query_params["limit"])

    def test_49_add_params_overwrites_existing(self):
        """Test that add_params overwrites existing params"""
        query = (self.query
                 .param("key1", "value1")
                 .add_params({"key1": "new_value1", "key2": "value2"}))
        
        self.assertEqual("new_value1", query.query_params["key1"])
        self.assertEqual("value2", query.query_params["key2"])

    def test_50_query_overwrites_existing_parameter(self):
        """Test that query overwrites existing parameter"""
        query = (self.query
                 .query("field1", "value1")
                 .query("field1", "value2"))
        
        self.assertEqual("value2", query.parameters["field1"])

    def test_51_where_overwrites_existing_parameter(self):
        """Test that where overwrites existing parameter"""
        query = (self.query
                 .where("title", QueryOperation.EQUALS, fields="Apple")
                 .where("title", QueryOperation.EQUALS, fields="Orange"))
        
        self.assertEqual("Orange", query.parameters["title"])

    def test_52_chaining_returns_self(self):
        """Test that all methods return self for chaining"""
        query = self.query
        self.assertIs(query, query.where("field", QueryOperation.EQUALS, fields="value"))
        self.assertIs(query, query.include_count())
        self.assertIs(query, query.skip(10))
        self.assertIs(query, query.limit(20))
        self.assertIs(query, query.order_by_ascending("field"))
        self.assertIs(query, query.order_by_descending("field"))
        self.assertIs(query, query.param("key", "value"))
        self.assertIs(query, query.add_params({}))
        self.assertIs(query, query.query("key", "value"))
        self.assertIs(query, query.remove_param("key"))


if __name__ == '__main__':
    unittest.main()

