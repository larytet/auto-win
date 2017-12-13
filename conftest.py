#
#

import pytest
import os
from collections import namedtuple
import re


def pytest_addoption(parser):
    # TODO add --kernels specify a file containing list of kernels
     
    #TODO More choices: check_environment, dry_run, install 
    parser.addoption("--iso", 
                     action="append", 
                     type="string",
                     dest="iso",
                     default=None,
                     metavar="ISO",
                     help="ISO file or url for download. This option can be used more than once")

    parser.addoption("--os", 
                     action="append", 
                     type="string",
                     dest="target",
                     metavar="TARGET",
                     default=['win8:64'],
                     choices=['win8:64', 'win10:64', 'win8', 'win10', "win8:32", "win10:32"],
                     help="Target OS. This option can be used more than once")
    
TargetPlatform = namedtuple('TargetPlatform', ['os', 'architecture'])
target_platforms = []
    
def pytest_configure(config):
    iso_path = config.getoption("--iso")
    if iso_path:
        print(f"Using ISO {iso_path}")

    for target_name in config.getoption("--os"):
        target_name = target_name.lower().strip()
        if ":" in target_name:
            os, architecture = target_name.split(":")
        else:
            architecture = "64"
            os = target_name
        assert(architecture in ["32", "64"])
        assert(os in ["win8", "win10"])
        target_platforms.append(TargetPlatform(os, architecture))

@pytest.fixture
def target_os(request):
        return target_platforms
    