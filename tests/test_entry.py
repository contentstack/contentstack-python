import logging
import unittest

from contentstack import Entry
from contentstack.stack import Stack


class TestEntry(unittest.TestCase):

    log = logging.getLogger(__name__)

    def setUp(self):

        api_key: str = 'blt20962a819b57e233'
        access_token: str = 'cs18efd90468f135a3a5eda3ba'
        env_prod: str = 'production'
        self.entry_uid = 'blt9965f5f9840923ba'
        self.stack_entry = Stack(api_key=api_key, access_token=access_token, environment=env_prod)

    def test_entry_by_uid(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        result = _entry.fetch()
        if result is not None:
            self.assertEqual(Entry, type(result))

    def test_entry_title(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        result: Entry = _entry.fetch()
        if result is not None:
            self.assertEqual("Redmi Note 3", result.title)

    def test_entry_url(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        result: Entry = _entry.fetch()
        if result is not None:
            self.assertEqual("", result.urls)

    def test_entry_tags(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        result: Entry = _entry.fetch()
        if result is not None:
            self.assertEqual(list, type(result.tags))

    def test_entry_content_type(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        result = _entry.fetch()
        if result is not None:
            self.assertEqual('product', _entry.content_type)

    def test_is_entry_uid_correct(self):
        entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        result = entry.fetch()
        if result is not None:
            self.assertEqual(self.entry_uid, result.uid)

    def test_entry_locale(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result: Entry = _entry.fetch()
        if result is not None:
            if '-' in result.locale:
                self.assertEqual('en-us', result.locale)

    def test_entry_to_json(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            self.assertEqual(dict, type(_entry.to_json))

    def test_entry_get(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result: Entry = _entry.fetch()
        if result is not None:
            self.assertEqual('blt9965f5f9840923ba', result.get('uid'))

    def test_entry_string(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result: Entry = _entry.fetch()
        if result is not None:
            self.assertEqual(str, type(result.get_string('description')))

    def test_entry_boolean(self):
        entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        entry.locale = 'en-us'
        result = entry.fetch()
        if result is not None:
            self.assertFalse(None, type(entry.get_boolean('description')))

    def test_entry_json(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result: Entry = _entry.fetch()
        if result is not None:
            json_result = result.get_json('publish_details')
            self.assertEqual(dict, type(json_result))

    def test_entry_get_int(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            json_result = _entry.get_int('color')
            self.assertFalse(None, type(json_result))

    def test_entry_get_created_at(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            created_at = _entry.created_at
            self.assertTrue(str, type(created_at))

    def test_entry_get_created_by(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            created_by = _entry.created_by
            self.assertTrue(str, type(created_by))

    def test_entry_get_updated_at(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            updated_at = _entry.updated_at
            self.assertTrue(str, type(updated_at))

    def test_entry_get_updated_by(self):
        _entry = self.stack_entry.content_type('product').entry(self.entry_uid)
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            updated_by = _entry.updated_by
            self.assertTrue(str, type(updated_by))

    def test_entry_get_asset(self):
        # _entry = self.stack_entry.content_type('product').entry(self.entry_uid))
        # _entry.locale = 'en-us'
        pass
