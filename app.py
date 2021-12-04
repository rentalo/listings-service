#!/usr/bin/env python3
import os
from aws_cdk import core as cdk

from listings_service.listings_service_stack import ListingsServiceStack


USER_POOL_ARN = os.environ["USER_POOL_ARN"]


app = cdk.App()
ListingsServiceStack(app, "ListingsServiceStack",
                     user_pool_arn=USER_POOL_ARN,
                     env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="eu-south-1"))

app.synth()
