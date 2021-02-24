# python3 -m unittest tests
# nosetests --with-coverage --cover-html
# clean all the .pyc files
# find . -name \*.pyc -delete
# nosetests --with-coverage --cover-html
# pytest --cov=contentstack
# pytest -v --cov=contentstack --cov-report=html
# pytest --html=report/test-report.html
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
    runner = HTMLTestRunner(output='reports', combine_reports=True, add_timestamp=False)
    test_suite = unittest.TestLoader().discover('./', '*_test.py', '.')
    runner.run(test_suite)