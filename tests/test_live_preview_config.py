import unittest

import config
import contentstack

_preview = {
    'enable': True,
    'authorization': 'management_token@fake@testing',
    'host': 'fake-live-preview.contentstack.io'
}


class TestLivePreviewConfig(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(
            config.api_key, config.delivery_token,
            config.environment, host=config.host)

    def test_01_live_preview_enabled_(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        entry = self.stack.content_type('live_content_type').entry('live_entry_uid')
        self.assertEqual(3, len(self.stack.get_live_preview))
        self.assertTrue(self.stack.get_live_preview['enable'])
        self.assertTrue(self.stack.get_live_preview['authorization'])

    def test_02_live_preview_enabled_(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_021_live_preview_enabled_(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(_preview['authorization'], self.stack.live_preview_dict['authorization'])

    def test_03_set_host(self):
        host = 'abc.contentstack.com'
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_031_set_host_value(self):
        host = 'abc.contentstack.com'
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(_preview['host'], self.stack.live_preview_dict['host'])

    def test_04_include_edit_tags(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_05_include_edit_tags_type(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_06_live_preview_query(self):
        _live_preview = {
            'include_edit_tags': True,
            'edit_tags_type': object,
        }
        _preview.update(_live_preview)
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview
        )
        self.assertEqual(5, len(self.stack.live_preview_dict))

    def test_07_live_preview_query_hash_included(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview
        )
        self.stack.live_preview_query(
            hash='live_preview',
            content_type_uid='fake@content_type')
        self.assertEqual(7, len(self.stack.live_preview_dict))

    def test_08_live_preview_query_hash_excluded(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview
        )
        self.stack.live_preview_query(
            content_type_uid='_content_type_live_preview')
        self.stack.content_type('_content_type_live_preview') \
            .entry(entry_uid='entry_uid_1234')

        self.assertEqual(2, len(self.stack.headers))
        self.assertEqual(False, 'live_preview' in self.stack.headers)
        self.assertEqual(True, 'api_key' in self.stack.headers)

    def test_09_live_preview_check_hash_value(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview
        )
        self.stack.live_preview_query(
            content_type_uid='_content_type_live_preview')
        self.stack.content_type('_content_type_live_preview') \
            .entry(entry_uid='entry_uid_1234')

        self.assertEqual(2, len(self.stack.headers))
        self.assertEqual(config.api_key, self.stack.headers['api_key'])

    def test_10_live_preview_fail_expected_due_to_invalid_host(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview
        )
        self.stack.live_preview_query(
            live_preview='abcd@fake',
            content_type_uid='_content_type_live_preview')
        content_type = self.stack.content_type(content_type_uid='_content_type_live_preview')
        entry = content_type.entry(entry_uid='entry@fake@uid')
        entry.fetch()
        self.assertEqual(3, entry.http_instance)
        self.assertEqual('https://fake-live-preview.contentstack.io/v3', entry.http_instance.endpoint)
        self.assertEqual(2, len(entry.http_instance.headers))
