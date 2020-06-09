import logging
import unittest
from tests import credentials
import HtmlTestRunner
import contentstack
from contentstack.entryqueryable import Include


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.access_token = credentials.keys['access_token']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        entry_uid = credentials.keys['entry_uid']
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.entry = stack.content_type('faq').entry(entry_uid)

    def test_entry_by_uid(self):
        result = self.entry.fetch()
        if result is not None:
            logging.info(' => entry result is: {}'.format(result['entry']))
            self.assertEqual('blt53ca1231625bdde4', result['entry']['uid'])

    def test_entry_environment(self):
        self.entry.environment('test')
        self.assertEqual("test", self.entry.http_instance.headers['environment'])

    def test_entry_locale(self):
        self.entry.locale('en-eu-ei').fetch()
        self.assertEqual('en-eu-ei', self.entry.entry_param['locale'])

    def test_entry_version(self):
        self.entry.version(3)
        self.assertEqual(3, self.entry.entry_param['version'])

    def test_entry_params(self):
        self.entry.param('param_key', 'param_value').fetch()
        self.assertEqual('param_value', self.entry.entry_param['param_key'])

    def test_entry_base_only(self):
        self.entry.only('field_uid').fetch()
        self.assertEqual({'only[BASE][]': 'field_uid', 'environment': 'development'}, self.entry.entry_param)

    def test_entry_base_excepts(self):
        self.entry.excepts('field_uid').fetch()
        self.assertEqual({'except[BASE][]': 'field_uid', 'environment': 'development'}, self.entry.entry_param)

    def test_entry_base_include_reference_default(self):
        self.entry.include_reference(Include.DEFAULT, 'reference_field_uid').fetch()
        self.assertEqual({'include[]': 'reference_field_uid', 'environment': 'development'}, self.entry.entry_param)

    def test_entry_base_include_reference_only(self):
        self.entry.include_reference(Include.ONLY, 'reference_field_uid',
                                     field_uid=['field1', 'field2', 'field3']).fetch()
        self.assertEqual({'only': {'reference_field_uid': ['field1', 'field2', 'field3']}},
                         self.entry.entry_param['include[]'])

    def test_entry_base_include_reference_excepts(self):
        self.entry.include_reference(Include.EXCEPT, 'reference_field_uid',
                                     field_uid=['field1', 'field2', 'field3']).fetch()
        self.assertEqual({'except': {'reference_field_uid': ['field1', 'field2', 'field3']}},
                         self.entry.entry_param['include[]'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestEntry)
outfile = open("reports/test_report.html", "w")
runner = HtmlTestRunner.HTMLTestRunner(
    stream=outfile
)
runner.run(suite)
