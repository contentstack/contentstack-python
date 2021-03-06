"""
Utils
contentstack
Last modified by Shailesh Mishra on 06/08/20.
Copyright 2019 Contentstack. All rights reserved.
"""

# ************* Module utility checked using pylint **************
# Your code has been rated at 10.00/10

import json
import logging
from urllib import parse

log = logging.getLogger(__name__)


def config_logging(logging_type: logging.WARNING):
    """
    This is to create logging config
    :param logging_type:  Level of the logging
    :return: basicConfig instance
    """
    logging.basicConfig(
        filename='app.log',
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
        """
        To encode url with query parameters
        :param params:
        :return: encoded url
        """
        return parse.urlencode(params)

    @staticmethod
    def get_complete_url(base_url: str, params: dict):
        """
        creates complete url using base_url and their respective parameters
        :param base_url:
        :param params:
        :return:
        """
        if 'query' in params:
            params["query"] = json.dumps(params["query"])
        query = parse.urlencode(params)
        return '{}&{}'.format(base_url, query)
