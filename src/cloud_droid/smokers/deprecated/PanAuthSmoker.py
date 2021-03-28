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

# ConfigureURLHERE

pano_url = "https://vpn.company.com"

# smoker for panorama auth faild


def PanAuthSmoker():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    logger.info("Testing panorama auth fail to device")
    headers = {
        "Origin": pano_url,
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "droid (Security Incident Response Automated Simulations)",
        "Referer": str(pano_url) + "/php/login.php",
    }

    data = {
        "prot": "https:",
        "server": "vpn.company.com",
        "authType": "init",
        "user": "droid-testing",
        "passwd": "droidtest",
        "challengePwd": "",
        "ok": "Log In",
    }

    logger.info(iso_now_time + " testing user: droid-testing")
    time.sleep(5)
    response = requests.post(
        pano_url + "/php/login.php", headers=headers, data=data, verify=False
    )
    logger.info(" this is going to take a while ...")
    time.sleep(5)
    response = requests.post(
        pano_url + "/php/login.php", headers=headers, data=data, verify=False
    )
    time.sleep(5)
    response = requests.post(
        pano_url + "/php/login.php", headers=headers, data=data, verify=False
    )
    logger.info(" working....")
    time.sleep(5)
    response = requests.post(
        pano_url + "/php/login.php", headers=headers, data=data, verify=False
    )
    time.sleep(5)
    response = requests.post(
        pano_url + "/php/login.php", headers=headers, data=data, verify=False
    )
    logger.info(iso_now_time + " done!")
