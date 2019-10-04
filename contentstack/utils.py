"""
Utils
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

"""

import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.basicConfig(filename='report_log.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger("Config")


def log(message):
    logging.debug(message)


def is_connected():
    import socket
    try:
        host = socket.gethostbyname('cdn.contentstack.io')
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        return False