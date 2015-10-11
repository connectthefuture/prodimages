#!/bin/bash



function get_multiurl_header_size ()
    {
    URLS="$@"
    args=$(echo "${URLS}\n")
    {	
    for url in $args;
    do
        size=$(curl -A "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -sI "$url" | grep Content-Length | awk '{print $2}');
        wget --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -O $(echo "$url" | sed "s|.pct\&outputx\=583\&outputy\=700\&level\=1|_"${size:1:7}".jpg|g" | sed -E "s///g" | sed "s|http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=||g") "$url";
        done;
    }
}





x="nixcraft.com"
echo ${x:3:5}

urlslist=`echo http\://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms\?img\=332{0..9}{0..9}{0..9}{0..9}01.pct\&outputx\=583\&outputy\=700\&level\=1  | xargs  -n1`


cd /Users/johnb/Desktop/new

get_multiurl_header_size "$urlslist"