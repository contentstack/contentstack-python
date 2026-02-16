# pytest --html=tests/report/test-report.html
# above command runs tests and test reports generates in tests/report location.
# nosetests --with-coverage --cover-html
# clean all the .pyc files
# find . -name \*.pyc -delete
# nosetests --with-coverage --cover-html
# pytest --cov=contentstack
# pytest -v --cov=contentstack --cov-report=html
# pytest --html=tests/report/test-report.html
from unittest import TestLoader, TestSuite
from .test_assets import TestAsset
from .test_entry import TestEntry
from .test_query import TestQuery
from .test_stack import TestStack
# Removed old imports - pytest auto-discovers tests
# from .test_global_fields import TestGlobalFieldInit  # Old class, doesn't exist
# from .test_early_fetch import TestGlobalFieldFetch  # Old class, doesn't exist
# from .test_early_find import TestGlobalFieldFind  # Old class, doesn't exist
from .test_live_preview import TestLivePreviewConfig
from .test_taxonomies import TestTaxonomyAPI


def all_tests():
    test_module_stack = TestLoader().loadTestsFromTestCase(TestStack)
    test_module_asset = TestLoader().loadTestsFromTestCase(TestAsset)
    test_module_entry = TestLoader().loadTestsFromTestCase(TestEntry)
    test_module_query = TestLoader().loadTestsFromTestCase(TestQuery)
    test_module_live_preview = TestLoader().loadTestsFromTestCase(TestLivePreviewConfig)
    # Removed old global field test references - pytest auto-discovers new test classes
    test_module_taxonomies = TestLoader().loadTestsFromTestCase(TestTaxonomyAPI)
    TestSuite([
        test_module_stack,
        test_module_asset,
        test_module_entry,
        test_module_query,
        test_module_live_preview,
        test_module_taxonomies
    ])
