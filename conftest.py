#
#

import pytest
import os
from collections import namedtuple


def pytest_addoption(parser):

    parser.addoption("--os", 
                     action="append", 
                     type="string",
                     dest="target",
                     metavar="TARGET",
                     default=[],
                     choices=['win8:64', 'win10:64', 'win8', 'win10', "win8:32", "win10:32"],
                     help="Target OS. This option can be used more than once")
    
    parser.addoption("--iso", 
                     action="append", 
                     type="string",
                     dest="iso",
                     default=None,
                     metavar="ISO",
                     help="ISO file for installation of missing operating systems. ISOs should be specified in the same order as --os. This option can be used more than once")

    parser.addoption("--cleanall", 
                     action="store_true", 
                     default=False,
                     help="Start from scratch: remove all VMs")
    
    parser.addoption("--headless_vms", 
                     action="store_true", 
                     default=False,
                     help="Start VMs headless")
    
    parser.addoption("--dryrun", 
                     action="store_true", 
                     default=False,
                     help="Do not modify VMs")
    
    
TargetPlatforms = []
    
def pytest_configure(config):
    iso_path = config.getoption("--iso")
    if iso_path:
        print(f"Using ISO {iso_path}")

    targets = config.getoption("--os")
    if len(targets):
        print(f"Running for {targets}")
    else:
        targets = ["win8:64"]
    for target_name in config.getoption("--os"):
        target_name = target_name.lower().strip()
        if ":" in target_name:
            os_name, architecture = target_name.split(":")
        else:
            architecture = "64"
            os_name = target_name
        assert(architecture in ["32", "64"])
        assert(os_name in ["win8", "win10"])
        TargetPlatforms.append({"os_name":os_name, "architecture":architecture})

    if not len(TargetPlatforms):
        TargetPlatforms.append({"os_name":"win8", "architecture":"64"})

@pytest.fixture
def target_platforms(request):
        return TargetPlatforms

@pytest.fixture
def isos(request):
    iso_path = request.config.getoption("--iso")
    if not iso_path:
        iso_path = []
    return iso_path

@pytest.fixture
def remove_vms(request):
    cleanall = request.config.getoption("--cleanall")
    return cleanall

@pytest.fixture
def headless_vms(request):
    headless = request.config.getoption("--headless_vms")
    return headless

@pytest.fixture
def dryrun(request):
    dryrun = request.config.getoption("--dryrun")
    return dryrun
