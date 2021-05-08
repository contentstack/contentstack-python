import unittest

import config
import contentstack


class TestConfig(unittest.TestCase):

    def setup(self):
        stack = contentstack.Stack(config.api_key, config.delivery_token,
                                   config.environment, host=config.host, branch='development')
        self.assertEqual('development', stack.branch)
