#
#
#

import pytest
import time
import os
import sys
import threading
import utils

import virtualbox_shell

class TestInstallVm:
    '''
    Get lits of the installed VMs, install missing VMs if neccessary
    '''
    
    def __get_vm_name(self, os, architecture):
        return f"{os}.{architecture}"

    def __get_vm_group(self):
        return "test"
    
    def __get_vm_path(self, os, architecture):
        vbox = virtualbox_shell.VirtualBox()
        machine_folder = vbox.default_machine_folder()
        return machine_folder
    
    def __vm_presents(self, os, architecture):
        vm_name = self.__get_vm_name(os, architecture)
        vbox = virtualbox_shell.VirtualBox()
        for vm in vbox.machines():
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
        vbox = virtualbox_shell.VirtualBox()
        for os_type in vbox.guest_os_types(): 
            if machine_type in os_type.description and architecture in os_type.description:
                return os_type.id
        return None
            
            
                    
    def __install_machine(self, iso, os, architecture):
        
        self.__patch_iso(iso, os, architecture)
        
        machine_path = self.__get_vm_path(os, architecture)
        machine_name = self.__get_vm_name(os, architecture)
        os_type_id = self.__find_machine_type(os, architecture)
        vbox = virtualbox_shell.VirtualBox()
        machine = vbox.create_machine(machine_path, machine_name, os_type_id)
        vbox.register_machine(machine)
        
    def test_virtual_box(self):
        assert virtualbox_shell.VirtualBox().is_ready(), "No VBoxManage in the path?"

    def test_installed_machines(self, target_platforms, isos):
        '''
        Collect list of missing VMs
        '''
        missing_platforms = []
        print(target_platforms)
        index = 0
        for target_platform in target_platforms:
            if not self.__vm_presents(target_platform.os, target_platform.architecture):
                missing_platforms.append((index, target_platform))
            index += 1

        print(f"Missing: {missing_platforms}")
        for index, target_platform in missing_platforms:
            assert len(isos) > index, f"No ISO is specified for the missing {target_platform}"
            self.__install_machine(isos[index], target_platform.os, target_platform.architecture)
            
            
            
