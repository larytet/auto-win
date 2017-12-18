
Write-Output "AutoStart: $AutoStart"
$is_64bit = [IntPtr]::size -eq 8

# setup openssh
if ($is_64bit) {
    $cygwin_download_url = "https://www.cygwin.com/setup-x86_64.exe"
}
else {
    $cygwin_download_url = "https://www.cygwin.com/setup-x86.exe"
}

Set-Location -Path "C:\Windows\Temp"
Write-Output "Downloading $cygwin_download_url"
(New-Object System.Net.WebClient).DownloadFile($cygwin_download_url, "C:\Windows\Temp\setup-x86.exe")

Start-Process "C:\Windows\Temp\setup-x86.exe" "--quiet-mode --packages wget,zip,screen" -NoNewWindow -Wait
