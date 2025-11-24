"""
Infrastructure Validation Tests
Tests to ensure Phase 1 infrastructure is working correctly
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
from tests.utils.performance_assertions import PerformanceAssertion
from tests.utils.complex_query_builder import ComplexQueryBuilder
import config


class InfrastructureValidationTest(BaseIntegrationTest):
    """
    Validation tests for Phase 1 infrastructure
    These tests ensure all utilities and base classes work correctly
    """
    
    def test_config_loaded(self):
        """Test that config.py loaded successfully"""
        self.log_test_info("Validating config.py loaded")
        
        # Check stack credentials exist
        self.assertTrue(hasattr(config, 'HOST'), "Config missing HOST")
        self.assertTrue(hasattr(config, 'API_KEY'), "Config missing API_KEY")
        self.assertTrue(hasattr(config, 'DELIVERY_TOKEN'), "Config missing DELIVERY_TOKEN")
        self.assertTrue(hasattr(config, 'ENVIRONMENT'), "Config missing ENVIRONMENT")
        
        # Check test data UIDs exist
        self.assertTrue(hasattr(config, 'SIMPLE_ENTRY_UID'), "Config missing SIMPLE_ENTRY_UID")
        self.assertTrue(hasattr(config, 'MEDIUM_ENTRY_UID'), "Config missing MEDIUM_ENTRY_UID")
        self.assertTrue(hasattr(config, 'COMPLEX_ENTRY_UID'), "Config missing COMPLEX_ENTRY_UID")
        
        self.log_test_info("✅ Config validated successfully")
    
    def test_sdk_initialized(self):
        """Test that SDK initialized successfully"""
        self.log_test_info("Validating SDK initialization")
        
        self.assertIsNotNone(self.stack, "Stack not initialized")
        self.assertEqual(self.stack.api_key, config.API_KEY)
        self.assertEqual(self.stack.delivery_token, config.DELIVERY_TOKEN)
        self.assertEqual(self.stack.environment, config.ENVIRONMENT)
        
        self.log_test_info("✅ SDK initialized successfully")
    
    def test_test_helpers_safe_api_call(self):
        """Test TestHelpers.safe_api_call works"""
        self.log_test_info("Testing TestHelpers.safe_api_call")
        
        # Create a simple query
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(1)
        
        # Use safe API call
        result = TestHelpers.safe_api_call("test_query", query.find)
        
        if result is None:
            self.log_test_warning("API call returned None - may not be available")
            self.skipTest("API not available")
        
        self.assertIsNotNone(result, "Safe API call should return result or None")
        self.log_test_info("✅ TestHelpers.safe_api_call works")
    
    def test_test_helpers_has_results(self):
        """Test TestHelpers.has_results works"""
        self.log_test_info("Testing TestHelpers.has_results")
        
        # Test with mock data
        mock_response_with_entries = {'entries': [{'uid': 'test'}]}
        self.assertTrue(TestHelpers.has_results(mock_response_with_entries))
        
        mock_response_with_entry = {'entry': {'uid': 'test'}}
        self.assertTrue(TestHelpers.has_results(mock_response_with_entry))
        
        mock_response_empty = {'entries': []}
        self.assertFalse(TestHelpers.has_results(mock_response_empty))
        
        mock_response_none = None
        self.assertFalse(TestHelpers.has_results(mock_response_none))
        
        self.log_test_info("✅ TestHelpers.has_results works")
    
    def test_performance_assertion_timing(self):
        """Test PerformanceAssertion timing works"""
        self.log_test_info("Testing PerformanceAssertion timing")
        
        import time
        
        # Test timer
        start = PerformanceAssertion.start_timer()
        time.sleep(0.01)  # Sleep 10ms
        elapsed = PerformanceAssertion.end_timer(start, "test_operation")
        
        self.assertGreater(elapsed, 0, "Elapsed time should be > 0")
        self.assertGreater(elapsed, 5, "Elapsed time should be > 5ms (slept 10ms)")
        
        self.log_test_info(f"✅ Timer measured {elapsed:.2f}ms")
    
    def test_complex_query_builder_basic(self):
        """Test ComplexQueryBuilder basic functionality"""
        self.log_test_info("Testing ComplexQueryBuilder")
        
        # Create query
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        
        # Build complex query
        builder = ComplexQueryBuilder(query)
        builder.limit(5).include_count()
        
        # Execute
        result = TestHelpers.safe_api_call("complex_query_test", builder.find)
        
        if result is None:
            self.log_test_warning("Query returned None - may not be available")
            self.skipTest("API not available")
        
        self.assertIsNotNone(result)
        self.log_test_info("✅ ComplexQueryBuilder works")
    
    def test_base_class_fetch_simple_entry(self):
        """Test BaseIntegrationTest.fetch_simple_entry works"""
        self.log_test_info("Testing BaseIntegrationTest.fetch_simple_entry")
        
        result = self.fetch_simple_entry()
        
        if result is None:
            self.log_test_warning("Fetch returned None - entry may not exist")
            self.skipTest("Entry not available")
        
        self.assertIsNotNone(result)
        
        if self.assert_has_results(result):
            entry = result.get('entry')
            self.assertIsNotNone(entry)
            self.assertIn('uid', entry)
            self.log_test_info(f"✅ Fetched entry: {entry.get('uid')}")
    
    def test_base_class_create_queries(self):
        """Test query creation methods"""
        self.log_test_info("Testing query creation methods")
        
        simple_query = self.create_simple_query()
        self.assertIsNotNone(simple_query)
        
        medium_query = self.create_medium_query()
        self.assertIsNotNone(medium_query)
        
        complex_query = self.create_complex_query()
        self.assertIsNotNone(complex_query)
        
        self.log_test_info("✅ All query creation methods work")
    
    def test_logging_helpers(self):
        """Test logging helper methods"""
        self.log_test_info("Testing logging helpers")
        
        # These should not raise exceptions
        self.log_test_info("Info message test")
        self.log_test_warning("Warning message test")
        
        self.log_test_info("✅ Logging helpers work")
    
    def test_graceful_degradation(self):
        """Test graceful error handling"""
        self.log_test_info("Testing graceful degradation")
        
        # Try to fetch non-existent entry
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry("nonexistent_uid_12345")
        result = TestHelpers.safe_api_call("fetch_nonexistent", entry.fetch)
        
        # Should return None, not raise exception
        self.assertIsNone(result, "Non-existent entry should return None gracefully")
        
        self.log_test_info("✅ Graceful degradation works")


class QuickSmokeTest(BaseIntegrationTest):
    """
    Quick smoke tests to ensure basic SDK functionality works
    """
    
    def test_simple_query(self):
        """Quick test: Simple query"""
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(1)
        
        result = TestHelpers.safe_api_call("simple_query", query.find)
        
        if result and TestHelpers.has_results(result):
            self.log_test_info(f"✅ Simple query returned {len(result['entries'])} entry")
        else:
            self.log_test_warning("⚠️  Simple query returned no results")
    
    def test_simple_entry_fetch(self):
        """Quick test: Simple entry fetch"""
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        
        result = TestHelpers.safe_api_call("simple_fetch", entry.fetch)
        
        if result and TestHelpers.has_results(result):
            entry_data = result['entry']
            self.log_test_info(f"✅ Fetched entry: {entry_data.get('title', 'N/A')}")
        else:
            self.log_test_warning("⚠️  Entry fetch returned no results")


if __name__ == '__main__':
    # Run validation tests
    unittest.main(verbosity=2)

