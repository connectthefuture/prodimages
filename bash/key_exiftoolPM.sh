#!/bin/bash
. ~/.bash_profile

FormatFile=$1
headersExif=`cat $FormatFile | grep -v "#"`
echo $headersExif | awk -F"," '{ print $1, $2, $3, $4, $5, $6, $7, $8, $9 }' | xargs -n1 | sed s/\\$/\/g | sed s/\{//g | sed s/\}//g | sed s/\\:/\/g | cat -n | xargs -n2 | sed 's/\ /,/' | sort -k 1.1,1.0 -n | sed 's/FileName/Style_Number/g' | sed 's/EXIFDateTimeOriginal/Photo_Date/g' | sed 's/XMPGenre/Product_Category/g' | sed 's/Keywords/Brand_Name/g' | sed 's/XMPAlbum/Event_Group/g' | sed 's/IPTCSource/Sample_Status/g' | sed 's/IPTCCopyrightNotice/Production_Status/g' | sed 's/IPTCSpecialInstructions/Start_Date/g' | sed 's/IPTCSimilarityIndex/Sample_Status_Date/g'
