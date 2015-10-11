#!/bin/bash

DAY=`date "+%Y-%m-%d-RetouchToDo"`

#metaTagSed=`cat /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/TableWithPathRecentCSVTags.csv` ;
#metaTagFix=`echo $metaTagSed > /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/styleFixed.csv` ;

cat /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/header_7_MetaCsv.csv /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/AlfrescoCSVTags.csv > /mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/AlfrescoCSVTagsHeaded.csv ;
exiftool -r -f -P -fast2 -overwrite_original_in_place -m -csv='/mnt/Post_Complete/CSV_updates/PrdExtra_Photoshop_Logs/AlfrescoCSVTagsHeaded.csv' /mnt/Post_Ready/zAlfresco_Primary/Alfresco_Batch_Import/Images
exit;
