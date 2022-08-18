# Copyright (c) 2022 The MathWorks, Inc
# Get Strategy matrix for every week to use in GitHub Worflow
from collections import OrderedDict
from datetime import date
import json
import os
import re

# Set the initial date to 1st August 2022 (Monday) in YYYY,MM,DD format
date1 = date(2022, 8, 1)
date2 = date.today()
days = abs(date2 - date1).days

# // = floor division operator
# Count number of weeks
no_of_weeks = days // 7

# Dictionary of configurations to be used for every run
# Latest Releases are directly picked up from the repository
config_filepath = os.path.join(os.path.dirname(__file__), "config.json")
config = OrderedDict()
with open(config_filepath) as file_obj:
    config = json.load(file_obj)

# Get latest releases in ascending order
latest_releases = [x[0] for x in os.walk("releases")]
latest_releases = list(filter(re.compile("^releases/").match, latest_releases))
latest_releases = [x.lstrip("releases/") for x in latest_releases]
latest_releases.sort(reverse=True)

# Add a key for matlab releases
config.update({"release": latest_releases[:2]})

# Total number of combination of configurations
total_combinations = 1
for key in config.keys():
    total_combinations *= len(config[key])

# Get the iteration number for current week
# Repeat the iteration if the count of weeeks exceeds total combinations possible
iteration_no = no_of_weeks % total_combinations

# Map a different configuration each week
weekly_map = OrderedDict()
for key, value in config.items():
    weekly_map[key] = [value[int(iteration_no % len(value))]]
    iteration_no = iteration_no / len(value)

# print the output to be consumed by github workflow
print("::set-output name=matrix::" + json.dumps(weekly_map))
