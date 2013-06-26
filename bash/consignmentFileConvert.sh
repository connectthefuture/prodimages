#!/bin/bash


. ~/.bash_profile

vendorDrop=$PRODSRV/var/consignment
zipFiles=`find $vendorDrop -type f`
poNums=`find $vendorDrop -type f -exec basename {} \;| awk -F"." '{ print $1 }'`

echo $poNums/$zipFiles;
