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
#        metatag['colorstyle'] = row['colorstyle']
        metatag['IPTC:PONumber'] = row['po_num']
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        metatag['IPTC:Brand'] = row['brand']
        metatag['Keywords'] = row['brand']
        metatag['XMP:Genre'] = row['category_parent']
        metatag['IPTC:ProductType'] = row['category_sub']
        metatag['EventID'] = row['event_id']
        try:
            metatag['XMP:Album'] = "EventID " + str(row['event_id'])
        except:
            pass
        metatag['IPTC:Credit'] = row['event_title']
        metatag['IPTC:CopyrightNotice'] = row['production_status']

        if metatag['IPTC:CopyrightNotice'] == 'Production Incomplete':
            metatag['XMP:Label'] = 'Red'
        else:
            metatag['XMP:Label'] = 'Blue'
#        metatag['IPTC:SpecialInstructions'] = '{:%d-%m-%Y}'.format(row['copy_dt'])
#        metatag['IPTC:SpecialInstructions'] = row['copy_dt']
        metatag['IPTC:SimilarityIndex'] = row['sample_status']
#        metatag['IPTC:SampleStatusDate'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:Source'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:SampleStatusDate'] = row['sample_dt']
#        metatag['IPTC:Source'] = row['sample_dt']
#        metatag['SourceFile'] = f
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
globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*.??g'))
#print globtoconvert


def get_dbinfo_for_metatags_filelist(filelist):   
    metafield_dict = {}
    listed = []
    for f in filelist:
        stylefile = os.path.basename(f)
        style = stylefile.split('_')[0].strip('.png').strip('.jpg')
        #print style, f
        ### string = key/val as k=filepath, val=all metadata as k/v pairs
        exiftoolstring = sqlQueryMetatags(style,f)
        #pairs = zip(exiftoolstring.values(), exiftoolstring.keys())
    
        for k,v in exiftoolstring.iteritems():
            #full = tuple(value.values())
            #full = value
            tmpd = {}
            for val in v:
                #valpair = val,v[val]
                #listed.append
                tmpd[val] = v[val]
                listed.append(tmpd)
            metafield_dict[k] = tmpd

    return metafield_dict
    #return listed

        #pairs = zip(exiftoolstring.values(), exiftoolstring.keys())
    
#for f in globtoconvert:
#    metafield_dict = {}
#    style = stylefile.split('_')[0]
#    exiftoolstring = sqlQueryMetatags(style,f)
#    for k,v in exiftoolstring.items():
#        metatags = []
#        for val in v:
#            metapairs = val,v[val]
#            metapairs = tuple(metapairs)
#            metatags.append(metapairs)
#            #print metatags
#    metafield_dict[k] = metatags

metadict = get_dbinfo_for_metatags_filelist(globtoconvert)
exiftags = []
exifdict = {}
for k,v in metadict.items():
    metatags = []

    for val in v:
        #m = []
        filename = str(k)
        exiftag = val
        exifvalue = v[val]
        #exifpart = str(' -' + "'" + str(exiftag) + "=" + str(exifvalue) + "'" + ''),
        exifpart = "-'{exiftag}'='{exifvalue}'".format(exiftag=exiftag,exifvalue=exifvalue)
        #print exifpart
        #exifcmd = str('exiftool -' + "'" + str(exiftag) + "=" + str(exifvalue) + "'" + '')
        #lines = str(exifcmd + " " + filename)
        metatags.append(exifpart)
        #print metatags
        #m.append(exifpart)
        #print val,v[val]
    #exifdict[filename] = [x for x in metatags]
    #metatags = (str(tag) for tag in metatags)
    exifdict[filename] = " ".join(metatags)
#    for line in metatags:
#        print line[0]
#        exifcmd = str('exiftool -m -fast2 -q ' + line[0] + ' ' + filename)
#        exiftags.append(exifcmd)
execlist = []
for key,value in exifdict.iteritems():
    execstring = "exiftool -m -overwrite_original_in_place -fast2 -q {0} {1}".format(value,key)
    execlist.append(execstring)

def bashexec_subproc(cmdstring):
    import subprocess
    p = subprocess.Popen(cmdstring, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()
    return retval

for line in execlist:
    os.system(line)
    print line

#print execlist
#print exifdict
    

#         
#     
#     except KeyError:
#         continue
#     except sqlalchemy.exc.DatabaseError:
#         continue
#         print "DBERR" + f


