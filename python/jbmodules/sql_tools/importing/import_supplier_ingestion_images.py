#!/usr/bin/env python


"""
Created on mo jun 9 20:48:56 2014

@author: jb
"""
def sqlQuerySupplierIngestImages():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    querymake_supplier_ingest_images="""SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR AS "colorstyle",
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
                            WHERE 
                              POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%%' 
                            and(POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE  > trunc(sysdate-30) or POMGR.SUPPLIER_INGEST_IMAGE.MODIFIED_DATE > trunc(sysdate-30))
                            ORDER BY 
                            POMGR.SUPPLIER_INGEST_IMAGE.MODIFIED_DATE desc nulls last,
                            POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last,
                            POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last,
                            POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND Nulls Last,
                            POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last,
                            POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last"""

    ## use as where to rm primary img --->  WHERE POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%%' AND POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER != '1'


    result = connection.execute(querymake_supplier_ingest_images)
    importdata = {}
    for row in result:
        importdata_tmp = {}
        importdata_tmp['colorstyle'] = row['colorstyle']
        importdata_tmp['vendor_style'] = row['vendor_style']
        importdata_tmp['po_number'] = 'x' #row['po_number']
        importdata_tmp['version'] = row['version']
        importdata_tmp['vendor_name'] = row['vendor_name']
        importdata_tmp['bfly_product_path'] = row['bfly_product_path']
        importdata_tmp['image_url'] = row['image_url']
        importdata_tmp['alt'] = row['alt']
        importdata_tmp['image_download_valid'] = row['image_download_valid']
        importdata_tmp['ingest_style_id'] = row['ingest_style_id']
        importdata_tmp['modified_dt'] = row['modified_dt']
        ## Set primary key and image location urls
        if row['alt'] != 1:
            primarykey  = '{0}_alt0{1}'.format(str(row['colorstyle']), str(int(row['alt']) - 1))
            srcLOCAL    = 'NotAvailable'
            srcZOOM     = 'http://images1.qa.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(primarykey, row['version'])
            siteZOOM    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(primarykey, row['version'])
            siteLIST    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(primarykey.split('_')[0])
            sitePDP     = 'http://is5.l3.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}'.format(primarykey, row['version'])
        elif row['alt'] == 1:
            primarykey  =  str(row['colorstyle'])
            srcLOCAL    = ''
            srcZOOM     = 'http://images1.qa.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(primarykey, row['version'])
            siteZOOM    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(primarykey, row['version'])
            siteLIST    = 'http://is5.l3.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=738&outputy=700&level=1&ver={1}'.format(primarykey, row['version'])
            sitePDP     = 'http://is5.l3.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}'.format(primarykey, row['version'])

        print primarykey
        importdata_tmp['bfly_local_src']  = srcLOCAL
        importdata_tmp['bfly_zoom_src']   = srcZOOM
        importdata_tmp['bfly_zoom_site']  = siteZOOM
        importdata_tmp['bfly_list_site']  = siteLIST
        importdata_tmp['bfly_pdp_site']  = sitePDP


        ## colorstyle and alt as dict KEY
        importdata[primarykey] = importdata_tmp

        ## colorstyle as dict KEY
        ## importdata[row['colorstyle']] = importdata_tmp

    connection.close()
    return importdata
def main():
    #### Run Import To Mysql
    import sys
    import os
    import sqlalchemy


    importdata = sqlQuerySupplierIngestImages()

    for k,v in importdata.iteritems():
        print "BEGIN-->\t", k
        try:

            mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
            mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
            connection_data = mysql_engine_data.connect()
            connection_www = mysql_engine_www.connect()

            try:
                connection_www.execute("""INSERT INTO supplier_ingest_images (file_name, colorstyle, vendor_style, po_number, version, vendor_name, bfly_product_path, image_url, alt, image_download_valid, ingest_style_id, modified_dt, bfly_local_src, bfly_zoom_src, bfly_zoom_site, bfly_list_site, bfly_pdp_site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                file_name      = VALUES(file_name),
                bfly_local_src = VALUES(bfly_local_src),
                version        = VALUES(version), 
                vendor_name    = VALUES(vendor_name), 
                bfly_product_path  = VALUES(bfly_product_path), 
                image_url      = VALUES(image_url), 
                alt            = VALUES(alt), 
                image_download_valid  = VALUES(image_download_valid),
                ingest_style_id  = VALUES(ingest_style_id), 
                modified_dt = VALUES(modified_dt);""", k, v['colorstyle'], v['vendor_style'], v['po_number'], v['version'], v['vendor_name'], v['bfly_product_path'], v['image_url'], v['alt'], v['image_download_valid'], v['ingest_style_id'], v['modified_dt'], v['bfly_local_src'], v['bfly_zoom_src'], v['bfly_zoom_site'], v['bfly_list_site'], v['bfly_pdp_site'])

                print "Inserted {0}".format(k)

            except sqlalchemy.exc.IntegrityError:
                print "Duplicate Entry {0}".format(k)
            
            #except sqlalchemy.exc.OperationalError:
            #    print "Invalid Path or Entry {0}".format(k)

            
            #print "Successful Insaert Push_Photoselecs --> {0}".format(k)


        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
        # except sqlalchemy.exc.DatabaseError:
        #     continue
        #     print "DBERR" + k

    #     except KeyError:
    #         continue


if __name__ == '__main__':
    main()
