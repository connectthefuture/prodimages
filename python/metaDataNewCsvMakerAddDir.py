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
        metatag['Keywords'] = row['brand']
        metatag['IPTC:SpecialInstructions'] = row['copy_dt']
        metatag['XMP:Genre'] = row['category_parent'] + "_" + row['category_sub']
        #metatag['category_sub'] = row['category_sub']
        metatag['XMP:Album'] = row['event_id']
        metatag['IPTC:CopyrightNotice'] = row['production_status']
        metatag['IPTC:Credit'] = row['event_title']
        metatag['IPTC:Source'] = row['sample_dt']
        metatag['IPTC:SimilarityIndex'] = row['sample_status']
        metatag['IPTC:PONumber'] = row['po_num']
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        #metatag['SourceFile'] = str(f)
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag
        
    connection.close()
    return metatags
    
    
def newDatedCsvWriter(lines):
    import csv, string, datetime
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter=',')
            writer.writerows([lines])

def csv_readfile(csvfile):
    with open(csvfile, 'rb') as f:
        readfile = csv.reader(f, delimiter=",")
        rows = []
        for row in readfile: 
            rows.append(row)
        return sorted(rows)

#def writeXmp(imgfile,xmpkey,xmpvalue):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[xmpkey] = xmpvalue
#    
#def writeIptc(imgfile,iptckey,iptcvalue):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[iptckey] = iptcvalue
#
#def writeExif(imgfile,exifkey,exifvalue):
#    import pyexiv2    
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[exifkey] = exifvalue
#
#def readIptc(imgfile):
#    import pyexiv2    
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    mdataprint = metadata.read()
#    print metadata

####### 
#####################
#######    
                                                

import sys
import os
import glob
import sqlalchemy,csv
#glbdir = sys.argv[1]
glbdir='/mnt/Post_Ready/aPhotoPush'
#glbdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117257'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')

globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*/*/*.jpg'))
#print globtoconvert

#for f in globtoconvert:
#    stylefile = os.path.basename(f)
#    style = stylefile.split('_')[0]
#    exiftoolstring = sqlQueryMetatags(style,f)
#    for key, values in exiftoolstring.iteritems():
#        #exifcmds = {}
#        for value in iter(values):
#            #exifcmd = {}
#            exifcmd = str('exiftool -' + "'" + value + "=" + str(values[value]) + "'" + '')
#            lines = str(exifcmd + " " + f)
#            #os.popen()
#            ###    Now MAke csv file with each tag as line of exiftool shell script
#            #print lines
#            newDatedCsvWriter([lines])
            
    
    
for f in globtoconvert:
    stylefile = os.path.basename(f)
    style = stylefile.split('_')[0]
    exiftoolstring = sqlQueryMetatags(style,f)
    for key, values in exiftoolstring.iteritems():
        for value in iter(values):
            exifcmd = str('exiftool -' + "'" + value + "=" + str(values[value]) + "'" + '')
            lines = str(exifcmd + " " + f)
            newDatedCsvWriter([lines])

