import logging
import unittest

from contentstack import Asset, Error
from contentstack.stack import Stack


class TestAsset(unittest.TestCase):
    log = logging.getLogger(__name__)

    def setUp(self):

        api_key: str = 'blt20962a819b57e233'
        access_token: str = 'blt01638c90cc28fb6f'
        env_prod: str = 'production'
        self.asset_uid = 'blt91af1e5af9c3639f'
        self.stack_asset = Stack(api_key=api_key, access_token=access_token, environment=env_prod)

    def test_asset(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        _asset.version(1)
        _asset.relative_urls()
        _asset.include_dimension()
        result: Asset = _asset.fetch()
        if result is not None:
            self.assertEqual(tuple, type(result.dimension))
            logging.debug(result)
        else:
            error_message = Error().error_message
            raise Exception(error_message)

    def test_asset_relative_urls(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        _asset.relative_urls()
        result: Asset = _asset.fetch()
        if result is not None:
            self.assertNotIn('images.contentstack.io/', result.url)
            logging.debug(result)
        else:
            raise Exception(Error.error_message)

    def test_asset_version(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        _asset.version(1)
        result: Asset = _asset.fetch()
        if result is not None:
            self.assertEqual(1, result.get_version)
            logging.debug(result)

    def test_asset_include_dimension(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        _asset.include_dimension()
        result: Asset = _asset.fetch()
        if result is not None:
            self.assertEqual(tuple, type(result.dimension))
            logging.debug('tuple dimension is %s ' + _asset.dimension.__str__())

    def test_asset_remove_header(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        _asset.remove_header('access_token')
        result: Asset = _asset.fetch()
        if result is not None and isinstance(result, Error):
            self.assertEqual(105, result.error_code)
        else:
            self.assertEqual("Default Failed", "Failing")

    def test_asset_check_uid_is_valid(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual(self.asset_uid, result.asset_uid)

    def test_asset_check_filetype(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('image/png', result.filetype)

    def test_asset_file_size(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('63430', result.filesize)

    def test_asset_filename(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('.png', result.filename[-4:])

    def test_asset_url(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual('.png', result.url[-4:])

    def test_asset_to_json(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            self.assertEqual(dict, type(result.to_json))

    def test_asset_create_at(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            sallie: str = result.create_at
            var_shailesh, fileid = sallie.split('T')
            self.assertEqual('2017-01-10', var_shailesh)

    def test_asset_create_by(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            sallie: str = result.create_by
            var_shailesh, fileid = sallie.split('_')
            self.assertEqual('sys', var_shailesh)

    def test_asset_update_at(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result: Asset = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                sallie: str = result.update_at
                var_shailesh, fileid = sallie.split('T')
                self.assertEqual('2017-01-10', var_shailesh)
            else:
                self.assertFalse(True)

    def test_asset_update_by(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result: Asset = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                sallie: str = result.update_by
                var_shailesh, fileid = sallie.split('_')
                self.assertEqual('sys', var_shailesh)
            else:
                self.assertFalse(True)

    def test_asset_tags(self):
        _asset = self.stack_asset.asset(self.asset_uid)
        result = _asset.fetch()
        if result is not None:
            if isinstance(result, Asset):
                self.assertEqual(list, type(result.tags))

    def test_assets(self):
        _asset = self.stack_asset.asset()
        result = _asset.fetch_all()
        if result is not None:
            self.assertEqual(list, type(result))

    # [Asset Library]

    def test_asset_library(self):
        _asset_library = self.stack_asset.asset_library()
        result = _asset_library.fetch_all()
        if result is not None:
            self.assertEqual(list, type(result))
