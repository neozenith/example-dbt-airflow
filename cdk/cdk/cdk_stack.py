#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#

#!/usr/bin/env python3
import os
from aws_cdk import core

from mwaairflow.mwaairflow_stack import MWAAirflowStack
# https://github.com/aws-samples/cdk-amazon-mwaa-cicd/blob/main/app.py
app = core.App()
MWAAirflowStack(
    app,
    "MWAAirflowStack",
    env=core.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)