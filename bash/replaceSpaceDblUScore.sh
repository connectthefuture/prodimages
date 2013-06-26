#!/bin/bash

. ~/.bash_profile


for d in `find "$@" -type d`
do
	
#	for f in `find $d -type f -iname \*.\*g`

cd $d
ls -1 | while read file; 
do 
new_file=$(echo $file | sed 's/\ /__/g'); 
mv "$file" "$new_file"; 
done;
done;
