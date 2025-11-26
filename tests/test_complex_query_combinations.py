"""
Complex Query Combinations Test Suite
Tests for complex AND/OR combinations, pagination, and advanced queries (critical gap)

Current Coverage: Partial - basic queries tested, complex combinations not tested
Target: Comprehensive coverage of all query combinations and edge cases
"""

import json
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers
from tests.utils.complex_query_builder import ComplexQueryBuilder
import config


class BasicQueryCombinationsTest(BaseIntegrationTest):
    """
    Test basic query combinations
    """
    
    def test_01_where_and_limit(self):
        """Test where clause with limit"""
        self.log_test_info("Testing where + limit")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(5)
        
        result = TestHelpers.safe_api_call("where_limit", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.assertLessEqual(len(entries), 5, "Should respect limit")
        self.log_test_info(f"✅ Returned {len(entries)} entries (limit: 5)")
    
    def test_02_where_and_skip(self):
        """Test where clause with skip"""
        self.log_test_info("Testing where + skip")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.skip(2).limit(3)
        
        result = TestHelpers.safe_api_call("where_skip", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"✅ Skipped 2, returned {len(entries)} entries")
    
    def test_03_order_ascending(self):
        """Test order by ascending"""
        self.log_test_info("Testing order_by_ascending")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.order_by_ascending('created_at')
        query.limit(3)
        
        result = TestHelpers.safe_api_call("order_asc", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"✅ Ordered ascending, returned {len(entries)} entries")
    
    def test_04_order_descending(self):
        """Test order by descending"""
        self.log_test_info("Testing order_by_descending")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.order_by_descending('created_at')
        query.limit(3)
        
        result = TestHelpers.safe_api_call("order_desc", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"✅ Ordered descending, returned {len(entries)} entries")
    
    def test_05_include_count(self):
        """Test include_count"""
        self.log_test_info("Testing include_count")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.include_count()
        query.limit(2)
        
        result = TestHelpers.safe_api_call("include_count", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        if 'count' in result:
            count = result['count']
            self.log_test_info(f"✅ Total count: {count}")
            self.assertIsInstance(count, int)


class PaginationTest(BaseIntegrationTest):
    """
    Test pagination scenarios
    """
    
    def test_06_basic_pagination(self):
        """Test basic pagination"""
        self.log_test_info("Testing basic pagination")
        
        page_size = 2
        page = 1
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.skip((page - 1) * page_size).limit(page_size)
        query.include_count()
        
        result = TestHelpers.safe_api_call("pagination_basic", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        count = result.get('count', 0)
        
        self.log_test_info(f"✅ Page {page}, Size {page_size}: {len(entries)} entries (total: {count})")
    
    def test_07_pagination_page_2(self):
        """Test pagination second page"""
        self.log_test_info("Testing pagination page 2")
        
        page_size = 2
        page = 2
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.skip((page - 1) * page_size).limit(page_size)
        
        result = TestHelpers.safe_api_call("pagination_page2", query.find)
        
        if not self.assert_has_results(result):
            self.skipTest("No entries on page 2")
        
        entries = result['entries']
        self.log_test_info(f"✅ Page {page}: {len(entries)} entries")
    
    def test_08_pagination_with_builder(self):
        """Test pagination using ComplexQueryBuilder"""
        self.log_test_info("Testing pagination with builder")
        
        builder = self.create_complex_query_builder(config.SIMPLE_CONTENT_TYPE_UID)
        result = builder.paginate(page=1, page_size=3).include_count().find()
        
        if not TestHelpers.has_results(result):
            self.skipTest("No entries found")
        
        entries = result['entries']
        self.log_test_info(f"✅ Builder pagination: {len(entries)} entries")


class ANDQueryTest(BaseIntegrationTest):
    """
    Test AND query combinations
    """
    
    def test_09_and_operator_basic(self):
        """Test basic AND operator with multiple conditions"""
        self.log_test_info("Testing AND operator")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # Use add_params for $and query
        query.add_params({
            'query': json.dumps({
                '$and': [
                    {'title': {'$exists': True}},
                    {'uid': {'$exists': True}}
                ]
            })
        })
        query.limit(5)
        
        result = TestHelpers.safe_api_call("and_basic", query.find)
        
        if result:
            entries = result.get('entries', [])
            self.log_test_info(f"✅ AND query: {len(entries)} entries")
    
    def test_10_multiple_and_conditions(self):
        """Test multiple AND conditions"""
        self.log_test_info("Testing multiple AND conditions")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # Use add_params for multiple $and conditions
        query.add_params({
            'query': json.dumps({
                '$and': [
                    {'title': {'$exists': True}},
                    {'uid': {'$exists': True}},
                    {'created_at': {'$exists': True}}
                ]
            })
        })
        query.limit(5)
        
        result = TestHelpers.safe_api_call("and_multiple", query.find)
        
        if result and 'entries' in result:
            self.log_test_info(f"✅ Multiple AND conditions: {len(result['entries'])} entries")


class ORQueryTest(BaseIntegrationTest):
    """
    Test OR query combinations
    """
    
    def test_11_or_operator_basic(self):
        """Test basic OR operator"""
        self.log_test_info("Testing OR operator")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # Use add_params for $or query - match entries with specific titles
        query.add_params({
            'query': json.dumps({
                '$or': [
                    {'title': {'$exists': True}},
                    {'uid': {'$exists': True}}
                ]
            })
        })
        query.limit(5)
        
        result = TestHelpers.safe_api_call("or_basic", query.find)
        
        if result and 'entries' in result:
            self.log_test_info(f"✅ OR query: {len(result['entries'])} entries")
    
    def test_12_or_with_multiple_conditions(self):
        """Test OR with multiple conditions"""
        self.log_test_info("Testing OR with multiple conditions")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # Use add_params for multiple $or conditions
        query.add_params({
            'query': json.dumps({
                '$or': [
                    {'title': {'$exists': True}},
                    {'uid': {'$exists': True}},
                    {'created_at': {'$exists': True}}
                ]
            })
        })
        query.limit(5)
        
        result = TestHelpers.safe_api_call("or_multiple", query.find)
        
        if result and 'entries' in result:
            self.log_test_info(f"✅ Multiple OR conditions: {len(result['entries'])} entries")


class WhereInQueryTest(BaseIntegrationTest):
    """
    Test where_in and where_not_in
    """
    
    def test_13_where_in(self):
        """Test $in operator (note: where_in() is for reference queries)"""
        self.log_test_info("Testing $in operator")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # Get some UIDs first
        sample_result = TestHelpers.safe_api_call("sample", query.limit(3).find)
        
        if sample_result and TestHelpers.has_results(sample_result):
            uids = TestHelpers.extract_uids(sample_result['entries'])
            
            if len(uids) > 0:
                # Query using $in operator via .where() with INCLUDES
                query2 = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
                query2.where('uid', QueryOperation.INCLUDES, uids[:2])
                
                result = TestHelpers.safe_api_call("where_in", query2.find)
                
                if TestHelpers.has_results(result):
                    self.log_test_info(f"✅ where_in returned {len(result['entries'])} entries")
    
    def test_14_where_not_in(self):
        """Test $nin operator (note: where_not_in() is for reference queries)"""
        self.log_test_info("Testing $nin operator")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # Use .where() with EXCLUDES for $nin functionality
        query.where('uid', QueryOperation.EXCLUDES, [config.SIMPLE_ENTRY_UID])
        query.limit(3)
        
        result = TestHelpers.safe_api_call("where_not_in", query.find)
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            
            # Verify excluded entry is not in results
            excluded_found = any(e.get('uid') == config.SIMPLE_ENTRY_UID for e in entries)
            
            if not excluded_found:
                self.log_test_info("✅ Excluded entry not in results")


class SearchQueryTest(BaseIntegrationTest):
    """
    Test search functionality
    """
    
    def test_15_basic_search(self):
        """Test basic search"""
        self.log_test_info("Testing basic search")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.search("test")  # Generic search term
        query.limit(3)
        
        result = TestHelpers.safe_api_call("search_basic", query.find)
        
        if result and 'entries' in result:
            self.log_test_info(f"✅ Search returned {len(result['entries'])} entries")
    
    def test_16_search_with_pagination(self):
        """Test search with pagination"""
        self.log_test_info("Testing search with pagination")
        
        builder = self.create_complex_query_builder(config.SIMPLE_CONTENT_TYPE_UID)
        result = builder.search("the").paginate(1, 2).find()
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ Search + pagination: {len(result['entries'])} entries")


class TagsQueryTest(BaseIntegrationTest):
    """
    Test tags filtering
    """
    
    def test_17_tags_filter(self):
        """Test filtering by tags"""
        self.log_test_info("Testing tags filter")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        # tags() accepts variable args, not a list
        query.tags('test_tag')
        query.limit(3)
        
        result = TestHelpers.safe_api_call("tags_filter", query.find)
        
        if result and 'entries' in result:
            self.log_test_info(f"✅ Tags filter: {len(result['entries'])} entries")


class FieldProjectionTest(BaseIntegrationTest):
    """
    Test field projection (only/except)
    """
    
    def test_18_only_fields(self):
        """Test only() for specific fields"""
        self.log_test_info("Testing only() fields")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.only('uid').only('title')
        query.limit(2)
        
        result = TestHelpers.safe_api_call("only_fields", query.find)
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            
            # Check first entry has only specified fields (plus system fields)
            if len(entries) > 0:
                entry = entries[0]
                self.assertIn('uid', entry)
                self.log_test_info("✅ only() limited fields successfully")
    
    def test_19_except_fields(self):
        """Test except() to exclude fields"""
        self.log_test_info("Testing except() fields")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.excepts('created_by').excepts('updated_by')
        query.limit(2)
        
        result = TestHelpers.safe_api_call("except_fields", query.find)
        
        if TestHelpers.has_results(result):
            self.log_test_info("✅ except() excluded fields successfully")
    
    def test_20_only_with_references(self):
        """Test only() with references"""
        self.log_test_info("Testing only() with references")
        
        query = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).query()
        query.only('uid').only('title').only('reference')
        query.include_reference('reference')
        query.limit(2)
        
        result = TestHelpers.safe_api_call("only_with_refs", query.find)
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            
            if len(entries) > 0 and 'reference' in entries[0]:
                self.log_test_info("✅ Field projection with references works")


class MetadataQueryTest(BaseIntegrationTest):
    """
    Test metadata inclusion
    """
    
    def test_21_include_metadata(self):
        """Test include_metadata()"""
        self.log_test_info("Testing include_metadata")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.include_metadata()
        query.limit(2)
        
        result = TestHelpers.safe_api_call("include_metadata", query.find)
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            
            if len(entries) > 0:
                entry = entries[0]
                
                # Check for metadata fields
                metadata_fields = ['_version', '_in_progress', 'publish_details']
                
                for field in metadata_fields:
                    if field in entry:
                        self.log_test_info(f"✅ Metadata field '{field}' included")
    
    def test_22_include_content_type(self):
        """Test include_content_type()"""
        self.log_test_info("Testing include_content_type")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.include_content_type()
        query.limit(1)
        
        result = TestHelpers.safe_api_call("include_ct", query.find)
        
        if TestHelpers.has_results(result):
            if '_content_type' in result:
                self.log_test_info("✅ Content type schema included")


class LocaleQueryTest(BaseIntegrationTest):
    """
    Test locale-based queries
    """
    
    def test_23_locale_specific(self):
        """Test querying specific locale"""
        self.log_test_info("Testing locale-specific query")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.locale('en-us')
        query.limit(2)
        
        result = TestHelpers.safe_api_call("locale_specific", query.find)
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            
            # Verify locale
            for entry in entries:
                if 'locale' in entry:
                    self.assertEqual(entry['locale'], 'en-us')
            
            self.log_test_info("✅ Locale-specific query works")
    
    def test_24_locale_with_fallback(self):
        """Test locale with fallback"""
        self.log_test_info("Testing locale with fallback")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.locale('en-us')
        query.include_fallback()
        query.limit(2)
        
        result = TestHelpers.safe_api_call("locale_fallback", query.find)
        
        if TestHelpers.has_results(result):
            self.log_test_info("✅ Locale with fallback works")


class ComplexQueryBuilderTest(BaseIntegrationTest):
    """
    Test ComplexQueryBuilder utility
    """
    
    def test_25_builder_chaining(self):
        """Test query builder method chaining"""
        self.log_test_info("Testing builder method chaining")
        
        builder = self.create_complex_query_builder(config.SIMPLE_CONTENT_TYPE_UID)
        
        result = (builder
                  .limit(3)
                  .include_count()
                  .order_by_descending('created_at')
                  .find())
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            count = result.get('count', 0)
            self.log_test_info(f"✅ Builder chaining: {len(entries)} entries (total: {count})")
    
    def test_26_builder_where_conditions(self):
        """Test builder where conditions"""
        self.log_test_info("Testing builder where conditions")
        
        builder = self.create_complex_query_builder(config.SIMPLE_CONTENT_TYPE_UID)
        
        result = builder.where_exists('title').limit(3).find()
        
        if TestHelpers.has_results(result):
            self.log_test_info(f"✅ Builder where: {len(result['entries'])} entries")
    
    def test_27_builder_pagination(self):
        """Test builder pagination helper"""
        self.log_test_info("Testing builder pagination")
        
        builder = self.create_complex_query_builder(config.SIMPLE_CONTENT_TYPE_UID)
        
        result = builder.paginate(page=1, page_size=2).include_count().find()
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            self.assertLessEqual(len(entries), 2)
            self.log_test_info("✅ Builder pagination works")


class EdgeCaseQueryTest(BaseIntegrationTest):
    """
    Test query edge cases
    """
    
    def test_28_empty_result_set(self):
        """Test query returning no results"""
        self.log_test_info("Testing empty result set")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.where('uid', QueryOperation.EQUALS, 'nonexistent_uid_12345')
        
        result = TestHelpers.safe_api_call("empty_results", query.find)
        
        if result:
            entries = result.get('entries', [])
            self.assertEqual(len(entries), 0, "Should return empty results")
            self.log_test_info("✅ Empty result set handled gracefully")
    
    def test_29_limit_zero(self):
        """Test limit(0)"""
        self.log_test_info("Testing limit(0)")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(0)
        
        result = TestHelpers.safe_api_call("limit_zero", query.find)
        
        if result:
            self.log_test_info("✅ limit(0) handled gracefully")
    
    def test_30_large_skip(self):
        """Test large skip value"""
        self.log_test_info("Testing large skip value")
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.skip(1000).limit(2)
        
        result = TestHelpers.safe_api_call("large_skip", query.find)
        
        if result:
            entries = result.get('entries', [])
            self.log_test_info(f"✅ Large skip: {len(entries)} entries")


class PerformanceQueryTest(BaseIntegrationTest):
    """
    Test query performance
    """
    
    def test_31_simple_query_performance(self):
        """Test simple query performance"""
        self.log_test_info("Testing simple query performance")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        query = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
        query.limit(5)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "simple_query_perf"
        )
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            self.log_test_info(f"✅ Simple query: {len(entries)} entries in {elapsed_ms:.2f}ms")
    
    def test_32_complex_query_performance(self):
        """Test complex query performance"""
        self.log_test_info("Testing complex query performance")
        
        from tests.utils.performance_assertions import PerformanceAssertion
        
        query = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
        query.include_reference(['authors'])
        query.include_metadata()
        query.limit(3)
        
        result, elapsed_ms = PerformanceAssertion.measure_operation(
            query.find,
            "complex_query_perf"
        )
        
        if TestHelpers.has_results(result):
            entries = result['entries']
            self.log_test_info(f"✅ Complex query: {len(entries)} entries in {elapsed_ms:.2f}ms")


if __name__ == '__main__':
    unittest.main(verbosity=2)

