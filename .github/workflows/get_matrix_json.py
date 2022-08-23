# Copyright (c) 2022 The MathWorks, Inc
# Get Strategy matrix for every week to use in GitHub Worflow
from collections import OrderedDict
from datetime import date
import json
import os
import re

# Dictionary of configurations to be used for every run
# Latest Releases are dynamically picked up from the repository
config_filepath = os.path.join(os.path.dirname(__file__), "config.json")
config = dict()
with open(config_filepath) as file_obj:
    config = json.load(file_obj)

# Get latest releases in ascending order
latest_releases = [x[0] for x in os.walk("releases")]
latest_releases = list(filter(re.compile("^releases/").match, latest_releases))
latest_releases = [x.lstrip("releases/") for x in latest_releases]
latest_releases.sort(reverse=True)

# Add a key containing the last 2 matlab releases
config.update({"release": latest_releases[:2]})

# print the output to be consumed by github workflow
print("::set-output name=matrix::" + json.dumps(config))
