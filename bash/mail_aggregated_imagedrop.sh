#!/bin/bash

. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -200 -exec ls -cltrs {} \;| awk '{ print $NF }' | tail -1)

allfiles=`cat "$fname" | grep \.png | wc -l`
primaryonly=`cat "$fname" | grep \_m.jpg | wc -l`
altonly=`cat "$fname" | grep \_alt0?.*ng | wc -l`
process_time=`ls -cltrs "$fname" | awk '{print $7,$8,$9}'`

main_styles_list=`cat "$fname" | grep \_m.jpg | awk '{ print $NF }' | cut -c1-9 | sort -run` 
alt_styles_list=`cat "$fname" | grep \_alt0?.*ng | awk '{ print $NF }' | cut -c1-9 | sort -run` 

echo  "${allfiles} files - ${primaryonly} Styles at ${process_time} ${altonly} --- ${main_styles_list} - ${alt_styles_list}"

subject=$(echo "Uploaded: ${allfiles} files - ${primaryonly} Styles at ${process_time}")
##content=`echo "<html><body><table><tr>Total Styles: ${allfiles} </tr><tr>Main Images Total: ${primaryonly} </tr><tr>Total Alts: ${altonly}</tr></table><table> $(for X in ${alt_styles_list}; do echo \"<tr>${X}</tr>\";done)</table><table> $(for X in ${main_styles_list};do echo \"<tr>${X}</tr>\"; done) </table></body></html>"`
content=`echo "<html><body><table><tr>Total Styles: ${allfiles} </tr><tr>Main Images Total: ${primaryonly} </tr><tr>Total Alts: ${altonly}</tr></table><table> $(for X in ${alt_styles_list}; do echo "<tr>${X}</tr>";done)</table><table> $(for X in ${main_styles_list};do echo "<tr>${X}</tr>"; done) </table></body></html>"`


/usr/local/batchRunScripts/python/mailGmailStdOut.py "${content}" "${subject}"

echo "${subject} -- \n ${content}"