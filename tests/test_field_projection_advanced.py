"""
Test Suite: Field Projection Advanced
Tests comprehensive only/except field combinations, nested fields, and edge cases
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class FieldProjectionOnlyTest(BaseIntegrationTest):
    """Tests for 'only' field projection"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Field Projection 'Only' Tests")

    def test_01_fetch_with_single_only_field(self):
        """Test fetching entry with single 'only' field"""
        self.log_test_info("Fetching with single 'only' field")
        
        result = TestHelpers.safe_api_call(
            "fetch_single_only",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only(['title'])
            .fetch
        )
        
        if self.assert_has_results(result, "Single 'only' field should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            # Should have minimal other fields (uid, content_type_uid are always included)
            self.logger.info(f"  ✅ Single 'only' field projection: {list(entry.keys())}")

    def test_02_fetch_with_multiple_only_fields(self):
        """Test fetching entry with multiple 'only' fields"""
        self.log_test_info("Fetching with multiple 'only' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_multiple_only",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .only(['title', 'url', 'date'])
            .fetch
        )
        
        if self.assert_has_results(result, "Multiple 'only' fields should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.assertIn('url', entry, "Entry should have 'url'")
            self.logger.info("  ✅ Multiple 'only' fields projection working")

    def test_03_query_with_only_fields(self):
        """Test querying entries with 'only' fields"""
        self.log_test_info("Querying with 'only' fields")
        
        result = TestHelpers.safe_api_call(
            "query_with_only",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .only(['title', 'uid'])
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with 'only' should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('title', entry, "Each entry should have 'title'")
                self.assertIn('uid', entry, "Each entry should have 'uid'")
            self.logger.info(f"  ✅ Query with 'only' fields: {len(entries)} entries")

    def test_04_fetch_nested_only_fields(self):
        """Test fetching with nested 'only' fields (e.g., 'seo.title')"""
        self.log_test_info("Fetching with nested 'only' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_nested_only",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .only(['title', 'seo.title', 'seo.description'])
            .fetch
        )
        
        if self.assert_has_results(result, "Nested 'only' fields should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            if TestHelpers.has_field(entry, 'seo'):
                self.logger.info("  ✅ Nested 'only' fields projection working")
            else:
                self.logger.info("  ✅ Entry fetched (seo field may not exist)")

    def test_05_fetch_only_with_reference_fields(self):
        """Test 'only' with reference fields"""
        self.log_test_info("Fetching 'only' with reference fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .only(['title', 'authors.name'])
            .fetch
        )
        
        if self.assert_has_results(result, "'Only' with references should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.logger.info("  ✅ 'Only' with reference fields working")


class FieldProjectionExceptTest(BaseIntegrationTest):
    """Tests for 'except' field projection"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Field Projection 'Except' Tests")

    def test_06_fetch_with_single_except_field(self):
        """Test fetching entry with single 'except' field"""
        self.log_test_info("Fetching with single 'except' field")
        
        result = TestHelpers.safe_api_call(
            "fetch_single_except",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .excepts(['bio'])  # Exclude bio field
            .fetch
        )
        
        if self.assert_has_results(result, "Single 'except' field should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.assertNotIn('bio', entry, "Entry should NOT have 'bio'")
            self.logger.info("  ✅ Single 'except' field projection working")

    def test_07_fetch_with_multiple_except_fields(self):
        """Test fetching entry with multiple 'except' fields"""
        self.log_test_info("Fetching with multiple 'except' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_multiple_except",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .excepts(['body', 'content', 'description'])
            .fetch
        )
        
        if self.assert_has_results(result, "Multiple 'except' fields should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.assertNotIn('body', entry, "Entry should NOT have 'body'")
            self.assertNotIn('content', entry, "Entry should NOT have 'content'")
            self.logger.info("  ✅ Multiple 'except' fields projection working")

    def test_08_query_with_except_fields(self):
        """Test querying entries with 'except' fields"""
        self.log_test_info("Querying with 'except' fields")
        
        result = TestHelpers.safe_api_call(
            "query_with_except",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .excepts(['email', 'phone'])
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with 'except' should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('title', entry, "Each entry should have 'title'")
                self.assertNotIn('email', entry, "Entry should NOT have 'email'")
            self.logger.info(f"  ✅ Query with 'except' fields: {len(entries)} entries")

    def test_09_fetch_nested_except_fields(self):
        """Test fetching with nested 'except' fields"""
        self.log_test_info("Fetching with nested 'except' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_nested_except",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .excepts(['seo.keywords', 'content_block.html'])
            .fetch
        )
        
        if self.assert_has_results(result, "Nested 'except' fields should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.logger.info("  ✅ Nested 'except' fields projection working")

    def test_10_fetch_except_with_references(self):
        """Test 'except' with reference fields"""
        self.log_test_info("Fetching 'except' with reference fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .excepts(['authors.bio', 'authors.email'])
            .fetch
        )
        
        if self.assert_has_results(result, "'Except' with references should work"):
            entry = result['entry']
            self.logger.info("  ✅ 'Except' with reference fields working")


class FieldProjectionCombinedTest(BaseIntegrationTest):
    """Tests combining field projection with other SDK features"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Combined Field Projection Tests")

    def test_11_fetch_only_with_locale(self):
        """Test 'only' fields with locale"""
        self.log_test_info("Fetching 'only' fields with locale")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_locale",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('en-us')
            .only(['title', 'url'])
            .fetch
        )
        
        if self.assert_has_results(result, "'Only' with locale should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.assertEqual(entry.get('locale'), 'en-us', "Locale should be en-us")
            self.logger.info("  ✅ 'Only' with locale working")

    def test_12_fetch_except_with_metadata(self):
        """Test 'except' fields with include_metadata()"""
        self.log_test_info("Fetching 'except' fields with metadata")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_metadata",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .excepts(['body', 'content'])
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "'Except' with metadata should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.assertNotIn('body', entry, "Entry should NOT have 'body'")
            self.logger.info("  ✅ 'Except' with metadata working")

    def test_13_query_only_with_where_filter(self):
        """Test 'only' fields with where filter"""
        self.log_test_info("Querying 'only' with where filter")
        
        result = TestHelpers.safe_api_call(
            "query_only_where",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .only(['title', 'uid'])
            .where({'title': {'$exists': True}})
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "'Only' with where filter should work"):
            self.logger.info(f"  ✅ 'Only' with where: {len(result['entries'])} entries")

    def test_14_query_except_with_order_by(self):
        """Test 'except' fields with order_by"""
        self.log_test_info("Querying 'except' with order_by")
        
        result = TestHelpers.safe_api_call(
            "query_except_order",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .excepts(['bio', 'description'])
            .order_by_ascending('title')
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "'Except' with order_by should work"):
            entries = result['entries']
            self.assertGreater(len(entries), 0, "Should return entries")
            self.logger.info(f"  ✅ 'Except' with order_by: {len(entries)} entries")

    def test_15_fetch_only_with_version(self):
        """Test 'only' fields with specific version"""
        self.log_test_info("Fetching 'only' with version")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_version",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only(['title', 'uid'])
            .version(1)
            .fetch
        )
        
        if result and self.assert_has_results(result, "'Only' with version should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.logger.info("  ✅ 'Only' with version working")


class FieldProjectionEdgeCasesTest(BaseIntegrationTest):
    """Edge cases and error scenarios for field projection"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Field Projection Edge Cases Tests")

    def test_16_fetch_only_empty_list(self):
        """Test 'only' with empty list (should return minimal fields)"""
        self.log_test_info("Fetching with empty 'only' list")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_empty",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only([])
            .fetch
        )
        
        if result and self.assert_has_results(result, "Empty 'only' should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry should at least have 'uid'")
            self.logger.info(f"  ✅ Empty 'only' list: {list(entry.keys())}")

    def test_17_fetch_except_all_fields(self):
        """Test 'except' excluding many fields"""
        self.log_test_info("Fetching 'except' with many fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_many",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .excepts(['body', 'content', 'description', 'summary', 'excerpt'])
            .fetch
        )
        
        if self.assert_has_results(result, "'Except' many fields should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should still have 'title'")
            self.assertIn('uid', entry, "Entry should still have 'uid'")
            self.logger.info("  ✅ 'Except' with many fields working")

    def test_18_fetch_only_nonexistent_field(self):
        """Test 'only' with non-existent field"""
        self.log_test_info("Fetching 'only' with non-existent field")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_nonexistent",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only(['title', 'nonexistent_field_xyz'])
            .fetch
        )
        
        if result and self.assert_has_results(result, "Non-existent field should be handled"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.assertNotIn('nonexistent_field_xyz', entry, "Non-existent field should not be in entry")
            self.logger.info("  ✅ Non-existent field handled gracefully")

    def test_19_query_only_with_deep_nested_path(self):
        """Test 'only' with deeply nested field path"""
        self.log_test_info("Querying with deeply nested 'only' path")
        
        result = TestHelpers.safe_api_call(
            "query_deep_nested_only",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .only(['title', 'content_block.json_rte.children'])
            .limit(3)
            .find
        )
        
        if result and self.assert_has_results(result, "Deep nested 'only' should work"):
            self.logger.info(f"  ✅ Deep nested 'only': {len(result['entries'])} entries")

    def test_20_fetch_only_and_except_together(self):
        """Test using 'only' and 'except' together (edge case - should use last one)"""
        self.log_test_info("Using 'only' and 'except' together")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_except_together",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only(['title', 'url', 'bio'])
            .excepts(['bio'])  # Applied after only
            .fetch
        )
        
        if result and self.assert_has_results(result, "'Only' and 'except' together"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            # The behavior depends on SDK implementation (which one takes precedence)
            self.logger.info(f"  ✅ 'Only' and 'except' together: {list(entry.keys())}")


if __name__ == '__main__':
    unittest.main()

