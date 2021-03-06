#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Bypass Certificate authentication
import urllib3
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

urllib3.disable_warnings()

#global single_flag
#
# update_query="""SELECT DISTINCT
#                   POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR AS colorstyle,
#                   POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER          AS alt,
#                   POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID             AS vendor_name,
#                   POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND          AS vendor_brand,
#                   POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE          AS vendor_style,
#                   POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID              AS genstyleid,
#                   POMGR.PRODUCT_COLOR.COPY_READY_DT          AS copy_ready_dt,
#                   POMGR.PRODUCT_COLOR.IMAGE_READY_DT         AS image_ready_dt,
#                   POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE   AS img_ingest_dt,
#                   POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE   AS style_ingest_dt,
#                   POMGR.SUPPLIER_INGEST_STYLE.MODIFIED_DATE  AS style_mod_dt,
#                   POMGR.PRODUCT_COLOR.ACTIVE                        AS active,
#                   POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY      AS product_folder,
#                   POMGR.SUPPLIER_INGEST_IMAGE.URL                   AS image_url
#                 FROM POMGR.SUPPLIER_INGEST_STYLE
#                 LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID
#                 INNER JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR
#                 WHERE pomgr.supplier_ingest_image.created_date >= sysdate - {0}
#                   AND POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{1}%'
#                   AND POMGR.SUPPLIER_INGEST_IMAGE.URL IS NOT NULL
#                   AND POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER  <= 6
#                   AND pomgr.supplier_ingest_image.created_date > image_ready_dt + 3
#                   AND POMGR.SUPPLIER_INGEST_STYLE.modified_date >= POMGR.SUPPLIER_INGEST_STYLE.created_date
#                 ORDER BY vendor_name Nulls Last, img_ingest_dt DESC Nulls Last,  1,  colorstyle Nulls Last
#                 """.format(kwargs.get(vendor, "_"), kwargs.get(str(date_range_int), "4"))

def sqlQuery_GetIMarketplaceImgs(vendor=None, vendor_brand=None, po_number=None, ALL=None, **kwargs):
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    try:
        import sys
        date_range = str(sys.argv[3])
        if date_range.isdigit() == True:
            kwargs.update(date_range_int=date_range)
    except IndexError:
        pass
    #print vendor_brand, "Vendorbrand"
    connection = orcl_engine.connect()
    if po_number:
        if ALL == 'Image':
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.PO_LINE.PO_HDR_ID LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(po_number)
        # prod complete null vs image null as above only on po search
        elif not ALL:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.PO_LINE.PO_HDR_ID LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(po_number)
    ##
    elif vendor and not vendor_brand:
        # null prdcmp
        if vendor.isdigit() == True and len(vendor) == 9:
            colorstyle = str(vendor)
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR like '%{0}%' and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 ORDER BY POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last".format(colorstyle)
            #print query_marketplace_inprog
        elif not ALL:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {1} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' AND POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID NOT LIKE '%TESTFLAG%') and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 ORDER BY POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last".format(vendor, kwargs.get('date_range_int', '155')).replace('TESTFLAG', 'TESTFLAG')
        elif ALL.isdigit():
            kwargs.update(date_range_int=ALL)
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {1} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 ORDER BY POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last".format(vendor, kwargs.get('date_range_int', '45'))
        elif ALL.lower() == 'url':
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_IMAGE.created_date as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {1} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL  like '%{0}%' ) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID not LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_IMAGE.created_date DESC nulls last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, kwargs.get('date_range_int', '221'))
        elif ALL.lower() == 'notall':
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_IMAGE.created_date as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {1} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID not LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_IMAGE.created_date DESC nulls last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, kwargs.get('date_range_int', '21'))
        #not null prd cmp
        else:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_IMAGE.created_date as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {1} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NOT NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_IMAGE.created_date DESC nulls last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, kwargs.get('date_range_int', '45'))

    elif vendor_brand:
        # below is both complete and incomplete
        #
        if not ALL:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {2} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and POMGR.SUPPLIER_INGEST_IMAGE.URL IS NOT NULL and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' and POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND LIKE '%{1}%') AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, vendor_brand, kwargs.get('date_range_int', '45'))

        # below is prod not null
        else:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {2} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS not NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' and POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND LIKE '%{1}%') AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, vendor_brand, kwargs.get('date_range_int', '45'))


    ## WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    ## AND POMGR.PRODUCT_COLOR.COPY_READY_DT IS NOT NULL
    ##
    print query_marketplace_inprog
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
        style_alt = "{0}_{1}".format(row['colorstyle'], row['alt'])
        #consigstyle['vendor_style'] = row['vendor_style']
        styles[style_alt] = styledata

    print '\n\n\n\n\n\n\n\t\tIn Under 10 Seconds\nWe will be Attempting\nt\tThe Download and Processing\vof\n\t\v{0} Image Urls\n\n\n\n\n\n'.format(len(styles))
    from time import sleep
    sleep(10)
    connection.close()
    return styles


def parse_mplace_dict2tuple(styles_dict,dest_root=None):
    import os.path, sys
    count = ''
    try:
        if str(sys.argv[1]).isdigit() and len(str(sys.argv[1])) == 9:
            count = 1
        else:
            count = len(set(list([k for k in styles_dict.keys()])))
    except IndexError:
        count = 2 #len(set(list([k for k in styles_dict.keys()])))

    print ' Count ', count, styles_dict.keys()

    mproc_tuple_Qlist = []
    for k,v in styles_dict.iteritems():
        try:
            colorstyle  = v['colorstyle']
            image_url   = v['image_url']
            po_number   = v['po_number']
            vendor_name = v['vendor_name']
            alt_number  = v['alt']
            ext = '.' + image_url.split('.')[-1]
            if len(image_url.split('.')[-1]) == 3:
                ext = '.' + str(image_url.split('.')[-1][:3])
                ext = ext.lower().strip('?dl=0')
                ext = ext.lower().strip('?dl=1')
            else:
                ext = '.jpg'
            if alt_number:
                bfly_ext = "_{0}{1}".format(alt_number,ext)
                ext = bfly_ext
            if count > 1:
                destdir  = os.path.join(dest_root, str(vendor_name), str(po_number))
            elif count == 1:
                destdir  = os.path.join(dest_root, str(vendor_name), str(po_number), str(colorstyle))
            else:
                raise ValueError

            destpath = os.path.join(destdir, colorstyle + ext)
            tupleargs = (image_url, destpath, )
            mproc_tuple_Qlist.append(tupleargs)
            if os.path.isdir(destdir):
                pass
            else:
                try:
                    os.makedirs(destdir)
                except:
                    pass
        except ValueError:
            print 'Raised ValueError ', count, k,' ',v
            pass
    return mproc_tuple_Qlist


def drive_match_fileid(image_url):
    import re
    regex_drive3 = re.compile(r'^(https://d(.+?)\.google\.com/file/d/)(?P<fileid>.+?)/(edit|view)\?usp\=.*?$', re.U)
    drivefile = regex_drive3.match(image_url)
    if drivefile:
        fileid = drivefile.groupdict()['fileid']
        return fileid


def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata




# def exchange_tokens(refresh_token=None):
#     from boxsdk import OAuth2
#     TOKENS_FILE = 'tokens_priv.pkl'
#     CLIENT_ID = 'bxccmj5xnkngs8mggxv5ev49zuh80xs9'  # Insert Box client ID here
#     CLIENT_SECRET = 'g4R1o909fgf1PSsa5mLMDslpAwcbfIQl'  # Insert Box client secret here
#     from os import chdir, path, curdir
#     ## Check for stored tokens
#     import cPickle as pickle
#     initdir = path.abspath(curdir)
#     #chdir(path.dirname(path.realpath(__file__)))
#     #TOKENS_FILE = 'tokens.pkl'
#     if path.isfile(TOKENS_FILE):
#         import requests, json
#         #with open(TOKENS_FILE,'rb') as fr:
#         #    oldaccess_token, valid_refresh_token = pickle.load(fr)
#         with open(TOKENS_FILE,'rb') as fr:
#             try:
#                 oldaccess_token, valid_refresh_token = pickle.load(fr)
#             except:
#                 valid_refresh_token = None
#                 pass
#             if valid_refresh_token is not None:
#                 pass
#             else:
#                 print 'Valid Refresh is None'
#                 return
#             #else:
#             #    oldaccess_token, valid_refresh_token = 'uyT2xUxxZxROzlRjW8T6ge9q7Ne0drdC', 'IVilutwMwaxD9xWWLIpNVffJSQx4GX36Ido8Y2guCFzU6pKrhyovRtooJU8milXn'
#         box_api_token_root = "https://app.box.com/api/oauth2/token"
#         data = {
#              ##'Authorization': "Bearer " + access_token,
#              ##'BoxApi': "shared_link=" + shared_link,
#              'grant_type': 'refresh_token',
#              'refresh_token': valid_refresh_token,
#              'client_id': CLIENT_ID,
#              'client_secret': CLIENT_SECRET
#              }
#         headers = {
#                 'Content-Type': 'application/json; charset=UTF-8'
#         }
#         res = requests.post(box_api_token_root, data=data, headers=headers)
#         newcreds = json.loads(res.content)
#         print(newcreds)
#         try:
#             access_token = newcreds['access_token']
#             refresh_token = newcreds['refresh_token']
#             ## Replace old cred dumping new creds to tokens.pkl
#             ##---NOTE---## refresh token is valid for 60 days,
#             ##  ------  ## afterwhich the pickle file token_priv should be manually edited/synced
#             with open(TOKENS_FILE,'wb') as fw:
#                 pickle.dump((access_token, refresh_token,),  fw)
#                 print('BoxSuccess')
#                 return access_token, refresh_token
#         except KeyError:
#             return
#     ###################
#     else:
#         import __builtin__
#         access_token, refresh_token = authenticate()
#         pickle.dump((access_token, refresh_token,),  __builtin__.open(TOKENS_FILE,'wb'))
#         #chdir(initdir)
#         return access_token, refresh_token

##########################
##########################
##########################
def md5_checksumer(src_filepath):
    import hashlib
    import os.path as path
    if src_filepath is not None and path.isfile(src_filepath):
        filepath = path.abspath(src_filepath)
        try:
            _file = open(filepath, "rb")
            content = _file.read()
            _file.close()
            md5 = hashlib.md5(content)
            _hash = md5.hexdigest()
            return _hash
        except IndexError:
            print "Not Index Error Checksummer"
            return False

##########################
######### REDIS ##########
##########################
def check_updated_image_by_md5checksum(filename, md5checksum=None, image_url=None, colorstyle=None, alt=None, local_filepath=None, version=None):
    import redis
    #redis_host = 'pub-redis-17996.us-east-1-4.3.ec2.garantiadata.com'
    #redis_port = 17996
    redis_host = '127.0.0.1'
    redis_port = 6379

    r = redis.Redis(host=redis_host, port=redis_port, encoding='utf-8', encoding_errors='strict', db=0)  ##,db=0, password=None, socket_timeout=None, connection_pool=None, unix_socket_path=None)

    if not filename:
        filename=local_filepath.split('/')[-1]
    if filename is not None and filename[:9].isdigit():
        colorstyle = filename[:9]
        ext = filename.split('.')[-1]
        alt = filename.split('_')[1].split('.')[0][-1]
        md5checksum = md5_checksumer(filename)
        if alt.isdigit():
            pass
        else:
            alt = 'NA'
    else:
        colorstyle='NA'
        alt='NA'
        ext = 'NA'

    if r.sadd("marketplace:currentsite", filename):
    #if r.mset("google_drive:ll_editorial", filename):
        ## Faking Hashes with Sets
        ## r.set("filename:%s:colorstyle" % filename, colorstyle)
        ## r.set("filename:%s:local_filepath" % filename, local_filepath)
        r.hset("filename:%s" % filename, "md5checksum", md5checksum)
        r.hset("filename:%s" % filename, "image_url", image_url)
        r.hset("filename:%s" % filename, "colorstyle", colorstyle)
        r.hset("filename:%s" % filename, "alt", alt)
        r.hset("filename:%s" % filename, "ext", ext)
        r.hset("filename:%s" % filename, "local_filepath", local_filepath)
        r.hmset("filename:%s" % filename, {"media_version": version})
        r.hsetnx("filename:%s" % filename, "ref_count", 0)
        r.hincrby("filename:%s" % filename, "ref_count", 1)
        print '\tREDIS SUCCESS --> ', r.hvals("filename:%s" % filename)
        return True
    else:
        print '\tREDIS FAILED --> ', filename
        return False

###############
###############
###############

def get_box_access_token():
    import os
    # reg
    #initdir = os.path.abspath(__file__)
    #os.chdir(os.path.join(os.path.abspath(__file__), '../../http_tools/auth/Box'))
    from http_tools.auth.Box.boxapi_full_auth_dload import exchange_tokens
    access_token, refresh_token = exchange_tokens()
    #--# Return the valid access and fresh return token
    ##---NOTE---## refresh token is valid for 60 days, afterwhich the pickle file should be manually synced
    #os.chdir(initdir)
    return access_token


def get_real_box_download_url(shared_link, access_token=None):
    import requests
    # try:
    #     access_token = get_box_access_token()
    # except:
    #     pass

    if not access_token:
        # GET TEMP DEVELOPER TOKEN TO PUSH THROUGH IF EXCHANGING FOR REFRESH KEY FAILS
        access_token = '420ovyrdxCShLxroHTPjNYZCtktUOU3p' # get_box_access_token()
    box_api_shared_root = "https://api.box.com/2.0/shared_items"
    headers = {
         'Authorization': "Bearer " + access_token,
         'BoxApi': "shared_link=" + shared_link,
     }
    res = requests.get(box_api_shared_root, headers=headers)
    try:
        file_id = res.json()['id']
        file_name = res.json()['name']
        download_url = res.json()['shared_link']['download_url']
        print 'downloadUrl', '<--->', download_url
        return download_url
    except ValueError:
        print shared_link, ' Value3 Error '
        return shared_link


def download_mplce_url(urldest_tuple):
    import requests, re, urllib, urllib2, urllib3, OpenSSL, subprocess
    from os import path

    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
    urllib3.disable_warnings()

    countimage = 0
    countstyle = 0
    image_url, destpath = urldest_tuple
    destdir = path.dirname(destpath)
    colorstyle = destpath.split('/')[-1][:9]
    alt_number = destpath.split('_')[-1][0]
    try:
        image_url = 'https://www.drop'.join(image_url.split('https://wwwop'))
        image_url = urllib.unquote_plus(image_url)
    except:
        pass
    ########################################################

    ########################################################
    ## Image URL Cleanup and Replace Extraneous/Bad Chars ##
    ########################################################
    ####### Dropbox Fix for View vs DL value ###############
    regex_dbx = re.compile(r'^https://www.dropbox.com/.+?\.[jpngJPNG]{3}$')
    regex_dbxprev = re.compile(r'^https://www.dropbox.com/.+?preview.*\.[jpngJPNG]{3}$')
    image_url = image_url.replace('dl=9','dl=1').replace('dl=0', 'dl=1').replace('dl=2', 'dl=1').replace('dl=3', 'dl=1').replace('dl=4', 'dl=1').replace('dl=5', 'dl=1').replace('dl=6', 'dl=1').replace('dl=7', 'dl=1').replace('dl=8', 'dl=1')
    regex_dl = re.compile(r'^.+\?dl=1.*?$')
    if regex_dbx.findall(image_url):
        if regex_dbxprev.findall(image_url):
            print 'REGEX DBXPRE'
            import http_tools.auth.Dropbox.dropboxapi_service as dropboxapi_service
            final_path = image_url #dropboxapi_service.download_auth_file(image_url=image_url, destpath=destpath)

            if final_path:
                print final_path, 'Final DBX Path'
                image_url = final_path
            else:
                pass
        else:
            image_url.replace('.JPG', '.jpg')
            image_url.replace('.PNG', '.png')
            print 'REGEX DBX dl=1'
        if not regex_dl.findall(image_url):
            image_url = image_url + '&dl=1'

    ########################################################
    ###########---- BEGIN UGLY Tmp Fix ---##################
    ########################################################
    ####### URL ENCODED % ESCAPES Fix ######################
    ## Strip error causing Line Feed ascii char
    #  -- Should be commented usually, only for temp fixing single uploads
    # image_url = ''.join(image_url.split('%0A'))
    ########################################################
    ############       Finally     #########################
    #####     Replace ALL url encoding % escapes    ########
    ###  TWICE TO ACCOUNT FOR EX. %2520 --> %20 --> ' '  ###
    # image_url  = image_url.replace('/Flat%2520Images/', '/Flat%20Images/')
    # print image_url, ' URL'
    ##############-------------------------#################
    ##############---- END UGLY Tmp Fix ---#################
    ########################################################

    regex_validurl = re.compile(r'^http[s]?://.+?$', re.U)
    regex_ftpurl = re.compile(r'^ftp[s]?://.+?$', re.U)
    regex_drive2 = re.compile(r'^(https://d(.+?)\.google\.com/).*\?id\=(?P<fileId>.+?)\&?.*?$', re.U)
    regex_drive3 = re.compile(r'^(https://d(.+?)\.google\.com/file/d/)(?P<fileId>.+?)/(edit|view)\?usp\=.*?$', re.U)

    # regex_dropbox = re.compile(r'^https?://www.dropbox.com/.+?\.[jpngJPNG]{3}$')
    ######################
    #### BOX API AUTH ####
    regex_boxapi  = re.compile(r'^(https?)?(?:\://)?(?P<VENDER_ROOT>.*)?(.*?)\.box\.com/(s/)?(?P<SHARED_LINK_ID>.+)?/?(\.?[jpngJPNG]{3,4})?(.*?)?\??(.*?)?$', re.U)
    if regex_boxapi.findall(image_url):
        'REGEX BOXEd'
        m = regex_boxapi.match(image_url)
        m.groupdict()
        try:
            image_url_temp = image_url.rstrip('.jpg')
            image_url = get_real_box_download_url(image_url_temp)
            print 'boxingapi -->', image_url_temp, image_url, m.groupdict()
        except OSError:
            print "OSError LINE 356;"
            pass
    else:
        pass
    # finally:
    #     pass
    #         #import jbmodules.http_tools.auth.Box.boxapi_auth_downloader as boxapi_auth_downloader
        #final_path = boxapi_auth_downloader.download_boxapi_drive_file(image_url=image_url, destpath=destpath)
        #if final_path:
            #return final_path
        #else:
        #    pass
    # if regex_dropbox.findall(image_url):
    #     import http_tools.auth.Dropbox.dropboxapi_service as dropboxapi_service
    #     final_path = dropboxapi_service.download_auth_file(image_url=image_url, destpath=destpath)
    #     if final_path:
    #         return final_path
    # elif regex_boxapi.findall(image_url):
    #     import http_tools.auth.Box.boxapi_auth_downloader as boxapi_auth_downloader
    #     final_path = boxapi_auth_downloader.download_boxapi_drive_file(image_url=image_url, destpath=destpath)
    #     if final_path:
    #         return final_path
    # elif regex_drive2.findall(image_url):

    ########################
    #### DRIVE API AUTH ####
    #if regex_drive2.findall(image_url):

    import urllib3

    print ' 404 - 1 - Trying Urllib3 ', image_url
    hostname = urllib3.get_host(image_url)[1]
    ####################################################################################################
    ####################################################################################################
    ####
    #################
    ########### TEMPORARY RESTRICT URL from Merchantry Placeholder ###########
    old_blue_sweater_placeholder_url = 'https://pim-image-4b2a111d-0df4-447e-bc31-d288a9-s3bucket-1in4kl2m21ire.s3.amazonaws.com/7274a8bcbb3fa06076da6e1c2950e617b24baf4f5d467def6c88f276a0e15f12.jpg'
    placeholder_url = 'https://pim-image-4b2a111d-0df4-447e-bc31-d288a9-s3bucket-1in4kl2m21ire.s3.amazonaws.com/5d167c72a8100a911f06940395589769857cbd395e452bf21416503d1c43861c.jpg'
    if image_url == placeholder_url or image_url == old_blue_sweater_placeholder_url:
        print 'RESTRICTING DOWNLOAD of Merchantry Placeholder image.--> {}'.format(image_url)
        return
    ######################### END ###### Adjust below elif to initial if once removed above #############
    #################
    ####
    ####################################################################################################
    ####################################################################################################
    elif regex_drive3.findall(image_url):
        image_url = drive_match_fileid(image_url)
        print image_url, ' DRIVE3 --ID--> '
        import http_tools.auth.Google.google_drive_auth_downloader as google_drive_auth_downloader
        try:
            final_path = google_drive_auth_downloader.download_google_drive_file(image_url=image_url, destpath=destpath)
            if final_path:
                return final_path
            else:
                print 'Final DRIVE Failure ', destpath, '\n', image_url
        except IndexError:
            print 'Final DRIVE Exception ', destpath, '\n', image_url

    elif regex_drive2.findall(image_url):
        print image_url, ' DRIVE'
        #import jbmodules
        #from jbmodules
        import http_tools.auth.Google.google_drive_auth_downloader as google_drive_auth_downloader
        try:
            final_path = google_drive_auth_downloader.download_google_drive_file(image_url=image_url, destpath=destpath)
            if final_path:
                return final_path
            else:
                print 'Final DRIVE Failure ', destpath, '\n', image_url
        except IndexError:
            print 'Final DRIVE Exception ', destpath, '\n', image_url
            #return

    elif regex_ftpurl.findall(image_url):
        print image_url, ' FTP--FTP\n...probably Jaipur...'
        from http_tools.ftp_functions import pycurl_ftp_download
        import pycurl
        #from jbmodules
        try:
            res = pycurl_ftp_download(imageurl=image_url,destpath=destpath)
            print 'FTEPPEE --> {}\n{}\t\n'.format(res, image_url, destpath)
            return destpath
        except pycurl.error, error:
            print 'Pycurl error in FTP Download --> ', error

    #############
    ## No Auth ##
    elif regex_validurl.findall(image_url):
        import httplib2
        # image_url = httplib2.urlnorm(httplib2.urllib.unquote(image_url))[-1]
        #print 'RRR final', image_url
        headers = {'Content-Accept': 'gzip', 'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0'}
        ########################################################
        ####### Google Drive Fix ###############################
        ########################################################
        regex_drive = re.compile(r'^(https://drive.google.com/.+?)/edit\?usp=sharing$')
        #regex_drive = re.compile(r'^(https://d(.+?)\.google\.com/.+?)/(edit|view)\?usp\=.*?$')
        if regex_drive.findall(image_url):
            image_url = image_url.split('/edit?')[0]
            image_url = image_url.split('/view?')[0]
        else: pass

        try:
            print image_url, destpath
            if not image_url[:5] == 'https':
                res = requests.get(image_url, timeout=17, verify=False, headers=headers)
                print ' HTTP Yippie ', res
            else:
                res = requests.get(image_url, timeout=12, verify=False, headers=headers)
                print ' HTTPS Oh Yes ', image_url,  res.headers
            print 'ALMOST'
            urlcode_value = res.status_code
            print urlcode_value
            if urlcode_value == 209:
                print urlcode_value
                #res = urllib.urlretrieve(image_url, destpath)
                res = requests.get(image_url, timeout=7, verify=False, headers=headers)
                with open(destpath, 'wb+') as f:
                    f.write(res.content)
                    f.close()
                    countimage += 1
                print "Image Download Count: {}".format(countimage)
                if alt_number == 1:
                    countstyle += 1
                print "Total New Styles Downloaded: {}".format(countstyle)
                return destpath
            elif urlcode_value < 400:
                print urlcode_value
                try:
                    print 'TRYsub400', image_url, destpath, '476'
                    if image_url[:5] == 'https':
                        #res = requests.get(image_url, stream=False, timeout=11, verify=False, headers=headers)
                        print 'Streaming False \n', res.headers, ' RES HTTPS HEAD <400  URL-->\t', image_url
                    else:
                        print ''
                        #res = requests.get(image_url, timeout=11, verify=False, headers=headers)
                    with open(destpath, 'wb+') as f:
                        f.write(res.content)
                        f.close()
                    print res.headers, ' RES HEAD <400  URL-->\t', image_url, '\v', destpath
                    return destpath
                except:
                    #subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                    print 'Failed Downloading HTTPS file {}'.format(image_url)

            elif urlcode_value == 404:
                ########## Temp Mrktplce MErchantry workaround to fix their urls they are feeding ###
                #import urllib3
                print ' 404 - 2 - Trying Urllib3 ', image_url
                #hostname = urllib3.get_host(image_url)[1]
                if hostname == 'marketplace.merchantry.com':
                    image_url = image_url.replace(hostname, 'pim2.merchantry.com')
                elif hostname == 'pim1.merchantry.com':
                    image_url = image_url.replace(hostname, 'pim2.merchantry.com')
                else:
                    print hostname, ' MERCHANTRY URLs Respond with 404 Errors '
                #######################################################################################

                #######################################################################################

                try:
                    print 'TRY404'
                    res = requests.get(image_url, timeout=10, verify=False, headers=headers)
                    with open(destpath, 'wb+') as f:
                        f.write(res.content)
                        f.close()
                    print res, ' 2nd Attempt using Merchantry Replaced URL OK'
                    return destpath
                except requests.exceptions.ConnectionError:
                    print '\t\tConnectionError FinalFailureNotice'
                    # import path
                    return urlcode_value
                    # badurldir = path.join(destdir,'error404')
                    # if path.isdir(badurldir):
                    #     pass
                    # else:
                    #     try:
                    #         os.makedirs(badurldir, 16877)
                    #     except:
                    #         pass
                    # try:
                    #     with open(path.join(path.abspath(badurldir), image_url + '_error404.txt'), 'ab+') as f:
                    #         f.write("{0}\t{1}\n".format(image_url + '_imgnum_' + '_errcode_' + urlcode_value))
                    #         return destpath
                    # except:
                    #     print '\v\v\tPrint Failed write 404 file'

        except requests.exceptions.ConnectionError:
            print 'ConnectionError\n ', locals()
            return 0
        except IOError:
            print 'Hidden IO Error Related to timeout value in get'


def multi_url_downloader(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import subprocess
    import requests
    q = Queue.Queue()
    for i in argslist: #put 30 tasks in the queue
        if i:
            q.put(i)

    def worker():

        count = 0
        while True:
            item = q.get()
            #execute a task: call a shell program and wait until it completes
            #subprocess.call("echo "+str(item), shell=True)
            downloaded_file = download_mplce_url(item)
            ## Delete Non Images before the whole shebang continues
            try:
                metadata = get_exif_all_data(downloaded_file)
                ## Catch placeholder from Merchantry and throw Key error after checking mdata for actual image
                if metadata.get('File:MIMEType') is not None and metadata.get('File:MIMEType').split('/')[0] != 'image':
                    from os import remove
                    print 'Removing File with metadata--> ', metadata
                    # with open('/mnt/Post_Complete/Complete_Archive/badfiles_200code_removed.txt','ab+') as f:
                    #     for k,v in metadata.items():
                    #         try:
                    #             import codecs
                    #             mimetype = codecs.decode(metadata.get('File:MIMEType'), 'utf-8')
                    #             keyutf8 = codecs.decode(k, 'utf-8')
                    #             valuesutf8 = codecs.decode(v, 'utf-8')
                    #             error_logged = "Wrong MIMEType: {}, '{}': '{}'\n\t{}".format(mimetype, keyutf8, valuesutf8, item)
                    #             print error_logged
                    #         except UnicodeEncodeError:
                    #             print 'UnicodeEncodeError Passing ---'
                    #             pass
                    remove(downloaded_file)
                    q.task_done()
                elif metadata.get('Composite:ImageSize') == '75x89':
                    print 'Halting and discarding Marchantry Placeholder.\n\tSize is--> ', metadata.get('Composite:ImageSize')
                    raise KeyError
                    #print metadata.get('File:MIMEType'), ' <--BadImage - Removed --> ', downloaded_file
                else:
                    count += 1
                    #### Check and Add to Redis
                    check_updated_image_by_md5checksum(downloaded_file)
                    print count, ' NotRemoved --> ', downloaded_file, metadata.get('File:MIMEType')
                    q.task_done()
            except requests.exceptions.ConnectionError:
                print 'ConnectionError Probably a timeout issue with download func--> ', downloaded_file
                q.task_done()
            except AttributeError:
                print 'AttributeError --> ', downloaded_file
                q.task_done()
            except KeyError:
                print 'KeyError --> ', downloaded_file
                try:
                    from os import remove
                    remove(downloaded_file)
                except:
                    pass
                q.task_done()
            finally:
                #try:
                print '\n\n\n\n\n\n\t\t\t\t\t\tDONE Downloading in Parallel\n\n\n\n\n\n' #q.task_done()
                #except:
                #    pass

    cpus=multiprocessing.cpu_count() * 2 #detect number of cores
    print("Creating %d threads" % cpus)
    for i in xrange(cpus):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()

    q.join() #block until all tasks are done


def mongo_update_url_dest_info(urldest_tuple):
    #print urldest_tuple, ' Url Dest Tuple mongo_update_url_dest_info'
    image_url, destpath  = urldest_tuple[0]
    image_url            = image_url
    tmpfilename          = str(destpath.split('/')[-1])
    colorstyle           = str(tmpfilename[:9])
    image_number         = str(tmpfilename.split('.')[-2][-1])
    content_type         = str(tmpfilename.split('.')[-1]).lower().replace('jpg', 'jpeg')
    hostname             = None # '127.0.0.1' # 'mongodb://relic7:mongo7@ds031591.mongolab.com:31591/gridfs_mrktplce' # None
    #hostname             = 'ds031591.mongolab.com:31591' ###'mongodb://mongo:mongo@prodimages.ny.bluefly.com:27017/gridfs_mrktplce' #
    db_name              = 'gridfs_mrktplce' # hostname.split('/')[-1]

    if image_url:
        #import jbmodules
        #from jbmodules import mongo_tools
        import sys, os
        jbmade = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        print jbmade
        sys.path.append(jbmade)
        sys.path.append('/usr/local/batchRunScripts/python/jbmodules')
        sys.path.append('/usr/local/batchRunScripts/python/jbmodules/mongo_tools')
        from mongo_tools import mongo_image_prep as mongo_image_prep

        updateCheck = mongo_image_prep.update_gridfs_extract_metadata(
            destpath,
            hostname = hostname,
            db_name = db_name,
            image_url = image_url,
            filename = tmpfilename,
            colorstyle  = colorstyle,
            image_number  = image_number,
            content_type  = 'image/{}'.format(content_type)
            )     ## image_url=image_url, destpath=destpath)
        return updateCheck, destpath



def mongo_upsert_threaded(argslist=None):
    import Queue
    import threading
    import multiprocessing
    # import jbmodules
    qmongo = Queue.Queue()
    #print type(argslist), type(argslist)
    i = ''
    for i in argslist: #put 30 tasks in the queue
        if i:
            #print i, ' Is a file to add to mongo argslist'
            qmongo.put([i])

    ## Return for
    restest = ''
    if i:
        restest = '/'.join(i[1].split('/')[:-1])

    def mongoworker():

        count = 0
        while True:
            item = qmongo.get()
            #print item, ' MongoWorker'
            if item is None:
                break
            elif item is not None:
                res, destpath = mongo_update_url_dest_info(item)
                if not res and res is not False:
                    #print ' NewsIt NotRes', count, res
                    pass
                elif res != 'Duplicate':
                    pass #print ' NotRes Duplicate count is --> ', res, destpath
                elif res == 'Duplicate' and destpath is not None:
                    ## Then remove the download and delete
                    try:
                        import os
                        os.remove(destpath)
                        print ' -- MongoWorkerRemoved ', destpath, res
                    except OSError:
                        print ' OSError in MongoWorker '
                        pass
                    print ' Removed Duplicate image ', destpath.split('/')[-2], ' ---> ', item[0], ' Style\v ', destpath.split('/')[-1]

            print ' Mongo Res Done', res
            # try:
            #     insertres =  jbmodules.mongo_image_prep.insert_gridfs_extract_metadata(item)
            # except:
            #     insertres =  jbmodules.mongo_image_prep.update_gridfs_extract_metadata(item)
            count += 1
            #print count, res, item, ' <-- now task done MongoWorker' ## '\n\t', imgdata
            qmongo.task_done()

    jobcount = multiprocessing.cpu_count() - 2 #len(argslist) #detect number of cores
    print("Creating %d threads for the MongoMachine" % jobcount)
    for i in xrange(jobcount):
        tmongo = threading.Thread(target=mongoworker)
        tmongo.daemon = True
        tmongo.start()

    qmongo.join() #block until all tasks are done
    print 'Mongo Upsert threads done'
    if restest:
        return restest
    else:
        return


def main(vendor=None, vendor_brand=None, dest_root=None, ALL=None):
    sys.path.append('/usr/local/batchRunScripts/mozu')
    sys.path.append('/usr/local/batchRunScripts/python')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/mongo_tools')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/image_processing')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace')
    countimage = 0
    countstyle = 0
    if not dest_root:
        dest_root='/mnt/Post_Complete/Complete_Archive/MARKETPLACE'
    if not ALL:
        ALL = ''
    if not vendor:
        vendor = '_'

    ################################
    # Get the New Style's Urls ####
    #########
    ## 1 ## Query for new Marketplace Styles
    # global single_flag
    single_flag = ''
    testflag = str(vendor)
    if testflag.isdigit() and len(testflag) == 9:
        single_flag = str(vendor)
    marketplace_styles=sqlQuery_GetIMarketplaceImgs(vendor=vendor, vendor_brand=vendor_brand, po_number='', ALL=ALL)

    #########
    #  Create 2 item tuple list of every style with valid incomplete urls
    #  Each Tuple contains a full remote url[0] and a full absolute destination file path[1]
    #########
    ## 1A ## Parse Query Result creating 2 item tuples as a list for multi thread
    urlsdload_list = parse_mplace_dict2tuple(marketplace_styles, dest_root=dest_root)
    ## Download the urls in the 2 tuple list
    ########
    ########
    ## 2 ###
    # Download the tuples urls
    multi_url_downloader(argslist=urlsdload_list)
    print 'Done with downloader ', len(urlsdload_list)
    #########
    ## 2A ##
    #  Import urls and download data+imageBlob into mongo db grisfs_mrktplce
    ##########################
    res = ''
    #res = mongo_upsert_threaded(argslist=urlsdload_list)
    print ' Done With 2B Mongo Upsert Threads'
    ##########################
    ########
    ## TDO: Make possible to include all the urls in 1 queue and send/add to and process and upload queue
    ## Process the files running each brand in a separate parallel process
    ########
    # 3A Set root image dir from res or default
    if vendor != '_' or vendor_brand:
        print res, ' <-- CoercedUnicode Failed Cuz of None Type'
        import os.path
        #if res is not None and os.path.isdir(res):
        #    root_img_dir = res
        #    print ' If Vend/VendBrd ResIsDir rootimgdir --> ', res
        #elif os.path.isdir(os.path.join(dest_root, vendor)):
        #    root_img_dir = os.path.join(dest_root, vendor, '*')
        #    print ' If Vend/VendBrd ResNOT-Dir rootimgdir then res --> ', root_img_dir, res
        #else:
        if ALL:
            root_img_dir = dest_root
        elif res is not None and os.path.isdir(res):
            root_img_dir = res
        else:
            root_img_dir = dest_root
        print ' YES to the vend Res-->IsNotDir AND rootimgdir --> ', res
    else:
        root_img_dir = dest_root
        print ' Not vend Res-->IsDir AND rootimgdir --> ', res

    #########
    ## 3X ### Process the images
    #
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    import multiprocmagick2 as multiprocmagick2
    #import jbmodules.image_processing.marketplace.multiprocmagick2 as multiprocmagick2

    #multiprocmagick.funkRunner2(root_img_dir=root_img_dir)
    print 'Single Flaggin It with --> ', single_flag, '\n', urlsdload_list
    ## This is where almost all the work begins...
    multiprocmagick2.funkRunner3(root_img_dir=root_img_dir, single_flag=single_flag)
    print 'Done With multiprocmagick --> ', root_img_dir


if __name__ == '__main__':
    import sys
    try:
        vendor = sys.argv[1]
        # Uncomment and complete to use po number in SQL query
        # if vendor.isdigit() and len(vendor) == 6:
        #     po_number = vendor
        # else: pass
        try:
            vendor_brand = sys.argv[2]
            ALL = ''
            if sys.argv[2][-3:].upper() == 'ALL' or sys.argv[2].isdigit() == True or sys.argv[2].lower() == 'url':
                ALL = sys.argv[2]
                vendor_brand = ''
            main(vendor=vendor, vendor_brand=vendor_brand, ALL=ALL)
        except IndexError:
            main(vendor=vendor)
    except IndexError:
        main()


## Its the Goods! 0307150250
