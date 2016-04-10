#!/usr/bin/env python
# coding: utf-8


# single style or multistyle list
def get_media_version_number(colorstyle):
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


def set_media_version_number_single(productColorId, media_version,**kwargs):
    import requests, json
    headers = {"Content-Type": "application/json"}
    media_version_api_url = 'http://ccapp102.l3.bluefly.com:17080/manager/api/v2/productsattributes/update'
    qa_media_version_api_url = 'http://manager.qa.bluefly.com/manager/api/v2/productsattributes/update'
    dest_url = kwargs.get('dest_url', media_version_api_url)
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
    res = requests.put(dest_url, data=json.dumps(update_products_dict), headers=headers)
    return res


def build_media_version_number_data_batch(colorstyles,**kwargs):
    import requests, json
    from collections import defaultdict
    headers = {"Content-Type": "application/json"}
    media_version_api_url = 'http://ccapp102.l3.bluefly.com:17080/manager/api/v2/productsattributes/update'
    qa_media_version_api_url = 'http://manager.qa.bluefly.com/manager/api/v2/productsattributes/update'
    dest_url = kwargs.get('dest_url', media_version_api_url)
    products = {}
    products['products'] = []
    product_styles = {}
    prod_style_ver_dict = get_media_version_number(colorstyles)
    #prod_style_ver_dict =  {'382835401': 3, '382835901': 4, '382836901': 4}
    for style,ver in prod_style_ver_dict.items():
        try:
            vernew = str(int(ver) + 1)
            product_style_data_item = { "productColorId": style,
                                     "attributes": [{ "name": "media_version", "value": vernew }],
                                     # "name": "alternate_image1", "value": "N"},
                                     }
            product_styles.setdefault(vernew, []).append(product_style_data_item)
            products['products'].append(product_style_data_item)
        except TypeError:
            print 'NoneType Passing 106'
    print "\n\nSending Version info for\n", products
    return products
    res = requests.put(dest_url,data=json.dumps(products), headers=headers)
    return res


def _exec_put_data_batch(**kwargs):
    import requests, json
    media_version_api_url    = 'http://ccapp102.l3.bluefly.com:17080/manager/api/v2/productsattributes/update'
    qa_media_version_api_url = 'http://manager.qa.bluefly.com/manager/api/v2/productsattributes/update'
    dest_url = kwargs.get('dest_url', media_version_api_url)
    headers = kwargs.get('headers', {"Content-Type": "application/json"} )
    data = kwargs.get('data', '')
    if data and headers:
        res = requests.put(dest_url,data=json.dumps(data),headers=headers)
        print res.headers, dest_url
        return res
    else:
        print 'Either data or Headers not supplied '


def batch_process_by_style_list(colorstyles):
    data = build_media_version_number_data_batch(colorstyles)
    res = _exec_put_data_batch(data=data)
    print 'Done with {0}'.format(data)
    return res

def generic_increment_style_single(colorstyle):
    data = get_media_version_number(colorstyle).items()
    res = set_media_version_number_single(data[0][0],str(int(data[0][1])))
    return res


import argparse
#
# Define and Instantiate parser Base
parser = argparse.ArgumentParser(description='Utility functions to get and set media_version attrib for image updates and versioning of image url', add_help=True)
##############################
#
######### Style ##############
parser.add_argument('--get-version', default=False, action='store_true', help='Supply a valid 9 digit colorstyle to get the current media_version')
parser.add_argument('--set-version', default=False, action='store_true', help='Supply a valid 9 digit colorstyle AND the new media_version to set')
parser.add_argument('--style', '-s', action='store', help='A Valid 9 Digit Bluefly Style' )
parser.add_argument('--version', '--media-version', action='store', help='Valid 9 Digit Bluefly Style' )
parser.add_argument('--batch', '-b', default=False, action='store_true', help='Set flag if batch inserts are desired and a list of styles numbers are supplied')
#
######## Styles List 1 or more
parser.add_argument('styles_list', action='append', nargs=argparse.REMAINDER, help='Valid 9 Digit Bluefly Style Numbers. Each style must be separated by a space.' )
#
#
if __name__ == '__main__':
    import sys, json
    #args = sys.argv[1:]
    # parsed = parser.parse_args(sys.argv)
    # args = parsed.__dict__
    # print args.items()
    args=sys.argv[1:]
    if len(args) == 2 and len(args[-1]) < 9:
        set_media_version_number_single(args[0],args[1])
        print '1'
    elif len(args) >= 1 and len(args[-1]) == 9:
        print '22'
        batch_process_by_style_list(args)
    else:
        stylevers = get_media_version_number(args)
        print '333\n\nNo changes sent\n'
        print stylevers
