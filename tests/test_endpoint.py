import unittest

import contentstack
from contentstack.endpoint import Endpoint
from contentstack.stack import ContentstackRegion, Stack

API_KEY = 'test_api_key'
DELIVERY_TOKEN = 'test_delivery_token'
ENVIRONMENT = 'test_environment'


class TestEndpoint(unittest.TestCase):

    def setUp(self):
        Endpoint.reset_cache()

    # -------------------------------------------------------------------------
    # Default region (us / na)
    # -------------------------------------------------------------------------

    def test_default_region_returns_all_endpoints(self):
        endpoints = Endpoint.get_contentstack_endpoint()
        self.assertIsInstance(endpoints, dict)
        self.assertIn('contentDelivery', endpoints)
        self.assertIn('contentManagement', endpoints)

    def test_default_region_content_delivery(self):
        url = Endpoint.get_contentstack_endpoint('us', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_default_region_content_management(self):
        url = Endpoint.get_contentstack_endpoint('us', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    # -------------------------------------------------------------------------
    # All 7 regions — contentDelivery spot-checks
    # -------------------------------------------------------------------------

    def test_content_delivery_na(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_content_delivery_eu(self):
        url = Endpoint.get_contentstack_endpoint('eu', 'contentDelivery')
        self.assertEqual('https://eu-cdn.contentstack.com', url)

    def test_content_delivery_au(self):
        url = Endpoint.get_contentstack_endpoint('au', 'contentDelivery')
        self.assertEqual('https://au-cdn.contentstack.com', url)

    def test_content_delivery_azure_na(self):
        url = Endpoint.get_contentstack_endpoint('azure-na', 'contentDelivery')
        self.assertEqual('https://azure-na-cdn.contentstack.com', url)

    def test_content_delivery_azure_eu(self):
        url = Endpoint.get_contentstack_endpoint('azure-eu', 'contentDelivery')
        self.assertEqual('https://azure-eu-cdn.contentstack.com', url)

    def test_content_delivery_gcp_na(self):
        url = Endpoint.get_contentstack_endpoint('gcp-na', 'contentDelivery')
        self.assertEqual('https://gcp-na-cdn.contentstack.com', url)

    def test_content_delivery_gcp_eu(self):
        url = Endpoint.get_contentstack_endpoint('gcp-eu', 'contentDelivery')
        self.assertEqual('https://gcp-eu-cdn.contentstack.com', url)

    # -------------------------------------------------------------------------
    # All 7 regions — contentManagement spot-checks
    # -------------------------------------------------------------------------

    def test_content_management_na(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_content_management_eu(self):
        url = Endpoint.get_contentstack_endpoint('eu', 'contentManagement')
        self.assertEqual('https://eu-api.contentstack.com', url)

    def test_content_management_au(self):
        url = Endpoint.get_contentstack_endpoint('au', 'contentManagement')
        self.assertEqual('https://au-api.contentstack.com', url)

    def test_content_management_azure_na(self):
        url = Endpoint.get_contentstack_endpoint('azure-na', 'contentManagement')
        self.assertEqual('https://azure-na-api.contentstack.com', url)

    def test_content_management_azure_eu(self):
        url = Endpoint.get_contentstack_endpoint('azure-eu', 'contentManagement')
        self.assertEqual('https://azure-eu-api.contentstack.com', url)

    def test_content_management_gcp_na(self):
        url = Endpoint.get_contentstack_endpoint('gcp-na', 'contentManagement')
        self.assertEqual('https://gcp-na-api.contentstack.com', url)

    def test_content_management_gcp_eu(self):
        url = Endpoint.get_contentstack_endpoint('gcp-eu', 'contentManagement')
        self.assertEqual('https://gcp-eu-api.contentstack.com', url)

    # -------------------------------------------------------------------------
    # NA aliases all resolve to the same endpoint
    # -------------------------------------------------------------------------

    def test_alias_na(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_alias_us(self):
        url = Endpoint.get_contentstack_endpoint('us', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_alias_aws_na_hyphen(self):
        url = Endpoint.get_contentstack_endpoint('aws-na', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_alias_aws_na_underscore(self):
        url = Endpoint.get_contentstack_endpoint('aws_na', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_alias_na_uppercase(self):
        url = Endpoint.get_contentstack_endpoint('NA', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_alias_us_uppercase(self):
        url = Endpoint.get_contentstack_endpoint('US', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    # -------------------------------------------------------------------------
    # Case-insensitive alias matching for other regions
    # -------------------------------------------------------------------------

    def test_alias_aws_na_uppercase(self):
        url = Endpoint.get_contentstack_endpoint('AWS-NA', 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_alias_azure_na_underscore(self):
        url = Endpoint.get_contentstack_endpoint('azure_na', 'contentDelivery')
        self.assertEqual('https://azure-na-cdn.contentstack.com', url)

    def test_alias_gcp_eu_underscore(self):
        url = Endpoint.get_contentstack_endpoint('gcp_eu', 'contentManagement')
        self.assertEqual('https://gcp-eu-api.contentstack.com', url)

    # -------------------------------------------------------------------------
    # ContentstackRegion enum constants resolve correctly
    # -------------------------------------------------------------------------

    def test_region_constant_us(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.US.value, 'contentDelivery')
        self.assertEqual('https://cdn.contentstack.io', url)

    def test_region_constant_eu(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.EU.value, 'contentDelivery')
        self.assertEqual('https://eu-cdn.contentstack.com', url)

    def test_region_constant_au(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.AU.value, 'contentDelivery')
        self.assertEqual('https://au-cdn.contentstack.com', url)

    def test_region_constant_azure_na(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.AZURE_NA.value, 'contentDelivery')
        self.assertEqual('https://azure-na-cdn.contentstack.com', url)

    def test_region_constant_azure_eu(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.AZURE_EU.value, 'contentDelivery')
        self.assertEqual('https://azure-eu-cdn.contentstack.com', url)

    def test_region_constant_gcp_na(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.GCP_NA.value, 'contentDelivery')
        self.assertEqual('https://gcp-na-cdn.contentstack.com', url)

    def test_region_constant_gcp_eu(self):
        url = Endpoint.get_contentstack_endpoint(ContentstackRegion.GCP_EU.value, 'contentDelivery')
        self.assertEqual('https://gcp-eu-cdn.contentstack.com', url)

    # -------------------------------------------------------------------------
    # omit_https flag
    # -------------------------------------------------------------------------

    def test_omit_https_strips_scheme_single_service(self):
        url = Endpoint.get_contentstack_endpoint('eu', 'contentDelivery', omit_https=True)
        self.assertEqual('eu-cdn.contentstack.com', url)

    def test_omit_https_strips_scheme_all_services(self):
        endpoints = Endpoint.get_contentstack_endpoint('na', omit_https=True)
        self.assertIsInstance(endpoints, dict)
        for key, url in endpoints.items():
            self.assertNotIn('https://', url, f'Service {key} still has https://')
            self.assertNotIn('http://', url, f'Service {key} still has http://')

    def test_omit_https_false_retains_scheme(self):
        url = Endpoint.get_contentstack_endpoint('na', 'contentManagement', omit_https=False)
        self.assertTrue(url.startswith('https://'))

    # -------------------------------------------------------------------------
    # No service — returns full dict
    # -------------------------------------------------------------------------

    def test_no_service_returns_dict(self):
        result = Endpoint.get_contentstack_endpoint('au')
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 1)

    def test_no_service_contains_correct_urls(self):
        endpoints = Endpoint.get_contentstack_endpoint('au')
        self.assertEqual('https://au-cdn.contentstack.com', endpoints['contentDelivery'])
        self.assertEqual('https://au-api.contentstack.com', endpoints['contentManagement'])

    # -------------------------------------------------------------------------
    # Error cases
    # -------------------------------------------------------------------------

    def test_empty_region_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            Endpoint.get_contentstack_endpoint('')
        self.assertIn('Empty region', str(ctx.exception))

    def test_unknown_region_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            Endpoint.get_contentstack_endpoint('invalid-region')
        self.assertIn('Invalid region', str(ctx.exception))

    def test_unknown_service_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            Endpoint.get_contentstack_endpoint('na', 'unknownService')
        self.assertIn('unknownService', str(ctx.exception))

    # -------------------------------------------------------------------------
    # contentstack.get_contentstack_endpoint() module-level proxy
    # -------------------------------------------------------------------------

    def test_module_proxy_returns_same_result(self):
        via_class = Endpoint.get_contentstack_endpoint('eu', 'contentDelivery')
        via_module = contentstack.get_contentstack_endpoint('eu', 'contentDelivery')
        self.assertEqual(via_class, via_module)

    def test_module_proxy_default_region(self):
        url = contentstack.get_contentstack_endpoint('us', 'contentManagement')
        self.assertEqual('https://api.contentstack.io', url)

    def test_module_proxy_omit_https(self):
        url = contentstack.get_contentstack_endpoint('gcp-na', 'contentDelivery', omit_https=True)
        self.assertEqual('gcp-na-cdn.contentstack.com', url)

    def test_module_proxy_all_endpoints(self):
        endpoints = contentstack.get_contentstack_endpoint('azure-eu')
        self.assertIsInstance(endpoints, dict)
        self.assertIn('contentDelivery', endpoints)

    # -------------------------------------------------------------------------
    # Stack host resolution via Endpoint
    # -------------------------------------------------------------------------

    def test_stack_us_host_resolves_to_default_cdn(self):
        stack = Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.US)
        self.assertEqual('cdn.contentstack.io', stack.host)

    def test_stack_eu_host_resolves_via_endpoint(self):
        stack = Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.EU)
        self.assertEqual('eu-cdn.contentstack.com', stack.host)

    def test_stack_au_host_resolves_via_endpoint(self):
        stack = Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.AU)
        self.assertEqual('au-cdn.contentstack.com', stack.host)

    def test_stack_azure_na_host_resolves_via_endpoint(self):
        stack = Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.AZURE_NA)
        self.assertEqual('azure-na-cdn.contentstack.com', stack.host)

    def test_stack_gcp_eu_host_resolves_via_endpoint(self):
        stack = Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.GCP_EU)
        self.assertEqual('gcp-eu-cdn.contentstack.com', stack.host)

    def test_stack_explicit_host_overrides_region(self):
        stack = Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT,
            host='custom.cdn.example.com',
            region=ContentstackRegion.EU
        )
        self.assertEqual('custom.cdn.example.com', stack.host)

    def test_stack_endpoint_built_from_resolved_host(self):
        stack = Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.EU)
        self.assertEqual('https://eu-cdn.contentstack.com/v3', stack.endpoint)


if __name__ == '__main__':
    unittest.main()
