#!/bin/sh
echo "This is WeIO post install procedure"

# migrating old config file to the new one
cd /weio/scripts/
./migrateConfig.py
cd /weio
rm /tmp/config.weio

# Populate system with the new files
cp -r /weio/scripts/update/* /
rm -r /weio/scripts/update

# Fix between v1.0 and v1.1
chmod +x /etc/init.d/ntpd

#change password
cd /weio/scripts/
sh ./change_root_pswd.sh houat

# flashing new firmware to LPC chip
cd /weio/scripts/
./flash_lpc_fw.py

cd /
