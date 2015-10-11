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
    connection = orcl_engine.connect()
    if not po_number:
        query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.IMAGE_READY_DT IS {1} NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6) and (POMGR.SUPPLIER_INGEST_IMAGE.CREATED_DATE > trunc(sysdate-{2}) or POMGR.SUPPLIER_INGEST_IMAGE.MODIFIED_DATE > trunc(sysdate-{2})) and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%{0}%' ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format('VOID', updateonly_flag, str(update_time))
        # prod complete null vs image null as above only on po search
    else:
        query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS {1} NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.PO_LINE.PO_HDR_ID LIKE '%{0}%'  and POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER <= 6  and BLUEFLY_PRODUCT_COLOR not like ('0_%') and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ) ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(po_number, updateonly_flag)
    ##
    # elif vendor:
    #     #not null prd cmp
    #     #query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS not NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%'  and BLUEFLY_PRODUCT_COLOR not like ('0_%') and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ) ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor)
    #     # null prdcmp
    #     query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID LIKE '%{0}%'  and BLUEFLY_PRODUCT_COLOR not like ('0_%') and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ) ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor)

    # elif vendor_brand:
    #     query_marketplace_inprog = "SELECT DISTINCT POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_number, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID as vendor_name, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND as vendor_brand, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_STYLE as vendor_style, POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_CATEGORY as product_folder, POMGR.SUPPLIER_INGEST_IMAGE.URL as image_url, POMGR.SUPPLIER_INGEST_IMAGE.DOWNLOADED as download_status, POMGR.SUPPLIER_INGEST_IMAGE.IMAGE_NUMBER as alt, POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID as genstyleid, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as production_complete_dt, POMGR.PRODUCT_COLOR.ACTIVE as active, POMGR.SUPPLIER_INGEST_SKU.THIRD_SUPPLIER_ID as third_supplierid, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE as ingest_dt FROM POMGR.SUPPLIER_INGEST_STYLE RIGHT JOIN POMGR.SUPPLIER_INGEST_SKU ON POMGR.SUPPLIER_INGEST_SKU.STYLE_ID = POMGR.SUPPLIER_INGEST_STYLE.ID LEFT JOIN POMGR.SUPPLIER_INGEST_IMAGE ON POMGR.SUPPLIER_INGEST_STYLE.ID = POMGR.SUPPLIER_INGEST_IMAGE.STYLE_ID RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR RIGHT JOIN POMGR.PRODUCT_COLOR ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE (POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT IS NULL and POMGR.SUPPLIER_INGEST_IMAGE.URL IS not NULL) and (POMGR.SUPPLIER_INGEST_STYLE.VENDOR_BRAND LIKE '%{0}%'  and BLUEFLY_PRODUCT_COLOR not like ('0_%') and POMGR.PRODUCT_COLOR.VENDOR_STYLE NOT LIKE '%VOID%' ) ORDER BY POMGR.SUPPLIER_INGEST_STYLE.BLUEFLY_PRODUCT_COLOR Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.CREATED_DATE DESC Nulls Last, POMGR.SUPPLIER_INGEST_STYLE.VENDOR_ID Nulls Last".format(vendor_brand)


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


def post_or_put_style_to_api(colorstyle, api_url=None, AuthToken=None):
    import requests, json
    import http.client, urllib.parse
    if not api_url:
        api_url = 'http://prodimages.ny.bluefly.com/image-update/'

    update_styles = list(set(sorted(update_styles)))
    for colorstyle in update_styles:
        data = {'colorstyle': colorstyle}
        #params = urllib.parse.urlencode(data)
        params = json.dumps(data)
        auth = {'Authorization': 'Token ' + AuthToken}
        content_type = {'content-type': 'application/json'}
        headers = json.dumps(auth,content_type)
        # conn = http.client.HTTPConnection(api_url, 80)
        # conn.request("PUT", "/", BODY)
        #response = conn.getresponse()
        try:
            response = requests.post(api_url, headers=headers, params=params)
            print response.status, response.method, data
            #print(resp.status, response.reason)
        except:
            try:
                response = requests.put(api_url, headers=headers, params=params)
                print response.status, response.method, data
            except:
                curlauth = 'Authorization: Token ' + AuthToken
                curldata = 'colorstyle=' + colorstyle
                try:
                    subprocess.call([ 'curl', '-u', 'james:hoetker', '-d', curldata, '-H', curlauth, '-X', 'PUT', api_url])
                except:
                    subprocess.call([ 'curl', '-u', 'james:hoetker' '-d', curldata, '-H', curlauth, api_url])

############################################################ RUN ##################################################
############################################################ RUN ##################################################
import os,re,sys,urllib, glob, re, subprocess, shutil
import requests

## Create image dir Root if not exist
try:
    #imagedir = os.path.abspath(os.path.join(os.path.expanduser('~'),'MARKETPLACE'))
    imagedir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')

    #imagedir = os.path.abspath(os.path.join('/mnt/Post_Complete/Complete_Archive/SendReceive_BGRemoval/', 'Pictures'))
except:
    imagedir = os.path.abspath(os.path.join(os.path.expanduser('~'),'Pictures'))

    # imagedir = os.path.abspath(os.path.join(sys.argv[1], 'Pictures'))

regex_swi   = re.compile(r'^.*?SWI.jpg$')

if os.path.isdir(imagedir):
    ## Remove previous days imports only from the PO dir prior to new import, SWI stays separate
    remove_prior_import = glob.glob(os.path.join(imagedir, '*/*/*.jpg'))
    try:
        [ os.remove(f) for f in remove_prior_import if not re.findall(regex_swi,f) ]
    except:
        pass
else:
    try:
        os.makedirs(imagedir, 16877)
    except:
        pass

updateonly_flag = ''
update_time     = ''

try:
    updateonly_flag = sys.argv[1]
    if updateonly_flag:
        updateonly_flag = 'not'
    try:
        update_time = sys.argv[2]
    except:
        update_time = 20
except IndexError:
    updateonly_flag = ''
    pass

countimage = 0
countstyle = 0
update_styles = []
vaultstyles=sqlQuery_GetIMarketplaceImgs(vendor='', vendor_brand='', po_number='', all_flag='AllCronRun', updateonly_flag=updateonly_flag, update_time=update_time)
for k,v in vaultstyles.iteritems():
    colorstyle  = v['colorstyle']
    image_url   = v['image_url']
    po_number   = v['po_number']
    vendor_name = v['vendor_name']
    alt_number  = v['alt']

    if len(image_url.split('.')[-1]) == 3:
        ext = '.' + str(image_url.split('.')[-1])
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
        #with open(destpath,'wb') as f:
            #f.write(requests.get(image_url).content)
        try:
            image_url = 'https://www.drop'.join(image_url.split('https://wwwop'))
        except:
            pass


        ########################################################
        ########################################################
        ## Image URL Cleanup and Replace Extraneous/Bad Chars ##
        ########################################################
        ########################################################
        ####### Google Drive Fix ###############################
        regex_drive = re.compile(r'^(https://drive.google.com/.+?)/edit\?usp=sharing$')
        ## Strip query string and edit RETURNNG URL TO IMG ON GOOGLE DRIVE
        if regex_drive.findall(image_url):
            image_url = image_url.split('/edit?')[0]
        ########################################################
        ########################################################
        ####### Dropbox Fix for View vs DL value ###############
        image_url = image_url.replace('?dl=0', '?dl=1')
        ########################################################
        ####### URL ENCODED % ESCAPES Fix ######################
        ## Strip error causing Line Feed ascii char
        import urllib2
        image_url = ''.join(image_url.split('%0A'))
        ########################################################
        ############       Finally     #########################
        #####     Replace ALL url encoding % escapes    ########
        ###  TWICE TO ACCOUNT FOR EX. %2520 --> %20 --> ' '  ###
        image_url = urllib2.unquote(urllib2.unquote(image_url))
        ########################################################
        ########################################################

        try:
            print image_url, destpath #.split('/' )[-1].replace('.jpg','_1200.jpg')
            error_check = urllib.urlopen(image_url)
            urlcode_value = error_check.getcode()
            print urlcode_value

            if urlcode_value == 200:
                res = urllib.urlretrieve(image_url, destpath)
                if res != '2':
                    subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                countimage += 1
                print "Image Download Count: {}".format(countimage)
                if alt_number == 1:
                    countstyle += 1
                print "Total New Styles Downloaded: {}".format(countstyle)
                if updateonly_flag:
                    update_styles.append(colorstyle)
            elif urlcode_value == 403:
                try:
                    res = requests.get(image_url, stream=True, timeout=1)
                    with open(destpath, 'ab+') as f:
                        f.write(res.content)
                        f.close()
                    if res != '2':
                        subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                        if updateonly_flag:
                            update_styles.append(colorstyle)
                except:
                    subprocess.call(['wget','-O','/'.join(destpath.split('/')[:-1]) + '/' + colorstyle + ext, image_url])
                    print 'Failed Downloading HTTPS file {}'.format(image_url)
                    if updateonly_flag:
                        update_styles.append(colorstyle)

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

## Send updated styles to api to clear
if update_styles:
    post_or_put_style_to_api(update_styles, api_url=None, AuthToken=None)
else:
    print 'NO UPDATES TO CLEAR'

# for d in dirlist:
#     # Added try error handler so as not to hold up all vendors if file error from one of them raises CalledProcessError
#     try:
#         subprocess.call(['/usr/local/batchRunScripts/python/magicColorspace_modulate-aspect-normalize_AND_Upload.py', d])
#     except: #subprocess.CalledProcessError:
#         pass
