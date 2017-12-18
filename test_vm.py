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
import shutil

class TestInstallVm:
    '''
    Get lits of the installed VMs, install missing VMs if neccessary
    '''
    
    def __get_vm_name(self, os_name, architecture):
        return f"test.{os_name}.{architecture}"

    def __get_vm_group(self):
        return "test"
    
    def __get_vm_path(self, os_name, architecture):
        vbox = virtualbox_shell.VirtualBox()
        machine_folder = vbox.default_machine_folder()
        return machine_folder
    
    def __vm_presents(self, os_name, architecture):
        vm_name = self.__get_vm_name(os_name, architecture)
        vbox = virtualbox_shell.VirtualBox()
        for vm in vbox.machines():
            if vm_name == vm.name:
                return True, vm;
        return False, None
            
    def __vm_running(self, os_name, architecture):
        vm_name = self.__get_vm_name(os_name, architecture)
        vbox = virtualbox_shell.VirtualBox()
        for vm in vbox.running_machines():
            if vm_name == vm.name:
                return True, vm;
        return False, None
        
    def __find_iso(self, isos, os_name, architecture):
        '''
        Find an ISO which is a reasonable match for the spcified OS
        '''
        for iso in isos:
            iso = iso.lower().strip()
            if os_name in iso and architecture in iso:
                return iso
        return None
    
    def __find_machine_type(self, os_name, architecture):
        # Dictionary which translates my OS target to vbox.guest_os_types.description
        machine_types = {"win8":"Windows 8", "win10":"Windows 10"}
        machine_type = machine_types[os_name]
        vbox = virtualbox_shell.VirtualBox()
        os_types = vbox.guest_os_types()
        for os_type in os_types: 
            if machine_type in os_type.description and architecture in os_type.description:
                print(f"Hit OS type {os_type}")
                return os_type.id
        return None
                    
    def __install_machine(self, os_name, architecture):
        machine_path = self.__get_vm_path(os_name, architecture)
        machine_name = self.__get_vm_name(os_name, architecture)
        os_type_id = self.__find_machine_type(os_name, architecture)
        vbox = virtualbox_shell.VirtualBox()
        res, uuid, settings_file = vbox.create_machine(machine_path, machine_name, os_type_id)
        assert res, f"Failed to create {machine_name}"
        print(f"Created machine {machine_name} uuid={uuid} in {settings_file}")
        vbox.register_machine(uuid)
        return uuid, settings_file
        
    def test_environment(self):
        assert virtualbox_shell.VirtualBox().is_ready(), "No VBoxManage in the path? Try apt-get install virtualbox"
        #assert utils.executable_exists("fuseiso"), "No fuseiso? Try apt-get install fuseiso"
        
    def test_stop_machines(self, target_platforms):
        '''
        Stop all running VMs before I start to modify them
        '''
        vbox = virtualbox_shell.VirtualBox()
        for target_platform in target_platforms:
            running, vm = self.__vm_running(target_platform.os_name, target_platform.architecture)
            if running:
                vbox.stop_machine(vm.name)
        # a short delay in case a human being watches the GUI - all VNs are disappearing here
        time.sleep(0.5)

    def test_remove_machines(self, remove_vms, target_platforms):
        if not remove_vms:
            return
        print("Removing all VMs")
        vbox = virtualbox_shell.VirtualBox()
        for target_platform in target_platforms:
            presents, vm = self.__vm_presents(target_platform.os_name, target_platform.architecture)
            if presents:
                vbox.remove_machine(vm.name)
        # a short delay in case a human being watches the GUI - all VNs are disappearing here
        time.sleep(0.5)
            
    def __get_autounattend_vfd(self, os_name):
        source_root = utils.source_root_folder()
        return os.path.join(source_root, "autounattend", f"Autounattend-{os_name}-mbr.vfd")
    
    def __get_autounattend_vfd_command(self, os_name):
        source_root = utils.source_root_folder()
        return f"export SRCROOT={source_root};sudo -E $SRCROOT/create-floppy.py -i $SRCROOT/autounattend/packer-floppy-{os_name} -t . -o $SRCROOT/autounattend/Autounattend-{os_name}-mbr.vfd"
        
    def test_install_machines(self, target_platforms, isos):
        '''
        Collect list of missing VMs
        '''
        missing_platforms = []
        print(target_platforms)
        index = 0
        for target_platform in target_platforms:
            presents, _ = self.__vm_presents(target_platform.os_name, target_platform.architecture)
            if not presents:
                missing_platforms.append((index, target_platform))
            index += 1
        
        res, adapter_name, ip_address = utils.get_connected_network_adapter()
        assert res, "I did not find any connected network adapters on the host machine"
        print(f"I am going to use network adapter {adapter_name}, {ip_address}")

        if len(missing_platforms):
            print(f"Missing: {missing_platforms}")
            
        for index, target_platform in missing_platforms:
            os_name, architecture = target_platform.os_name, target_platform.architecture
            autounattend_vfd = self.__get_autounattend_vfd(os_name)
            if not os.path.isfile(autounattend_vfd):
                autounattend_command = self.__get_autounattend_vfd_command(os_name)
                assert False, f"Floppy image {autounattend_vfd} is not found. Try {autounattend_command}"
                
            iso = isos[index]
            assert len(isos) > index, f"No ISO is specified for the missing {target_platform}"
            uuid, settings_file = self.__install_machine(os_name, architecture)
            self.__setup_machine(target_platform, settings_file, uuid, adapter_name)
            vbox = virtualbox_shell.VirtualBox()
            vbox.add_boot_disk(uuid, iso)
            vbox.add_floppy_disk(uuid, autounattend_vfd)

        vbox = virtualbox_shell.VirtualBox()
        # patch for the laptops which switch between adapters often
        for target_platform in target_platforms:
            os_name, architecture = target_platform.os_name, target_platform.architecture
            presents, machine = self.__vm_presents(os_name, architecture)
            vbox.set_network_adapter(machine.uuid, adapter_name)

    def __setup_machine(self, target_platform, settings_file, uuid, adapter_name):            
        vbox = virtualbox_shell.VirtualBox()
        memory = 2*1024
        os_name, architecture = target_platform.os_name, target_platform.architecture
        presents, machine = self.__vm_presents(os_name, architecture)
        assert presents, f"Failed to find machine {os_name} {architecture}"           
        vbox.set_machine(machine.uuid, memory)
        vbox.add_hard_disk(settings_file, uuid, 32*1024)
            
