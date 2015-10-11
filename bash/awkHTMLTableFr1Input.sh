#!/bin/bash
. ~/.bash_profile

awk -F="\n" 'BEGIN{print "<table>"} {print "<tr>";for(i=1;i<=NF;i++)print "<td>" $i"</td>";print "</tr>"} END{print "</table>"}' $1
