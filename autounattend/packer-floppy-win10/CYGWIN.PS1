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

Write-Output "Downloading Firefox"
$firefox_download_url = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/57.0.2/win32/en-US/Firefox%20Installer.exe"
(New-Object System.Net.WebClient).DownloadFile($firefox_download_url, "C:\Users\User\Downloads\firefox-installer.exe")


# Make sure that there is autologon for user
New-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "AutoAdminLogon" -Value "1" -PropertyType "String" -Force
New-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "DefaultUserName" -Value "user" -PropertyType "String" -Force
New-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" -Name "DefaultPassword" -Value "user" -PropertyType "String" -Force
