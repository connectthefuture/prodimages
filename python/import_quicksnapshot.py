#!/usr/bin/env python


"""
Created on sun jul 22 14:48:56 2013

@author: jb
"""
def sqlQuerylivesnapshot():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

        querymake_livesnapshot="""SELECT Distinct
          POMGR.PRODUCT_COLOR.ID                AS colorstyle,
          POMGR.PO_LINE.PO_HDR_ID               AS po_number,
          POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID AS vendor,
          POMGR.PRODUCT_COLOR.VENDOR_COLOR vendor_color,
          POMGR.COLOR_GROUP.DESCRIPTION AS color,
          POMGR.BRAND.NAME              AS brand,
          POMGR.PRODUCT_COLOR.VENDOR_STYLE vendor_style,
          POMGR.PRODUCT_COLOR.IMAGE_READY_DT AS image_ready_dt,
          POMGR.PRODUCT_COLOR.COPY_READY_DT copy_ready_dt,
          POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT   AS production_complete_dt,
          POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE     AS supplier_create_image,
          POMGR.SUPPLIER_INGEST_STYLE.MODIFIED_DATE    AS supplier_mod_style,
          POMGR.PRODUCT_COLOR.CREATED_DATE             AS prodclr_create,
          POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE        AS mainimage,
          POMGR.PRODUCT_COLOR_DETAIL.ZOOM_IMAGE        AS png,
          POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1 AS alt1,
          POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2 AS alt2,
          POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH AS swatch,
          POMGR.PRODUCT_COLOR_DETAIL.SHORT_NAME        AS shortname,
          POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION     AS version,
          POMGR.PRODUCT_FOLDER.NAME                    AS product_subtype,
          POMGR.PROD_FAMILY_DENORM_LK.PROD_DEPARTMENT  AS gender,
          POMGR.PROD_FAMILY_DENORM_LK.PROD_FAMILY_TREE AS category,
          PROD_FAMILY_DENORM_LK1.PROD_FAMILY_DESC      AS product_type
        FROM
          POMGR.PRODUCT_COLOR
        FULL JOIN POMGR.SUPPLIER_INGEST_STYLE
        ON
          POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR = POMGR.PRODUCT_COLOR.ID
        LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL
        ON
          POMGR.PRODUCT_COLOR.ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID
        LEFT JOIN POMGR.PO_LINE
        ON
          POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID
        LEFT JOIN POMGR.PRODUCT
        ON
          POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT.ID
        INNER JOIN POMGR.COLOR_GROUP
        ON
          POMGR.PRODUCT_COLOR.COLOR_GROUP_ID = POMGR.COLOR_GROUP.ID
        INNER JOIN POMGR.BRAND
        ON
          POMGR.BRAND.ID = POMGR.PRODUCT.BRAND_ID
        INNER JOIN POMGR.PRODUCT_FOLDER
        ON
          POMGR.PRODUCT_FOLDER.ID = POMGR.PRODUCT.PRODUCT_FOLDER_ID
        INNER JOIN POMGR.PROD_FAMILY_DENORM_LK
        ON
          POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PROD_FAMILY_DENORM_LK.PROD_FAMILY_ID
        INNER JOIN POMGR.PROD_FAMILY_DENORM_LK PROD_FAMILY_DENORM_LK1
        ON
          POMGR.PROD_FAMILY_DENORM_LK.PARENT_PROD_FAMILY_ID =
          PROD_FAMILY_DENORM_LK1.PROD_FAMILY_ID
        INNER JOIN POMGR.SUPPLIER_INGEST_IMAGE
        ON
          POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID
        WHERE
          POMGR.PRODUCT_COLOR.CREATED_DATE > SysDate - 150
        GROUP BY
          POMGR.PRODUCT_COLOR.ID,
          POMGR.PO_LINE.PO_HDR_ID,
          Pomgr.Product_Color.Vendor_Style,
          POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID,
          POMGR.PRODUCT_COLOR.VENDOR_COLOR,
          POMGR.BRAND.NAME,
          Pomgr.Product_Color.Created_Date,
          POMGR.PRODUCT_COLOR.IMAGE_READY_DT,
          POMGR.PRODUCT_COLOR.COPY_READY_DT,
          POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT,
          POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE,
          POMGR.SUPPLIER_INGEST_STYLE.MODIFIED_DATE,
          POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE,
          POMGR.PRODUCT_COLOR_DETAIL.ZOOM_IMAGE,
          POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1,
          POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2,
          POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH,
          Pomgr.Color_Group.Description,
          POMGR.PRODUCT_COLOR_DETAIL.SHORT_NAME,
          POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION,
          POMGR.PRODUCT_FOLDER.LABEL,
          POMGR.PRODUCT_FOLDER.NAME,
          POMGR.PROD_FAMILY_DENORM_LK.PROD_DEPARTMENT,
          POMGR.PROD_FAMILY_DENORM_LK.PROD_FAMILY_TREE,
          PROD_FAMILY_DENORM_LK1.PROD_FAMILY_DESC
        ORDER BY
          1 DESC Nulls Last"""
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
