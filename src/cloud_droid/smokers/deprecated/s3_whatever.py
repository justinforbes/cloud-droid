#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError

from cloud_droid.aws_smoker import AwsSmoker


class S3WhateverSmoker(AwsSmoker):
    def simulate(self):
        # Implement your function here
        pass
