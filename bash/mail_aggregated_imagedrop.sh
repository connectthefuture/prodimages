#!/bin/bash

#. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -200 -exec ls -cltrs {} \;| awk '{ print $NF }' | tail -1)

allfiles=`cat "$fname" | grep \.*ng | wc -l`
primaryonly=`cat "$fname" | grep \_m.*pg | wc -l`
altonly=`cat "$fname" | grep \_alt0?.*ng | wc -l`
process_time=`ls -cltrs "$fname" | awk '{print $7,$8,$9}'`

main_styles_list=$(cat "$fname" | grep \_m.jpg | awk '{ print $NF }' | cut -c1-9 | sort -run | awk '{ print ",""\""$NF"\""}' | sed 's/ //g' | sed 's/,//1')
alt_styles_list=$(cat "$fname" | grep \_alt0?.*ng | awk '{ print $NF }' | cut -c1-9 | sort -run | awk '{ print ",""\""$NF"\""}' | sed 's/ //g' | sed 's/,//1')


# Format string as list for MySQL IN clause
# mainstyles=`echo "(" $(echo $main_styles_list) ")"| sed 's/ //g' | sed 's/,//1'`
mainstyles=`echo "( $(echo ${main_styles_list} | tr -s ' ' ',') )"`
altstyles=`echo "( $(echo ${alt_styles_list} | tr -s ' ' ',') )"`
# altstyles=`echo "( $(echo $alt_styles_list | sed 's/ //g' | sed 's/,//1') )"`

#echo  "${allfiles} files - ${mainstyles} Styles at ${process_time} ${altonly} --- ${main_styles_list} - ${alt_styles_list}"
msql="select distinct count(colorstyle) as style_ct, brand, category, (CASE WHEN (production_complete_dt = sysdate) or (image_ready_dt is null and copy_ready_dt is not null) THEN 1 ELSE 0 END) complete_today from product_snapshot_vendor where colorstyle in ${mainstyles} group by brand, category order by 1 desc, 2 asc;"
asql="select distinct count(colorstyle) as style_ct, brand, category, (CASE WHEN (production_complete_dt = sysdate) or (image_ready_dt is null and copy_ready_dt is not null) THEN 1 ELSE 0 END) complete_today from product_snapshot_vendor where colorstyle in ${altstyles} group by brand, category order by 1 desc, 2 asc;"
echo "$msql"
echo "$asql"
main_results=$(mysql --host=127.0.0.1 --port=3301 --column-names=True --table --user=root --password=mysql -e "${msql}" -D www_django)
alt_results=$(mysql --host=127.0.0.1 --port=3301 --column-names=True --table --user=root --password=mysql -e "${asql}" -D www_django)

#
# $(mysql --host=127.0.0.1 --port=3301 --column-names=False --user=root --password=mysql -e """select distinct t1.colorstyle from image_update t1 join product_snapshot_vendor t2 on t1.colorstyle=t2.colorstyle where t2.colorstyle in ('',''));""" -D www_django);

# aggregates="PLACE_HOLDER"

subject=$(echo "Last Upload: ${allfiles} Files - Total Styles: ${primaryonly} at ${process_time}")

content=$(echo "Total Styles: ${allfiles} \nPrimary-Images: ${primaryonly} \t Alt-Images: ${altonly} \n\n---- Main-Results --> \n\n${main_results} \n\n\n----> Alt-Results -->\n\n ${alt_results}") ## --- \n -- ${msql} - ${asql}")

# $(for X in ${alt_styles_list}; do echo \"${X}\";done) -- $(for X in ${main_styles_list};do echo \"${X}\"; done)"`
#content=`echo "<html><body><table><tr>Total Styles: ${allfiles} </tr><tr>Main Images Total: ${primaryonly} </tr><tr>Total Alts: ${altonly}</tr></table><table> $(for X in ${alt_styles_list}; do echo "<tr>${X}</tr>";done)</table><table> $(for X in ${main_styles_list};do echo "<tr>${X}</tr>"; done) </table></body></html>"`


/usr/local/batchRunScripts/python/mailGmailStdOut.py "${content}" "${subject}"

echo "${subject} -- \\\\n ${content}"
