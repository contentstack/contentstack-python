import logging
import unittest
from contentstack import Error, Config
from contentstack import Stack
from tests.creds import stack_keys as keys


class TestStack(unittest.TestCase):

    log = logging.getLogger(__name__)

    def setUp(self):
        # Credentials taken from __init__() class
        from contentstack.config import ContentstackRegion
        self.config = Config()
        self.config.host = 'cdn.contentstack.io'
        self.config.version('v3')
        # self.config.region = ContentstackRegion.EU
        
        api_key = keys().get('api_key')
        access_token = keys().get('access_token')
        environment = keys().get('environment')
        self.stack = Stack(api_key=api_key, access_token=access_token, environment=environment)

        # [Credentials for SyncStack]
        self.sync_api_key = keys().get('sync_api_key')
        self.sync_delivery__token = keys().get('sync_delivery__token')
        self.sync_stack = Stack(api_key=self.sync_api_key, access_token=self.sync_delivery__token, environment='web')

    def test_stack(self):
        self.assertEqual(keys().get('environment'), self.stack.environment)
        self.assertEqual(keys().get('access_token'), self.stack.access_token)
        self.assertEqual(keys().get('api_key'), self.stack.api_key)

    # def test_stack_config_region(self):
    #     from config import ContentstackRegion
    #     config = Config()
    #     config.region = ContentstackRegion.EU
    #     host = config.host
    #     self.assertEqual('cdn.contentstack.com', host)

    def test_stack_config_endpoint(self):
        """[config functional test]
        tests the endpoint        
        """ 
        self.assertEqual('https://cdn.contentstack.io/v3', self.config.endpoint)
        print(self.config.endpoint)

    def test_stack_collaborators(self):
        is_contains = False
        self.stack.collaborators()
        result = self.stack.fetch()
        if result is not None:
            if 'collaborators' in result:
                is_contains = True
            self.assertEqual(True, is_contains)

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

    def test_image_transformation_url_check_query_params_compare(self):
        resp = None
        url = self.stack.image_transform("www.contentstack.io/endpoint", width="500", height="200")
        if url is not None:
            resp = url.split('?')
        if resp[1] is not None:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    # [Sync]

    def test_sync_pagination(self):
        result = self.sync_stack.pagination('bltbb61f31a70a572e6c9506a')
        if result is not None:
            if isinstance(result, Error):
                logging.debug(result)
                self.assertEqual(141, result.error_code)

    def test_init_sync_with_from_date(self):
        from contentstack.stack import SyncResult
        result = self.sync_stack.sync(from_date='2018-01-14T00:00:00.000Z')
        if result is not None:
            print(SyncResult, type(result))
            self.assertEqual(123, result.count)

    def test_init_sync_with_content_type_uid(self):
        from contentstack.stack import SyncResult
        result = self.sync_stack.sync(content_type_uid='session')
        if result is not None:
            print(SyncResult, type(result))
            self.assertEqual(31, result.count)

    def test_init_sync_with_publish_type(self):
        from contentstack.stack import SyncResult
        result = self.sync_stack.sync(publish_type='entry_published')
        if result is not None:
            print(SyncResult, type(result))
            self.assertEqual(123, result.count)

    def test_init_sync(self):
        from contentstack.stack import SyncResult
        result = self.sync_stack.sync(from_date='2018-01-14T00:00:00.000Z', content_type_uid='session',
                                      publish_type='entry_published')
        if result is not None:
            print(SyncResult, type(result))
            self.assertEqual(31, result.count)

    def test_sync_token(self):
        sync_response = self.sync_stack.sync_token('bltbb61f31a70a572e6c9506a')
        if isinstance(sync_response, Error):
            self.assertTrue(109, sync_response.error_code)

    def test_content_types(self):
        # passing query params like below as a dictionary
        query_params = {'include_count': 'true'}
        result = self.stack.get_content_types(query_params)
        if result is not None:
            self.assertEqual(6, len(result))

    def test_content_type(self):
        content_type = self.stack.content_type('product')
        result = content_type.fetch()
        if result is not None:
            if 'schema' in result:
                schema_result = result['schema']
                for schema in schema_result:
                    logging.debug(schema)
                self.assertEqual(list, type(schema_result))
