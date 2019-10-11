import os
import sys
import enum
import logging
sys.path.insert(0, os.path.abspath('.'))

"""
Config
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

"""


logging.basicConfig(filename='report.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)


class ContentstackRegion(enum.Enum):
    US = 'us'
    EU = 'eu'


class Config(object):

    def __init__(self):

        """

        """
        self.default = dict(protocol="https", region=ContentstackRegion.US, host="cdn.contentstack.io", version="v3")

    @property
    def region(self):
        """ :returns  region of the stack """
        return self.default['region']

    @region.setter
    def region(self, region=ContentstackRegion.US):

        """
        The base URL for Content Delivery API is cdn.contentstack.io.
        default region is for ContentstackRegion is US

        :param region: Region support given for US and EU
        :return: ContentstackRegion

        ==============================

        [Example:]

        >>> config = Config()
        >>> config.region = ContentstackRegion.US

        ==============================
        """

        if region is not None and isinstance(region, ContentstackRegion):
            self.default['region'] = region


    @property
    def host(self):

        return self.default['host']

    @host.setter
    def host(self, host):

        """
        The base URL for Content Delivery API is cdn.contentstack.io.
        host is the domain name or IP address of the host that serves the API. It may include the 
        port number if different from the scheme's default
        port (443 for HTTPS).
        
        Returns:
            [Config] -- Config, So we can chain more functions

        """

        if host is not None and isinstance(host, str):
            self.default['host'] = host

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
        region = self.default['region'].value
        if region is not None:
            if region is not 'us':
                if self.default["host"] == 'cdn.contentstack.io':
                    self.default["host"] = 'cdn.contentstack.com'
                host = '{}-{}'.format(region, self.default["host"])
        return "{0}://{1}/{2}".format(self.default["protocol"], host, self.default["version"])