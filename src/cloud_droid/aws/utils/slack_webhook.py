import json
import logging
import requests

log = logging.getLogger()
log.setLevel(logging.INFO)


def message_to_slack(message, webhook_url):

    try:

        data = {
            'text': '***************************************************************\n\n'
                    + '* Starting incident simulation for: * ' + message + '\n'
                    + '***************************************************************',
            'username': 'CLOUD SNIPER BUDDY',
            'icon_emoji': ':robot_face:'
        }

        response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        log.info('Sending message to Slack. Response: ' + str(response.text) + ' Response Code: ' + str(response.status_code))

    except Exception as e:
        log.info("Message could not be send to Slack: " + str(e))