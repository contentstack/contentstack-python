""" contentstack python sdk. """
import warnings

__author__ = 'Shailesh Mishra'
__status__ = 'debug'
__version__ = '1.0.0'
__package__ = 'contentstack'
__endpoint__ = 'cdn.contentstack.io'

from .entry import Entry
from .asset import Asset
from .config import Config
from .content_type import ContentType
from .errors import Error, ConfigError, FileModeWarning
from .http_connection import HTTPConnection

# Set a default logger to prevent "No handler found" warnings
# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

# FileModeWarnings go off per the default.
warnings.simplefilter('default', FileModeWarning, append=True)
