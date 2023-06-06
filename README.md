<p align="center">
  <img src="./images/cloud-droid.png">
</p>

***Cloud Droid*** is a platform designed to manage Incident and Response Simulations; you can execute controlled actions that let you test your Incident Response plan in realistic scenarios.

The main goal of ***Cloud Droid*** is to provide red teaming exercises as code, generating simulations against attack scenarios and highlighting possible failures in your incident response plan. The tests are called ***Smokers***, each one executing real actions and then cleaning up the resources created during execution.

The system is currently available for *AWS*, but it is to be extended to others cloud platforms.

### How it works?

![alt text](images/cloud-droid-diagram.png "DIAGRAM")

### How to run it?

#### Using the official Docker image:

```bash
docker run --rm \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    -e AWS_SESSION_TOKEN \
    -e AWS_DEFAULT_REGION=us-east-1 \
    cloudsniper/cloud-droid:latest -s XXXX -B XXXX
```

#### Running Docker build:

1. Build the Docker image.
```bash
docker build -t cloud-droid .
```

2. Run the container by passing your aws credentials.
```bash
docker run --rm \
    -e AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY \
    -e AWS_DEFAULT_REGION=us-east-1 \
    cloud-droid -s XXXX -b XXXX
```

#### Mandatory command options for running ***Cloud Droid***

You must use the ***-s*** option to run a ***Smoker***.

| -s  | Description  |
| :------------ |:---------------|
| **all** | Run all ***Smokers*** |
| **test** | Test Cloud Droid |
| **sg** | Create an open security group |
| **pa** | Multiple authentication failure in Palo Alto VPN portal. Must configure ***pano_url*** located in ***smoker/PanAuthSmoker.py*** |
| **au** | Create an administrator user |
| **aca** | Multiple authentication failure in AWS console. Must configure ***account_id*** located in ***smoker/awsConsoleAuthSmoker.py*** |
| **ctr** | Create a CloudTrail trail  |
| **s3p** | Create a public S3 bucket |
| **esb** | Create a public EBS snapshot. Must configure a snapshot id in ***smoker/EBSPublicSmoker*** - line27 |

#### Optional command options to run ***Cloud Droid***

| -b        | Description                       |
|-----------|-----------------------------------|
| **true**  | Store the results in an S3 bucket |
| **false** | Prints the output on the console  |

### Requirements
- Docker
- AWS Credentials
- Variable named 'BUCKETS3' to store records in S3.

### Upcoming ***Smokers***
- Kubernetes
- AWS VPC changes
- AWS EC2
- GuardDuty

### Get Involved
* [EMAIL](mailto:cloudsniper.cba@gmail.com)
* [SLACK](https://join.slack.com/t/cloudsniper/shared_invite/zt-gdto90pu-C25tsP54IOqTZd8ykQHmTw)

### Contributing
We welcome all contributions, suggestions, and feedback, so please do not hesitate to reach out. 

Ways you can contribute:
1. Report potential bugs 
2. Request a feature
3. Join our community
4. Submit a PR for open issues
5. Fix or improve documentation

### Code of Conduct

This project adheres to the Linux Foundation [Code of Conduct](https://events.linuxfoundation.org/about/code-of-conduct/) available on the event page. By participating, you are expected to honor this code.
