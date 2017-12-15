*  Windows guest running in VirtualBox VM 
*  Linux Host
*  PyDev


Usage (Python 3.6 assumed):

	sudo apt-get install virtualbox mkisofs
	sudo apt-get install python3-pip
	# install VirtualBox SDK from https://www.virtualbox.org/wiki/Downloads
	wget http://download.virtualbox.org/virtualbox/5.2.2/VirtualBoxSDK-5.2.2-119230.zip
	unzip VirtualBoxSDK-5.2.2-119230.zip
	cd sdk/installer/
	sudo VBOX_INSTALL_PATH=/usr/lib/virtualboxpython3 python3.6 ./vboxapisetup.py install
 
	git clone git@github.com:larytet/auto-win.git
	cd auto-win
	sudo pip3 install -r requirements.txt