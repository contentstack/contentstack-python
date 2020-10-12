import logging
import unittest

from HtmlTestRunner import HTMLTestRunner

import contentstack
from contentstack.stack import ContentstackRegion
from tests import credentials

api_key = credentials.keys['api_key']
delivery_token = credentials.keys['delivery_token']
environment = credentials.keys['environment']
host = credentials.keys['host']
stack_instance = contentstack.Stack(api_key, delivery_token, environment, host=host)


class TestStack(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        self.host = credentials.keys['host']
        self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment, host=self.host)

    def test_01_stack_credentials(self):
        self.assertEqual(self.environment, stack_instance.environment)
        self.assertEqual(self.delivery_token, stack_instance.delivery_token)
        self.assertEqual(self.environment, stack_instance.environment)
        self.assertEqual(self.api_key, stack_instance.api_key)

    def test_02_stack_region(self):
        stack_region = contentstack.Stack(self.api_key, self.delivery_token, self.environment,
                                          region=ContentstackRegion.EU)
        self.assertEqual('eu-cdn.contentstack.com', stack_region.host)

    def test_03_stack_endpoint(self):
        logging.info('endpoint for the stack is {}'.format(self.stack.endpoint))
        self.assertEqual("https://{}/v3".format(self.host), self.stack.endpoint)

    def test_04_permission_error_api_key(self):
        try:
            stack_local = contentstack.Stack('', self.delivery_token, self.environment)
            self.assertEqual(None, stack_local.api_key)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual("'You are not permitted to the stack without valid Api Key'", e.args[0])

    def test_05_permission_error_delivery_token(self):
        try:
            stack = contentstack.Stack(self.api_key, '', self.environment)
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual("'You are not permitted to the stack without valid Delivery Token'", e.args[0])

    def test_05_permission_error_environment(self):
        try:
            stack = contentstack.Stack(self.api_key, self.delivery_token, '')
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual("You are not permitted to the stack without valid Environment", e.args[0])

    @unittest.skip("demonstrating skipping")
    def test_06_skip_for_nothing(self):
        self.fail("shouldn't happen")

    def test_07_get_api_key(self):
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.assertEqual(self.api_key, stack.get_api_key)

    def test_08_get_delivery_token(self):
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.assertEqual(self.delivery_token, stack.get_delivery_token)

    def test_09_get_environment(self):
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.assertEqual(self.environment, stack.get_environment)

    def test_10_get_headers(self):
        stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)
        self.assertEqual(True, 'api_key' in stack.headers)
        self.assertEqual(True, 'access_token' in stack.get_headers)
        self.assertEqual(True, 'environment' in stack.get_headers)
        self.assertEqual(3, stack.get_headers.__len__())

    def test_11_image_transformation(self):
        image_transform = self.stack.image_transform("cdn.contentstack.io/v3/endpoint",
                                                     width=230, height=300, other="filter")
        result_url = image_transform.get_url()
        logging.info('result url is: {}'.format(result_url))
        self.assertEqual('cdn.contentstack.io/v3/endpoint?width=230&height=300&other=filter', result_url)

    def test_12_image_transformation_get_url_with_height_width(self):
        image_url = 'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343' \
                    '/59e0c41ac0eddd140d5a8e3e/download'
        image_transform = self.stack.image_transform(image_url, width=500, height=550)
        result_url = image_transform.get_url()
        self.assertEqual(
            'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343'
            '/59e0c41ac0eddd140d5a8e3e/download?width=500&height=550',
            result_url)

    def test_13_image_transformation_get_url_with_format(self):
        image_url = 'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343' \
                    '/59e0c41ac0eddd140d5a8e3e/download'
        image_transform = self.stack.image_transform(image_url, format='gif')
        result_url = image_transform.get_url()
        self.assertEqual(
            'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343'
            '/59e0c41ac0eddd140d5a8e3e/download?format=gif',
            result_url)

    def test_14_image_transformation_invalid_input(self):
        try:
            image_transform = self.stack.image_transform('', format='gif')
            self.assertEqual(None, image_transform.get_url())
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual("image_url required for the image_transformation", e.args[0])

    def test__15_sync_pagination_with_invalid_pagination_token(self):
        result = self.stack.pagination('pagination_token')
        if result is not None:
            self.assertEqual('is not valid.', result['errors']['pagination_token'][0])

    def test_16_initialise_sync(self):
        result = self.stack.sync_init()
        if result is not None:
            logging.info(result['total_count'])
            self.assertEqual(123, result['total_count'])

    def test_17_entry_with_sync_token(self):
        result = self.stack.sync_token('sync_token')
        if result is not None:
            self.assertEqual('is not valid.', result['errors']['sync_token'][0])

    def test_18_init_sync_with_content_type_uid(self):
        result = self.stack.sync_init(content_type_uid='room')
        if result is not None:
            self.assertEqual(29, result['total_count'])

    def test_19_init_sync_with_publish_type(self):
        result = self.stack.sync_init(publish_type='entry_published', content_type_uid='track')
        if result is not None:
            self.assertEqual(16, result['total_count'])

    def test_20_init_sync_with_all_params(self):
        result = self.stack.sync_init(from_date='2018-01-14T00:00:00.000Z', content_type_uid='track',
                                      publish_type='entry_published', locale='en-us', )
        if result is not None:
            self.assertEqual(16, result['total_count'])

    def test_21_content_type(self):
        content_type = self.stack.content_type('application_theme')
        result = content_type.fetch()
        if result is not None:
            self.assertEqual('application_theme', result['content_type']['uid'])

    def test_22_content_types_with_query_param(self):
        query = {'include_count': 'true'}
        content_type = self.stack.content_type('application_theme')
        result = content_type.find(params=query)
        if result is not None:
            if 'count' in result['content_types']:
                self.assertEqual(11, result['content_types']['count'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestStack)
runner = HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)
