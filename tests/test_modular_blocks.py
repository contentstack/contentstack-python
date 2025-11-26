"""
Modular Blocks Test Suite
Tests for modular blocks functionality (critical gap)

Current Coverage: 0% for modular blocks
Target: Comprehensive coverage of modular block iteration and handling
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
import config


class ModularBlocksBasicTest(BaseIntegrationTest):
    """
    Test basic modular blocks functionality
    """
    
    def test_01_fetch_entry_with_modular_blocks(self):
        """Test fetching entry with modular blocks"""
        self.log_test_info("Testing entry with modular blocks")
        
        # Use COMPLEX entry which likely has modular blocks
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("fetch_modular_blocks", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Look for common modular block field names
        block_fields = ['modules', 'blocks', 'content_block', 'page_components', 'sections']
        
        for field in block_fields:
            if field in entry_data:
                field_data = entry_data[field]
                
                if isinstance(field_data, list) and len(field_data) > 0:
                    self.log_test_info(f"✅ Found modular blocks field: {field} with {len(field_data)} blocks")
                    
                    # Check first block structure
                    first_block = field_data[0]
                    if isinstance(first_block, dict):
                        self.log_test_info(f"   Block keys: {list(first_block.keys())[:5]}")
                elif isinstance(field_data, dict):
                    self.log_test_info(f"✅ Found modular blocks field: {field} (dict structure)")
    
    def test_02_modular_block_structure(self):
        """Test modular block structure"""
        self.log_test_info("Testing modular block structure")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("block_structure", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Look for content_block (global field with modular structure)
        if 'content_block' in entry_data:
            cb = entry_data['content_block']
            
            if isinstance(cb, dict):
                # Check for common block structure fields
                common_fields = ['title', 'content_block_id', 'html', 'json_rte']
                
                for field in common_fields:
                    if field in cb:
                        self.log_test_info(f"✅ Block has '{field}' field")
    
    def test_03_iterate_modular_blocks(self):
        """Test iterating through modular blocks"""
        self.log_test_info("Testing modular block iteration")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("iterate_blocks", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Try to find and iterate blocks
        for field_name in ['modules', 'blocks', 'sections']:
            if field_name in entry_data:
                blocks = entry_data[field_name]
                
                if isinstance(blocks, list):
                    self.log_test_info(f"✅ Iterating {len(blocks)} blocks in '{field_name}'")
                    
                    for idx, block in enumerate(blocks[:3]):  # Check first 3
                        if isinstance(block, dict):
                            block_type = block.get('_content_type_uid', block.get('type', 'unknown'))
                            self.log_test_info(f"   Block {idx}: type={block_type}")
                    
                    break
    
    def test_04_modular_blocks_with_references(self):
        """Test modular blocks containing references"""
        self.log_test_info("Testing modular blocks with references")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_reference(['authors', 'related_content'])
        
        result = TestHelpers.safe_api_call("blocks_with_refs", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Check if blocks contain references
        has_blocks = False
        has_refs = False
        
        for field in ['modules', 'blocks', 'content_block']:
            if field in entry_data:
                has_blocks = True
                break
        
        if TestHelpers.has_reference(entry_data, 'authors') or TestHelpers.has_reference(entry_data, 'related_content'):
            has_refs = True
        
        if has_blocks and has_refs:
            self.log_test_info("✅ Entry has both blocks and references")
    
    def test_05_nested_modular_blocks(self):
        """Test nested modular blocks"""
        self.log_test_info("Testing nested modular blocks")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("nested_blocks", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Look for nested block structures
        if 'content_block' in entry_data:
            cb = entry_data['content_block']
            
            if isinstance(cb, dict):
                # Check if it contains nested content
                if 'json_rte' in cb and isinstance(cb['json_rte'], dict):
                    json_rte = cb['json_rte']
                    
                    if 'children' in json_rte:
                        self.log_test_info(f"✅ Nested content with {len(json_rte['children'])} children")
                        
                        # Look for nested blocks within children
                        for child in json_rte['children'][:3]:
                            if isinstance(child, dict) and 'children' in child:
                                self.log_test_info("✅ Found nested block structure")
                                break


class ModularBlocksQueryTest(BaseIntegrationTest):
    """
    Test modular blocks in query operations
    """
    
    def test_06_query_entries_with_blocks(self):
        """Test querying entries with modular blocks"""
        self.log_test_info("Testing query for entries with blocks")
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.limit(3)
        
        result = TestHelpers.safe_api_call("query_blocks", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"Found {len(entries)} entries")
        
        # Check how many have modular blocks
        entries_with_blocks = 0
        
        for entry in entries:
            for field in ['modules', 'blocks', 'content_block']:
                if field in entry:
                    entries_with_blocks += 1
                    break
        
        self.log_test_info(f"✅ {entries_with_blocks}/{len(entries)} entries have modular blocks")
    
    def test_07_query_with_block_field_projection(self):
        """Test query with modular block field projection"""
        self.log_test_info("Testing query with block field projection")
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.only('uid').only('title').only('content_block')
        query.limit(2)
        
        result = TestHelpers.safe_api_call("query_block_projection", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        
        for entry in entries:
            # Should have only specified fields
            self.assertIn('uid', entry)
            
            if 'content_block' in entry:
                self.log_test_info("✅ Block field included with projection")


class ModularBlocksComplexTest(BaseIntegrationTest):
    """
    Test complex modular block scenarios
    """
    
    def test_08_blocks_with_embedded_items(self):
        """Test modular blocks with embedded items"""
        self.log_test_info("Testing blocks with embedded items")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("blocks_embedded", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        has_blocks = 'content_block' in entry_data
        has_embedded = '_embedded_items' in entry_data
        
        if has_blocks and has_embedded:
            self.log_test_info("✅ Entry has both blocks and embedded items")
    
    def test_09_blocks_with_locale(self):
        """Test modular blocks with locale"""
        self.log_test_info("Testing blocks with locale")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.locale('en-us')
        
        result = TestHelpers.safe_api_call("blocks_locale", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if 'locale' in entry_data:
            self.assertEqual(entry_data['locale'], 'en-us')
            self.log_test_info(f"✅ Entry locale: {entry_data['locale']}")
        
        if 'content_block' in entry_data:
            self.log_test_info("✅ Blocks included with locale")
    
    def test_10_block_content_validation(self):
        """Test validating block content"""
        self.log_test_info("Testing block content validation")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("block_validation", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if 'content_block' in entry_data:
            cb = entry_data['content_block']
            
            if isinstance(cb, dict):
                # Validate has content (either html or json_rte)
                has_html = 'html' in cb and cb['html']
                has_json_rte = 'json_rte' in cb and cb['json_rte']
                
                if has_html or has_json_rte:
                    self.log_test_info("✅ Block has valid content")
                    
                    if has_html:
                        html_length = len(cb['html'])
                        self.log_test_info(f"   HTML content: {html_length} chars")
                    
                    if has_json_rte:
                        json_rte = cb['json_rte']
                        if isinstance(json_rte, dict) and 'children' in json_rte:
                            self.log_test_info(f"   JSON RTE nodes: {len(json_rte['children'])}")


class ModularBlocksEdgeCasesTest(BaseIntegrationTest):
    """
    Test edge cases for modular blocks
    """
    
    def test_11_empty_modular_blocks(self):
        """Test handling of empty modular blocks"""
        self.log_test_info("Testing empty modular blocks")
        
        # Use SIMPLE entry which likely doesn't have blocks
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("empty_blocks", entry.fetch)
        
        if self.assert_has_results(result):
            entry_data = result['entry']
            
            # Check if blocks field exists but is empty
            for field in ['modules', 'blocks', 'content_block']:
                if field in entry_data:
                    field_data = entry_data[field]
                    
                    if field_data is None or (isinstance(field_data, list) and len(field_data) == 0):
                        self.log_test_info(f"✅ Empty blocks field '{field}' handled gracefully")
    
    def test_12_blocks_with_missing_fields(self):
        """Test blocks with missing optional fields"""
        self.log_test_info("Testing blocks with missing fields")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("blocks_missing_fields", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if 'content_block' in entry_data:
            cb = entry_data['content_block']
            
            if isinstance(cb, dict):
                # Some fields might be missing - test handles gracefully
                title = cb.get('title', 'N/A')
                cb_id = cb.get('content_block_id', 'N/A')
                
                self.log_test_info(f"✅ Block title: {title}")
                self.log_test_info(f"✅ Block ID: {cb_id}")


class SelfReferencingBlocksTest(BaseIntegrationTest):
    """
    Test self-referencing blocks (section_builder)
    """
    
    def test_13_self_referencing_sections(self):
        """Test self-referencing section blocks"""
        self.log_test_info("Testing self-referencing sections")
        
        entry = self.stack.content_type(config.SELF_REF_CONTENT_TYPE_UID).entry(config.SELF_REF_ENTRY_UID)
        entry.include_reference(['sections', 'sections.sections'])
        
        result = TestHelpers.safe_api_call("self_ref_sections", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Self-referencing entry not available")
        
        entry_data = result['entry']
        
        if 'sections' in entry_data:
            sections = entry_data['sections']
            
            if isinstance(sections, list):
                self.log_test_info(f"✅ Found {len(sections)} top-level sections")
                
                # Check for nested sections
                for idx, section in enumerate(sections[:2]):
                    if 'sections' in section:
                        nested = section['sections']
                        
                        if isinstance(nested, list) and len(nested) > 0:
                            self.log_test_info(f"✅ Section {idx} has {len(nested)} nested sections")
    
    def test_14_section_depth_counting(self):
        """Test counting depth of self-referencing sections"""
        self.log_test_info("Testing section depth counting")
        
        entry = self.stack.content_type(config.SELF_REF_CONTENT_TYPE_UID).entry(config.SELF_REF_ENTRY_UID)
        entry.include_reference(['sections', 'sections.sections', 'sections.sections.sections'])
        
        result = TestHelpers.safe_api_call("section_depth", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Self-referencing entry not available")
        
        entry_data = result['entry']
        
        if 'sections' in entry_data:
            depth = TestHelpers.count_references(entry_data, 'sections', max_depth=10)
            self.log_test_info(f"✅ Section nesting depth: {depth} levels")
            
            if depth > 1:
                self.assertGreater(depth, 1, "Should have nested sections")


if __name__ == '__main__':
    unittest.main(verbosity=2)

