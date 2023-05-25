import unittest

import config
import contentstack
from contentstack.deep_merge_lp import DeepMergeMixin

management_token = 'cs8743874323343u9'
entry_uid = 'blt8743874323343u9'

_lp_query = {
    'live_preview': '#0#0#0#0#0#0#0#0#0#',
    'content_type_uid': 'product',
    'entry_uid': entry_uid
}
_lp = {
    'enable': True,
    'host': 'api.contentstack.io',
    'management_token': management_token
}

API_KEY = config.APIKEY
DELIVERY_TOKEN = config.DELIVERYTOKEN
ENVIRONMENT = config.ENVIRONMENT
HOST = config.HOST
ENTRY_UID = config.APIKEY


class TestLivePreviewConfig(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN,
            ENVIRONMENT, host=HOST)

    def test_live_preview_disabled(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview={
                'enable': False,
                'host': 'api.contentstack.io',
                'management_token': 'string987654321'
            })
        self.stack.content_type('product').entry(entry_uid)
        self.assertEqual(3, len(self.stack.get_live_preview))
        self.assertFalse(self.stack.get_live_preview['enable'])
        self.assertTrue(self.stack.get_live_preview['management_token'])

    def test_021_live_preview_enabled(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp)
        self.stack.live_preview_query(live_preview_query=_lp_query)
        self.assertIsNotNone(self.stack.live_preview['management_token'])
        self.assertEqual(7, len(self.stack.live_preview))
        self.assertEqual('product', self.stack.live_preview['content_type_uid'])

    def test_03_set_host(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp)
        self.assertEqual(7, len(self.stack.live_preview))
        self.assertEqual(True, 'enable' in self.stack.live_preview)

    def test_031_set_host_value(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp)
        self.stack.live_preview_query(live_preview_query=_lp_query)
        self.assertEqual(7, len(self.stack.live_preview))
        self.assertIsNotNone(self.stack.live_preview['host'])

    def test_06_live_preview_query(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp
        )
        self.assertEqual(7, len(self.stack.live_preview))

    def test_07_branching(self):
        stack = contentstack.Stack(
            'api_key', 'delivery_token', 'environment', branch='dev_branch')
        stack.content_type('product')
        self.assertEqual('dev_branch', stack.get_branch)

    def test_08_live_preview_query_hash_included(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp
        )
        self.stack.live_preview_query(live_preview_query=_lp_query)
        self.assertEqual(7, len(self.stack.live_preview))

    def test_09_live_preview_query_hash_excluded(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp
        )
        self.stack.live_preview_query(live_preview_query=_lp_query)
        self.stack.content_type('product').entry(entry_uid=entry_uid)
        self.assertEqual(3, len(self.stack.headers))
        self.assertEqual(True, 'access_token' in self.stack.headers)
        self.assertEqual(True, 'api_key' in self.stack.headers)

    def test_10_live_preview_check_hash_value(self):
        self.stack = contentstack.Stack(
            API_KEY,
            DELIVERY_TOKEN,
            ENVIRONMENT,
            live_preview=_lp
        )
        self.stack.live_preview_query(live_preview_query=_lp_query)
        entry = self.stack.content_type('product').entry(entry_uid=ENTRY_UID)
        resp = entry.fetch()
        print(resp)
        self.assertEqual(6, len(self.stack.headers))
        self.assertEqual(API_KEY, self.stack.headers['api_key'])
        self.assertEqual(DELIVERY_TOKEN, self.stack.headers['access_token'])
        self.assertEqual(ENVIRONMENT, self.stack.headers['environment'])


lp_response = [
    {
        "uid": "76743678743",
        "comment": "this belongs to live preview object",
        "_version": 2,
        "locale": "en-us",
        "ACL": {},
        "author": [
            {
                "uid": "77f3f0ea3630e06",
                "_content_type_uid": "author"
            }
        ]
    },
    {
        "uid": "7634767463",
        "_version": 2,
        "locale": "en-us",
        "comment": "this belongs to live preview object",
        "ACL": {},
        "author": [
            {
                "uid": "bltb77f3f0ea3630e06",
                "_content_type_uid": "author"
            }
        ]
    }
]

entry_response = [
    {
        "uid": "76743678743",
        "_version": 3,
        "locale": "en-uk",
        "title": "Updated Title",
        "comment": "this belongs to entry object",
    },
    {
        "uid": "47634767463",
        "_version": 3,
        "locale": "en-uk",
        "title": "Updated Title",
        "comment": "this belongs to entry object",
    },
    {
        "uid": "34767463",
        "_version": 3,
        "locale": "en-us",
        "comment": "this belongs to entry object",
        "title": "You have received a new merged entry response"
    }
]


class TestLivePreviewObject(unittest.TestCase):

    def setUp(self):
        self.stack = contentstack.Stack(
            API_KEY, DELIVERY_TOKEN,
            ENVIRONMENT, host=HOST)

    def test_setup_live_preview(self):
        self.stack = contentstack.Stack(API_KEY, DELIVERY_TOKEN, ENVIRONMENT, live_preview={
            'enable': False,
            'host': 'api.contentstack.io',
            'management_token': 'string987654321'
        })
        self.stack.content_type('product').entry(entry_uid)
        self.assertEqual(3, len(self.stack.get_live_preview))
        self.assertFalse(self.stack.get_live_preview['enable'])
        self.assertTrue(self.stack.get_live_preview['management_token'])

    def test_deep_merge_object(self):
        merged_response = DeepMergeMixin(entry_response, lp_response)
        self.assertTrue(isinstance(merged_response.entry_response, list))
        self.assertEqual(3, len(merged_response.entry_response))
        print(merged_response.entry_response)


if __name__ == '__main__':
    unittest.main()
