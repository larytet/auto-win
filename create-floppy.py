#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""create-floppy

Create vfd file with a floppy disk image for VirtualBox
Use sudo to run the script  
 
Usage:
  create-floppy.py -h | --help
  create-floppy.py -i <FILENAME> -o <FFILENAME>
  create-floppy.py -i <FILENAME> -t <FILENAME> -o <FFILENAME>

Example:
    create-floppy.py -i Autounattend.xml -o win8_autounattend.vfd 
    create-floppy.py -i Autounattend-win8-mbr.xml -t Autounattend.xml -o win8_autounattend.vfd 
   
Options:
  -h --help                  Show this screen.
  -i --infile=<FILENAME>     File/folder to copy to the image
  -t --target=<FILENAME>     Name of the file/folder in the image
  -o --outfile=<FILENAME>    Name of the image
"""

import os
from docopt import docopt
import re
import hashlib
import tempfile
import shutil

import utils

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    image_filename = arguments['--outfile']
    image_filename = os.path.realpath(image_filename)
    image_folder = os.path.dirname(image_filename)
    image_basename = os.path.basename(image_filename)
    
    image_mount_tmp = tempfile.mkdtemp(None, "mount-iso-", image_folder) 
    mount_point = os.path.join(image_folder, image_mount_tmp)

    size = 1440*1024
    while True:
        
        res = utils.run_shell_command(f"fallocate -l {size} {image_filename}", "", None)
        msg = f"Failed to allocate {size} bytes for {image_filename}"
        if not res:
            break; 
        
        res = utils.run_shell_command(f"mkfs.vfat {image_filename}", "", None)
        msg = f"Failed to create file system in the {image_filename}"
        if not res:
            break; 
        
        res = utils.run_shell_command(f"mount -o loop {image_filename} {mount_point}", "", None)
        msg = f"Failed to mount {image_filename} using mount point {mount_point}"
        if not res:
            break; 
        
        image_content = arguments['--infile']
        target_name = arguments.get('--target', os.path.basename(image_content))
        if os.path.isdir(image_content):
            res = utils.run_shell_command(f"mkdir -p {mount_point}/target_name", "", None)
            res = utils.run_shell_command(f"cp -R {image_content}/* {mount_point}/{target_name}/.", "", None)
        else:
            res = utils.run_shell_command(f"cp -R {image_content} {mount_point}/{target_name}", "", None)
        msg = f"Failed to copy {image_content} to {mount_point}"
        if not res:
            break; 

    break
    if not res:
        print(msg)
    
    if os.path.dirname(mount_point):
        utils.run_shell_command(f"umount {mount_point}", "", None)
        shutil.rmtree(image_mount_tmp)
