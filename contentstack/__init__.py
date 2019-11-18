
"""
__init__.py
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""

import warnings

__author__ = 'Contentstack'
__status__ = 'debug'
__version__ = '0.1.0'
__package__ = 'contentstack'
__endpoint__ = 'cdn.contentstack.io'
__email__ = "mobile@contentstack.com"

from .entry import Entry
from .asset import Asset
from .config import Config
from .content_type import ContentType
from .errors import Error, FileModeWarning
from .http_connection import HTTPConnection
from .stack import Stack

import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())
warnings.simplefilter('default', FileModeWarning, append=True)
