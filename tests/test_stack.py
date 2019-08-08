import logging
import unittest

from contentstack import Error
from contentstack.stack import Stack


class TestStack(unittest.TestCase):
    log = logging.getLogger(__name__)

    def setUp(self):

        self.stack = Stack(api_key="blt20962a819b57e233", access_token="blt01638c90cc28fb6f", environment="development")

    def test_stack(self):
        self.assertEqual('development', self.stack.environment)
        self.assertEqual('blt01638c90cc28fb6f', self.stack.access_token)
        self.assertEqual('blt20962a819b57e233', self.stack.application_key)

    def test_config(self):
        from contentstack import Config
        conf = Config()
        self.assertEqual('v3', conf.version())
        self.assertEqual('cdn.contentstack.io', conf.host())
        self.assertEqual('https://cdn.contentstack.io/v3/stacks', conf.endpoint('stacks'))

    def test_include_collaborators(self):
        is_contains = False
        self.stack.collaborators()
        result = self.stack.fetch()
        if result is not None:
            if 'collaborators' in result:
                is_contains = True
            self.assertEqual(True, is_contains)

    def test_stack_fetch_collaborators(self):
        stack_fetch = self.stack.collaborators()
        result = stack_fetch.fetch()
        if result is not None:
            if 'collaborators' in result:
                self.assertTrue(True)

    def test_stack_fetch_discrete_variables(self):
        discrete_var = self.stack.include_discrete_variables()
        result = discrete_var.fetch()
        if result is not None:
            if 'discrete_variables' in result:
                self.assertTrue(True)

    def test_stack_fetch_stack_variables(self):
        stack_var = self.stack.include_stack_variables()
        result = stack_var.fetch()
        if 'stack_variables' in result:
            self.assertTrue(True)

    def test_stack_include_count(self):
        stack_var = self.stack.include_count()
        result = stack_var.fetch()
        if 'stack_variables' in result:
            self.assertTrue(True)

    def test_image_transform(self):
        url = self.stack.image_transform("www.contentstack.io/endpoint",
                                         firstname="sita", lastname="sharma", age=22, phone=1234567890)
        if 'age' in url:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    # [Sync]

    def test_sync_pagination(self):
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        result = sync_stack.pagination('bltbb61f31a70a572e6c9506a')
        if result is not None:
            if isinstance(result, Error):
                logging.debug(result)
                self.assertEqual(141, result.error_code)

    def test_init_sync(self):
        from contentstack.stack import SyncResult
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        result = sync_stack.sync(from_date='2018-01-14T00:00:00.000Z', content_type_uid='session',
                                 publish_type='entry_published')
        if result is not None:
            print(SyncResult, type(result))
            self.assertEqual(31, result.count)

    def test_sync_token(self):
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        response = sync_stack.sync_token('bltbb61f31a70a572e6c9506a')
        items = response.count
        self.assertTrue(9, items)

    # [ContentType class]

    def test_content_type_headers(self):
        variable = self.stack.content_type('product')
        var_ct: dict = variable.headers
        var_head: dict = self.stack.headers
        self.assertEqual(len(var_ct), len(var_head))

    def test_content_types(self):
        result = self.stack.get_content_types()
        if result is not None:
            self.assertEqual(4, len(result))

    def test_content_type(self):
        content_type = self.stack.content_type('product')
        result = content_type.fetch()
        if result is not None:
            if 'schema' in result:
                schema_result = result['schema']
                for schema in schema_result:
                    logging.debug(schema)
                self.assertEqual(list, type(schema_result))
