import unittest

import config
import contentstack

API_KEY = config.API_KEY
DELIVERY_TOKEN = config.DELIVERY_TOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST
COMPLEX_ENTRY_UID = config.COMPLEX_ENTRY_UID
COMPLEX_CONTENT_TYPE_UID = config.COMPLEX_CONTENT_TYPE_UID
VARIANT_UID = config.VARIANT_UID

class TestEntry(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)

    def test_run_initial_query(self):
        query = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).query()
        result = query.find()
        if result is not None:
            self.faq_uid = result['entries'][0]['uid']
            print(f'the uid is: {self.faq_uid}')

    def test_entry_by_UID(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID)
        result = entry.fetch()
        if result is not None:
            self.assertEqual(COMPLEX_ENTRY_UID, result['entry']['uid'])

    def test_03_entry_environment(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).environment('test')
        self.assertEqual("test", entry.http_instance.headers['environment'])

    def test_04_entry_locale(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).locale('en-ei')
        entry.fetch()
        self.assertEqual('en-ei', entry.entry_param['locale'])

    def test_05_entry_version(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).version(3)
        entry.fetch()
        self.assertEqual(3, entry.entry_param['version'])

    def test_06_entry_params(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).param('param_key', 'param_value')
        entry.fetch()
        self.assertEqual('param_value', entry.entry_param['param_key'])

    def test_07_entry_base_only(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).only('field_UID')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'only[BASE][]': 'field_UID'}, entry.entry_param)

    def test_08_entry_base_excepts(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).excepts('field_UID')
        entry.fetch()
        self.assertEqual({'environment': 'development',
                          'except[BASE][]': 'field_UID'}, entry.entry_param)

    def test_10_entry_base_include_reference_only(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).only('field1')
        entry.fetch()
        self.assertEqual({'environment': 'development', 'only[BASE][]': 'field1'},
                         entry.entry_param)

    def test_11_entry_base_include_reference_excepts(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).excepts('field1')
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
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).include_fallback()
        self.assertEqual(
            True, entry.entry_param.__contains__('include_fallback'))

    def test_14_entry_queryable_only(self):
        try:
            entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).only(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field UID. Provide a valid UID and try again.", e.args[0])

    def test_entry_queryable_excepts(self):
        try:
            entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).excepts(4)
            result = entry.fetch()
            self.assertEqual(None, result['uid'])
        except KeyError as e:
            if hasattr(e, 'message'):
                self.assertEqual("Invalid field UID. Provide a valid UID and try again.", e.args[0])

    def test_16_entry_queryable_include_content_type(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).include_content_type()
        self.assertEqual({'include_content_type': 'true', 'include_global_field_schema': 'true'},
                         entry.entry_queryable_param)

    def test_reference_content_type_uid(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).include_reference_content_type_uid()
        self.assertEqual({'include_reference_content_type_uid': 'true'},
                         entry.entry_queryable_param)

    def test_19_entry_queryable_add_param(self):
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).add_param('cms', 'contentstack')
        self.assertEqual({'cms': 'contentstack'}, entry.entry_queryable_param)

    def test_20_entry_include_fallback(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.entry("878783238783").include_fallback()
        result = entry.fetch()
        self.assertEqual({'environment': 'development',
                          'include_fallback': 'true'}, entry.entry_param)

    def test_21_entry_include_embedded_items(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.entry("878783238783").include_embedded_items()
        result = entry.fetch()
        self.assertEqual({'environment': 'development',
                          'include_embedded_items[]': 'BASE'}, entry.entry_param)

    def test_22_entry_include_metadata(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.entry("878783238783").include_metadata()
        self.assertEqual({'include_metadata': 'true'}, entry.entry_queryable_param)
                
    def test_23_content_type_variants(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.variants(VARIANT_UID).find()
        self.assertIn('variants', entry['entries'][0]['publish_details'])
        
    def test_24_entry_variants(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.entry(COMPLEX_ENTRY_UID).variants(VARIANT_UID).fetch()
        self.assertIn('variants', entry['entry']['publish_details'])
        
    def test_25_content_type_variants_with_has_hash_variant(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.variants([VARIANT_UID]).find()
        self.assertIn('variants', entry['entries'][0]['publish_details'])
        
    def test_25_content_type_entry_variants_with_has_hash_variant(self):
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID)
        entry = content_type.variants([VARIANT_UID]).fetch()
        self.assertIn('variants', entry['entry']['publish_details'])

    # ========== Additional Test Cases ==========

    def test_26_entry_method_chaining_locale_version(self):
        """Test entry method chaining with locale and version"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .locale('en-us')
                 .version(1))
        entry.fetch()
        self.assertEqual('en-us', entry.entry_queryable_param['locale'])
        self.assertEqual(1, entry.entry_param['version'])

    def test_27_entry_method_chaining_environment_locale(self):
        """Test entry method chaining with environment and locale"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .environment('test')
                 .locale('en-us'))
        entry.fetch()
        self.assertEqual('test', entry.http_instance.headers['environment'])
        self.assertEqual('en-us', entry.entry_queryable_param['locale'])

    def test_28_entry_only_multiple_fields(self):
        """Test entry only with multiple field calls"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .only('field1')
                 .only('field2'))
        entry.fetch()
        # Note: Multiple only calls may overwrite or append
        self.assertIn('only[BASE][]', entry.entry_param)

    def test_29_entry_excepts_multiple_fields(self):
        """Test entry excepts with multiple field calls"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .excepts('field1')
                 .excepts('field2'))
        entry.fetch()
        # Note: Multiple excepts calls may overwrite or append
        self.assertIn('except[BASE][]', entry.entry_param)

    def test_30_entry_include_fallback_with_locale(self):
        """Test entry include_fallback combined with locale"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .locale('en-gb')
                 .include_fallback())
        entry.fetch()
        self.assertEqual('en-gb', entry.entry_queryable_param['locale'])
        self.assertIn('include_fallback', entry.entry_param)

    def test_31_entry_include_metadata_with_version(self):
        """Test entry include_metadata combined with version"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .version(2)
                 .include_metadata())
        entry.fetch()
        self.assertEqual(2, entry.entry_param['version'])
        self.assertEqual('true', entry.entry_queryable_param['include_metadata'])

    def test_32_entry_include_content_type_with_locale(self):
        """Test entry include_content_type combined with locale"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .locale('en-us')
                 .include_content_type())
        entry.fetch()
        self.assertEqual('en-us', entry.entry_queryable_param['locale'])
        self.assertIn('include_content_type', entry.entry_queryable_param)

    def test_33_entry_include_reference_content_type_uid_with_version(self):
        """Test entry include_reference_content_type_uid combined with version"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .version(1)
                 .include_reference_content_type_uid())
        entry.fetch()
        self.assertEqual(1, entry.entry_param['version'])
        self.assertIn('include_reference_content_type_uid', entry.entry_queryable_param)

    def test_34_entry_add_param_multiple_times(self):
        """Test entry add_param called multiple times"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .add_param('key1', 'value1')
                 .add_param('key2', 'value2'))
        entry.fetch()
        self.assertEqual('value1', entry.entry_queryable_param['key1'])
        self.assertEqual('value2', entry.entry_queryable_param['key2'])

    def test_35_entry_complex_method_chaining(self):
        """Test entry with complex method chaining"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .environment('test')
                 .locale('en-us')
                 .version(1)
                 .include_fallback()
                 .include_metadata()
                 .include_content_type()
                 .add_param('custom', 'value'))
        entry.fetch()
        self.assertEqual('test', entry.http_instance.headers['environment'])
        self.assertEqual('en-us', entry.entry_queryable_param['locale'])
        self.assertEqual(1, entry.entry_param['version'])
        self.assertIn('include_fallback', entry.entry_param)
        self.assertIn('include_metadata', entry.entry_queryable_param)
        self.assertIn('include_content_type', entry.entry_queryable_param)
        self.assertEqual('value', entry.entry_queryable_param['custom'])

    def test_36_entry_include_embedded_items_with_locale(self):
        """Test entry include_embedded_items combined with locale"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .locale('en-us')
                 .include_embedded_items())
        entry.fetch()
        self.assertEqual('en-us', entry.entry_queryable_param['locale'])
        self.assertIn('include_embedded_items[]', entry.entry_param)

    def test_37_entry_param_with_different_values(self):
        """Test entry param method with different value types"""
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID)
        entry.param('string_param', 'string_value')
        entry.param('int_param', 123)
        entry.fetch()
        self.assertEqual('string_value', entry.entry_param['string_param'])
        self.assertEqual('123', entry.entry_param['int_param'])  # Converted to string

    def test_38_entry_only_and_excepts_together(self):
        """Test entry with both only and excepts"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .only('field1')
                 .excepts('field2'))
        entry.fetch()
        self.assertIn('only[BASE][]', entry.entry_param)
        self.assertIn('except[BASE][]', entry.entry_param)

    def test_39_entry_include_reference_with_multiple_fields(self):
        """Test entry include_reference with multiple fields"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .include_reference(['field1', 'field2', 'field3']))
        result = entry.fetch()
        self.assertIsNotNone(result)

    def test_40_entry_variants_with_params(self):
        """Test entry variants with params"""
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.entry(COMPLEX_ENTRY_UID).variants(VARIANT_UID, params={'locale': 'en-us'})
        result = entry.fetch()
        self.assertIn('variants', result['entry']['publish_details'])

    def test_41_entry_variants_multiple_uids(self):
        """Test entry variants with multiple variant UIDs"""
        content_type = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
        entry = content_type.entry(COMPLEX_ENTRY_UID).variants([VARIANT_UID, VARIANT_UID])
        result = entry.fetch()
        self.assertIn('variants', result['entry']['publish_details'])

    def test_42_entry_environment_removal(self):
        """Test entry remove_environment method"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .environment('test')
                 .remove_environment())
        self.assertNotIn('environment', entry.http_instance.headers)

    def test_43_entry_version_zero(self):
        """Test entry version with zero value"""
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).version(0)
        entry.fetch()
        self.assertEqual(0, entry.entry_param['version'])

    def test_44_entry_locale_empty_string(self):
        """Test entry locale with empty string"""
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).locale('')
        entry.fetch()
        self.assertEqual('', entry.entry_queryable_param['locale'])

    def test_45_entry_include_reference_empty_list(self):
        """Test entry include_reference with empty list"""
        entry = self.stack.content_type(COMPLEX_CONTENT_TYPE_UID).entry(COMPLEX_ENTRY_UID).include_reference([])
        result = entry.fetch()
        self.assertIsNotNone(result)

    def test_46_entry_all_queryable_methods_combined(self):
        """Test entry with all EntryQueryable methods combined"""
        entry = (self.stack.content_type(COMPLEX_CONTENT_TYPE_UID)
                 .entry(COMPLEX_ENTRY_UID)
                 .locale('en-us')
                 .only('field1')
                 .excepts('field2')
                 .include_reference(['ref1', 'ref2'])
                 .include_content_type()
                 .include_reference_content_type_uid()
                 .add_param('custom', 'value'))
        entry.fetch()
        self.assertEqual('en-us', entry.entry_queryable_param['locale'])
        self.assertIn('only[BASE][]', entry.entry_param)
        self.assertIn('except[BASE][]', entry.entry_param)
        self.assertIn('include_content_type', entry.entry_queryable_param)
        self.assertIn('include_reference_content_type_uid', entry.entry_queryable_param)
        self.assertEqual('value', entry.entry_queryable_param['custom'])

        
if __name__ == '__main__':
    unittest.main()
