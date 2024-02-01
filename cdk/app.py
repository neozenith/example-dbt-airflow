#!/usr/bin/env python3

# Third Party
import aws_cdk as cdk

# Our Libraries
from cdk.cdk_stack import CdkStack

app = cdk.App()
CdkStack(app, "CdkStack")

app.synth()
