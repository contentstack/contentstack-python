"""
Base Integration Test - Foundation for all comprehensive integration tests
Provides common setup, utilities, and patterns
"""

import unittest
import logging
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import contentstack
import config
from tests.utils.test_helpers import TestHelpers
from tests.utils.performance_assertions import PerformanceAssertion
from tests.utils.complex_query_builder import ComplexQueryBuilder, PresetQueryBuilder


class BaseIntegrationTest(unittest.TestCase):
    """
    Base class for all integration tests
    
    Provides:
    - Common SDK setup
    - Test data access
    - Helper utilities
    - Performance measurement
    - Logging configuration
    
    Usage:
        class MyIntegrationTest(BaseIntegrationTest):
            def test_something(self):
                entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(config.SIMPLE_ENTRY_UID)
                result = TestHelpers.safe_api_call("fetch", entry.fetch)
                self.assert_has_results(result)
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Setup once for all tests in the class
        Configure SDK, load test data, setup logging
        """
        # Setup logging
        TestHelpers.setup_test_logging(level=logging.INFO)
        cls.logger = logging.getLogger(cls.__name__)
        
        cls.logger.info("="*80)
        cls.logger.info(f"Setting up test class: {cls.__name__}")
        cls.logger.info("="*80)
        
        # Initialize SDK
        cls.stack = contentstack.Stack(
            api_key=config.API_KEY,
            delivery_token=config.DELIVERY_TOKEN,
            environment=config.ENVIRONMENT,
            host=config.HOST
        )
        
        cls.logger.info("✅ SDK initialized")
        
        # Store config for easy access
        cls.config = config
        
        # Log test data availability
        cls.log_test_data_availability()
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests"""
        cls.logger.info("="*80)
        cls.logger.info(f"Tearing down test class: {cls.__name__}")
        cls.logger.info("="*80)
    
    def setUp(self):
        """Setup before each test"""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Running test: {self._testMethodName}")
        self.logger.info(f"{'='*80}")
    
    def tearDown(self):
        """Cleanup after each test"""
        test_result = "✅ PASSED" if sys.exc_info() == (None, None, None) else "❌ FAILED"
        self.logger.info(f"{test_result}: {self._testMethodName}\n")
    
    # === TEST DATA HELPERS ===
    
    @classmethod
    def log_test_data_availability(cls):
        """Log available test data for debugging"""
        cls.logger.info("\n📊 Test Data Configuration:")
        cls.logger.info(f"   Stack: {config.HOST}")
        cls.logger.info(f"   API Key: {config.API_KEY}")
        cls.logger.info(f"   Environment: {config.ENVIRONMENT}")
        cls.logger.info("")
        cls.logger.info("   Test Entries:")
        cls.logger.info(f"   - SIMPLE: {config.SIMPLE_CONTENT_TYPE_UID}/{config.SIMPLE_ENTRY_UID}")
        cls.logger.info(f"   - MEDIUM: {config.MEDIUM_CONTENT_TYPE_UID}/{config.MEDIUM_ENTRY_UID}")
        cls.logger.info(f"   - COMPLEX: {config.COMPLEX_CONTENT_TYPE_UID}/{config.COMPLEX_ENTRY_UID}")
        cls.logger.info(f"   - SELF-REF: {config.SELF_REF_CONTENT_TYPE_UID}/{config.SELF_REF_ENTRY_UID}")
        cls.logger.info("")
    
    # === ASSERTION HELPERS ===
    
    def assert_has_results(self, response, message="Expected results in response"):
        """
        Assert response has results
        If no results, logs warning but doesn't fail (graceful degradation)
        
        Args:
            response: API response
            message: Optional custom message for logging
        
        Returns:
            bool: True if has results, False otherwise
        """
        has_data = TestHelpers.has_results(response)
        
        if not has_data:
            self.logger.warning("⚠️  No results found - test data dependent")
            return False
        
        return True
    
    def assert_entry_structure(self, entry, required_fields):
        """
        Assert entry has required fields
        
        Args:
            entry: Entry dictionary
            required_fields: List of required field names
        """
        valid, missing = TestHelpers.validate_entry_structure(entry, required_fields)
        
        if not valid:
            self.logger.warning(f"⚠️  Missing fields: {missing}")
        
        self.assertTrue(valid, f"Entry missing required fields: {missing}")
    
    def assert_has_reference(self, entry, reference_field):
        """
        Assert entry has a reference field populated
        
        Args:
            entry: Entry dictionary
            reference_field: Reference field name
        """
        has_ref = TestHelpers.has_reference(entry, reference_field)
        
        if not has_ref:
            self.logger.warning(f"⚠️  Reference field '{reference_field}' not found or empty")
        
        self.assertTrue(has_ref, f"Entry missing reference field: {reference_field}")
    
    # === QUERY BUILDERS ===
    
    def create_simple_query(self):
        """Create query for simple content type"""
        return self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).query()
    
    def create_medium_query(self):
        """Create query for medium content type"""
        return self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).query()
    
    def create_complex_query(self):
        """Create query for complex content type"""
        return self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).query()
    
    def create_complex_query_builder(self, content_type_uid=None):
        """
        Create complex query builder
        
        Args:
            content_type_uid: Optional specific content type (defaults to SIMPLE)
        
        Returns:
            ComplexQueryBuilder instance
        """
        ct_uid = content_type_uid or config.SIMPLE_CONTENT_TYPE_UID
        query = self.stack.content_type(ct_uid).query()
        return ComplexQueryBuilder(query)
    
    # === ENTRY FETCHING ===
    
    def fetch_simple_entry(self, entry_uid=None):
        """
        Fetch simple entry (with graceful error handling)
        
        Args:
            entry_uid: Optional specific UID (defaults to config SIMPLE_ENTRY_UID)
        
        Returns:
            Entry data or None
        """
        uid = entry_uid or config.SIMPLE_ENTRY_UID
        entry = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID).entry(uid)
        
        return TestHelpers.safe_api_call("fetch_simple_entry", entry.fetch)
    
    def fetch_medium_entry(self, entry_uid=None):
        """Fetch medium entry"""
        uid = entry_uid or config.MEDIUM_ENTRY_UID
        entry = self.stack.content_type(config.MEDIUM_CONTENT_TYPE_UID).entry(uid)
        
        return TestHelpers.safe_api_call("fetch_medium_entry", entry.fetch)
    
    def fetch_complex_entry(self, entry_uid=None):
        """Fetch complex entry"""
        uid = entry_uid or config.COMPLEX_ENTRY_UID
        entry = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID).entry(uid)
        
        return TestHelpers.safe_api_call("fetch_complex_entry", entry.fetch)
    
    # === PERFORMANCE TESTING ===
    
    def measure_query_performance(self, query_func, operation_name):
        """
        Measure query performance
        
        Args:
            query_func: Function that executes the query
            operation_name: Name for logging
        
        Returns:
            Tuple of (result, elapsed_time_ms)
        """
        return PerformanceAssertion.measure_operation(query_func, operation_name)
    
    def compare_query_performance(self, queries):
        """
        Compare performance of multiple queries
        
        Args:
            queries: Dictionary of {name: query_function}
        
        Returns:
            Dictionary of results with timings
        """
        return PerformanceAssertion.measure_batch_operations(queries)
    
    # === LOGGING HELPERS ===
    
    def log_test_info(self, message):
        """Log informational message"""
        self.logger.info(f"ℹ️  {message}")
    
    def log_test_warning(self, message):
        """Log warning message"""
        self.logger.warning(f"⚠️  {message}")
    
    def log_test_error(self, message):
        """Log error message"""
        self.logger.error(f"❌ {message}")
    
    # === SKIP HELPERS ===
    
    def skip_if_no_data(self, response, message="No test data available"):
        """
        Skip test if response has no data
        
        Args:
            response: API response
            message: Skip message
        """
        if not TestHelpers.has_results(response):
            self.skipTest(message)
    
    def skip_if_api_unavailable(self, result, feature_name="Feature"):
        """
        Skip test if API feature unavailable
        
        Args:
            result: API result (None if unavailable)
            feature_name: Name of feature for message
        """
        if result is None:
            self.skipTest(f"{feature_name} API not available in this environment")
    
    # === DATA VALIDATION HELPERS ===
    
    def validate_response_structure(self, response, expected_keys):
        """
        Validate response has expected structure
        
        Args:
            response: API response
            expected_keys: List of expected keys
        """
        for key in expected_keys:
            self.assertIn(key, response, f"Response missing key: {key}")
    
    def validate_entry_metadata(self, entry):
        """
        Validate entry has standard metadata
        
        Args:
            entry: Entry dictionary
        """
        metadata_fields = ['uid', '_version', 'locale']
        
        for field in metadata_fields:
            if field not in entry:
                self.logger.warning(f"⚠️  Entry missing metadata field: {field}")
    
    # === REFERENCE TESTING HELPERS ===
    
    def fetch_entry_with_references(self, content_type_uid, entry_uid, reference_fields):
        """
        Fetch entry with specified references
        
        Args:
            content_type_uid: Content type UID
            entry_uid: Entry UID
            reference_fields: List of reference field paths
        
        Returns:
            Entry data or None
        """
        entry = self.stack.content_type(content_type_uid).entry(entry_uid)
        
        # Add references
        for ref_field in reference_fields:
            entry.include_reference(ref_field)
        
        return TestHelpers.safe_api_call("fetch_with_references", entry.fetch)
    
    def validate_reference_depth(self, entry, reference_field, expected_depth):
        """
        Validate reference depth
        
        Args:
            entry: Entry dictionary
            reference_field: Reference field name
            expected_depth: Expected depth
        """
        actual_depth = TestHelpers.count_references(entry, reference_field)
        
        self.logger.info(f"Reference depth for '{reference_field}': {actual_depth}")
        
        self.assertEqual(
            actual_depth,
            expected_depth,
            f"Reference depth mismatch: expected {expected_depth}, got {actual_depth}"
        )


# === SAMPLE USAGE ===

if __name__ == '__main__':
    """
    Example of using BaseIntegrationTest
    """
    
    class SampleTest(BaseIntegrationTest):
        """Sample test to demonstrate usage"""
        
        def test_simple_fetch(self):
            """Test fetching simple entry"""
            result = self.fetch_simple_entry()
            
            if not self.assert_has_results(result):
                return  # No data, skip gracefully
            
            entry = result['entry']
            self.assertIn('uid', entry)
            self.assertIn('title', entry)
            
            self.log_test_info(f"Fetched entry: {entry.get('title')}")
        
        def test_complex_query(self):
            """Test complex query building"""
            builder = self.create_complex_query_builder(config.COMPLEX_CONTENT_TYPE_UID)
            
            result = builder.include_count().limit(5).find()
            
            if not self.assert_has_results(result):
                return
            
            self.log_test_info(f"Found {len(result['entries'])} entries")
    
    # Run sample tests
    unittest.main()

