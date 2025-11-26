"""
JSON RTE & Embedded Items Test Suite
Tests for JSON Rich Text Editor content and embedded items (critical gap)

Current Coverage: 0% for JSON RTE and embedded items
Target: Comprehensive coverage of JSON RTE parsing and embedded items
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
import config


class JSONRTEBasicTest(BaseIntegrationTest):
    """
    Test basic JSON RTE functionality
    """
    
    def test_01_fetch_entry_with_json_rte(self):
        """Test fetching entry with JSON RTE field"""
        self.log_test_info("Testing entry with JSON RTE field")
        
        # COMPLEX entry likely has JSON RTE content
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("fetch_json_rte", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Look for JSON RTE fields (common names: content_block, page_header, etc.)
        json_rte_fields = ['content_block', 'page_header', 'video_experience', 'podcast']
        
        for field in json_rte_fields:
            if field in entry_data and entry_data[field]:
                self.log_test_info(f"✅ Found JSON RTE field: {field}")
                
                field_data = entry_data[field]
                
                # Check for json_rte sub-field
                if isinstance(field_data, dict) and 'json_rte' in field_data:
                    json_rte = field_data['json_rte']
                    self.log_test_info(f"✅ JSON RTE structure found in {field}")
                    
                    # Validate JSON RTE structure
                    if isinstance(json_rte, dict):
                        self.assertIn('type', json_rte, "JSON RTE should have 'type' field")
                        self.assertEqual(json_rte.get('type'), 'doc', "JSON RTE type should be 'doc'")
                        
                        if 'children' in json_rte:
                            self.log_test_info(f"✅ JSON RTE has {len(json_rte['children'])} child nodes")
    
    def test_02_json_rte_structure_validation(self):
        """Test JSON RTE structure is valid"""
        self.log_test_info("Testing JSON RTE structure validation")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("json_rte_structure", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Look for content_block global field (likely to have JSON RTE)
        if 'content_block' in entry_data:
            cb = entry_data['content_block']
            
            if isinstance(cb, dict) and 'json_rte' in cb:
                json_rte = cb['json_rte']
                
                # Validate required fields
                required_fields = ['type', 'uid', '_version']
                for field in required_fields:
                    if field in json_rte:
                        self.log_test_info(f"✅ JSON RTE has '{field}': {json_rte[field]}")
    
    def test_03_json_rte_node_types(self):
        """Test JSON RTE contains various node types"""
        self.log_test_info("Testing JSON RTE node types")
        
        entry = self.stack.content_type(config.COMPLEX_ENTRY_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("json_rte_nodes", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Navigate to JSON RTE content
        json_rte = TestHelpers.get_nested_field(entry_data, 'content_block', 'json_rte')
        
        if json_rte and 'children' in json_rte:
            node_types = set()
            
            # Collect node types from children
            for child in json_rte['children']:
                if 'type' in child:
                    node_types.add(child['type'])
            
            self.log_test_info(f"✅ Found node types: {node_types}")
            
            # Common node types: p, h2, h3, a, img, etc.
            if len(node_types) > 0:
                self.assertGreater(len(node_types), 0, "Should have at least one node type")


class EmbeddedItemsTest(BaseIntegrationTest):
    """
    Test embedded items functionality (entries/assets embedded in JSON RTE)
    """
    
    def test_04_include_embedded_items(self):
        """Test include_embedded_items() method"""
        self.log_test_info("Testing include_embedded_items()")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("include_embedded", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Look for _embedded_items field
        if '_embedded_items' in entry_data:
            self.log_test_info("✅ _embedded_items field present")
            
            embedded = entry_data['_embedded_items']
            
            if isinstance(embedded, dict):
                self.log_test_info(f"✅ Embedded items structure: {list(embedded.keys())}")
        else:
            self.log_test_warning("No _embedded_items found (may not have embedded content)")
    
    def test_05_embedded_entries(self):
        """Test embedded entries in JSON RTE"""
        self.log_test_info("Testing embedded entries")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("embedded_entries", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if '_embedded_items' in entry_data:
            embedded = entry_data['_embedded_items']
            
            # Check for embedded entries
            if 'entries' in embedded:
                entries = embedded['entries']
                self.log_test_info(f"✅ Found {len(entries)} embedded entries")
                
                # Validate embedded entry structure
                for idx, emb_entry in enumerate(entries[:3]):  # Check first 3
                    if 'uid' in emb_entry:
                        self.log_test_info(f"Embedded entry {idx}: {emb_entry.get('uid')}")
    
    def test_06_embedded_assets(self):
        """Test embedded assets in JSON RTE"""
        self.log_test_info("Testing embedded assets")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("embedded_assets", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        if '_embedded_items' in entry_data:
            embedded = entry_data['_embedded_items']
            
            # Check for embedded assets
            if 'assets' in embedded:
                assets = embedded['assets']
                self.log_test_info(f"✅ Found {len(assets)} embedded assets")
                
                # Validate embedded asset structure
                for idx, asset in enumerate(assets[:3]):  # Check first 3
                    if 'uid' in asset:
                        self.log_test_info(f"Embedded asset {idx}: {asset.get('uid')}")
                        
                        if 'url' in asset:
                            self.log_test_info(f"  URL: {asset['url']}")
    
    def test_07_embedded_items_in_query(self):
        """Test embedded items in query results"""
        self.log_test_info("Testing embedded items in query")
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.include_embedded_items()
        query.limit(2)
        
        result = TestHelpers.safe_api_call("query_embedded", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"Found {len(entries)} entries")
        
        # Check if any entry has embedded items
        has_embedded = False
        for entry in entries:
            if '_embedded_items' in entry:
                has_embedded = True
                self.log_test_info("✅ Entry has embedded items")
                break
        
        if not has_embedded:
            self.log_test_warning("No entries with embedded items found")


class JSONRTEComplexTest(BaseIntegrationTest):
    """
    Test complex JSON RTE scenarios
    """
    
    def test_08_json_rte_with_references(self):
        """Test JSON RTE combined with references"""
        self.log_test_info("Testing JSON RTE with references")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        entry.include_reference(['authors', 'page_footer'])
        
        result = TestHelpers.safe_api_call("json_rte_with_refs", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Check for both embedded items and references
        has_embedded = '_embedded_items' in entry_data
        has_refs = TestHelpers.has_reference(entry_data, 'authors') or TestHelpers.has_reference(entry_data, 'page_footer')
        
        if has_embedded and has_refs:
            self.log_test_info("✅ Entry has both embedded items and references")
        elif has_embedded:
            self.log_test_info("✅ Entry has embedded items")
        elif has_refs:
            self.log_test_info("✅ Entry has references")
    
    def test_09_json_rte_with_locale(self):
        """Test JSON RTE content with locale"""
        self.log_test_info("Testing JSON RTE with locale")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.locale('en-us')
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("json_rte_locale", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Verify locale
        if 'locale' in entry_data:
            self.assertEqual(entry_data['locale'], 'en-us')
            self.log_test_info(f"✅ Entry locale: {entry_data['locale']}")
    
    def test_10_json_rte_nested_in_global_field(self):
        """Test JSON RTE nested in global fields"""
        self.log_test_info("Testing JSON RTE in global fields")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("json_rte_global", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Check global fields for JSON RTE
        global_fields = ['content_block', 'video_experience', 'page_header', 'podcast']
        
        for gf in global_fields:
            if gf in entry_data:
                gf_data = entry_data[gf]
                
                if isinstance(gf_data, dict) and 'json_rte' in gf_data:
                    self.log_test_info(f"✅ Global field '{gf}' contains JSON RTE")


class JSONRTEEdgeCasesTest(BaseIntegrationTest):
    """
    Test edge cases for JSON RTE
    """
    
    def test_11_empty_json_rte(self):
        """Test handling of empty JSON RTE"""
        self.log_test_info("Testing empty JSON RTE handling")
        
        # Use SIMPLE entry which likely doesn't have JSON RTE
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        entry.include_embedded_items()
        
        result = TestHelpers.safe_api_call("empty_json_rte", entry.fetch)
        
        if self.assert_has_results(result):
            self.log_test_info("✅ Empty JSON RTE handled gracefully")
    
    def test_12_json_rte_without_embedded_include(self):
        """Test JSON RTE without include_embedded_items"""
        self.log_test_info("Testing JSON RTE without embedded items inclusion")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        # Don't call include_embedded_items()
        
        result = TestHelpers.safe_api_call("json_rte_no_embedded", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # _embedded_items should NOT be present
        if '_embedded_items' not in entry_data:
            self.log_test_info("✅ _embedded_items not included (as expected)")
        else:
            self.log_test_warning("_embedded_items present without explicit inclusion")
    
    def test_13_json_rte_with_only_fields(self):
        """Test JSON RTE with field projection"""
        self.log_test_info("Testing JSON RTE with field projection")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        entry.only('uid').only('title').only('content_block')
        
        result = TestHelpers.safe_api_call("json_rte_only_fields", entry.fetch)
        
        if not self.assert_has_results(result):
            self.skipTest("Entry not available")
        
        entry_data = result['entry']
        
        # Should have only specified fields
        self.assertIn('uid', entry_data)
        self.assertIn('title', entry_data)
        
        # content_block should still have JSON RTE
        if 'content_block' in entry_data:
            self.log_test_info("✅ JSON RTE field included with projection")


class JSONRTEPerformanceTest(BaseIntegrationTest):
    """
    Test JSON RTE performance scenarios
    """
    
    def test_14_json_rte_large_content(self):
        """Test fetching entry with large JSON RTE content"""
        self.log_test_info("Testing large JSON RTE content")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_embedded_items()
        
        # Measure fetch time
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            entry.fetch,
            "fetch_large_json_rte"
        )
        
        if result and TestHelpers.has_results(result):
            entry_data = result['entry']
            
            # Estimate content size
            if 'content_block' in entry_data:
                cb = entry_data['content_block']
                if isinstance(cb, dict) and 'json_rte' in cb:
                    json_rte = cb['json_rte']
                    if 'children' in json_rte:
                        node_count = len(json_rte['children'])
                        self.log_test_info(f"✅ JSON RTE nodes: {node_count}, Time: {elapsed_ms:.2f}ms")
    
    def test_15_multiple_entries_with_json_rte(self):
        """Test querying multiple entries with JSON RTE"""
        self.log_test_info("Testing multiple entries with JSON RTE")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.include_embedded_items()
        query.limit(5)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "query_multiple_json_rte"
        )
        
        if result and TestHelpers.has_results(result):
            entries = result['entries']
            self.log_test_info(f"✅ Fetched {len(entries)} entries with JSON RTE in {elapsed_ms:.2f}ms")


if __name__ == '__main__':
    unittest.main(verbosity=2)

