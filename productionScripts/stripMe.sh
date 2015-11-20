#!/bin/bash

# clean old file
#rm weio.tar.bz2

if [ -d weio ]; then
    rm -r weio
fi

# after all process to decompress type : tar -zxvf weio.tar.gz
# make new dir for stripped version at level -1
mkdir weio

# copy all visible files, ignore unvisible git files
rsync -av --exclude=".*" --exclude="productionScripts" ../ weio

# exclude production folders
rm -r weio/doc
rm -r weio/graphicsSource
rm -r weio/openWrt
rm -r weio/sandbox
rm -r weio/updateMaker
rm weio/README.md

# exclude local dependant symlinks that will break
rm -r weio/userFiles/examples
rm -r weio/userFiles/flash
rm weio/examples/userProjects/require.js

# kill all .pyc files to leave native arch to build them
find weio -name '*.pyc' -delete
# kill all .less files because they are compiled to .css
find weio -name '*.less' -delete
# kill all OS X crap
find weio -name '.DS_Store' -delete
# compress all html, css, js file
#find weio -name '*.html' -exec bash -c " html-minifier --remove-comments --use-short-doctype --collapse-whitespace -o {} {}" \; -print
#find weio -name '*.css' -exec bash -c "cleancss -o {} {}" \; -print
#find weio -name '*.js' -exec bash -c "uglifyjs {} --compress --mangle -o {}" \; -print
##find weio -name '*.sh' -exec bash -c "sed 's/^[#;] .*$//' {} | sed /^$/d  > {}" \; -print
##find . -name '*.py' -exec bash -c "sed 's/[#;].*$//' {} | sed /^$/d  > {}" \; -print

# compress in every case
tar -zcvf weio.tar.gz weio/

echo "WeIO stripped and compressed"
tar -zcvf weio.tar.gz weio/
# kill weio folder
rm -r weio

# To decompress type : tar -zxvf weio.tar.gz

echo ""
echo "Created archive weio.tar.gz"
echo ""
echo "Now do:"
echo "$ scp -r weio.tar.gz root@houat.local:/tmp"
echo "and then in WeIO:"
echo "tar -xzvf /tmp/weio.tar.gz"

# make tar archive
# if [ "$1" == "no_compression" ]; then
#     echo "WeIO stripped no compression is executed"
# else
#     echo "Patching WeIO project for production"
#     #patch weio/www/libs/weio/weioApi.js < 01_portChange.patch
#
#     echo "WeIO stripped and compressed"
#     tar -zcvf weio.tar.gz weio/
#     # kill weio folder
#     rm -r weio
#
#     # To decompress type : tar -zxvf weio.tar.gz
#
#     echo ""
#     echo "Created archive weio.tar.gz"
#     echo ""
#     echo "Now do:"
#     echo "$ scp -r weio.tar.gz root@houat.local:/tmp"
#     echo "and then in WeIO:"
#     echo "tar -xzvf /tmp/weio.tar.gz"
#
# fi
