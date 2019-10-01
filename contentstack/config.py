"""
Config
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

"""

import logging
import enum

logging.basicConfig(filename='report.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)


class ContentstackRegion(enum.Enum):
    US = 'us'
    EU = 'eu'


class Config(object):

    def __init__(self):
        self.default = dict(protocol="https", region=ContentstackRegion.US, host="cdn.contentstack.io", version="v3")

    def region(self, region=ContentstackRegion.US):

        """
        The base URL for Content Delivery API is cdn.contentstack.io.
        default region is for ContentstackRegion is US
        :param region: ContentstackRegion
        :return: self
        ==============================
        [Example:]
        >>> config  = Config().region(region=ContentstackRegion.US)
        ==============================
        """

        if region is not None and isinstance(region, ContentstackRegion):
            self.default['region'] = region
        return self

    def host(self, host):

        """
        The base URL for Content Delivery API is cdn.contentstack.io.
        host is the domain name or IP address (
        IPv4) of the host that serves the API. It may include the port number if different from the scheme's default
        port (443 for HTTPS).

        Note: contentstack supports HTTPS only
        :param host: host is the domain name
        :type host: str
        :return: self
        :rtype: Config

        ==============================
        [Example:]
        >>> config  = Config().host('api.contentstack.io')
        ==============================
        """

        if host is not None and isinstance(host, str):
            self.default['host'] = host
        return self

    def version(self, version=None):

        """
        Note: Only version 3 is supported on the CDN. If you're still using version 2 (which we recommend you should
        not), switch to the CDN version for even faster loading.
        :param version: The API version can be found in the URL that is basePath
        :type version: str
        :return: self
        :rtype: Config
        ==============================
        [Example:] The API version (in our case, 'v3') can be found in the URL

        >>> config  = Config()
        >>> config.version = 'v3'
        ==============================
        """

        if version is not None and isinstance(version, str):
            self.default['version'] = version

        return self

    @property
    def endpoint(self):

        """
        :return: url endpoint to make Http requst
        """
        return self.__get_url()

    def __get_url(self):
        host = self.default["host"]
        if self.default['region'] is not ContentstackRegion.US:
            if self.default["host"] == 'cdn.contentstack.io':
                self.default["host"] = 'cdn.contentstack.com'
            else:
                regional_host = str(self.default['region'].value)
                host = '{}-{}'.format(regional_host, self.default["host"])
        return "{0}://{1}/{2}".format(self.default["protocol"], host, self.default["version"])
