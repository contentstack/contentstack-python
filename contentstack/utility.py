"""
Utils
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""

# ************* Module utility **************
# Your code has been rated at 10.00/10


import logging
import json
import urllib.parse as urlparse


def config_logging(logging_type: logging.WARNING):
    import logging
    logging.basicConfig(
        filename='application.log',
        level=logging_type,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


class Utils:
    """
    Utility for the contentstack
    """

    @staticmethod
    def config_logging():
        """ Setting up logging """
        logging.basicConfig(
            filename='report_log.log',
            format='%(asctime)s - %(message)s',
            level=logging.INFO
        )

    @staticmethod
    def setup_logger():
        """setup logger for the application"""
        return logging.getLogger("Config")

    @staticmethod
    def log(message):
        """this generates log message"""
        logging.debug(message)

    @staticmethod
    def do_url_encode(params):
        from urllib import parse
        return parse.urlencode(params)

    @staticmethod
    def get_complete_url(base_url: str, params: dict):
        if 'query' in params:
            params["query"] = json.dumps(params["query"])
        query = urlparse.urlencode(params)
        url = '{}&{}'.format(base_url, query)
        return url
