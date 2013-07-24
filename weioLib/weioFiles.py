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
# This file is part of WEIO
# WEIO is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WEIO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

import os
import weio_config
from collections import namedtuple

from os import listdir, sep
from os.path import abspath, basename, isdir
from sys import argv


_ntuple_diskusage = namedtuple('usage', 'total used free')


global htmlTree
    
# Tree function was originaly written by Doug Dahms
# Code was modified by Uros Petrevski


def tree(dir, padding, print_files=True):
    global htmlTree
    #print padding[:-1] + '<label for="folder">' + basename(abspath(dir)) + '/' + "</label><input type='checkbox' id='folder1' />" 
    htmlTree+=padding[:-1] + '<label for="folder">' + basename(abspath(dir)) + "</label><input type='checkbox' id='folder1' checked/>"
    htmlTree+="\n"
    #print "<ol>"
    htmlTree+="<ol>"
    htmlTree+="\n"
    padding = padding + ' '
    files = []
    if print_files:
        files = listdir(dir)
    else:
        files = [x for x in listdir(dir) if isdir(dir + sep + x)]
    count = 0
    for file in files:
        count += 1
        #print padding
        htmlTree+=padding
        htmlTree+="\n"
        path = dir + sep + file 
        if isdir(path):
            if count == len(files):
                #print "<li>"
                htmlTree+="<li>"
                htmlTree+="\n"
                tree(path, padding + '  ', print_files)
                #print "</li>"
                htmlTree+="</li>"
                htmlTree+="\n"
            else:
                #print "<li>"
                htmlTree+="<li>"
                htmlTree+="\n"
                tree(path, padding + ' ', print_files)
                #print "</li>"
                htmlTree+="</li>"
                htmlTree+="\n"
        else:
            #print padding + '<li class="file"><a href="">' + file + '</a></li>'
            # filer all osx crap DS_Store and all binary Python files
            if ((file != ".DS_Store") and (".pyc" not in file)) :
                fullpath =  "'" + dir + file + "'"
                htmlTree+=padding + '<li class="file"><a href="javascript:addNewEditorStrip('+fullpath+');">' + file + '</a>'
                htmlTree+='<a href="javascript:prepareToDeleteFile('+ fullpath +');">'
                htmlTree+='<i class="icon-remove" id="deleteFileButton" role="button" data-toggle="modal" href="javascript:prepareToDeleteFile('+ fullpath +');"></i>'
                htmlTree+='</a>'
                htmlTree+='</li>'
                htmlTree+="\n"

    #print "</ol>"
    htmlTree+="</ol>"
    htmlTree+="\n"

def getHtmlTree(path) :
    """Scans user folder and all folders inside that folder in search for files.
    Exports HTML string that can be directly used inside editor
    """
    global htmlTree
    htmlTree = "<li>"
    tree(path, " ")
    htmlTree+="</li>"
    print htmlTree
    return htmlTree

def listOnlyFolders(path):
    """Scan only folders. This is useful to retreive all project from user projects"""
    return os.walk(path).next()[1]
            
def getFileType(path):
    """Extracts file extension and matches with proper name"""
    extension = os.path.splitext(path)[1]
        
    types = {
    ".css" : "css",
    ".py": "python",
    ".js": "javascript",
    ".html":"html",
    ".txt" : "text",
    ".json": "json"
    }
     
    if (extension in types) :
        return types[extension]
    else :
        return "other"
         
def getFilenameFromPath(path):
    """Extracts filename from path"""
    return os.path.basename(path)
    
def getStinoFromFile(path):
    """Returns st_ino of file. This is used for unique file id number"""
    return os.stat(path).st_ino
    
def getRawContentFromFile(path):
    
    """Reads contents from given filename and returns it. Be aware that this function
     can explore the whole OS. Use checkIfPathIsInUserFolder(path) function to check if path is in user
     only folder."""
    
    inputFile = open(path, 'r')
    rawData = inputFile.read()
    inputFile.close()
    return rawData
    
def saveRawContentToFile(path, data):
    
    """Writes contents to given filename. Be aware that this function
     can explore the whole OS. Use checkIfPathIsInUserFolder(path) function to check if path is in user
     only folder."""
    
    inputFile = open(path, 'w')
    print(inputFile)
    ret = inputFile.write(data)
    inputFile.close()
    
        
def checkIfPathIsInUserFolder(path):
    
    """Checks if given path is in user folder"""
    confFile = weio_config.getConfiguration()
    pathToCurrentProject = confFile["user_projects_path"] + confFile['last_opened_project'] 
    
    if pathToCurrentProject in (path) :
        return True
    else :
        return False
        
def removeFile(path):
    """Removes specified file, if folder path is passed exception is rised"""
    os.remove(path)
    
def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in Megabytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total/1000000, used/1000000, free/1000000)
       
#print(scanFolders())
