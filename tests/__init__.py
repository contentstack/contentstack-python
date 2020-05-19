import unittest
# python -m unittest -v tests
from .test_assets import TestAsset
from .test_entry import TestEntry
from .test_query import TestQuery
from .test_stack import TestStack


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAsset))
    suite.addTest(unittest.makeSuite(TestEntry))
    suite.addTest(unittest.makeSuite(TestQuery))
    suite.addTest(unittest.makeSuite(TestStack))
    return suite
