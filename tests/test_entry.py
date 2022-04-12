import unittest

import config
import contentstack

_uid = 'blt53ca1231625bdde4'
api_key = config.api_key
delivery_token = config.delivery_token
environment = config.environment
env_host = config.host


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(api_key, delivery_token, environment, host=env_host)

    def test_run_initial_query(self):
        query = self.stack.content_type('faq').query()
        result = query.find()
        global _uid
        if result is not None:
            _uid = result['entries'][0]['uid']
            print(f'the uid is: {_uid}')

    def test_entry_by_uid(self):
        global _uid
        entry = self.stack.content_type('faq').entry(_uid)
        result = entry.fetch()
        if result is not None:
            _uid = result['entry']['uid']
            self.assertEqual(_uid, result['entry']['uid'])

    def test_03_entry_environment(self):
        global _uid
        entry = self.stack.content_type('faq').entry(
            _uid).environment('test')
        self.assertEqual("test", entry.http_instance.headers['environment'])

    def test_04_entry_locale(self):
        global _uid
        entry = self.stack.content_type('faq').entry(_uid).locale('en-ei')
        entry.fetch()
        self.assertEqual('en-ei', entry.entry_param['locale'])

    def test_05_entry_version(self):
        global _uid
        entry = self.stack.content_type('faq').entry(_uid).version(3)
        entry.fetch()
        self.assertEqual(3, entry.entry_param['version'])

    def test_06_entry_params(self):
        global _uid
        entry = self.stack.content_type('faq').entry(
            _uid).param('param_key', 'param_value')
        entry.fetch()
        self.assertEqual('param_value', entry.entry_param['param_key'])

    def test_07_entry_base_only(self):
        global _uid
        entry = self.stack.content_type(
            'faq').entry(_uid).only('field_uid')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'only[BASE][]': 'field_uid'}, entry.entry_param)

    def test_08_entry_base_excepts(self):
        global _uid
        entry = self.stack.content_type('faq').entry(
            _uid).excepts('field_uid')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'except[BASE][]': 'field_uid'}, entry.entry_param)

    def test_10_entry_base_include_reference_only(self):
        global _uid
        entry = self.stack.content_type('faq').entry(_uid).only('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'only[BASE][]': 'field1'},
                         entry.entry_param)

    def test_11_entry_base_include_reference_excepts(self):
        global _uid
        entry = self.stack.content_type(
            'faq').entry(_uid).excepts('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'except[BASE][]': 'field1'},
                         entry.entry_param)

    def test_12_entry_include_reference_github_issue(self):
        stack_for_products = contentstack.Stack(
            "api_key", "delivery_token", "environment")
        _entry = stack_for_products.content_type('product').entry("ENTRY_UI").include_reference(
            ["categories",
             "brand"])
        response = _entry.fetch()
        # print(response)
        # categories = response['entry']['categories']
        # self.assertEqual(2, len(categories))

    def test_13_entry_support_include_fallback_unit_test(self):
        global _uid
        entry = self.stack.content_type('faq').entry(
            _uid).include_fallback()
        self.assertEqual(
            True, entry.entry_param.__contains__('include_fallback'))

    def test_14_entry_queryable_only(self):
        try:
            entry = self.stack.content_type('faq').entry(_uid).only(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field_uid provided", e.args[0])

    def test_15_entry_queryable_excepts(self):
        try:
            entry = self.stack.content_type('faq').entry(_uid).excepts(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field_uid provided", e.args[0])

    def test_16_entry_queryable_include_content_type(self):
        entry = self.stack.content_type('faq').entry(
            _uid).include_content_type()
        self.assertEqual({'include_content_type': 'true', 'include_global_field_schema': 'true'},
                         entry.entry_queryable_param)

    def test_18_entry_queryable_include_reference_content_type_uid(self):
        entry = self.stack.content_type('faq').entry(
            _uid).include_reference_content_type_uid()
        self.assertEqual({'include_reference_content_type_uid': 'true'},
                         entry.entry_queryable_param)

    def test_19_entry_queryable_add_param(self):
        entry = self.stack.content_type('faq').entry(
            _uid).add_param('cms', 'contentstack')
        self.assertEqual({'cms': 'contentstack'}, entry.entry_queryable_param)

    def test_20_entry_include_fallback(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.entry("878783238783").include_fallback()
        result = entry.fetch()
        print(result)
        self.assertEqual({'environment': 'development',
                          'include_fallback': 'true'}, entry.entry_param)

    def test_21_entry_include_embedded_items(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.entry("878783238783").include_embedded_items()
        result = entry.fetch()
        print(result)
        self.assertEqual({'environment': 'development',
                          'include_embedded_items[]': 'BASE'}, entry.entry_param)

# if __name__ == '__main__':
#     unittest.main()
