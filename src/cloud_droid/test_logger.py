#!/usr/bin/python

import logging

logger = logging.getLogger("Cloud Droid")
log_format = (
    "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
)
log_date_format = "%m/%d/%Y %I:%M:%S %p"
logFormatter = logging.Formatter(log_format)


def test_message():
    logger.warning("Droid S3 logging test")
    logger.warning("This is a WARNING level message")
    logger.error("oops! This is a test ERROR message, don't worry")
    logger.info("This is a INFO level message")
    return 0
