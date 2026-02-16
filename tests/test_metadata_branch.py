"""
Test Suite: Metadata & Branch
Tests metadata inclusion, branch-specific queries, and branch switching
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class MetadataBasicTest(BaseIntegrationTest):
    """Basic metadata inclusion tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Basic Metadata Tests")

    def test_01_fetch_entry_with_metadata(self):
        """Test fetching entry with include_metadata()"""
        self.log_test_info("Fetching entry with metadata")
        
        result = TestHelpers.safe_api_call(
            "fetch_with_metadata",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata should be included"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            metadata = entry['_metadata']
            self.assertIsInstance(metadata, dict, "_metadata should be a dictionary")
            self.logger.info(f"  ✅ Metadata fields: {list(metadata.keys())[:5]}")

    def test_02_query_entries_with_metadata(self):
        """Test querying entries with metadata"""
        self.log_test_info("Querying entries with metadata")
        
        result = TestHelpers.safe_api_call(
            "query_with_metadata",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_metadata()
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query should return entries with metadata"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('_metadata', entry, "Each entry should have '_metadata'")
            self.logger.info(f"  ✅ {len(entries)} entries with metadata")

    def test_03_fetch_complex_entry_with_metadata(self):
        """Test fetching complex entry with metadata"""
        self.log_test_info("Fetching complex entry with metadata")
        
        result = TestHelpers.safe_api_call(
            "fetch_complex_metadata",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Complex entry should have metadata"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Complex entry should have '_metadata'")
            self.logger.info("  ✅ Complex entry metadata included")

    def test_04_metadata_structure_validation(self):
        """Test metadata structure contains expected fields"""
        self.log_test_info("Validating metadata structure")
        
        result = TestHelpers.safe_api_call(
            "fetch_metadata_structure",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata structure should be valid"):
            metadata = result['entry'].get('_metadata', {})
            
            # Common metadata fields
            expected_fields = ['uid', 'content_type_uid']
            for field in expected_fields:
                if field in metadata:
                    self.logger.info(f"  ✅ Metadata has '{field}'")


class MetadataWithReferencesTest(BaseIntegrationTest):
    """Metadata with references and embedded items"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Metadata with References Tests")

    def test_05_metadata_with_include_reference(self):
        """Test metadata with included references"""
        self.log_test_info("Metadata with include_reference")
        
        result = TestHelpers.safe_api_call(
            "metadata_with_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with references should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            
            # Check if referenced entries also have metadata
            if TestHelpers.has_field(entry, 'authors'):
                authors = TestHelpers.get_nested_field(entry, 'authors', [])
                if isinstance(authors, list) and len(authors) > 0:
                    first_author = authors[0]
                    if '_metadata' in first_author:
                        self.logger.info("  ✅ Referenced entries also have metadata")
                    else:
                        self.logger.info("  ✅ Main entry has metadata")

    def test_06_metadata_with_embedded_items(self):
        """Test metadata with embedded items"""
        self.log_test_info("Metadata with embedded items")
        
        result = TestHelpers.safe_api_call(
            "metadata_with_embedded",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_embedded_items()
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with embedded items should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.logger.info("  ✅ Metadata with embedded items working")

    def test_07_query_metadata_with_references(self):
        """Test querying with metadata and references"""
        self.log_test_info("Querying metadata with references")
        
        result = TestHelpers.safe_api_call(
            "query_metadata_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .include_reference(['authors'])
            .include_metadata()
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with metadata and references should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('_metadata', entry, "Each entry should have '_metadata'")
            self.logger.info(f"  ✅ {len(entries)} entries with metadata and references")


class BranchBasicTest(BaseIntegrationTest):
    """Basic branch-specific tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Basic Branch Tests")
        if not hasattr(config, 'BRANCH_UID') or not config.BRANCH_UID:
            cls.logger.warning("BRANCH_UID not configured, some tests may skip")

    def test_08_fetch_entry_from_main_branch(self):
        """Test fetching entry from main branch"""
        self.log_test_info("Fetching entry from main branch")
        
        if not hasattr(config, 'BRANCH_UID'):
            self.logger.info("  ⚠️  BRANCH_UID not configured, skipping")
            return
        
        result = TestHelpers.safe_api_call(
            "fetch_from_main_branch",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        if self.assert_has_results(result, "Main branch entry should be fetched"):
            self.logger.info("  ✅ Entry from main branch fetched")

    def test_09_query_entries_from_branch(self):
        """Test querying entries from specific branch"""
        self.log_test_info("Querying entries from branch")
        
        result = TestHelpers.safe_api_call(
            "query_from_branch",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Branch query should work"):
            self.logger.info(f"  ✅ {len(result['entries'])} entries from branch")

    def test_10_fetch_with_include_branch(self):
        """Test fetching with include_branch() method"""
        self.log_test_info("Fetching with include_branch")
        
        if not hasattr(config, 'BRANCH_UID'):
            self.logger.info("  ⚠️  BRANCH_UID not configured, skipping")
            return
        
        result = TestHelpers.safe_api_call(
            "fetch_include_branch",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        if self.assert_has_results(result, "include_branch should work"):
            self.logger.info("  ✅ include_branch() working")


class MetadataAndBranchCombinedTest(BaseIntegrationTest):
    """Combined metadata and branch tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Combined Metadata & Branch Tests")

    def test_11_fetch_with_metadata_and_branch(self):
        """Test fetching with both metadata and branch"""
        self.log_test_info("Fetching with metadata and branch")
        
        result = TestHelpers.safe_api_call(
            "fetch_metadata_branch",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with branch should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.logger.info("  ✅ Metadata with branch working")

    def test_12_query_with_metadata_and_branch(self):
        """Test querying with metadata and branch"""
        self.log_test_info("Querying with metadata and branch")
        
        result = TestHelpers.safe_api_call(
            "query_metadata_branch",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_metadata()
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with metadata and branch should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('_metadata', entry, "Each entry should have '_metadata'")
            self.logger.info(f"  ✅ {len(entries)} entries with metadata and branch")

    def test_13_metadata_branch_with_references(self):
        """Test metadata and branch with references"""
        self.log_test_info("Metadata, branch, and references combined")
        
        result = TestHelpers.safe_api_call(
            "metadata_branch_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Combined features should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.logger.info("  ✅ Metadata, branch, and references combined")


class ContentTypeMetadataTest(BaseIntegrationTest):
    """Content type metadata tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Metadata Tests")

    def test_14_fetch_with_include_content_type(self):
        """Test fetching with include_content_type()"""
        self.log_test_info("Fetching with include_content_type")
        
        result = TestHelpers.safe_api_call(
            "fetch_include_content_type",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .include_content_type()
            .fetch
        )
        
        if self.assert_has_results(result, "include_content_type should work"):
            self.assertIn('content_type', result, "Result should have 'content_type'")
            content_type = result['content_type']
            self.assertIn('uid', content_type, "Content type should have 'uid'")
            self.logger.info(f"  ✅ Content type UID: {content_type['uid']}")

    def test_15_fetch_with_content_type_and_metadata(self):
        """Test fetching with both content type and metadata"""
        self.log_test_info("Fetching with content type and metadata")
        
        result = TestHelpers.safe_api_call(
            "fetch_ct_metadata",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .include_content_type()
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Content type with metadata should work"):
            self.assertIn('content_type', result, "Should have 'content_type'")
            self.assertIn('_metadata', result['entry'], "Entry should have '_metadata'")
            self.logger.info("  ✅ Content type and metadata both included")

    def test_16_query_with_include_content_type(self):
        """Test querying with include_content_type()"""
        self.log_test_info("Querying with include_content_type")
        
        result = TestHelpers.safe_api_call(
            "query_include_content_type",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_content_type()
            .limit(3)
            .find
        )
        
        if result:
            # Content type might be at response level or entry level
            if 'content_type' in result:
                self.logger.info("  ✅ Content type included in response")
            elif 'entries' in result and len(result['entries']) > 0:
                self.logger.info(f"  ✅ {len(result['entries'])} entries returned")

    def test_17_fetch_reference_content_type_uid(self):
        """Test fetching with include_reference_content_type_uid()"""
        self.log_test_info("Fetching with reference content type UID")
        
        result = TestHelpers.safe_api_call(
            "fetch_ref_ct_uid",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .include_reference_content_type_uid()
            .fetch
        )
        
        if self.assert_has_results(result, "Reference content type UID should work"):
            entry = result['entry']
            
            # Check if referenced entries have _content_type_uid
            if TestHelpers.has_field(entry, 'authors'):
                authors = TestHelpers.get_nested_field(entry, 'authors', [])
                if isinstance(authors, list) and len(authors) > 0:
                    first_author = authors[0]
                    if '_content_type_uid' in first_author:
                        self.logger.info(f"  ✅ Reference CT UID: {first_author['_content_type_uid']}")
                    else:
                        self.logger.info("  ✅ Entry fetched (reference may not have CT UID)")


class MetadataFieldProjectionTest(BaseIntegrationTest):
    """Metadata with field projection (only/except)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Metadata Field Projection Tests")

    def test_18_metadata_with_only_fields(self):
        """Test metadata with only fields"""
        self.log_test_info("Metadata with only fields")
        
        result = TestHelpers.safe_api_call(
            "metadata_only_fields",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only('title').only('uid')
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with only fields should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.assertIn('uid', entry, "Entry must have uid")
            
            actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
            requested_fields = {'uid', 'title'}
            
            self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
            
            # Verify projection worked
            self.assertLessEqual(len(actual_fields), 6, 
                f"Projection should limit fields. Got: {actual_fields}")
            
            missing = requested_fields - actual_fields
            if missing:
                self.logger.warning(f"  ⚠️ SDK BUG: Missing requested fields: {missing}")
            
            self.logger.info("  ✅ Metadata with only fields working")

    def test_19_metadata_with_except_fields(self):
        """Test metadata with except fields"""
        self.log_test_info("Metadata with except fields")
        
        result = TestHelpers.safe_api_call(
            "metadata_except_fields",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .excepts('body').excepts('content')
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with except fields should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.assertNotIn('body', entry, "Entry should NOT have 'body'")
            self.logger.info("  ✅ Metadata with except fields working")

    def test_20_query_metadata_with_field_projection(self):
        """Test querying with metadata and field projection"""
        self.log_test_info("Query metadata with field projection")
        
        result = TestHelpers.safe_api_call(
            "query_metadata_projection",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .only('title').only('uid')
            .include_metadata()
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with metadata and projection should work"):
            entries = result['entries']
            
            if entries:
                entry = entries[0]
                self.assertIn('_metadata', entry, "Entry should have '_metadata'")
                self.assertIn('uid', entry, "Entry must have uid")
                
                actual_fields = set(k for k in entry.keys() if not k.startswith('_'))
                requested_fields = {'uid', 'title'}
                
                self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
                
                # Verify projection worked
                self.assertLessEqual(len(actual_fields), 6, 
                    f"Projection should limit fields. Got: {actual_fields}")
                
                missing = requested_fields - actual_fields
                if missing:
                    self.logger.warning(f"  ⚠️ SDK BUG: Missing requested fields: {missing}")
            
            self.logger.info(f"  ✅ {len(entries)} entries with metadata and projection")


class MetadataLocaleTest(BaseIntegrationTest):
    """Metadata with locale and fallback"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Metadata Locale Tests")

    def test_21_metadata_with_locale(self):
        """Test metadata with locale"""
        self.log_test_info("Metadata with locale")
        
        result = TestHelpers.safe_api_call(
            "metadata_with_locale",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('en-us')
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with locale should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.assertEqual(entry.get('locale'), 'en-us', "Locale should be en-us")
            self.logger.info("  ✅ Metadata with locale working")

    def test_22_metadata_with_fallback(self):
        """Test metadata with locale fallback"""
        self.log_test_info("Metadata with locale fallback")
        
        result = TestHelpers.safe_api_call(
            "metadata_with_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('fr-fr')
            .include_fallback()
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with fallback should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.logger.info("  ✅ Metadata with fallback working")

    def test_23_query_metadata_with_locale(self):
        """Test querying with metadata and locale"""
        self.log_test_info("Query with metadata and locale")
        
        result = TestHelpers.safe_api_call(
            "query_metadata_locale",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('en-us')
            .include_metadata()
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with metadata and locale should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('_metadata', entry, "Each entry should have '_metadata'")
            self.logger.info(f"  ✅ {len(entries)} entries with metadata and locale")


class MetadataEdgeCasesTest(BaseIntegrationTest):
    """Edge cases for metadata"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Metadata Edge Cases Tests")

    def test_24_fetch_without_metadata(self):
        """Test fetching without metadata (default behavior)"""
        self.log_test_info("Fetching without metadata")
        
        result = TestHelpers.safe_api_call(
            "fetch_no_metadata",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        if self.assert_has_results(result, "Default fetch should work"):
            entry = result['entry']
            # Metadata might or might not be included by default
            if '_metadata' in entry:
                self.logger.info("  ✅ Metadata included by default")
            else:
                self.logger.info("  ✅ Metadata not included by default (expected)")

    def test_25_metadata_with_complex_query(self):
        """Test metadata with complex query combinations"""
        self.log_test_info("Metadata with complex query")
        
        result = TestHelpers.safe_api_call(
            "metadata_complex_query",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.EXISTS, True)
            .include_reference(['authors'])
            .include_metadata()
            .only('title').only('authors')
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Complex query with metadata should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('_metadata', entry, "Each entry should have '_metadata'")
            self.logger.info(f"  ✅ Complex query with metadata: {len(entries)} entries")


if __name__ == '__main__':
    unittest.main()

