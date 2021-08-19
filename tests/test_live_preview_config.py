import unittest

import config
import contentstack


class TestLivePreviewConfig(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(
            config.api_key, config.delivery_token,
            config.environment, host=config.host)

    def test_01_live_preview_enabled_(self):
        enable_preview = {'enable': 'true', 'authorization': 'authorization_token'}
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=enable_preview
        )
        entry = self.stack.content_type('live_content_type').entry('live_entry_uid')
        self.assertEqual(2, len(self.stack.get_live_preview))
        self.assertTrue(self.stack.get_live_preview['enable'])
        self.assertTrue(self.stack.get_live_preview['authorization'])

    def test_02_live_preview_enabled_(self):
        live_preview = {
            'enable': True,
            'authorization': 'management_token',
        }
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=live_preview)
        self.assertEqual(2, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_021_live_preview_enabled_(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
            })
        self.assertEqual('management_token',
                         self.stack.live_preview_dict['authorization'])

    def test_03_set_host(self):
        host = 'abc.contentstack.com'
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
                'host': host,
            })
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_031_set_host_value(self):
        host = 'abc.contentstack.com'
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
                'host': host,
            })
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(host, self.stack.live_preview_dict['host'])

    def test_04_include_edit_tags(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
                'include_edit_tags': True,
            })
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_041_include_edit_tags_value(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
                'include_edit_tags': True,
            })
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['include_edit_tags'])

    def test_05_include_edit_tags_type(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
                'edit_tags_type': 'string'
            })
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_051_include_edit_tags_type(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview={
                'enable': True,
                'authorization': 'management_token',
                'edit_tags_type': 'string'
            })
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual('string', self.stack.live_preview_dict['edit_tags_type'])

    def test_06_live_preview_query(self):
        live_preview = {
            'enable': True,
            'authorization': 'management_token',
            'host': 'api.contentstack.com',
            'include_edit_tags': True,
            'edit_tags_type': object,
        }
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=live_preview
        )
        self.assertEqual(5, len(self.stack.live_preview_dict))

    def test_07_live_preview_query_hash_included(self):
        live_preview = {
            'enable': True,
            'authorization': 'management_token',
            'host': 'api.contentstack.com',
        }
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=live_preview
        )
        self.stack.live_preview_query(
            hash='_hash_key',
            content_type_uid='_content_type_live_preview')
        self.assertEqual(5, len(self.stack.live_preview_dict))

    def test_08_live_preview_query_hash_excluded(self):
        live_preview = {
            'enable': True,
            'authorization': 'management_token',
            'host': 'api.contentstack.com',
        }
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=live_preview
        )
        self.stack.live_preview_query(
            content_type_uid='_content_type_live_preview')
        self.stack.content_type('_content_type_live_preview') \
            .entry(entry_uid='entry_uid_1234')

        self.assertEqual(3, len(self.stack.headers))
        self.assertEqual(False, 'hash' in self.stack.headers)
        self.assertEqual(True, 'api_key' in self.stack.headers)

    def test_09_live_preview_check_hash_value(self):
        live_preview = {
            'enable': True,
            'authorization': 'management_token',
            'host': 'api.contentstack.com',
        }
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=live_preview
        )
        self.stack.live_preview_query(
            content_type_uid='_content_type_live_preview')
        self.stack.content_type('_content_type_live_preview') \
            .entry(entry_uid='entry_uid_1234')

        self.assertEqual(3, len(self.stack.headers))
        self.assertEqual(config.api_key, self.stack.headers['api_key'])

    # def test_10_live_preview_query_content_type_check(self):
    #     live_preview = {
    #         'enable': True,
    #         'authorization': 'management_token',
    #         'host': 'live.contentstack.com',
    #     }
    #     self.stack = contentstack.Stack(
    #         config.api_key,
    #         config.delivery_token,
    #         config.environment,
    #         live_preview=live_preview
    #     )
    #     self.stack.live_preview_query(
    #         hash='_hash_key',
    #         content_type_uid='_content_type_live_preview')
    #     content_type = self.stack.content_type(content_type_uid='_content_type_live_preview')
    #     entry = content_type.entry(entry_uid='live_content_type')
    #     entry.fetch()
    #     self.assertEqual(3, entry.http_instance)
