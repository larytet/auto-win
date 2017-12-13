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

class TestInstallVm:
    '''
    Get lits of the installed VMs, install missing VMs if neccessary
    '''
    
    def __get_vm_name(self, os, architecture):
        return f"{os}.{architecture}"

    def __get_vm_group(self):
        return "test"
    
    def __get_vm_path(self, os, architecture):
        vbox = virtualbox.VirtualBox()
        machine_name = self.__get_vm_name(os, architecture)
        return vbox.compose_machine_filename(machine_name, self.__get_vm_group())
        '''
        machine_folder = vbox.system_properties().default_machine_folder()
        machine_path = os.path.join(machine_folder, machine_name)
        return machine_path
        '''
    
    def __vm_presents(self, os, architecture):
        vm_name = self.__get_vm_name(os, architecture)
        # returns IVirtualBox (?)
        vbox = virtualbox.VirtualBox()
        # Call to vbox.find_machine(vm_name) fails for unknown reason
        # I run a loop instead
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
    
    def __find_machine_type(self, os, architecture):
        # Dictionary which translates my OS target to vbox.guest_os_types.description
        machine_types = {"win8":"Windows 8", "win10":"Windows 10"}
        machine_type = machine_types[os]
        vbox = virtualbox.VirtualBox()
        for os_type in vbox.guest_os_types: 
            if machine_type in os_type.description and architecture in os_type.description:
                return machine_type
        return None
            
            
                    
    def __install_machine(self, isos, os, architecture):
        assert(len(isos))
        iso = self.__find_iso(isos, os, architecture)
        assert(iso != None)
        
        self.__patch_iso(iso, os, architecture)
        
        machine_path = self.__get_vm_path(os, architecture)
        machine_name = self.__get_vm_name(os, architecture)
        os_type_id = self.__find_machine_type(os, architecture)
        vbox = virtualbox.VirtualBox()
        machine = vbox.create_machine(machine_path, machine_name, self.__get_vm_group(), os_type_id)
        vbox.register_machine(machine)
        
        
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
            
            
            
