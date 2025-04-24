"""
Utility functions for logging and URL manipulation.
Last modified by ishaileshmishra on 06/08/20.
Copyright 2019 Contentstack. All rights reserved.
"""

import json
import logging
from urllib.parse import urlencode


def setup_logging(logging_type=logging.INFO, filename='app.log'):
    """
    Global one-time logging configuration.
    Should be called from your main application entry point.
    """
    logging.basicConfig(
        filename=filename,
        level=logging_type,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


class Utils:
    @staticmethod
    def setup_logger(name="AppLogger", level=logging.INFO, filename='app.log'):
        """
        Creates and configures a named logger with file and console output.
        Prevents duplicate handlers.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(level)

            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    @staticmethod
    def log(message, level=logging.DEBUG):
        """
        Log a message with the specified level.
        Default is DEBUG.
        """
        logger = logging.getLogger("AppLogger")
        logger.log(level, message)

    @staticmethod
    def do_url_encode(params):
        """
        Encode query parameters to URL-safe format.
        :param params: Dictionary of parameters
        :return: Encoded URL query string
        """
        if not isinstance(params, dict):
            raise ValueError("params must be a dictionary")
        return urlencode(params, doseq=True)

    @staticmethod
    def get_complete_url(base_url: str, params: dict, skip_encoding=False) -> str:
        """
        Construct a full URL by combining base URL and encoded parameters.
        Handles JSON stringification for the `query` key.
        :param base_url: Base API URL
        :param params: Dictionary of query parameters
        :param skip_encoding: Set True to skip URL encoding
        :return: Complete URL
        """
        if not isinstance(base_url, str) or not isinstance(params, dict):
            raise ValueError("base_url must be a string and params must be a dictionary")

        if 'query' in params and not skip_encoding:
            params["query"] = json.dumps(params["query"], separators=(',', ':'))

        if not skip_encoding:
            query_string = urlencode(params, doseq=True)
        else:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())

        # Append with appropriate separator
        return f'{base_url}&{query_string}' if '?' in base_url else f'{base_url}?{query_string}'
