"""
Copyright (c) 2022 The MathWorks, Inc.

Set Up deployment for MATLAB Linux Refarch on AWS
"""

import boto3
import os

import tools.deploy as deploy
import tools.instances_info as instances_info


def main():
    name_prefix = "MATLABLinuxHealthCheck"
    region_name = os.environ["AWS_REGION"]
    release = os.environ["RELEASE"]
    template_url = (
        "https://matlab-on-aws.s3.amazonaws.com/"
        + release
        + "/aws-matlab-template.json"
    )
    extra_parameters = {
        "InstanceType": os.environ["INSTANCE_TYPE"],
        "Password": os.environ["REFARCH_PASSWORD"],
    }

    template_parameter_file = os.path.join(
        "parameter_files", "matlab_linux_parameter_template.json"
    )
    stack = deploy.deploy_stack(
        template_url,
        template_parameter_file,
        region_name,
        stack_base_name=name_prefix + "refArchTest",
        extra_parameters=extra_parameters,
    )


if __name__ == "__main__":
    main()
