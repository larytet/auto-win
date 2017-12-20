Write-Output "Configuring firewall"
New-NetFirewallRule -Protocol TCP -LocalPort 22 -Direction Inbound -Action Allow -DisplayName SSH
New-NetFirewallRule -Protocol TCP -LocalPort 22 -Direction Outbound -Action Allow -DisplayName SSH

Write-Output "Create a home directory for the user"
& "mkdir" C:\cygwin\home\user

# The trick here is to start a "screen" session with DISPLAY correctly set 
# and allow starting GUI applications remotely
# This cmd file will invoke Cygwin bash with screen
Write-Output "Create C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_screen.cmd"
$StartScreenBat = @"
@echo off 
C:
chdir C:\cygwin\bin
set HOME=\cygwin\home\user
echo Calling bash
bash --login -i `"/home/user/start_screen.sh`"
"@
$StartScreenBat | Out-File -FilePath "C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_screen.cmd" -Encoding ASCII

Write-Output "Create input file for ssh-host-config C:\cygwin\home\user\password"
$SshConfigInput = @"
user
user
"@
$SshConfigInput | Out-File -FilePath "C:\cygwin\home\user\password" -Encoding ASCII

# I iwll run this BASH script every time user logins
# This is a real Linux bash script with Unix end of line 
Write-Output "C:\cygwin\home\user\start_screen.sh"
$StartScreenSh = @"
#!/bin/bash
ssh-host-config -y < /home/user/password
cygrunsrv -S sshd
screen -dmS `"main`"
"@
$StartScreenSh | Out-File -FilePath "C:\cygwin\home\user\start_screen.sh" -Encoding ASCII
