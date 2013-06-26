#!/bin/bash

. ~/.bash_profile



/usr/local/batchRunScripts/searchStyle_formater.sh $1 $2 | awk -F~ -v RS="\n" 'BEGIN{print "<table>"} {print "<tr>";for(i=1;i<=NF;i++)print "<td>" $i"</td>";print "</tr>"} END{print "</table>"}'
