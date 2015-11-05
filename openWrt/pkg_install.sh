#!/bin/bash

# Update package base
./scripts/feeds update

# Install base packages
./scripts/feeds install

# Install additional packages
./scripts/feeds install python
./scripts/feeds install avahi-daemon
./scripts/feeds install ntpd
./scripts/feeds install nano
./scripts/feeds install python-pip
./scripts/feeds install avrdude
#./scripts/feeds install nginx
./scripts/feeds install https://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/oldpackages/dfu-util_r3095-1_ar71xx.ipk
