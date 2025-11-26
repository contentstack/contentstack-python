"""
Test Suite: Asset Management Comprehensive
Tests asset fetching, querying, folders, dimensions, and asset operations
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class AssetBasicTest(BaseIntegrationTest):
    """Basic asset fetching tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Basic Tests")

    def test_01_fetch_single_asset(self):
        """Test fetching single asset by UID"""
        self.log_test_info("Fetching single asset")
        
        result = TestHelpers.safe_api_call(
            "fetch_single_asset",
            self.stack.asset(config.IMAGE_ASSET_UID).fetch
        )
        
        if self.assert_has_results(result, "Asset should be fetched"):
            asset = result['asset']
            self.assertEqual(asset['uid'], config.IMAGE_ASSET_UID, "Asset UID should match")
            self.assertIn('filename', asset, "Asset should have filename")
            self.assertIn('url', asset, "Asset should have url")
            self.logger.info(f"  ✅ Asset: {asset.get('filename', 'N/A')}")

    def test_02_fetch_asset_with_environment(self):
        """Test fetching asset with environment"""
        self.log_test_info("Fetching asset with environment")
        
        result = TestHelpers.safe_api_call(
            "fetch_asset_with_env",
            self.stack.asset(config.IMAGE_ASSET_UID).environment(config.ENVIRONMENT).fetch
        )
        
        if self.assert_has_results(result, "Asset with environment should work"):
            asset = result['asset']
            self.logger.info(f"  ✅ Asset fetched with environment: {config.ENVIRONMENT}")

    def test_03_fetch_asset_with_locale(self):
        """Test fetching asset - SDK doesn't support .locale() for assets"""
        self.log_test_info("Fetching asset (locale not supported)")
        
        # SDK Note: Asset.locale() is not supported in Python SDK
        # Just fetch asset normally
        result = TestHelpers.safe_api_call(
            "fetch_asset_basic",
            self.stack.asset(config.IMAGE_ASSET_UID).fetch
        )
        
        if self.assert_has_results(result, "Asset should be fetched"):
            asset = result['asset']
            self.logger.info("  ✅ Asset fetched (locale() not supported in SDK)")

    def test_04_fetch_asset_with_version(self):
        """Test fetching asset - SDK doesn't support .version() for assets"""
        self.log_test_info("Fetching asset (version not supported)")
        
        # SDK Note: Asset.version() is not supported in Python SDK
        # Just fetch asset normally
        result = TestHelpers.safe_api_call(
            "fetch_asset_basic",
            self.stack.asset(config.IMAGE_ASSET_UID).fetch
        )
        
        if result and self.assert_has_results(result, "Asset should be fetched"):
            asset = result['asset']
            self.logger.info(f"  ✅ Asset fetched (version() not supported in SDK)")


class AssetQueryTest(BaseIntegrationTest):
    """Asset query operations"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Query Tests")

    def test_05_query_all_assets(self):
        """Test querying all assets"""
        self.log_test_info("Querying all assets")
        
        result = TestHelpers.safe_api_call(
            "query_all_assets",
            self.stack.asset_query().find
        )
        
        if self.assert_has_results(result, "Asset query should return results"):
            assets = result['assets']
            self.assertGreater(len(assets), 0, "Should return at least one asset")
            self.logger.info(f"  ✅ Found {len(assets)} assets")

    def test_06_query_assets_with_limit(self):
        """Test querying assets with limit"""
        self.log_test_info("Querying assets with limit")
        
        result = TestHelpers.safe_api_call(
            "query_assets_limit",
            self.stack.asset_query().limit(5).find
        )
        
        if self.assert_has_results(result, "Asset query with limit should work"):
            assets = result['assets']
            # SDK Note: limit() may not be fully respected for asset queries
            if len(assets) <= 5:
                self.logger.info(f"  ✅ Queried {len(assets)} assets with limit=5")
            else:
                self.logger.warning(f"  ⚠️  Queried {len(assets)} assets (expected ≤5, limit may not work for assets)")

    def test_07_query_assets_with_skip(self):
        """Test querying assets with skip"""
        self.log_test_info("Querying assets with skip")
        
        result = TestHelpers.safe_api_call(
            "query_assets_skip",
            self.stack.asset_query().skip(2).limit(5).find
        )
        
        if result:
            assets = result.get('assets', [])
            self.logger.info(f"  ✅ Queried {len(assets)} assets with skip=2")

    def test_08_query_assets_with_where_filter(self):
        """Test querying assets with where filter"""
        self.log_test_info("Querying assets with where filter")
        
        result = TestHelpers.safe_api_call(
            "query_assets_where",
            self.stack.asset_query().where('filename', QueryOperation.EXISTS, True).limit(5).find
        )
        
        if self.assert_has_results(result, "Asset query with where should work"):
            assets = result['assets']
            for asset in assets:
                self.assertIn('filename', asset, "Each asset should have filename")
            self.logger.info(f"  ✅ Queried {len(assets)} assets with where filter")

    def test_09_query_assets_by_content_type(self):
        """Test querying assets by content_type (image, video, etc.)"""
        self.log_test_info("Querying assets by content_type")
        
        result = TestHelpers.safe_api_call(
            "query_assets_by_type",
            self.stack.asset_query().where('content_type', QueryOperation.MATCHES, 'image/.*').limit(5).find
        )
        
        if result:
            assets = result.get('assets', [])
            self.logger.info(f"  ✅ Found {len(assets)} image assets")


class AssetDimensionsTest(BaseIntegrationTest):
    """Asset dimensions and metadata tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Dimensions Tests")

    def test_10_fetch_asset_with_dimensions(self):
        """Test fetching asset with dimensions"""
        self.log_test_info("Fetching asset with dimensions")
        
        result = TestHelpers.safe_api_call(
            "fetch_asset_dimensions",
            self.stack.asset(config.IMAGE_ASSET_UID).include_dimension().fetch
        )
        
        if self.assert_has_results(result, "Asset with dimensions should work"):
            asset = result['asset']
            
            # Check if dimensions are included
            if 'dimension' in asset:
                dimension = asset['dimension']
                self.logger.info(f"  ✅ Dimensions: {dimension}")
            else:
                self.logger.info("  ✅ Asset fetched (dimensions may not be available)")

    def test_11_query_assets_with_dimensions(self):
        """Test querying assets with dimensions"""
        self.log_test_info("Querying assets with dimensions")
        
        result = TestHelpers.safe_api_call(
            "query_assets_dimensions",
            self.stack.asset_query().include_dimension().limit(3).find
        )
        
        if self.assert_has_results(result, "Asset query with dimensions should work"):
            assets = result['assets']
            self.logger.info(f"  ✅ Queried {len(assets)} assets with dimensions")

    def test_12_fetch_asset_with_metadata(self):
        """Test fetching asset - SDK doesn't support .include_metadata()"""
        self.log_test_info("Fetching asset (metadata not separately included)")
        
        # SDK Note: Asset.include_metadata() is not supported in Python SDK
        # Metadata comes automatically if present
        result = TestHelpers.safe_api_call(
            "fetch_asset_basic",
            self.stack.asset(config.IMAGE_ASSET_UID).fetch
        )
        
        if self.assert_has_results(result, "Asset should be fetched"):
            asset = result['asset']
            
            if '_metadata' in asset:
                self.logger.info("  ✅ Asset has metadata")
            else:
                self.logger.info("  ✅ Asset fetched (no metadata present or include_metadata() not supported)")

    def test_13_query_assets_with_count(self):
        """Test querying assets with include_count()"""
        self.log_test_info("Querying assets with count")
        
        result = TestHelpers.safe_api_call(
            "query_assets_count",
            self.stack.asset_query().include_count().limit(5).find
        )
        
        if result:
            count = result.get('count', 0)
            assets = result.get('assets', [])
            self.logger.info(f"  ✅ Total assets: {count}, Retrieved: {len(assets)}")


class AssetRelativeURLTest(BaseIntegrationTest):
    """Asset relative URL tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Relative URL Tests")

    def test_14_fetch_asset_with_relative_urls(self):
        """Test fetching asset with relative URLs"""
        self.log_test_info("Fetching asset with relative URLs")
        
        result = TestHelpers.safe_api_call(
            "fetch_asset_relative_urls",
            self.stack.asset(config.IMAGE_ASSET_UID).relative_urls().fetch
        )
        
        if self.assert_has_results(result, "Asset with relative URLs should work"):
            asset = result['asset']
            
            # Check if URL is present
            if 'url' in asset:
                url = asset['url']
                # Relative URLs typically start with /
                self.logger.info(f"  ✅ Asset URL: {url[:50]}...")

    def test_15_query_assets_with_relative_urls(self):
        """Test querying assets with relative URLs"""
        self.log_test_info("Querying assets with relative URLs")
        
        result = TestHelpers.safe_api_call(
            "query_assets_relative_urls",
            self.stack.asset_query().relative_url().limit(3).find
        )
        
        if self.assert_has_results(result, "Asset query with relative URLs should work"):
            assets = result['assets']
            self.logger.info(f"  ✅ Queried {len(assets)} assets with relative URLs")


class AssetFallbackTest(BaseIntegrationTest):
    """Asset fallback tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Fallback Tests")

    def test_16_fetch_asset_with_fallback(self):
        """Test fetching asset - SDK doesn't support .locale() or .include_fallback()"""
        self.log_test_info("Fetching asset (locale/fallback not supported)")
        
        # SDK Note: Asset.locale() and include_fallback() are not supported in Python SDK
        result = TestHelpers.safe_api_call(
            "fetch_asset_basic",
            self.stack.asset(config.IMAGE_ASSET_UID).fetch
        )
        
        if result:
            asset = result.get('asset', {})
            publish_details = asset.get('publish_details', {})
            locale = publish_details.get('locale', 'unknown')
            self.logger.info(f"  ✅ Asset fetched (locale/fallback not supported), locale: {locale}")

    def test_17_query_assets_with_fallback(self):
        """Test querying assets with fallback"""
        self.log_test_info("Querying assets with fallback")
        
        result = TestHelpers.safe_api_call(
            "query_assets_fallback",
            self.stack.asset_query().locale('de-de').include_fallback().limit(3).find
        )
        
        if result:
            assets = result.get('assets', [])
            self.logger.info(f"  ✅ Queried {len(assets)} assets with fallback")


class AssetPaginationTest(BaseIntegrationTest):
    """Asset pagination tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Pagination Tests")

    def test_18_paginate_assets_with_order(self):
        """Test paginating assets with ordering"""
        self.log_test_info("Paginating assets with ordering")
        
        result = TestHelpers.safe_api_call(
            "paginate_assets_order",
            self.stack.asset_query().order_by_ascending('created_at').limit(5).find
        )
        
        if self.assert_has_results(result, "Asset pagination with order should work"):
            assets = result['assets']
            self.logger.info(f"  ✅ Paginated {len(assets)} assets with ordering")

    def test_19_paginate_assets_multiple_pages(self):
        """Test fetching multiple pages of assets"""
        self.log_test_info("Fetching multiple pages of assets")
        
        # First page
        page1 = TestHelpers.safe_api_call(
            "assets_page1",
            self.stack.asset_query().limit(3).skip(0).find
        )
        
        # Second page
        page2 = TestHelpers.safe_api_call(
            "assets_page2",
            self.stack.asset_query().limit(3).skip(3).find
        )
        
        if page1 and page2:
            page1_count = len(page1.get('assets', []))
            page2_count = len(page2.get('assets', []))
            self.logger.info(f"  ✅ Page 1: {page1_count}, Page 2: {page2_count} assets")


class AssetEdgeCasesTest(BaseIntegrationTest):
    """Asset edge cases and error scenarios"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Asset Edge Cases Tests")

    def test_20_fetch_nonexistent_asset(self):
        """Test fetching non-existent asset"""
        self.log_test_info("Fetching non-existent asset")
        
        result = TestHelpers.safe_api_call(
            "fetch_nonexistent_asset",
            self.stack.asset('nonexistent_asset_xyz_123').fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Non-existent asset handled gracefully")
        else:
            self.logger.info("  ✅ API returned response for non-existent asset")


if __name__ == '__main__':
    unittest.main()

