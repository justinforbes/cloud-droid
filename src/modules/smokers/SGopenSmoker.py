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
logger = logging.getLogger('cloud-droid')

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

# smoker for security open group


def SGopenSmoker():
    TAG = [
        {"Key": "Department", "Value": "security"},
        {"Key": "Program", "Value": "droid"},
        {"Key": "Purpose", "Value": "droid"}
    ]
    descript = ' droid smoke security group ' + iso_now_time
    name = ' droid_smoke_group'
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    try:
        response = ec2.create_security_group(GroupName=name,
                                             Description=descript,
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        logger.info(' Security Group Created %s in vpc %s.' %
                    (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ], )
        logger.info(' Ingress Successfully Set %s' % data)
    except ClientError as e:
        logger.info(e)
    try:
        response = ec2.delete_security_group(GroupId=security_group_id)
        logger.info(' Security Group Deleted')
    except ClientError as e:
        logger.info(e)
