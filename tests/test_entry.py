import logging
import unittest

from HtmlTestRunner import HTMLTestRunner

import contentstack
from tests import credentials

global entry_uid


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)

    def test_01_run_initial_query(self):
        query = self.stack.content_type('faq').query()
        result = query.find()
        if result is not None:
            global entry_uid
            entry_uid = result['entries'][0]['uid']
            logging.debug(entry_uid)
            logging.info(' => query result is: {}'.format(result['entries']))
            self.assertEqual('blt53ca1231625bdde4', result['entries'][0]['uid'])

    def test_02_entry_by_uid(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid)
        result = entry.fetch()
        if result is not None:
            logging.info(' => entry result is: {}'.format(result['entry']))
            self.assertEqual('blt53ca1231625bdde4', result['entry']['uid'])

    def test_03_entry_environment(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).environment('test')
        self.assertEqual("test", entry.http_instance.headers['environment'])

    def test_04_entry_locale(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).locale('en-eu-ei')
        entry.fetch()
        self.assertEqual('en-eu-ei', entry.entry_param['locale'])

    def test_05_entry_version(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).version(3)
        entry.fetch()
        self.assertEqual(3, entry.entry_param['version'])

    def test_06_entry_params(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).param('param_key', 'param_value')
        entry.fetch()
        self.assertEqual('param_value', entry.entry_param['param_key'])

    def test_07_entry_base_only(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).only('field_uid')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'only[BASE][]': 'field_uid'}, entry.entry_param)

    def test_08_entry_base_excepts(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).excepts('field_uid')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'except[BASE][]': 'field_uid'}, entry.entry_param)

    def test_10_entry_base_include_reference_only(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).only('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'only[BASE][]': 'field1'},
                         entry.entry_param)

    def test_11_entry_base_include_reference_excepts(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).excepts('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'except[BASE][]': 'field1'},
                         entry.entry_param)

    def test_12_entry_include_reference_github_issue(self):
        stack_for_products = contentstack.Stack("blt02f7b45378b008ee", "cs5b69faf35efdebd91d08bcf4", "production")
        github_entry = stack_for_products.content_type('product').entry("blte63b2ff6f6414d8e").include_reference(
            ["categories",
             "brand"])
        response = github_entry.fetch()


suite = unittest.TestLoader().loadTestsFromTestCase(TestEntry)
runner = HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)
