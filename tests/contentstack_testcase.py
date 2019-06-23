from unittest import TestCase
from contentstack import config
from contentstack.stack import Stack


class ContentstackTestcase(TestCase):

    def setUp(self):
        set_obj = config.Config()
        set_obj.set_host('stag-cdn.contentstack.io')
        self.stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development', set_obj)

    def test_stack(self):
        self.assertEqual('development', self.stack.get_environment())
        self.assertEqual('blt01638c90cc28fb6f', self.stack.get_access_token())
        self.assertEqual('blt20962a819b57e233', self.stack.get_application_key())

    def test_config(self):
        conf = config.Config()
        self.assertEqual('v3', conf.get_version())
        self.assertEqual('https://', conf.get_http_protocol())
        self.assertEqual('cdn.contentstack.io', conf.get_host())
        self.assertEqual('https://cdn.contentstack.io/v3/stacks', conf.get_endpoint('stacks'))

    def test_include_collaborators(self):
        is_contains = False
        self.stack.get_collaborators()
        stack_query = self.stack._get_stack_query()
        if 'include_collaborators' in stack_query:
            is_contains = True
        self.assertEqual(True, is_contains)

    def test_content_type(self):
        variable = self.stack.content_type('product')
        self.assertEqual('product', variable.content_type_id)

    def test_content_types(self):
        result = self.stack.content_types()
        self.assertEqual(list, type(result))
        self.assertEqual(4, len(result))

    def test_stack_fetch_collaborators(self):
        stack_fetch = self.stack.get_collaborators()
        result = stack_fetch.fetch()
        if 'collaborators' in result:
            collaborators = result["collaborators"]
            print("collaborators", collaborators)
            print("collaborators count", len(collaborators))
            self.assertTrue(True)

    def test_stack_fetch_discrete_variables(self):
        discrete_var = self.stack.get_included_descrete_variables()
        result = discrete_var.fetch()
        if 'discrete_variables' in result:
            discrete_variables = result["discrete_variables"]
            print("discrete_var", discrete_variables)
            self.assertTrue(True)

    def test_stack_fetch_stack_variables(self):
        stack_var = self.stack.get_included_stack_variables()
        result = stack_var.fetch()
        if 'stack_variables' in result:
            stack_variables = result["stack_variables"]
            print("stack_variables", stack_variables)
            self.assertTrue(True)

    def test_stack_include_count(self):
        stack_var = self.stack.include_count()
        result = stack_var.fetch()
        if 'stack_variables' in result:
            stack_variables = result["stack_variables"]
            print("stack_variables", stack_variables)
            self.assertTrue(True)

    ##############################################################
    # [Sync-testcases]
    ##############################################################

    def test_sync_pagination(self):
        sync_stack = Stack("blt20962a819b57e233", "cs18efd90468f135a3a5eda3ba", "development")
        stack_sync = sync_stack.sync_pagination('csfakepaginationtoken')
        sync_result = stack_sync.fetch_sync()
        if 'error_code' in sync_result:
            error_code = sync_result["error_code"]
            self.assertEquals(141, error_code)

    def test_init_sync(self):
        sync_stack = Stack("blt20962a819b57e233", "cs18efd90468f135a3a5eda3ba", "production")
        stack_sync = sync_stack.sync(from_date='2018-01-14T00:00:00.000Z', content_type_uid='product', publish_type='entry_published')
        sync_result = stack_sync.fetch_sync()
        self.assertEquals(list, type(sync_result))
        self.assertEquals(7, len(sync_result))
        for data in sync_result:
            type_of_data = data["type"]
            print(type_of_data, data["data"])
            self.assertEquals('entry_published', type_of_data)

    def test_sync_token(self):
        sync_stack = Stack("blt20962a819b57e233", "cs18efd90468f135a3a5eda3ba", "development")
        stack_sync = sync_stack.sync_token('csfakepaginationtoken')
        sync_result = stack_sync.fetch_sync()
        if 'error_code' in sync_result:
            error_code = sync_result["error_code"]
            self.assertEquals(141, error_code)
