import unittest

import config
import contentstack
from contentstack.basequery import QueryOperation


class TestAsset(unittest.TestCase):
    global asset_uid

    def setUp(self):
        self.asset_uid = None
        self.stack = contentstack.Stack(
            config.api_key, config.delivery_token, config.environment, host=config.host)
        self.asset_query = self.stack.asset_query()

    def test_011_setting_timeout(self):
        excepted = 13  # setting a custom timeout
        self.stack = contentstack.Stack(config.api_key, config.delivery_token, config.environment, host=config.host,
                                        timeout=excepted)
        self.assertEqual(excepted, self.stack.timeout)

    def test_12_setting_timeout_failure(self):
        try:
            excepted = 0.01  # setting a custom timeout
            self.stack = contentstack.Stack(config.api_key, config.delivery_token, config.environment, host=config.host,
                                            timeout=excepted)
            # self.assertEqual(1, self.stack.timeout)
            result = self.stack.asset_query().find()
        except TimeoutError:
            self.assertEqual('Timeout expired.', TimeoutError.__doc__)

    def test_013_setting_retry_strategy_unit(self):
        from urllib3 import Retry
        self.stack = contentstack.Stack(config.api_key, config.delivery_token,
                                        config.environment, host=config.host,
                                        retry_strategy=Retry(total=3, backoff_factor=1, status_forcelist=[408]))
        self.assertEqual(1, self.stack.retry_strategy.backoff_factor)
        self.assertEqual(3, self.stack.retry_strategy.total)
        self.assertEqual([408], self.stack.retry_strategy.status_forcelist)

    def test_014_setting_retry_strategy_api(self):
        from urllib3 import Retry
        self.stack = contentstack.Stack(config.api_key, config.delivery_token,
                                        config.environment, host=config.host,
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
                    self.asset_uid = item['uid']
                    global asset_uid
                    asset_uid = item['uid']
        self.assertEqual(9, len(assets))

    def test_02_asset_method(self):
        self.asset = self.stack.asset(uid=asset_uid)
        result = self.asset.relative_urls().include_dimension().fetch()
        if result is not None:
            result = result['asset']['dimension']
            self.assertEqual({'height': 50, 'width': 50}, result)

    def test_03_asset_uid(self):

        self.asset = self.stack.asset(uid=asset_uid)
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual(asset_uid, result['asset']['uid'])

    def test_04_asset_filetype(self):
        self.asset = self.stack.asset(uid=asset_uid)
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual('image/png', result['asset']['content_type'])

    def test_05_remove_environment(self):
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset.remove_environment()
        self.assertEqual(
            False, 'environment' in self.asset.http_instance.headers)

    def test_06_add_environment(self):
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset.environment("dev")
        self.assertEqual(
            'dev', self.asset.http_instance.headers['environment'])

    def test_07_add_param(self):
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset.params("paramKey", 'paramValue')
        print(self.asset.base_url)

    def test_071_check_none_coverage(self):
        try:
            self.asset = self.stack.asset(None)
        except Exception as inst:
            self.assertEqual('Please provide a valid uid', inst.args[0])

    def test_072_check_none_coverage_test(self):
        try:
            self.asset = self.stack.asset(uid=asset_uid)
            self.asset.params(2, 'value')
        except Exception as inst:
            self.assertEqual('Kindly provide valid params', inst.args[0])

    def test_08_support_include_fallback(self):
        self.asset = self.stack.asset(uid=asset_uid)
        asset_params = self.asset.include_fallback().asset_params
        self.assertEqual({'environment': 'development',
                          'include_fallback': 'true'}, asset_params)

    ############################################
    # ==== Asset Query ====
    ############################################

    def test_09_assets_query(self):
        result = self.asset_query.find()
        if result is not None:
            self.assertEqual(9, len(result['assets']))

    def test_10_assets_base_query_where_exclude_title(self):
        query = self.asset_query.where(
            'title', QueryOperation.EXCLUDES, fields=['images_(1).jpg'])
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result['assets']))

    def test_11_assets_base_query_where_equals_str(self):
        query = self.asset_query.where(
            'title', QueryOperation.EQUALS, fields='images_(1).jpg')
        result = query.find()
        if result is not None:
            self.assertEqual("images_(1).jpg", result['assets'][0]['filename'])

    def test_12_assets_base_query_where_exclude(self):
        query = self.asset_query.where(
            'file_size', QueryOperation.EXCLUDES, fields=[5990, 3200])
        result = query.find()
        if result is not None:
            self.assertEqual(6, len(result['assets']))

    def test_13_assets_base_query_where_includes(self):
        query = self.asset_query.where('title', QueryOperation.INCLUDES,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$in': [
                         'images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_14_assets_base_query_where_is_less_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lt': [
                         'images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_15_assets_base_query_where_is_less_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN_OR_EQUAL,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lte': [
                         'images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_16_assets_base_query_where_is_greater_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gt': [
                         'images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_17_assets_base_query_where_is_greater_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN_OR_EQUAL,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gte': [
                         'images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_18_assets_base_query_where_matches(self):
        query = self.asset_query.where('title', QueryOperation.MATCHES,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$regex': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}},
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
        _in = ['ja-jp']
        entry = self.asset_query.locale('ja-jp').find()
        self.assertEqual(0, entry['assets'].__len__())
        entry_locale = 'publish_details' in entry
        flag = entry_locale in entry['assets']
        self.assertEqual(False, flag)
