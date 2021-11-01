#!/usr/bin/python

import abc
import logging
import datetime
import time
import yaml

LOGGER_NAME = "Cloud Droid"
DEFAULT_SLEEP_TIME = 60

class BaseSmoker(abc.ABC):
    def __init__(self, config_file_path, **kwargs):
        with open(config_file_path) as fd:
            self.config = yaml.load(fd.read(), Loader=yaml.FullLoader)
        self.sleep_time = self.config.get("sleep_time", DEFAULT_SLEEP_TIME)
        self.args = kwargs
        self.logger = logging.getLogger(f"{LOGGER_NAME}.{self.__class__.__name__}")
        self.iso_now_time = datetime.datetime.now().isoformat()

    def go_to_sleep(self):
        time.sleep(self.sleep_time)

    @abc.abstractmethod
    def simulate(self):
        pass
