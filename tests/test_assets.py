from tests import credentials
import unittest
import contentstack


class TestAsset(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.access_token = credentials.keys['access_token']
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
