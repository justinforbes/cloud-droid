#!/usr/bin/python

import abc
import logging
import datetime
import yaml

LOGGER_NAME = "Cloud Droid"


class BaseSmoker(abc.ABC):
    def __init__(self, config_file_path, **kwargs):
        with open(config_file_path) as fd:
            self.config = yaml.load(fd.read(), Loader=yaml.FullLoader)
        self.args = kwargs
        self.logger = logging.getLogger(f"{LOGGER_NAME}.{self.__class__.__name__}")
        self.iso_now_time = datetime.datetime.now().isoformat()

    @abc.abstractmethod
    def simulate(self):
        pass
