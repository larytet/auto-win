#
#
#

import os
from collections import namedtuple
import re
import utils
import collections

Machine = collections.namedtuple("Machine", ["name", "uuid"])
OS_Type = collections.namedtuple("OS_Type", ["description", "id"])

class VirtualBox():
    '''
    Wrapper for VirtualBox command line
    I need it because I failed to use Python bindings of VirtualBox SDK 
    '''
    
    def __init__(self):
        pass
    
    def is_ready(self):
        return utils.executable_exists("VBoxManage")
    
    def default_machine_folder(self):
        home = os.path.expanduser("~")
        return os.path.join(home, "VirtualBox")

    def __run_command(self, arguments, copy_to_output=False):
        lines = []
        command = "VBoxManage "+arguments
        log_prompt = None
        if copy_to_output:
            log_prompt = "VBoxManage"
        res = utils.run_shell_command(command, log_prompt, lines)
        assert res, f"Failed to run {command}"
        return lines
            
    def machines(self):
        lines = self.__run_command("list vms")
        existing_machines = []
        for line in lines:
            m = re.match('"(\S+)" {(\S+)}', line)
            print(f"line={line}")
            if m:
                name = m.group(1)
                uuid = m.group(2)
                existing_machines.append(Machine(name, uuid))
        return existing_machines
    
    def guest_os_types(self):
        lines = self.__run_command("list ostypes")
        os_types = []
        
        os_id = None
        os_description = None
        for line in lines:
            m = re.match('ID:\s+(.+)', line)
            if m and not os_id and not os_description:
                os_id = m.group(1)
            m = re.match('Description:\s+(.+)', line)
            if m and os_id and not os_description:
                os_description = m.group(1)
                os_types.append(OS_Type(os_description, os_id))
                os_id = None
                os_description = None

        return os_types
    
    def create_machine(self, path, name, type):
        arguments = f"createvm --name '{name}' --ostype {type} --register"
        lines = self.__run_command(arguments, True)
        uuid = None
        settings_file = None
        for line in lines:
            m = re.match('UUID:\s+(.+)', line)
            if m:
                uuid = m.group(1)
            m = re.match('Settings file:\s+(.+)', line)
            if m:
                settings_file = m.group(1)
            if uuid and settings_file:
                return True, uuid, settings_file

        return False, None 
    
    def set_machine(self, uuid, memory, adapter_name):
        arguments = f"modifyvm {uuid} --memory {memory} --vram 128 --acpi on --nic1 bridged --nictype1 82540EM --bridgeadapter1 {adapter_name}"
        self.__run_command(arguments, True)
        arguments = f"modifyvm {uuid} --ioapic on"
        self.__run_command(arguments, True)
        arguments = f"modifyvm {uuid} --boot1 dvd --boot2 disk --boot3 none --boot4 none"
        self.__run_command(arguments, True)
        
    def add_hard_disk(self, settings_file, uuid, size, iso_path):
        '''
        See https://www.perkin.org.uk/posts/create-virtualbox-vm-from-the-command-line.html
        https://www.praim.com/virtualbox-scripting-tutorial
        @param size: maximum size of the hard disk in MB 
        '''
        name = os.path.basename(settings_file)
        folder = os.path.dirname(settings_file)
        vdi_filename = os.path.join(folder, name+".vdi")
        # Create vmdk image
        size = min(32768, size*1024)
        arguments = f"createhd --filename {vdi_filename} --size {size}"
        self.__run_command(arguments, True)
        
        # Add hard disk controller
        arguments = f"storagectl {uuid} --name 'SATA Controller' --add sata --controller IntelAHCI"
        self.__run_command(arguments, True)
        
        # Attach disk to the VM
        arguments = f"storageattach {uuid} --storagectl 'SATA Controller' --port 0 --device 0 --type hdd --medium {vdi_filename}"
        self.__run_command(arguments, True)
        
        # attach boot disk
        arguments = f"storagectl {uuid} --name 'IDE Controller' --add ide"
        self.__run_command(arguments, True)
        arguments = f"storageattach $VM --storagectl 'IDE Controller' --port 0 --device 0 --type dvddrive --medium {iso_path}"
                
    def register_machine(self, name):
        pass

