#!/bin/bash

#. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -200 -exec ls -cltrs {} \;| awk '{ print $NF }' | tail -1)

allfiles=`cat "$fname" | grep \.*ng | wc -l`
primaryonly=`cat "$fname" | grep \_m.*pg | wc -l`
altonly=`cat "$fname" | grep \_alt0?.*ng | wc -l`
process_time=`ls -cltrs "$fname" | awk '{print $7,$8,$9}'`

main_styles_list=`cat "$fname" | grep \_m.jpg | awk '{ print $NF }' | cut -c1-9 | sort -run | awk '{ print ",""\""$NF"\""}'`
alt_styles_list=`cat "$fname" | grep \_alt0?.*ng | awk '{ print $NF }' | cut -c1-9 | sort -run | awk '{ print ",""\""$NF"\""}'`


# Format string as list for MySQL IN clause
mainstyles=`echo "(" $(echo $main_styles_list) ")"| sed 's/ //g' | sed 's/,//1'`
altstyles=`echo "(" $(echo $alt_styles_list) ")"| sed 's/ //g' | sed 's/,//1'`

echo  "${allfiles} files - ${primaryonly} Styles at ${process_time} ${altonly} --- ${main_styles_list} - ${alt_styles_list}"

main_results=`mysql --host=127.0.0.1 --port=3301 --column-names=True --table --user=root --password=mysql -e "select distinct count(colorstyle) as style_ct, brand from product_snapshot_live where colorstyle in ${mainstyles} group by brand order by 1 desc;" -D www_django`;

alt_results=`mysql --host=127.0.0.1 --port=3301 --column-names=True --table --user=root --password=mysql -e "select distinct count(colorstyle) as style_ct, brand from product_snapshot_live where colorstyle in ${altstyles} group by brand order by 1 desc;" -D www_django`;

#
# $(mysql --host=127.0.0.1 --port=3301 --column-names=False --user=root --password=mysql -e """select distinct t1.colorstyle from image_update t1 join product_snapshot_live t2 on t1.colorstyle=t2.colorstyle where t2.colorstyle in ('',''));""" -D www_django);

aggregates="PLACE_HOLDER"

subject=$(echo "Most_Recent_Upload: ${allfiles} files - ${primaryonly} Styles at ${process_time}")
content=`echo "Total Styles: ${allfiles} Main Images Total: ${primaryonly} Total Alts: ${altonly} \n---- Main-Results --> ${main_results} \n----> Alt-Results --> ${alt_results} --- \n -- ${main_styles_list} - ${alt_styles_list}"`

# $(for X in ${alt_styles_list}; do echo \"${X}\";done) -- $(for X in ${main_styles_list};do echo \"${X}\"; done)"`
#content=`echo "<html><body><table><tr>Total Styles: ${allfiles} </tr><tr>Main Images Total: ${primaryonly} </tr><tr>Total Alts: ${altonly}</tr></table><table> $(for X in ${alt_styles_list}; do echo "<tr>${X}</tr>";done)</table><table> $(for X in ${main_styles_list};do echo "<tr>${X}</tr>"; done) </table></body></html>"`


/usr/local/batchRunScripts/python/mailGmailStdOut.py "${content}" "${subject}"

echo "${subject} -- \\\\n ${content}"
