#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""patch_iso

Clone ISO, add relevant Autounattend.xml file
Use sudo to run the script  
 
Usage:
  patch_iso.py -h | --help
  patch_iso.py -i <FILENAME>

Example:
    patch_iso.py -i SW_DVD5_WIN_ENT_10_1703_64BIT_English_MLF_X21-36478.ISO
   
Options:
  -h --help                 Show this screen.
  -i --iso=<FILENAME>       ISO image 
"""

import os
from docopt import docopt
import re
import hashlib
import tempfile
import shutil

import utils

def get_autounattend_file(iso):
    iso = iso.lower()

    source_root = utils.source_root_folder()
    if re.match(".+win_ent_8_.+", iso):
        return os.path.join(source_root, "Autounattend-win8-mbr.xml"), "Windows 8"
    if re.match(".+win_ent_10_.+", iso):
        return os.path.join(source_root, "Autounattend-win10-mbr.xml"), "Windows 10"
    return None, None
    
if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    iso_filename = arguments['--iso']
    iso_filename = os.path.realpath(iso_filename)
    iso_folder = os.path.dirname(iso_filename)
    iso_basename = os.path.basename(iso_filename)
    
    iso_mount_tmp = tempfile.mkdtemp(None, "mount_iso", iso_folder) 
    mount_point = os.path.join(iso_folder, iso_mount_tmp)
    res = utils.run_shell_command(f"mount -t udf,loop {iso_filename} {mount_point}", "", None)
    assert res, f"Failed to mount {iso_filename}"
    autounattend_filename, os_name = get_autounattend_file(os.path.basename(iso_basename))
    assert autounattend_filename, f"Failed to figure out version of the Windows for {iso_basename}"
    print(f"This is {os_name} iso")
    iso_autounattend_filename = os.path.join(mount_point, "Autounattend.xml")
    while True:
        if os.path.exists(iso_autounattend_filename):
            print(f"File {iso_autounattend_filename} found")
            iso_autounattend_hash = hashlib.md5(open(iso_autounattend_filename, 'rb').read()).hexdigest()
            autounattend_hash = hashlib.md5(open(autounattend_filename, 'rb').read()).hexdigest()
            if (iso_autounattend_hash == autounattend_hash):
                print(f"Same hash {iso_autounattend_hash} for {iso_autounattend_filename} and {autounattend_filename}")
                print(f"Do nothing")
                break
        break
        iso_clone_tmp = tempfile.mkdtemp(None, "iso_clone", iso_folder)
        print(f"Clone {iso_filename}")
        res = utils.run_shell_command(f"cp -rf {mount_point}/* {iso_clone_tmp}", "", None)
        assert res, f"Failed to clone {iso_filename} using mount point {mount_point}"
        iso_autounattend_filename = os.path.join(iso_clone_tmp, "Autounattend.xml")
        res = utils.run_shell_command(f"cp -f {autounattend_filename} {iso_autounattend_filename}", "", None)
        assert res, f"Failed to copy {autounattend_filename}"
        
        utils.run_shell_command(f"umount {mount_point}", "", None)
        os.unlink(iso_mount_tmp)
        os.unlink(iso_filename)
        mount_point = None
        
        res = utils.run_shell_command(f"", "", None)
        assert res, f"Failed to copy {autounattend_filename}"
        
        

    if mount_point:
        utils.run_shell_command(f"umount {mount_point}", "", None)
        os.unlink(iso_mount_tmp)
    
    
    
    