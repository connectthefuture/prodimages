#!/usr/bin/env python


"""
Created on sun jun 12 14:48:56 2015

@author: jb
"""

def oracle_query_dict(q):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    result = connection.execute(q)
    styles = {}
    for row in result:
        style = {}
        style['colorstyle'] = row['colorstyle']
        style['vendor']  = row['vendor']
        style['brand']  = row['brand']
        style['po_number']  = row['po_number']
        style['vendor_style']  = row['vendor_style']
        style['vendor_color']  = row['vendor_color']
        style['color']  = row['color']
        style['image_ready_dt']  = row['image_ready_dt']
        style['copy_ready_dt']  = row['copy_ready_dt']
        style['production_complete_dt']  = row['production_complete_dt']
        style['prodclr_create_dt']  = row['prodclr_create_dt']
        style['gender']  = row['gender']
        style['product_type']  = row['product_type']
        style['product_subtype']  = row['product_subtype']
        style['category']  = row['category']
        style['image_number']  = row['image_number']
        style['url']  = row['url']
        style['image_create_dt'] = row['image_create_dt']
        style['vendor_create_dt'] = row['vendor_create_dt']
        style['vendor_mod_dt'] = row['vendor_mod_dt']
        styles[str(row['colorstyle'])] = style
    connection.close()
    return styles


def import_to_mysql(res):
    import sqlalchemy
    for k,v in res.iteritems():
        try:
            mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
            connection_www = mysql_engine_www.connect()
            try:
                connection_www.execute("""
                        INSERT INTO product_snapshot_vendor
                            (colorstyle, vendor, brand, po_number, prodclr_create_dt, vendor_create_dt, vendor_mod_dt, image_create_dt, copy_ready_dt, image_ready_dt, production_complete_dt, gender, category, product_type, product_subtype, vendor_style, color, vendor_color,  image_number, url)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            category                = VALUES(category),
                            production_complete_dt  = VALUES(production_complete_dt),
                            copy_ready_dt           = VALUES(copy_ready_dt),
                            image_ready_dt          = VALUES(image_ready_dt),
                            color                   = VALUES(color),
                            vendor_mod_dt           = VALUES(vendor_mod_dt),
                            image_create_dt         = VALUES(image_create_dt),
                            image_number            = VALUES(image_number),
                            url                     = VALUES(url),
                            vendor_create_dt        = VALUES(vendor_create_dt),
                            prodclr_create_dt       = VALUES(prodclr_create_dt);
                                   """, v['colorstyle'], v['vendor'], v['brand'], v['po_number'], v['prodclr_create_dt'], v['vendor_create_dt'],  v['vendor_mod_dt'], v['image_create_dt'], v['copy_ready_dt'], v['image_ready_dt'], v['production_complete_dt'], v['gender'], v['category'], v['product_type'], v['product_subtype'], v['vendor_style'], v['color'], v['vendor_color'],v['image_number'],  v['url'])
            #print "Updated Entry {0}".format(k)
            except sqlalchemy.exc.IntegrityError:
                print "Duplicate Entry {0}".format(k)

            except sqlalchemy.exc.IntegrityError:
                print "Duplicate Entry {0}".format(k)
        except sqlalchemy.exc.DatabaseError:
            print "DBERR" + k
            continue


#     except KeyError:
#         continue

query_vendor_snapshot= """
        SELECT DISTINCT
        Pomgr.Product_Color.ID                AS colorstyle,
        POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID AS vendor,
        POMGR.BRAND.NAME                      AS brand,
        POMGR.PO_HDR.ID AS po_number,
        Pomgr.Product_Color.VENDOR_STYLE AS vendor_style,
        Pomgr.Product_Color.VENDOR_COLOR AS vendor_color,
        POMGR.COLOR_GROUP.DESCRIPTION      AS color,
        Pomgr.Product_Color.IMAGE_READY_DT AS image_ready_dt,
        Pomgr.Product_Color.COPY_READY_DT AS copy_ready_dt,
        Pomgr.Product_Color.PRODUCTION_COMPLETE_DT AS production_complete_dt,
        Pomgr.Product_Color.CREATED_DATE           AS prodclr_create_dt,
        POMGR.LK_DEPT.NAME                         AS gender,
        (
          CASE
            WHEN PROD_FAMILY_DENORM_LK1.PROD_FAMILY_DESC IS NULL
            THEN POMGR.PRODUCT_FOLDER.NAME
            ELSE PROD_FAMILY_DENORM_LK1.PROD_FAMILY_DESC
          END) product_type,
        POMGR.PRODUCT_FOLDER.NAME AS product_subtype,
        (
          CASE
            WHEN POMGR.PROD_FAMILY_DENORM_LK.PROD_FAMILY_TREE IS NULL
            THEN POMGR.PRODUCT_FOLDER.NAME
            ELSE POMGR.PROD_FAMILY_DENORM_LK.PROD_FAMILY_TREE
          END) category,
        POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER  AS image_number,
        POMGR.SUPPLIER_INGEST_IMAGE.URL           AS url,
        trunc(POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE) AS image_create_dt,
        trunc(POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE)  AS vendor_create_dt,
        trunc(POMGR.SUPPLIER_INGEST_STYLE.MODIFIED_DATE) AS vendor_mod_dt
      FROM
        Pomgr.Product_Color
      LEFT OUTER JOIN POMGR.SUPPLIER_INGEST_STYLE
      ON
        POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR = Pomgr.Product_Color.ID
      LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE
      ON
        POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID
      INNER JOIN POMGR.COLOR_GROUP
      ON
        Pomgr.Product_Color.COLOR_GROUP_ID = POMGR.COLOR_GROUP.ID
      LEFT JOIN POMGR.PRODUCT
      ON
        Pomgr.Product_Color.PRODUCT_ID = POMGR.PRODUCT.ID
      INNER JOIN POMGR.BRAND
      ON
        POMGR.BRAND.ID = POMGR.PRODUCT.BRAND_ID
      LEFT JOIN POMGR.PRODUCT_FOLDER
      ON
        POMGR.PRODUCT.PRODUCT_FOLDER_ID = POMGR.PRODUCT_FOLDER.ID
      LEFT JOIN POMGR.PROD_FAMILY_DENORM_LK
      ON
        POMGR.PRODUCT_FOLDER.ID = POMGR.PROD_FAMILY_DENORM_LK.PROD_FAMILY_ID
      LEFT OUTER JOIN POMGR.PROD_FAMILY_DENORM_LK PROD_FAMILY_DENORM_LK1
      ON
       POMGR.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID = PROD_FAMILY_DENORM_LK1.PROD_FAMILY_ID
      INNER JOIN POMGR.LK_DEPT
      ON
        POMGR.LK_DEPT.ID = POMGR.PRODUCT_FOLDER.DEPT_ID
      LEFT outer JOIN POMGR.PO_LINE
      ON
        POMGR.PO_LINE.PRODUCT_COLOR_ID = Pomgr.Product_Color.PRODUCT_ID
      left outer join POMGR.PO_HDR
      ON
        POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID
      WHERE
        (
          Pomgr.Product_Color.CREATED_DATE >= SysDate - 240
        )
      OR
        (
          POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER   <= 1
        AND trunc(POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE) >= SysDate - 15
        )
      ORDER BY
        prodclr_create_dt DESC,
        1 DESC Nulls Last"""

def run_threaded_mysql_insert(import_dict=None):
    import Queue
    import threading
    import multiprocessing

    q = Queue.Queue()
    for i in import_dict.iteritems(): #put 30 tasks in the queue
        #print 'i ', ' import_dict'
        if i:
            q.put([i])

    def worker():
        count = 0
        while True:
            item = q.get()
            #
            import_to_mysql(item)
            count += 1
            print count, '\n\t Insert Threade'#, imgdata
            q.task_done()

    jobcount = multiprocessing.cpu_count() - 6  # --> detects number of cores on host manchine
    print("Creating %d threads" % jobcount)
    for i in xrange(jobcount):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    q.join() #block until all tasks are done


def main():
    print 'Getting Data from Oracle'
    res = oracle_query_dict(query_vendor_snapshot)
    print 'Importing to MySql'
    #run_threaded_mysql_insert(import_dict=(list(res.items()),))
    import_to_mysql(res)
    print 'Import Complete'
    for k,v in res.iteritems():
        print "{0}: {1}".format(k,v)

if __name__ == '__main__':
    main()
