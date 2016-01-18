#!/bin/sh
echo "setting root password"
echo -e "houat\nhouat" | passwd
echo "setting weio user SMB password. Same as root password"
(echo "houat"; echo "houat") | smbpasswd -s -a weio
