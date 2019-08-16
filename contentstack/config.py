"""
 * MIT License
 *
 * Copyright (c) 2012 - 2019 Contentstack
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.

"""
import logging


logging.basicConfig(filename='cs.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger("Config")


class Config(object):
    """
    All API paths are relative to this base URL, for example, /users actually means <scheme>://<host>/<basePath>/users.

    """

    def __init__(self):

        # It initialises the Config with the default endpoint
        self.default = dict(protocol="https", host="cdn.contentstack.io", port=443, version="v3")

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

        Example:

            >>> config  = Config().host('api.contentstack.io')

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

        Example: The API version (in our case, 'v3') can be found in the URL, e.g.

            >>> config  = Config()
            >>> config.version = 'v3'

        """
        if version is not None and isinstance(version, str):
            self.default['version'] = version

        return self

    @property
    def endpoint(self):
        url = "{0}://{1}/{2}".format(self.default["protocol"], self.default["host"], self.default["version"])
        return url
