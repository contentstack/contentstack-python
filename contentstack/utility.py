"""
Utils
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""

# ************* Module utility **************
# Your code has been rated at 10.00/10


import logging


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
    def do_urlencode(params):
        from urllib import parse
        return parse.urlencode(params)
    