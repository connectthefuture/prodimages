#!/bin/bash
. ~/.bash_profile


finddir="$@"

for f in `find $finddir -type f -iname \*.\*g`;
do
cd "$d" ; 
echo "$f"
	FILENAME="${f//[\?%\+\:\&\ \#\(\)]/_}";
	mv -f "$f" "$FILENAME"
done;
