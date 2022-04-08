import unittest

import config
import contentstack

_preview = {
    'enable': True,
    'authorization': 'management_token@fake@testing',
    'host': 'cdn.contentstack.io'
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
        self.stack.content_type(
            'live_content_type').entry('live_entry_uid')
        self.assertEqual(3, len(self.stack.get_live_preview))
        self.assertTrue(self.stack.get_live_preview['enable'])
        self.assertTrue(self.stack.get_live_preview['authorization'])

    def test_021_live_preview_enabled_(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(_preview['authorization'],
                         self.stack.live_preview_dict['authorization'])

    def test_03_set_host(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(True, self.stack.live_preview_dict['enable'])

    def test_031_set_host_value(self):
        self.stack = contentstack.Stack(
            config.api_key,
            config.delivery_token,
            config.environment,
            live_preview=_preview)
        self.assertEqual(3, len(self.stack.live_preview_dict))
        self.assertEqual(_preview['host'],
                         self.stack.live_preview_dict['host'])

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
        self.stack.content_type('fake@content_type') \
            .entry(entry_uid='just@fakeit')

        self.assertEqual(2, len(self.stack.headers))
        self.assertEqual(config.api_key, self.stack.headers['api_key'])

    def test_branching(self):
        stack = contentstack.Stack(
            'api_key', 'delivery_token', 'environment', branch='dev_branch')
        stack.content_type('product')
        self.assertEqual('dev_branch', stack.get_branch)

    def test_branching_header(self):
        stack = contentstack.Stack(
            'api_key', 'delivery_token', 'environment', branch='dev_branch')
        stack.content_type('product')
        has = 'branch' in stack.headers
        if has:
            self.assertTrue(has)
