import unittest
# python3 -m unittest tests
from .test_stack import TestStack
from .test_assets import TestAsset
from .test_entry import TestEntry
from .test_query import TestQuery
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner


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
        test_module_query
    ])
    runner = HTMLTestRunner(combine_reports=True, report_name="test_report", add_timestamp=False)
    runner.run(suite)
