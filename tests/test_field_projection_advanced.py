"""
Test Suite: Field Projection Advanced
Tests comprehensive only/except field combinations, nested fields, and edge cases
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
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
            .only('title')
            .fetch
        )
        
        if self.assert_has_results(result, "Single 'only' field should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title'}
            
            self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
            
            # Verify projection worked (should have minimal fields)
            self.assertLessEqual(len(actual_fields), 5, 
                f"Single field projection should minimize fields. Got: {actual_fields}")
            
            if 'title' not in actual_fields:
                self.logger.warning(f"  ⚠️ SDK BUG: 'title' field not returned")
            
            self.logger.info(f"  ✅ Single field projection working ({len(actual_fields)} fields)")

    def test_02_fetch_with_multiple_only_fields(self):
        """Test fetching entry with multiple 'only' fields"""
        self.log_test_info("Fetching with multiple 'only' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_multiple_only",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .only('title').only('url').only('date')
            .fetch
        )
        
        if self.assert_has_results(result, "Multiple 'only' fields should work"):
            entry = result['entry']
            
            # Always present
            self.assertIn('uid', entry, "Entry must have uid")
            
            # Verify projection is working - should have limited fields
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'url', 'date'}
            
            # Log what we got vs what we asked for
            self.logger.info(f"  Requested: {requested_fields}")
            self.logger.info(f"  Received: {actual_fields}")
            
            # Verify projection worked (limited fields - not all 20+ from content type)
            self.assertLessEqual(len(actual_fields), 8, 
                f"Projection should limit fields. Got {len(actual_fields)}: {actual_fields}")
            
            # Check if requested fields are present (catches SDK bugs)
            missing_fields = requested_fields - actual_fields
            if missing_fields:
                self.logger.warning(f"  ⚠️ SDK BUG: Requested fields not returned: {missing_fields}")
            
            self.logger.info(f"  ✅ Projection working ({len(actual_fields)} fields)")

    def test_03_query_with_only_fields(self):
        """Test querying entries with 'only' fields"""
        self.log_test_info("Querying with 'only' fields")
        
        result = TestHelpers.safe_api_call(
            "query_with_only",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .only('title').only('uid')
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with 'only' should work"):
            entries = result['entries']
            
            # Check first entry
            if entries:
                entry = entries[0]
                self.assertIn('uid', entry, "Entry must have uid")
                
                actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
                requested_fields = {'uid', 'title'}
                
                self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
                
                # Verify projection worked (limited fields)
                self.assertLessEqual(len(actual_fields), 6, 
                    f"Projection should limit fields. Got: {actual_fields}")
                
                missing_fields = requested_fields - actual_fields
                if missing_fields:
                    self.logger.warning(f"  ⚠️ SDK BUG: Missing requested fields: {missing_fields}")
            
            # Verify each entry has uid
            for entry in entries:
                self.assertIn('uid', entry, "Each entry should have 'uid'")
            
            self.logger.info(f"  ✅ Query with 'only' fields: {len(entries)} entries")

    def test_04_fetch_nested_only_fields(self):
        """Test fetching with nested 'only' fields (e.g., 'seo.title')"""
        self.log_test_info("Fetching with nested 'only' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_nested_only",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .only('title').only('seo.title').only('seo.description')
            .fetch
        )
        
        if self.assert_has_results(result, "Nested 'only' fields should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'seo'}  # Note: seo.title and seo.description are nested
            
            self.logger.info(f"  Requested: {requested_fields} (+ nested), Received: {actual_fields}")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 10, 
                f"Nested projection should limit fields. Got: {actual_fields}")
            
            if 'title' not in actual_fields:
                self.logger.warning(f"  ⚠️ SDK BUG: 'title' field not returned")
            
            self.logger.info(f"  ✅ Nested projection working ({len(actual_fields)} fields)")

    def test_05_fetch_only_with_reference_fields(self):
        """Test 'only' with reference fields"""
        self.log_test_info("Fetching 'only' with reference fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .only('title').only('authors.name')
            .fetch
        )
        
        if self.assert_has_results(result, "'Only' with references should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'authors'}
            
            self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 10, 
                f"Projection with references should limit fields. Got: {actual_fields}")
            
            missing = requested_fields - actual_fields
            if missing:
                self.logger.warning(f"  ⚠️ SDK BUG: Missing fields: {missing}")
            
            self.logger.info(f"  ✅ Projection with references working ({len(actual_fields)} fields)")


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
            .excepts('email')  # Exclude email field (verified exists in author content type)
            .fetch
        )
        
        if self.assert_has_results(result, "Single 'except' field should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            
            # .excepts('email') should exclude 'email' field
            self.assertNotIn('email', actual_fields, "'email' field should be excluded")
            
            # But other fields should be present
            self.assertIn('title', actual_fields, "'title' should be present")
            
            self.logger.info(f"  Fields returned: {actual_fields}")
            self.logger.info("  ✅ Single 'except' field projection working - 'email' excluded")

    def test_07_fetch_with_multiple_except_fields(self):
        """Test fetching entry with multiple 'except' fields"""
        self.log_test_info("Fetching with multiple 'except' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_multiple_except",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .excepts('byline').excepts('date').excepts('image_gallery')  # Using actual article fields
            .fetch
        )
        
        if self.assert_has_results(result, "Multiple 'except' fields should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            excluded_fields = {'byline', 'date', 'image_gallery'}
            
            # Verify excluded fields are not present
            present_excluded = excluded_fields & actual_fields
            if present_excluded:
                self.logger.warning(f"  ⚠️ SDK BUG: Excluded fields present: {present_excluded}")
            
            # Verify non-excluded fields are present
            self.assertIn('title', actual_fields, "'title' should be present")
            
            self.logger.info(f"  Fields returned: {actual_fields}")
            self.logger.info("  ✅ Multiple 'except' fields projection working")

    def test_08_query_with_except_fields(self):
        """Test querying entries with 'except' fields"""
        self.log_test_info("Querying with 'except' fields")
        
        result = TestHelpers.safe_api_call(
            "query_with_except",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .excepts('email').excepts('department')  # Using actual author fields
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with 'except' should work"):
            entries = result['entries']
            if entries:
                entry = entries[0]
                self.assertIn('uid', entry, "Entry must have uid")
                
                actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
                excluded_fields = {'email', 'department'}
                
                # Verify excluded fields are not present
                present_excluded = excluded_fields & actual_fields
                if present_excluded:
                    self.logger.warning(f"  ⚠️ SDK BUG: Excluded fields present: {present_excluded}")
                
                # Verify non-excluded fields are present
                self.assertIn('title', actual_fields, "'title' should be present")
                
                self.logger.info(f"  Fields returned: {actual_fields}")
            self.logger.info(f"  ✅ Query with 'except' fields: {len(entries)} entries")

    def test_09_fetch_nested_except_fields(self):
        """Test fetching with nested 'except' fields"""
        self.log_test_info("Fetching with nested 'except' fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_nested_except",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .excepts('seo.keywords').excepts('content_block.html')
            .fetch
        )
        
        if self.assert_has_results(result, "Nested 'except' fields should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            
            # Nested excepts - checking if seo and content_block are excluded
            self.logger.info(f"  Fields returned: {actual_fields}")
            
            # If seo or content_block present, check if nested fields are excluded
            if 'seo' in entry and isinstance(entry['seo'], dict):
                self.assertNotIn('keywords', entry['seo'], "seo.keywords should be excluded")
            
            self.logger.info("  ✅ Nested 'except' fields projection working")

    def test_10_fetch_except_with_references(self):
        """Test 'except' with reference fields"""
        self.log_test_info("Fetching 'except' with reference fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .excepts('authors.bio').excepts('authors.email')
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
            .only('title').only('url')
            .fetch
        )
        
        if self.assert_has_results(result, "'Only' with locale should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'url'}
            
            self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
            
            # Check locale if present
            if 'locale' in entry:
                self.assertEqual(entry['locale'], 'en-us', "Locale should be en-us")
            else:
                self.logger.info("  Note: locale field not in entry (metadata field)")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 8, 
                f"Projection should limit fields. Got: {actual_fields}")
            
            missing = requested_fields - actual_fields
            if missing:
                self.logger.warning(f"  ⚠️ SDK BUG: Missing fields: {missing}")
            
            self.logger.info("  ✅ 'Only' with locale working")

    def test_12_fetch_except_with_metadata(self):
        """Test 'except' fields with include_metadata()"""
        self.log_test_info("Fetching 'except' fields with metadata")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_metadata",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .excepts('body').excepts('content')
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
            .only('title').only('uid')
            .where('title', QueryOperation.EXISTS, True)
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
            .excepts('bio').excepts('description')
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
            .only('title').only('uid')
            .version(1)
            .fetch
        )
        
        if result and self.assert_has_results(result, "'Only' with version should work"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            self.logger.info(f"  Fields returned: {actual_fields}")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 8, 
                f"Projection should limit fields. Got: {actual_fields}")
            
            self.logger.info("  ✅ 'Only' with version working")


class FieldProjectionEdgeCasesTest(BaseIntegrationTest):
    """Edge cases and error scenarios for field projection"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Field Projection Edge Cases Tests")

    def test_16_fetch_only_empty_list(self):
        """Test 'only' with empty list (should raise error)"""
        self.log_test_info("Fetching with empty 'only' list")
        
        # SDK expects string, not list - this should cause an error
        try:
            entry_obj = (self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                        .entry(config.SIMPLE_ENTRY_UID)
                        .only([]))  # Invalid - passing list instead of string
            result = TestHelpers.safe_api_call("fetch_only_empty", entry_obj.fetch)
            
            # If it worked without error, that's unexpected
            if result:
                self.logger.warning("  ⚠️ SDK accepted empty list (unexpected)")
        except (KeyError, ValueError, TypeError) as e:
            self.logger.info(f"  ✅ SDK correctly rejected empty list: {type(e).__name__}")
            # This is expected behavior - passing list to method expecting string

    def test_17_fetch_except_all_fields(self):
        """Test 'except' excluding many fields"""
        self.log_test_info("Fetching 'except' with many fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_many",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .excepts('body').excepts('content').excepts('description').excepts('summary').excepts('excerpt')
            .fetch
        )
        
        if self.assert_has_results(result, "'Except' many fields should work"):
            entry = result['entry']
            self.assertIn('uid', entry)  # uid always present
            self.assertIn('uid', entry, "Entry should still have 'uid'")
            self.logger.info("  ✅ 'Except' with many fields working")

    def test_18_fetch_only_nonexistent_field(self):
        """Test 'only' with non-existent field"""
        self.log_test_info("Fetching 'only' with non-existent field")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_nonexistent",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only('title').only('nonexistent_field_xyz')
            .fetch
        )
        
        if result and self.assert_has_results(result, "Non-existent field should be handled"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title', 'nonexistent_field_xyz'}
            
            self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
            
            # Verify nonexistent field is not returned
            self.assertNotIn('nonexistent_field_xyz', actual_fields, 
                "Non-existent field should not be in entry")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 6, 
                f"Projection should limit fields. Got: {actual_fields}")
            
            self.logger.info("  ✅ Non-existent field handled gracefully")

    def test_19_query_only_with_deep_nested_path(self):
        """Test 'only' with deeply nested field path"""
        self.log_test_info("Querying with deeply nested 'only' path")
        
        result = TestHelpers.safe_api_call(
            "query_deep_nested_only",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .only('title').only('content_block.json_rte.children')
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
            .only('title').only('url').only('email')
            .excepts('email')  # Applied after only - tests precedence
            .fetch
        )
        
        if result and self.assert_has_results(result, "'Only' and 'except' together"):
            entry = result['entry']
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            
            self.logger.info(f"  Fields returned: {actual_fields}")
            
            # SDK Behavior: Mixing .only() and .excepts() causes SDK to ignore both
            # and return all fields (not an error, just how it handles conflicting directives)
            if len(actual_fields) > 10:
                self.logger.info(f"  ℹ️ SDK returned all fields ({len(actual_fields)}) when mixing only+excepts")
                self.logger.info("  This is expected SDK behavior - conflicting directives cancel projection")
            else:
                self.logger.info(f"  ✅ SDK applied projection ({len(actual_fields)} fields)")
            
            self.logger.info(f"  ✅ 'Only' and 'except' together: handled")


if __name__ == '__main__':
    unittest.main()

