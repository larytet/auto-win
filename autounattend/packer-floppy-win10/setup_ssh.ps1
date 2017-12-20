# configure firewall

Write-Output "Configuring firewall"
New-NetFirewallRule -Protocol TCP -LocalPort 22 -Direction Inbound -Action Allow -DisplayName SSH
New-NetFirewallRule -Protocol TCP -LocalPort 22 -Direction Outbound -Action Allow -DisplayName SSH

# Create a home directory for the user
& "mkdir" C:\cygwin\home\user

$StartScreenBat = @"
@echo off 
C:
chdir C:\cygwin\bin
set HOME=\cygwin\home\user
echo Calling bash
bash --login -i `"/home/user/start_screen.sh`"
sleep 30
"@
$StartScreenBat | Out-File -FilePath "C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_screen.cmd" -Encoding ASCII
Start-Sleep -s 30

$SshConfigInput = @"
user
user
"@
$SshConfigInput | Out-File -FilePath "C:\cygwin\home\user\password" -Encoding ASCII
Start-Sleep -s 30

$StartScreenSh = @"
#!/bin/bash
ssh-host-config -y < /home/user/password
cygrunsrv -S sshd
screen -dmS `"main`"
"@
$StartScreenSh | Out-File -FilePath "C:\cygwin\home\user\start_screen.sh" -Encoding ASCII
Start-Sleep -s 30
