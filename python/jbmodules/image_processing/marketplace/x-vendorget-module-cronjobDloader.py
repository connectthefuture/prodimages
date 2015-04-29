#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        if not ALL:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 ORDER BY POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last".format(vendor)

        #not null prd cmp
        else:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_IMAGE.created_date as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.SUPPLIER_INGEST_IMAGE.created_date >= sysdate - {1} and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6 and (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS NOT NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_IMAGE.created_date DESC nulls last, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, kwargs.get('date_range_int', '45'))

    elif vendor_brand:
        # below is only incomplete
        # 
        if not ALL:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND LIKE '%{1}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, vendor_brand)
        # below is prod not null
        else:
            query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS not NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%' and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND LIKE '%{1}%' AND POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%') ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor, vendor_brand)


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


def parse_mplace_dict2tuple(styles_dict,dest_root=None):
    import os.path
    mproc_tuple_Qlist = []
    for k,v in styles_dict.iteritems():
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
        destdir  = os.path.join(dest_root, str(vendor_name), str(po_number))
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

    return mproc_tuple_Qlist


def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata


def download_mplce_url(urldest_tuple):
    import requests, re, urllib, urllib2, subprocess
    import os.path
    countimage = 0
    countstyle = 0
    image_url, destpath = urldest_tuple
    destdir = os.path.dirname(destpath)
    alt_number = destpath.split('_')[-1][0]
    try:
        image_url = 'https://www.drop'.join(image_url.split('https://wwwop'))
    except:
        pass
    ########################################################  
    ########################################################
    ## Image URL Cleanup and Replace Extraneous/Bad Chars ##
    ########################################################
    ####### Dropbox Fix for View vs DL value ###############
    regex_dbx = re.compile(r'^https://www.dropbox.com/.+?\.[jpngJPNG]{3}$')
    image_url = image_url.replace('?dl=0', '?dl=1')
    if regex_dbx.findall(image_url):
        image_url.replace('.jpg', '.jpg?dl=1')
        image_url.replace('.png', '.png?dl=1')
    ########################################################
    ####### URL ENCODED % ESCAPES Fix ######################
    ## Strip error causing Line Feed ascii char
    image_url = ''.join(image_url.split('%0A'))
    ########################################################
    ############       Finally     #########################
    #####     Replace ALL url encoding % escapes    ########
    ###  TWICE TO ACCOUNT FOR EX. %2520 --> %20 --> ' '  ###
    # image_url  = image_url.replace('/Flat%2520Images/', '/Flat%20Images/')
    # print image_url, ' URL'
    regex_validurl = re.compile(r'^http[s]?://.+?$', re.U)
    regex_drive2 = re.compile(r'^(https://d(.+?)\.google\.com/).*\?id\=(?P<fileId>.+?)\&?.*?$', re.U)
    
    # regex_dropbox = re.compile(r'^https?://www.dropbox.com/.+?\.[jpngJPNG]{3}$')

    ######################
    #### BOX API AUTH ####
    # regex_boxapi  = re.compile(r'^(https?)?(?:\://)?(.*)?app.box.com/(.+)?(\.?[jpngJPNG]{3,4})(.*?)?\??(.*?)?$', re.U)
    # if regex_boxapi.findall(image_url):
    #     #import jbmodules.http_tools.auth.Box.boxapi_auth_downloader as boxapi_auth_downloader
    #     #final_path = boxapi_auth_downloader.download_boxapi_drive_file(image_url=image_url, destpath=destpath)
    #     #if final_path:
    #         #return final_path
    #     pass
    # else:
    #     pass
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
    if regex_drive2.findall(image_url):
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

    #############
    ## No Auth ##
    elif regex_validurl.findall(image_url):
        import httplib2
        image_url = httplib2.urlnorm(httplib2.urllib.unquote(image_url))[-1]
        #print 'RRR final', image_url
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:33.0) Gecko/20100101 Firefox/33.0'}
        ########################################################
        ####### Google Drive Fix ###############################
        ########################################################
        ## regex_drive = re.compile(r'^(https://drive.google.com/.+?)/edit\?usp=sharing$')
        regex_drive = re.compile(r'^(https://d(.+?)\.google\.com/.+?)/edit\?usp\=.*?$')
        if regex_drive.findall(image_url):
            image_url = image_url.split('/edit?')[0]
        else: pass

        try:
            print image_url, destpath
            if not image_url[:5] == 'https':
                res = requests.get(image_url, timeout=5, headers=headers)
                #print ' HTTP Yippie ', res
            else:
                res = requests.get(image_url, timeout=10, verify=False, headers=headers)
                #print ' HTTPS Oh Yes ', res
            print 'ALMOST'
            urlcode_value = res.status_code
            print urlcode_value
            if urlcode_value == 209:
                print urlcode_value 
                #res = urllib.urlretrieve(image_url, destpath)
                res = requests.get(image_url, timeout=1, headers=headers)
                with open(destpath, 'w+') as f:
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
                    print 'TRY'
                    res = requests.get(image_url, timeout=5, verify=False, headers=headers)
                    with open(destpath, 'w+') as f:
                        f.write(res.content)
                        f.close()
                    print res
                    return destpath
                except:
                    #subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                    print 'Failed Downloading HTTPS file {}'.format(image_url)

            elif urlcode_value == 404:
                ########## Temp Mrktplce MErchantry workaround to fix their urls they are feeding ###
                import urllib3
                print ' 404 Trying Urllib3 ', image_url
                hostname = urllib3.get_host(image_url)[1]
                if hostname == 'marketplace.merchantry.com':
                    image_url = image_url.replace(hostname, 'pim2.merchantry.com')
                elif hostname == 'pim1.merchantry.com':
                    image_url = image_url.replace(hostname, 'pim2.merchantry.com')
                else:
                    print hostname, ' MERCHANTRY URLs Respond with 404 Errors '
                #######################################################################################
                
                #######################################################################################
                
                try:
                    print 'TRY'
                    res = requests.get(image_url, timeout=1,headers=headers)
                    with open(destpath, 'w+') as f:
                        f.write(res.content)
                        f.close()
                    print res, ' 2nd Attempt using Merchantry Replaced URL OK'
                    return destpath
                except requests.exceptions.ConnectionError:
                    print 'ConnectionError FinalFailureNotice'
                    import os.path
                    print urlcode_value
                    badurldir = os.path.join(destdir,'error404')
                    if os.path.isdir(badurldir):
                        pass
                    else:
                        try:
                            os.makedirs(badurldir, 16877)
                        except:
                            pass
                    try:
                        with open(os.path.join(os.path.abspath(badurldir), image_url + '_error404.txt'), 'a+') as f:
                            f.write("{0}\t{1}\n".format(image_url + '_imgnum_' + '_errcode_' + urlcode_value))
                            return destpath
                    except:
                        print 'Print Failed write 404 file'
                        pass

        # except requests.exceptions.ConnectionError:
        #     print 'ConnectionError'
        #     pass
        except IOError:
            pass


def multi_url_downloader(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import subprocess
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
                if metadata['File:MIMEType'] is not None and metadata['File:MIMEType'].split('/')[0] != 'image':
                    import os
                    os.remove(downloaded_file)
                    #print metadata['File:MIMEType'], ' <--BadImage - Removed --> ', downloaded_file
                    q.task_done()
                else:    
                    count += 1
                    #print count, ' NotRemoved --> ', downloaded_file, metadata['File:MIMEType']
                    q.task_done()
            except AttributeError:
                #print 'AttributeError --> ', downloaded_file
                q.task_done()
            except KeyError:
                #print 'KeyError --> ', downloaded_file
                try:
                    import os
                    os.remove(downloaded_file)
                except:
                    pass
                q.task_done()

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
    hostname             = 'mongodb://mongo:mongo@prodimages.ny.bluefly.com:27017/gridfs_mrktplce' # 'mongodb://relic7:mongo7@ds031591.mongolab.com:31591/gridfs' # None
    db_name              = hostname.split('/')[-1]
  
    if image_url:
        #import jbmodules
        #from jbmodules import mongo_tools
        import sys, os
        jbmade = os.path.join('../..', os.path.dirname(__file__))
        print jbmade
        sys.path.append(jbmade)
        sys.path.append('/usr/local/batchRunScripts/python/jbmodules')
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
            if item is not None:
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
            else:
                #print ' NewsIt WITHALITTLE --> RES'
                pass
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
    res = mongo_upsert_threaded(argslist=urlsdload_list)
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
    multiprocmagick2.funkRunner3(root_img_dir=root_img_dir)
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
            if sys.argv[2] == 'ALL':
                ALL = 'ALL'
                vendor_brand = ''
            main(vendor=vendor, vendor_brand=vendor_brand, ALL=ALL)
        except IndexError:
            main(vendor=vendor)
    except IndexError:
        main()


## Its the Goods! 0307150250
