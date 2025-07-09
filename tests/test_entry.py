import unittest

import config
import contentstack

API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST
FAQ_UID = config.FAQ_UID  # Add this in your config.py
VARIANT_UID = config.VARIANT_UID

class TestEntry(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)

    def test_run_initial_query(self):
        query = self.stack.content_type('faq').query()
        result = query.find()
        if result is not None:
            self.faq_uid = result['entries'][0]['uid']
            print(f'the uid is: {self.faq_uid}')

    def test_entry_by_UID(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID)
        result = entry.fetch()
        if result is not None:
            self.assertEqual(FAQ_UID, result['entry']['uid'])

    def test_03_entry_environment(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).environment('test')
        self.assertEqual("test", entry.http_instance.headers['environment'])

    def test_04_entry_locale(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).locale('en-ei')
        entry.fetch()
        self.assertEqual('en-ei', entry.entry_param['locale'])

    def test_05_entry_version(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).version(3)
        entry.fetch()
        self.assertEqual(3, entry.entry_param['version'])

    def test_06_entry_params(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).param('param_key', 'param_value')
        entry.fetch()
        self.assertEqual('param_value', entry.entry_param['param_key'])

    def test_07_entry_base_only(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).only('field_UID')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'only[BASE][]': 'field_UID'}, entry.entry_param)

    def test_08_entry_base_excepts(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).excepts('field_UID')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'except[BASE][]': 'field_UID'}, entry.entry_param)

    def test_10_entry_base_include_reference_only(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).only('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'only[BASE][]': 'field1'},
                         entry.entry_param)

    def test_11_entry_base_include_reference_excepts(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).excepts('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'except[BASE][]': 'field1'},
                         entry.entry_param)

    def test_12_entry_include_reference_github_issue(self):
        stack_for_products = contentstack.Stack(
            "API_KEY", "DELIVERY_TOKEN", "ENVIRONMENT")
        _entry = stack_for_products.content_type('product').entry("ENTRY_UI").include_reference(
            ["categories",
             "brand"])
        response = _entry.fetch()

    def test_13_entry_support_include_fallback_unit_test(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).include_fallback()
        self.assertEqual(
            True, entry.entry_param.__contains__('include_fallback'))

    def test_14_entry_queryable_only(self):
        try:
            entry = self.stack.content_type('faq').entry(FAQ_UID).only(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field_UID provided", e.args[0])

    def test_entry_queryable_excepts(self):
        try:
            entry = self.stack.content_type('faq').entry(FAQ_UID).excepts(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field_UID provided", e.args[0])

    def test_16_entry_queryable_include_content_type(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).include_content_type()
        self.assertEqual({'include_content_type': 'true', 'include_global_field_schema': 'true'},
                         entry.entry_queryable_param)

    def test_reference_content_type_uid(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).include_reference_content_type_uid()
        self.assertEqual({'include_reference_content_type_uid': 'true'},
                         entry.entry_queryable_param)

    def test_19_entry_queryable_add_param(self):
        entry = self.stack.content_type('faq').entry(FAQ_UID).add_param('cms', 'contentstack')
        self.assertEqual({'cms': 'contentstack'}, entry.entry_queryable_param)

    def test_20_entry_include_fallback(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.entry("878783238783").include_fallback()
        result = entry.fetch()
        self.assertEqual({'environment': 'development',
                          'include_fallback': 'true'}, entry.entry_param)

    def test_21_entry_include_embedded_items(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.entry("878783238783").include_embedded_items()
        result = entry.fetch()
        self.assertEqual({'environment': 'development',
                          'include_embedded_items[]': 'BASE'}, entry.entry_param)

    def test_22_entry_include_metadata(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.entry("878783238783").include_metadata()
        self.assertEqual({'include_metadata': 'true'}, entry.entry_queryable_param)
                
    def test_23_content_type_variants(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.variants(VARIANT_UID).find()
        self.assertIn('variants', entry['entries'][0]['publish_details'])
        
    def test_24_entry_variants(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.entry(FAQ_UID).variants(VARIANT_UID).fetch()
        self.assertIn('variants', entry['entry']['publish_details'])
        
    def test_25_content_type_variants_with_has_hash_variant(self):
        content_type = self.stack.content_type('faq')
        entry = content_type.variants([VARIANT_UID]).find()
        self.assertIn('variants', entry['entries'][0]['publish_details'])
        
    def test_25_content_type_entry_variants_with_has_hash_variant(self):
        content_type = self.stack.content_type('faq').entry(FAQ_UID)
        entry = content_type.variants([VARIANT_UID]).fetch()
        self.assertIn('variants', entry['entry']['publish_details'])
        
        


if __name__ == '__main__':
    unittest.main()
