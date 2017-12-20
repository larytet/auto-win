#
#
#

import subprocess
import sys
import re
import os
import paramiko


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def __run_shell_command_read_output(p, log_prompt=None, lines=None):
    nextline = p.stdout.readline()
    res = nextline != b""
    #print(f"nextline={nextline}")
    if nextline != b""  and log_prompt != None:
        sys.stdout.write("{1}{0}".format(nextline.decode('UTF-8'), log_prompt))
        sys.stdout.flush()
        
    nextline = nextline.decode('UTF-8').strip() 
    if lines != None and nextline != "":
        #print("Line '{0}' appended to the list".format(nextline))
        lines.append(nextline)
    return res
        
def run_shell_command(command, log_prompt=None, lines=None, silent=False):
    '''
    Execute the specified shell command, return result
    @param lines - if the list is not None collect the output
    @param log_prompt - if not None send the output to stdout 
    '''
    if not silent:
        print(f"{command}")
    #if log_prompt == None:
    #    log_prompt = "\t"
    p = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_ended = False
    while True:
        process_ended = p.poll() is not None
        while __run_shell_command_read_output(p, log_prompt, lines): pass;

        if process_ended:
            break
        
    while __run_shell_command_read_output(p, log_prompt, lines): pass;
    exitcode = p.wait()
    while __run_shell_command_read_output(p, log_prompt, lines): pass;
    
    if exitcode != 0:
        print(f"Command {command} failed")
    if not silent:
        print("Done {0} ...".format(command[:20]))

    
    return exitcode == 0

def executable_exists(name):
    result = run_shell_command("which {0}".format(name))
    return result

def get_connected_network_adapter():
    lines = []
    run_shell_command("ifconfig", "", lines)
    adapter_name = None
    ip_address = None
    for line in lines:
        m = re.match('^(.+): flags=.+', line)
        if m and not adapter_name and not ip_address:
            adapter_name = m.group(1)
        m = re.match('inet\s+(\S+)\s+netmask.+', line)
        if m and adapter_name and not ip_address:
            ip_address = m.group(1)
            if ip_address != "127.0.0.1":
                return True, adapter_name, ip_address
            adapter_name = None
            ip_address = None
            
    return False, None, None 

def mount_iso(iso, mount_point):
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
    print(f"Mount {iso} in {mount_point}")
    res = run_shell_command(f"fuseiso {iso} {mount_point}", "")
    return res;
    
def umount_iso(mount_point):
    res = run_shell_command(f"fuseiso -u {mount_point}", "")
    return res;
    
def source_root_folder():
    return os.path.dirname(os.path.realpath(__file__))
    
def find_ip_by_mac(macaddress):
    lines = []
    res = run_shell_command("arp -a -n", None, lines, True)
    assert res, "Failed to access the system arp table"
    # I am expecting 'test-win-8-64.corp.cyren.com (172.20.21.114) at 08:00:27:25:8e:39 [ether] on enp0s31f6'
    macaddress = macaddress.lower()
    for line in lines:
        m = re.match(f"(.+) \((.+)\) at {macaddress} .+", line)
        if m:
            return True, m.group(1), m.group(2)
    return False, None, None 

class SSH():
    def __init(self, username, password):
        self.username, self.password = username, password
        self.ssh = None
    
    def connect(self, hostname):
             
def connect_ssh(hostname):
    ssh = None
    err_msg = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, 22, "user", "user")
    except paramiko.AuthenticationException:
        err_msg = "Authentication failed when connecting" 
        return False, ssh, err_msg    
    except Exception as exc:
        err_msg = "Failed to connect"+str(exc) 
        return False, ssh, err_msg    
        
    return True, ssh, "Ok"
    
    
    