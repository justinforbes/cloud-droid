import boto3
import os
import json
import logging
from datetime import date, datetime
from jinja2 import Template

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

s = boto3.session.Session(region_name=os.environ['AWS_REGION'])

r_ec2 = s.resource('ec2')
ec2 = s.client('ec2')
sts = s.client('sts')


def create_sg():

    security_group = r_ec2.create_security_group(
        Description='ir-automation-test',
        GroupName='ir-automation-test',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ir-automation-test'
                    },
                ]
            },
        ],
    )

    security_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=22,
        ToPort=22,
        IpProtocol='tcp',
    )

    sg_id = security_group.id
    logger.info(f'Security Group {sg_id} has been created')
    return sg_id


def delete_sg(sg_id):
    security_group = r_ec2.SecurityGroup(sg_id)
    security_group.delete()
    logger.info(f'Security Group {sg_id} has been deleted')


def create_ec2_instance(sg_id):

    ec2_instance = r_ec2.create_instances(
        ImageId='ami-02e136e904f3da870', # Amazon Linux 2
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',

        SecurityGroupIds=[
            sg_id,
        ],

        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Owner',
                        'Value': 'team-security'
                    },
                    {
                        'Key': 'Department',
                        'Value': 'security'
                    },
                    {
                        'Key': 'Partner',
                        'Value': 'asapp'
                    },
                    {
                        'Key': 'ComplianceScope',
                        'Value': 'none'
                    },
                    {
                        'Key': 'Environment',
                        'Value': 'sandbox'
                    },
                    {
                        'Key': 'Name',
                        'Value': 'amazon-linux-ir-automation-test'
                    },
                ]
            },
        ],
    )

    instance_id = ec2_instance[0].id
    logger.info(f'Instance {instance_id} has been created')
    return instance_id


def describe_ec2_instance(ec2_id):

    def json_datetime_serializer(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    response = ec2.describe_instances(
        InstanceIds=[
            ec2_id,
        ],
    )

    logger.info(f'Processing {ec2_id} attributes:')

    for reservation in response['Reservations']:

        ec2_attributes = (json.dumps(
                reservation,
                default=json_datetime_serializer,
                indent=4
            )
        )
        ec2_attributes_dict = json.loads(ec2_attributes)

    return ec2_attributes_dict


def delete_ec2_instance(ec2_id):
    instance = r_ec2.instances.filter(
        InstanceIds=[
            ec2_id,
        ],
    )
    instance.terminate()
    logger.info(f'Instance {ec2_id} deleted')


def render_template(ec2_attributes_dict):

    template = """ 
    {
        "detail": {
            "schemaVersion": "2.0",
            "accountId": "{{account_id}}",
            "region": "{{region}}",
            "partition": "aws",
            "id": "96bc45904630a733b7086e775e3e4c74",
            "type": "{{ttp}}",
            "resource": {
                "resourceType": "Instance",
                "instanceDetails": {
                    "instanceId": "{{instance_id}}",
                    "instanceType": "m3.xlarge",
                    "launchTime": "2016-08-02T02:05:06Z",
                    "networkInterfaces": [{
                        "networkInterfaceId": "eni-bfcffe88",
                        "privateIpAddress": "10.0.0.1",
                        "privateIpAddresses": [{
                            "privateDnsName": "GeneratedFindingPrivateName",
                            "privateIpAddress": "10.0.0.1"
                        }],
                        "subnetId": "{{subnet_id}}",
                        "vpcId": "{{vpc_id}}",
                        "securityGroups": [{
                            "groupName": "{{sg_name}}",
                            "groupId": "{{sg_id}}"
                        }],
                        "publicIp": "98.51.100.0"
                    }],
                    "tags": [{
                            "key": "{{tag_key}}",
                            "value": "{{tag_value}}"
                        }
                    ],
                    "instanceState": "running",
                    "imageId": "ami-99999999",
                    "imageDescription": "GeneratedFindingInstaceImageDescription"
                }
            },
            "service": {
                "serviceName": "guardduty",
                "detectorId": "c6bc4590070c5c63ecaade1eebbb83f0",
                "action": {
                    "actionType": "NETWORK_CONNECTION",
                    "networkConnectionAction": {
                        "connectionDirection": "INBOUND",
                        "localIpDetails": {
                            "ipAddressV4": "10.0.0.23"
                        },
                        "remoteIpDetails": {
                            "ipAddressV4": "{{src_ip}}",
                            "organization": {
                                "asn": "{{asn}}",
                                "asnOrg": "{{asn_org}}",
                                "isp": "{{isp}}",
                                "org": "{{org}}"
                            },
                            "country": {
                                "countryName": "{{country}}"
                            },
                            "city": {
                                "cityName": "{{city}}"
                            },
                            "geoLocation": {
                                "lat": 0,
                                "lon": 0
                            }
                        },
                        "remotePortDetails": {
                            "port": 32794,
                            "portName": "Unknown"
                        },
                        "localPortDetails": {
                            "port": 22,
                            "portName": "SSH"
                        },
                        "protocol": "TCP",
                        "blocked": false
                    }
                },
                "resourceRole": "TARGET",
                "additionalInfo": {
                    "sample": true
                },
                "eventFirstSeen": "{{event_first_seen}}",
                "eventLastSeen": "2021-04-01T01:51:09.409Z",
                "count": {{hits}}
            },
            "severity": 2,
            "createdAt": "2021-04-01T01:51:09.409Z",
            "updatedAt": "2021-04-01T01:51:09.409Z",
            "title": "18.51.100.0 is performing SSH brute force attacks against i-99999999.",
            "description": "18.51.100.0 is performing SSH brute force attacks against i-99999999. Brute force attacks are used to gain unauthorized access to your instance by guessing the SSH password."
        }
    } 
    """

    data = {
        "ttp": "UnauthorizedAccess:EC2/SSHBruteForce",
        "hits": "734",
        "account_id": str(sts.get_caller_identity()["Account"]),
        "region": str(s.region_name),
        "subnet_id": str(ec2_attributes_dict['Instances'][0]['SubnetId']),
        "src_ip": "111.164.189.99",
        "instance_id": str(ec2_attributes_dict['Instances'][0]['InstanceId']),
        "country": "China",
        "city": "Tianjin",
        "asn_org": "CHINA UNICOM China169 Backbone",
        "org": "China Unicom Liaoning",
        "isp": "China Unicom Liaoning",
        "asn": "4837",
        "vpc_id": str(ec2_attributes_dict['Instances'][0]['VpcId']),
        "sg_name": str(ec2_attributes_dict['Instances'][0]['SecurityGroups'][0]['GroupName']),
        "sg_id": str(ec2_attributes_dict['Instances'][0]['SecurityGroups'][0]['GroupId']),
        "tag_key": "TTE",
        "tag_value": "Automation testing",
        "event_first_seen": "2021-04-01T01:51:09.409Z",
    }

    j2_template = Template(template)
    ti_feed = j2_template.render(data)
    logger.info("Render generated")
    return ti_feed