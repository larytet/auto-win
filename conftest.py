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
    
def pytest_configure(config):
    iso_path = config.getoption("--iso")
    if iso_path:
        print(f"Using ISO {iso_path}")

