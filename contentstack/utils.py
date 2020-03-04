"""
Utils
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.
"""
import logging

logging.basicConfig(
    filename='report_log.log',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
    )
logging.getLogger("Config")


def log(message):
    "this generates log message"
    logging.debug(message)
