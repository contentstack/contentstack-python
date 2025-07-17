import logging
import unittest
import config
import contentstack
import pytest

API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST

class TestTaxonomyAPI(unittest.TestCase):
    def setUp(self):
        self.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)
    
    def test_01_taxonomy_complex_query(self):
        """Test complex taxonomy query combining multiple filters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.and_(
            {"taxonomies.category": {"$in": ["test"]}},
            {"taxonomies.test1": {"$exists": True}}
        ).or_(
            {"taxonomies.status": {"$in": ["active"]}},
            {"taxonomies.priority": {"$in": ["high"]}}
        ).find({'limit': 10})
        if result is not None:
            self.assertIn('entries', result)
            
    def test_02_taxonomy_in_query(self):
        """Test taxonomy query with $in filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["category1", "category2"]).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_03_taxonomy_exists_query(self):
        """Test taxonomy query with $exists filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.exists("taxonomies.test1").find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_04_taxonomy_or_query(self):
        """Test taxonomy query with $or filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.or_(
            {"taxonomies.category": {"$in": ["category1"]}},
            {"taxonomies.test1": {"$exists": True}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_05_taxonomy_and_query(self):
        """Test taxonomy query with $and filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.and_(
            {"taxonomies.category": {"$in": ["category1"]}},
            {"taxonomies.test1": {"$exists": True}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_06_taxonomy_equal_and_below(self):
        """Test taxonomy query with $eq_below filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_below("taxonomies.color", "blue", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_07_taxonomy_below(self):
        """Test taxonomy query with $below filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.below("taxonomies.hierarchy", "parent_uid", levels=2).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_08_taxonomy_equal_and_above(self):
        """Test taxonomy query with $eq_above filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_above("taxonomies.hierarchy", "child_uid", levels=3).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_09_taxonomy_above(self):
        """Test taxonomy query with $above filter"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.above("taxonomies.hierarchy", "child_uid", levels=2).find()
        if result is not None:
            self.assertIn('entries', result)
    
    def test_10_taxonomy_find_with_params(self):
        """Test taxonomy find with additional parameters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find({'limit': 5})
        if result is not None:
            self.assertIn('entries', result)
    
if __name__ == '__main__':
    unittest.main()
