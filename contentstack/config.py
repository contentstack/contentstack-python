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


class Config:

    def __init__(self):
        self.default_config = dict(protocol="https", host="cdn.contentstack.io", port=443, version="v3", urls={
            "sync": "/stacks/sync",
            "content_types": "/content_types/",
            "entries": "/entries/",
            "assets": "/assets/",
            "environments": "/environments/"
        })

    def host(self, host_url=None):
        if host_url is not None:
            self.default_config["host"] = host_url
        return self.default_config["host"]

    def version(self):
        return self.default_config["host"]

    def protocol(self):
        return self.default_config["protocol"]

    def get_endpoint(self, url_path):
        config_url = "{0}{1}/{2}/{3}".format(self.protocol(), self.host(), self.version(), url_path)
        return config_url

    def hiShailesh(self):
        print("Something")


config = Config()
host = config.host("stag-cdn.contentstack.io")
print(host)

