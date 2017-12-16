#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""create-floppy

Create vfp file with a floppy disk image for VirtualBox
Use sudo to run the script  
 
Usage:
  create-floppy.py -h | --help
  create-floppy.py -i <FILENAME> -o <FFILENAME>
  create-floppy.py -i <FILENAME> -t <FILENAME> -o <FFILENAME>

Example:
    create-floppy.py -i Autounattend.xml -o win8_autounattend.vfp 
    create-floppy.py -i Autounattend-win8-mbr.xml -t Autounattend.xml -o win8_autounattend.vfp 
   
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

# See 
# https://unix.stackexchange.com/questions/283446/how-to-create-bootable-windows-8-iso-image-in-linux/313254
# https://github.com/Lekensteyn/windows-bootstrap
# Working Win10 https://virgo47.wordpress.com/2016/03/18/building-windows-virtualbox-machines/
# https://superuser.com/questions/342433/how-to-create-an-empty-floppy-image-with-virtualbox-windows-guest
    
if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    image_filename = arguments['--outfile']
    image_filename = os.path.realpath(image_filename)
    image_folder = os.path.dirname(image_filename)
    image_basename = os.path.basename(image_filename)
    
    image_mount_tmp = tempfile.mkdtemp(None, "mount-iso-", image_folder) 
    mount_point = os.path.join(image_folder, image_mount_tmp)

    size = 1440*1024
    res = utils.run_shell_command(f"fallocate -l {size} {image_filename}", "", None)
    assert res, f"Failed to allocate {size} bytes for {image_filename}"
    
    res = utils.run_shell_command(f"mkfs.vfat {image_filename}", "", None)
    assert res, f"Failed to create file system in the {image_filename}"
    
    res = utils.run_shell_command(f"mount -o loop {image_filename} {mount_point}", "", None)
    assert res, f"Failed to mount {image_filename} using mount point {mount_point}"
    
    image_content = arguments['--infile']
    target_name = arguments.get('--target', os.path.basename(image_content))
    if os.path.isdir(image_content):
        res = utils.run_shell_command(f"mkdir -p {mount_point}/target_name", "", None)
        res = utils.run_shell_command(f"cp -R {image_content}/* {mount_point}/{target_name}/.", "", None)
    else:
        res = utils.run_shell_command(f"cp -R {image_content} {mount_point}/{target_name}", "", None)
    assert res, f"Failed to copy {image_content} to {mount_point}"

        
    utils.run_shell_command(f"umount {mount_point}", "", None)
    shutil.rmtree(image_mount_tmp)
