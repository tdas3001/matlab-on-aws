"""
Copyright (c) 2022 The MathWorks, Inc.

Teardown deployment for MATLAB Linux Refarch on AWS
"""

import os
import sys

import tools.deploy as deploy


def main(stack_name):
    region_name = os.environ["AWS_REGION"]
    deploy.delete_stack_by_name(region_name, stack_name)


if __name__ == "__main__":
    main(sys.argv[1])
