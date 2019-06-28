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
 *
 """

import logging


class Config:

    def __init__(self, host_url: str = 'cdn.contentstack.io'):
        self.host_url = host_url
        self.api_version: str = 'v3'
        self.http_protocol: str = 'https://'

    def set_host(self, host_url=None):
        logging.info("set host", host_url)
        self.host_url = host_url
        return self

    def get_host(self):
        logging.info('getting host url', self.host_url)
        return self.host_url

    def get_version(self):
        logging.info('getting api version', self.api_version)
        return self.api_version

    def get_http_protocol(self):
        logging.info('get http protocol', self.http_protocol)
        return self.http_protocol

    def get_endpoint(self, url_path):
        api_version: str = self.get_version()
        host_url = self.get_host()
        http_protocol = self.get_http_protocol()
        config_url = "{0}{1}/{2}/{3}".format(http_protocol, host_url, api_version, url_path)
        return config_url
