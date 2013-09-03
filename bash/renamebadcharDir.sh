#!/bin/bash
. ~/.bash_profile

SAVEIFS=$IFS

FILES=$1/*
  for f in $FILES
  do
  	echo "$f"
  	FILENAME="${f//[\?%\+]/_}";
  	mv "$f" "$FILENAME"
 done ;
IFS=$SAVEIFS
exit ;
