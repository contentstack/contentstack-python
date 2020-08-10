# python3 -m unittest tests
# clean all the .pyc files
# find . -name \*.pyc -delete
import unittest
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner
from .test_assets import TestAsset
from .test_entry import TestEntry
from .test_query import TestQuery
from .test_stack import TestStack


def all_tests():
    test_module_stack = TestLoader().loadTestsFromTestCase(TestStack)
    test_module_asset = TestLoader().loadTestsFromTestCase(TestAsset)
    test_module_entry = TestLoader().loadTestsFromTestCase(TestEntry)
    test_module_query = TestLoader().loadTestsFromTestCase(TestQuery)
    suite = TestSuite([
        test_module_stack,
        test_module_asset,
        test_module_entry,
        test_module_query,
    ])
    runner = HTMLTestRunner(output='reports')
    test_suite = unittest.TestLoader().discover('./', '*_test.py', '.')
    runner.run(test_suite)

