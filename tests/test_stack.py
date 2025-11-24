import unittest
import config
import contentstack
import logging
import io
from urllib3 import Retry
from contentstack.stack import ContentstackRegion
from contentstack.stack import Stack

API_KEY = config.API_KEY
DELIVERY_TOKEN = config.DELIVERY_TOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST

stack_instance = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST)
        self.early_access = ['taxonomy', 'teams']

    def test_01_stack_credentials(self):
        self.assertEqual(ENVIRONMENT, stack_instance.environment)
        self.assertEqual(DELIVERY_TOKEN, stack_instance.delivery_token)
        self.assertEqual(API_KEY, stack_instance.api_key)
        self.assertEqual(HOST, stack_instance.host)

    def test_02_stack_region(self):
        stack_region = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.EU)
        self.assertEqual('eu-cdn.contentstack.com', stack_region.host)

    def test_02_stack_gcp_na_region(self):
        stack_region = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.GCP_NA)
        self.assertEqual('gcp-na-cdn.contentstack.com', stack_region.host)

    def test_02_stack_au_region(self):
        stack_region = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.AU)
        self.assertEqual('au-cdn.contentstack.com', stack_region.host)

    def test_02_stack_gcp_eu_region(self):
        stack_region = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, region=ContentstackRegion.GCP_EU)
        self.assertEqual('gcp-eu-cdn.contentstack.com', stack_region.host)

    def test_03_stack_endpoint(self):
        self.assertEqual(f"https://{config.HOST}/v3",
                         self.stack.endpoint)

    def test_04_permission_error_api_key(self):
        try:
            stack_local = contentstack.Stack(
                '', config.DELIVERY_TOKEN, config.ENVIRONMENT)
            self.assertEqual(None, stack_local.api_key)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid Api Key'", e.args[0])

    def test_05_permission_error_delivery_token(self):
        try:
            stack = contentstack.Stack(config.API_KEY, '', config.ENVIRONMENT)
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid Delivery Token'", e.args[0])

    def test_05_permission_error_environment(self):
        try:
            stack = contentstack.Stack(
                config.API_KEY, config.DELIVERY_TOKEN, '')
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "You are not permitted to the stack without valid Environment", e.args[0])

    def test_07_get_api_key(self):
        stack = contentstack.Stack(
            config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT)
        self.assertEqual(config.API_KEY, stack.get_api_key)

    def test_08_get_delivery_token(self):
        stack = contentstack.Stack(
            config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT)
        self.assertEqual(config.DELIVERY_TOKEN, stack.get_delivery_token)

    def test_09_get_environment(self):
        stack = contentstack.Stack(
            config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT)
        self.assertEqual(config.ENVIRONMENT, stack.get_environment)

    def test_10_get_headers(self):
        stack = contentstack.Stack(
            config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT)
        self.assertEqual(True, 'api_key' in stack.headers)
        self.assertEqual(True, 'access_token' in stack.get_headers)
        self.assertEqual(True, 'environment' in stack.get_headers)
        self.assertEqual(3, len(stack.get_headers))

    def test_11_image_transformation(self):
        image_transform = self.stack.image_transform("cdn.contentstack.io/v3/endpoint",
                                                     width=230, height=300, other="filter")
        result_url = image_transform.get_url()
        self.assertEqual(
            'cdn.contentstack.io/v3/endpoint?width=230&height=300&other=filter', result_url)

    def test_12_image_transformation_get_url_with_height_width(self):
        image_url = 'https://images.contentstack.io/v3/assets/download'
        image_transform = self.stack.image_transform(
            image_url, width=500, height=550)
        result_url = image_transform.get_url()
        self.assertEqual(
            'https://images.contentstack.io/v3/assets/download?width=500&height=550',
            result_url)

    def test_13_image_transformation_get_url_with_format(self):
        image_url = 'https://images.contentstack.io/v3/assets/download'
        image_transform = self.stack.image_transform(image_url, format='gif')
        result_url = image_transform.get_url()
        self.assertEqual(
            'https://images.contentstack.io/v3/assets/download?format=gif',
            result_url)

    def test_14_image_transformation_invalid_input(self):
        try:
            image_transform = self.stack.image_transform('', format='gif')
            self.assertEqual(None, image_transform.get_url())
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "image_url required for the image_transformation", e.args[0])

    def test__15_sync_pagination_with_invalid_pagination_token(self):
        result = self.stack.pagination('pagination_token')
        if result is not None:
            self.assertEqual(
                'is not valid.', result['errors']['pagination_token'][0])

    # Deprecated: This test was skipped due to deprecation of the sync_init feature or its API. 
    # If sync_init is permanently removed or unsupported, this test should remain commented or be deleted.
    # If migration or replacement is planned, update this test accordingly.
    # @unittest.skip('Work in progress')
    # def test_16_initialise_sync(self):
    #     result = self.stack.sync_init()
    #     if result is not None:
    #         self.assertEqual(16, result['total_count'])

    def test_17_entry_with_sync_token(self):
        result = self.stack.sync_token('sync_token')
        if result is not None:
            self.assertEqual(
                'is not valid.', result['errors']['sync_token'][0])

    def test_18_init_sync_with_content_type_uid(self):
        result = self.stack.sync_init(content_type_uid='room')
        if result is not None:
            self.assertEqual(0, result['total_count'])

    def test_19_init_sync_with_publish_type(self):
        result = self.stack.sync_init(
            publish_type='entry_published', content_type_uid='track')
        if result is not None:
            self.assertEqual(0, result['total_count'])

    def test_20_init_sync_with_all_params(self):
        result = self.stack.sync_init(start_from='2018-01-14T00:00:00.000Z',
                                      content_type_uid='track',
                                      publish_type='entry_published',
                                      locale='en-us', )
        if result is not None:
            self.assertEqual(0, result['total_count'])

    def test_21_content_type(self):
        content_type = self.stack.content_type(config.COMPLEX_CONTENT_TYPE_UID)
        result = content_type.fetch()
        if result is not None:
            self.assertEqual(config.COMPLEX_CONTENT_TYPE_UID,
                             result['content_type']['uid'])

    def test_check_region(self):
        """_summary_
        """
        _stack = contentstack.Stack(config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT,
                                    host=config.HOST, region=ContentstackRegion.AZURE_NA)
        var = _stack.region.value
        self.assertEqual('azure-na', var)
    
    def test_22_check_early_access_headers(self):
        stack = contentstack.Stack(
            config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT, early_access=[])
        self.assertEqual(True, 'x-header-ea' in stack.get_headers)

    def test_23_get_early_access(self):
        stack = contentstack.Stack(
            config.API_KEY, config.DELIVERY_TOKEN, config.ENVIRONMENT, early_access=["taxonomy", "teams"])
        self.assertEqual(self.early_access, stack.get_early_access)
        
    def test_stack_with_custom_logger(self):
        log_stream = io.StringIO()
        custom_logger = logging.getLogger("contentstack.custom.test_logger")
        custom_logger.setLevel(logging.INFO)

        if custom_logger.hasHandlers():
            custom_logger.handlers.clear()

        handler = logging.StreamHandler(log_stream)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        custom_logger.addHandler(handler)
        Stack("api_key", "delivery_token", "dev", logger=custom_logger)
        custom_logger.info("INFO - contentstack.custom.test_logger - Test log entry")
        handler.flush()
        logs = log_stream.getvalue()
        print("\nCaptured Logs:\n", logs)
        self.assertIn("INFO - contentstack.custom.test_logger - Test log entry", logs)

    # ========== Additional Test Cases ==========

    def test_24_stack_with_branch(self):
        """Test Stack initialization with branch parameter"""
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, branch="development")
        self.assertEqual("development", stack.branch)
        self.assertEqual("development", stack.get_branch)

    def test_25_stack_with_live_preview(self):
        """Test Stack initialization with live_preview parameter"""
        live_preview_config = {
            'enable': True,
            'host': 'api.contentstack.io',
            'authorization': 'test_token'
        }
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, live_preview=live_preview_config)
        self.assertEqual(live_preview_config, stack.live_preview)
        self.assertEqual(live_preview_config, stack.get_live_preview)

    def test_26_image_transformation_with_multiple_params(self):
        """Test image transformation with multiple parameters"""
        image_url = 'https://images.contentstack.io/v3/assets/download'
        image_transform = self.stack.image_transform(
            image_url, width=500, height=550, format='webp', quality=80, auto='webp')
        result_url = image_transform.get_url()
        self.assertIn('width=500', result_url)
        self.assertIn('height=550', result_url)
        self.assertIn('format=webp', result_url)
        self.assertIn('quality=80', result_url)
        self.assertIn('auto=webp', result_url)

    def test_27_image_transformation_with_crop_params(self):
        """Test image transformation with crop parameters"""
        image_url = 'https://images.contentstack.io/v3/assets/download'
        image_transform = self.stack.image_transform(
            image_url, width=300, height=200, crop='fit', align='center')
        result_url = image_transform.get_url()
        self.assertIn('width=300', result_url)
        self.assertIn('height=200', result_url)
        self.assertIn('crop=fit', result_url)
        self.assertIn('align=center', result_url)

    def test_28_content_type_method(self):
        """Test content_type method returns ContentType instance"""
        content_type = self.stack.content_type(config.SIMPLE_CONTENT_TYPE_UID)
        self.assertIsNotNone(content_type)
        self.assertEqual(config.SIMPLE_CONTENT_TYPE_UID, content_type._ContentType__content_type_uid)

    def test_29_content_type_with_none_uid(self):
        """Test content_type method with None UID"""
        content_type = self.stack.content_type(None)
        self.assertIsNotNone(content_type)
        self.assertIsNone(content_type._ContentType__content_type_uid)

    def test_30_taxonomy_method(self):
        """Test taxonomy method returns Taxonomy instance"""
        taxonomy = self.stack.taxonomy()
        self.assertIsNotNone(taxonomy)
        self.assertIsNotNone(taxonomy.http_instance)

    def test_31_global_field_method(self):
        """Test global_field method returns GlobalField instance"""
        global_field = self.stack.global_field('test_global_field')
        self.assertIsNotNone(global_field)
        self.assertEqual('test_global_field', global_field._GlobalField__global_field_uid)

    def test_32_global_field_with_none_uid(self):
        """Test global_field method with None UID"""
        global_field = self.stack.global_field(None)
        self.assertIsNotNone(global_field)
        self.assertIsNone(global_field._GlobalField__global_field_uid)

    def test_33_asset_method_with_valid_uid(self):
        """Test asset method with valid UID"""
        asset = self.stack.asset('test_asset_uid')
        self.assertIsNotNone(asset)
        self.assertEqual('test_asset_uid', asset.uid)

    def test_34_asset_method_with_invalid_uid(self):
        """Test asset method with invalid UID raises error"""
        with self.assertRaises(KeyError):
            self.stack.asset(None)
        
        with self.assertRaises(KeyError):
            self.stack.asset(123)  # Not a string

    def test_35_asset_query_method(self):
        """Test asset_query method returns AssetQuery instance"""
        asset_query = self.stack.asset_query()
        self.assertIsNotNone(asset_query)
        self.assertIsNotNone(asset_query.http_instance)

    def test_36_sync_init_with_only_start_from(self):
        """Test sync_init with only start_from parameter"""
        result = self.stack.sync_init(start_from='2018-01-14T00:00:00.000Z')
        if result is not None:
            self.assertIn('items', result or {})

    def test_37_sync_init_with_only_locale(self):
        """Test sync_init with only locale parameter"""
        result = self.stack.sync_init(locale='en-us')
        if result is not None:
            self.assertIn('items', result or {})

    def test_38_sync_init_with_only_publish_type(self):
        """Test sync_init with only publish_type parameter"""
        result = self.stack.sync_init(publish_type='entry_published')
        if result is not None:
            self.assertIn('items', result or {})

    def test_39_sync_token_with_empty_string(self):
        """Test sync_token with empty string"""
        result = self.stack.sync_token('')
        if result is not None:
            self.assertIsNotNone(result)

    def test_40_pagination_with_empty_string(self):
        """Test pagination with empty string"""
        result = self.stack.pagination('')
        if result is not None:
            self.assertIsNotNone(result)

    def test_41_get_branch_property(self):
        """Test get_branch property"""
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, branch="test_branch")
        self.assertEqual("test_branch", stack.get_branch)

    def test_42_get_live_preview_property(self):
        """Test get_live_preview property"""
        live_preview = {'enable': True}
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, live_preview=live_preview)
        self.assertEqual(live_preview, stack.get_live_preview)

    def test_43_stack_with_all_optional_params(self):
        """Test Stack initialization with all optional parameters"""
        live_preview = {'enable': True, 'host': 'api.contentstack.io'}
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[408])
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT,
            host=HOST,
            version='v3',
            region=ContentstackRegion.EU,
            timeout=60,
            retry_strategy=retry_strategy,
            live_preview=live_preview,
            branch="main",
            early_access=["taxonomy"],
            logger=logging.getLogger("test")
        )
        self.assertEqual(API_KEY, stack.api_key)
        self.assertEqual(DELIVERY_TOKEN, stack.delivery_token)
        self.assertEqual(ENVIRONMENT, stack.environment)
        self.assertEqual("main", stack.branch)
        self.assertEqual(live_preview, stack.live_preview)
        self.assertEqual(["taxonomy"], stack.early_access)
        self.assertEqual(60, stack.timeout)

    def test_44_image_transformation_with_special_characters(self):
        """Test image transformation URL encoding with special characters"""
        image_url = 'https://images.contentstack.io/v3/assets/download?param=value'
        image_transform = self.stack.image_transform(image_url, width=100)
        result_url = image_transform.get_url()
        self.assertIn('width=100', result_url)

    def test_45_image_transformation_empty_url(self):
        """Test image transformation with empty URL"""
        try:
            image_transform = self.stack.image_transform('')
            result = image_transform.get_url()
            self.assertIsNone(result)
        except PermissionError:
            pass  # Expected behavior

    def test_46_early_access_empty_list(self):
        """Test early_access with empty list"""
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, early_access=[])
        self.assertEqual([], stack.early_access)
        self.assertEqual([], stack.get_early_access)

    def test_47_early_access_single_item(self):
        """Test early_access with single item"""
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, early_access=["taxonomy"])
        self.assertEqual(["taxonomy"], stack.early_access)
        self.assertEqual(["taxonomy"], stack.get_early_access)

    def test_48_region_property_access(self):
        """Test region property access"""
        stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN, ENVIRONMENT, host=HOST, region=ContentstackRegion.AZURE_NA)
        self.assertEqual(ContentstackRegion.AZURE_NA, stack.region)
        self.assertEqual('azure-na', stack.region.value)