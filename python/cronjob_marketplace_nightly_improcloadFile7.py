#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sqlQuery_GetIMarketplaceImgs(vendor=None,vendor_brand=None, po_number=None, all_flag=None, updateonly_flag='', update_time=None):
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    # orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    # if not vendor and not vendor_brand and not all_flag:
    #     arg = sys.argv[1]
    #     if arg.isdigit():
    #         all_flag = arg
    #     else:
    #         vendor = arg
    if updateonly_flag:
        updateonly_flag = 'not'
    if not update_time:
        update_time = 20

    ## Exclusion/Inclusion Vars ##
    # Manually Set vendor ID then choose All('') from Vendor and none from other vendors
    # or None('not') from vendid and All From other vendors
    # or comment out for All from All incomplete
    # Usually comment out for everything but allows to exclude slow and redundant vendors info
    vendid = 'Skye'
    if vendid:
        notvendor='not'
    else:
        notvendor=''
    #############################

    connection = orcl_engine.connect()
    if not po_number:
        query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS {1} NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6) and (POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE > trunc(sysdate-{2})) and POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID {3} LIKE '%{0}%' and BLUEFLY_PRODUCT_COLOR not like ('0_%') and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%'  ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendid, updateonly_flag, str(update_time), notvendor)
        # prod complete null vs image null as above only on po search
    else:
        query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS {1} NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.PO_LINE.PO_HDR_ID LIKE '%{0}%'  and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6  and BLUEFLY_PRODUCT_COLOR not like ('0_%') and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ) and BLUEFLY_PRODUCT_COLOR not like ('0_%') ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(po_number, updateonly_flag)
    ##
    ## WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    ## AND POMGR.PRODUCT_COLOR.COPY_READY_DT IS NOT NULL
    ##

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

    #print consigstyles
    connection.close()
    return styles



############################################################ RUN ##################################################
############################################################ RUN ##################################################
import os,re,sys,urllib, glob, re, subprocess, shutil
import requests

## Create image dir Root if not exist
try:
    #imagedir = os.path.abspath(os.path.join(os.path.expanduser('~'),'MARKETPLACE'))
    if sys.argv[1] == 'jblocal':
        imagedir = os.path.abspath('/mnt/Post_Ready/Retouchers/JohnBragato/MARKETPLACE_LOCAL')
    else:
        imagedir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
except IndexError:
    imagedir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
except:
    imagedir = os.path.abspath(os.path.join(os.path.expanduser('~'),'Pictures'))
    # imagedir = os.path.abspath(os.path.join(sys.argv[1], 'Pictures'))


regex_swi   = re.compile(r'^.*?SWI.+?\.jpg$')
if os.path.isdir(imagedir):
    ## Remove previous days imports only from the PO dir prior to new import, SWI stays separate
    remove_prior_import = glob.glob(os.path.join(imagedir, '*/*/*.jpg'))
    try:
        [ os.remove(f) for f in remove_prior_import ]
    except:
        pass
else:
    try:
        os.makedirs(imagedir, 16877)
    except:
        pass


def google_drive_url_handler(image_url):
    ####### Google Drive Fix ###############################
    import re, requests
    regex_drive = re.compile(r'^(https://d(.+?)\.google\.com/.+?)/edit\?usp\=.*?$')
    regex_drive2=re.compile(r'^(https://d(.+?)\.google\.com/).*\?id\=(.*?)\&?.*?$')
    ## Strip query string and edit RETURNNG URL TO IMG ON GOOGLE DRIVE
    if regex_drive2.findall(image_url):
        image_url = requests.get(image_url).url
        #image_url = image_url.split('?')[1]
        #params = (image_url.split('&'))
        print image_url
    if regex_drive.findall(image_url):
        image_url = image_url.split('/edit?')[0]
        print image_url
    return image_url


updateonly_flag = ''
update_time     = ''

#try:
    #updateonly_flag = sys.argv[1]
#    if updateonly_flag:
updateonly_flag = ''
    #try:
    #    update_time = sys.argv[2]
    #except:
update_time = 20
#except IndexError:
#    updateonly_flag = ''
#    pass

countimage = 0
countstyle = 0
update_styles = []
marketplace_styles=sqlQuery_GetIMarketplaceImgs(vendor='', vendor_brand='', po_number='', all_flag='AllCronRun', updateonly_flag=updateonly_flag, update_time=update_time)
for k,v in marketplace_styles.iteritems():
    colorstyle  = v['colorstyle']
    image_url   = v['image_url']
    po_number   = v['po_number']
    vendor_name = v['vendor_name']
    alt_number  = v['alt']

    if len(image_url.split('.')[-1]) == 3:
        ext = '.' + str(image_url.split('.')[-1][:3])
        ext = ext.lower()
    else:
        ext = '.jpg'
    if alt_number:
        bfly_ext = "_{0}{1}".format(alt_number,ext)
        ext = bfly_ext
    destdir  = os.path.join(imagedir, str(vendor_name), str(po_number))
    destpath = os.path.join(destdir, colorstyle + ext)
    badurldir = ''
    if os.path.isdir(destdir):
        pass
    else:
        try:
            os.makedirs(destdir, 16877)
        except:
            pass


    if image_url:
        ########## Temp Mrktplce MErchantry workaround to fix their urls they are feeding ###
        image_url = image_url.replace('https://marketplace.merchantry.com/mp/product/image/', 'http://pim2.merchantry.com/mp/product/image/')
        ########################################################
        ########################################################
        ## Image URL Cleanup and Replace Extraneous/Bad Chars ##
        ########################################################
        ########################################################
        ####### Dropbox Fix for View vs DL value ###############
        ########################################################
        try:
            image_url = 'https://www.drop'.join(image_url.split('https://wwwop'))
        except:
            pass
        regex_dbx = re.compile(r'^https://www.dropbox.com/.+?\.[jpngJPNG]{3}$')
        image_url = image_url.replace('?dl=0', '?dl=1')
        if regex_dbx.findall(image_url):
            image_url.replace('.jpg', '.jpg?dl=1')
            image_url.replace('.png', '.png?dl=1')
        ########################################################
        ########################################################
        ####### Google Drive Fixes #############################
        ########################################################
        ########################################################
        ## regex_drive = re.compile(r'^(https://drive.google.com/.+?)/edit\?usp=sharing$')
        regex_drive = re.compile(r'^(https://d(.+?)\.google\.com/.+?)/edit\?usp\=.*?$')
        regex_drive2=re.compile(r'^(https://d(.+?)\.google\.com/).*\?id\=(.*?)\&?.*?$')
        ## Strip query string and edit RETURNNG URL TO IMG ON GOOGLE DRIVE
        if regex_drive2.findall(image_url):
            image_url = image_url.split('?')[1]
            params = (image_url.split('&'))

        elif regex_drive.findall(image_url):
            image_url = image_url.split('/edit?')[0]
        elif regex_drive2.findall(image_url):
            image_url = google_drive_url_handler(image_url)

        ########################################################
        ########################################################
        ########################################################
        ####### URL ENCODED % ESCAPES Fix ######################
        ## Strip error causing Line Feed ascii char
        image_url = ''.join(image_url.split('%0A'))
        ########################################################
        ########################################################
        regex_validurl = re.compile(r'^http[s]?://.+?$', re.U)

        if regex_validurl.findall(image_url):
            ########################################################
            ############       Finally     #########################
            #####     Replace ALL url encoding % escapes    ########
            ###  TO ACCOUNT FOR EX. %2520 --> %20 --> ' '   ########
            ########################################################
            import httplib2
            image_url = httplib2.urlnorm(httplib2.urllib.unquote(image_url))[-1]
            print 'RRR'
            headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0'}
            try:
                print image_url, destpath #.split('/' )[-1].replace('.jpg','_1200.jpg')
                res = requests.get(image_url, stream=False, timeout=5, headers=headers)
                print 'ALMOST'
                urlcode_value = res.status_code
                print urlcode_value
                if urlcode_value < 404:
                    try:
                        with open(destpath, 'ab+') as f:
                            f.write(res.content)
                            f.close()
                        if res != '2':
                            subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                            # if updateonly_flag:
                            #     update_styles.append(colorstyle)
                    except:
                        subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                        print 'Failed Downloading HTTPS file {}'.format(image_url)
                        # if updateonly_flag:
                        #     update_styles.append(colorstyle)

                elif urlcode_value == 404:
                    badurldir = os.path.join(destdir,'error404')
                    if os.path.isdir(badurldir):
                        pass
                    else:
                        try:
                            os.makedirs(badurldir, 16877)
                        except:
                            pass
                    try:
                        with open(os.path.join(os.path.abspath(badurldir), colorstyle + ext + '_error404.txt'), 'wb+') as f:
                            f.write("{0}\t{1}\n".format(image_url,colorstyle + '_imgnum_' + ext + '_errcode_' + urlcode_value))
                    except:
                        'Print Failed write 404 file'
                        pass
            except IOError:
                pass

    if badurldir:
        badlist = []
        failed = glob.glob(os.path.join(badurldir,'*.txt'))
        [badlist.append(style.split('/')[-1][:9]) for style in failed]
        for f in failed:
            try:
                shutil.move(f,os.path.join(imagedir,'ERRORS'))
            except:
                pass

######## Process Images and Load Downloaded files in VendorNAme-->POnumber subdir of main images dir #####
#dirlist = []
#[dirlist.append(os.path.abspath(g)) for g in glob.glob(os.path.join(imagedir, '*/*')) if os.path.isdir(g)]
import subprocess, multiprocmagick

multiprocmagick.run_multiproccesses_magick(searchdir=imagedir)
print 'Done With multiprocmagick'
