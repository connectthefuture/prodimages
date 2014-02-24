#!/bin/bash

. ~/.bash_profile


fpath=$1

/usr/local/batchRunScripts/python/mtags_singlefile_RAW.py $fpath && /usr/local/batchRunScripts/python/organize_zimages_4digit.py $fpath
