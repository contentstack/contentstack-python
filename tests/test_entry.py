import logging
import unittest
from tests import credentials
import HtmlTestRunner
import contentstack
from contentstack.entryqueryable import Include

global entry_uid


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)

    def test_01_run_initial_query(self):
        result = self.stack.content_type('faq').query().find()
        if result is not None:
            global entry_uid
            entry_uid = result['entries'][0]['uid']
            logging.debug(entry_uid)
            logging.info(' => query result is: {}'.format(result['entries']))
            self.assertEqual('blt53ca1231625bdde4', result['entries'][0]['uid'])

    def test_02_entry_by_uid(self):
        global entry_uid
        result = self.stack.content_type('faq').entry(entry_uid).fetch()
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
        self.assertEqual({'only[BASE][]': 'field_uid', 'environment': 'development'}, entry.entry_param)

    def test_08_entry_base_excepts(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).excepts('field_uid')
        entry.fetch()
        self.assertEqual({'except[BASE][]': 'field_uid', 'environment': 'development'}, entry.entry_param)

    def test_09_entry_base_include_reference_default(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid).include_reference(Include.DEFAULT,
                                                                                  'reference_field_uid')
        entry.fetch()
        self.assertEqual({'include[]': 'reference_field_uid', 'environment': 'development'}, entry.entry_param)

    def test_10_entry_base_include_reference_only(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid) \
            .include_reference(Include.ONLY, 'reference_field_uid',
                               field_uid=['field1', 'field2', 'field3'])
        entry.fetch()
        self.assertEqual({'only': {'reference_field_uid': ['field1', 'field2', 'field3']}},
                         entry.entry_param['include[]'])

    def test_11_entry_base_include_reference_excepts(self):
        global entry_uid
        entry = self.stack.content_type('faq').entry(entry_uid) \
            .include_reference(Include.EXCEPT, 'reference_field_uid',
                               field_uid=['field1', 'field2', 'field3'])
        entry.fetch()
        self.assertEqual({'except': {'reference_field_uid': ['field1', 'field2', 'field3']}},
                         entry.entry_param['include[]'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestEntry)
runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)
