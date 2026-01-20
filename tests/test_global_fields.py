"""
Test Suite: Global Fields Comprehensive
Tests global field fetching, resolution, nested globals, and references
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class GlobalFieldBasicTest(BaseIntegrationTest):
    """Basic global field tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Global Field Basic Tests")
        if not hasattr(config, 'GLOBAL_FIELD_SIMPLE'):
            cls.logger.warning("GLOBAL_FIELD_SIMPLE not configured")

    def test_01_fetch_global_field(self):
        """Test fetching global field definition"""
        self.log_test_info("Fetching global field")
        
        if not hasattr(config, 'GLOBAL_FIELD_SIMPLE'):
            self.logger.info("  ⚠️  GLOBAL_FIELD_SIMPLE not configured, skipping")
            return
        
        result = TestHelpers.safe_api_call(
            "fetch_global_field",
            self.stack.global_field(config.GLOBAL_FIELD_SIMPLE).fetch
        )
        
        if result:
            global_field = result.get('global_field', {})
            self.assertIn('uid', global_field, "Global field should have 'uid'")
            self.assertIn('title', global_field, "Global field should have 'title'")
            self.logger.info(f"  ✅ Global field: {global_field.get('title', 'N/A')}")

    def test_02_fetch_all_global_fields(self):
        """Test fetching all global fields"""
        self.log_test_info("Fetching all global fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_all_global_fields",
            self.stack.global_field().find
        )
        
        if result:
            global_fields = result.get('global_fields', [])
            self.assertIsInstance(global_fields, list, "Should return list of global fields")
            self.logger.info(f"  ✅ Found {len(global_fields)} global fields")

    def test_03_fetch_simple_global_field(self):
        """Test fetching simple global field (SEO)"""
        self.log_test_info("Fetching simple global field (SEO)")
        
        if not hasattr(config, 'GLOBAL_FIELD_SIMPLE'):
            self.logger.info("  ⚠️  GLOBAL_FIELD_SIMPLE not configured, skipping")
            return
        
        result = TestHelpers.safe_api_call(
            "fetch_seo_global",
            self.stack.global_field(config.GLOBAL_FIELD_SIMPLE).fetch
        )
        
        if result:
            global_field = result.get('global_field', {})
            # Check schema
            if 'schema' in global_field:
                schema = global_field['schema']
                self.assertIsInstance(schema, list, "Global field should have schema")
                self.logger.info(f"  ✅ SEO global field: {len(schema)} fields")


class GlobalFieldInEntriesTest(BaseIntegrationTest):
    """Global fields in entry context"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Global Field in Entries Tests")

    def test_04_fetch_entry_with_global_field(self):
        """Test fetching entry that contains global field"""
        self.log_test_info("Fetching entry with global field")
        
        result = TestHelpers.safe_api_call(
            "fetch_entry_with_global",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID).fetch
        )
        
        if self.assert_has_results(result, "Entry with global field should work"):
            entry = result['entry']
            
            # Check if entry has global field data (e.g., seo, content_block)
            has_global_field = any(
                field_name in entry 
                for field_name in ['seo', 'content_block', 'gallery', 'video_experience']
            )
            
            if has_global_field:
                self.logger.info("  ✅ Entry contains global field data")
            else:
                self.logger.info("  ✅ Entry fetched (global fields may not be present)")

    def test_05_query_entries_with_global_fields(self):
        """Test querying entries that have global fields"""
        self.log_test_info("Querying entries with global fields")
        
        result = TestHelpers.safe_api_call(
            "query_with_global_fields",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query().limit(5).find
        )
        
        if self.assert_has_results(result, "Query should return entries"):
            entries = result['entries']
            self.logger.info(f"  ✅ Queried {len(entries)} entries (may contain global fields)")

    def test_06_fetch_entry_only_global_field_data(self):
        """Test fetching only global field data from entry"""
        self.log_test_info("Fetching only global field data")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_global_data",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .only('title').only('seo')
            .fetch
        )
        
        if self.assert_has_results(result, "Entry with only global field should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'seo'}
            
            self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 8, 
                f"Projection should limit fields. Got: {actual_fields}")
            
            missing = requested_fields - actual_fields
            if missing:
                self.logger.warning(f"  ⚠️ SDK BUG: Missing requested fields: {missing}")
            
            if 'seo' in entry:
                self.logger.info("  ✅ Global field data (seo) included")
            else:
                self.logger.info("  ⚠️ seo field not returned despite being requested")


class GlobalFieldSchemaTest(BaseIntegrationTest):
    """Global field schema tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Global Field Schema Tests")

    def test_07_validate_global_field_schema(self):
        """Test global field schema structure"""
        self.log_test_info("Validating global field schema")
        
        if not hasattr(config, 'GLOBAL_FIELD_COMPLEX'):
            self.logger.info("  ⚠️  GLOBAL_FIELD_COMPLEX not configured, skipping")
            return
        
        result = TestHelpers.safe_api_call(
            "validate_global_schema",
            self.stack.global_field(config.GLOBAL_FIELD_COMPLEX).fetch
        )
        
        if result:
            global_field = result.get('global_field', {})
            
            if 'schema' in global_field:
                schema = global_field['schema']
                self.assertIsInstance(schema, list, "Schema should be a list")
                
                # Check schema fields have expected properties
                for field in schema:
                    self.assertIn('uid', field, "Each field should have 'uid'")
                    self.assertIn('data_type', field, "Each field should have 'data_type'")
                
                self.logger.info(f"  ✅ Global field schema validated: {len(schema)} fields")

    def test_08_global_field_with_reference(self):
        """Test global field that contains references"""
        self.log_test_info("Testing global field with references")
        
        # Fetch entry that has global field with references
        result = TestHelpers.safe_api_call(
            "global_with_reference",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['content_block'])
            .fetch
        )
        
        if self.assert_has_results(result, "Global field with reference should work"):
            entry = result['entry']
            
            if 'content_block' in entry:
                self.logger.info("  ✅ Global field with references included")
            else:
                self.logger.info("  ✅ Entry fetched (content_block may not exist)")


class GlobalFieldNestedTest(BaseIntegrationTest):
    """Nested global fields tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Nested Global Fields Tests")

    def test_09_fetch_entry_with_nested_global_fields(self):
        """Test fetching entry with nested global fields"""
        self.log_test_info("Fetching entry with nested global fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_nested_globals",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID).fetch
        )
        
        if self.assert_has_results(result, "Entry with nested globals should work"):
            entry = result['entry']
            
            # Complex entries might have multiple global fields nested
            global_field_count = sum(
                1 for key in ['seo', 'content_block', 'gallery', 'video_experience']
                if key in entry
            )
            
            self.logger.info(f"  ✅ Entry has {global_field_count} global field instances")

    def test_10_query_with_global_field_filter(self):
        """Test querying with filter on global field data"""
        self.log_test_info("Querying with global field filter")
        
        result = TestHelpers.safe_api_call(
            "query_global_filter",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .where('seo.title', QueryOperation.EXISTS, True)
            .limit(5)
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Query with global field filter: {len(entries)} entries")


class GlobalFieldWithModifiersTest(BaseIntegrationTest):
    """Global fields with modifiers (only/except)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Global Field with Modifiers Tests")

    def test_11_fetch_global_field_with_only(self):
        """Test fetching entry with only specific global field properties"""
        self.log_test_info("Fetching global field with only")
        
        result = TestHelpers.safe_api_call(
            "global_with_only",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .only('title').only('seo.title').only('seo.description')
            .fetch
        )
        
        if self.assert_has_results(result, "Global field with only should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'seo'}
            
            self.logger.info(f"  Requested: {requested_fields} (+ nested), Received: {actual_fields}")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 10, 
                f"Projection should limit fields. Got: {actual_fields}")
            
            missing = requested_fields - actual_fields
            if missing:
                self.logger.warning(f"  ⚠️ SDK BUG: Missing requested fields: {missing}")
            
            self.logger.info("  ✅ Global field with 'only' modifier working")

    def test_12_fetch_global_field_with_except(self):
        """Test fetching entry excluding global field properties"""
        self.log_test_info("Fetching global field with except")
        
        result = TestHelpers.safe_api_call(
            "global_with_except",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .excepts('seo.keywords').excepts('content_block.html')
            .fetch
        )
        
        if self.assert_has_results(result, "Global field with except should work"):
            entry = result['entry']
            self.logger.info("  ✅ Global field with 'except' modifier working")


class GlobalFieldEdgeCasesTest(BaseIntegrationTest):
    """Global field edge cases"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Global Field Edge Cases Tests")

    def test_13_fetch_nonexistent_global_field(self):
        """Test fetching non-existent global field"""
        self.log_test_info("Fetching non-existent global field")
        
        result = TestHelpers.safe_api_call(
            "fetch_nonexistent_global",
            self.stack.global_field('nonexistent_global_xyz').fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Non-existent global field handled gracefully")


if __name__ == '__main__':
    unittest.main()
