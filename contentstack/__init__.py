"""
The __init__.py files are required to make Python treat the directories as containing
packages; this is done to prevent directories with a common name, such as string,
from unintentionally hiding valid modules that occur later on the module search path

Used: Safety checks your installed dependencies for known security vulnerabilities
file __init__.py contains package information like
__author__, __status__, __version__, __endpoint__ and __email__

"""
from .entry import Entry
from .asset import Asset
from .contenttype import ContentType
from .https_connection import HTTPSConnection
from contentstack.stack import Stack
from .utility import Utils

__title__ = 'contentstack-python'
__author__ = 'Contentstack'
__status__ = 'debug'
__version__ = '1.5.0'
__endpoint__ = 'cdn.contentstack.io'
__email__ = 'shailesh.mishra@contentstack.com'
