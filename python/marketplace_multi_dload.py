#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sqlQuery_GetIMarketplaceImgs(ponum=None):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    if not ponum:
        query_marketplace_inprog = """SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%VAULT%' AND POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS NULL AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last"""  
    ## 
    ## WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    ## AND POMGR.PRODUCT_COLOR.COPY_READY_DT IS NOT NULL
    ##
    
    result = connection.execute(query_marketplace_inprog)
    styles = {}
    for row in result:
        styledata = {}           
        styledata['colorstyle'] = row['colorstyle']
        styledata['po_number'] = row['po_number']
        styledata['vendor_name'] = row['vendor_name']
        styledata['vendor_brand'] = row['vendor_brand']
        styledata['vendor_style'] = row['vendor_style']
        styledata['product_folder'] = row['product_folder']
        styledata['image_url'] = row['image_url']
        styledata['download_status'] = row['download_status']
        styledata['alt'] = row['alt']
        styledata['genstyleid'] = row['genstyleid']
        styledata['copy_ready_dt'] = row['copy_ready_dt']
        styledata['image_ready_dt'] = row['image_ready_dt']
        styledata['production_complete_dt'] = row['production_complete_dt']
        styledata['active'] = row['active']
        styledata['third_supplierid'] = row['third_supplierid']
        styledata['ingest_dt'] = row['ingest_dt']
        
        #consigstyle['vendor_style'] = row['vendor_style']
        styles[row['colorstyle']] = styledata
        
    #print consigstyles
    connection.close()
    return styles

############################################################ RUN ##################################################
############################################################ RUN ##################################################
import os,re,sys,urllib
import requests
from magick_cropandpad_x480 import subproc_pad_to_x480  as magickcrop480
from magick_cropandpad_x480 import subproc_pad_to_x1200 as magickcrop1200

imagedir = os.path.abspath(os.path.join(os.path.expanduser('~'),'Pictures'))
#if os.path.isdir(imagedir):
#    pass
#else:
#    imagedir = os.path.join(os.path.abspath(os.curdir), 'images_downloaded')
#    os.mkdir(imagedir, 0755 )


vaultstyles=sqlQuery_GetIMarketplaceImgs()
for k,v in vaultstyles.iteritems():
    colorstyle = k
    image_url  = v['image_url']
    alt_number = v['alt']
    ext = '.jpg'
    if alt_number != None:
        bfly_ext = "_{0}{1}".format(alt_number,ext)
        ext = bfly_ext
    destpath = os.path.join(imagedir, colorstyle + ext)

    if image_url:
        #with open(destpath,'wb') as f:
            #f.write(requests.get(image_url).content)
        print image_url, destpath.split('/')[-1].replace('.jpg','_1200.jpg')
        error_check = urllib.urlopen(image_url)
        urlcode_value = error_check.getcode()
        print urlcode_value
            
        if urlcode_value == 200:
            urllib.urlretrieve(image_url, destpath)
        #magickcrop1200(destpath, imagedir)#, os.path.join(imagedir,colorstyle + '_1200.jpg')) #os.path.abspath(os.path.join(imagedir, destpath.split('/')[-1].replace('.jpg','_1200.jpg'))))
        #magickcrop480(destpath, os.path.join(imagedir,colorstyle + '_l.jpg'))   # os.path.abspath(os.path.join(imagedir, destpath.split('/')[-1].replace('.jpg','_l.jpg'))))
        #magickcrop480(destpath, os.path.join(imagedir,colorstyle + '_m.jpg'))   #os.path.abspath(os.path.join(imagedir, destpath.split('/')[-1].replace('.jpg','_m.jpg'))))
        
