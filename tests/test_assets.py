import unittest

from urllib3 import Retry
import config
import contentstack
from contentstack.basequery import QueryOperation

ASSET_UID = ''
IMAGE = 'images_(1).jpg'
API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST


class TestAsset(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)
        self.asset_query = self.stack.asset_query()

    def test_011_setting_timeout(self):
        excepted = 13  # setting a custom timeout
        self.stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=config.HOST, timeout=excepted)
        self.assertEqual(excepted, self.stack.timeout)

    def test_12_setting_timeout_failure(self):
        try:
            excepted = 1.00  # setting a custom timeout
            self.stack = contentstack.Stack(
                API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=config.HOST, timeout=excepted)
            self.stack.asset_query().find()
        except TimeoutError:
            self.assertEqual('Timeout expired.', TimeoutError.__doc__)

    def test_013_setting_retry_strategy_unit(self):
        self.stack = contentstack \
            .Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST,
                   retry_strategy=Retry(total=3, backoff_factor=1, status_forcelist=[408]))
        self.assertEqual(1, self.stack.retry_strategy.backoff_factor)
        self.assertEqual(3, self.stack.retry_strategy.total)
        self.assertEqual([408], self.stack.retry_strategy.status_forcelist)

    def test_014_setting_retry_strategy_api(self):
        self.stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT,
            host=HOST,
            retry_strategy=Retry(total=5, backoff_factor=0, status_forcelist=[408, 429]))
        self.assertEqual(0, self.stack.retry_strategy.backoff_factor)
        self.assertEqual(5, self.stack.retry_strategy.total)
        self.assertEqual(
            [408, 429], self.stack.retry_strategy.status_forcelist)

    def test_01_assets_query_initial_run(self):
        result = self.asset_query.find()
        if result is not None:
            assets = result['assets']
            for item in assets:
                if item['title'] == 'if_icon-72-lightning_316154_(1).png':
                    global ASSET_UID
                    ASSET_UID = item['uid']
        self.assertEqual(8, len(assets))

    def test_02_asset_method(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        result = self.asset.relative_urls().include_dimension().fetch()
        if result is not None:
            result = result['asset']['dimension']
            self.assertEqual({'height': 50, 'width': 50}, result)

    def test_03_ASSET_UID(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual(ASSET_UID, result['asset']['uid'])

    def test_04_asset_filetype(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual('image/png', result['asset']['content_type'])

    def test_05_remove_environment(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        self.asset.remove_environment()
        self.assertEqual(
            False, 'environment' in self.asset.http_instance.headers)

    def test_06_add_environment(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        self.asset.environment("dev")
        self.assertEqual(
            'dev', self.asset.http_instance.headers['environment'])

    def test_07_add_param(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        self.asset.params("paramKey", 'paramValue')

    def test_071_check_none_coverage(self):
        try:
            self.asset = self.stack.asset(None)
        except Exception as inst:
            self.assertEqual('Invalid UID. Provide a valid UID and try again.', inst.args[0])

    def test_072_check_none_coverage_test(self):
        try:
            self.asset = self.stack.asset(uid=ASSET_UID)
            self.asset.params(2, 'value')
        except Exception as inst:
            self.assertEqual('Invalid parameters. Provide valid parameters and try again.', inst.args[0])

    def test_08_support_include_fallback(self):
        self.asset = self.stack.asset(uid=ASSET_UID)
        asset_params = self.asset.include_fallback().asset_params
        self.assertEqual({'environment': 'development',
                          'include_fallback': 'true'}, asset_params)

    ############################################
    # ==== Asset Query ====
    ############################################

    def test_09_assets_query(self):
        result = self.asset_query.find()
        if result is not None:
            self.assertEqual(8, len(result['assets']))

    def test_10_assets_base_query_where_exclude_title(self):
        query = self.asset_query.where(
            'title', QueryOperation.EXCLUDES, fields=['women'])
        result = query.find()
        self.assertIsNotNone(result)

    def test_11_assets_base_query_where_equals_str(self):
        query = self.asset_query.where(
            'title', QueryOperation.EQUALS, fields=IMAGE)
        result = query.find()
        self.assertIsNotNone(result)

    def test_12_assets_base_query_where_exclude(self):
        query = self.asset_query.where(
            'file_size', QueryOperation.EXCLUDES, fields=[5990, 3200])
        result = query.find()
        self.assertIsNotNone(result)

    def test_13_assets_base_query_where_includes(self):
        query = self.asset_query.where('title', QueryOperation.INCLUDES,
                                       fields=[IMAGE, 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$in': [
            IMAGE, 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_14_assets_base_query_where_is_less_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN,
                                       fields=[IMAGE, 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lt': [
            IMAGE, 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_15_assets_base_query_where_is_less_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN_OR_EQUAL,
                                       fields=[IMAGE, 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lte': [
            IMAGE, 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_16_assets_base_query_where_is_greater_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN,
                                       fields=[IMAGE, 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gt': [
            IMAGE, 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_17_assets_base_query_where_is_greater_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN_OR_EQUAL,
                                       fields=[IMAGE, 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gte': [
            IMAGE, 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_18_assets_base_query_where_matches(self):
        query = self.asset_query.where('title', QueryOperation.MATCHES,
                                       fields=[IMAGE, 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$regex': [IMAGE, 'images_(2).jpg', 'images_(3).jpg']}},
                         query.parameters)

    def test_19_environment(self):
        query = self.asset_query.environment("dev")
        self.assertEqual('dev', query.http_instance.headers['environment'])

    def test_20_asset_query_with_version(self):
        query = self.asset_query.environment("dev").version("1")
        self.assertEqual({'version': '1'}, query.asset_query_params)

    def test_21_asset_query_with_include_dimension(self):
        query = self.asset_query.environment("dev").include_dimension()
        self.assertEqual({'include_dimension': 'true'},
                         query.asset_query_params)

    def test_22_asset_query_with_relative_url(self):
        query = self.asset_query.environment("dev").relative_url()
        self.assertEqual({'relative_urls': 'true'}, query.asset_query_params)

    def test_23_support_include_fallback(self):
        query = self.asset_query.include_fallback()
        self.assertEqual({'include_fallback': 'true'},
                         query.asset_query_params)

    def test_24_default_find_no_fallback(self):
        entry = self.asset_query.locale('ja-jp').find()
        self.assertIsNotNone(entry)

    def test_25_include_metadata(self):
        entry = self.asset_query.include_metadata()
        self.assertTrue(
            self.asset_query.asset_query_params.__contains__('include_metadata'))

    def test_26_where_with_include_count_and_pagination(self):
        """Test combination of where, include_count, skip, and limit for assets"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .include_count()
                 .skip(2)
                 .limit(5))
        self.assertEqual({"title": IMAGE}, query.parameters)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("2", query.query_params["skip"])
        self.assertEqual("5", query.query_params["limit"])

    def test_27_where_with_order_by_and_pagination(self):
        """Test combination of where, order_by, skip, and limit for assets"""
        query = (self.asset_query
                 .where("file_size", QueryOperation.IS_GREATER_THAN, fields=1000)
                 .order_by_ascending("file_size")
                 .skip(0)
                 .limit(10))
        self.assertEqual({"file_size": {"$gt": 1000}}, query.parameters)
        self.assertEqual("file_size", query.query_params["asc"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_28_multiple_where_conditions_with_all_base_methods(self):
        """Test multiple where conditions combined with all BaseQuery methods for assets"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .where("file_size", QueryOperation.IS_LESS_THAN, fields=10000)
                 .where("content_type", QueryOperation.INCLUDES, fields=["image/jpeg", "image/png"])
                 .include_count()
                 .skip(5)
                 .limit(20)
                 .order_by_descending("created_at")
                 .param("locale", "en-us"))
        
        # Verify parameters
        self.assertEqual(3, len(query.parameters))
        self.assertEqual(IMAGE, query.parameters["title"])
        self.assertEqual({"$lt": 10000}, query.parameters["file_size"])
        self.assertEqual({"$in": ["image/jpeg", "image/png"]}, query.parameters["content_type"])
        
        # Verify query_params
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])
        self.assertEqual("created_at", query.query_params["desc"])
        self.assertEqual("en-us", query.query_params["locale"])

    def test_29_where_with_all_query_operations_combined(self):
        """Test where with all QueryOperation types combined for assets"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .where("file_size", QueryOperation.NOT_EQUALS, fields=0)
                 .where("tags", QueryOperation.INCLUDES, fields=["tag1"])
                 .where("excluded", QueryOperation.EXCLUDES, fields=["tag2"])
                 .where("min_size", QueryOperation.IS_GREATER_THAN, fields=100)
                 .where("max_size", QueryOperation.IS_LESS_THAN, fields=1000000)
                 .where("width", QueryOperation.IS_GREATER_THAN_OR_EQUAL, fields=100)
                 .where("height", QueryOperation.IS_LESS_THAN_OR_EQUAL, fields=2000)
                 .where("has_metadata", QueryOperation.EXISTS, fields=True)
                 .where("filename", QueryOperation.MATCHES, fields=".*\\.jpg$"))
        
        self.assertEqual(10, len(query.parameters))
        self.assertEqual(IMAGE, query.parameters["title"])
        self.assertEqual({"$ne": 0}, query.parameters["file_size"])
        self.assertEqual({"$in": ["tag1"]}, query.parameters["tags"])
        self.assertEqual({"$nin": ["tag2"]}, query.parameters["excluded"])
        self.assertEqual({"$gt": 100}, query.parameters["min_size"])
        self.assertEqual({"$lt": 1000000}, query.parameters["max_size"])
        self.assertEqual({"$gte": 100}, query.parameters["width"])
        self.assertEqual({"$lte": 2000}, query.parameters["height"])
        self.assertEqual({"$exists": True}, query.parameters["has_metadata"])
        self.assertEqual({"$regex": ".*\\.jpg$"}, query.parameters["filename"])

    def test_30_asset_specific_methods_with_base_query_methods(self):
        """Test AssetQuery specific methods combined with BaseQuery methods"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .environment("dev")
                 .version("1")
                 .include_dimension()
                 .relative_url()
                 .include_count()
                 .skip(0)
                 .limit(10)
                 .order_by_ascending("title"))
        
        self.assertEqual({"title": IMAGE}, query.parameters)
        self.assertEqual("dev", query.http_instance.headers["environment"])
        self.assertEqual("1", query.asset_query_params["version"])
        self.assertEqual("true", query.asset_query_params["include_dimension"])
        self.assertEqual("true", query.asset_query_params["relative_urls"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])
        self.assertEqual("title", query.query_params["asc"])

    def test_31_include_fallback_with_where_and_base_methods(self):
        """Test include_fallback combined with where and BaseQuery methods"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .include_fallback()
                 .include_count()
                 .skip(5)
                 .limit(15)
                 .order_by_ascending("title"))
        
        self.assertEqual({"title": IMAGE}, query.parameters)
        self.assertEqual("true", query.asset_query_params["include_fallback"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("15", query.query_params["limit"])
        self.assertEqual("title", query.query_params["asc"])

    def test_32_include_metadata_with_where_and_base_methods(self):
        """Test include_metadata combined with where and BaseQuery methods"""
        query = (self.asset_query
                 .where("file_size", QueryOperation.IS_GREATER_THAN, fields=1000)
                 .include_metadata()
                 .include_count()
                 .skip(10)
                 .limit(20)
                 .order_by_descending("file_size"))
        
        self.assertEqual({"file_size": {"$gt": 1000}}, query.parameters)
        self.assertEqual("true", query.asset_query_params["include_metadata"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])
        self.assertEqual("file_size", query.query_params["desc"])

    def test_33_locale_with_where_and_pagination(self):
        """Test locale combined with where and pagination for assets"""
        query = (self.asset_query
                 .locale('en-us')
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .include_count()
                 .skip(0)
                 .limit(10))
        
        self.assertEqual("en-us", query.asset_query_params["locale"])
        self.assertEqual({"title": IMAGE}, query.parameters)
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_34_include_branch_with_where_and_base_methods(self):
        """Test include_branch combined with where and BaseQuery methods"""
        query = (self.asset_query
                 .where("title", QueryOperation.INCLUDES, fields=[IMAGE, "other.jpg"])
                 .include_branch()
                 .include_count()
                 .skip(0)
                 .limit(10))
        
        self.assertEqual({"title": {"$in": [IMAGE, "other.jpg"]}}, query.parameters)
        self.assertEqual("true", query.asset_query_params["include_branch"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_35_complex_combination_all_asset_and_base_methods(self):
        """Test complex combination of all AssetQuery and BaseQuery methods"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .where("file_size", QueryOperation.IS_GREATER_THAN, fields=1000)
                 .where("content_type", QueryOperation.INCLUDES, fields=["image/jpeg", "image/png"])
                 .environment("production")
                 .version("2")
                 .include_dimension()
                 .relative_url()
                 .include_fallback()
                 .include_metadata()
                 .include_branch()
                 .locale("en-us")
                 .include_count()
                 .skip(10)
                 .limit(50)
                 .order_by_descending("created_at")
                 .param("custom_param", "custom_value"))
        
        # Verify parameters
        self.assertEqual(3, len(query.parameters))
        self.assertEqual(IMAGE, query.parameters["title"])
        self.assertEqual({"$gt": 1000}, query.parameters["file_size"])
        self.assertEqual({"$in": ["image/jpeg", "image/png"]}, query.parameters["content_type"])
        
        # Verify asset_query_params
        self.assertEqual("production", query.http_instance.headers["environment"])
        self.assertEqual("2", query.asset_query_params["version"])
        self.assertEqual("true", query.asset_query_params["include_dimension"])
        self.assertEqual("true", query.asset_query_params["relative_urls"])
        self.assertEqual("true", query.asset_query_params["include_fallback"])
        self.assertEqual("true", query.asset_query_params["include_metadata"])
        self.assertEqual("true", query.asset_query_params["include_branch"])
        self.assertEqual("en-us", query.asset_query_params["locale"])
        
        # Verify query_params
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("50", query.query_params["limit"])
        self.assertEqual("created_at", query.query_params["desc"])
        self.assertEqual("custom_value", query.query_params["custom_param"])

    def test_36_add_params_with_where_and_other_methods(self):
        """Test add_params combined with where and other methods for assets"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .add_params({"locale": "en-us", "include_count": "true"})
                 .skip(5)
                 .limit(10))
        
        self.assertEqual({"title": IMAGE}, query.parameters)
        self.assertEqual("en-us", query.query_params["locale"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("5", query.query_params["skip"])
        self.assertEqual("10", query.query_params["limit"])

    def test_37_remove_param_after_combination(self):
        """Test remove_param after building a complex asset query"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .include_count()
                 .skip(10)
                 .limit(20)
                 .param("key1", "value1")
                 .param("key2", "value2")
                 .remove_param("key1"))
        
        self.assertEqual({"title": IMAGE}, query.parameters)
        self.assertNotIn("key1", query.query_params)
        self.assertEqual("value2", query.query_params["key2"])
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("10", query.query_params["skip"])
        self.assertEqual("20", query.query_params["limit"])

    def test_38_order_by_ascending_then_descending_coexist(self):
        """Test that order_by_ascending and order_by_descending can coexist for assets"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .order_by_ascending("title")
                 .order_by_descending("file_size"))
        
        self.assertEqual({"title": IMAGE}, query.parameters)
        # Both asc and desc can coexist (they use different keys)
        self.assertEqual("title", query.query_params["asc"])
        self.assertEqual("file_size", query.query_params["desc"])

    def test_39_multiple_where_conditions_with_complex_operations(self):
        """Test multiple where conditions with complex operations and all BaseQuery methods for assets"""
        query = (self.asset_query
                 .where("title", QueryOperation.EQUALS, fields=IMAGE)
                 .where("file_size", QueryOperation.IS_GREATER_THAN, fields=1000)
                 .where("file_size", QueryOperation.IS_LESS_THAN, fields=100000)
                 .where("tags", QueryOperation.INCLUDES, fields=["image", "photo"])
                 .where("excluded_tags", QueryOperation.EXCLUDES, fields=["archive"])
                 .include_count()
                 .skip(0)
                 .limit(100)
                 .order_by_descending("file_size")
                 .param("locale", "en-us")
                 .include_fallback())
        
        # Verify all where conditions are present
        self.assertEqual(IMAGE, query.parameters["title"])
        # Note: file_size is overwritten by the second where call - last call wins
        self.assertEqual({"$lt": 100000}, query.parameters["file_size"])
        self.assertEqual({"$in": ["image", "photo"]}, query.parameters["tags"])
        self.assertEqual({"$nin": ["archive"]}, query.parameters["excluded_tags"])
        
        # Verify all query_params
        self.assertEqual("true", query.query_params["include_count"])
        self.assertEqual("0", query.query_params["skip"])
        self.assertEqual("100", query.query_params["limit"])
        self.assertEqual("file_size", query.query_params["desc"])
        self.assertEqual("en-us", query.query_params["locale"])
        self.assertEqual("true", query.asset_query_params["include_fallback"])

# if __name__ == '__main__':
#     unittest.main()
