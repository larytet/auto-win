#
#
#

import os
from collections import namedtuple
import re
import utils
import collections

Machine = collections.namedtuple("Machine", ["name"])
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
        res = utils.run_shell_command(command, copy_to_output, lines)
        assert res, f"Failed to run {command}"
        return lines
            
    def machines(self):
        lines = self.__run_command("list vms")
        existing_machines = []
        for line in lines:
            m = re.match('"(\S+)" \S+', line)
            print(f"line={line}")
            if m:
                machine_name = m.group(1)
                existing_machines.append(Machine(machine_name))
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
        return name
        
    def register_machine(self, name):
        pass

