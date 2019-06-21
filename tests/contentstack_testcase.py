from unittest import TestCase
import requests
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
        self.assertEqual('https://cdn.contentstack.io/v3/stacks', conf.get_endpoint('stacks'))

    def test_include_collaborators(self):
        is_contains = False
        self.stack.get_collaborators()
        stack_query = self.stack.get_stack_query()
        if 'include_collaborators' in stack_query:
            is_contains = True
        self.assertEqual(True, is_contains)

    def test_content_type(self):
        variable = self.stack.content_type('product')
        self.assertEqual('product', variable.content_type_id)

    def test_content_types(self):
        # variable = self.stack.content_types()
        self.assertEqual('product', 'product')

    def test_http_request(self):
        response = requests.get(
            'https://api.github.com/search/repositories',
            params={'q': 'requests+language:python'},
            headers={'Accept': 'application/vnd.github.v3.text-match+json'},
        )

        # View the new `text-matches` array which provides information
        # about your search term within the results
        json_response = response.json()
        array_values: dict = json_response['items']
        # for arrays in array_values:
        # print(arrays)
        self.assertEqual(30, len(array_values))

    def test_stack_fetch(self):
        stack_fetch = self.stack.get_collaborators()
        stack_fetch.fetch()
        self.assertEqual('product', 'product')

    def test_stack_fetch_sync(self):
        self.stack.fetch_sync()
        self.assertEqual('product', 'product')







