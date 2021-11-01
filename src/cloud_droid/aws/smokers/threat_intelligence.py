import os
import time
from ..utils.aws_ec2_utils import create_sg
from ..utils.aws_ec2_utils import create_ec2_instance
from ..utils.aws_ec2_utils import describe_ec2_instance
from ..utils.aws_ec2_utils import render_template
from ..utils.aws_ec2_utils import delete_ec2_instance
from ..utils.aws_ec2_utils import delete_sg
from ..utils.aws_sqs_utils import send_queue_message


class ThreatIntelligenceSmoker(AwsSmoker):

    # DO NOT MODIFY THIS CONSTRUCTOR
    def __init__(self):
        config_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "route53_danglingdns" + ".yaml"
        )
        super().__init__(config_file_path)


    # MODIFY THIS FUNCTION IMPLEMENTATION
    def simulate(self):
        '''
        8. add weebhook
        9. remove hardcoded queue
        10. add logging
        '''

        queue_url = "https://sqs.us-east-1.amazonaws.com/BLABLA/test-automation"

        sg_id = create_sg()
        instance_id = create_ec2_instance(sg_id)
        time.sleep(20)
        ec2_attributes_dict = describe_ec2_instance(instance_id)
        ti_feed = render_template(ec2_attributes_dict)
        delete_ec2_instance(instance_id)
        time.sleep(60)
        delete_sg(sg_id)
        send_queue_message(queue_url,ti_feed)