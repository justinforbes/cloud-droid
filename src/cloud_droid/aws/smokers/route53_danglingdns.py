import os
import boto3

from ..aws_smoker_base import AwsSmoker
from .. import aws_utils as utils


class Route53DanglingdnsSmoker(AwsSmoker):

    # DO NOT MODIFY THIS CONSTRUCTOR
    def __init__(self):
        config_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "route53_danglingdns" + ".yaml"
        )
        super().__init__(config_file_path)

    # MODIFY THIS FUNCTION IMPLEMENTATION
    def simulate(self):
        # Implement your function here
        print("I'm smoking, don't bother me")
        # This way you can read your config variables
        my_variable = self.config["my_variable"]
        print(f"my_variable = {my_variable}")
        print()