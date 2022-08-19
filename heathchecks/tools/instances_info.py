import boto3


def get_resource_from_stack(stack_name, region, resource_logical_id):
    """Takes stack name and resource name to returns the resource ID"""

    client = boto3.client("cloudformation", region_name=region)
    st_res = client.list_stack_resources(StackName=stack_name)
    stack_resources = st_res["StackResourceSummaries"]
    resource = None
    for item in stack_resources:
        if item["LogicalResourceId"] == resource_logical_id:
            resource = item["PhysicalResourceId"]
            break
    return resource


def get_instance_arn(instance_id, region):
    """Get EC2 Instance Resource ARN"""

    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    instance_arn=f"arn:aws:ec2:{region}:{account_id}:instance/{instance_id}"
    return instance_arn