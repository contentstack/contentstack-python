"""
Utils
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""
import logging


class Utils(object):

    @staticmethod
    def configLogging():
        """ Setting up logging """
        logging.basicConfig(
            filename='report_log.log',
            format='%(asctime)s - %(message)s',
            level=logging.INFO
        )

    @staticmethod
    def setupLogger():
        """setup logger for the application"""
        return logging.getLogger("Config")

    @staticmethod
    def log(message):
        """this generates log message"""
        logging.debug(message)
