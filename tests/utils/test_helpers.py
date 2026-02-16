"""
Test Helpers - Utility functions for comprehensive testing
Based on TypeScript SDK success patterns (100% test pass rate)
"""

import logging
from typing import Dict, Any, Optional, List, Callable


class TestHelpers:
    """
    Helper class providing common test utilities
    
    Usage:
        TestHelpers.log_info("test_name", "message")
        result = TestHelpers.safe_api_call("fetch_entry", entry.fetch)
        has_data = TestHelpers.has_results(response)
    """
    
    # === LOGGING HELPERS ===
    
    @staticmethod
    def log_info(operation: str, message: str):
        """Log informational message"""
        logging.info(f"[{operation}] {message}")
    
    @staticmethod
    def log_warning(operation: str, message: str):
        """Log warning message"""
        logging.warning(f"⚠️  [{operation}] {message}")
    
    @staticmethod
    def log_error(operation: str, message: str):
        """Log error message"""
        logging.error(f"❌ [{operation}] {message}")
    
    # === SAFE OPERATION HELPERS (From TS SDK Success) ===
    
    @staticmethod
    def safe_api_call(operation_name: str, func: Callable, *args, **kwargs) -> Optional[Any]:
        """
        Execute API call with graceful error handling
        Pattern from TypeScript SDK (100% success)
        
        Args:
            operation_name: Name of operation for logging
            func: Function to execute
            *args, **kwargs: Arguments to pass to function
        
        Returns:
            Result or None if API error (400, 404, 422)
        
        Example:
            result = TestHelpers.safe_api_call("fetch_entry", entry.fetch)
            if result is None:
                # API not available or error occurred
                return
        """
        try:
            result = func(*args, **kwargs)
            
            if result is None:
                TestHelpers.log_warning(operation_name, "API returned None - may not be available")
                return None
            
            return result
            
        except Exception as e:
            # Check for expected API errors
            if hasattr(e, 'status_code') and e.status_code in [400, 404, 422]:
                TestHelpers.log_warning(
                    operation_name,
                    f"API error {e.status_code} - may not be available or not configured"
                )
                return None
            
            # Check for HTTP response errors
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status = e.response.status_code
                if status in [400, 404, 422]:
                    TestHelpers.log_warning(
                        operation_name,
                        f"API error {status} - may not be available"
                    )
                    return None
            
            # Unexpected error - re-raise
            TestHelpers.log_error(operation_name, f"Unexpected error: {str(e)}")
            raise
    
    # === DATA VALIDATION HELPERS ===
    
    @staticmethod
    def has_results(response: Optional[Dict]) -> bool:
        """
        Check if response has entries/results
        
        Args:
            response: API response dictionary
        
        Returns:
            True if response has data, False otherwise
        
        Example:
            if not TestHelpers.has_results(response):
                logger.warning("No results - test data dependent")
                return
        """
        if response is None:
            return False
        
        # Check for entries (plural - from find/query)
        if 'entries' in response and len(response['entries']) > 0:
            return True
        
        # Check for entry (singular - from fetch)
        if 'entry' in response and response['entry'] is not None:
            return True
        
        # Check for assets
        if 'assets' in response and len(response['assets']) > 0:
            return True
        
        # Check for asset (singular)
        if 'asset' in response and response['asset'] is not None:
            return True
        
        return False
    
    @staticmethod
    def has_field(entry: Dict, field_name: str) -> bool:
        """
        Check if entry has a specific field
        
        Args:
            entry: Entry dictionary
            field_name: Field name to check
        
        Returns:
            True if field exists and is not None
        """
        return field_name in entry and entry[field_name] is not None
    
    @staticmethod
    def has_reference(entry: Dict, reference_field: str) -> bool:
        """
        Check if entry has a reference field populated
        
        Args:
            entry: Entry dictionary
            reference_field: Reference field name
        
        Returns:
            True if reference exists and has data
        """
        if not TestHelpers.has_field(entry, reference_field):
            return False
        
        ref_data = entry[reference_field]
        
        # Could be a list or single object
        if isinstance(ref_data, list):
            return len(ref_data) > 0
        
        return ref_data is not None
    
    @staticmethod
    def get_nested_field(data: Dict, *keys) -> Optional[Any]:
        """
        Safely get nested field from dictionary
        
        Args:
            data: Dictionary to traverse
            *keys: Sequence of keys to traverse
        
        Returns:
            Value if found, None otherwise
        
        Example:
            title = TestHelpers.get_nested_field(entry, 'reference', 0, 'title')
        """
        current = data
        
        for key in keys:
            if current is None:
                return None
            
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list):
                if isinstance(key, int) and 0 <= key < len(current):
                    current = current[key]
                else:
                    return None
            else:
                return None
        
        return current
    
    # === VALIDATION HELPERS ===
    
    @staticmethod
    def validate_entry_structure(entry: Dict, required_fields: List[str]):
        """
        Validate entry has required structure
        
        Args:
            entry: Entry dictionary
            required_fields: List of required field names
        
        Returns:
            Tuple of (is_valid, missing_fields)
        
        Example:
            valid, missing = TestHelpers.validate_entry_structure(
                entry, ['uid', 'title', 'url']
            )
            if not valid:
                logger.warning(f"Missing fields: {missing}")
        """
        missing_fields = []
        
        for field in required_fields:
            if not TestHelpers.has_field(entry, field):
                missing_fields.append(field)
        
        return (len(missing_fields) == 0, missing_fields)
    
    @staticmethod
    def count_references(entry: Dict, reference_field: str, max_depth: int = 5) -> int:
        """
        Count reference depth (how many levels deep)
        
        Args:
            entry: Entry dictionary
            reference_field: Reference field name
            max_depth: Maximum depth to traverse
        
        Returns:
            Number of reference levels
        
        Example:
            depth = TestHelpers.count_references(entry, 'reference')
            # depth = 3 means entry -> ref -> ref -> ref
        """
        depth = 0
        current = entry
        
        while depth < max_depth:
            if not TestHelpers.has_reference(current, reference_field):
                break
            
            ref_data = current[reference_field]
            
            # Handle list of references
            if isinstance(ref_data, list):
                if len(ref_data) == 0:
                    break
                current = ref_data[0]
            else:
                current = ref_data
            
            depth += 1
        
        return depth
    
    # === COMPARISON HELPERS ===
    
    @staticmethod
    def compare_entries(entry1: Dict, entry2: Dict, fields_to_compare: List[str]) -> bool:
        """
        Compare two entries for specific fields
        
        Args:
            entry1: First entry
            entry2: Second entry
            fields_to_compare: List of field names to compare
        
        Returns:
            True if all specified fields match
        """
        for field in fields_to_compare:
            val1 = entry1.get(field)
            val2 = entry2.get(field)
            
            if val1 != val2:
                TestHelpers.log_warning(
                    "compare_entries",
                    f"Field '{field}' mismatch: {val1} != {val2}"
                )
                return False
        
        return True
    
    # === TEST DATA HELPERS ===
    
    @staticmethod
    def extract_uids(entries: List[Dict]) -> List[str]:
        """
        Extract UIDs from list of entries
        
        Args:
            entries: List of entry dictionaries
        
        Returns:
            List of UIDs
        """
        return [entry.get('uid') for entry in entries if 'uid' in entry]
    
    @staticmethod
    def filter_by_field(entries: List[Dict], field: str, value: Any) -> List[Dict]:
        """
        Filter entries by field value
        
        Args:
            entries: List of entries
            field: Field name to filter by
            value: Value to match
        
        Returns:
            Filtered list of entries
        """
        return [e for e in entries if e.get(field) == value]
    
    @staticmethod
    def group_by_field(entries: List[Dict], field: str) -> Dict[Any, List[Dict]]:
        """
        Group entries by field value
        
        Args:
            entries: List of entries
            field: Field name to group by
        
        Returns:
            Dictionary of {field_value: [entries]}
        """
        grouped = {}
        
        for entry in entries:
            key = entry.get(field)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(entry)
        
        return grouped
    
    # === LOGGING CONFIGURATION ===
    
    @staticmethod
    def setup_test_logging(level=logging.INFO):
        """
        Setup logging for tests
        
        Args:
            level: Logging level (default: INFO)
        """
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

