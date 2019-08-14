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


logging.basicConfig(filename='contentstack.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger("Config")


class Config:

    def __init__(self):
        self.defaultConfig = dict(protocol="https:/",
                                  host="cdn.contentstack.io",
                                  port=443,
                                  version="v3",
                                  path={
                                      "stacks": "stacks",
                                      "sync": "stacks/sync",
                                      "content_types": "content_types",
                                      "entries": "content_types",
                                      "assets": "assets",
                                      "environments": "environments"
                                  })

    def host(self, host_url=None):
        if host_url is not None and isinstance(host_url, str):
            self.defaultConfig['host'] = host_url
        return self.defaultConfig['host']

    def version(self, version=None):
        if version is not None and isinstance(version, str):
            self.defaultConfig['version'] = version
            return self.defaultConfig['version']
        else:
            return self.defaultConfig['version']

    def path(self, path):
        url_section = self.defaultConfig['path']
        if path in url_section:
            return url_section[path]
        else:
            logging.error("{0} is invalid endpoint path".format(path))
            raise Exception('Invalid endpoint!!, {0} is invalid endpoint path, Path can be found among {1}'
                            .format(path, url_section.keys()))

    @property
    def default_endpoint(self):
        endpoint_url = "{0}/{1}/{2}".format(self.defaultConfig["protocol"], self.host(), self.version())
        return endpoint_url

    def endpoint(self, path):
        url = self.path(path)
        if url is not None and isinstance(url, str):
            url = "{0}/{1}/{2}/{3}".format(self.defaultConfig["protocol"], self.host(), self.version(), url)
            logging.info('endpoint is :: {0} '.format(url))

        return url


# config = Config()
# config.host("stag-cdn.contentstack.io")
# result_url = config.endpoint('assets')
# print(result_url)

