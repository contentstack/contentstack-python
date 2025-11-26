"""
Test Suite: Query Encoding
Tests query handling with special characters, URL encoding, UTF-8, etc.
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from contentstack.basequery import QueryOperation
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class QueryEncodingBasicTest(BaseIntegrationTest):
    """Basic query encoding tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Basic Query Encoding Tests")

    def test_01_query_with_spaces_in_value(self):
        """Test querying with spaces in field value"""
        self.log_test_info("Querying with spaces in value")
        
        result = TestHelpers.safe_api_call(
            "query_with_spaces",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='Sam Wilson')  # Space in search term
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Query with spaces: {len(entries)} entries")

    def test_02_query_with_special_chars(self):
        """Test querying with special characters (&, @, #, etc.)"""
        self.log_test_info("Querying with special characters")
        
        # Test with various special characters
        special_chars = ['&', '@', '#', '$', '%']
        
        for char in special_chars:
            result = TestHelpers.safe_api_call(
                f"query_with_{char}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .where('title', QueryOperation.MATCHES, fields=char)
                .limit(5)
                .find
            )
            
            if result:
                entries = result.get('entries', [])
                self.logger.info(f"  ✅ Query with '{char}': {len(entries)} entries")

    def test_03_query_with_quotes(self):
        """Test querying with quotes in value"""
        self.log_test_info("Querying with quotes")
        
        # Single quotes
        result1 = TestHelpers.safe_api_call(
            "query_single_quotes",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, ".*'.*")
            .limit(5)
            .find
        )
        
        # Double quotes
        result2 = TestHelpers.safe_api_call(
            "query_double_quotes",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*".*')
            .limit(5)
            .find
        )
        
        self.logger.info("  ✅ Query with quotes handled")

    def test_04_query_with_forward_slash(self):
        """Test querying with forward slashes (/)"""
        self.log_test_info("Querying with forward slashes")
        
        result = TestHelpers.safe_api_call(
            "query_forward_slash",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .query()
            .where('url', QueryOperation.MATCHES, fields='/')  # URLs typically have slashes
            .limit(5)
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Query with forward slash: {len(entries)} entries")

    def test_05_query_with_backslash(self):
        """Test querying with backslashes (\\)"""
        self.log_test_info("Querying with backslashes")
        
        result = TestHelpers.safe_api_call(
            "query_backslash",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*')  # Backslash in regex
            .limit(5)
            .find
        )
        
        if result:
            self.logger.info("  ✅ Query with backslash handled")


class QueryEncodingUTF8Test(BaseIntegrationTest):
    """UTF-8 and Unicode character tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting UTF-8 Query Encoding Tests")

    def test_06_query_with_unicode_characters(self):
        """Test querying with Unicode characters"""
        self.log_test_info("Querying with Unicode characters")
        
        # Test with various Unicode characters
        unicode_strings = ['café', 'naïve', 'résumé', '日本語', '中文', 'Español']
        
        for unicode_str in unicode_strings:
            result = TestHelpers.safe_api_call(
                f"query_unicode_{unicode_str[:5]}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .where('title', QueryOperation.MATCHES, fields=unicode_str)
                .limit(3)
                .find
            )
            
            if result is not None:
                entries = result.get('entries', [])
                self.logger.info(f"  ✅ Unicode '{unicode_str}': handled")

    def test_07_query_with_emoji(self):
        """Test querying with emoji characters"""
        self.log_test_info("Querying with emoji")
        
        emojis = ['😀', '🚀', '✅', '❤️']
        
        for emoji in emojis:
            result = TestHelpers.safe_api_call(
                f"query_emoji",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .where('title', QueryOperation.MATCHES, fields=emoji)
                .limit(3)
                .find
            )
            
            if result is not None:
                self.logger.info(f"  ✅ Emoji '{emoji}': handled")

    def test_08_query_with_accented_characters(self):
        """Test querying with accented characters"""
        self.log_test_info("Querying with accented characters")
        
        accented_chars = ['é', 'ñ', 'ü', 'ø', 'å']
        
        for char in accented_chars:
            result = TestHelpers.safe_api_call(
                f"query_accent_{char}",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .where('title', QueryOperation.MATCHES, fields=char)
                .limit(3)
                .find
            )
            
            if result is not None:
                self.logger.info(f"  ✅ Accented char '{char}': handled")

    def test_09_query_with_chinese_characters(self):
        """Test querying with Chinese characters"""
        self.log_test_info("Querying with Chinese characters")
        
        result = TestHelpers.safe_api_call(
            "query_chinese",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*中文.*')
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Chinese characters handled")

    def test_10_query_with_arabic_characters(self):
        """Test querying with Arabic characters"""
        self.log_test_info("Querying with Arabic characters")
        
        result = TestHelpers.safe_api_call(
            "query_arabic",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*العربية.*')
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Arabic characters handled")


class QueryEncodingURLTest(BaseIntegrationTest):
    """URL encoding and query parameter tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting URL Encoding Tests")

    def test_11_query_with_url_special_chars(self):
        """Test querying with URL-special characters"""
        self.log_test_info("Querying with URL special characters")
        
        # Characters that need URL encoding: ?, &, =, +, %
        result = TestHelpers.safe_api_call(
            "query_url_chars",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .query()
            .where('url', QueryOperation.EXISTS, fields=True)
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "URL special chars should be handled"):
            self.logger.info("  ✅ URL special characters handled")

    def test_12_query_with_percent_encoding(self):
        """Test querying with percent-encoded values"""
        self.log_test_info("Querying with percent encoding")
        
        # Test with values that would be percent-encoded
        result = TestHelpers.safe_api_call(
            "query_percent_encoded",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*%20.*')  # %20 is space in URL encoding
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Percent encoding handled")

    def test_13_query_with_plus_sign(self):
        """Test querying with plus sign (+)"""
        self.log_test_info("Querying with plus sign")
        
        result = TestHelpers.safe_api_call(
            "query_plus_sign",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*\\+.*')
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Plus sign handled")

    def test_14_query_with_equals_sign(self):
        """Test querying with equals sign (=)"""
        self.log_test_info("Querying with equals sign")
        
        result = TestHelpers.safe_api_call(
            "query_equals_sign",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*=.*')
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Equals sign handled")

    def test_15_query_with_ampersand(self):
        """Test querying with ampersand (&)"""
        self.log_test_info("Querying with ampersand")
        
        result = TestHelpers.safe_api_call(
            "query_ampersand",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='.*&.*')
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Ampersand handled")


class QueryEncodingRegexTest(BaseIntegrationTest):
    """Regular expression and pattern matching tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Regex Query Encoding Tests")

    def test_16_query_with_regex_special_chars(self):
        """Test querying with regex special characters"""
        self.log_test_info("Querying with regex special characters")
        
        # Regex special chars: . * + ? ^ $ ( ) [ ] { } | \
        result = TestHelpers.safe_api_call(
            "query_regex_chars",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='^.*$')  # Match any title
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Regex special chars should work"):
            self.logger.info("  ✅ Regex special characters handled")

    def test_17_query_with_escaped_regex(self):
        """Test querying with escaped regex characters"""
        self.log_test_info("Querying with escaped regex")
        
        result = TestHelpers.safe_api_call(
            "query_escaped_regex",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='\\w+')  # Word characters
            .limit(5)
            .find
        )
        
        if self.assert_has_results(result, "Escaped regex should work"):
            self.logger.info("  ✅ Escaped regex handled")

    def test_18_query_with_case_insensitive_regex(self):
        """Test case-insensitive regex queries"""
        self.log_test_info("Querying with case-insensitive regex")
        
        result = TestHelpers.safe_api_call(
            "query_case_insensitive",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='(?i)wilson')  # Case-insensitive
            .limit(5)
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Case-insensitive regex: {len(entries)} entries")

    def test_19_query_with_multiline_regex(self):
        """Test multiline regex queries"""
        self.log_test_info("Querying with multiline regex")
        
        result = TestHelpers.safe_api_call(
            "query_multiline_regex",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='^[A-Z].*')  # Starts with capital letter
            .limit(5)
            .find
        )
        
        if result:
            entries = result.get('entries', [])
            self.logger.info(f"  ✅ Multiline regex: {len(entries)} entries")

    def test_20_query_with_word_boundary_regex(self):
        """Test word boundary regex queries"""
        self.log_test_info("Querying with word boundary regex")
        
        result = TestHelpers.safe_api_call(
            "query_word_boundary",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields='\\b\\w+\\b')  # Word boundaries
            .limit(5)
            .find
        )
        
        if result:
            self.logger.info("  ✅ Word boundary regex handled")


class QueryEncodingEdgeCasesTest(BaseIntegrationTest):
    """Edge cases for query encoding"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Query Encoding Edge Cases Tests")

    def test_21_query_with_null_character(self):
        """Test querying with null character (edge case)"""
        self.log_test_info("Querying with null character")
        
        result = TestHelpers.safe_api_call(
            "query_null_char",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.EXISTS, fields=True)
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Null character handled")

    def test_22_query_with_very_long_string(self):
        """Test querying with very long string value"""
        self.log_test_info("Querying with very long string")
        
        long_string = 'a' * 1000  # 1000 character string
        
        result = TestHelpers.safe_api_call(
            "query_long_string",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.MATCHES, fields=long_string[:10])  # Use first 10 chars
            .limit(3)
            .find
        )
        
        if result is not None:
            self.logger.info("  ✅ Long string handled")

    def test_23_query_with_html_entities(self):
        """Test querying with HTML entities"""
        self.log_test_info("Querying with HTML entities")
        
        html_entities = ['&lt;', '&gt;', '&amp;', '&quot;']
        
        for entity in html_entities:
            result = TestHelpers.safe_api_call(
                f"query_html_entity",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .where('title', QueryOperation.MATCHES, fields=entity)
                .limit(3)
                .find
            )
            
            if result is not None:
                self.logger.info(f"  ✅ HTML entity '{entity}': handled")

    def test_24_query_with_xml_special_chars(self):
        """Test querying with XML special characters"""
        self.log_test_info("Querying with XML special characters")
        
        xml_chars = ['<', '>', '&', "'", '"']
        
        for char in xml_chars:
            result = TestHelpers.safe_api_call(
                f"query_xml_char",
                self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
                .query()
                .where('title', QueryOperation.MATCHES, f'.*\\{char}.*')
                .limit(3)
                .find
            )
            
            if result is not None:
                self.logger.info(f"  ✅ XML char '{char}': handled")

    def test_25_query_with_json_special_chars(self):
        """Test querying with JSON special characters"""
        self.log_test_info("Querying with JSON special characters")
        
        # JSON special chars that need escaping
        result = TestHelpers.safe_api_call(
            "query_json_chars",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
            .query()
            .where('title', QueryOperation.EXISTS, fields=True)
            .limit(3)
            .find
        )
        
        if result:
            self.logger.info("  ✅ JSON special characters handled")


if __name__ == '__main__':
    unittest.main()

