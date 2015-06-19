#!/bin/bash

. ~/.bash_profile



fname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -200 -exec ls -cltrs {} \;| awk '{ print $NF }' | tail -5)
sizefname=$(find /mnt/Post_Complete/ImageDrop/bkup/*LSTransfer* -type f -mmin -200  | xargs ls -lrSh | awk '{ print $NF }')

allfiles=`cat ${fname[@]} | grep \.*ng | wc -l`
primaryonly=`cat ${fname[@]} | grep \_m.*pg | wc -l`
altonly=`cat ${fname[@]} | grep \_alt0?.*ng | wc -l`
process_time=`ls -cltrs ${fname[-1]} | awk '{print $7,$8,$9}'`

main_styles_list=$(cat ${fname[@]} | grep \_m.jpg | awk '{ print $NF }' | cut -c1-9 | sort -run | awk '{ print ",""\""$NF"\""}' | sed 's/ //g' | sed 's/,//1')
alt_styles_list=$(cat ${fname[@]} | grep \_alt0?.*ng | awk '{ print $NF }' | cut -c1-9 | sort -run | awk '{ print ",""\""$NF"\""}' | sed 's/ //g' | sed 's/,//1')

# Format string as list for MySQL IN clause
# mainstyles=`echo "(" $(echo $main_styles_list) ")"| sed 's/ //g' | sed 's/,//1'`
mainstyles=`echo -e "( $(echo -e ${main_styles_list} | tr -s ' ' ',') )"`
altstyles=`echo -e "( $(echo -e ${alt_styles_list} | tr -s ' ' ',') )"`
# altstyles=`echo "( $(echo $alt_styles_list | sed 's/ //g' | sed 's/,//1') )"`

#echo  "${allfiles} files - ${mainstyles} Styles at ${process_time} ${altonly} --- ${main_styles_list} - ${alt_styles_list}"
msql="select distinct count(colorstyle) as style_ct, brand, product_type, sum(CASE WHEN production_complete_dt = current_date() THEN 1 WHEN image_ready_dt is null THEN 1 ELSE 0 END) complete_today from product_snapshot_vendor where colorstyle in ${mainstyles} group by brand, product_type order by 1 desc, 2 asc;"
# asql="select distinct count(colorstyle) as style_ct, brand, product_type, sum(CASE WHEN production_complete_dt = current_date() THEN 1 WHEN image_ready_dt is null THEN 1 ELSE 0 END) complete_today from product_snapshot_vendor where colorstyle in ${altstyles} group by brand, product_type order by 1 desc, 2 asc;"
#echo "$msql"
#echo "$asql"
main_results=`mysql --host=127.0.0.1 --port=3301 --column-names=True --table -H --user=root --password=mysql -e "$msql" -D www_django`
# alt_results=`mysql --host=127.0.0.1 --port=3301 --column-names=True --table -H --user=root --password=mysql -e "$asql" -D www_django`


subject=$(echo -e "Last Hours Total Styles: ${primaryonly} -- Alts Only ${altonly}")
#subject=$(echo -e "Last Upload Total Styles: ${primaryonly} -- Alts Only ${altonly}  at ${process_time}")

#content=$(echo -e "Primary-Images: \t\t\t\t${primaryonly} \nAlt-Images: \t\t\t\t${altonly}  \n\n\nMain-Results --> \n\n\n\n${main_results} \n -----\n\n\nAlt-Results --> \n\n\n\n${alt_results} \n-----XX---- \n\n\n\v\v${msql}")
# $(for X in ${alt_styles_list}; do echo \"${X}\";done) -- $(for X in ${main_styles_list};do echo \"${X}\"; done)"`
# content=`echo "<html><body><table><tr>Total Styles: ${allfiles} </tr><tr>Main Images Total: ${primaryonly} </tr><tr>Total Alts: ${altonly}</tr></table><table> $(for X in ${alt_styles_list}; do echo "<tr>${X}</tr>";done)</table><table> $(for X in ${main_styles_list};do echo "<tr>${X}</tr>"; done) </table></body></html>"`

content=$(echo -e "${main_results}")


/usr/local/batchRunScripts/python/mailHTMLpythonSSL.py "${content}" "${subject}"

echo -e "${content}"

