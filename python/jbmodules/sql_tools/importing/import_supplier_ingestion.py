#!/usr/bin/env python


"""
Created on mo jun 9 20:48:56 2014

@author: jb
"""
def sqlQuerySupplierIngest():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    querymake_supplier_ingest="""SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR AS "colorstyle",
                              POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID                           AS "vendor_name",
                              POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND                        AS "vendor_brand",
                              POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE                        AS "vendor_style",
                              POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY                    AS "bfly_product_path",
                              POMGR.SUPPLIER_INGEST_IMAGE.URL                                 AS "image_url",
                              POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED                          AS "image_download_valid",
                              POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER                        AS "alt",
                              POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID                            AS "ingest_style_id",
                              POMGR.PRODUCT_COLOR.COPY_READY_DT                               AS "copy_ready_dt",
                              POMGR.PRODUCT_COLOR.IMAGE_READY_DT                              AS "image_ready_dt",
                              POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT                      AS "production_complete_dt",
                              POMGR.PRODUCT_COLOR.ACTIVE                                      AS "active",
                              POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID                     AS "third_supplier_id",
                              POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE                        AS "create_dt",
                              POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_TYPE                          AS "image_type",
                              POMGR.SUPPLIER_INGEST_IMAGE.MODIFIED_DATE                       AS "modified_dt",
                              POMGR.PRODUCT_COLOR.START_DATE                                  AS "start_dt",
                              POMGR.PRODUCT_COLOR.VERSION                                     AS "version"
                            FROM
                              POMGR.SUPPLIER_INGEST_STYLE
                            RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU
                            ON
                              POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID
                            LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE
                            ON
                              POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID
                            RIGHT JOIN POMGR.PRODUCT_COLOR
                            ON
                              POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR = POMGR.PRODUCT_COLOR.ID
                            WHERE POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%%' and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER = '1'
                            and(POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE  > trunc(sysdate-30) or POMGR.SUPPLIER_INGEST_IMAGE.MODIFIED_DATE > trunc(sysdate-30))
                            ORDER BY 
                            POMGR.SUPPLIER_INGEST_IMAGE.MODIFIED_DATE desc nulls last,
                            POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last,
                            POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last,
                            POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND Nulls Last,
                            POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last,
                            POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last"""

    result = connection.execute(querymake_supplier_ingest)
    importdata = {}
    for row in result:
        importdata_tmp = {}
        importdata_tmp['colorstyle'] = row['colorstyle']
        importdata_tmp['vendor_style'] = row['vendor_style']
        importdata_tmp['po_number'] = 'x' #row['po_number']
        importdata_tmp['version'] = row['version']
        importdata_tmp['vendor_name'] = row['vendor_name']
        importdata_tmp['vendor_brand'] = row['vendor_brand']
        importdata_tmp['bfly_product_path'] = row['bfly_product_path']
        importdata_tmp['image_url'] = row['image_url']
        importdata_tmp['alt'] = row['alt']
        importdata_tmp['image_download_valid'] = row['image_download_valid']
        importdata_tmp['ingest_style_id'] = row['ingest_style_id']
        importdata_tmp['copy_ready_dt'] = row['copy_ready_dt']
        importdata_tmp['image_ready_dt'] = row['image_ready_dt']
        importdata_tmp['production_complete_dt'] = row['production_complete_dt']
        importdata_tmp['active'] = row['active']
        importdata_tmp['create_dt'] = row['create_dt']
        importdata_tmp['modified_dt'] = row['modified_dt']
        importdata_tmp['start_dt'] = row['start_dt']
        print row['colorstyle']

        ## colorstyle as dict KEY
        importdata[row['colorstyle']] = importdata_tmp

    connection.close()
    return importdata


def main():
    #### Run Import To Mysql
    import sys
    import os
    import sqlalchemy


    importdata = sqlQuerySupplierIngest()

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

    for k,v in importdata.iteritems():
        print k,v, "BEGIN"
        try:

            mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
            mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
            connection_data = mysql_engine_data.connect()
            connection_www = mysql_engine_www.connect()

            # try:
            #     connection_data.execute("""
            #             INSERT INTO supplier_ingest 
            #                 (colorstyle, vendor_style, po_number, version, vendor_name, vendor_brand, bfly_product_path, image_url, alt, image_download_valid, ingest_style_id, copy_ready_dt, image_ready_dt, production_complete_dt, active, create_dt, image_type, copy_ready_dt, modified_dt, start_dt)
            #                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            #             ON DUPLICATE KEY UPDATE 
            #                 version  = VALUES(version), 
            #                 vendor_name  = VALUES(vendor_name), 
            #                 vendor_brand  = VALUES(vendor_brand), 
            #                 bfly_product_path  = VALUES(bfly_product_path), 
            #                 image_url  = VALUES(image_url), 
            #                 alt  = VALUES(alt), 
            #                 image_download_valid  = VALUES(image_download_valid), 
            #                 ingest_style_id  = VALUES(ingest_style_id), 
            #                 copy_ready_dt  = VALUES(copy_ready_dt), 
            #                 image_ready_dt  = VALUES(image_ready_dt), 
            #                 production_complete_dt           = VALUES(production_complete_dt), 
            #                 active     = VALUES(active), 
            #                 create_dt       = VALUES(create_dt), 
            #                 image_type     = VALUES(image_type), 
            #                 copy_ready_dt        = VALUES(copy_ready_dt), 
            #                 modified_dt = VALUES(modified_dt), 
            #                 start_dt        = VALUES(start_dt);
            #                        """, v['version'], v['vendor_name'], v['vendor_brand'], v['bfly_product_path'], v['image_url'], v['alt'], v['image_download_valid'], v['ingest_style_id'], v['copy_ready_dt'], v['image_ready_dt'], v['production_complete_dt'], v['active'], v['create_dt'], v['image_type'], v['copy_ready_dt'], v['modified_dt'], v['start_dt'])
            # except sqlalchemy.exc.IntegrityError:
            #     print "Duplicate Entry {0}".format(k)
            
            
            

            try:
                connection_www.execute("""INSERT INTO supplier_ingest (colorstyle, vendor_style, po_number, version, vendor_name, vendor_brand, bfly_product_path, image_url, alt, image_download_valid, ingest_style_id, copy_ready_dt, image_ready_dt, production_complete_dt, active, create_dt, modified_dt, start_dt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                version  = VALUES(version), 
                vendor_name  = VALUES(vendor_name), 
                vendor_brand  = VALUES(vendor_brand), 
                bfly_product_path  = VALUES(bfly_product_path), 
                image_url  = VALUES(image_url), 
                alt  = VALUES(alt), 
                image_download_valid  = VALUES(image_download_valid),
                ingest_style_id  = VALUES(ingest_style_id), 
                copy_ready_dt  = VALUES(copy_ready_dt), 
                image_ready_dt  = VALUES(image_ready_dt), 
                production_complete_dt = VALUES(production_complete_dt), 
                active = VALUES(active), 
                create_dt = VALUES(create_dt), 
                modified_dt = VALUES(modified_dt), 
                start_dt = VALUES(start_dt);""", v['colorstyle'], v['vendor_style'], v['po_number'], v['version'], v['vendor_name'], v['vendor_brand'], v['bfly_product_path'], v['image_url'], v['alt'], v['image_download_valid'], v['ingest_style_id'], v['copy_ready_dt'], v['image_ready_dt'], v['production_complete_dt'], v['active'], v['create_dt'], v['modified_dt'], v['start_dt'])

                print "Inserted {0}".format(k)

            except sqlalchemy.exc.IntegrityError:
                print "Duplicate Entry {0}".format(k)
            
            except sqlalchemy.exc.OperationalError:
                print "Invalid Path or Entry {0}".format(k)

            
            #print "Successful Insaert Push_Photoselecs --> {0}".format(k)


        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
        # except sqlalchemy.exc.DatabaseError:
        #     continue
        #     print "DBERR" + k

        # except KeyError:
        #     continue

if __name__ == '__main__':
    main()

