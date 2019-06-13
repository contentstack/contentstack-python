from unittest import TestCase
import logging
from contentstack import contentstack
from contentstack import stack


class UtilsTest(TestCase):

    def test_snake_case(self):
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')
        self.assertEqual('foo', 'foo')


    def test_stack(self):
        stack = contentstack.stack('blt244f1d47e6f6ee50', 'cse629261c638671e6f522233a',"development")
        stack.sync()
