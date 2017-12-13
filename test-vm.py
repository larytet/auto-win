#
#
#

import pytest
import time
import os
import sys
import glob
import re
from collections import namedtuple
import threading

class TestInstallVm:
    '''
    Get lits of the installed VMs, install missing VMs if neccessary
    '''
    
    def test_installed_machines(self):
        '''
        Collect list of missing VMs
        '''