#!/usr/bin/env python

def sqlQuery_GetStyleVendor_ByPO(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is null AND POMGR.PRODUCT_COLOR.ID = '" + colorstyle + "'"
    
    # AND POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE like '%JACQUESLEMANS%'"

    result = connection.execute(querymake_StylesByPO)
    styles = {}
    for row in result:
        style = {}        
        style['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        styles[row['vendor_style']] = style
        
    #print consigstyles
    connection.close()
    return styles

def url_download_file(url,filepath):
    import urllib
    error_check = urllib.urlopen(url)
    urlcode_value = error_check.getcode()
    print urlcode_value
    if urlcode_value == 200:
        urllib.urlretrieve(url, filepath)
        print "Retrieved: " + url + " ---> " + filepath
    elif urlcode_value == 404:
        url_split = url.split('/')[-1]
        url_split = url_split.split('-')[1:]
        url_split = '-'.join(url_split)       
        url_parent = url.split('/')[:-1]
        url_parent = '/'.join(url_parent)
        url = os.path.join(url_parent, url_split)
        try:
            urllib.urlretrieve(url, filepath)
            print "Retrieved: " + url + " ---> " + filepath
        except:
            print "Failed {0} on 2nd Try".format(url)
    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)
        


def build_url_colorstyle_dict(file):
    import csv
    filedict = {}
    with open(file, 'rbU') as f:
        reader = csv.reader(f, dialect=csv)
        for row in reader:
            localdict = {}
            localdict['url'] = row[2]
            localdict['style'] = row[1]
            filedict[row[1]] = localdict
    return filedict


########### RUN ########

import csv,datetime,os,sys
dt = str(datetime.datetime.now())
today = dt.split(' ')[0]

## Should be run after Imap get attachments so that todays swi file is used
try:
    file = sys.argv[1]
except:
    file = os.path.join('/mnt/Post_Complete/.Vendor_to_Load/feeds', today + '_sku-luxury-conv.csv')

## Completed Downloads

upload_drop = '/Users/johnb/Documents/swi_1000_dload'
## upload_drop = '/mnt/Post_Complete/.Vendor_to_Load/upload_drop'

daily_dir = os.path.join(upload_drop, today + '_jpgs')
try:
    os.mkdir(daily_dir, 16877)
except OSError:
    pass


filedict = build_url_colorstyle_dict(file)


for k,v in filedict.iteritems():
    os.chdir(daily_dir)
    
    vendor_url = v['url']
    vendor_url_back = vendor_url.replace('.jpg', '-back.jpg')
    vendor_url_side = vendor_url.replace('.jpg', '-side.jpg')
    
    colorstyle = k + "_1.jpg"
    colorstyle_back = k + "_2.jpg"
    colorstyle_side = k + "_3.jpg"
    
    colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
    colorstyle_back_file = os.path.join(os.path.abspath(os.curdir), colorstyle_back)
    colorstyle_side_file = os.path.join(os.path.abspath(os.curdir), colorstyle_side)
    imagefalse = sqlQuery_GetStyleVendor_ByPO(k)
    if imagefalse:
        try:            
        #print imagefalse,vendor_url, colorstyle_file
            url_download_file(vendor_url,colorstyle_file)
            #url_download_file(vendor_url_back,colorstyle_back_file)
            #url_download_file(vendor_url_side,colorstyle_side_file)
        except:
            print "Failed {}{}".format(vendor_url,colorstyle_file)
            #print swiurl
        
        
#for k,v in stylesDict.iteritems():
#    for val in v:
#        vendor_url = 'http://admin.swisswatchintl.com/Z/'
#        vendor_style = k + ".jpg"
#        colorstyle = str(v[val]) + ".jpg"
#        #vendor_stripped = k
#        vendor_file = vendor_url + vendor_style
#
#        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
#        # 
#        #print vendor_file, colorstyle_file
#        #try:
#        url_download_file(vendor_file,colorstyle_file)