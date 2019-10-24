import logging
import unittest
from contentstack import Asset, Error, Config
from contentstack.config import ContentstackRegion
from contentstack.stack import Stack


class TestAsset(unittest.TestCase):

    log = logging.getLogger(__name__)

    def setUp(self):

        # api_key: str = 'blt20962a819b57e233'
        # access_token: str = 'blt01638c90cc28fb6f'
        # env_prod: str = 'production'
        # config = Config()
        # config.region = ContentstackRegion.US
        # Credentials taken from __init__() class

        from tests import stack_keys
        self.credentials = stack_keys()
        api_key = self.credentials['api_key']
        access_token = self.credentials['access_token']
        env = self.credentials['environment_prod']
        self.asset_uid: str = 'blt91af1e5af9c3639f'
        self.__stack = Stack(api_key=api_key, access_token=access_token, environment=env)

    def test_single_asset(self):
        _asset: Asset = self.__stack.asset(self.asset_uid)
        _asset.relative_urls()
        _asset.include_dimension()
        result: Asset = _asset.fetch()
        if result is not None:
            self.assertEqual(dict, type(result.dimension))
            logging.debug(result)

    def test_asset_relative_urls(self):
        _asset = self.__stack.asset(self.asset_uid)
        _asset.relative_urls()
        result = _asset.fetch()
        if result is not None:
            self.assertNotIn('images.contentstack.io/', result.url)
            logging.debug(result)
        else:
            raise Exception(Error.error_message)

    def test_asset_count(self):
        _asset = self.__stack.asset()
        _asset.include_count()
        result: Asset = _asset.fetch_all()
        if result is not None:
            self.assertEqual(37, result.count)
            logging.debug(result)

    def test_asset_include_dimension(self):
        _asset = self.__stack.asset(self.asset_uid)
        _asset.include_dimension()
        result: Asset = _asset.fetch()
        if result is not None:
            self.assertEqual(dict, type(result.dimension))
            logging.debug('tuple dimension is %s ' + _asset.dimension.__str__())

    def test_asset_check_uid_is_valid(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual(self.asset_uid, result.uid)

    def test_asset_check_filetype(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('image/png', result.filetype)

    def test_asset_file_size(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('63430', result.filesize)

    def test_asset_filename(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('.png', result.filename[-4:])

    def test_asset_url(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('.png', result.url[-4:])

    def test_asset_to_json(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual(dict, type(result.json))

    def test_asset_created_at(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            sallie: str = result.created_at
            var_shailesh, fileid = sallie.split('T')
            self.assertEqual('2017-01-10', var_shailesh)

    def test_asset_created_by(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            sallie: str = result.created_by
            var_shailesh, fileid = sallie.split('_')
            self.assertEqual('sys', var_shailesh)

    def test_asset_updated_at(self):
        _asset = self.__stack.asset(self.asset_uid)
        result: Asset = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                sallie: str = result.updated_at
                var_shailesh, fileid = sallie.split('T')
                self.assertEqual('2017-01-10', var_shailesh)
            else:
                self.assertFalse(True)

    def test_asset_updated_by(self):
        _asset = self.__stack.asset(self.asset_uid)
        result: Asset = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                sallie: str = result.updated_by
                var_shailesh, fileid = sallie.split('_')
                self.assertEqual('sys', var_shailesh)
            else:
                self.assertFalse(True)

    def test_asset_tags(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                self.assertEqual(list, type(result.tags))

    def test_asset_version_returns_with_type(self):
        _asset = self.__stack.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                self.assertEqual(int, type(result.version))

    def test_assets(self):
        _asset = self.__stack.asset()
        result = _asset.fetch_all()
        if result is not None:
            self.assertEqual(list, type(result))

    def test_asset_library_check(self):
        _asset_library = self.__stack.asset()
        result = _asset_library.fetch_all()
        if result is not None:
            self.assertEqual(list, type(result))

    def test_asset_library_example(self):
        from contentstack.asset import OrderType
        _asset_library = self.__stack.asset()
        _asset_library.sort('title', OrderType.DESC)
        result = _asset_library.fetch_all()
        if result is not None:
            self.assertEqual(list, type(result))



