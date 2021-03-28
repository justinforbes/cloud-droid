#!/usr/bin/python

import boto3
import json
import logging
import datetime
import os
import gzip
import sys
from io import BytesIO
from botocore.exceptions import ClientError
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

##### define standard configurations ####

# Setup the verbose logger
logger = logging.getLogger("cloud-droid")

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

# smoker for s3 public (creation and delete)


def S3PublicSmoker():
    bucket_name = "droid-smoke-s3public-nuke"
    TAG = [
        {"Key": "Department", "Value": "security"},
        {"Key": "Program", "Value": "droid"},
        {"Key": "Purpose", "Value": "droid"},
    ]
    # Create s3 bucket
    s3 = boto3.client("s3")
    logger.info("Creating bucket named: " + bucket_name + " " + iso_now_time)
    s3_smoke = s3.create_bucket(ACL="public-read", Bucket=bucket_name)
    logger.info("detailed info creation: " + str(s3_smoke))
    # delete objects
    s3o = boto3.resource("s3")
    bucket = s3o.Bucket(bucket_name)
    bucket.objects.all().delete()
    # delete bucket now
    delete_bucket = s3.delete_bucket(Bucket=bucket_name)
    logger.info("detailed info delete: " + str(delete_bucket))
    logger.info(iso_now_time + " done!")
