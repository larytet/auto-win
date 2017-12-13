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
        return f"test.{os}.{architecture}"
    
    def __vm_presents(self, os, architecture):
        vm_name = self.__create_vm_name(os, architecture)
        vbox = virtualbox.VirtualBox()
        for vm in vbox.machines:
            if vm_name == vm.name:
                return True;
        return False
            
        
    def __find_iso(self, isos, os, architecture):
        '''
        Find an ISO which is a reasonable match for the spcified OS
        '''
        for iso in isos:
            iso = iso.lower().strip()
            if os in iso and architecture in iso:
                return iso
        return None
    
    def __patch_iso(self, iso, os, architecture):
        '''
        Add file AutoUnattend.xml to the ISO image if missing
        '''
        pass
    
    def __install_machine(self, isos, os, architecture):
        iso = self.__find_iso(isos, os, architecture)
        assert(iso != None)
        self.__patch_iso(iso, os, architecture)
        
        
    def test_installed_machines(self, target_platforms, isos):
        '''
        Collect list of missing VMs
        '''
        missing_platforms = []
        print(target_platforms)
        for target_platform in target_platforms:
            if not self.__vm_presents(target_platform.os, target_platform.architecture):
                missing_platforms.append(target_platform)
        print(f"Missing: {missing_platforms}")
        for target_platform in missing_platforms:
            self.__install_machine(isos, target_platform.os, target_platform.architecture)
            
            
            
