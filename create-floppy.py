#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""create-floppy

Create vfp file with a floppy disk image for VirtualBox
Use sudo to run the script  
 
Usage:
  create-floppy.py -h | --help
  create-floppy.py -i <FILENAME> -o <FFILENAME>

Example:
    create-floppy.py -i Autounattend.xml -o win8_autounattend.vfp 
   
Options:
  -h --help                 Show this screen.
  -i --infile=<FILENAME>    File/folder to copy to the image
  -o --outfile=<FILENAME>   Name of the image
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

        print(f"Clone {iso_filename}")
        iso_clone_tmp = tempfile.mkdtemp(None, "iso_clone", iso_folder)
        res = utils.run_shell_command(f"cp -R {mount_point}/* {iso_clone_tmp}", "", None)
        assert res, f"Failed to clone {iso_filename} using mount point {mount_point}"

        utils.run_shell_command(f"umount {mount_point}", "", None)
        os.unlink(iso_mount_tmp)
        os.unlink(iso_filename)
        mount_point = None

        iso_autounattend_filename = os.path.join(iso_clone_tmp, "Autounattend.xml")
        res = utils.run_shell_command(f"cp -f {autounattend_filename} {iso_autounattend_filename}", "", None)
        assert res, f"Failed to copy {autounattend_filename}"
        
        # See 
        # https://unix.stackexchange.com/questions/283446/how-to-create-bootable-windows-8-iso-image-in-linux/313254
        # https://github.com/Lekensteyn/windows-bootstrap
        # Working Win10 https://virgo47.wordpress.com/2016/03/18/building-windows-virtualbox-machines/
        # https://superuser.com/questions/342433/how-to-create-an-empty-floppy-image-with-virtualbox-windows-guest
        res = utils.run_shell_command(f"genisoimage -udf -o {iso_filename} {iso_clone_tmp}", "", None)
        assert res, f"Failed to generate {iso_filename}"
        os.unlink(iso_clone_tmp)

        break
    
    if mount_point:
        utils.run_shell_command(f"umount {mount_point}", "", None)
        os.unlink(iso_mount_tmp)
    
    
    
    