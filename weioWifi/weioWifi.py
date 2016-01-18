### 
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######  
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ######    ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform 
#
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

import subprocess
import re
import shutil
import time

import sys, os, logging

import iwInfo

from weioLib import weioSubprocess
from weioLib import weioIpAddress
from weioLib import weioConfig


logging.basicConfig()
log = logging.getLogger("WeioWifi")
log.setLevel(logging.DEBUG)


class WeioWifi() :
    def __init__(self, interface):
        self.data = None
        self.interface = interface
        self.mode = None
        self.passwd = ""
        self.encryption = ""
        self.periodicCheck = None
        """ Counts the number of times we found deauthenticated state.
        This mechanism protect us from network hick-ups - i.e. we will not
        disconnect the same moment we lost our AP. wpa_supplicant will re-try authenticating,
        and we will check connection periodically. After some nuber of spoted disconnection mode,
        we will give up and go to AP mode. """
        self.disconnectedCounter = 0

    def checkConnection(self) :
        command = "iwconfig " + self.interface
        status = weioSubprocess.shellBlocking(command)

        #print(str(status))
        # We are in STA mode, so check if we are connected
        if (status == "ERR_CMD") or "No such device" in status :
            # WiFi is DOWN
            print "Wifi is DOWN"
            self.mode = None
        # Check if wlan0 is in Master mode
        elif "Mode:Master" in status :
            print "AP Mode"
            self.mode = "ap"
            #self.essid = status.strip().startswith("ESSID:").split(':')[1]
        elif "Mode:Managed" in status :
            if "Access Point: Not-Associated" in status :
                self.mode = None
            else :
                self.mode = "sta"

        # We can not serve anything if we are not in sta or ap mode
        #print "CHECKING WIFI!"
        #if (self.mode != None):
        #   print "self.mode = " + self.mode
        #print "weioIpAddress.getLocalIpAddress() = " + weioIpAddress.getLocalIpAddress()

        if (self.mode == None):
            self.disconnectedCounter = self.disconnectedCounter + 1
        else:
            self.disconnectedCounter = 0

        config = weioConfig.getConfiguration()

        if ((self.disconnectedCounter >= 2 or (self.mode == "sta" and weioIpAddress.getLocalIpAddress() == ''))
             and config['auto_to_ap'] == "YES"):
            # Move to Master mode
            print "Trying to move to AP RESCUE mode..."
            subprocess.call("scripts/wifi_set_mode.sh rescue", shell=True)

            self.disconnectedCounter = 0

            # Restart Tornado (shell script bring it up whenever it exits)
            #cmd = "/etc/init.d/weio_run restart"
            #weioSubprocess.shellBlocking(cmd)
            print "************* EXITING ****************"
            os._exit(os.EX_OK)

        # At this point connection has been maid, and all we have to do is check ESSID
        #print "WIFI ESSID : ", status
        pat = r"(?<=ESSID:\")(.*\n?)(?=\")"
        #print "RESULT", re.findall(pat, status)[0]
        essidName = re.findall(pat, status)
        if (len(essidName)>0):
            self.essid = essidName[0]
        
        #print essid
        #for word in status.split(" ") :
        #    if word.startswith("ESSID") :
        #        self.essid = word.split('\"')[1]
        #        break

    def setConnection(self, mode):

        # Stop checking WiFi periodically (we will reset)
        self.periodicCheck.stop()
        
        print "SETTING THE CONNECTION " + mode

        """ First shut down the WiFi on Carambola """
        weioSubprocess.shellBlocking("wifi down")

        if (mode is 'ap') :
            fname = "/etc/config/wireless.ap"

            with open(fname) as f:
                out_fname = fname + ".tmp"
                out = open(out_fname, "w")
                for line in f:
                    line = re.sub(r"option\s+ssid\s.*$", r"option ssid " +
                            "'" + self.essid + "'", line)

                    if (self.passwd == ""):
                        line = re.sub(r'option\s+encryption\s.*$', r'option encryption '
                               + "'none'", line)
                    else:
                        line = re.sub(r"option\s+key\s.*$", r"option key " +
                                "'" + self.passwd + "'", line)
                        line = re.sub(r'option\s+encryption\s.*$', r'option encryption '
                               + "'psk2+tkip+ccmp'", line)
                    out.write(line)
                out.close()
                os.rename(out_fname, fname)
                shutil.copy(fname, "/etc/config/wireless")

            cmd = "scripts/wifi_set_mode.sh ap"
            subprocess.call(cmd, shell=True)

        elif (mode is 'sta') :
            """ Change the /etc/config/wireless.sta : replace the params """
            fname = "/etc/config/wireless.sta"
            with open(fname) as f:
                out_fname = fname + ".tmp"
                out = open(out_fname, "w")
                for line in f:
                    line = re.sub(r'option\s+ssid\s.*$', r'option ssid ' + "'" + self.essid + "'", line)
                    line = re.sub(r'option\s+key\s.*$', r'option key ' + "'" + self.passwd + "'", line)
                    if (self.passwd == ""):
                        line = re.sub(r'option\s+encryption\s.*$', r'option encryption '
                               + "'none'", line)
                    else:
                        line = re.sub(r"option\s+key\s.*$", r"option key " +
                                "'" + self.passwd + "'", line)
                        line = re.sub(r'option\s+encryption\s.*$', r'option encryption ' +
                                "'" + self.encryption + "'", line)
                    out.write(line)
                out.close()
                os.rename(out_fname, fname)
                shutil.copy(fname, "/etc/config/wireless")
	
            cmd = "scripts/wifi_set_mode.sh sta"
            subprocess.call(cmd, shell=True)

        # Reset disconnectedCounter
        self.disconnectedCounter = 0

        # Restart Tornado (shell script bring it up whenever it exits)
        #cmd = "/etc/init.d/weio_run restart"
        #weioSubprocess.shellBlocking(cmd)
        print "======== EXIT TO GO TO SET CONNECTION ==============="
        os._exit(os.EX_OK)


    def getCurrentEssidName(self) :
        """Get current ESSID name from configuration file - wireless"""
        inputFile = open("/etc/config/wireless", 'r')
        rawData = inputFile.read()
        inputFile.close()

        lines = rawData.splitlines()
        for l in lines :
            if ("option ssid" in l) :
                name = l.split("       option ssid ")
                essid = name[1].split("'")
                return essid[1]


    def scan(self) :
        iwi = iwInfo.IWInfo(self.interface)

        return iwi.getData()
