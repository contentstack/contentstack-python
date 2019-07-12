"""
 * MIT License
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
 * [ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE ]
 *
"""

import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


    # logging.basicConfig(filename='contentstack.log', format='%(asctime)s - %(message)s', level=logging.INFO)
    # logging.getLogger("Config")

    def log(message: str):
        logging.debug(message)


    def is_connected(cls):
        import socket
        try:
            host = socket.gethostbyname('cdn.contentstack.io')
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            pass
        return False


    def header_agents() -> dict:

        import contentstack
        import platform

        """
        Contentstack-User-Agent header.
        """
        header = {'sdk': {
            'name': contentstack.__package__,
            'version': contentstack.__version__
        }}
        os_name = platform.system()
        if os_name == 'Darwin':
            os_name = 'macOS'
        elif not os_name or os_name == 'Java':
            os_name = None
        elif os_name and os_name not in ['macOS', 'Windows']:
            os_name = 'Linux'
        header['os'] = {
            'name': os_name,
            'version': platform.release()
        }

        local_headers = {'X-User-Agent': header, "Content-Type": 'application/json'}
        return local_headers
