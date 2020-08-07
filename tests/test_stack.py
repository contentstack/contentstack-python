import logging
import unittest

from HtmlTestRunner import HTMLTestRunner

import contentstack
from contentstack.stack import ContentstackRegion
from tests import credentials

api_key = credentials.keys['api_key']
delivery_token = credentials.keys['delivery_token']
environment = credentials.keys['environment']
stack_instance = contentstack.Stack(api_key, delivery_token, environment)


class TestStack(unittest.TestCase):

    def setUp(self):
        self.api_key = credentials.keys['api_key']
        self.delivery_token = credentials.keys['delivery_token']
        self.environment = credentials.keys['environment']
        self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment)

    def test_stack_credentials(self):
        self.assertEqual(self.environment, stack_instance.environment)
        self.assertEqual(self.delivery_token, stack_instance.delivery_token)
        self.assertEqual(self.api_key, stack_instance.api_key)

    def test_stack_region(self):
        stack_region = contentstack.Stack(self.api_key, self.delivery_token, self.environment,
                                          region=ContentstackRegion.EU)
        self.assertEqual('eu-cdn.contentstack.com', stack_region.host)

    def test_stack_endpoint(self):
        logging.info('endpoint for the stack is {}'.format(self.stack.endpoint))
        self.assertEqual('https://cdn.contentstack.io/v3', self.stack.endpoint)

    def test_fail(self):
        try:
            stack_local = contentstack.Stack('', self.delivery_token, self.environment)
            self.assertEqual(None, stack_local.api_key)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual("'You are not permitted to the stack without valid Api Key'", e.args[0])

    def test_fail_delivery_token(self):
        try:
            stack = contentstack.Stack(self.api_key, '', self.environment)
            self.assertEqual(None, stack.delivery_token)
        except PermissionError as e:
            if hasattr(e, 'message'):
                self.assertEqual("'You are not permitted to the stack without valid Delivery Token'", e.args[0])

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf('', '')
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    def test_image_transformation(self):
        image_transform = self.stack.image_transform("cdn.contentstack.io/v3/endpoint",
                                                     width=230, height=300, other="filter")
        result_url = image_transform.get_url()
        logging.info('result url is: {}'.format(result_url))
        self.assertEqual('cdn.contentstack.io/v3/endpoint?width=230&height=300&other=filter', result_url)

    def test_image_transformation_get_url_with_height_width(self):
        image_url = 'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343' \
                    '/59e0c41ac0eddd140d5a8e3e/download'
        image_transform = self.stack.image_transform(image_url, width=500, height=550)
        result_url = image_transform.get_url()
        self.assertEqual(
            'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343'
            '/59e0c41ac0eddd140d5a8e3e/download?width=500&height=550',
            result_url)

    def test_image_transformation_get_url_with_format(self):
        image_url = 'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343' \
                    '/59e0c41ac0eddd140d5a8e3e/download'
        image_transform = self.stack.image_transform(image_url, format='gif')
        result_url = image_transform.get_url()
        self.assertEqual(
            'https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343'
            '/59e0c41ac0eddd140d5a8e3e/download?format=gif',
            result_url)

    # [ functional test-cases fot Synchronization ]

    # def test_sync_pagination(self):
    #     result = self.stack.pagination('blt376f0470f9334d8e512f5e')
    #     if result is not None:
    #         sync_token = result['sync_token']
    #         print(sync_token)
    #         # self.assertIsNotNone(result['sync_token'])

    def test_init_sync_no_params(self):
        result = self.stack.sync_init()
        if result is not None:
            logging.info(result['total_count'])
            self.assertEqual(123, result['total_count'])

    def test_init_sync_with_content_type_uid(self):
        result = self.stack.sync_init(content_type_uid='room')
        if result is not None:
            self.assertEqual(29, result['total_count'])

    def test_init_sync_with_publish_type(self):
        result = self.stack.sync_init(publish_type='entry_published', content_type_uid='track')
        if result is not None:
            self.assertEqual(16, result['total_count'])

    def test_init_sync_with_all_params(self):
        result = self.stack.sync_init(from_date='2018-01-14T00:00:00.000Z', content_type_uid='track',
                                      publish_type='entry_published', locale='en-us', )
        if result is not None:
            self.assertEqual(16, result['total_count'])

    def test_sync_token(self):
        result = self.stack.sync_token('blt3f16ec623aaa004a2c2539')
        sync_token = result['sync_token']
        print(sync_token)

    def test_content_type(self):
        content_type = self.stack.content_type('application_theme')
        result = content_type.fetch()
        if result is not None:
            self.assertEqual('application_theme', result['content_type']['uid'])

    def test_content_types_with_query_param(self):
        query = {'include_count': 'true'}
        content_type = self.stack.content_type('application_theme')
        result = content_type.find(params=query)
        if result is not None:
            if 'count' in result['content_types']:
                self.assertEqual(11, result['content_types']['count'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestStack)
runner = HTMLTestRunner(combine_reports=True, add_timestamp=False)
runner.run(suite)
