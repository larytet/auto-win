# configure firewall
Write-Output "Configuring firewall"
netsh advfirewall firewall add rule name="SSH port 22" dir=in action=allow protocol=TCP localport=22
netsh advfirewall firewall add rule name="SSH port 22" dir=out action=allow protocol=TCP localport=22

  
$StartScreenBat = @"
@echo off 
C:
mkdir C:\cygwin\home\user
chdir C:\cygwin\bin
set HOME=\cygwin\home\user
bash --login -i `"/home/user/start_screen.sh`"
"@
$StartScreenBat | Out-File -FilePath "C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_screen.cmd" -Encoding ASCII

$StartScreenSh = @"
#!/bin/bash
echo user > password
echo user >> password
ssh-host-config -y < password
cygrunsrv -S sshd
screen -dmS `"main`"
"@
$StartScreenSh | Out-File -FilePath "C:\cygwin\home\user\start_screen.sh" -Encoding ASCII

