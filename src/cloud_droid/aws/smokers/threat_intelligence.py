import os

from ..aws_smoker_base import AwsSmoker

# import below the utils that you want, for instance
from ..utils import aws_ec2 as ec2_utils
from ..utils import aws_sqs as sqs_utils
from ..utils import slack_webhook as slack_webhook


class ThreatIntelligenceSmoker(AwsSmoker):

    # DO NOT MODIFY THIS CONSTRUCTOR
    def __init__(self):
        config_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "threat_intelligence" + ".yaml"
        )
        super().__init__(config_file_path)


    # MODIFY THIS FUNCTION IMPLEMENTATION
    def simulate(self):
        '''
        9. remove hardcoded queue + webhook
        '''

        slack_webhook.message_to_slack("TI feeds", self.config.get("webhook_url"))

        sg_id = ec2_utils.create_sg()
        instance_id = ec2_utils.create_ec2_instance(sg_id)
        self.go_to_sleep()

        ec2_attributes_dict = ec2_utils.describe_ec2_instance(instance_id)
        ti_feed = ec2_utils.render_template(ec2_attributes_dict)
        sqs_utils.send_queue_message(self.config.get("queue_url"), ti_feed)
        self.go_to_sleep()

        ec2_utils.delete_ec2_instance(instance_id)
        self.go_to_sleep()

        ec2_utils.delete_sg(sg_id)

