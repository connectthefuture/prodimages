#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Pass 9 digit style numbers as sys.argv or main(styles_list)
def make_q(args):
    query_oracle= """
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
            Pomgr.Product_Color.ID in ('{0}')
          ORDER BY
            prodclr_create_dt DESC,
            1 DESC Nulls Last""".format(unicode("','".join(args)))
    return query_oracle


def url_tester(url):
    import requests
    res = requests.get(url)
    #res = requests.request('HEADERS', url)
    http_code = res.status_code
    return http_code


def url_tester_headers(url):
    import requests
    #res = requests.get(url)
    res = requests.request('HEADERS', url)
    headers = res.headers
    return headers


def run_query_outdict(q):
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    # try:
    #     import sys
    #     date_range = str(sys.argv[3])
    #     if date_range.isdigit() == True:
    #         kwargs.update(date_range_int=date_range)
    # except IndexError:
    #     pass
    #print vendor_brand, "Vendorbrand"
    connection = orcl_engine.connect()

    result = connection.execute(q)
    styledata = {}
    resct = len(result.items())
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
        if resct < 100:    
            try:
                style['url_status_code'] = url_tester(row['url'])
            except:
                style['url_status_code'] = 666
        else:
            style['url_status_code'] = 999
        style['image_create_dt'] = row['image_create_dt']
        style['vendor_create_dt'] = row['vendor_create_dt']
        style['vendor_mod_dt'] = row['vendor_mod_dt']
        styledata[str(row['colorstyle'])] = style
    connection.close()
    return styledata


def main(styles_list):
    if len(styles_list) > 1000:
        styles_list = styles_list[-999:]
    
    if len(styles_list) > 0 and len(styles_list) < 1000:
        args = [x for x in styles_list if x.isdigit() and len(x) == 9]
        q = make_q(args)
        result = run_query_outdict(q)
        incompletes = []
        #print q
        count_total = len(result.items())
        count_marketplace_inc = 0
        count_marketplace_inc_404 = 0
        count_error = 0
        for k,v in result.iteritems():
            if v['production_complete_dt']:
                k, v['production_complete_dt']
            else:
                k, v['production_complete_dt']
                incompletes.append((k,v['url'],))
                if v['url']:
                    count_marketplace_inc += 1
                    if v['url_status_code'] >= 300 and v['url_status_code'] != 666:
                        count_marketplace_inc_404 += 1
                    else:
                        count_error += 1
                    print v['colorstyle'], v['url_status_code'], v['url'] 
        if incompletes:
            count_incomplete = len(incompletes)
            count_complete   = count_total - count_incomplete
            count_asset_inc  = count_incomplete - count_marketplace_inc
            res="\nTotal Styles: {0}\n\t\tComplete: {1}\n\t\tIncomplete: {2}\n\t\t\tAsset: {3}\n\t\t\tMarketplace: {4}\v404 Errors: {5}".format(count_total, count_complete, count_incomplete, count_asset_inc, count_marketplace_inc, count_marketplace_inc_404)
            if count_error:
                res = "{0}\n\tMargin of Error: {1}\v{2}".format(res, round((float(count_error) / float(count_total)), 3), count_error)
            print res
            return incompletes
        else:
            print 'Total Styles: {}\n\tNo Matches Found'.format(count_total) ##result
            return None
    else:
        print 'You Need to Enter Some Styles ...'
        pass


if __name__ == '__main__':
    import sys
    main(sys.argv)
