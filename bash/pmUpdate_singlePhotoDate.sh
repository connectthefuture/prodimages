#!/bin/bash
. ~/.bash_profile


f="$1"

outName=`basename "$f" | sed s/_1.jpg//g`

curl -d sample_image=Y -d photographed_date=now -X PUT http://dmzimage01.l3.bluefly.com:8080/photo/"$outName"
