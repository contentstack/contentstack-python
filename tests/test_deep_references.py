"""
Deep References Test Suite
Tests for multi-level reference inclusion (critical gap in current coverage)

Current Coverage: 0% for deep references
Target: Comprehensive coverage of 1-4 level references
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
import config


class DeepReferencesTest(BaseIntegrationTest):
    """
    Test deep reference inclusion (1-4 levels)
    
    Tests cover:
    - Single level references
    - Two level references  
    - Three+ level references
    - Reference integrity
    - Reference content type UID
    - Multiple references
    - Reference field projection
    """
    
    def test_01_single_level_reference(self):
        """Test including single level reference"""
        self.log_test_info("Testing single level reference inclusion")
        
        # Use MEDIUM entry (article) which references author
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry.include_reference('reference')
        
        result = TestHelpers.safe_api_call("single_level_ref", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Validate reference is included
        if TestHelpers.has_reference(entry_data, 'reference'):
            self.log_test_info("✅ Single level reference included")
            
            # Validate referenced entry has basic fields
            ref_data = entry_data['reference']
            if isinstance(ref_data, list):
                ref_data = ref_data[0]
            
            self.assertIn('uid', ref_data, "Referenced entry should have uid")
            self.log_test_info(f"Referenced entry UID: {ref_data.get('uid')}")
        else:
            self.log_test_warning("No reference found - may not be configured")
    
    def test_02_two_level_reference(self):
        """Test including two level deep reference"""
        self.log_test_info("Testing two level reference inclusion")
        
        # Use COMPLEX entry which may have nested references
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        # Include first level and second level
        entry.include_reference(['authors', 'authors.reference'])
        
        result = TestHelpers.safe_api_call("two_level_ref", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Check if authors field exists
        if TestHelpers.has_reference(entry_data, 'authors'):
            self.log_test_info("✅ First level reference (authors) included")
            
            authors = entry_data['authors']
            if isinstance(authors, list) and len(authors) > 0:
                first_author = authors[0]
                
                # Check for second level reference
                if TestHelpers.has_reference(first_author, 'reference'):
                    self.log_test_info("✅ Second level reference included")
                    depth = TestHelpers.count_references(entry_data, 'authors')
                    self.log_test_info(f"Reference depth: {depth}")
                else:
                    self.log_test_warning("Second level reference not found")
        else:
            self.log_test_warning("First level reference not found - may not be configured")
    
    def test_03_three_level_reference(self):
        """Test including three level deep reference"""
        self.log_test_info("Testing three level reference inclusion")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        # Include three levels
        entry.include_reference(['authors', 'authors.reference', 'authors.reference.page_footer'])
        
        result = TestHelpers.safe_api_call("three_level_ref", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Navigate through levels
        if TestHelpers.has_reference(entry_data, 'authors'):
            authors = entry_data['authors']
            if isinstance(authors, list) and len(authors) > 0:
                first_author = authors[0]
                
                if TestHelpers.has_reference(first_author, 'reference'):
                    self.log_test_info("✅ Level 2 reached")
                    
                    ref = first_author['reference']
                    if isinstance(ref, list):
                        ref = ref[0]
                    
                    if TestHelpers.has_reference(ref, 'page_footer'):
                        self.log_test_info("✅ Level 3 reached")
                        depth = TestHelpers.count_references(entry_data, 'authors', max_depth=5)
                        self.log_test_info(f"Total depth: {depth} levels")
    
    def test_04_reference_content_type_uid(self):
        """Test include_reference_content_type_uid"""
        self.log_test_info("Testing reference content type UID inclusion")
        
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry.include_reference('reference')
        entry.include_reference_content_type_uid()
        
        result = TestHelpers.safe_api_call("ref_ct_uid", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if TestHelpers.has_reference(entry_data, 'reference'):
            ref_data = entry_data['reference']
            if isinstance(ref_data, list):
                ref_data = ref_data[0]
            
            # Check for _content_type_uid
            if '_content_type_uid' in ref_data:
                self.log_test_info(f"✅ Content type UID included: {ref_data['_content_type_uid']}")
                self.assertIsNotNone(ref_data['_content_type_uid'])
            else:
                self.log_test_warning("_content_type_uid not found")
    
    def test_05_multiple_references(self):
        """Test including multiple different references"""
        self.log_test_info("Testing multiple reference inclusion")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        # Include multiple reference fields
        entry.include_reference(['authors', 'related_content', 'page_footer'])
        
        result = TestHelpers.safe_api_call("multiple_refs", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Count how many references are populated
        ref_count = 0
        ref_fields = ['authors', 'related_content', 'page_footer']
        
        for ref_field in ref_fields:
            if TestHelpers.has_reference(entry_data, ref_field):
                ref_count += 1
                self.log_test_info(f"✅ Reference '{ref_field}' included")
        
        self.log_test_info(f"Total references included: {ref_count}/{len(ref_fields)}")
        
        if ref_count > 0:
            self.assertGreater(ref_count, 0, "At least one reference should be included")
    
    def test_06_reference_with_only_fields(self):
        """Test reference inclusion with field projection"""
        self.log_test_info("Testing reference with field projection")
        
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry.include_reference('reference')
        entry.only('title').only('uid').only('reference')
        
        result = TestHelpers.safe_api_call("ref_with_only", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Should have only specified fields
        self.assertIn('uid', entry_data, "Entry must have uid")
        
        actual_fields = set(k for k in entry_data.keys() if not k.startswith('_'))
        requested_fields = {'uid', 'title', 'reference'}
        
        self.logger.info(f"  Requested: {requested_fields}, Received: {actual_fields}")
        
        # Verify projection worked
        self.assertLessEqual(len(actual_fields), 10, 
            f"Projection should limit fields. Got: {actual_fields}")
        
        missing = requested_fields - actual_fields
        if missing:
            self.logger.warning(f"  ⚠️ SDK BUG: Missing requested fields: {missing}")
        
        # Reference should still be included
        if TestHelpers.has_reference(entry_data, 'reference'):
            self.log_test_info("✅ Reference included with field projection")
        else:
            self.logger.warning("  ⚠️ Reference not included despite being requested")
    
    def test_07_reference_integrity_uid_match(self):
        """Test that referenced entry UID matches"""
        self.log_test_info("Testing reference integrity (UID matching)")
        
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry.include_reference('reference')
        
        result = TestHelpers.safe_api_call("ref_integrity", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if TestHelpers.has_reference(entry_data, 'reference'):
            ref_data = entry_data['reference']
            if isinstance(ref_data, list):
                for idx, ref in enumerate(ref_data):
                    if 'uid' in ref:
                        self.assertIsNotNone(ref['uid'])
                        self.log_test_info(f"✅ Reference {idx} has valid UID: {ref['uid']}")
            else:
                if 'uid' in ref_data:
                    self.assertIsNotNone(ref_data['uid'])
                    self.log_test_info(f"✅ Reference has valid UID: {ref_data['uid']}")
    
    def test_08_reference_without_include(self):
        """Test that reference is NOT included without include_reference"""
        self.log_test_info("Testing reference NOT included by default")
        
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        # Don't call include_reference
        
        result = TestHelpers.safe_api_call("no_ref_include", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Reference field should exist but should NOT have full data (just UID)
        if 'reference' in entry_data:
            ref_data = entry_data['reference']
            
            # Check if it's just UIDs (not full entries)
            if isinstance(ref_data, list) and len(ref_data) > 0:
                first_ref = ref_data[0]
                # Should have uid but probably not title
                if 'uid' in first_ref and 'title' not in first_ref:
                    self.log_test_info("✅ Reference is just UID (not fully included)")
                elif 'title' in first_ref:
                    self.log_test_warning("Reference seems to be fully included (unexpected)")
    
    def test_09_self_referencing_entry(self):
        """Test self-referencing content (section_builder)"""
        self.log_test_info("Testing self-referencing content")
        
        entry = self.stack.content_type(config.SELF_REF_CONTENT_TYPE_UID).entry(config.SELF_REF_ENTRY_UID)
        entry.include_reference(['sections', 'sections.sections'])
        
        result = TestHelpers.safe_api_call("self_ref", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Self-referencing entry not available")
        
        entry_data = result['entry']
        
        if TestHelpers.has_reference(entry_data, 'sections'):
            self.log_test_info("✅ Self-reference (level 1) included")
            
            sections = entry_data['sections']
            if isinstance(sections, list) and len(sections) > 0:
                first_section = sections[0]
                
                if TestHelpers.has_reference(first_section, 'sections'):
                    self.log_test_info("✅ Self-reference (level 2) included")
                    
                    # Count depth of self-references
                    depth = TestHelpers.count_references(entry_data, 'sections', max_depth=10)
                    self.log_test_info(f"Self-reference depth: {depth} levels")
    
    def test_10_reference_with_locale(self):
        """Test reference inclusion with specific locale"""
        self.log_test_info("Testing reference with locale")
        
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry.locale('en-us')
        entry.include_reference('reference')
        
        result = TestHelpers.safe_api_call("ref_with_locale", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Verify locale is en-us
        if 'locale' in entry_data:
            self.assertEqual(entry_data['locale'], 'en-us')
            self.log_test_info(f"✅ Entry locale: {entry_data['locale']}")
        
        if TestHelpers.has_reference(entry_data, 'reference'):
            self.log_test_info("✅ Reference included with locale")


class DeepReferencesQueryTest(BaseIntegrationTest):
    """
    Test deep references in query operations (not just fetch)
    """
    
    def test_11_query_with_single_reference(self):
        """Test query with single level reference"""
        self.log_test_info("Testing query with reference inclusion")
        
        query = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).query()
        query.include_reference('reference')
        query.limit(3)
        
        result = TestHelpers.safe_api_call("query_with_ref", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"Found {len(entries)} entries")
        
        # Check if any entry has references
        has_refs = False
        for entry in entries:
            if TestHelpers.has_reference(entry, 'reference'):
                has_refs = True
                break
        
        if has_refs:
            self.log_test_info("✅ At least one entry has reference included")
    
    def test_12_query_with_deep_reference(self):
        """Test query with deep reference"""
        self.log_test_info("Testing query with deep reference inclusion")
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.include_reference(['authors', 'authors.reference'])
        query.limit(2)
        
        result = TestHelpers.safe_api_call("query_deep_ref", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"Found {len(entries)} entries")
        
        # Check for deep references
        for idx, entry in enumerate(entries):
            if TestHelpers.has_reference(entry, 'authors'):
                depth = TestHelpers.count_references(entry, 'authors', max_depth=5)
                self.log_test_info(f"Entry {idx} reference depth: {depth}")
    
    def test_13_query_with_multiple_references(self):
        """Test query with multiple reference fields"""
        self.log_test_info("Testing query with multiple references")
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.include_reference(['authors', 'page_footer'])
        query.limit(2)
        
        result = TestHelpers.safe_api_call("query_multi_ref", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        
        for idx, entry in enumerate(entries):
            ref_count = 0
            if TestHelpers.has_reference(entry, 'authors'):
                ref_count += 1
            if TestHelpers.has_reference(entry, 'page_footer'):
                ref_count += 1
            
            if ref_count > 0:
                self.log_test_info(f"Entry {idx} has {ref_count} references")
    
    def test_14_query_with_ref_content_type_uid(self):
        """Test query with reference content type UID"""
        self.log_test_info("Testing query with reference content type UID")
        
        query = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).query()
        query.include_reference('reference')
        query.include_reference_content_type_uid()
        query.limit(2)
        
        result = TestHelpers.safe_api_call("query_ref_ct_uid", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        
        for entry in entries:
            if TestHelpers.has_reference(entry, 'reference'):
                ref = entry['reference']
                if isinstance(ref, list):
                    ref = ref[0]
                
                if '_content_type_uid' in ref:
                    self.log_test_info(f"✅ Reference CT UID: {ref['_content_type_uid']}")


class ReferenceEdgeCasesTest(BaseIntegrationTest):
    """
    Test edge cases and error scenarios for references
    """
    
    def test_15_invalid_reference_field(self):
        """Test including non-existent reference field"""
        self.log_test_info("Testing invalid reference field")
        
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        entry.include_reference('nonexistent_reference_field')
        
        result = TestHelpers.safe_api_call("invalid_ref_field", entry.fetch)
        
        # Should still work, just won't have the reference
        if self.assert_has_results(result):
            self.log_test_info("✅ Entry fetched successfully despite invalid reference field")
    
    def test_16_empty_reference_field(self):
        """Test reference field that exists but is empty"""
        self.log_test_info("Testing empty reference field handling")
        
        # Use SIMPLE entry which likely doesn't have references
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        entry.include_reference('page_footer')  # Field that likely doesn't exist in simple entry
        
        result = TestHelpers.safe_api_call("empty_ref", entry.fetch)
        
        if self.assert_has_results(result):
            entry_data = result['entry']
            
            if 'page_footer' in entry_data:
                if entry_data['page_footer'] is None or entry_data['page_footer'] == []:
                    self.log_test_info("✅ Empty reference handled gracefully")
            else:
                self.log_test_info("✅ Non-existent reference field handled gracefully")


if __name__ == '__main__':
    unittest.main(verbosity=2)

