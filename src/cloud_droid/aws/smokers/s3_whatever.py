import boto3

from ..aws_smoker_base import AwsSmoker
from .. import aws_utils as utils


class s3_whateverSmoker(AwsSmoker):

    def simulate(self):
        # Implement your function here
        print("I'm smoking, don't bother me")