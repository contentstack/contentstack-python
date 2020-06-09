from tests import credentials
import unittest
import contentstack
from contentstack.basequery import QueryOperation
import HtmlTestRunner


class TestAsset(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        asset_uid = credentials.keys['asset_uid']
        self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.asset = self.stack.asset(uid=asset_uid)
        self.asset_query = self.stack.asset_query()

    def test_asset_method(self):
        result = self.asset.relative_urls().include_dimension().fetch()
        if result is not None:
            self.assertEqual({'height': 171, 'width': 294}, result['asset']['dimension'])

    def test_asset_uid(self):
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual(credentials.keys['asset_uid'], result['asset']['uid'])

    def test_asset_filetype(self):
        result = self.asset.fetch()
        if result is not None:
            self.assertEqual('image/jpeg', result['asset']['content_type'])

    ############################################
    # ==== Asset Query ====
    ############################################

    def test_assets_query(self):
        result = self.asset_query.find()
        if result is not None:
            self.assertEqual(8, len(result['assets']))

    def test_assets_base_query_where_exclude_title(self):
        query = self.asset_query.where('title', QueryOperation.EXCLUDES, fields=['images_(1).jpg'])
        result = query.find()
        if result is not None:
            self.assertEqual(7, len(result['assets']))

    def test_assets_base_query_where_equals_str(self):
        query = self.asset_query.where('title', QueryOperation.EQUALS, fields='images_(1).jpg')
        result = query.find()
        if result is not None:
            self.assertEqual(1, len(result['assets']))

    def test_assets_base_query_where_exclude(self):
        query = self.asset_query.where('file_size', QueryOperation.EXCLUDES, fields=[5990, 3200])
        result = query.find()
        if result is not None:
            self.assertEqual(6, len(result['assets']))

    def test_assets_base_query_where_includes(self):
        query = self.asset_query.where('title', QueryOperation.INCLUDES,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$in': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)
        # result = query.find()
        # if result is not None:
        #     self.assertEqual(6, len(result['assets']))

    def test_assets_base_query_where_is_less_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lt': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)
        # result = query.find()
        # if result is not None:
        #     self.assertEqual(6, len(result['assets']))

    def test_assets_base_query_where_is_less_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_LESS_THAN_OR_EQUAL,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$lte': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)
        # result = query.find()
        # if result is not None:
        #     self.assertEqual(6, len(result['assets']))

    def test_assets_base_query_where_is_greater_than(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gt': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)
        # result = query.find()
        # if result is not None:
        #     self.assertEqual(6, len(result['assets']))

    def test_assets_base_query_where_is_greater_than_or_equal(self):
        query = self.asset_query.where('title', QueryOperation.IS_GREATER_THAN_OR_EQUAL,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$gte': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}}, query.parameters)
        # result = query.find()
        # if result is not None:
        #     self.assertEqual(6, len(result['assets']))

    def test_assets_base_query_where_matches(self):
        query = self.asset_query.where('title', QueryOperation.MATCHES,
                                       fields=['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg'])
        self.assertEqual({'title': {'$regex': ['images_(1).jpg', 'images_(2).jpg', 'images_(3).jpg']}},
                         query.parameters)


suite = unittest.TestLoader().loadTestsFromTestCase(TestAsset)
runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)