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
import utils

def get_autounattend_file(iso):
    iso = iso.lower()
    source_root = utils.source_root_folder()
    if re.match(".+win_ent_8_.+", iso):
        return os.path.join(source_root, "Autounattend-win8-mbr.xml")
    if re.match(".+win_ent_10_.+", iso):
        return os.path.join(source_root, "Autounattend-win10-mbr.xml")
    return None
    
if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    iso_filename = arguments['--iso']
    iso_filename = os.path.realpath(iso_filename)
    iso_folder = os.path.dirname(iso_filename)
    iso_basename = os.path.basename(iso_filename)
    mount_point = os.path.join(iso_folder, "iso_mount")
    res = utils.run_shell_command(f"mount -t udf,loop {iso_filename} {mount_point}", "", None)
    assert res, f"Failed to mount {iso_filename}"
    autounattend_filename = get_autounattend_file(os.path.basename(iso_basename))
    assert autounattend_filename, f"Failed to figure out version of the Windows for {iso_basename}"
    