#!/bin/bash



function get_multiurl_header_size ()
    {
    URLS="$@"
    {	
    for url in ${URLS};
    do
        curl --user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3" -sI "$url" | grep Content-Length | awk '{print $2}';
    done;
    }
}







urlslist=`echo http\://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms\?img\=3156{0..9}{0..9}{0..9}{0..9}01.pct\&outputx\=583\&outputy\=700\&level\=1  | xargs  -n1`
 
cd /Users/johnb/Desktop/OldFirefoxData

get_multiurl_header_size "$urlslist"
