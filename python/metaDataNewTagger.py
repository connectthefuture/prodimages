#!/usr/bin/env python

# #!/bin/bash
# 
# . ~/.bash_profile
# . ~/.bashrc
# 
# DATE=`date "+%Y-%m-%d"`
# DAY=`date "+%Y-%m-%d-RetouchToDo"`
# 
# searchDir="$1"
# 
# stylePath=`find $searchDir -iname \*[^2-9][0-9,{8}]_[1-6].\*`
# 
# for f in $stylePath:
# do
# style=`basename $f | awk -F_ '{ print $1 }'`
# paired=`echo "$style,$f"`
# 
# echo $paired >> $LIMBO/$DATE_tagpairs.csv
# 
# done


"""
Created on Fri Mar  8 14:48:56 2013

@author: jb
"""
def sqlQueryMetatags(style,f):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    
    
    querymake_metatags="SELECT DISTINCT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.BRAND.NAME AS brand, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') AS copy_dt, POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL AS category_parent, POMGR_SNP.PRODUCT_FOLDER.LABEL AS category_sub, MAX(ATG_SNP.EVENT.ID) AS event_id, POMGR_SNP.LK_PRODUCT_STATUS.NAME AS production_status, MAX(ATG_SNP.EVENT.EVENT_DESCRIPTION) AS event_title, MAX(to_date(POMGR_SNP.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')) AS sample_dt, MAX(POMGR_SNP.LK_SAMPLE_STATUS.NAME) AS sample_status, MAX(POMGR_SNP.PO_LINE.PO_HDR_ID) AS po_num, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style FROM POMGR_SNP.PRODUCT_COLOR LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON POMGR_SNP.PRODUCT_COLOR.ID = ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID LEFT JOIN ATG_SNP.EVENT ON ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID INNER JOIN POMGR_SNP.PRODUCT ON POMGR_SNP.PRODUCT_COLOR.PRODUCT_ID = POMGR_SNP.PRODUCT.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER ON POMGR_SNP.PRODUCT.PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER.ID INNER JOIN POMGR_SNP.BRAND ON POMGR_SNP.PRODUCT.BRAND_ID = POMGR_SNP.BRAND.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED ON POMGR_SNP.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.ID LEFT JOIN POMGR_SNP.SAMPLE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.SAMPLE.PRODUCT_COLOR_ID LEFT JOIN POMGR_SNP.SAMPLE_TRACKING ON POMGR_SNP.SAMPLE.ID = POMGR_SNP.SAMPLE_TRACKING.SAMPLE_ID LEFT JOIN POMGR_SNP.LK_SAMPLE_STATUS ON POMGR_SNP.SAMPLE_TRACKING.STATUS_ID = POMGR_SNP.LK_SAMPLE_STATUS.ID LEFT JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.ID = '" + style + "' GROUP BY POMGR_SNP.PRODUCT_COLOR.ID, POMGR_SNP.BRAND.NAME, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD'), POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL, POMGR_SNP.PRODUCT_FOLDER.LABEL, POMGR_SNP.LK_PRODUCT_STATUS.NAME, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE ORDER BY POMGR_SNP.PRODUCT_COLOR.ID DESC"
    
    result = connection.execute(querymake_metatags)
    metatags = {}
    for row in result:
        metatag = {}        
        metatag['colorstyle'] = row['colorstyle']
        metatag['brand'] = row['brand']
        metatag['copy_dt'] = row['copy_dt']
        metatag['category_parent'] = row['category_parent']
        metatag['category_sub'] = row['category_sub']
        metatag['event_id'] = row['event_id']
        metatag['production_status'] = row['production_status']
        metatag['event_title'] = row['event_title']
        metatag['sample_dt'] = row['sample_dt']
        metatag['sample_status'] = row['sample_status']
        metatag['po_num'] = row['po_num']
        metatag['vendor_style'] = row['vendor_style']
        
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag
        
    connection.close()
    return metatags
    
    
    
#sqlQueryConsigRename(vnum, ponum)[vnum]    

import sys
import os
import glob
import sqlalchemy
glbdir = sys.argv[1]
#glbdir='/mnt/Post_Ready/aPhotoPush'
#glbdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117257'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')
globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*/*/*.jpg'))
#print globtoconvert

for f in globtoconvert:
    stylefile = os.path.basename(f)
    try:
        style = stylefile.split('_')[0]
        if style.isdigit():
            pass
        else:
            style = stylefile.split('.')[0][:9]
    except:
        print "Error --> {}".format(f)
        pass
    #print style, f
    ### string = key/val as k=filepath, val=all metadata as k/v pairs
    exiftoolstring = sqlQueryMetatags(style,f)
    
    
    for key,value in exiftoolstring.iteritems():
        full = str(value.values())
        print f, full
    
   #  #print globtoconvert
#     try:
#         name = os.path.basename(f)
#         vnumfile = os.path.splitext(name)
#         pdirname = os.path.dirname(f)
#         vnum = vnumfile[0]
#         ext = vnumfile[1]
#         ponum = pdirname.split('/')[-1]
#         altnum = vnum.split('_')[-1]
#         #altnum = '1'
#         vnum = vnum.split('_')[0]
#         exiftoolstring = sqlQueryConsigRename(vnum, ponum)
#         #print bflyfile
#         for key,value in exiftoolstring.iteritems():
#             style = str(value.values())            
#             #for kv in value:
#             #    style = value.values()
#             #print style            
#             newname = os.path.join(pdirname, str(style) + "_" + altnum + ext)
#                 
#             newname1 = newname.replace(vnum, '')
#             newname2 = newname1.replace('[', '')
#             newname3 = newname2.replace(']_.', '.')
#             newname4 = newname3.replace(']_', '_')
#             finalnewname = newname4
#             print finalnewname + '\t' + f
#             os.rename(f, finalnewname)
#             #print "HELPPLLLP"
#             break
#         
#     
#     except KeyError:
#         continue
#     except sqlalchemy.exc.DatabaseError:
#         continue
#         print "DBERR" + f
