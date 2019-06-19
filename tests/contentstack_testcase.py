from unittest import TestCase
import logging
import requests
from contentstack.stack import Stack
from contentstack.stack import Stack
from contentstack.HTTPConnection import HTTPConnection


class ContentstackTestcase(TestCase):

    # def setUp(self):
    #    self.stack = contentstack.Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development')
    #    pass

    def test_stack(self):
        self.stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f')
        self.assertEqual(self.stack.get_application_key(), 'blt01638c90cc28fb6f')
        self.assertEqual(self.stack.get_environment(), 'blt01638c90cc28fb6f')
        self.assertEqual(self.stack.get_access_token(), 'blt01638c90cc28fb6f')
        logging.getLogger('stack-test').debug('passed')

    def get_api_response(self):
        requests.get('https://api.github.com')
        print(requests.Response)
        self.assertEqual('abc', 'abc')

    def get_url(self):
        print(self.stack.get_collaborators())
        self.stack._get_url('shailesh')

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
