import unittest

from HtmlTestRunner import HTMLTestRunner

import contentstack
from contentstack.basequery import QueryOperation
from tests import credentials

global asset_uid


class TestAsset(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.asset_query = self.stack.asset_query()

    def test_01_assets_query_initial_run(self):
        result = self.asset_query.find()
        if result is not None:
            global asset_uid
            asset_uid = result['assets'][7]['uid']
            self.assertEqual(8, len(result['assets']))

    def test_02_asset_method(self):
        global asset_uid
        self.asset = self.stack.asset(uid=asset_uid)
        result = self.asset.relative_urls().include_dimension().fetch()
        if result is not None:
            self.assertEqual({'height': 171, 'width': 294}, result['asset']['dimension'])

    def test_03_asset_uid(self):
        global asset_uid
        self.asset = self.stack.asset(uid=asset_uid)
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual(asset_uid, result['asset']['uid'])

    def test_04_asset_filetype(self):
        global asset_uid
        self.asset = self.stack.asset(uid=asset_uid)
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual('image/jpeg', result['asset']['content_type'])

    def test_16_remove_environment(self):
        global asset_uid
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset.remove_environment()
        self.assertEqual(False, 'environment' in self.asset.http_instance.headers)

    def test_17_add_environment(self):
        global asset_uid
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset.environment("dev")
        self.assertEqual('dev', self.asset.http_instance.headers['environment'])

    def test_18_add_param(self):
        global asset_uid
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset.params("paramKey", 'paramValue')
        print(self.asset.base_url)

    ############################################
    # ==== Asset Query ====
    ############################################

    def test_05_assets_query(self):
        result = self.asset_query.find()
        if result is not None:
            self.assertEqual(8, len(result['assets']))

    def test_06_assets_base_query_where_exclude_title(self):
        query = self.asset_query.where('title', QueryOperation.EXCLUDES, fields=['images_(1).jpg'])
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result['assets']))

    def test_07_assets_base_query_where_equals_str(self):
        query = self.asset_query.where('title', QueryOperation.EQUALS, fields='images_(1).jpg')
        result = query.find()
        if result is not None:
            self.assertEqual("images_(1).jpg", result['assets'][0]['filename'])

    def test_08_assets_base_query_where_exclude(self):
        query = self.asset_query.where('file_size', QueryOperation.EXCLUDES, fields=[5990, 3200])
        result = query.find()
        if result is not None:
            self.assertEqual(6, len(result['assets']))

    def test_09_assets_base_query_where_includes(self):
        query = self.asset_query.where('title', QueryOperation.INCLUDES,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$in': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_10_assets_base_query_where_is_less_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lt': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_11_assets_base_query_where_is_less_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN_OR_EQUAL,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lte': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_12_assets_base_query_where_is_greater_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gt': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_13_assets_base_query_where_is_greater_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN_OR_EQUAL,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gte': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)

    def test_14_assets_base_query_where_matches(self):
        query = self.asset_query.where('title', QueryOperation.MATCHES,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$regex': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}},
                         query.parameters)

    def test_15_environment(self):
        query = self.asset_query.environment("dev")
        self.assertEqual('dev', query.http_instance.headers['environment'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestAsset)
runner = HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)
