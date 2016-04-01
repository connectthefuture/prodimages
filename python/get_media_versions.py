#!/usr/bin/env python
# coding: utf-8


def query_version_number(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    if type(colorstyle) == list and len(colorstyle) > 1:
        colorstyles = colorstyle
        colorstyles = tuple(["{0}".format(s) for s in colorstyles])
        #querymake_version_number = "SELECT DISTINCT POMGR.PO_LINE.PRODUCT_COLOR_ID as colorstyle, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.VERSION as version FROM POMGR.PRODUCT_COLOR RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID RIGHT JOIN POMGR.PO_HDR ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID RIGHT JOIN POMGR.VENDOR ON POMGR.VENDOR.ID = POMGR.PO_HDR.VENDOR_ID INNER JOIN POMGR.LK_PO_TYPE ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID LEFT JOIN POMGR.INVENTORY ON POMGR.INVENTORY.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID LEFT JOIN POMGR.PRODUCT_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PRODUCT_COLOR_ID in {0} ORDER BY POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last, POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last".format(colorstyles)
    # Multiple
        qry= """SELECT DISTINCT
              POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID AS "colorstyle",
              POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION    AS "media_version",
              POMGR.PRODUCT_COLOR_DETAIL.ZOOM_IMAGE as "base_zoom",
              POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE as "0",
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
              POMGR.PRODUCT_COLOR_DETAIL.ZOOM_IMAGE as "base_zoom",
              POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE as "0",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1 as "1",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2 as "2",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_3 as "3",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_4 as "4",
              POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_5 as "5",
              POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH as "swatch"
            FROM
              POMGR.PRODUCT_COLOR_DETAIL
            WHERE
              POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID like '{0}%'
              """.format(colorstyle)
    #else:
    #    querymake_version_number = "SELECT DISTINCT POMGR.PO_LINE.PRODUCT_COLOR_ID as colorstyle, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.VERSION as version FROM POMGR.PRODUCT_COLOR RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID RIGHT JOIN POMGR.PO_HDR ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID RIGHT JOIN POMGR.VENDOR ON POMGR.VENDOR.ID = POMGR.PO_HDR.VENDOR_ID INNER JOIN POMGR.LK_PO_TYPE ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID LEFT JOIN POMGR.INVENTORY ON POMGR.INVENTORY.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID LEFT JOIN POMGR.PRODUCT_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PRODUCT_COLOR_ID like '%{0}%' ORDER BY POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last, POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last".format(colorstyle)

    try:
        result = connection.execute(qry)
        styles = {}
        for row in result:
            #style_info = {}
            #style_info['version'] = row['version']
            # Convert Colorstyle to string then set as KEY
            styles[str(row['colorstyle'])] = row['media_version']
        return styles
    except sqlalchemy.exc.DatabaseError:
        print 'This Search needs to have at least 1 style supplied as args, \nyou returned zero results.'

    finally:
        connection.close()


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    stylevers = query_version_number(args)
    print stylevers
