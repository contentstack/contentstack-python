"""
contentstack.resource
~~~~~~~~~~~~~~~~~~~
"""


class Resource(object):

    def __init__(self, default_locale='en-us', **item):
        self.raw = item
        self.default_locale = default_locale

    def fields(self, locale=None):
        if locale is None:
            locale = self._locale()

    @property
    def locale(self):
        pass
