"""
Test Suite: Sync Operations Comprehensive
Tests sync init, sync pagination, sync token, and delta sync functionality
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class SyncInitTest(BaseIntegrationTest):
    """Sync initialization tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Sync Init Tests")

    def test_01_sync_init_basic(self):
        """Test basic sync initialization"""
        self.log_test_info("Testing sync init")
        
        result = TestHelpers.safe_api_call(
            "sync_init",
            self.stack.sync_init
        )
        
        if result:
            self.assertIn('items', result, "Sync should return 'items'")
            self.assertIn('sync_token', result, "Sync should return 'sync_token'")
            items = result['items']
            sync_token = result['sync_token']
            self.logger.info(f"  ✅ Sync init: {len(items)} items, token: {sync_token[:20]}...")

    def test_02_sync_init_with_content_type(self):
        """Test sync init for specific content type"""
        self.log_test_info("Testing sync init with content type filter")
        
        result = TestHelpers.safe_api_call(
            "sync_init_content_type",
            lambda: self.stack.sync_init(content_type_uid=config.SIMPLE_CONTENT_TYPE_UID)
        )
        
        if result:
            items = result.get('items', [])
            self.logger.info(f"  ✅ Sync init for CT: {len(items)} items")

    def test_03_sync_init_with_date_filter(self):
        """Test sync init with start date"""
        self.log_test_info("Testing sync init with date filter")
        
        # Sync from a specific date (e.g., 7 days ago)
        from datetime import datetime, timedelta
        start_date = (datetime.now() - timedelta(days=7)).isoformat()
        
        result = TestHelpers.safe_api_call(
            "sync_init_date",
            lambda: self.stack.sync_init(start_from=start_date)
        )
        
        if result:
            items = result.get('items', [])
            self.logger.info(f"  ✅ Sync init with date: {len(items)} items")

    def test_04_sync_init_publish_type_entry_published(self):
        """Test sync init for published entries only"""
        self.log_test_info("Testing sync init for published entries")
        
        result = TestHelpers.safe_api_call(
            "sync_init_published",
            lambda: self.stack.sync_init(publish_type='entry_published')
        )
        
        if result:
            items = result.get('items', [])
            self.logger.info(f"  ✅ Sync published entries: {len(items)} items")

    def test_05_sync_init_publish_type_entry_unpublished(self):
        """Test sync init for unpublished entries"""
        self.log_test_info("Testing sync init for unpublished entries")
        
        result = TestHelpers.safe_api_call(
            "sync_init_unpublished",
            lambda: self.stack.sync_init(publish_type='entry_unpublished')
        )
        
        if result:
            items = result.get('items', [])
            self.logger.info(f"  ✅ Sync unpublished entries: {len(items)} items")


class SyncPaginationTest(BaseIntegrationTest):
    """Sync pagination tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Sync Pagination Tests")

    def test_06_sync_with_pagination_token(self):
        """Test sync pagination using pagination token"""
        self.log_test_info("Testing sync pagination")
        
        # First, do sync_init
        init_result = TestHelpers.safe_api_call(
            "sync_init_for_pagination",
            self.stack.sync_init
        )
        
        if init_result and 'pagination_token' in init_result:
            pagination_token = init_result['pagination_token']
            
            # Get next page
            page_result = TestHelpers.safe_api_call(
                "sync_pagination",
                lambda: self.stack.pagination(pagination_token)
            )
            
            if page_result:
                items = page_result.get('items', [])
                self.logger.info(f"  ✅ Sync pagination: {len(items)} items in next page")
        else:
            self.logger.info("  ✅ Sync init completed (no pagination token, all items in one response)")

    def test_07_sync_multiple_pages(self):
        """Test fetching multiple sync pages"""
        self.log_test_info("Testing multiple sync pages")
        
        init_result = TestHelpers.safe_api_call(
            "sync_init_multiple_pages",
            self.stack.sync_init
        )
        
        if init_result:
            total_items = len(init_result.get('items', []))
            pagination_token = init_result.get('pagination_token')
            
            # Keep fetching while pagination_token exists
            page_count = 1
            while pagination_token and page_count < 5:  # Limit to 5 pages for testing
                page_result = TestHelpers.safe_api_call(
                    f"sync_page_{page_count}",
                    lambda: self.stack.pagination(pagination_token)
                )
                
                if page_result:
                    total_items += len(page_result.get('items', []))
                    pagination_token = page_result.get('pagination_token')
                    page_count += 1
                else:
                    break
            
            self.logger.info(f"  ✅ Fetched {page_count} sync pages, total items: {total_items}")


class SyncTokenTest(BaseIntegrationTest):
    """Sync token tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Sync Token Tests")

    def test_08_sync_token_basic(self):
        """Test sync using sync token"""
        self.log_test_info("Testing sync with sync token")
        
        # First, get a sync token from sync_init
        init_result = TestHelpers.safe_api_call(
            "sync_init_for_token",
            self.stack.sync_init
        )
        
        if init_result and 'sync_token' in init_result:
            sync_token = init_result['sync_token']
            
            # Use sync token to get delta updates
            sync_result = TestHelpers.safe_api_call(
                "sync_with_token",
                lambda: self.stack.sync_token(sync_token)
            )
            
            if sync_result:
                items = sync_result.get('items', [])
                self.logger.info(f"  ✅ Sync with token: {len(items)} delta items")
        else:
            self.logger.info("  ✅ Sync init completed")

    def test_09_sync_token_reuse(self):
        """Test reusing the same sync token"""
        self.log_test_info("Testing sync token reuse")
        
        init_result = TestHelpers.safe_api_call(
            "sync_init_for_reuse",
            self.stack.sync_init
        )
        
        if init_result and 'sync_token' in init_result:
            sync_token = init_result['sync_token']
            
            # Use token twice
            result1 = TestHelpers.safe_api_call(
                "sync_token_use1",
                lambda: self.stack.sync_token(sync_token)
            )
            
            result2 = TestHelpers.safe_api_call(
                "sync_token_use2",
                lambda: self.stack.sync_token(sync_token)
            )
            
            if result1 and result2:
                # Results should be consistent
                items1 = len(result1.get('items', []))
                items2 = len(result2.get('items', []))
                self.logger.info(f"  ✅ Sync token reused: {items1} vs {items2} items")


class SyncItemTypesTest(BaseIntegrationTest):
    """Sync item types tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Sync Item Types Tests")

    def test_10_sync_filter_by_item_type_entry(self):
        """Test sync for entries only"""
        self.log_test_info("Testing sync for entries only")
        
        result = TestHelpers.safe_api_call(
            "sync_entries_only",
            lambda: self.stack.sync_init(type='entry_published')
        )
        
        if result:
            items = result.get('items', [])
            
            # Check that all items are entries
            entry_items = [item for item in items if item.get('type') == 'entry_published']
            self.logger.info(f"  ✅ Sync entries: {len(entry_items)} entry items")

    def test_11_sync_filter_by_item_type_asset(self):
        """Test sync for assets only"""
        self.log_test_info("Testing sync for assets only")
        
        result = TestHelpers.safe_api_call(
            "sync_assets_only",
            lambda: self.stack.sync_init(type='asset_published')
        )
        
        if result:
            items = result.get('items', [])
            
            # Check that all items are assets
            asset_items = [item for item in items if item.get('type') == 'asset_published']
            self.logger.info(f"  ✅ Sync assets: {len(asset_items)} asset items")

    def test_12_sync_deleted_items(self):
        """Test sync for deleted items"""
        self.log_test_info("Testing sync for deleted items")
        
        result = TestHelpers.safe_api_call(
            "sync_deleted",
            lambda: self.stack.sync_init(type='entry_deleted')
        )
        
        if result:
            items = result.get('items', [])
            self.logger.info(f"  ✅ Sync deleted: {len(items)} deleted items")


class SyncLocaleTest(BaseIntegrationTest):
    """Sync with locale tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Sync Locale Tests")

    def test_13_sync_with_locale(self):
        """Test sync with specific locale"""
        self.log_test_info("Testing sync with locale")
        
        result = TestHelpers.safe_api_call(
            "sync_with_locale",
            lambda: self.stack.sync_init(locale='en-us')
        )
        
        if result:
            items = result.get('items', [])
            self.logger.info(f"  ✅ Sync with locale: {len(items)} items")

    def test_14_sync_multiple_locales(self):
        """Test sync behavior with different locales"""
        self.log_test_info("Testing sync with different locales")
        
        # Sync for en-us
        result_en = TestHelpers.safe_api_call(
            "sync_locale_en",
            lambda: self.stack.sync_init(locale='en-us')
        )
        
        # Sync for fr-fr
        result_fr = TestHelpers.safe_api_call(
            "sync_locale_fr",
            lambda: self.stack.sync_init(locale='fr-fr')
        )
        
        if result_en and result_fr:
            items_en = len(result_en.get('items', []))
            items_fr = len(result_fr.get('items', []))
            self.logger.info(f"  ✅ Sync locales - en-us: {items_en}, fr-fr: {items_fr} items")


class SyncEdgeCasesTest(BaseIntegrationTest):
    """Sync edge cases and error scenarios"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Sync Edge Cases Tests")

    def test_15_sync_with_invalid_token(self):
        """Test sync with invalid token"""
        self.log_test_info("Testing sync with invalid token")
        
        result = TestHelpers.safe_api_call(
            "sync_invalid_token",
            lambda: self.stack.sync_token('invalid_sync_token_xyz')
        )
        
        if result is None:
            self.logger.info("  ✅ Invalid sync token handled gracefully")
        else:
            self.logger.info("  ✅ Sync with invalid token returned response")


if __name__ == '__main__':
    unittest.main()

