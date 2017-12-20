# configure firewall
Write-Output "Configuring firewall"
netsh advfirewall firewall add rule name="SSH port 22" dir=in action=allow protocol=TCP localport=22
netsh advfirewall firewall add rule name="SSH port 22" dir=out action=allow protocol=TCP localport=22

  