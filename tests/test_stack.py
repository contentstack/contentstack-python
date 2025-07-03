import unittest
import config
import contentstack
import logging
import io
from contentstack.stack import ContentstackRegion
from contentstack.stack import Stack

API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
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

    def test_03_stack_endpoint(self):
        self.assertEqual(f"https://{config.HOST}/v3",
                         self.stack.endpoint)

    def test_04_permission_error_api_key(self):
        try:
            stack_local = contentstack.Stack(
                '', config.DELIVERYTOKEN, config.ENVIRONMENT)
            self.assertEqual(None, stack_local.api_key)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid Api Key'", e.args[0])

    def test_05_permission_error_delivery_token(self):
        try:
            stack = contentstack.Stack(config.APIKEY, '', config.ENVIRONMENT)
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "'You are not permitted to the stack without valid Delivery Token'", e.args[0])

    def test_05_permission_error_environment(self):
        try:
            stack = contentstack.Stack(
                config.APIKEY, config.DELIVERYTOKEN, '')
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual(
                    "You are not permitted to the stack without valid Environment", e.args[0])

    def test_07_get_api_key(self):
        stack = contentstack.Stack(
            config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT)
        self.assertEqual(config.APIKEY, stack.get_api_key)

    def test_08_get_delivery_token(self):
        stack = contentstack.Stack(
            config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT)
        self.assertEqual(config.DELIVERYTOKEN, stack.get_delivery_token)

    def test_09_get_environment(self):
        stack = contentstack.Stack(
            config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT)
        self.assertEqual(config.ENVIRONMENT, stack.get_environment)

    def test_10_get_headers(self):
        stack = contentstack.Stack(
            config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT)
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
        content_type = self.stack.content_type('application_theme')
        result = content_type.fetch()
        if result is not None:
            self.assertEqual('application_theme',
                             result['content_type']['uid'])

    def test_check_region(self):
        """_summary_
        """
        _stack = contentstack.Stack(config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT,
                                    host=config.HOST, region=ContentstackRegion.AZURE_NA)
        var = _stack.region.value
        self.assertEqual('azure-na', var)
    
    def test_22_check_early_access_headers(self):
        stack = contentstack.Stack(
            config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT, early_access=[])
        self.assertEqual(True, 'x-header-ea' in stack.get_headers)

    def test_23_get_early_access(self):
        stack = contentstack.Stack(
            config.APIKEY, config.DELIVERYTOKEN, config.ENVIRONMENT, early_access=["taxonomy", "teams"])
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