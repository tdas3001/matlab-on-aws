"""
Copyright 2022 The MathWorks, Inc.

Tools for populating the parameters for CF template
"""

import boto3
import confuse
import json
from requests import get
from string import Template


def read_template_parameter_file(param_file):
    """Loads the parameter json file"""

    with open(param_file) as param_file_obj:
        return json.load(param_file_obj)


def get_params_for_region(region, param_template, extra_parameters={}):
    """Takes the parameters from parameter template and updates them based on value provided in config.yaml"""

    params_for_region = next(p for p in params_per_region if p["Region"] == region)
    params_for_region.update(extra_parameters)

    for param in param_template:
        if param["ParameterKey"] == "ClientIPAddress":
            clientIPAddressValue = get("https://api.ipify.org").text + "/32"
            param["ParameterValue"] = clientIPAddressValue
        else:
            param["ParameterValue"] = Template(param["ParameterValue"]).substitute(
                params_for_region
            )

    return param_template


def get_param_value(parameters, param_key):
    return next(
        param["ParameterValue"]
        for param in parameters
        if param["ParameterKey"] == param_key
    )


def get_private_key_for_region(region):
    params_for_region = next(p for p in params_per_region if p["Region"] == region)
    return params_for_region["PrivateKeyFile"]


def get_regions():
    return [p["Region"] for p in params_per_region]


def _load_params_for_regions(config):
    """Loads the parameters for the account from the configuration file"""

    return config["Regions"].get()


# Static module data
config = confuse.Configuration("aws_refarch_tools", __name__)
params_per_region = _load_params_for_regions(config)
