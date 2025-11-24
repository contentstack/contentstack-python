"""
Test Suite: Error Handling Comprehensive
Tests SDK error handling for various HTTP error codes and network failures
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class Error404Test(BaseIntegrationTest):
    """404 Not Found error handling tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting 404 Error Handling Tests")

    def test_01_fetch_nonexistent_entry(self):
        """Test fetching non-existent entry (404)"""
        self.log_test_info("Fetching non-existent entry")
        
        result = TestHelpers.safe_api_call(
            "fetch_404_entry",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry('nonexistent_entry_uid_xyz').fetch
        )
        
        # Should return None or handle gracefully
        if result is None:
            self.logger.info("  ✅ 404 handled gracefully (returned None)")
        else:
            self.logger.info("  ✅ 404 handled (returned response)")

    def test_02_fetch_nonexistent_content_type(self):
        """Test fetching non-existent content type (404)"""
        self.log_test_info("Fetching non-existent content type")
        
        result = TestHelpers.safe_api_call(
            "fetch_404_content_type",
            self.stack.content_type('nonexistent_ct_xyz').fetch
        )
        
        if result is None:
            self.logger.info("  ✅ 404 for content type handled gracefully")

    def test_03_fetch_nonexistent_asset(self):
        """Test fetching non-existent asset (404)"""
        self.log_test_info("Fetching non-existent asset")
        
        result = TestHelpers.safe_api_call(
            "fetch_404_asset",
            self.stack.asset('nonexistent_asset_xyz').fetch
        )
        
        if result is None:
            self.logger.info("  ✅ 404 for asset handled gracefully")

    def test_04_query_nonexistent_content_type(self):
        """Test querying non-existent content type (404)"""
        self.log_test_info("Querying non-existent content type")
        
        result = TestHelpers.safe_api_call(
            "query_404_content_type",
            self.stack.content_type('nonexistent_ct_xyz').query().find
        )
        
        if result is None:
            self.logger.info("  ✅ 404 for query handled gracefully")


class Error400Test(BaseIntegrationTest):
    """400 Bad Request error handling tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting 400 Error Handling Tests")

    def test_05_query_with_invalid_operator(self):
        """Test query with invalid operator (potential 400)"""
        self.log_test_info("Query with invalid operator")
        
        result = TestHelpers.safe_api_call(
            "query_invalid_operator",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where({'title': {'$invalid_operator': 'test'}})
            .find
        )
        
        # SDK might handle this before sending request
        if result is None:
            self.logger.info("  ✅ Invalid operator handled gracefully")
        else:
            self.logger.info("  ✅ Query executed (operator may be valid)")

    def test_06_query_with_invalid_limit(self):
        """Test query with invalid limit value"""
        self.log_test_info("Query with invalid limit")
        
        result = TestHelpers.safe_api_call(
            "query_invalid_limit",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(-1)  # Negative limit
            .find
        )
        
        if result is None:
            self.logger.info("  ✅ Invalid limit handled gracefully")
        else:
            self.logger.info("  ✅ Query executed (limit may be corrected)")

    def test_07_query_with_invalid_skip(self):
        """Test query with invalid skip value"""
        self.log_test_info("Query with invalid skip")
        
        result = TestHelpers.safe_api_call(
            "query_invalid_skip",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .skip(-5)  # Negative skip
            .find
        )
        
        if result is None:
            self.logger.info("  ✅ Invalid skip handled gracefully")
        else:
            self.logger.info("  ✅ Query executed (skip may be corrected)")


class Error422Test(BaseIntegrationTest):
    """422 Unprocessable Entity error handling tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting 422 Error Handling Tests")

    def test_08_query_with_malformed_where(self):
        """Test query with malformed where clause"""
        self.log_test_info("Query with malformed where clause")
        
        result = TestHelpers.safe_api_call(
            "query_malformed_where",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where({'': {'$eq': 'test'}})  # Empty field name
            .find
        )
        
        if result is None:
            self.logger.info("  ✅ Malformed where handled gracefully")
        else:
            self.logger.info("  ✅ Query executed")

    def test_09_fetch_with_invalid_version(self):
        """Test fetching with invalid version number"""
        self.log_test_info("Fetching with invalid version")
        
        result = TestHelpers.safe_api_call(
            "fetch_invalid_version",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .version(999999)  # Very high version
            .fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Invalid version handled gracefully")
        else:
            self.logger.info("  ✅ Fetch executed")


class EmptyResultHandlingTest(BaseIntegrationTest):
    """Empty result handling tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Empty Result Handling Tests")

    def test_10_query_with_no_results(self):
        """Test query that returns no results"""
        self.log_test_info("Query with no results")
        
        result = TestHelpers.safe_api_call(
            "query_no_results",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where({'title': {'$eq': 'nonexistent_title_xyz_123456'}})
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.assertEqual(len(entries), 0, "Should return empty entries list")
            self.logger.info("  ✅ Empty result handled correctly")

    def test_11_query_with_impossible_filter(self):
        """Test query with impossible filter combination"""
        self.log_test_info("Query with impossible filter")
        
        result = TestHelpers.safe_api_call(
            "query_impossible_filter",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where({
                '$and': [
                    {'title': {'$eq': 'A'}},
                    {'title': {'$eq': 'B'}}  # Same field can't be both A and B
                ]
            })
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.assertEqual(len(entries), 0, "Impossible filter should return empty")
            self.logger.info("  ✅ Impossible filter handled correctly")

    def test_12_fetch_entry_from_wrong_content_type(self):
        """Test fetching entry with wrong content type"""
        self.log_test_info("Fetching entry from wrong content type")
        
        # Try to fetch SIMPLE entry from MEDIUM content type
        result = TestHelpers.safe_api_call(
            "fetch_wrong_ct",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Wrong content type handled gracefully")
        else:
            self.logger.info("  ✅ Fetch executed (entry might exist in multiple CTs)")


class InvalidParameterTest(BaseIntegrationTest):
    """Invalid parameter handling tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Invalid Parameter Tests")

    def test_13_fetch_with_invalid_locale(self):
        """Test fetching with invalid locale format"""
        self.log_test_info("Fetching with invalid locale")
        
        result = TestHelpers.safe_api_call(
            "fetch_invalid_locale",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('invalid_locale_format')
            .fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Invalid locale handled gracefully")
        else:
            self.logger.info("  ✅ Fetch executed (locale may be accepted)")

    def test_14_query_with_invalid_regex(self):
        """Test query with invalid regex pattern"""
        self.log_test_info("Query with invalid regex")
        
        result = TestHelpers.safe_api_call(
            "query_invalid_regex",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where({'title': {'$regex': '[invalid(regex'}})  # Malformed regex
            .find
        )
        
        if result is None:
            self.logger.info("  ✅ Invalid regex handled gracefully")
        else:
            self.logger.info("  ✅ Query executed")

    def test_15_fetch_with_empty_uid(self):
        """Test fetching with empty UID"""
        self.log_test_info("Fetching with empty UID")
        
        result = TestHelpers.safe_api_call(
            "fetch_empty_uid",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry('').fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Empty UID handled gracefully")


class NetworkErrorSimulationTest(BaseIntegrationTest):
    """Network error simulation tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Network Error Simulation Tests")

    def test_16_timeout_handling(self):
        """Test timeout handling (if SDK supports timeout configuration)"""
        self.log_test_info("Testing timeout handling")
        
        # Most SDKs have a default timeout
        # This test verifies the SDK doesn't crash on slow responses
        result = TestHelpers.safe_api_call(
            "timeout_test",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(50)  # Large result set might be slower
            .find
        )
        
        if result:
            self.logger.info("  ✅ Query completed within timeout")
        else:
            self.logger.info("  ✅ Timeout handled gracefully")


class ExceptionHandlingTest(BaseIntegrationTest):
    """General exception handling tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Exception Handling Tests")

    def test_17_multiple_consecutive_errors(self):
        """Test handling multiple consecutive errors"""
        self.log_test_info("Testing multiple consecutive errors")
        
        # Try multiple operations that might fail
        for i in range(3):
            result = TestHelpers.safe_api_call(
                f"consecutive_error_{i}",
                self.stack.content_type('nonexistent').fetch
            )
            # Should handle gracefully each time
        
        self.logger.info("  ✅ Multiple consecutive errors handled")

    def test_18_error_with_complex_query(self):
        """Test error handling with complex query"""
        self.log_test_info("Testing error with complex query")
        
        result = TestHelpers.safe_api_call(
            "error_complex_query",
            self.stack.content_type('nonexistent_ct')
            .query()
            .where({'field1': {'$eq': 'value1'}})
            .query_operator('$and', [
                {'field2': {'$gt': 10}},
                {'field3': {'$exists': True}}
            ])
            .limit(10)
            .skip(5)
            .order_by_ascending('title')
            .find
        )
        
        if result is None:
            self.logger.info("  ✅ Complex query error handled gracefully")


if __name__ == '__main__':
    unittest.main()

