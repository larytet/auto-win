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
        return f"test.{os}.{architecture}"

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
                return True, vm;
        return False, None
            
        
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
        os_types = vbox.guest_os_types()
        for os_type in os_types: 
            if machine_type in os_type.description and architecture in os_type.description:
                print(f"Hit OS type {os_type}")
                return os_type.id
        return None
                    
    def __install_machine(self, iso, os, architecture):
        
        self.__patch_iso(iso, os, architecture)
        
        machine_path = self.__get_vm_path(os, architecture)
        machine_name = self.__get_vm_name(os, architecture)
        os_type_id = self.__find_machine_type(os, architecture)
        vbox = virtualbox_shell.VirtualBox()
        res, machine_uuid, machine_settings_file = vbox.create_machine(machine_path, machine_name, os_type_id)
        assert res, f"Failed to create {machine_name}"
        print(f"Created machine {machine_name} uuid={machine_uuid} in {machine_settings_file}")
        vbox.register_machine(machine_uuid)
        
    def test_virtual_box(self):
        assert virtualbox_shell.VirtualBox().is_ready(), "No VBoxManage in the path?"

    def test_network(self):
        res, adapter_name, ip_address = utils.get_connected_network_adapter()
        assert res, "I did not find any connected network adapters on the host machine"
        print(f"I am going to use network adapter {adapter_name}, {ip_address}")
        
    def test_install_machines(self, target_platforms, isos):
        '''
        Collect list of missing VMs
        '''
        missing_platforms = []
        print(target_platforms)
        index = 0
        for target_platform in target_platforms:
            presents, _ = self.__vm_presents(target_platform.os, target_platform.architecture)
            if not presents:
                missing_platforms.append((index, target_platform))
            index += 1

        print(f"Missing: {missing_platforms}")
        for index, target_platform in missing_platforms:
            assert len(isos) > index, f"No ISO is specified for the missing {target_platform}"
            self.__install_machine(isos[index], target_platform.os, target_platform.architecture)
            self.__setup_machines(target_platforms)

    def __setup_machines(self, target_platforms):            
        res, adapter_name, _ = utils.get_connected_network_adapter()
        assert res, "I did not find any connected network adapters on the host machine"
        
        vbox = virtualbox_shell.VirtualBox()
        memory = 2*1024
        for target_platform in target_platforms:
            os, architecture = target_platform.os, target_platform.architecture
            presents, machine = self.__vm_presents(os, architecture)
            assert presents, f"Failed to find machine {os} {architecture}"           
            vbox.set_machine(machine.uuid, memory, adapter_name)

            
            
            
