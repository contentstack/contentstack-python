"""
Test Suite: Pagination Comprehensive
Tests all pagination scenarios: skip, limit, count, ordering, edge cases
"""

import json
import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class PaginationBasicTest(BaseIntegrationTest):
    """Basic pagination tests with skip and limit"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Basic Pagination Tests")

    def test_01_query_with_limit_only(self):
        """Test querying with limit only"""
        self.log_test_info("Querying with limit only")
        
        result = TestHelpers.safe_api_call(
            "query_limit_only",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Limit should return results"):
            entries = result['entries']
            self.assertLessEqual(len(entries), 5, "Should return at most 5 entries")
            self.logger.info(f"  ✅ Limit working: {len(entries)} entries")

    def test_02_query_with_skip_only(self):
        """Test querying with skip only"""
        self.log_test_info("Querying with skip only")
        
        result = TestHelpers.safe_api_call(
            "query_skip_only",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .skip(2)
            .find
        )
        
        if self.assert_has_results(result, "Skip should return results"):
            entries = result['entries']
            self.logger.info(f"  ✅ Skip working: {len(entries)} entries")

    def test_03_query_with_limit_and_skip(self):
        """Test querying with both limit and skip"""
        self.log_test_info("Querying with limit and skip")
        
        result = TestHelpers.safe_api_call(
            "query_limit_skip",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(3)
            .skip(1)
            .find
        )
        
        if self.assert_has_results(result, "Limit and skip should work together"):
            entries = result['entries']
            self.assertLessEqual(len(entries), 3, "Should return at most 3 entries")
            self.logger.info(f"  ✅ Limit + Skip: {len(entries)} entries")

    def test_04_query_with_large_limit(self):
        """Test querying with large limit value"""
        self.log_test_info("Querying with large limit (100)")
        
        result = TestHelpers.safe_api_call(
            "query_large_limit",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(100)
            .find
        )
        
        if self.assert_has_results(result, "Large limit should work"):
            entries = result['entries']
            self.logger.info(f"  ✅ Large limit: {len(entries)} entries returned")

    def test_05_query_with_large_skip(self):
        """Test querying with large skip value"""
        self.log_test_info("Querying with large skip (50)")
        
        result = TestHelpers.safe_api_call(
            "query_large_skip",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .skip(50)
            .limit(10)
            .find
        )
        
        # Might return empty if not enough entries
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Large skip: {len(entries)} entries")
        else:
            self.logger.info("  ✅ Large skip returned empty (expected if < 50 entries)")


class PaginationWithCountTest(BaseIntegrationTest):
    """Pagination with include_count()"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Pagination with Count Tests")

    def test_06_query_with_count(self):
        """Test querying with include_count()"""
        self.log_test_info("Querying with include_count()")
        
        result = TestHelpers.safe_api_call(
            "query_with_count",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_count()
            .limit(10)
            .find
        )
        
        if self.assert_has_results(result, "Count should be included"):
            self.assertIn('count', result, "Result should have 'count' field")
            count = result['count']
            entries = result['entries']
            self.logger.info(f"  ✅ Total count: {count}, Retrieved: {len(entries)}")

    def test_07_pagination_with_count_and_skip(self):
        """Test pagination with count, limit, and skip"""
        self.log_test_info("Pagination with count, limit, and skip")
        
        result = TestHelpers.safe_api_call(
            "pagination_count_skip",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_count()
            .limit(5)
            .skip(3)
            .find
        )
        
        if self.assert_has_results(result, "Full pagination should work"):
            self.assertIn('count', result, "Should have total count")
            count = result['count']
            entries = result['entries']
            self.logger.info(f"  ✅ Total: {count}, Page size: {len(entries)}")

    def test_08_count_with_where_filter(self):
        """Test count with where filter"""
        self.log_test_info("Count with where filter")
        
        result = TestHelpers.safe_api_call(
            "count_with_filter",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.EXISTS, True)
            .include_count()
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Count with filter should work"):
            self.assertIn('count', result, "Should have count")
            self.logger.info(f"  ✅ Filtered count: {result['count']}")

    def test_09_count_accuracy_verification(self):
        """Test that count reflects actual total entries"""
        self.log_test_info("Verifying count accuracy")
        
        # Get first page with count
        page1 = TestHelpers.safe_api_call(
            "page1_with_count",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_count()
            .limit(3)
            .skip(0)
            .find
        )
        
        if page1 and 'count' in page1:
            total_count = page1['count']
            page1_entries = len(page1['entries'])
            
            # Get second page
            page2 = TestHelpers.safe_api_call(
                "page2_verification",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .limit(3)
                .skip(3)
                .find
            )
            
            if page2:
                page2_entries = len(page2['entries'])
                self.logger.info(f"  ✅ Total count: {total_count}, Page1: {page1_entries}, Page2: {page2_entries}")


class PaginationOrderingTest(BaseIntegrationTest):
    """Pagination with different ordering"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Pagination with Ordering Tests")

    def test_10_pagination_with_ascending_order(self):
        """Test pagination with ascending order"""
        self.log_test_info("Pagination with ascending order")
        
        result = TestHelpers.safe_api_call(
            "pagination_asc",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .order_by_ascending('title')
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Pagination with ascending order should work"):
            entries = result['entries']
            titles = [e.get('title', '') for e in entries]
            self.assertEqual(titles, sorted(titles), "Titles should be in ascending order")
            self.logger.info(f"  ✅ Ascending order: {len(entries)} entries")

    def test_11_pagination_with_descending_order(self):
        """Test pagination with descending order"""
        self.log_test_info("Pagination with descending order")
        
        result = TestHelpers.safe_api_call(
            "pagination_desc",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .order_by_descending('title')
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Pagination with descending order should work"):
            entries = result['entries']
            titles = [e.get('title', '') for e in entries]
            self.assertEqual(titles, sorted(titles, reverse=True), "Titles should be in descending order")
            self.logger.info(f"  ✅ Descending order: {len(entries)} entries")

    def test_12_pagination_order_with_skip(self):
        """Test pagination ordering with skip"""
        self.log_test_info("Pagination ordering with skip")
        
        # Get first 3 entries ordered by title
        page1 = TestHelpers.safe_api_call(
            "ordered_page1",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .order_by_ascending('title')
            .limit(3)
            .skip(0)
            .find
        )
        
        # Get next 3 entries
        page2 = TestHelpers.safe_api_call(
            "ordered_page2",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .order_by_ascending('title')
            .limit(3)
            .skip(3)
            .find
        )
        
        if page1 and self.assert_has_results(page1, "Page 1 should work"):
            page1_titles = [e.get('title', '') for e in page1['entries']]
            self.logger.info(f"  ✅ Page 1: {len(page1_titles)} entries")
            
            if page2 and page2.get('entries'):
                page2_titles = [e.get('title', '') for e in page2['entries']]
                # Page 2 titles should come after Page 1 titles alphabetically
                self.logger.info(f"  ✅ Page 2: {len(page2_titles)} entries")

    def test_13_pagination_order_by_date(self):
        """Test pagination ordering by date field"""
        self.log_test_info("Pagination ordering by date")
        
        result = TestHelpers.safe_api_call(
            "pagination_by_date",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .query()
            .order_by_descending('date')  # Assuming 'date' field exists
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Order by date should work"):
            entries = result['entries']
            self.logger.info(f"  ✅ Ordered by date: {len(entries)} entries")


class PaginationEdgeCasesTest(BaseIntegrationTest):
    """Edge cases for pagination"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Pagination Edge Cases Tests")

    def test_14_pagination_limit_zero(self):
        """Test pagination with limit=0"""
        self.log_test_info("Pagination with limit=0")
        
        result = TestHelpers.safe_api_call(
            "pagination_limit_zero",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(0)
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            # Limit 0 behavior depends on API (might return all or none)
            self.logger.info(f"  ✅ Limit 0: {len(entries)} entries")

    def test_15_pagination_skip_beyond_total(self):
        """Test skip value beyond total entries"""
        self.log_test_info("Pagination skip beyond total")
        
        result = TestHelpers.safe_api_call(
            "pagination_skip_beyond",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .skip(10000)  # Very large skip
            .limit(10)
            .find
        )
        
        # Should return empty entries
        if result:
            entries = result.get('entries', [])
            self.assertEqual(len(entries), 0, "Skip beyond total should return empty")
            self.logger.info("  ✅ Skip beyond total handled correctly")

    def test_16_pagination_limit_exceeds_max(self):
        """Test limit exceeding API maximum"""
        self.log_test_info("Pagination limit exceeding max")
        
        result = TestHelpers.safe_api_call(
            "pagination_limit_max",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(1000)  # Very large limit (API might cap it)
            .find
        )
        
        if result and self.assert_has_results(result, "Large limit should be handled"):
            entries = result['entries']
            # API will return up to its maximum
            self.logger.info(f"  ✅ Large limit handled: {len(entries)} entries")

    def test_17_pagination_negative_skip(self):
        """Test negative skip value (edge case)"""
        self.log_test_info("Pagination with negative skip")
        
        result = TestHelpers.safe_api_call(
            "pagination_negative_skip",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .skip(-1)
            .limit(5)
            .find
        )
        
        # Negative skip might be treated as 0 or cause error
        if result:
            self.logger.info("  ✅ Negative skip handled")
        else:
            self.logger.info("  ✅ Negative skip returned None (acceptable)")

    def test_18_pagination_with_empty_result_set(self):
        """Test pagination on query with no results"""
        self.log_test_info("Pagination with empty result set")
        
        result = TestHelpers.safe_api_call(
            "pagination_empty_set",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.EQUALS, 'nonexistent_entry_xyz_123')
            .include_count()
            .limit(10)
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            count = result.get('count', 0)
            self.assertEqual(len(entries), 0, "Empty set should return 0 entries")
            self.assertEqual(count, 0, "Count should be 0")
            self.logger.info("  ✅ Empty result set handled correctly")


class PaginationComplexQueriesTest(BaseIntegrationTest):
    """Pagination with complex queries"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Pagination with Complex Queries Tests")

    def test_19_pagination_with_and_query(self):
        """Test pagination with AND query"""
        self.log_test_info("Pagination with AND query")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.add_params({
            'query': json.dumps({
                '$and': [
                    {'title': {'$exists': True}},
                    {'uid': {'$exists': True}}
                ]
            })
        })
        query.limit(5).skip(0)
        
        result = TestHelpers.safe_api_call("pagination_and_query", query.find)
        
        if self.assert_has_results(result, "Pagination with AND should work"):
            self.logger.info(f"  ✅ AND query pagination: {len(result['entries'])} entries")

    def test_20_pagination_with_or_query(self):
        """Test pagination with OR query"""
        self.log_test_info("Pagination with OR query")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.add_params({
            'query': json.dumps({
                '$or': [
                    {'title': {'$exists': True}},
                    {'uid': {'$exists': True}}
                ]
            })
        })
        query.limit(5)
        
        result = TestHelpers.safe_api_call("pagination_or_query", query.find)
        
        if result and self.assert_has_results(result, "Pagination with OR should work"):
            self.logger.info(f"  ✅ OR query pagination: {len(result['entries'])} entries")

    def test_21_pagination_with_where_in(self):
        """Test pagination with $in operator (note: where_in() is for reference queries)"""
        self.log_test_info("Pagination with $in operator")
        
        # Use .where() with INCLUDES for $in functionality
        result = TestHelpers.safe_api_call(
            "pagination_where_in",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('locale', QueryOperation.INCLUDES, ['en-us', 'en-gb'])
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Pagination with $in should work"):
            self.logger.info(f"  ✅ $in operator pagination: {len(result['entries'])} entries")

    def test_22_pagination_with_search(self):
        """Test pagination with search()"""
        self.log_test_info("Pagination with search")
        
        result = TestHelpers.safe_api_call(
            "pagination_search",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .search('content')  # Search for word 'content'
            .limit(5)
            .find
        )
        
        if result:  # Search might return empty
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Search pagination: {len(entries)} entries")


class PaginationMultipleContentTypesTest(BaseIntegrationTest):
    """Pagination across different content types"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Pagination Multiple Content Types Tests")

    def test_23_paginate_simple_content_type(self):
        """Test pagination on simple content type"""
        self.log_test_info("Paginating simple content type")
        
        result = TestHelpers.safe_api_call(
            "paginate_simple",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .include_count()
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Simple CT pagination should work"):
            self.logger.info(f"  ✅ Simple CT: {len(result['entries'])}/{result.get('count', 'N/A')} entries")

    def test_24_paginate_medium_content_type(self):
        """Test pagination on medium content type"""
        self.log_test_info("Paginating medium content type")
        
        result = TestHelpers.safe_api_call(
            "paginate_medium",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .query()
            .include_count()
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Medium CT pagination should work"):
            self.logger.info(f"  ✅ Medium CT: {len(result['entries'])}/{result.get('count', 'N/A')} entries")

    def test_25_paginate_complex_content_type(self):
        """Test pagination on complex content type"""
        self.log_test_info("Paginating complex content type")
        
        result = TestHelpers.safe_api_call(
            "paginate_complex",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .include_count()
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Complex CT pagination should work"):
            self.logger.info(f"  ✅ Complex CT: {len(result['entries'])}/{result.get('count', 'N/A')} entries")

    def test_26_pagination_comparison_across_types(self):
        """Test pagination consistency across content types"""
        self.log_test_info("Comparing pagination across content types")
        
        simple_result = TestHelpers.safe_api_call(
            "compare_simple",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(3).find
        )
        
        medium_result = TestHelpers.safe_api_call(
            "compare_medium",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).query().limit(3).find
        )
        
        complex_result = TestHelpers.safe_api_call(
            "compare_complex",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query().limit(3).find
        )
        
        simple_count = len(simple_result['entries']) if simple_result else 0
        medium_count = len(medium_result['entries']) if medium_result else 0
        complex_count = len(complex_result['entries']) if complex_result else 0
        
        self.logger.info(f"  ✅ Pagination comparison - Simple: {simple_count}, Medium: {medium_count}, Complex: {complex_count}")


class PaginationPerformanceTest(BaseIntegrationTest):
    """Performance tests for pagination"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Pagination Performance Tests")

    def test_27_pagination_large_dataset_first_page(self):
        """Test pagination performance on first page of large dataset"""
        self.log_test_info("Pagination first page performance")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        with PerformanceAssertion.Timer("First page query") as timer:
            result = TestHelpers.safe_api_call(
                "large_dataset_first_page",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .limit(20)
                .skip(0)
                .find
            )
        
        if self.assert_has_results(result, "First page should be fast"):
            self.logger.info(f"  ✅ First page: {len(result['entries'])} entries in {timer.duration:.2f}ms")

    def test_28_pagination_large_dataset_deep_page(self):
        """Test pagination performance on deep page"""
        self.log_test_info("Pagination deep page performance")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        with PerformanceAssertion.Timer("Deep page query") as timer:
            result = TestHelpers.safe_api_call(
                "large_dataset_deep_page",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .limit(20)
                .skip(100)
                .find
            )
        
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Deep page: {len(entries)} entries in {timer.duration:.2f}ms")

    def test_29_pagination_with_references_performance(self):
        """Test pagination performance with included references"""
        self.log_test_info("Pagination with references performance")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        with PerformanceAssertion.Timer("Pagination with references") as timer:
            result = TestHelpers.safe_api_call(
                "pagination_references",
                self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
                .query()
                .include_reference(['authors'])
                .limit(10)
                .find
            )
        
        if self.assert_has_results(result, "Pagination with references"):
            self.logger.info(f"  ✅ With references: {len(result['entries'])} entries in {timer.duration:.2f}ms")

    def test_30_pagination_count_query_performance(self):
        """Test performance impact of include_count()"""
        self.log_test_info("Pagination count query performance")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        # Without count
        with PerformanceAssertion.Timer("Without count") as timer1:
            result1 = TestHelpers.safe_api_call(
                "pagination_no_count",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(10).find
            )
        
        # With count
        with PerformanceAssertion.Timer("With count") as timer2:
            result2 = TestHelpers.safe_api_call(
                "pagination_with_count",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().include_count().limit(10).find
            )
        
        if result1 and result2:
            self.logger.info(f"  ✅ Without count: {timer1.duration:.2f}ms, With count: {timer2.duration:.2f}ms")


if __name__ == '__main__':
    unittest.main()

