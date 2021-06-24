#!/usr/bin/python

import abc

from smoker_base import BaseSmoker


class AwsSmoker(BaseSmoker, abc.ABC):

    def __init__(self, config_file_path):
        super().__init__(config_file_path)

