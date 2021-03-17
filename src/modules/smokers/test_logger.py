#!/usr/bin/python

import logging

logger = logging.getLogger('cloud-droid')
log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
log_date_format = "%m/%d/%Y %I:%M:%S %p"
logFormatter = logging.Formatter(log_format)


def test_message():
    logger.warning("Testing test for loggin s3 droid")
    logger.warning("other message to be more fancy")
    logger.error("ups this is a test ERROR message not worries")
    logger.info("Im done, this is a info level message")
    return 0
