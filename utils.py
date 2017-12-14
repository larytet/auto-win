#
#
#

import subprocess
import sys

def run_shell_command(command, log_prompt=None, lines=None):
    '''
    Execute the specified shell command, return result
    @param lines - if the list is not None collect the output
    @param log_prompt - if not None send the output to stdout 
    '''
    print("Execute '{0}'".format(command))
    p = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        nextline = p.stdout.readline()
        if nextline == '' and p.poll() is not None:
            break
        if nextline != ""  and log_prompt:
            sys.stdout.write("{1}:{0}".format(nextline, log_prompt))
            sys.stdout.flush()
            
        nextline = nextline.strip() 
        if lines != None and nextline != "":
            #print("Line '{0}' appended to the list".format(nextline))
            lines.append(nextline)
    exitcode = p.wait()
    
    if exitcode != 0:
        print("Command '{0}' failed".format(command))
    print("Done {0}".format(command))

    
    return exitcode == 0

def executable_exists(name):
    result = run_shell_command("which {0}".format(name))
    return result
