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

# smoker for cloudtrail (creation and delete)


def CTrailSmoker():
    name = "droid_smoke_cloudtrail"
    bucket_name = "droid-smoke-cloudtrail"
    TAG = [
        {"Key": "Department", "Value": "security"},
        {"Key": "Program", "Value": "droid"},
        {"Key": "Purpose", "Value": "droid"},
    ]
    # policy for bucket
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": "arn:aws:s3:::droid-smoke-cloudtrail",
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::droid-smoke-cloudtrail/*",
                "Condition": {
                    "StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}
                },
            },
        ],
    }
    # Create s3 bucket
    s3 = boto3.client("s3")
    logger.info("Creating bucket named: " + bucket_name + " " + iso_now_time)
    s3_smoke = s3.create_bucket(ACL="private", Bucket=bucket_name)
    # set bucketpolicy
    bucket_policy = json.dumps(policy)
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    # Create cloudtrial
    logger.info("Creating cloudtrail named: " + name + " " + iso_now_time)
    client = boto3.client("cloudtrail")
    response = client.create_trail(Name=name, S3BucketName=bucket_name)
    logger.info("detailed info: " + str(response))
    logger.info("Starting the trail: " + iso_now_time)
    response = client.start_logging(Name=name)
    logger.info("detailed info: " + str(response))
    logger.info(" Deleting trail now %s" % iso_now_time)
    response = client.delete_trail(Name=name)
    logger.info("detailed info: " + str(response))
    logger.info(" Deleting s3 now %s" % iso_now_time)
    # delete objects
    s3o = boto3.resource("s3")
    bucket = s3o.Bucket(bucket_name)
    bucket.objects.all().delete()
    # delete bucket now
    delete_bucket = s3.delete_bucket(Bucket=bucket_name)
    logger.info("detailed info: " + str(delete_bucket))
    logger.info(iso_now_time + " done!")
