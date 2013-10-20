#!/usr/bin/env python
import os, sys, re, csv
#
#import imap_get_attachments_gmail_UNSEENDiffed
#
#imap_get_attachments_gmail_UNSEENDiffed()
#
## echo "imap_get_attachments_gmail_UNSEEN-Diffed Done!"


def sqlQuery_geturl_ifmissing_image(style):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PRODUCT_COLOR.IMAGE_READY_DT AS image_status FROM POMGR.PRODUCT_COLOR WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is null AND POMGR.PRODUCT_COLOR.ID = '" + style + "'"
    
    # AND POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE like '%JACQUESLEMANS%'"

    result = connection.execute(querymake_StylesByPO)
    styles = {}
    for row in result:
        style = {}        
        style['colorstyle'] = row['colorstyle']
        style['image_status'] = row['image_status']
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
            if urlcode_value == 200:
                urllib.urlretrieve(url, filepath)
                print "2nd Try Retrieved: " + url + " ---> " + filepath
            else:
                print "Error 404:\tFile Not Found\n\t\t" + url + " ---> " + filepath
        except:
            print "Failed {0} on 2nd Try".format(url)
    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)
        
    

def write_excel_error_log(csvfile):
    import csv
    import xlrd
    import sys
    import os


    homedir = os.path.expanduser("~")
    #csvfile = os.path.join(homedir, "zimages1_photoselects.csv")
    outfile = os.path.join(homedir, "outfile.csv")
    xlfile = open((os.path.join(homedir, "compiled.csv")), 'rb')

    
    book = xlrd.open_workbook(xlfile)
    sh = book.sheet_by_index(0)

    convWriter = csv.writer(sys.stdout)

    for rowx in range(sh.ncols):
        convWriter.writerow(xlfile)
        


#####

csvfile = '/Volumes/Post_Complete/.Vendor_to_Load/feeds/sku-conv.csv'
    

missingdict = {}
with open(csvfile,'rbU') as f:
    reader = csv.reader(f,dialect=csv)
    
    for row in reader:
        vendorurl = row[2]
        colorstyle = row[1]
        vendorstyle = row[0]
        filepath = os.path.join(os.path.abspath('/Users/johnb/Pictures/SWI'), colorstyle + "_1.jpg")
        
        res = sqlQuery_geturl_ifmissing_image(colorstyle)
        if res:
            url_download_file(vendorurl,filepath)
            print res, vendorurl, colorstyle
        else:
            print "No Result".format(colorstyle)