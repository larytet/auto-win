
# Goals

*  Automatically install a Windows guest in VirtualBox VM 
*  Linux Host
*  PyDev

# How it works

The first test which actually does something is test_install_machines(). The script will create and setup a virtual machine for specified 
Windows version. The Windows setup will run automatically thanks to the floppy disk image which contains Autounattend.xml 

# Usage (Python 3.6 assumed):

	sudo apt-get install virtualbox mkisofs
	sudo apt-get install python3-pip
	
	# install VirtualBox SDK from https://www.virtualbox.org/wiki/Downloads
	# wget http://download.virtualbox.org/virtualbox/5.2.2/VirtualBoxSDK-5.2.2-119230.zip
	# unzip VirtualBoxSDK-5.2.2-119230.zip
	# cd sdk/installer/
	# sudo VBOX_INSTALL_PATH=/usr/lib/virtualboxpython3 python3.6 ./vboxapisetup.py install
 
	git clone git@github.com:larytet/auto-win.git
	cd auto-win
	sudo pip3 install -r requirements.txt

	
	export SRCROOT=$PWD;sudo -E $SRCROOT/create-floppy.py -i $SRCROOT/autounattend/packer-floppy-10 -t . -o $SRCROOT/autounattend/Autounattend-win10-mbr.vfd
	export SRCROOT=$PWD;sudo -E $SRCROOT/create-floppy.py -i $SRCROOT/autounattend/packer-floppy-8 -t . -o $SRCROOT/autounattend/Autounattend-win8-mbr.vfd
	
	# Download a Windows ISO from https://www.microsoft.com/en-us/evalcenter/
	./run-test.sh --iso='./SW_DVD5_SA_Win_Ent_8_64BIT_English_Full_MLF_X18-16254.ISO' --os=win8:64 
	
# Tips

## Enable WinRM in Win 8.1 
	
In the command line started as an administrator:

	net start WinRM
	powershell
	enable-psremoting -force
	exit
	winrm get winrm/config 
	winrm set winrm/config/service/auth @{Basic="true"}
	winrm set winrm/config/service @{AllowUnencrypted="true"}
	
		
# Links

* http://www.hurryupandwait.io/blog/creating-windows-base-images-for-virtualbox-and-hyper-v-using-packer-boxstarter-and-vagrant
* https://unix.stackexchange.com/questions/283446/how-to-create-bootable-windows-8-iso-image-in-linux/313254
* https://github.com/Lekensteyn/windows-bootstrap
* https://virgo47.wordpress.com/2016/03/18/building-windows-virtualbox-machines/  Working Win10
* https://superuser.com/questions/342433/how-to-create-an-empty-floppy-image-with-virtualbox-windows-guest
* http://windowsafg.no-ip.org
* https://github.com/joefitzgerald/packer-windows  Windows templates for Packer
* https://www.packer.io/intro/use-cases.html  Packer
* https://superuser.com/questions/531787/starting-windows-gui-program-in-windows-through-cygwin-sshd-from-ssh-client Open GUI applications via SSH 


# Relevant Issues

* https://github.com/joefitzgerald/packer-windows/issues/156
* https://github.com/mjdorma/pyvbox/issues/99
* https://github.com/joefitzgerald/packer-windows/issues/239
* https://github.com/joefitzgerald/packer-windows/issues/248