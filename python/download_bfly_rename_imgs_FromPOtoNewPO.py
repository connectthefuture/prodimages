#!/usr/bin/env python
import os, sys, re, csv


def sqlQuery_oldimage_newpo_duplimerge(oldpo, newpo):
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    query_image_duplimerge ="""with data as (
                                SELECT POMGR.PO_LINE.PO_HDR_ID      AS ponumber,
                                  POMGR.PRODUCT_COLOR.ID            AS colorstyle,
                                  POMGR.PRODUCT_COLOR.VENDOR_STYLE  AS vendor_style
                                FROM
                                  POMGR.PO_LINE
                                JOIN POMGR.PRODUCT_COLOR
                                ON
                                  POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID
                                WHERE
                                  POMGR.PO_LINE.PO_HDR_ID IN ('{0}', '{1}')
                                order by 3, 2 desc)
                                select count(distinct DATA.COLORSTYLE), DATA.VENDOR_STYLE, min(DATA.COLORSTYLE) as oldstyle, max(DATA.COLORSTYLE) as newstyle
                                from data
                                group by DATA.VENDOR_STYLE
                                having min(DATA.PONUMBER) <> max(DATA.ponumber)
                                and count(distinct DATA.COLORSTYLE) = 2;
                                order by
                                  colorstyle DESC""".format(oldpo, newpo)

    result = connection.execute(query_image_duplimerge)

    merge_styles = []
    for row in result:
        styles = {}
        styles['oldstyle'] = row['oldstyle']
        styles['newstyle'] = row['newstyle']
        merge_styles.append(styles)
    connection.close()
    return merge_styles


def sqlQuery_GetStyleVendor_ByPO(ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"

    # AND POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE like '%vendornum%'"

    result = connection.execute(querymake_StylesByPO)
    styleslist = []
    for row in result:
        #style = {}
        #style['vendor_style'] = row['vendor_style']
        #consigstyle['vendor_style'] = row['vendor_style']
        #styles[row['colorstyle']] = style
        style = row['colorstyle']
        styleslist.append(style)
    #print consigstyles
    connection.close()
    return styleslist


def url_download_file(url,dest_filepath):
    import urllib
    resp = urllib.urlretrieve(url, dest_filepath)
    if resp and resp.ok:
        print "Retrieved: " + url + " ---> " + dest_filepath
        return dest_filepath
    else:
        return


def main():
    #### Run ###
    import sys, urllib
    from os import chdir,curdir,path
    args = sys.argv[1:]
    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')
    args1 = args[0].split('\n')   #(','.join(str(arg) for arg in args)).split('\n')
    try:
        if len(args1) == 2 and args1[1].isdigit():
            oldponum = args1[0]
            newponum = args1[1]
            merge_styles = sqlQuery_GetStyleVendor_ByPO(oldponum, newponum)
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
        try:
            url_download_file(netsrv101_url_file, renamed_from_newpo_toload)
            alt = 0
            for x in range(1,6):
                try:
                    alt = x
                    ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
                    colorstyleoldalt = old_colorstyle + ext_ALT
                    netsrv101_url_filealt = path.join(netsrv101_url, old_colorstyle[:4], colorstyleoldalt)
                    colorstylenewalt = new_colorstyle + ext_ALT
                    renamed_from_newpo_toloadalt = path.join(path.abspath(path.expanduser('~')), 'Pictures', colorstylenewalt)
                    if url_download_file(netsrv101_url_filealt, renamed_from_newpo_toloadalt):
                        url_download_file(netsrv101_url_filealt, renamed_from_newpo_toloadalt)
                except IOError:
                    pass
        except IOError:
            pass
