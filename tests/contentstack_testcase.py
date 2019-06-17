from unittest import TestCase
import logging
import unittest
import contentstack.stack


class ContentstackTestcase(TestCase):

    def test_snake_case(self):
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')

    @staticmethod
    def stack_initialisation(self):
        init_stack = contentstack.stack.Stack('blt20962a819b57e233','blt01638c90cc28fb6f','development')
        access_token = init_stack.get_access_token()
        self.assertEqual(access_token, 'blt01638c90cc28fb6f')


# configs = Config()
# configs.set_host('stag-cdn.contentstack.io')
# stack  = stack.Stack(api_key='blt20962a819b57e233', access_token='blt01638c90cc28fb6f', environment='development', config=configs)
# content = stack.content_type('product')
# print(content.get_url())

# stack_config = stack.set_config(configs)
# print('configs host', stack_config.get_host())
# stack.sync(content_type_uid='product', from_date='12-03-2021',langauge='in-eu', publish_type='asset_published')

# content_type=stack.content_type('product')
# entry = content_type.entry('blt7392474')
# sync_params, stack_param = stack.print_object()
# print(sync_params, stack_param, configs.get_host())
