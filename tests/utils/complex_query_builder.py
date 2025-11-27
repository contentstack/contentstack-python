"""
Complex Query Builder - Utilities for building complex query combinations
Helps test complex AND/OR combinations, nested queries, and edge cases
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from contentstack.basequery import QueryOperation


class QueryOperator(Enum):
    """Query operators"""
    AND = "$and"
    OR = "$or"


class ComplexQueryBuilder:
    """
    Builder for creating complex query combinations
    
    Usage:
        builder = ComplexQueryBuilder(query)
        builder.where("title", "Test")\
               .or_where("url", "/test")\
               .include_reference(["author"])\
               .build()
    """
    
    def __init__(self, query_object):
        """
        Initialize with a query object
        
        Args:
            query_object: SDK Query object
        """
        self.query = query_object
        self.conditions = []
        self.or_conditions = []
    
    # === BASIC QUERY BUILDING ===
    
    def where(self, field: str, value: Any):
        """
        Add where condition
        
        Args:
            field: Field name
            value: Field value
        
        Returns:
            self for chaining
        """
        self.query.where(field, QueryOperation.EQUALS, value)
        return self
    
    def where_not(self, field: str, value: Any):
        """
        Add where not equal condition
        
        Args:
            field: Field name
            value: Field value to exclude
        
        Returns:
            self for chaining
        """
        self.query.where(field, QueryOperation.NOT_EQUALS, value)
        return self
    
    def where_in(self, field: str, values: List[Any]):
        """
        Add where in condition
        
        Args:
            field: Field name
            values: List of values
        
        Returns:
            self for chaining
        """
        self.query.where_in(field, values)
        return self
    
    def where_not_in(self, field: str, values: List[Any]):
        """
        Add where not in condition
        
        Args:
            field: Field name
            values: List of values to exclude
        
        Returns:
            self for chaining
        """
        self.query.where_not_in(field, values)
        return self
    
    # === COMPARISON OPERATORS ===
    
    def where_greater_than(self, field: str, value: Any):
        """Greater than condition"""
        self.query.where(field, QueryOperation.IS_GREATER_THAN, value)
        return self
    
    def where_less_than(self, field: str, value: Any):
        """Less than condition"""
        self.query.where(field, QueryOperation.IS_LESS_THAN, value)
        return self
    
    def where_greater_than_or_equal(self, field: str, value: Any):
        """Greater than or equal condition"""
        self.query.where(field, QueryOperation.IS_GREATER_THAN_OR_EQUAL, value)
        return self
    
    def where_less_than_or_equal(self, field: str, value: Any):
        """Less than or equal condition"""
        self.query.where(field, QueryOperation.IS_LESS_THAN_OR_EQUAL, value)
        return self
    
    def where_between(self, field: str, min_value: Any, max_value: Any):
        """Between condition (inclusive)"""
        # For between, we need two separate where conditions or use add_params
        # Simplified: just use gte for now
        self.query.where(field, QueryOperation.IS_GREATER_THAN_OR_EQUAL, min_value)
        return self
    
    # === PATTERN MATCHING ===
    
    def where_contains(self, field: str, value: str):
        """
        Contains condition (uses regex)
        
        Args:
            field: Field name
            value: Value to search for
        
        Returns:
            self for chaining
        """
        self.query.where(field, QueryOperation.MATCHES, f".*{value}.*")
        return self
    
    def where_starts_with(self, field: str, value: str):
        """Starts with condition"""
        self.query.where(field, QueryOperation.MATCHES, f"^{value}")
        return self
    
    def where_ends_with(self, field: str, value: str):
        """Ends with condition"""
        self.query.where(field, QueryOperation.MATCHES, f"{value}$")
        return self
    
    # === EXISTENCE CHECKS ===
    
    def where_exists(self, field: str, exists: bool = True):
        """
        Field exists condition
        
        Args:
            field: Field name
            exists: True if field should exist, False if should not exist
        
        Returns:
            self for chaining
        """
        self.query.where(field, QueryOperation.EXISTS, exists)
        return self
    
    # === REFERENCE QUERIES ===
    
    def include_reference(self, fields: List[str]):
        """
        Include referenced entries
        
        Args:
            fields: List of reference field paths
        
        Returns:
            self for chaining
        
        Example:
            .include_reference(["author", "category"])
            .include_reference(["author.reference"]) # Deep reference
        """
        for field in fields:
            self.query.include_reference(field)
        return self
    
    def include_reference_content_type_uid(self):
        """Include reference content type UID"""
        self.query.include_reference_content_type_uid()
        return self
    
    # === FIELD PROJECTION ===
    
    def only(self, fields: List[str]):
        """
        Include only specific fields
        
        Args:
            fields: List of field names to include
        
        Returns:
            self for chaining
        """
        # SDK's only() takes single string, call multiple times
        for field in fields:
            self.query.only(field)
        return self
    
    def excepts(self, fields: List[str]):
        """
        Exclude specific fields
        
        Args:
            fields: List of field names to exclude
        
        Returns:
            self for chaining
        """
        # SDK's excepts() takes single string, call multiple times
        for field in fields:
            self.query.excepts(field)
        return self
    
    # === PAGINATION ===
    
    def limit(self, count: int):
        """Set result limit"""
        self.query.limit(count)
        return self
    
    def skip(self, count: int):
        """Set skip count"""
        self.query.skip(count)
        return self
    
    def paginate(self, page: int, page_size: int):
        """
        Paginate results
        
        Args:
            page: Page number (1-indexed)
            page_size: Items per page
        
        Returns:
            self for chaining
        """
        skip_count = (page - 1) * page_size
        self.query.skip(skip_count).limit(page_size)
        return self
    
    # === SORTING ===
    
    def order_by_ascending(self, field: str):
        """Sort ascending by field"""
        self.query.order_by_ascending(field)
        return self
    
    def order_by_descending(self, field: str):
        """Sort descending by field"""
        self.query.order_by_descending(field)
        return self
    
    # === METADATA & EXTRAS ===
    
    def include_count(self):
        """Include total count in results"""
        self.query.include_count()
        return self
    
    def include_metadata(self):
        """Include entry metadata"""
        self.query.include_metadata()
        return self
    
    def include_content_type(self):
        """Include content type schema"""
        self.query.include_content_type()
        return self
    
    def include_embedded_items(self):
        """Include embedded items (for JSON RTE)"""
        self.query.include_embedded_items()
        return self
    
    def include_fallback(self):
        """Include locale fallback"""
        self.query.include_fallback()
        return self
    
    def locale(self, locale_code: str):
        """Set locale"""
        self.query.locale(locale_code)
        return self
    
    # === SEARCH ===
    
    def search(self, text: str):
        """
        Full-text search
        
        Args:
            text: Text to search for
        
        Returns:
            self for chaining
        """
        self.query.search(text)
        return self
    
    def tags(self, tag_list: List[str]):
        """
        Filter by tags
        
        Args:
            tag_list: List of tags
        
        Returns:
            self for chaining
        """
        # Unpack list as SDK's tags() uses *args
        self.query.tags(*tag_list)
        return self
    
    # === COMPLEX COMBINATIONS ===
    
    def and_query(self, conditions: List[Dict]):
        """
        Add AND conditions
        
        Args:
            conditions: List of condition dictionaries
        
        Returns:
            self for chaining
        
        Example:
            .and_query([
                {"title": {"$regex": "Test"}},
                {"status": "published"}
            ])
        """
        self.query.query_operator("$and")
        for condition in conditions:
            self.query.query(condition)
        return self
    
    def or_query(self, conditions: List[Dict]):
        """
        Add OR conditions
        
        Args:
            conditions: List of condition dictionaries
        
        Returns:
            self for chaining
        
        Example:
            .or_query([
                {"title": "Test 1"},
                {"title": "Test 2"}
            ])
        """
        self.query.query_operator("$or")
        for condition in conditions:
            self.query.query(condition)
        return self
    
    # === EXECUTION ===
    
    def build(self):
        """
        Return the built query (for inspection)
        
        Returns:
            The query object
        """
        return self.query
    
    def find(self):
        """
        Execute find operation
        
        Returns:
            Query results
        """
        return self.query.find()
    
    def find_one(self):
        """
        Execute find_one operation
        
        Returns:
            Single entry result
        """
        return self.query.find_one()
    
    def count(self):
        """
        Get count of matching entries
        
        Returns:
            Count of entries
        """
        self.include_count()
        result = self.query.find()
        return result.get('count', 0) if result else 0


# === PRESET BUILDERS ===

class PresetQueryBuilder:
    """
    Preset query builders for common scenarios
    """
    
    @staticmethod
    def create_pagination_query(query, page: int, page_size: int = 10):
        """
        Create a paginated query
        
        Args:
            query: SDK Query object
            page: Page number (1-indexed)
            page_size: Items per page
        
        Returns:
            ComplexQueryBuilder instance
        """
        return ComplexQueryBuilder(query).paginate(page, page_size).include_count()
    
    @staticmethod
    def create_search_query(query, search_text: str, fields_to_return: Optional[List[str]] = None):
        """
        Create a search query with field projection
        
        Args:
            query: SDK Query object
            search_text: Text to search
            fields_to_return: Optional list of fields to return
        
        Returns:
            ComplexQueryBuilder instance
        """
        builder = ComplexQueryBuilder(query).search(search_text)
        
        if fields_to_return:
            builder.only(fields_to_return)
        
        return builder
    
    @staticmethod
    def create_filtered_query(
        query,
        filters: Dict[str, Any],
        include_refs: Optional[List[str]] = None
    ):
        """
        Create a filtered query with references
        
        Args:
            query: SDK Query object
            filters: Dictionary of {field: value} filters
            include_refs: Optional list of references to include
        
        Returns:
            ComplexQueryBuilder instance
        """
        builder = ComplexQueryBuilder(query)
        
        for field, value in filters.items():
            builder.where(field, value)
        
        if include_refs:
            builder.include_reference(include_refs)
        
        return builder
    
    @staticmethod
    def create_comprehensive_query(query, entry_uid: Optional[str] = None):
        """
        Create a comprehensive query with all metadata
        
        Args:
            query: SDK Query object
            entry_uid: Optional specific entry UID
        
        Returns:
            ComplexQueryBuilder instance
        """
        builder = (
            ComplexQueryBuilder(query)
            .include_metadata()
            .include_content_type()
            .include_reference_content_type_uid()
            .include_count()
        )
        
        if entry_uid:
            builder.where("uid", entry_uid)
        
        return builder

