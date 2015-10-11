#!/bin/bash

. ~/.bash_profile



dbOutRaw=$LIMBO/iterateSpool.csv
dbOutClean=$LIMBO/sqlConsigRenameComplete.csv
textFileDir=/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/_textFiles
#rm $dbOutRaw ;
#touch $dbOutClean ;
#touch $dbOutRaw ;
textFiles=`find "$textFileDir" -iname \*.csv`
rm $dbOutClean ;
for textff in $textFiles
do
textf=`echo $textff | sed 's/\.csv//g'`
##echo $line ;
lines=`cat "$textf".csv_done.csv | xargs -L1` ;

for line in $lines
    do
    recCount=`echo $line | awk -F"," '{ print NF }'`
    ponumsql=`echo $line | awk -F"," '{ print $1 }'`
    vendornumsql=`echo $line | awk -F"," '{ print $2 }'`
    
##if [ "$(eval "echo \${$recCount[*]}")" != '2' ] ;
        ##echo $recCount
       

##    else ;
    
    sqlQuery='SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO AS "vendor_style", POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR AS "ponumber" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE POMGR_SNP.PRODUCT_SNAPSHOT.PO_HDR = '"'$ponumsql'"' AND POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO = '"'$vendornumsql'"' ;'
    
    echo -e "$sqlQuery" > $LIMBO/sqlIteratetmp.csv ;
    
    ##Bring in Spool settings to complete SQL file to run through SQLplus
    cat $LIBSRV/settingsSqlSpool.csv $LIMBO/sqlIteratetmp.csv > $LIMBO/sqlIterateSelect.csv;
    echo 'spool off' >> $LIMBO/sqlIterateSelect.csv;
    echo 'exit;' >> $LIMBO/sqlIterateSelect.csv;
    
    
    ###<----Make dbOutRaw
    $DSSPRDLOGIN @$LIMBO/sqlIterateSelect.csv;
    
    ###<----Fix the syntax errors migrating from oracle to mysql
    cat "$dbOutRaw" | sed s/'  '//g | sed s/'--'//g | sed s/' ,'/','/g | grep -e "," | sed s/', '/','/g >> "$dbOutClean" ;
    
    
##fi ;
    done;
        
        cat "$dbOutClean" | sort -t, -k2.1,2.9 -dr | uniq | grep -E [0-9A-Za-z] > "$textf".csv_done.csv ;
        
done;
