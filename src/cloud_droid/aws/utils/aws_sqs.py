import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


s = boto3.session.Session(region_name=os.environ['AWS_REGION'])
sqs = s.client('sqs')


def send_queue_message(queue_url, ti_feed):
    print("SQS POST", ti_feed)

    try:
        response = sqs.send_message(QueueUrl=queue_url,
                                    MessageBody=ti_feed)
    except ClientError:
        logger.exception(f'Could not send message to the - {queue_url}.')
        raise
    else:
        return response

    logger.info("Message sent")
