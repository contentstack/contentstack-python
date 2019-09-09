#  Utils
#  contentstack
#
#  Created by Shailesh Mishra on 22/06/19.
#  Copyright © 2019 Contentstack. All rights reserved.

import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.basicConfig(filename='contentstack.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.getLogger("Config")


def log(message: str):
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




