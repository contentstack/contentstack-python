import unittest

import config
import contentstack

ENTRY_UI = None


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(
            config.api_key, config.delivery_token, config.environment, host=config.host)

    def test_01_run_initial_query(self):
        query = self.stack.content_type('faq').query()
        result = query.find()
        if result is not None:
            global ENTRY_UI
            ENTRY_UI = result['entries'][0]['uid']
            self.assertEqual(ENTRY_UI, result['entries'][0]['uid'])

    def test_02_entry_by_uid(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(ENTRY_UI)
        result = entry.fetch()
        if result is not None:
            ENTRY_UI = result['entry']['uid']
            self.assertEqual(ENTRY_UI, result['entry']['uid'])

    def test_03_entry_environment(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).environment('test')
        self.assertEqual("test", entry.http_instance.headers['environment'])

    def test_04_entry_locale(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).locale('en-eu-ei')
        entry.fetch()
        self.assertEqual('en-eu-ei', entry.entry_param['locale'])

    def test_05_entry_version(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(ENTRY_UI).version(3)
        entry.fetch()
        self.assertEqual(3, entry.entry_param['version'])

    def test_06_entry_params(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).param('param_key', 'param_value')
        entry.fetch()
        self.assertEqual('param_value', entry.entry_param['param_key'])

    def test_07_entry_base_only(self):
        global ENTRY_UI
        entry = self.stack.content_type(
            'faq').entry(ENTRY_UI).only('field_uid')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'only[BASE][]': 'field_uid'}, entry.entry_param)

    def test_08_entry_base_excepts(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).excepts('field_uid')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'except[BASE][]': 'field_uid'}, entry.entry_param)

    def test_10_entry_base_include_reference_only(self):
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(ENTRY_UI).only('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'only[BASE][]': 'field1'},
                         entry.entry_param)

    def test_11_entry_base_include_reference_excepts(self):
        global ENTRY_UI
        entry = self.stack.content_type(
            'faq').entry(ENTRY_UI).excepts('field1')
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
        global ENTRY_UI
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).include_fallback()
        self.assertEqual(
            True, entry.entry_param.__contains__('include_fallback'))

    def test_14_entry_queryable_only(self):
        try:
            entry = self.stack.content_type('faq').entry(ENTRY_UI).only(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field_uid provided", e.args[0])

    def test_15_entry_queryable_excepts(self):
        try:
            entry = self.stack.content_type('faq').entry(ENTRY_UI).excepts(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field_uid provided", e.args[0])

    def test_16_entry_queryable_include_content_type(self):
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).include_content_type()
        self.assertEqual({'include_content_type': 'true', 'include_global_field_schema': 'true'},
                         entry.entry_queryable_param)

    def test_18_entry_queryable_include_reference_content_type_uid(self):
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).include_reference_content_type_uid()
        self.assertEqual({'include_reference_content_type_uid': 'true'},
                         entry.entry_queryable_param)

    def test_19_entry_queryable_add_param(self):
        entry = self.stack.content_type('faq').entry(
            ENTRY_UI).add_param('cms', 'contentstack')
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
