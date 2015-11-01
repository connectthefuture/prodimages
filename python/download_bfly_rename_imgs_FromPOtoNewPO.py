#!/usr/bin/env python

import pdb;pdb.set_trace()


def sqlQuery_oldimage_newpo_duplimerge(oldpo, newpo):
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    query_image_duplimerge = "WITH data AS ( SELECT POMGR.PO_LINE.PO_HDR_ID AS ponumber, POMGR.PRODUCT_COLOR.ID  AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, sum( case when POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null   then 1   else null end ) is_ready FROM POMGR.PO_LINE JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PO_LINE.PO_HDR_ID IN ('{0}', '{1}') GROUP BY POMGR.PO_LINE.PO_HDR_ID, POMGR.PRODUCT_COLOR.ID, POMGR.PRODUCT_COLOR.VENDOR_STYLE ORDER BY 3, 4 asc nulls last, 2 DESC ) SELECT COUNT(DISTINCT data.colorstyle), data.vendor_style, MIN(data.colorstyle) as oldstyle, MAX(data.colorstyle)  as newstyle,  data.is_ready FROM data GROUP BY data.vendor_style, data.is_ready HAVING COUNT(data.vendor_style) = 2 AND MIN(data.colorstyle) <> MAX(data.colorstyle) order by data.is_ready nulls last".format(oldpo, newpo)
    result = connection.execute(query_image_duplimerge)
    merge_styles = []
    total_count_rem = result.rowcount
    total_count_incr = 0
    for row in result:
        styles = {}
        styles['oldstyle'] = str(row['oldstyle'])
        styles['newstyle'] = str(row['newstyle'])
        total_count_incr += 1
        total_count_rem -= 1
        print "Styles Total: {}\vRemaining: {}".format(total_count_incr, total_count_rem)
        merge_styles.append(styles)
    connection.close()
    return merge_styles


def url_download_file(url,dest_filepath):
    import urllib
    try:
        resp = urllib.urlretrieve(url, dest_filepath)
        if resp:
            print "Retrieved: " + url + " ---> " + dest_filepath
            return dest_filepath
        else:
            return
    except IOError:
        print 'IOERROR 30'

# def url_download_file(url,dest_filepath):
#     import requests
#     resp = requests.get(url, dest_filepath)
#     if resp:
#         print "Retrieved: " + url + " ---> " + dest_filepath
#         with open(dest_filepath, 'wb+') as f:
#             f.write(resp.content)
#         return dest_filepath
#     else:
#         return


def main():
    #### Run ###
    import sys, urllib
    from os import chdir,curdir,path
    args = sys.argv[1:]
    print 'Moving images from PO: {} to PO --> {}'.format(*args)
    try:
        if len(args) == 2:
            merge_styles = sqlQuery_oldimage_newpo_duplimerge(*args)
        else:
            print "You neew to provide both the original po number and the po number to move images to.\nPo numbers are 6 digits each separated by a space."
            pass
    except IndexError:
        print "Enter at least PO Number as 1st Arg or Nothing will Happen"

    for item in merge_styles:
        netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
        old_colorstyle = item['oldstyle']
        new_colorstyle = item['newstyle']
        ext_PNG     = '.png'
        ext_JPG     = '.jpg'

        netsrv101_url_file = path.join(netsrv101_url, old_colorstyle[:4], old_colorstyle + ext_PNG)
        renamed_from_newpo_toload = path.join(path.abspath(path.expanduser('~')), 'Pictures', new_colorstyle + ext_PNG)

        url_download_file(netsrv101_url_file, renamed_from_newpo_toload)
        alt = 0
        for x in range(1,6):
            alt = x
            ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
            colorstyleoldalt = old_colorstyle + ext_ALT
            netsrv101_url_filealt = path.join(netsrv101_url, old_colorstyle[:4], colorstyleoldalt)
            colorstylenewalt = new_colorstyle + ext_ALT
            renamed_from_newpo_toloadalt = path.join(path.abspath(path.expanduser('~')), 'Pictures', colorstylenewalt)
            if url_download_file(netsrv101_url_filealt, renamed_from_newpo_toloadalt):
                url_download_file(netsrv101_url_filealt, renamed_from_newpo_toloadalt)

if __name__ == '__main__':
    main()
