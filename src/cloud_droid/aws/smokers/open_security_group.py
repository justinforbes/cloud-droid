import os
import sys
import logging
import boto3
import datetime
from botocore.exceptions import ClientError

from ..aws_smoker_base import AwsSmoker

# import below the utils that you want, for instance
# from ..utils import aws_ec2

logging.basicConfig(stream=sys.stdout,
                    format="%(asctime)s;%(levelname)s;%(message)s")
log = logging.getLogger("open_security_group")
log.setLevel(logging.INFO)


class OpenSecurityGroupSmoker(AwsSmoker):

    # DO NOT MODIFY THIS CONSTRUCTOR
    def __init__(self):
        config_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "open_security_group" + ".yaml"
        )
        super().__init__(config_file_path)

    # MODIFY THIS FUNCTION IMPLEMENTATION
    def simulate(self):
        # Implement your function here
        descript = 'droid smoke security group ' + datetime.datetime.now().isoformat()
        name = 'droid_smoke_group'
        ec2 = boto3.client('ec2')
        response = ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        try:
            response = ec2.create_security_group(GroupName=name,
                                                Description=descript,
                                                VpcId=vpc_id)
            security_group_id = response['GroupId']
            log.info('security group created %s in vpc %s.' %
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
            log.info('ingress successfully set %s' % data)
        except ClientError as e:
            log.error(e)
        try:
            response = ec2.delete_security_group(GroupId=security_group_id)
            log.info('security group deleted')
        except ClientError as e:
            log.error(e)