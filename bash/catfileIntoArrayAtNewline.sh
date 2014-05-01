#/bin/bash
. ~/.bash_profile

FILE="$1"
old_IFS=$IFS
IFS=$'\n'
lines=($(cat $FILE)) # array
IFS=$old_IFS

for line in "${lines[@]}"; do echo $line | xargs ; done 



( set -f; IFS='
'; exec /bin/bash $(cat <FILE) )