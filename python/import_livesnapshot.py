#!/usr/bin/env python


"""
Created on sun jul 22 14:48:56 2013

@author: jb
"""
def sqlQuerylivesnapshot():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    querymake_livesnapshot="SELECT DISTINCT MAX(POMGR.PRODUCT_COLOR.ID) AS colorstyle,POMGR.BRAND.NAME AS brand,POMGR.LK_PRODUCT_STATUS.NAME AS production_status,MAX(POMGR.PO_LINE.PO_HDR_ID) AS po_number,MAX(POMGR.LK_SAMPLE_STATUS.NAME) AS sample_status,MAX(POMGR.SAMPLE_TRACKING.CREATE_DT) AS status_dt,POMGR.PRODUCT_COLOR.COPY_READY_DT AS copy_ready_dt,POMGR.PRODUCT_COLOR.IMAGE_READY_DT AS image_ready_dt,POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT AS production_complete_dt,POMGR.PRODUCT_COLOR.START_DATE AS start_dt,POMGR.PRODUCT_COLOR.ORIGINAL_START_DATE AS orig_start_dt,POMGR.LK_DEPT.NAME AS gender,POMGR.BUYER_PRODUCT_LINE.NAME AS category,MAX(POMGR.CATEGORY.NAME) AS product_type,POMGR.PRODUCT_COLOR_DETAIL.PHOTOGRAPHED_DATE AS sample_image_dt,POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style,POMGR.COLOR_GROUP.DESCRIPTION AS color,MAX(POMGR.PRODUCT_FOLDER.LABEL) AS product_subtype,MAX(POMGR.SAMPLE_TRACKING_NUMBER.SAMPLE_ID) AS sample_id,MAX(POMGR.SKU.SKU_CODE) AS sku,MAX(POMGR.TRACKING_NUMBER.REF_NUMBER) AS track_number,MAX(POMGR.TRACKING_NUMBER.CREATE_DT) AS track_dt,MAX(POMGR.LK_SAMPLE_LOCATION.NAME)AS sample_location,MAX(POMGR.USERS.USERNAME) AS track_user,POMGR.LK_PO_TYPE.NAME AS po_type FROM POMGR.PRODUCT_COLOR LEFT JOIN POMGR.COLOR_GROUP ON POMGR.PRODUCT_COLOR.COLOR_GROUP_ID = POMGR.COLOR_GROUP.ID LEFT JOIN POMGR.LK_PRODUCT_STATUS ON POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID LEFT JOIN POMGR.SKU ON POMGR.PRODUCT_COLOR.ID = POMGR.SKU.PRODUCT_COLOR_ID LEFT JOIN POMGR.PO_SKU ON POMGR.SKU.ID = POMGR.PO_SKU.SKU_ID LEFT JOIN POMGR.SAMPLE ON POMGR.SAMPLE.PO_SKU_ID = POMGR.PO_SKU.ID LEFT JOIN POMGR.SAMPLE_TRACKING ON POMGR.SAMPLE.ID = POMGR.SAMPLE_TRACKING.SAMPLE_ID LEFT JOIN POMGR.USERS ON POMGR.SAMPLE_TRACKING.USER_ID = POMGR.USERS.ID LEFT JOIN POMGR.LK_SAMPLE_STATUS ON POMGR.SAMPLE_TRACKING.STATUS_ID = POMGR.LK_SAMPLE_STATUS.ID LEFT JOIN POMGR.SAMPLE_TRACKING_NUMBER ON POMGR.SAMPLE_TRACKING.SAMPLE_ID = POMGR.SAMPLE_TRACKING_NUMBER.SAMPLE_ID LEFT JOIN POMGR.TRACKING_NUMBER ON POMGR.SAMPLE_TRACKING_NUMBER.TRACKING_NUMBER_ID = POMGR.TRACKING_NUMBER.ID LEFT JOIN POMGR.LK_SAMPLE_LOCATION ON POMGR.SAMPLE_TRACKING.LOCATION_ID = POMGR.LK_SAMPLE_LOCATION.ID LEFT JOIN POMGR.PO_LINE ON POMGR.PO_SKU.PO_LINE_ID = POMGR.PO_LINE.ID LEFT JOIN POMGR.PO_HDR ON POMGR.PO_LINE.PO_HDR_ID = POMGR.PO_HDR.ID LEFT JOIN POMGR.LK_PO_STATUS ON POMGR.PO_HDR.PO_STATUS_ID = POMGR.LK_PO_STATUS.ID LEFT JOIN POMGR.LK_PO_TYPE ON POMGR.PO_HDR.PO_TYPE_ID = POMGR.LK_PO_TYPE.ID LEFT JOIN POMGR.PRODUCT ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT.ID INNER JOIN POMGR.BRAND ON POMGR.PRODUCT.BRAND_ID = POMGR.BRAND.ID INNER JOIN POMGR.PRODUCT_FOLDER ON POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PRODUCT_FOLDER.ID LEFT JOIN POMGR.PRD_FDR_CAT_REL ON POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PRD_FDR_CAT_REL.FOLDER_ID LEFT JOIN POMGR.CATEGORY ON POMGR.CATEGORY.ID = POMGR.PRD_FDR_CAT_REL.CATEGORY_ID LEFT JOIN POMGR.BUYER_PRODUCT_LINE ON POMGR.PRODUCT.BUYER_PRODUCT_LINE_ID = POMGR.BUYER_PRODUCT_LINE.ID LEFT JOIN POMGR.LK_DEPT ON POMGR.LK_DEPT.ID = POMGR.BUYER_PRODUCT_LINE.DEPT_ID LEFT JOIN POMGR.SUPPLIER_INGEST_STYLE ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR WHERE POMGR.SAMPLE_TRACKING.CREATE_DT >= TRUNC(SysDate - 50) GROUP BY POMGR.BRAND.NAME,POMGR.LK_PRODUCT_STATUS.NAME,POMGR.PRODUCT_COLOR.COPY_READY_DT,POMGR.PRODUCT_COLOR.IMAGE_READY_DT,POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT,POMGR.PRODUCT_COLOR.START_DATE,POMGR.PRODUCT_COLOR.ORIGINAL_START_DATE,POMGR.LK_DEPT.NAME,POMGR.BUYER_PRODUCT_LINE.NAME,POMGR.PRODUCT_COLOR_DETAIL.PHOTOGRAPHED_DATE,POMGR.PRODUCT_COLOR.VENDOR_STYLE,POMGR.COLOR_GROUP.DESCRIPTION,POMGR.LK_PO_TYPE.NAME,POMGR.PRODUCT.BRAND_ID ORDER by MAX(POMGR.PRODUCT_COLOR.ID) ASC"
    result = connection.execute(querymake_livesnapshot)
    snapshot = {}
    for row in result:
        snapshot_tmp = {}
        snapshot_tmp['colorstyle'] = row['colorstyle']
        snapshot_tmp['brand'] = row['brand']
        snapshot_tmp['production_status'] = row['production_status']
        snapshot_tmp['po_number'] = row['po_number']
        snapshot_tmp['sample_status'] = row['sample_status']
        snapshot_tmp['status_dt'] = row['status_dt']
        snapshot_tmp['copy_ready_dt'] = row['copy_ready_dt']
        snapshot_tmp['image_ready_dt'] = row['image_ready_dt']
        snapshot_tmp['production_complete_dt'] = row['production_complete_dt']
        snapshot_tmp['start_dt'] = row['start_dt']
        snapshot_tmp['orig_start_dt'] = row['orig_start_dt']
        snapshot_tmp['gender'] = row['gender']
        snapshot_tmp['category'] = row['category']
        snapshot_tmp['product_type'] = row['product_type']
        snapshot_tmp['sample_image_dt'] = row['sample_image_dt']
        snapshot_tmp['vendor_style'] = row['vendor_style']
        snapshot_tmp['color'] = row['color']
        snapshot_tmp['product_subtype'] = row['product_subtype']
        snapshot_tmp['sample_id'] = row['sample_id']
        snapshot_tmp['sku'] = row['sku']
        snapshot_tmp['track_number'] = row['track_number']
        snapshot_tmp['track_dt'] = row['track_dt']
        snapshot_tmp['sample_location'] = row['sample_location']
        snapshot_tmp['track_user'] = row['track_user']
        snapshot_tmp['po_type'] = row['po_type']

        ## colorstyle as dict KEY
        snapshot[row['colorstyle']] = snapshot_tmp

    connection.close()
    return snapshot

#### Run Import To Mysql
import sys
import os
import sqlalchemy


livesnapshot = sqlQuerylivesnapshot()

## Truncate Prior to Inserting new data
#mysql_engine = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
#connection1 = mysql_engine.connect()
#trunc_table = """TRUNCATE TABLE product_snapshot_live"""
#connection1.close()

## Trunc www_django vers wont TRUNC du to Foreign Keys
#mysql_engine_dj  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
#connectiondj = mysql_engine_dj.connect()
#trunc_table = """TRUNCATE TABLE product_snapshot_live"""
#connectiondj.close()

for k,v in livesnapshot.iteritems():
    try:

        mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
        mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
        connection_data = mysql_engine_data.connect()
        connection_www = mysql_engine_www.connect()

        try:
            connection_data.execute("""
                    INSERT INTO product_snapshot_live 
                        (colorstyle, brand, production_status, po_number, sample_status, status_dt, copy_ready_dt, image_ready_dt, production_complete_dt, start_dt, orig_start_dt, gender, category, product_type, sample_image_dt, vendor_style, color, product_subtype, sample_id, sku, track_number, track_dt, sample_location, track_user, po_type) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        production_status       = VALUES(production_status), 
                        production_complete_dt  = VALUES(production_complete_dt), 
                        copy_ready_dt           = VALUES(copy_ready_dt), 
                        image_ready_dt          = VALUES(image_ready_dt), 
                        track_number            = VALUES(track_number), 
                        track_dt                = VALUES(track_dt), 
                        track_user              = VALUES(track_user), 
                        sample_image_dt         = VALUES(sample_image_dt), 
                        sample_id               = VALUES(sample_id), 
                        status_dt               = VALUES(status_dt), 
                        sample_status           = VALUES(sample_status);
                               """, v['colorstyle'], v['brand'], v['production_status'], v['po_number'], v['sample_status'], v['status_dt'], v['copy_ready_dt'], v['image_ready_dt'], v['production_complete_dt'], v['start_dt'], v['orig_start_dt'], v['gender'], v['category'], v['product_type'], v['sample_image_dt'], v['vendor_style'], v['color'], v['product_subtype'], v['sample_id'], v['sku'], v['track_number'], v['track_dt'], v['sample_location'], v['track_user'], v['po_type'])
            #print "Updated Entry {0}".format(k)
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
        
        
        
        print v['colorstyle']
        try:
            connection_www.execute("""
                    INSERT INTO product_snapshot_live 
                        (colorstyle, brand, production_status, po_number, sample_status, status_dt, copy_ready_dt, image_ready_dt, production_complete_dt, start_dt, orig_start_dt, gender, category, product_type, sample_image_dt, vendor_style, color, product_subtype, sample_id, sku, track_number, track_dt, sample_location, track_user, po_type) 
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        production_status       = VALUES(production_status), 
                        production_complete_dt  = VALUES(production_complete_dt), 
                        copy_ready_dt           = VALUES(copy_ready_dt), 
                        image_ready_dt          = VALUES(image_ready_dt), 
                        track_number            = VALUES(track_number), 
                        track_dt                = VALUES(track_dt), 
                        track_user              = VALUES(track_user), 
                        sample_image_dt         = VALUES(sample_image_dt), 
                        sample_id               = VALUES(sample_id), 
                        status_dt               = VALUES(status_dt), 
                        sample_status           = VALUES(sample_status);
                               """, v['colorstyle'], v['brand'], v['production_status'], v['po_number'], v['sample_status'], v['status_dt'], v['copy_ready_dt'], v['image_ready_dt'], v['production_complete_dt'], v['start_dt'], v['orig_start_dt'], v['gender'], v['category'], v['product_type'], v['sample_image_dt'], v['vendor_style'], v['color'], v['product_subtype'], v['sample_id'], v['sku'], v['track_number'], v['track_dt'], v['sample_location'], v['track_user'], v['po_type'])
            #print "Updated Entry {0}".format(k)
        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
        
        
        
        #print "Successful Insert Push_Photoselecs --> {0}".format(k)


    except sqlalchemy.exc.IntegrityError:
        print "Duplicate Entry {0}".format(k)
    except sqlalchemy.exc.DatabaseError:
        continue
        print "DBERR" + k

#     except KeyError:
#         continue
