import os
import boto3

from ..aws_smoker_base import AwsSmoker

# import below the utils that you want, for instance
# from ..utils import aws_ec2


class S3PublicSmoker(AwsSmoker):

    # DO NOT MODIFY THIS CONSTRUCTOR
    def __init__(self):
        config_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "s3_public" + ".yaml"
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
