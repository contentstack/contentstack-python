import unittest
# python -m unittest -v tests
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
    suite = TestSuite([test_module_stack, test_module_asset, test_module_entry, test_module_query])
    unittest.TextTestRunner(verbosity=2).run(suite)
    # outfile = open("test_report.html", "w")
    # runner = HTMLTestRunner(output='test_report_suite')
    # runner = HTMLTestRunner(
    #     stream=outfile,
    # )
    # runner.run(suite)
    HTMLTestRunner(combine_reports=True, report_name="test_report", add_timestamp=False).run(suite)

    # suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestStack))
    # suite.addTest(unittest.makeSuite(TestAsset))
    # suite.addTest(unittest.makeSuite(TestEntry))
    # suite.addTest(unittest.makeSuite(TestQuery))
    # runner = HTMLTestRunner(output='example_suite')
    # runner.run(suite)
    # return suite
