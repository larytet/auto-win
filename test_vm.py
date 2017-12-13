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
import virtualbox
from platform import architecture

class TestInstallVm:
    '''
    Get lits of the installed VMs, install missing VMs if neccessary
    '''
    
    def __create_vm_name(self, os, architecture):
        return f"{os}.{architecture}"
    
    def __vm_presents(self, os, architecture):
        vm_name = self.__create_vm_name(os, architecture)
        vbox = virtualbox.VirtualBox()
        for vm in vbox.machines:
            if vm_name == vm.name:
                return True;
        return False
            
        
    def test_installed_machines(self, target_platforms):
        '''
        Collect list of missing VMs
        '''
        print(target_platforms)
        for target_platform in target_platforms:
            assert(self.__vm_presents(target_platform.os, target_platform.architecture))
        pass