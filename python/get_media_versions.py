#!/usr/bin/env python
# coding: utf-8

# single style or multistyle list
def get_query_version_number(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    if type(colorstyle) == list and len(colorstyle) > 1:
        colorstyles = colorstyle
        colorstyles = tuple(["{0}".format(s) for s in colorstyles])
    # Multiple
        qry= """SELECT DISTINCT
              POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID AS "colorstyle",
              POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION    AS "media_version",
              POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE as "0m",
              POMGR.PRODUCT_COLOR_DETAIL.ZOOM_IMAGE as "0",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1 as "1",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2 as "2",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_3 as "3",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_4 as "4",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_5 as "5",
              POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH as "swatch"
            FROM
              POMGR.PRODUCT_COLOR_DETAIL
            WHERE
              POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID IN {0} """.format(colorstyles)
    else:
        if type(colorstyle) == list:
            colorstyle=colorstyle[0]
    # Single Style
        qry= """SELECT DISTINCT
                POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID AS "colorstyle",
                POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION    AS "media_version",
                POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE as "0m",
                POMGR.PRODUCT_COLOR_DETAIL.ZOOM_IMAGE as "0",
                POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1 as "1",
                POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2 as "2",

                POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_3 as "3",
                POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_4 as "4",
                POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_5 as "5",
                POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH as "swatch"
            FROM
              POMGR.PRODUCT_COLOR_DETAIL
            WHERE
              POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID = '{0}' """.format(colorstyle)

    try:
        result = connection.execute(qry)
        productId_media_versions = {}
        for row in result:
            # Convert Colorstyle to string then set as KEY
            productId_media_versions[str(row['colorstyle'])] = row['media_version']
        return productId_media_versions
    except sqlalchemy.exc.DatabaseError:
        print 'This Search needs to have at least 1 style supplied as args, \nyou returned zero results.'

    finally:
        connection.close()


def set_media_version_number_single(productColorId, media_version):
    import requests, json
    headers = {"Content-Type": "application/json"}
    media_version_api_url = 'http://ccapp102.l3.bluefly.com:17080/manager/api/v2/productsattributes/update'
    update_products_dict = {
                            "products": [{
                            	"productColorId": productColorId,
                            	"attributes": [{
                            		"name": "media_version",
                            		"value": media_version
                            	}]
                            }],
                            }
    print "Sending Version info for {0} \nData: {1}".format(productColorId,update_products_dict)
    #res = requests.put(media_version_api_url,data=update_products_dict, headers=headers)


def set_media_version_number_batch(colorstyles):
    import requests, json
    headers = {"Content-Type": "application/json"}
    media_version_api_url    = 'http://ccapp102.l3.bluefly.com:17080/manager/api/v2/productsattributes/update'
    QA_media_version_api_url = 'http://manager.qa.bluefly.com/manager/api/v2/productsattributes/update'
    products = {}
    for style,ver in get_query_version_number(colorstyles):
        product_media_version_dict = {}
        product_media_version_dict['productColorId'] = style
        product_media_version_dict['media_version'] = ver.values()
        products[style] = product_media_version_dict
    print "Sending Version info for {0}".format(products)

    #res = requests.put(QA_media_version_api_url,data=products, headers=headers)






if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    stylevers = get_query_version_number(args)
    print stylevers
