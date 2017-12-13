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
                     action="store", 
                     type="string",
                     default=None,
                     metavar="ISO",
                     help="ISO file or url for download")

    parser.addoption("--os", 
                     action="append", 
                     type="string",
                     dest="targets",
                     metavar="TARGETS",
                     default=['win8'],
                     choices=['win8', 'win10'],
                     help="Target OS. This option can be used more than once")
    
    parser.addoption("--architecture", 
                     action="append", 
                     type="string",
                     dest="architectures",
                     metavar="ARCHITECTURES",
                     default=['64'],
                     choices=['32', '64'],
                     help="32 or 64 bits. This option can be used more than once")
    
def pytest_configure(config):
    iso_path = config.getoption("--iso")
    if iso_path:
        print(f"Using ISO {iso_path}")

@pytest.fixture
def target_os(request):
    return request.config.targets


@pytest.fixture
def architecture(request):
    return request.config.architectures

