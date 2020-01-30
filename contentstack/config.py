import enum
import logging

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

        """Config class arguments accepts protocol, region, host and version:
        
        protocol: It support https protocol only
        region: It accepts us and eu region.
        host: host of the stack
        version: API version, contentstack support v3 API version
        
        """
        self.default = dict(protocol="https", region=ContentstackRegion.US, host="cdn.contentstack.io", version="v3")

    @property
    def region(self):

        """It sets the region in the API, We support us and eu region
        default region will be us.
        
        Returns:
            ContentstackRegion -- It returns type of ContentstackRegion
        """
        return self.default['region']

    @region.setter
    def region(self, region=ContentstackRegion.US):

        """
        A Contentstack region refers to the location of the data centers where your organization's data resides.
        
        Keyword Arguments:
            region {ContentstackRegion} -- region refers to the location of the data centers where your organization's
            data resides. (default: {ContentstackRegion.US})

        For more details: https://www.contentstack.com/docs/developers/contentstack-regions
        
        ==============================

        [Example:]

            >>> config = Config()
            >>> config.region = ContentstackRegion.US

        ==============================
        """

        if region is not None and isinstance(region, ContentstackRegion):
            if region != ContentstackRegion.US:
                if self.default["host"] == 'cdn.contentstack.io':
                    self.default["host"] = 'cdn.contentstack.com'
            self.default['region'] = region

    @property
    def host(self):

        """host property returns host of the API
        
        Returns:
            str -- host of the API
        """

        return self.default['host']

    @host.setter
    def host(self, host):

        """
        The base URL for Content Delivery API is cdn.contentstack.io.
        host is the domain name or IP address of the host that serves the API. It may include the 
        port number if different from the scheme's default
        port (443 for HTTPS).
        
        Arguments:
            host {str} -- host of the stack
        
        Returns:
            [Config] -- Config, So we can chain more functions

        ==============================
        
        [Example:] 

            >>> config  = Config()
            >>> config.host = 'cdn.contentstack.io'
        
        ==============================
        """

        if host is not None and isinstance(host, str):
            self.default['host'] = host

    def version(self, version=None):

        """
        Only version v3 is supported on the CDN.
        
        Keyword Arguments:
            version {str} -- version of the API (default: {None})
        
        Returns:
            Config -- class instance to chain the functions

        ==============================
        
        [Example:] 

            >>> config = Config()
            >>> config = config.version('v3')
        
        ==============================

        """

        if version is not None and isinstance(version, str):
            self.default['version'] = version

        return self

    @property
    def endpoint(self):

        """It returns endpoint url of the API
        The base URL for Content Delivery API for the US region is cdn.contentstack.io. and  
        for the European region it is  eu-cdn.contentstack.com
        For more details: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#base-url
        
        Returns:
            str -- endpoint url of the API

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