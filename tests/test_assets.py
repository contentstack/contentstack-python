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
            self.assertEqual('Please provide a valid uid', inst.args[0])

    def test_072_check_none_coverage_test(self):
        try:
            self.asset = self.stack.asset(uid=ASSET_UID)
            self.asset.params(2, 'value')
        except Exception as inst:
            self.assertEqual('Kindly provide valid params', inst.args[0])

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

# if __name__ == '__main__':
#     unittest.main()
