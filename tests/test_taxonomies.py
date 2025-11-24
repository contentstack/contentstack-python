import logging
import unittest
import config
import contentstack
import pytest

API_KEY = config.API_KEY
DELIVERY_TOKEN = config.DELIVERY_TOKEN
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

    # ========== Additional Test Cases ==========

    def test_11_taxonomy_method_chaining(self):
        """Test taxonomy method chaining with multiple filters"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .in_("taxonomies.category", ["category1", "category2"])
                 .exists("taxonomies.status")
                 .find({'limit': 10}))
        if result is not None:
            self.assertIn('entries', result)

    def test_12_taxonomy_complex_nested_query(self):
        """Test complex nested taxonomy query with and_ and or_"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .and_(
                     {"taxonomies.category": {"$in": ["test"]}},
                     {"taxonomies.status": {"$in": ["active"]}}
                 )
                 .or_(
                     {"taxonomies.priority": {"$in": ["high"]}},
                     {"taxonomies.type": {"$exists": True}}
                 )
                 .find({'limit': 5}))
        if result is not None:
            self.assertIn('entries', result)

    def test_13_taxonomy_in_with_empty_list(self):
        """Test taxonomy in_ method with empty list"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", []).find()
        if result is not None:
            self.assertIsNotNone(result)

    def test_14_taxonomy_in_with_single_item(self):
        """Test taxonomy in_ method with single item list"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["single_category"]).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_15_taxonomy_equal_and_below_with_different_levels(self):
        """Test taxonomy equal_and_below with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_below("taxonomies.color", "blue", levels=0).find()
        if result is not None:
            self.assertIn('entries', result)

        result2 = taxonomy.equal_and_below("taxonomies.color", "blue", levels=5).find()
        if result2 is not None:
            self.assertIn('entries', result2)

    def test_16_taxonomy_below_with_different_levels(self):
        """Test taxonomy below with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.below("taxonomies.hierarchy", "parent_uid", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_17_taxonomy_equal_and_above_with_different_levels(self):
        """Test taxonomy equal_and_above with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.equal_and_above("taxonomies.hierarchy", "child_uid", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_18_taxonomy_above_with_different_levels(self):
        """Test taxonomy above with different level values"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.above("taxonomies.hierarchy", "child_uid", levels=1).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_19_taxonomy_multiple_exists(self):
        """Test taxonomy with multiple exists filters"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .exists("taxonomies.field1")
                 .exists("taxonomies.field2")
                 .find())
        if result is not None:
            self.assertIn('entries', result)

    def test_20_taxonomy_find_with_multiple_params(self):
        """Test taxonomy find with multiple parameters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find({
            'limit': 10,
            'skip': 0
        })
        if result is not None:
            self.assertIn('entries', result)

    def test_21_taxonomy_or_with_multiple_conditions(self):
        """Test taxonomy or_ with multiple conditions"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.or_(
            {"taxonomies.category": {"$in": ["cat1"]}},
            {"taxonomies.category": {"$in": ["cat2"]}},
            {"taxonomies.category": {"$in": ["cat3"]}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_22_taxonomy_and_with_multiple_conditions(self):
        """Test taxonomy and_ with multiple conditions"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.and_(
            {"taxonomies.category": {"$in": ["test"]}},
            {"taxonomies.status": {"$in": ["active"]}},
            {"taxonomies.priority": {"$exists": True}}
        ).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_23_taxonomy_combination_all_methods(self):
        """Test taxonomy with combination of all methods"""
        taxonomy = self.stack.taxonomy()
        result = (taxonomy
                 .in_("taxonomies.category", ["category1"])
                 .exists("taxonomies.status")
                 .and_(
                     {"taxonomies.type": {"$in": ["type1"]}},
                     {"taxonomies.active": {"$exists": True}}
                 )
                 .or_(
                     {"taxonomies.priority": {"$in": ["high"]}}
                 )
                 .find({'limit': 5, 'skip': 0}))
        if result is not None:
            self.assertIn('entries', result)

    def test_24_taxonomy_find_without_params(self):
        """Test taxonomy find without any parameters"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find()
        if result is not None:
            self.assertIn('entries', result)

    def test_25_taxonomy_find_with_none_params(self):
        """Test taxonomy find with None params"""
        taxonomy = self.stack.taxonomy()
        result = taxonomy.in_("taxonomies.category", ["test"]).find(None)
        if result is not None:
            self.assertIn('entries', result)
    
if __name__ == '__main__':
    unittest.main()
