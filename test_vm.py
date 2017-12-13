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
            
        
    def __install_machine(self, os, architecture):
        
    def test_installed_machines(self, target_platforms, isos):
        '''
        Collect list of missing VMs
        '''
        missing_platforms = []
        print(target_platforms)
        for target_platform in target_platforms:
            if not self.__vm_presents(target_platform.os, target_platform.architecture):
                missing_platforms.append(target_platform)
        print(f"Missing: {missing_machines}")
        for target_platform in missing_platforms:
            self.__install_machine(target_platform.os, target_platform.architecture)