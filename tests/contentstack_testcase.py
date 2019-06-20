from unittest import TestCase

import contentstack
from contentstack.stack import Stack


class ContentstackTestcase(TestCase):

    def setUp(self):
        self.stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development')

    def test_stack(self):
        # self.stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development')
        self.assertEqual('development', self.stack.get_environment())
        self.assertEqual('blt01638c90cc28fb6f', self.stack.get_access_token())
        self.assertEqual('blt20962a819b57e233', self.stack.get_application_key())

    def test_config(self):
        conf = contentstack.config.Config()
        self.assertEqual('v3', conf.get_version())
        self.assertEqual('https://', conf.get_http_protocol())
        self.assertEqual('cdn.contentstack.io', conf.get_host())
        self.assertEqual('https://cdn.contentstack.io/v3/', conf._get_endpoint())

    def test_stack_headers(self):
        is_contains = False
        self.stack.get_collaborators()
        stack_query = self.stack.get_stack_query()
        if 'include_collaborators' in stack_query:
            is_contains = True
        self.assertEqual(True, is_contains)








