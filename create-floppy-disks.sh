#!/bin/bash

# Absolute path to this script
SCRIPT=$(readlink -f $0)
# Absolute path this script is in
SCRIPTPATH=`dirname $SCRIPT`


os_list=( win8 win10 )
for os_name in "${os_list[@]}"
do
	printf "ping `hostname` -n 3\r\n" > $SCRIPTPATH/autounattend/packer-floppy-$os_name/pinghost.bat
	$SCRIPTPATH/create-floppy.py -i $SCRIPTPATH/autounattend/packer-floppy-$os_name -t . -o $SCRIPTPATH/autounattend/Autounattend-$os_name-mbr.vfd
done	

