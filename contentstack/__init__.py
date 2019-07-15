""" contentstack python sdk. """

__author__ = 'Shailesh Mishra'
__status__ = 'debug'
__version__ = '1.0.0'
__package__ = 'contentstack'
__endpoint__ = 'cdn.contentstack.io'

# from .stack import Stack
from .entry import Entry
from .asset import Asset
from .asset_library import AssetLibrary
from .config import Config
from .content_type import ContentType
from .errors import Error, ConfigError
from .group import Group
from .http_request import HTTPRequestConnection


# Set a default logger to prevent "No handler found" warnings
import logging
try:  # Python >=2.7
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())



