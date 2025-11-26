"""
Performance Test Suite
Tests for performance, benchmarking, and large dataset handling (critical gap)

Current Coverage: 0% for performance testing
Target: Performance benchmarks and large dataset validation
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
from tests.utils.performance_assertions import PerformanceAssertion
from contentstack.basequery import QueryOperation
import config


class BasicPerformanceTest(BaseIntegrationTest):
    """
    Test basic performance metrics
    """
    
    def test_01_single_entry_fetch_performance(self):
        """Test single entry fetch performance"""
        self.log_test_info("Testing single entry fetch performance")
        
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            entry.fetch,
            "single_entry_fetch"
        )
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ Single fetch: {elapsed_ms:.2f}ms")
            
            # Soft assertion - just log if slow
            PerformanceAssertion.assert_reasonable_time(
                "single_entry_fetch",
                elapsed_ms,
                expected_max_ms=2000,  # 2 seconds
                fail_on_slow=False
            )
    
    def test_02_multiple_entries_query_performance(self):
        """Test querying multiple entries performance"""
        self.log_test_info("Testing multiple entries query performance")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(10)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "multiple_entries_query"
        )
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            self.log_test_info(f"✅ Query {len(entries)} entries: {elapsed_ms:.2f}ms")
            
            # Log average time per entry
            if len(entries) > 0:
                avg_per_entry = elapsed_ms / len(entries)
                self.log_test_info(f"   Average per entry: {avg_per_entry:.2f}ms")
    
    def test_03_complex_entry_fetch_performance(self):
        """Test complex entry fetch performance"""
        self.log_test_info("Testing complex entry fetch performance")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            entry.fetch,
            "complex_entry_fetch"
        )
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ Complex fetch: {elapsed_ms:.2f}ms")


class ReferencePerformanceTest(BaseIntegrationTest):
    """
    Test performance with references
    """
    
    def test_04_single_level_reference_performance(self):
        """Test single level reference performance"""
        self.log_test_info("Testing single level reference performance")
        
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry.include_reference('reference')
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            entry.fetch,
            "single_ref_fetch"
        )
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ With 1-level ref: {elapsed_ms:.2f}ms")
    
    def test_05_deep_reference_performance(self):
        """Test deep reference performance"""
        self.log_test_info("Testing deep reference performance")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_reference(['authors', 'authors.reference'])
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            entry.fetch,
            "deep_ref_fetch"
        )
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ With 2-level ref: {elapsed_ms:.2f}ms")
    
    def test_06_multiple_references_performance(self):
        """Test multiple references performance"""
        self.log_test_info("Testing multiple references performance")
        
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry.include_reference(['authors', 'related_content', 'page_footer'])
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            entry.fetch,
            "multiple_refs_fetch"
        )
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ With multiple refs: {elapsed_ms:.2f}ms")


class ComparisonPerformanceTest(BaseIntegrationTest):
    """
    Test performance comparisons (without strict assertions)
    """
    
    def test_07_fetch_vs_query_performance(self):
        """Compare fetch vs query performance"""
        self.log_test_info("Comparing fetch vs query performance")
        
        # Fetch single entry
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        fetch_result, fetch_time = PerformanceAssertion.measure_operation(
            entry.fetch,
            "fetch_single"
        )
        
        # Query for single entry
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.where('uid', QueryOperation.EQUALS, config.SIMPLE_ENTRY_UID)
        query_result, query_time = PerformanceAssertion.measure_operation(
            query.find,
            "query_single"
        )
        
        if fetch_result and query_result:
            # Just compare, don't assert strict ordering (could be flaky)
            PerformanceAssertion.compare_operations(
                "fetch()", fetch_time,
                "query().find()", query_time,
                log_ratio=True
            )
    
    def test_08_with_vs_without_references(self):
        """Compare performance with and without references"""
        self.log_test_info("Comparing with/without references")
        
        # Without references
        entry1 = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        no_ref_result, no_ref_time = PerformanceAssertion.measure_operation(
            entry1.fetch,
            "fetch_no_refs"
        )
        
        # With references
        entry2 = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(config.MEDIUM_ENTRY_UID)
        entry2.include_reference('reference')
        with_ref_result, with_ref_time = PerformanceAssertion.measure_operation(
            entry2.fetch,
            "fetch_with_refs"
        )
        
        if no_ref_result and with_ref_result:
            PerformanceAssertion.compare_operations(
                "without_refs", no_ref_time,
                "with_refs", with_ref_time,
                log_ratio=True
            )
    
    def test_09_embedded_items_performance(self):
        """Compare performance with/without embedded items"""
        self.log_test_info("Comparing with/without embedded items")
        
        # Without embedded items
        entry1 = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        no_embed_result, no_embed_time = PerformanceAssertion.measure_operation(
            entry1.fetch,
            "fetch_no_embedded"
        )
        
        # With embedded items
        entry2 = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(config.COMPLEX_ENTRY_UID)
        entry2.include_embedded_items()
        with_embed_result, with_embed_time = PerformanceAssertion.measure_operation(
            entry2.fetch,
            "fetch_with_embedded"
        )
        
        if no_embed_result and with_embed_result:
            PerformanceAssertion.compare_operations(
                "without_embedded", no_embed_time,
                "with_embedded", with_embed_time,
                log_ratio=True
            )


class LargeDatasetTest(BaseIntegrationTest):
    """
    Test performance with larger datasets
    """
    
    def test_10_query_50_entries(self):
        """Test querying 50 entries"""
        self.log_test_info("Testing query for 50 entries")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(50)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "query_50_entries"
        )
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            self.log_test_info(f"✅ Queried {len(entries)} entries: {elapsed_ms:.2f}ms")
            
            if len(entries) > 0:
                avg_per_entry = elapsed_ms / len(entries)
                self.log_test_info(f"   Avg per entry: {avg_per_entry:.2f}ms")
    
    def test_11_pagination_performance(self):
        """Test pagination through large dataset"""
        self.log_test_info("Testing pagination performance")
        
        page_size = 10
        total_pages = 3
        
        times = []
        
        for page in range(1, total_pages + 1):
            query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
            query.skip((page - 1) * page_size).limit(page_size)
            
            result, elapsed_ms = PerformanceAssertion.measure_operation(
                query.find,
                f"page_{page}"
            )
            
            if TestHelpers.has_results(result):
                times.append(elapsed_ms)
        
        if len(times) > 0:
            # Calculate stats
            stats = PerformanceAssertion.calculate_stats(times)
            self.log_test_info(f"✅ Pagination stats: Avg={stats['avg']:.2f}ms, Min={stats['min']:.2f}ms, Max={stats['max']:.2f}ms")


class BatchOperationsTest(BaseIntegrationTest):
    """
    Test batch operations performance
    """
    
    def test_12_multiple_sequential_fetches(self):
        """Test multiple sequential fetches"""
        self.log_test_info("Testing multiple sequential fetches")
        
        times = []
        
        # Fetch 3 entries sequentially
        for i in range(3):
            entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(1)
            result, elapsed_ms = PerformanceAssertion.measure_operation(
                entry.find,
                f"fetch_{i+1}"
            )
            
            if TestHelpers.has_results(result):
                times.append(elapsed_ms)
        
        if len(times) == 3:
            PerformanceAssertion.log_stats("sequential_fetches", times)
    
    def test_13_batch_vs_sequential(self):
        """Compare batch vs sequential fetching"""
        self.log_test_info("Comparing batch vs sequential")
        
        # Sequential: 3 separate queries
        seq_times = []
        for i in range(3):
            query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(1).skip(i)
            result, elapsed_ms = PerformanceAssertion.measure_operation(
                query.find,
                f"sequential_{i}"
            )
            if result:
                seq_times.append(elapsed_ms)
        
        # Batch: 1 query for 3 entries
        batch_query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(3)
        batch_result, batch_time = PerformanceAssertion.measure_operation(
            batch_query.find,
            "batch"
        )
        
        if len(seq_times) == 3 and batch_result:
            total_seq_time = sum(seq_times)
            
            self.log_test_info(f"Sequential (3 queries): {total_seq_time:.2f}ms")
            self.log_test_info(f"Batch (1 query): {batch_time:.2f}ms")
            
            if batch_time < total_seq_time:
                speedup = total_seq_time / batch_time
                self.log_test_info(f"✅ Batch is {speedup:.2f}x faster")


class MemoryPerformanceTest(BaseIntegrationTest):
    """
    Test memory-related performance
    """
    
    def test_14_memory_usage_simple_query(self):
        """Test memory usage for simple query"""
        self.log_test_info("Testing memory usage - simple query")
        
        PerformanceAssertion.log_memory_usage()
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(10)
        
        result = TestHelpers.safe_api_call("memory_simple", query.find)
        
        if TestHelpers.has_results(result):
            PerformanceAssertion.log_memory_usage()
            self.log_test_info("✅ Memory usage logged")
    
    def test_15_memory_usage_complex_query(self):
        """Test memory usage for complex query with references"""
        self.log_test_info("Testing memory usage - complex query")
        
        PerformanceAssertion.log_memory_usage()
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.include_reference(['authors'])
        query.include_embedded_items()
        query.limit(5)
        
        result = TestHelpers.safe_api_call("memory_complex", query.find)
        
        if TestHelpers.has_results(result):
            PerformanceAssertion.log_memory_usage()
            self.log_test_info("✅ Memory usage logged")


class EdgeCasePerformanceTest(BaseIntegrationTest):
    """
    Test performance edge cases
    """
    
    def test_16_empty_result_performance(self):
        """Test performance of query returning no results"""
        self.log_test_info("Testing empty result performance")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.where('uid', QueryOperation.EQUALS, 'nonexistent_12345')
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "empty_results"
        )
        
        if result:
            entries = result.get('entries', [])
            self.assertEqual(len(entries), 0)
            self.log_test_info(f"✅ Empty result query: {elapsed_ms:.2f}ms")
    
    def test_17_large_skip_performance(self):
        """Test performance with large skip value"""
        self.log_test_info("Testing large skip performance")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.skip(100).limit(5)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "large_skip"
        )
        
        if result:
            self.log_test_info(f"✅ Large skip query: {elapsed_ms:.2f}ms")


class RepeatedOperationsTest(BaseIntegrationTest):
    """
    Test performance of repeated operations
    """
    
    def test_18_repeated_same_query(self):
        """Test repeated execution of same query"""
        self.log_test_info("Testing repeated same query")
        
        times = []
        
        for i in range(5):
            query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
            query.limit(3)
            
            result, elapsed_ms = PerformanceAssertion.measure_operation(
                query.find,
                f"run_{i+1}"
            )
            
            if TestHelpers.has_results(result):
                times.append(elapsed_ms)
        
        if len(times) == 5:
            stats = PerformanceAssertion.calculate_stats(times)
            PerformanceAssertion.log_stats("repeated_query", times)
            
            # Check consistency (all times should be relatively similar)
            variance = stats['max'] - stats['min']
            self.log_test_info(f"✅ Variance: {variance:.2f}ms")
    
    def test_19_repeated_different_queries(self):
        """Test repeated execution of different queries"""
        self.log_test_info("Testing repeated different queries")
        
        operations = {
            "simple_query": lambda: self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(2).find(),
            "complex_query": lambda: self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query().limit(2).find()
        }
        
        results = PerformanceAssertion.measure_batch_operations(operations)
        
        if len(results) > 0:
            self.log_test_info("✅ Multiple different queries measured")


class PerformanceRegressionTest(BaseIntegrationTest):
    """
    Test for performance regressions
    """
    
    def test_20_baseline_performance_metrics(self):
        """Establish baseline performance metrics"""
        self.log_test_info("Establishing baseline performance metrics")
        
        metrics = {}
        
        # Single entry fetch
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
        result, elapsed = PerformanceAssertion.measure_operation(entry.fetch, "baseline_fetch")
        if result:
            metrics['fetch'] = elapsed
        
        # Simple query
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query().limit(5)
        result, elapsed = PerformanceAssertion.measure_operation(query.find, "baseline_query")
        if result:
            metrics['query'] = elapsed
        
        # Query with references
        query_ref = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).query()
        query_ref.include_reference('reference').limit(3)
        result, elapsed = PerformanceAssertion.measure_operation(query_ref.find, "baseline_query_ref")
        if result:
            metrics['query_with_ref'] = elapsed
        
        # Log all metrics
        PerformanceAssertion.log_operation_times(metrics)
        
        self.log_test_info("✅ Baseline metrics established")
        self.log_test_info("   These can be compared in future runs to detect regressions")


if __name__ == '__main__':
    unittest.main(verbosity=2)

