#!/usr/bin/env python

"""
Created on Fri Jun 28 14:48:56 2013

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
        metatag['IPTC:CopyrightNotice'] = row['vendor_style']
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


def get_dbinfo_for_metatags_singlefile(f):   
    metafield_dict = {}
    listed = []
    stylefile = os.path.basename(f)
    style = stylefile.split('_')[0]
    #print style, f
    ### string = key/val as k=filepath, val=all metadata as k/v pairs
    exiftoolstring = sqlQueryMetatags(style,f)
    #pairs = zip(exiftoolstring.values(), exiftoolstring.keys())

    for k,v in exiftoolstring.iteritems():
        tmpd = {}
        for val in v:
            tmpd[val] = v[val]
            listed.append(tmpd)
        metafield_dict[k] = tmpd

    return metafield_dict
    #return listed
    


##################### Begin CMDS ##############

import sys
import os
import glob
import sqlalchemy

filename=os.path.abspath(sys.argv[1])


metadict = get_dbinfo_for_metatags_singlefile(filename)
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
        metatags.append(exifpart)
        #print metatags
        #m.append(exifpart)
        #print val,v[val]
    #exifdict[filename] = [x for x in metatags]
    #metatags = (str(tag) for tag in metatags)
    exifdict[filename] = " ".join(metatags)

execlist = []
for key,value in exifdict.iteritems():
    execstring = "exiftool -m -overwrite_original_in_place -fast2 -q {0} {1}".format(value,key)
    execlist.append(execstring)

for line in execlist:
    try:
        os.system(line)
        print line
    except:
        pass
        
