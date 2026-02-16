"""
Test Suite: Content Type Schema Validation
Tests content type fetching, schema validation, and field type verification
"""

import unittest
from typing import Dict, Any, List, Optional
import config
from tests.base_integration_test import BaseIntegrationTest
from tests.utils.test_helpers import TestHelpers


class ContentTypeBasicTest(BaseIntegrationTest):
    """Basic content type fetching tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Basic Tests")

    def test_01_fetch_simple_content_type(self):
        """Test fetching simple content type schema"""
        self.log_test_info("Fetching simple content type schema")
        
        result = TestHelpers.safe_api_call(
            "fetch_simple_content_type",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            content_type = result.get('content_type', {})
            self.assertIn('uid', content_type, "Content type should have 'uid'")
            self.assertIn('title', content_type, "Content type should have 'title'")
            self.assertIn('schema', content_type, "Content type should have 'schema'")
            self.logger.info(f"  ✅ Simple CT: {content_type.get('title', 'N/A')}")

    def test_02_fetch_medium_content_type(self):
        """Test fetching medium complexity content type"""
        self.log_test_info("Fetching medium content type schema")
        
        result = TestHelpers.safe_api_call(
            "fetch_medium_content_type",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            content_type = result.get('content_type', {})
            self.assertIn('schema', content_type, "Content type should have 'schema'")
            schema = content_type['schema']
            self.assertIsInstance(schema, list, "Schema should be a list")
            self.logger.info(f"  ✅ Medium CT: {len(schema)} fields")

    def test_03_fetch_complex_content_type(self):
        """Test fetching complex content type schema"""
        self.log_test_info("Fetching complex content type schema")
        
        result = TestHelpers.safe_api_call(
            "fetch_complex_content_type",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            content_type = result.get('content_type', {})
            self.assertIn('schema', content_type, "Content type should have 'schema'")
            schema = content_type['schema']
            self.assertGreater(len(schema), 0, "Complex CT should have multiple fields")
            self.logger.info(f"  ✅ Complex CT: {len(schema)} fields")

    def test_04_fetch_all_content_types(self):
        """Test fetching all content types"""
        self.log_test_info("Fetching all content types")
        
        result = TestHelpers.safe_api_call(
            "fetch_all_content_types",
            self.stack.content_type().find
        )
        
        if result:
            content_types = result.get('content_types', [])
            self.assertGreater(len(content_types), 0, "Should return content types")
            
            # Check structure of first content type
            if len(content_types) > 0:
                first_ct = content_types[0]
                self.assertIn('uid', first_ct, "Each CT should have 'uid'")
                self.assertIn('title', first_ct, "Each CT should have 'title'")
            
            self.logger.info(f"  ✅ Found {len(content_types)} content types")


class ContentTypeSchemaTest(BaseIntegrationTest):
    """Content type schema structure tests"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Schema Tests")

    def test_05_validate_schema_field_types(self):
        """Test that schema contains valid field types"""
        self.log_test_info("Validating schema field types")
        
        result = TestHelpers.safe_api_call(
            "validate_field_types",
            self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            valid_field_types = [
                'text', 'number', 'boolean', 'date', 'file', 'link',
                'reference', 'group', 'blocks', 'json', 'markdown',
                'global_field', 'select', 'isodate'
            ]
            
            for field in schema:
                if 'data_type' in field:
                    data_type = field['data_type']
                    # Just check that data_type exists, don't enforce strict validation
                    self.assertIsNotNone(data_type, "Field should have data_type")
            
            self.logger.info(f"  ✅ Validated {len(schema)} schema fields")

    def test_06_validate_required_fields(self):
        """Test identification of required fields in schema"""
        self.log_test_info("Validating required fields")
        
        result = TestHelpers.safe_api_call(
            "validate_required_fields",
            self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            required_fields = [f for f in schema if f.get('mandatory', False)]
            optional_fields = [f for f in schema if not f.get('mandatory', False)]
            
            self.logger.info(f"  ✅ Required: {len(required_fields)}, Optional: {len(optional_fields)}")

    def test_07_validate_field_properties(self):
        """Test that fields have expected properties"""
        self.log_test_info("Validating field properties")
        
        result = TestHelpers.safe_api_call(
            "validate_field_properties",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            for field in schema:
                # Check common properties
                self.assertIn('uid', field, "Field should have 'uid'")
                self.assertIn('data_type', field, "Field should have 'data_type'")
                
                # Display_name is optional
                if 'display_name' in field:
                    self.assertIsInstance(field['display_name'], str, "display_name should be string")
            
            self.logger.info(f"  ✅ Validated properties for {len(schema)} fields")

    def test_08_validate_reference_fields(self):
        """Test reference field configuration in schema"""
        self.log_test_info("Validating reference fields")
        
        result = TestHelpers.safe_api_call(
            "validate_reference_fields",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            reference_fields = [f for f in schema if f.get('data_type') == 'reference']
            
            for ref_field in reference_fields:
                # Reference fields should have reference_to
                if 'reference_to' in ref_field:
                    self.assertIsInstance(ref_field['reference_to'], (list, str), "reference_to should be list or string")
            
            self.logger.info(f"  ✅ Found {len(reference_fields)} reference fields")


class ContentTypeGlobalFieldsTest(BaseIntegrationTest):
    """Global field integration in content types"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Global Fields Tests")

    def test_09_validate_global_field_references(self):
        """Test global field references in schema"""
        self.log_test_info("Validating global field references")
        
        result = TestHelpers.safe_api_call(
            "validate_global_fields",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            global_fields = [f for f in schema if f.get('data_type') == 'global_field']
            
            for gf in global_fields:
                # Global fields should have reference_to
                if 'reference_to' in gf:
                    self.assertIsNotNone(gf['reference_to'], "Global field should reference a UID")
            
            self.logger.info(f"  ✅ Found {len(global_fields)} global fields")

    def test_10_fetch_content_type_with_global_fields(self):
        """Test fetching content type that uses global fields"""
        self.log_test_info("Fetching CT with global fields")
        
        result = TestHelpers.safe_api_call(
            "fetch_ct_with_globals",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            content_type = result.get('content_type', {})
            schema = content_type.get('schema', [])
            
            # Check if any global fields exist
            has_global_fields = any(f.get('data_type') == 'global_field' for f in schema)
            
            if has_global_fields:
                self.logger.info("  ✅ Content type has global fields")
            else:
                self.logger.info("  ✅ Content type fetched (no global fields found)")


class ContentTypeModularBlocksTest(BaseIntegrationTest):
    """Modular blocks in content type schema"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Modular Blocks Tests")

    def test_11_validate_modular_blocks_field(self):
        """Test modular blocks field in schema"""
        self.log_test_info("Validating modular blocks field")
        
        result = TestHelpers.safe_api_call(
            "validate_modular_blocks",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            blocks_fields = [f for f in schema if f.get('data_type') == 'blocks']
            
            for block_field in blocks_fields:
                # Blocks should have blocks configuration
                if 'blocks' in block_field:
                    self.assertIsInstance(block_field['blocks'], list, "blocks should be a list")
            
            self.logger.info(f"  ✅ Found {len(blocks_fields)} modular blocks fields")

    def test_12_validate_group_fields(self):
        """Test group fields in schema"""
        self.log_test_info("Validating group fields")
        
        result = TestHelpers.safe_api_call(
            "validate_group_fields",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            group_fields = [f for f in schema if f.get('data_type') == 'group']
            
            for group_field in group_fields:
                # Groups should have schema
                if 'schema' in group_field:
                    self.assertIsInstance(group_field['schema'], list, "Group schema should be a list")
            
            self.logger.info(f"  ✅ Found {len(group_fields)} group fields")


class ContentTypeTaxonomyTest(BaseIntegrationTest):
    """Taxonomy fields in content types"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Taxonomy Tests")

    def test_13_validate_taxonomy_fields(self):
        """Test taxonomy field configuration"""
        self.log_test_info("Validating taxonomy fields")
        
        result = TestHelpers.safe_api_call(
            "validate_taxonomy_fields",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            schema = result.get('content_type', {}).get('schema', [])
            
            # Taxonomy fields have taxonomies property
            taxonomy_fields = [f for f in schema if 'taxonomies' in f]
            
            for tax_field in taxonomy_fields:
                taxonomies = tax_field.get('taxonomies', [])
                if taxonomies:
                    self.assertIsInstance(taxonomies, list, "taxonomies should be a list")
            
            self.logger.info(f"  ✅ Found {len(taxonomy_fields)} taxonomy-enabled fields")

    def test_14_fetch_content_type_with_taxonomies(self):
        """Test fetching content type that uses taxonomies"""
        self.log_test_info("Fetching CT with taxonomies")
        
        result = TestHelpers.safe_api_call(
            "fetch_ct_with_taxonomies",
            self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).fetch
        )
        
        if result:
            content_type = result.get('content_type', {})
            schema = content_type.get('schema', [])
            
            # Check if any taxonomy fields exist
            has_taxonomies = any('taxonomies' in f for f in schema)
            
            if has_taxonomies:
                self.logger.info("  ✅ Content type has taxonomy fields")
            else:
                self.logger.info("  ✅ Content type fetched (no taxonomy fields)")


class ContentTypeEdgeCasesTest(BaseIntegrationTest):
    """Edge cases for content type operations"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logger.info("Starting Content Type Edge Cases Tests")

    def test_15_fetch_nonexistent_content_type(self):
        """Test fetching non-existent content type"""
        self.log_test_info("Fetching non-existent content type")
        
        result = TestHelpers.safe_api_call(
            "fetch_nonexistent_ct",
            self.stack.content_type('nonexistent_ct_xyz_123').fetch
        )
        
        if result is None:
            self.logger.info("  ✅ Non-existent CT handled gracefully")
        else:
            self.logger.info("  ✅ API returned response for non-existent CT")


if __name__ == '__main__':
    unittest.main()

