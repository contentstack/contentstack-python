import unittest

import config
import contentstack


class TestConfig(unittest.TestCase):

    def setup(self):
        stack = contentstack.Stack(config.api_key, config.delivery_token,
                                   config.environment, host=config.host, branch='development')
        self.assertEqual('development', stack.branch)

    def test_branch_variable(self):
        stack = contentstack.Stack(config.api_key, config.delivery_token,
                                   config.environment, host=config.host, branch='development')
        self.assertEqual('development', stack.branch)

    def test_branching_header_branch_is_avail(self):
        stack = contentstack.Stack(config.api_key, config.delivery_token,
                                   config.environment, host=config.host, branch='development')
        self.assertTrue('branch' in stack.headers)

    def test_branching_header_branch_key(self):
        stack = contentstack.Stack(config.api_key, config.delivery_token,
                                   config.environment, host=config.host, branch='development')
        self.assertEquals('development', stack.headers['branch'])
