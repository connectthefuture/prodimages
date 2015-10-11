#!/bin/bash

function cache_clear_dir_postapi ()
    {
    for f in $(find "$1" -maxdepth 1 -iname \*.jpg -exec basename {} \;| cut -c 1-9 | sort -nru); do
    curl -u stephen:parker -d colorstyle="${f}" -X POST http://prodimages.ny.bluefly.com/image-update/
    #/usr/local/batchRunScripts/python/newAll_Sites_CacheClear.py "$f";
    done ;
}

cache_clear_dir_postapi "$1" ;
