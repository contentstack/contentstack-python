import unittest
# python -m unittest -v tests
from .test_stack import TestStack
from .test_assets import TestAsset
# from .test_entry import TestEntry
# from .test_query import TestQuery


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStack))
    suite.addTest(unittest.makeSuite(TestAsset))
    # suite.addTest(unittest.makeSuite(TestEntry))
    # suite.addTest(unittest.makeSuite(TestQuery))
    return suite
