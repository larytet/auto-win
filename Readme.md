*  Windows guest running in VirtualBox VM 
*  Linux Host
*  PyDev


Usage (Python 3.6 assumed):

	sudo apt-get install virtualbox
	# install VirtualBox SDK from https://www.virtualbox.org/wiki/Downloads
	wget http://download.virtualbox.org/virtualbox/5.2.2/VirtualBoxSDK-5.2.2-119230.zip
	unzip VirtualBoxSDK-5.2.2-119230.zip
	export VBOX_INSTALL_PATH=/usr/lib/virtualbox
	sudo python3.6 ./sdk/installer/vboxapisetup.py
 
	sudo apt-get install python3-pip
	git clone git@github.com:larytet/auto-win.git
	cd auto-win
	sudo pip3 install -r requirements.txt