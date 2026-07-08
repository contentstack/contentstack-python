"""
The __init__.py files are required to make Python treat the directories as containing
packages; this is done to prevent directories with a common name, such as string,
from unintentionally hiding valid modules that occur later on the module search path
"""
from .entry import Entry
from .asset import Asset
from .contenttype import ContentType
from .endpoint import Endpoint
from .https_connection import HTTPSConnection
from contentstack.stack import Stack
from .utility import Utils
from .region_refresh import refresh_regions

__all__ = (
"Entry",
"Asset",
"ContentType",
"Endpoint",
"HTTPSConnection",
"Stack",
"Utils",
"refresh_regions",
)


def get_contentstack_endpoint(region='us', service='', omit_https=False):
    """
    Resolve a Contentstack service endpoint URL for a given region.

    Proxy to :class:`Endpoint.get_contentstack_endpoint` for convenience —
    mirrors ``Contentstack::getContentstackEndpoint()`` in the PHP SDK.

    :param region: Region ID or alias ('us', 'eu', 'azure-na', 'gcp-eu', ...).
    :param service: Service key ('contentDelivery', 'contentManagement', ...).
                    When empty, returns a dict of all endpoints for the region.
    :param omit_https: When True, strips 'https://' from the returned URL(s).
    :returns: str when service is provided, dict[str,str] otherwise.
    """
    return Endpoint.get_contentstack_endpoint(region, service, omit_https)

__title__ = 'contentstack-delivery-python'
__author__ = 'contentstack'
__status__ = 'debug'
__version__ = 'v2.6.1'
__endpoint__ = 'cdn.contentstack.io'
__email__ = 'support@contentstack.com'
__developer_email__ = 'mobile@contentstack.com'
__license__ = "MIT"
