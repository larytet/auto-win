#
#
#

import subprocess
import sys
import re

def __run_shell_command_read_output(p, log_prompt=None, lines=None):
    nextline = p.stdout.readline()
    res = nextline != b""
    #print(f"nextline={nextline}")
    if nextline != ""  and log_prompt:
        sys.stdout.write("{1}:{0}".format(nextline.decode('UTF-8'), log_prompt))
        sys.stdout.flush()
        
    nextline = nextline.decode('UTF-8').strip() 
    if lines != None and nextline != "":
        #print("Line '{0}' appended to the list".format(nextline))
        lines.append(nextline)
    return res
        
def run_shell_command(command, log_prompt=None, lines=None):
    '''
    Execute the specified shell command, return result
    @param lines - if the list is not None collect the output
    @param log_prompt - if not None send the output to stdout 
    '''
    print("Execute '{0}'".format(command))
    p = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_ended = False
    while True:
        process_ended = p.poll() is not None
        while __run_shell_command_read_output(p, log_prompt, lines): pass;
        __run_shell_command_read_output(p, log_prompt, lines)

        if process_ended:
            break
        
    while __run_shell_command_read_output(p, log_prompt, lines): pass;
    exitcode = p.wait()
    while __run_shell_command_read_output(p, log_prompt, lines): pass;
    
    if exitcode != 0:
        print("Command '{0}' failed".format(command))
    print("Done {0}".format(command))

    
    return exitcode == 0

def executable_exists(name):
    result = run_shell_command("which {0}".format(name))
    return result

def get_connected_network_adapter():
    lines = []
    run_shell_command("ifconfig", None, lines)
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
