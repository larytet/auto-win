$is_64bit = [IntPtr]::size -eq 8

# See https://github.com/joefitzgerald/packer-windows/issues/256 for helpful tips 
# get cygwin
if ($is_64bit) {
    # $cygwin_download_url = "https://www.cygwin.com/setup-x86_64.exe"
    $cygwin_download_url = "https://www.cygwin.com/setup-x86_64.exe"
}
else {
    $cygwin_download_url = "https://www.cygwin.com/setup-x86.exe"
}

Write-Output "Downloading $cygwin_download_url"
(New-Object System.Net.WebClient).DownloadFile($cygwin_download_url, "C:\Users\User\Downloads\setup-x86.exe")

$StartScreenBat = @"
@echo off 
C:
mkdir C:\cygwin\home\user
chdir C:\cygwin\bin
bash --login -i "/home/user/start_screen.sh"
"@
$StartScreenBat | Out-File -FilePath "C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_screen.cmd" -Encoding ASCII

$StartScreenSh = @"
#!/bin/bash
screen -dmS "main"
"@
$StartScreenSh | Out-File -FilePath "C:\cygwin\home\user\start_screen.sh" -Encoding ASCII

