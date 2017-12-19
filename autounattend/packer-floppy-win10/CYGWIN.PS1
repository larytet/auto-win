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
