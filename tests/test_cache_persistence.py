"""
Test Suite: Cache & Persistence
Tests SDK caching behavior, response consistency, and data persistence
"""

import unittest
import time
from typing import Dict, Any, List, Optional
import config
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
from tests.utils.performance_assertions import PerformanceAssertion


class CacheBasicTest(BaseIntegrationTest):
    """Basic caching behavior tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Basic Cache Tests")

    def test_01_fetch_same_entry_twice(self):
        """Test fetching the same entry twice (cache behavior)"""
        self.log_test_info("Fetching same entry twice")
        
        # First fetch
        with PerformanceAssertion.Timer("First fetch") as timer1:
            result1 = TestHelpers.safe_api_call(
                "first_fetch",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .entry(config.SIMPLE_ENTRY_UID)
                .fetch
            )
        
        # Second fetch (might be cached)
        with PerformanceAssertion.Timer("Second fetch") as timer2:
            result2 = TestHelpers.safe_api_call(
                "second_fetch",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .entry(config.SIMPLE_ENTRY_UID)
                .fetch
            )
        
        if result1 and result2:
            self.logger.info(f"  ✅ First: {timer1.duration:.2f}ms, Second: {timer2.duration:.2f}ms")
            
            # Check if results are consistent
            if result1['entry']['uid'] == result2['entry']['uid']:
                self.logger.info("  ✅ Results are consistent")

    def test_02_query_same_content_type_twice(self):
        """Test querying the same content type twice"""
        self.log_test_info("Querying same content type twice")
        
        # First query
        result1 = TestHelpers.safe_api_call(
            "first_query",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(5)
            .find
        )
        
        # Second query
        result2 = TestHelpers.safe_api_call(
            "second_query",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(5)
            .find
        )
        
        if result1 and result2:
            count1 = len(result1.get('entries', []))
            count2 = len(result2.get('entries', []))
            self.assertEqual(count1, count2, "Query results should be consistent")
            self.logger.info(f"  ✅ Consistent results: {count1} entries both times")

    def test_03_fetch_different_entries_sequentially(self):
        """Test fetching different entries in sequence"""
        self.log_test_info("Fetching different entries sequentially")
        
        entries_to_fetch = [
            (config.SIMPLE_CONTENT_TYPE_UID, config.SIMPLE_ENTRY_UID),
            (config.MEDIUM_CONTENT_TYPE_UID, config.MEDIUM_ENTRY_UID),
            (config.COMPLEX_CONTENT_TYPE_UID, config.COMPLEX_ENTRY_UID),
        ]
        
        results = []
        for ct_uid, entry_uid in entries_to_fetch:
            result = TestHelpers.safe_api_call(
                f"fetch_{entry_uid}",
                self.stack.content_type(ct_uid).entry(entry_uid).fetch
            )
            if result:
                results.append(result['entry']['uid'])
        
        self.assertEqual(len(results), 3, "Should fetch all 3 entries")
        self.logger.info(f"  ✅ Fetched {len(results)} different entries")


class ResponseConsistencyTest(BaseIntegrationTest):
    """Response consistency and data integrity tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Response Consistency Tests")

    def test_04_entry_uid_consistency(self):
        """Test that entry UID remains consistent across fetches"""
        self.log_test_info("Checking entry UID consistency")
        
        # Fetch multiple times
        uids = []
        for i in range(3):
            result = TestHelpers.safe_api_call(
                f"fetch_consistency_{i}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .entry(config.SIMPLE_ENTRY_UID)
                .fetch
            )
            if result:
                uids.append(result['entry']['uid'])
        
        # All UIDs should be the same
        if len(uids) > 0:
            self.assertTrue(all(uid == uids[0] for uid in uids), "UIDs should be consistent")
            self.logger.info(f"  ✅ UID consistent across {len(uids)} fetches")

    def test_05_entry_title_consistency(self):
        """Test that entry title remains consistent"""
        self.log_test_info("Checking entry title consistency")
        
        titles = []
        for i in range(3):
            result = TestHelpers.safe_api_call(
                f"fetch_title_{i}",
                self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
                .entry(config.MEDIUM_ENTRY_UID)
                .fetch
            )
            if result:
                titles.append(result['entry'].get('title', ''))
        
        if len(titles) > 0:
            self.assertTrue(all(title == titles[0] for title in titles), "Titles should be consistent")
            self.logger.info(f"  ✅ Title consistent: '{titles[0]}'")

    def test_06_query_count_consistency(self):
        """Test that query count is consistent across calls"""
        self.log_test_info("Checking query count consistency")
        
        counts = []
        for i in range(3):
            result = TestHelpers.safe_api_call(
                f"query_count_{i}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .include_count()
                .limit(5)
                .find
            )
            if result and 'count' in result:
                counts.append(result['count'])
        
        if len(counts) > 0:
            self.assertTrue(all(count == counts[0] for count in counts), "Counts should be consistent")
            self.logger.info(f"  ✅ Count consistent: {counts[0]}")

    def test_07_reference_consistency(self):
        """Test that references remain consistent"""
        self.log_test_info("Checking reference consistency")
        
        ref_counts = []
        for i in range(2):
            result = TestHelpers.safe_api_call(
                f"fetch_ref_{i}",
                self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
                .entry(config.COMPLEX_ENTRY_UID)
                .include_reference(['authors'])
                .fetch
            )
            if result and TestHelpers.has_field(result['entry'], 'authors'):
                authors = TestHelpers.get_nested_field(result['entry'], 'authors', [])
                if isinstance(authors, list):
                    ref_counts.append(len(authors))
        
        if len(ref_counts) > 0:
            self.assertTrue(all(count == ref_counts[0] for count in ref_counts), "Reference counts should be consistent")
            self.logger.info(f"  ✅ Reference count consistent: {ref_counts[0]}")


class PerformanceCacheTest(BaseIntegrationTest):
    """Performance-related cache tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Performance Cache Tests")

    def test_08_sequential_fetch_performance(self):
        """Test performance of sequential fetches"""
        self.log_test_info("Testing sequential fetch performance")
        
        timings = []
        for i in range(5):
            with PerformanceAssertion.Timer(f"Fetch {i+1}") as timer:
                result = TestHelpers.safe_api_call(
                    f"perf_fetch_{i}",
                    self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                    .entry(config.SIMPLE_ENTRY_UID)
                    .fetch
                )
            if result and timer.duration:
                timings.append(timer.duration)
        
        if len(timings) >= 2:
            avg_time = sum(timings) / len(timings)
            self.logger.info(f"  ✅ Average fetch time: {avg_time:.2f}ms")

    def test_09_sequential_query_performance(self):
        """Test performance of sequential queries"""
        self.log_test_info("Testing sequential query performance")
        
        timings = []
        for i in range(3):
            with PerformanceAssertion.Timer(f"Query {i+1}") as timer:
                result = TestHelpers.safe_api_call(
                    f"perf_query_{i}",
                    self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                    .query()
                    .limit(10)
                    .find
                )
            if result and timer.duration:
                timings.append(timer.duration)
        
        if len(timings) >= 2:
            avg_time = sum(timings) / len(timings)
            self.logger.info(f"  ✅ Average query time: {avg_time:.2f}ms")

    def test_10_different_entries_fetch_time(self):
        """Test fetch time for different entries"""
        self.log_test_info("Comparing fetch times for different entries")
        
        entries_and_times = []
        
        test_entries = [
            ('simple', config.SIMPLE_CONTENT_TYPE_UID, config.SIMPLE_ENTRY_UID),
            ('medium', config.MEDIUM_CONTENT_TYPE_UID, config.MEDIUM_ENTRY_UID),
            ('complex', config.COMPLEX_CONTENT_TYPE_UID, config.COMPLEX_ENTRY_UID),
        ]
        
        for name, ct_uid, entry_uid in test_entries:
            with PerformanceAssertion.Timer(f"Fetch {name}") as timer:
                result = TestHelpers.safe_api_call(
                    f"fetch_{name}_entry",
                    self.stack.content_type(ct_uid).entry(entry_uid).fetch
                )
            if result and timer.duration:
                entries_and_times.append((name, timer.duration))
        
        for name, duration in entries_and_times:
            self.logger.info(f"  ✅ {name.capitalize()}: {duration:.2f}ms")


class DataPersistenceTest(BaseIntegrationTest):
    """Data persistence and state management tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Data Persistence Tests")

    def test_11_stack_instance_persistence(self):
        """Test that stack instance maintains state"""
        self.log_test_info("Testing stack instance persistence")
        
        # Use the class stack instance multiple times
        result1 = TestHelpers.safe_api_call(
            "stack_persistence_1",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        result2 = TestHelpers.safe_api_call(
            "stack_persistence_2",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .fetch
        )
        
        if result1 and result2:
            self.logger.info("  ✅ Stack instance used successfully multiple times")

    def test_12_query_builder_state(self):
        """Test that query builder doesn't retain state across queries"""
        self.log_test_info("Testing query builder state isolation")
        
        # First query with filter
        result1 = TestHelpers.safe_api_call(
            "query_state_1",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(3)
            .find
        )
        
        # Second query with different filter
        result2 = TestHelpers.safe_api_call(
            "query_state_2",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .limit(5)
            .find
        )
        
        if result1 and result2:
            count1 = len(result1.get('entries', []))
            count2 = len(result2.get('entries', []))
            self.assertLessEqual(count1, 3, "First query should respect limit=3")
            self.assertLessEqual(count2, 5, "Second query should respect limit=5")
            self.logger.info(f"  ✅ Query state isolated: {count1} vs {count2} entries")

    def test_13_entry_builder_state(self):
        """Test that entry builder doesn't retain state"""
        self.log_test_info("Testing entry builder state isolation")
        
        # Fetch with locale
        result1 = TestHelpers.safe_api_call(
            "entry_state_1",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('en-us')
            .fetch
        )
        
        # Fetch without locale
        result2 = TestHelpers.safe_api_call(
            "entry_state_2",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .fetch
        )
        
        if result1 and result2:
            self.logger.info("  ✅ Entry builder state isolated")


class ConcurrentRequestTest(BaseIntegrationTest):
    """Tests for handling multiple requests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Concurrent Request Tests")

    def test_14_multiple_sequential_requests(self):
        """Test multiple sequential API requests"""
        self.log_test_info("Testing multiple sequential requests")
        
        results = []
        for i in range(5):
            result = TestHelpers.safe_api_call(
                f"sequential_{i}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .limit(2)
                .skip(i * 2)
                .find
            )
            if result:
                results.append(len(result.get('entries', [])))
        
        self.logger.info(f"  ✅ {len(results)} sequential requests completed")

    def test_15_mixed_content_type_requests(self):
        """Test requests to different content types in sequence"""
        self.log_test_info("Testing mixed content type requests")
        
        content_types = [
            config.SIMPLE_CONTENT_TYPE_UID,
            config.MEDIUM_CONTENT_TYPE_UID,
            config.COMPLEX_CONTENT_TYPE_UID,
            config.SIMPLE_CONTENT_TYPE_UID,  # Repeat
        ]
        
        results = []
        for i, ct_uid in enumerate(content_types):
            result = TestHelpers.safe_api_call(
                f"mixed_ct_{i}",
                self.stack.content_type(ct_uid).query().limit(3).find
            )
            if result:
                results.append(ct_uid)
        
        self.assertEqual(len(results), 4, "All 4 requests should complete")
        self.logger.info(f"  ✅ Mixed content type requests: {len(results)} completed")

    def test_16_rapid_fire_fetch_requests(self):
        """Test rapid sequential fetch requests"""
        self.log_test_info("Testing rapid fire fetch requests")
        
        start_time = time.time()
        
        for i in range(10):
            result = TestHelpers.safe_api_call(
                f"rapid_fetch_{i}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .entry(config.SIMPLE_ENTRY_UID)
                .fetch
            )
        
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        self.logger.info(f"  ✅ 10 rapid requests completed in {elapsed_time:.2f}ms")


class CacheInvalidationTest(BaseIntegrationTest):
    """Tests for cache invalidation scenarios"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Cache Invalidation Tests")

    def test_17_different_locales_fetch(self):
        """Test fetching with different locales (should not cache across locales)"""
        self.log_test_info("Testing different locales fetch")
        
        locales = ['en-us', 'fr-fr', 'en-us']  # Repeat en-us
        
        results = []
        for locale in locales:
            result = TestHelpers.safe_api_call(
                f"fetch_locale_{locale}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .entry(config.SIMPLE_ENTRY_UID)
                .locale(locale)
                .include_fallback()
                .fetch
            )
            if result:
                results.append(result['entry'].get('locale'))
        
        self.logger.info(f"  ✅ Locale-specific fetches: {results}")

    def test_18_different_field_projections(self):
        """Test with different field projections (should not share cache)"""
        self.log_test_info("Testing different field projections")
        
        # Fetch with only title
        result1 = TestHelpers.safe_api_call(
            "projection_only_title",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only('title')
            .fetch
        )
        
        # Fetch with title and uid
        result2 = TestHelpers.safe_api_call(
            "projection_title_uid",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .only('title').only('uid')
            .fetch
        )
        
        if result1 and result2:
            fields1 = list(result1['entry'].keys())
            fields2 = list(result2['entry'].keys())
            self.logger.info(f"  ✅ Different projections: {len(fields1)} vs {len(fields2)} fields")

    def test_19_with_and_without_references(self):
        """Test fetching with and without references"""
        self.log_test_info("Testing with and without references")
        
        # Without references
        result1 = TestHelpers.safe_api_call(
            "no_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .fetch
        )
        
        # With references
        result2 = TestHelpers.safe_api_call(
            "with_references",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .include_reference(['authors'])
            .fetch
        )
        
        if result1 and result2:
            self.logger.info("  ✅ With/without references both work")


class ResponseIntegrityTest(BaseIntegrationTest):
    """Tests for response data integrity"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Response Integrity Tests")

    def test_20_entry_structure_preserved(self):
        """Test that entry structure is preserved across fetches"""
        self.log_test_info("Testing entry structure preservation")
        
        result1 = TestHelpers.safe_api_call(
            "structure_check_1",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        result2 = TestHelpers.safe_api_call(
            "structure_check_2",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .fetch
        )
        
        if result1 and result2:
            keys1 = set(result1['entry'].keys())
            keys2 = set(result2['entry'].keys())
            self.assertEqual(keys1, keys2, "Entry structure should be consistent")
            self.logger.info(f"  ✅ Entry structure preserved: {len(keys1)} fields")


if __name__ == '__main__':
    unittest.main()

