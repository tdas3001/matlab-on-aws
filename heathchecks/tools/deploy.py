"""
Copyright 2022 The MathWorks, Inc.

Tools for deploying/deleting the AWS stack
"""

import datetime
import boto3

import tools.config as config


def deploy_stack(
    template_url,
    template_parameter_file,
    region,
    stack_base_name="refArchTest",
    extra_parameters={},
):
    """Deploys the stack with the parameters defined in the template parameter file"""
    stack_name = _create_stack_name(stack_base_name)

    # Consumed by Teardown to delete the stack
    print("::set-output name=stack_name::" + stack_name)
    template_parameters = config.read_template_parameter_file(template_parameter_file)
    params_for_region = config.get_params_for_region(
        region, template_parameters, extra_parameters
    )

    cloudformation = boto3.resource("cloudformation", region_name=region)
    stack = cloudformation.create_stack(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=params_for_region,
        Capabilities=["CAPABILITY_IAM"],
    )

    _wait_for_create_complete(cloudformation, stack)
    stack.reload()

    return stack


def _wait_for_create_complete(cloudformation, stack):
    """Waits for stack to get created"""
    cf_client = cloudformation.meta.client
    creation_waiter = cf_client.get_waiter("stack_create_complete")
    creation_waiter.wait(StackName=stack.stack_name)


def delete_stack(stack):
    """Deletes the stack"""
    stack.delete()

    deletion_waiter = stack.meta.client.get_waiter("stack_delete_complete")
    deletion_waiter.wait(StackName=stack.stack_name)


def get_stack_by_name(stack_name, region):
    cloudformation = boto3.resource("cloudformation", region_name=region)
    return cloudformation.Stack(stack_name)


def delete_stack_by_name(region, stack_name):
    """Wrapper for deleting the stack by stack name"""
    delete_stack(get_stack_by_name(stack_name, region))


def get_stack_output_value(stack, outputKey):
    output = next(
        output for output in stack.outputs if output["OutputKey"] == outputKey
    )
    return output["OutputValue"]


def _create_stack_name(name_base):
    """Creates stack name based on date and time"""
    return name_base + "-" + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S%f")
