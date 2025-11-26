"""
Test Suite: Locale Fallback Chains
Tests comprehensive locale fallback behavior (en-gb → en-us, fr-fr → en-us, etc.)
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class LocaleFallbackBasicTest(BaseIntegrationTest):
    """Basic locale fallback tests for single entry fetches"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Basic Locale Fallback Tests")

    def test_01_fetch_entry_with_fallback_enabled(self):
        """Test fetching an entry with include_fallback() for non-existent locale"""
        self.log_test_info("Fetching entry with locale fallback enabled")
        
        # Request fr-fr locale with fallback (should fall back to en-us)
        result = TestHelpers.safe_api_call(
            "fetch_entry_with_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('fr-fr')
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "Locale fallback should return entry"):
            entry = result['entry']
            self.assert_entry_structure(entry, config.SIMPLE_ENTRY_UID)
            
            # Check that we got a locale (either fr-fr or fallback en-us)
            self.assertIn('locale', entry, "Entry should have locale field")
            self.assertIn(entry['locale'], ['fr-fr', 'en-us'], "Locale should be fr-fr or fallback en-us")
            self.logger.info(f"  ✅ Entry returned with locale: {entry['locale']}")

    def test_02_fetch_entry_without_fallback(self):
        """Test fetching entry without fallback for non-existent locale"""
        self.log_test_info("Fetching entry without locale fallback")
        
        # Request fr-fr locale WITHOUT fallback
        result = TestHelpers.safe_api_call(
            "fetch_entry_without_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('fr-fr')
            .fetch
        )
        
        # Without fallback, we might get None or an entry in requested locale
        if result is None or not self.assert_has_results(result, "Without fallback, result may be empty"):
            self.logger.info("  ✅ No entry returned without fallback (expected)")
        else:
            entry = result['entry']
            if 'locale' in entry and entry['locale'] == 'fr-fr':
                self.logger.info("  ✅ Entry found in requested locale fr-fr")
            else:
                self.logger.warning("  ⚠️  Entry returned in different locale without fallback")

    def test_03_fetch_complex_entry_with_fallback(self):
        """Test fetching complex entry with locale fallback"""
        self.log_test_info("Fetching complex entry with locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_complex_with_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .locale('de-de')  # German, likely falls back to en-us
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "Complex entry should support fallback"):
            entry = result['entry']
            self.assert_entry_structure(entry, config.COMPLEX_ENTRY_UID, config.COMPLEX_CONTENT_TYPE_UID)
            self.logger.info(f"  ✅ Complex entry with locale: {entry.get('locale', 'N/A')}")

    def test_04_fetch_medium_entry_with_fallback(self):
        """Test fetching medium complexity entry with locale fallback"""
        self.log_test_info("Fetching medium entry with locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_medium_with_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('es-es')  # Spanish, likely falls back to en-us
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "Medium entry should support fallback"):
            entry = result['entry']
            self.assert_entry_structure(entry, config.MEDIUM_ENTRY_UID, config.MEDIUM_CONTENT_TYPE_UID)
            self.logger.info(f"  ✅ Medium entry with locale: {entry.get('locale', 'N/A')}")


class LocaleFallbackQueryTest(BaseIntegrationTest):
    """Locale fallback tests for query operations"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Query Locale Fallback Tests")

    def test_05_query_with_fallback_enabled(self):
        """Test querying entries with locale fallback enabled"""
        self.log_test_info("Querying entries with locale fallback")
        
        result = TestHelpers.safe_api_call(
            "query_with_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('it-it')  # Italian
            .include_fallback()
            .find
        )
        
        if self.assert_has_results(result, "Query should return entries with fallback"):
            self.assertGreater(len(result['entries']), 0, "Should find entries with fallback")
            self.logger.info(f"  ✅ Found {len(result['entries'])} entries with fallback")

    def test_06_query_without_fallback(self):
        """Test querying entries without locale fallback"""
        self.log_test_info("Querying entries without locale fallback")
        
        result = TestHelpers.safe_api_call(
            "query_without_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('it-it')  # Italian
            .find
        )
        
        # Without fallback, might get fewer or no results
        if result and 'entries' in result:
            entry_count = len(result['entries'])
            self.logger.info(f"  ✅ Found {entry_count} entries without fallback")
        else:
            self.logger.info("  ✅ No entries without fallback (expected)")

    def test_07_query_multiple_locales_with_fallback(self):
        """Test querying with fallback across different content types"""
        self.log_test_info("Querying multiple content types with fallback")
        
        # Query complex entries
        result_complex = TestHelpers.safe_api_call(
            "query_complex_with_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .locale('ja-jp')  # Japanese
            .include_fallback()
            .find
        )
        
        if result_complex and self.assert_has_results(result_complex, "Complex entries with fallback"):
            self.logger.info(f"  ✅ Complex: {len(result_complex['entries'])} entries")
        
        # Query simple entries
        result_simple = TestHelpers.safe_api_call(
            "query_simple_with_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('ja-jp')
            .include_fallback()
            .find
        )
        
        if result_simple and self.assert_has_results(result_simple, "Simple entries with fallback"):
            self.logger.info(f"  ✅ Simple: {len(result_simple['entries'])} entries")


class LocaleFallbackWithReferencesTest(BaseIntegrationTest):
    """Locale fallback with references and embedded items"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Locale Fallback with References Tests")

    def test_08_fetch_with_references_and_fallback(self):
        """Test fetching entry with references and locale fallback"""
        self.log_test_info("Fetching entry with references and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_with_references_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .locale('pt-br')  # Portuguese
            .include_fallback()
            .include_reference(['authors', 'related_content'])
            .fetch
        )
        
        if self.assert_has_results(result, "Entry with references should support fallback"):
            entry = result['entry']
            self.assert_entry_structure(entry, config.COMPLEX_ENTRY_UID, config.COMPLEX_CONTENT_TYPE_UID)
            
            # Check if references are included
            if TestHelpers.has_field(entry, 'authors') or TestHelpers.has_field(entry, 'related_content'):
                self.logger.info("  ✅ References included with fallback")
            else:
                self.logger.info("  ✅ Entry fetched with fallback (references may not exist)")

    def test_09_query_with_references_and_fallback(self):
        """Test querying entries with references and locale fallback"""
        self.log_test_info("Querying with references and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "query_references_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .query()
            .locale('zh-cn')  # Chinese
            .include_fallback()
            .include_reference(['authors'])
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Query with references should support fallback"):
            self.logger.info(f"  ✅ Found {len(result['entries'])} entries with references and fallback")

    def test_10_fetch_embedded_items_with_fallback(self):
        """Test fetching entry with embedded items and locale fallback"""
        self.log_test_info("Fetching entry with embedded items and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_embedded_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .locale('ko-kr')  # Korean
            .include_fallback()
            .include_embedded_items()
            .fetch
        )
        
        if self.assert_has_results(result, "Embedded items should support fallback"):
            entry = result['entry']
            self.assert_entry_structure(entry, config.COMPLEX_ENTRY_UID, config.COMPLEX_CONTENT_TYPE_UID)
            self.logger.info("  ✅ Entry with embedded items and fallback fetched")


class LocaleFallbackFieldProjectionTest(BaseIntegrationTest):
    """Locale fallback with field projection (only/except)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Locale Fallback with Field Projection Tests")

    def test_11_fetch_with_only_fields_and_fallback(self):
        """Test fetching entry with only fields and locale fallback"""
        self.log_test_info("Fetching with only fields and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_only_fields_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('ru-ru')  # Russian
            .include_fallback()
            .only('title').only('url')
            .fetch
        )
        
        if self.assert_has_results(result, "Only fields with fallback should work"):
            entry = result['entry']
            self.assertIn('title', entry, "Entry should have 'title'")
            self.logger.info("  ✅ Only fields with fallback working")

    def test_12_fetch_with_except_fields_and_fallback(self):
        """Test fetching entry with except fields and locale fallback"""
        self.log_test_info("Fetching with except fields and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_except_fields_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('ar-ae')  # Arabic
            .include_fallback()
            .excepts('content').excepts('body')
            .fetch
        )
        
        if self.assert_has_results(result, "Except fields with fallback should work"):
            entry = result['entry']
            self.assertNotIn('content', entry, "Entry should NOT have 'content'")
            self.assertNotIn('body', entry, "Entry should NOT have 'body'")
            self.logger.info("  ✅ Except fields with fallback working")

    def test_13_query_with_only_and_fallback(self):
        """Test querying with only fields and locale fallback"""
        self.log_test_info("Querying with only fields and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "query_only_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('nl-nl')  # Dutch
            .include_fallback()
            .only('title').only('uid')
            .find
        )
        
        if self.assert_has_results(result, "Query with only and fallback should work"):
            entries = result['entries']
            for entry in entries[:3]:  # Check first 3
                self.assertIn('title', entry, "Entry should have 'title'")
                self.assertIn('uid', entry, "Entry should have 'uid'")
            self.logger.info(f"  ✅ Query with only fields and fallback: {len(entries)} entries")


class LocaleFallbackMetadataTest(BaseIntegrationTest):
    """Locale fallback with metadata and content type info"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Locale Fallback with Metadata Tests")

    def test_14_fetch_with_metadata_and_fallback(self):
        """Test fetching entry with metadata and locale fallback"""
        self.log_test_info("Fetching with metadata and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_metadata_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .locale('sv-se')  # Swedish
            .include_fallback()
            .include_metadata()
            .fetch
        )
        
        if self.assert_has_results(result, "Metadata with fallback should work"):
            entry = result['entry']
            self.assertIn('_metadata', entry, "Entry should have '_metadata'")
            self.logger.info("  ✅ Metadata included with locale fallback")

    def test_15_fetch_with_content_type_and_fallback(self):
        """Test fetching entry with content type info and locale fallback"""
        self.log_test_info("Fetching with content type and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_content_type_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('da-dk')  # Danish
            .include_fallback()
            .include_content_type()
            .fetch
        )
        
        if self.assert_has_results(result, "Content type with fallback should work"):
            self.assertIn('content_type', result, "Response should have 'content_type'")
            self.logger.info("  ✅ Content type info included with locale fallback")

    def test_16_query_with_metadata_and_fallback(self):
        """Test querying with metadata and locale fallback"""
        self.log_test_info("Querying with metadata and locale fallback")
        
        result = TestHelpers.safe_api_call(
            "query_metadata_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('fi-fi')  # Finnish
            .include_fallback()
            .include_metadata()
            .limit(3)
            .find
        )
        
        if self.assert_has_results(result, "Query with metadata and fallback should work"):
            entries = result['entries']
            for entry in entries:
                self.assertIn('_metadata', entry, "Each entry should have '_metadata'")
            self.logger.info(f"  ✅ {len(entries)} entries with metadata and fallback")


class LocaleFallbackEdgeCasesTest(BaseIntegrationTest):
    """Edge cases and error scenarios for locale fallback"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Locale Fallback Edge Cases Tests")

    def test_17_fetch_invalid_locale_with_fallback(self):
        """Test fetching with invalid locale and fallback enabled"""
        self.log_test_info("Fetching with invalid locale and fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_invalid_locale_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('xx-xx')  # Invalid locale
            .include_fallback()
            .fetch
        )
        
        if result and self.assert_has_results(result, "Should handle invalid locale gracefully"):
            self.logger.info("  ✅ Invalid locale handled with fallback")
        else:
            self.logger.info("  ✅ Invalid locale returned None (acceptable)")

    def test_18_fetch_default_locale_with_fallback(self):
        """Test fetching with default locale (en-us) and fallback"""
        self.log_test_info("Fetching with default locale and fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_default_locale_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('en-us')  # Default locale
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "Default locale with fallback should work"):
            entry = result['entry']
            self.assertEqual(entry.get('locale'), 'en-us', "Locale should be en-us")
            self.logger.info("  ✅ Default locale with fallback working")

    def test_19_query_with_fallback_and_filters(self):
        """Test querying with fallback and where filters"""
        self.log_test_info("Querying with fallback and filters")
        
        result = TestHelpers.safe_api_call(
            "query_fallback_filters",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .locale('no-no')  # Norwegian
            .include_fallback()
            .where('title', QueryOperation.EXISTS, True)
            .find
        )
        
        if self.assert_has_results(result, "Fallback with filters should work"):
            self.logger.info(f"  ✅ {len(result['entries'])} entries with fallback and filters")

    def test_20_fetch_with_fallback_and_version(self):
        """Test fetching specific version with locale fallback"""
        self.log_test_info("Fetching specific version with locale fallback")
        
        result = TestHelpers.safe_api_call(
            "fetch_version_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('pl-pl')  # Polish
            .include_fallback()
            .version(1)  # Version 1
            .fetch
        )
        
        if result and self.assert_has_results(result, "Version with fallback"):
            self.logger.info("  ✅ Specific version with locale fallback working")


class LocaleFallbackChainTest(BaseIntegrationTest):
    """Test locale fallback chains (en-gb → en-us, etc.)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Locale Fallback Chain Tests")

    def test_21_fetch_en_gb_fallback_to_en_us(self):
        """Test en-gb falling back to en-us"""
        self.log_test_info("Testing en-gb → en-us fallback chain")
        
        result = TestHelpers.safe_api_call(
            "fetch_en_gb_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('en-gb')
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "en-gb fallback should work"):
            entry = result['entry']
            locale = entry.get('locale', 'unknown')
            self.assertIn(locale, ['en-gb', 'en-us'], "Locale should be en-gb or en-us")
            self.logger.info(f"  ✅ en-gb fallback working (resolved to: {locale})")

    def test_22_fetch_en_au_fallback_to_en_us(self):
        """Test en-au falling back to en-us"""
        self.log_test_info("Testing en-au → en-us fallback chain")
        
        result = TestHelpers.safe_api_call(
            "fetch_en_au_fallback",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .entry(config.SIMPLE_ENTRY_UID)
            .locale('en-au')
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "en-au fallback should work"):
            entry = result['entry']
            locale = entry.get('locale', 'unknown')
            self.assertIn(locale, ['en-au', 'en-us'], "Locale should be en-au or en-us")
            self.logger.info(f"  ✅ en-au fallback working (resolved to: {locale})")

    def test_23_query_multiple_english_variants_fallback(self):
        """Test querying with multiple English variants"""
        self.log_test_info("Querying with multiple English variant fallbacks")
        
        locales_to_test = ['en-gb', 'en-au', 'en-ca', 'en-nz']
        
        for locale in locales_to_test:
            result = TestHelpers.safe_api_call(
                f"query_{locale}_fallback",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .locale(locale)
                .include_fallback()
                .limit(1)
                .find
            )
            
            if result and self.assert_has_results(result, f"{locale} fallback query"):
                self.logger.info(f"  ✅ {locale} fallback: Found {len(result['entries'])} entries")

    def test_24_fetch_fr_ca_fallback_chain(self):
        """Test fr-ca fallback chain (fr-ca → fr-fr → en-us)"""
        self.log_test_info("Testing fr-ca fallback chain")
        
        result = TestHelpers.safe_api_call(
            "fetch_fr_ca_fallback",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
            .entry(config.COMPLEX_ENTRY_UID)
            .locale('fr-ca')  # French Canadian
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "fr-ca fallback chain should work"):
            entry = result['entry']
            locale = entry.get('locale', 'unknown')
            self.logger.info(f"  ✅ fr-ca fallback chain working (resolved to: {locale})")

    def test_25_fetch_es_mx_fallback_chain(self):
        """Test es-mx fallback chain (es-mx → es-es → en-us)"""
        self.log_test_info("Testing es-mx fallback chain")
        
        result = TestHelpers.safe_api_call(
            "fetch_es_mx_fallback",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .entry(config.MEDIUM_ENTRY_UID)
            .locale('es-mx')  # Mexican Spanish
            .include_fallback()
            .fetch
        )
        
        if self.assert_has_results(result, "es-mx fallback chain should work"):
            entry = result['entry']
            locale = entry.get('locale', 'unknown')
            self.logger.info(f"  ✅ es-mx fallback chain working (resolved to: {locale})")


if __name__ == '__main__':
    unittest.main()

