import json
import logging
import requests

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def message_to_slack(message, webhook_url):

    try:

        data = {
            'text': '***************************************************************\n\n'
                    + '*Starting incident response simulation for:* ' + message + '\n'
                    + '***************************************************************',
            'username': 'cloud-droid automation',
            'icon_emoji': ':robot_face:'
        }

        response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        logger.info('Sending message to Slack. Response: ' + str(response.text) + ' Response Code: ' + str(response.status_code))

    except Exception as e:
        logger.error("Message could not be send to Slack: " + str(e))