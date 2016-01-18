#!/bin/bash

###
# This is the script that compile houat
# into Carambola2 OpenWRT Buildroot SDK.
#
# Usage: place the script into the dicectori wgo containe houat and OpenWRT
#
# The script will:
#
# Usage:
###


BUILD_DIR=$PWD
DATE=$(%d-%m-%Y-%H-%M)

if [[ $# -eq 0 ]] ; then
    echo 'entre the 3 argument ex:'
    echo "compile_houat.sh dir_houat  2 clean"
    echo "the first in for the directori where is houat"
    echo " the second is for the make -j number"
    echo " the trird is for clean the build directori"
    exit 1
fi

    WEIO=$1

# Clean Carambola2 SDK
#
if [ $3 -eq "clean" ]
  then
    cd openwrt
    echo "clean distribution"
    make clean distclean
fi

cd ../$WEIO
echo "git pull $WEIO"
git pull

cd ../openwrt
echo "git pull openwrt"
git pull

echo "installWeio"
sh installWeio.sh $WEIO

echo "make -j $2"
make -j $2

echo " send ssh"
sshpass -p Zmh7c4\!\!35 scp bin/ar71xx/openwrt-ar71xx-generic-weio-squashfs-sysupgrade.bin root@91.121.193.187:/tmp/$1_recovery_$DATE.bin

echo "done"
