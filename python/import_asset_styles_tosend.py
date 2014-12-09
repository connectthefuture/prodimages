#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on sun March 18 14:48:56 2014

@author: jbragato
"""
#orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')

def sqlQueryAssetStyles():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_asset_ready='''SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO AS "vendor_style", SUM(POMGR_SNP.PRODUCT_SNAPSHOT.TOTAL_RECVD) AS "received_ct",SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) AS "available_ct", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME AS "gender", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME AS "category", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME AS "product_type", POMGR_SNP.PRODUCT_SNAPSHOT.ACTIVE AS "active", POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE AS "start_dt", POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY AS "image_ready_dt" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE SUBSTR(POMGR_SNP.PRODUCT_SNAPSHOT.SKU,1,1) not like 1 AND POMGR_SNP.PRODUCT_SNAPSHOT.SAMPLE_STATUS_DATE >= (SysDate - 90) GROUP BY POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE, POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME, POMGR_SNP.PRODUCT_SNAPSHOT.ACTIVE, POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE, POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY ORDER BY "image_ready_dt" DESC, "active" DESC'''
    #querymake_asset_ready='''SELECT DISTINCT POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE AS "colorstyle", POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO AS "vendor_style", SUM(POMGR_SNP.PRODUCT_SNAPSHOT.TOTAL_RECVD) AS "received_ct",SUM(POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND) AS "available_ct", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME AS "gender", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME AS "category", POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME AS "product_type", POMGR_SNP.PRODUCT_SNAPSHOT.ACTIVE AS "active", POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE AS "start_dt", POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY AS "image_ready_dt" FROM POMGR_SNP.PRODUCT_SNAPSHOT WHERE POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE < TRUNC(SysDate) AND POMGR_SNP.PRODUCT_SNAPSHOT.TOTAL_RECVD > 0 AND POMGR_SNP.PRODUCT_SNAPSHOT.AVAILABLE_ON_HAND > 0 GROUP BY POMGR_SNP.PRODUCT_SNAPSHOT.COLORSTYLE, POMGR_SNP.PRODUCT_SNAPSHOT.VENDOR_STYLE_NO, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL2_NAME, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL3_NAME, POMGR_SNP.PRODUCT_SNAPSHOT.LEVEL4_NAME, POMGR_SNP.PRODUCT_SNAPSHOT.ACTIVE, POMGR_SNP.PRODUCT_SNAPSHOT.START_DATE, POMGR_SNP.PRODUCT_SNAPSHOT.IMAGE_READY ORDER BY "colorstyle" DESC'''
    result = connection.execute(querymake_asset_ready)
    asset_styles = {}
    for row in result:
        asset_styles = {}
        asset_styles['colorstyle'] = row['colorstyle']
        asset_styles['vendor_style'] = row['vendor_style']
        asset_styles['received_ct'] = row['received_ct']
        asset_styles['available_ct'] = row['available_ct']
        asset_styles['gender'] = row['gender']
        asset_styles['category'] = row['category']
        asset_styles['product_type'] = row['product_type']
        asset_styles['active'] = row['active']
        asset_styles['start_dt'] = row['start_dt']
        asset_styles['image_ready_dt'] = row['image_ready_dt']
        asset_styles[row['colorstyle']] = asset_styles
    connection.close()
    return asset_styles

#### Run Import To Mysql
import sys
import os
import sqlalchemy


asset_styles = sqlQueryAssetStyles()
print "Offshore Gotten"
## Truncate Prior to Inserting new data
#mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
#connection1 = mysql_engine.connect()
#trunc_table = """TRUNCATE TABLE asset_status"""
#connection1.close()

## Trunc www_django vers wont TRUNC du to Foreign Keys
#mysql_engine_dj  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
#connectiondj = mysql_engine_dj.connect()
#trunc_table = """TRUNCATE TABLE asset_status"""
#connectiondj.close()


for k,v in asset_styles.iteritems():
    import datetime
    print "Off"
    try:
        mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
        connection_data = mysql_engine_data.connect()
        connection_www = mysql_engine_www.connect()
        print "Connext"
        try:
            print "Begin Execute"
            connection_www.execute("""INSERT INTO asset_status (colorstyle, vendor_style, received_ct, available_ct, gender, category, product_type, active, start_dt, image_ready_dt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            ON DUPLICATE KEY UPDATE
                        vendor_style       = VALUES(vendor_style),
                        received_ct        = VALUES(received_ct),
                        available_ct       = VALUES(available_ct),
                        gender             = VALUES(gender),
                        category           = VALUES(category),
                        product_type       = VALUES(product_type),
                        active             = VALUES(active),
                        start_dt           = VALUES(start_dt),
                        image_ready_dt     = VALUES(image_ready_dt);
                        """, str(k), v['vendor_style'], v['received_ct'], v['available_ct'], v['gender'], v['category'], v['product_type'], v['active'], v['start_dt'], v['image_ready_dt'])
            print "Successful Insert asset_status --> {0}".format(k)
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
    except sqlalchemy.exc.IntegrityError:
        print "Duplicate Entry {0}".format(k)
    except sqlalchemy.exc.DatabaseError:
        continue
        print "DBERR" + k



        ## must move this section above similar www_django one
        ## data_imagepaths
#        try:
#            connection_www.execute("""
#                    INSERT INTO asset_status
#                        (colorstyle, vendor_style, received_ct, available_ct, gender, category, product_type, active, start_dt, image_ready_dt)
#                        (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
#                    ON DUPLICATE KEY UPDATE
#                        vendor_style       = VALUES(vendor_style),
#                        received_ct        = VALUES(received_ct),
#                        available_ct       = VALUES(available_ct),
#                        gender             = VALUES(gender),
#                        category           = VALUES(category),
#                        product_type       = VALUES(product_type),
#                        active             = VALUES(active),
#                        start_dt           = VALUES(start_dt),
#                        image_ready_dt     = VALUES(image_ready_dt);
#                        """, v['colorstyle'], v['vendor_style'], v['received_ct'],
#                             v['available_ct'], v['gender'], v['category'], v['product_type'],
#                             v['active'], v['start_dt'], v['image_ready_dt'])
#            print "Successful Insert asset_status --> {0}".format(k)
            #print "Updated Entry {0}".format(k)
#            print "Duplicate Entry {0}".format(k)





#     except KeyError:
#         continue
