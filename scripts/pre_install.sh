#!/bin/sh
echo "This is WeIO pre install procedure"
# This will backup configuration file to /tmp directory and in post install procedure will copy back to /weio directory
# If any changements are required for config.weio they have to be done here in this script

# remove all symlinks before moving, othewise we create WORM
find /weioUser/flash -name "www" -exec rm -rf {} \;
mv /weioUser/flash /weioUserBackup
cp /weio/config.weio /weioUserBackup

# Protect directory from deleting
# B_PATH=`grep "/weioUserBackup/" /lib/upgrade/keep.d/base-files`
#
# MYSTRING="/weioUserBackup/"
# MYFILE=/lib/upgrade/keep.d/base-files
# if grep -q $MYSTRING $MYFILE; then
#     echo "/weioUserBackup/ already protected!"
# else
#     echo $MYSTRING >> $MYFILE
#     echo "/weioUserBackup/ is now protected!"
# fi
# Now I'm ready to start downloading new FW and reinstall everything
cd /tmp/weio/scripts/

# Protect files from deleting
cp base-files /lib/upgrade/keep.d/base-files

# Free RAM from any possible WeIO application left
/etc/init.d/weio_run stop

# I also need here config.weio for correct url for downloading FW
cp /weio/config.weio /tmp/weio/scripts/

#change password
cd /weio/scripts/
sh ./change_root_pswd.sh houat

# Run FW downloader script. This script will download the last version of FW and install it
python downloadFW.py
