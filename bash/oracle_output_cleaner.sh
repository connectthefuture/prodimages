#!/bin/bash

. ~/.bash_profile


## Use to Pipe input from SQLplus output and return cleaned removing spaces and dashes sorted

## echo "$@" | sed s/'  '//g | sed 's/CO||/COLOR_GROUP_ID||/1' | sed 's/COPY_READ||/COPY_READY||/1' |sed s/'--'//g | sed s/' ||'/'||'/g | sed s/'|| '/'||'/g | sort -k1.1,1.9 -dur | grep -e "||" | sed 's/||- /||/1' | sed 's/^ *//g'


echo "$@" | sed s/'  '//g | sed 's/COPY_READ~/COPY_READY~/1' | sed 's/CO~/COLOR_GROUP_ID/1' | sed s/'--'//g | sed s/' ~'/'~'/g | sed s/'~ '/'~'/g | sort -k1.1,1.9 -dur | grep -e "~" | sed 's/~- /~/1' | sed 's/~NULL\ /~NULL~/g' | sed 's/~~//g' | sed 's/COLOR_GROUP_IDCOPY_READ/COUNTRY_ORIGIN~COPY_READY||-/1' | sed -E 's/~-~~//1' | sed s/\'/\\\\\'/g | sed 's/^ *//g'
