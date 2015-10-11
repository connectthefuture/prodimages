#!/usr/bin/env python


"""
Created on mo jun 9 20:48:56 2014

@author: jb
"""
def sqlQueryToolData():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    querymake_tooldata="""WITH data AS
      (SELECT POMGR.PO_LINE.PRODUCT_COLOR_ID AS colorstyle,
        POMGR.PRODUCT_COLOR.VENDOR_STYLE     AS vendor_style,
        POMGR.PO_LINE.PO_HDR_ID AS po_number,
        POMGR.PRODUCT_DETAIL.MATERIAL AS material,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_1 AS bullet_1,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_2 AS bullet_2,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_3 AS bullet_3,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_4 AS bullet_4,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_5 AS bullet_5,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_6 AS bullet_6,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_7 AS bullet_7,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_8 AS bullet_8,
        POMGR.PRODUCT_COLOR_DETAIL.BULLET_9 AS bullet_9,
        POMGR.PRODUCT_COLOR_DETAIL.SHORT_NAME as short_name,
        POMGR.PRODUCT_COLOR_DETAIL.LONG_DESCRIPTION as long_description,
        POMGR.PRODUCT.COUNTRY_ORIGIN as country_origin,
        POMGR.PRODUCT_COLOR_DETAIL.BFLY_RETURN_POLICY_ID AS return_policy_id,
        POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt,
        POMGR.PRODUCT_DETAIL.CARE_INSTRUCTIONS_ID as care_instructions_id,
        POMGR.PRODUCT_COLOR.COLOR_GROUP_ID as color_group_id
      FROM POMGR.PRODUCT_COLOR
      RIGHT JOIN POMGR.PO_LINE
      ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
      RIGHT JOIN POMGR.PO_HDR
      ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID
      INNER JOIN POMGR.LK_PO_TYPE
      ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID
      LEFT JOIN POMGR.PRODUCT_DETAIL
      ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID
      LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL
      ON POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
      LEFT JOIN POMGR.PRODUCT
      ON POMGR.PRODUCT.ID = POMGR.PRODUCT_COLOR.PRODUCT_ID
      WHERE POMGR.PRODUCT.MODIFIED_DATE > trunc(sysdate - 4)
      ORDER BY POMGR.PRODUCT_COLOR.VENDOR_STYLE,
        POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last
      )
    SELECT *
    FROM data
    WHERE data.vendor_style is not null"""

    result = connection.execute(querymake_tooldata)
    importdata = {}
    for row in result:
        importdata_tmp = {}
        importdata_tmp['colorstyle'] = row['colorstyle']
        importdata_tmp['vendor_style'] = row['vendor_style']
        importdata_tmp['po_number'] = row['po_number']
        importdata_tmp['material'] = row['material']
        importdata_tmp['bullet_1'] = row['bullet_1']
        importdata_tmp['bullet_2'] = row['bullet_2']
        importdata_tmp['bullet_3'] = row['bullet_3']
        importdata_tmp['bullet_4'] = row['bullet_4']
        importdata_tmp['bullet_5'] = row['bullet_5']
        importdata_tmp['bullet_6'] = row['bullet_6']
        importdata_tmp['bullet_7'] = row['bullet_7']
        importdata_tmp['bullet_8'] = row['bullet_8']
        importdata_tmp['bullet_9'] = row['bullet_9']
        importdata_tmp['short_name'] = row['short_name']
        importdata_tmp['long_description'] = row['long_description']
        importdata_tmp['country_origin'] = row['country_origin']
        importdata_tmp['return_policy_id'] = row['return_policy_id']
        importdata_tmp['copy_ready_dt'] = row['copy_ready_dt']
        importdata_tmp['care_instructions_id'] = row['care_instructions_id']
        importdata_tmp['color_group_id'] = row['color_group_id']
        print row['colorstyle']

        ## colorstyle as dict KEY
        importdata[row['colorstyle']] = importdata_tmp

    connection.close()
    return importdata

#### Run Import To Mysql
import sys
import os
import sqlalchemy


importdata = sqlQueryToolData()

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
        #             INSERT INTO excel_tool_data 
        #                 (colorstyle, vendor_style, po_number, material, bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8, bullet_9, short_name, long_description, country_origin, return_policy_id, copy_ready_dt, care_instructions_id, color_group_id)
        #                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        #             ON DUPLICATE KEY UPDATE 
        #                 material  = VALUES(material), 
        #                 bullet_1  = VALUES(bullet_1), 
        #                 bullet_2  = VALUES(bullet_2), 
        #                 bullet_3  = VALUES(bullet_3), 
        #                 bullet_4  = VALUES(bullet_4), 
        #                 bullet_5  = VALUES(bullet_5), 
        #                 bullet_6  = VALUES(bullet_6), 
        #                 bullet_7  = VALUES(bullet_7), 
        #                 bullet_8  = VALUES(bullet_8), 
        #                 bullet_9  = VALUES(bullet_9), 
        #                 short_name           = VALUES(short_name), 
        #                 long_description     = VALUES(long_description), 
        #                 country_origin       = VALUES(country_origin), 
        #                 return_policy_id     = VALUES(return_policy_id), 
        #                 copy_ready_dt        = VALUES(copy_ready_dt), 
        #                 care_instructions_id = VALUES(care_instructions_id), 
        #                 color_group_id        = VALUES(color_group_id);
        #                        """, v['material'], v['bullet_1'], v['bullet_2'], v['bullet_3'], v['bullet_4'], v['bullet_5'], v['bullet_6'], v['bullet_7'], v['bullet_8'], v['bullet_9'], v['short_name'], v['long_description'], v['country_origin'], v['return_policy_id'], v['copy_ready_dt'], v['care_instructions_id'], v['color_group_id'])
        # except sqlalchemy.exc.IntegrityError:
        #     print "Duplicate Entry {0}".format(k)
        
        
        

        try:
            connection_www.execute("""INSERT INTO excel_tool_data (colorstyle, vendor_style, po_number, material, bullet_1, bullet_2, bullet_3, bullet_4, bullet_5, bullet_6, bullet_7, bullet_8, bullet_9, short_name, long_description, country_origin, return_policy_id, copy_ready_dt, care_instructions_id, color_group_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            ON DUPLICATE KEY UPDATE 
            material  = VALUES(material), 
            bullet_1  = VALUES(bullet_1), 
            bullet_2  = VALUES(bullet_2), 
            bullet_3  = VALUES(bullet_3), 
            bullet_4  = VALUES(bullet_4), 
            bullet_5  = VALUES(bullet_5), 
            bullet_6  = VALUES(bullet_6),
            bullet_7  = VALUES(bullet_7), 
            bullet_8  = VALUES(bullet_8), 
            bullet_9  = VALUES(bullet_9), 
            short_name = VALUES(short_name), 
            long_description = VALUES(long_description), 
            country_origin = VALUES(country_origin), 
            return_policy_id= VALUES(return_policy_id), 
            copy_ready_dt = VALUES(copy_ready_dt), 
            care_instructions_id = VALUES(care_instructions_id), 
            color_group_id = VALUES(color_group_id);""", v['colorstyle'], v['vendor_style'], v['po_number'], v['material'], v['bullet_1'], v['bullet_2'], v['bullet_3'], v['bullet_4'], v['bullet_5'], v['bullet_6'], v['bullet_7'], v['bullet_8'], v['bullet_9'], v['short_name'], v['long_description'], v['country_origin'], v['return_policy_id'], v['copy_ready_dt'], v['care_instructions_id'], v['color_group_id'])

            print "Inserted {0}".format(k)

        except sqlalchemy.exc.IntegrityError:
            print "Duplicate Entry {0}".format(k)
        
        
        
        #print "Successful Insaert Push_Photoselecs --> {0}".format(k)


    except sqlalchemy.exc.IntegrityError:
        print "Duplicate Entry {0}".format(k)
    # except sqlalchemy.exc.DatabaseError:
    #     continue
    #     print "DBERR" + k

#     except KeyError:
#         continue
