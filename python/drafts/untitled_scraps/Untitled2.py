#!/usr/bin/env python

def sqlQuery_GetStyleVendor_ByPO(ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "' AND POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE like '%NRICCISUN%'"
    
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
    error_value = error_check.getcode()
    print error_value
    urllib.urlretrieve(url, filepath)
#    import requests
#    r = requests.get(url)                    

a=urllib.urlopen('http://www.google.com/asdfsf')
a.getcode()


#### Run ###

import os,sys

try:
    ponum = sys.argv[1]
except:
    print "Enter a PO Number as 1st Arg or Nothing will Happen"

stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)


for k,v in stylesDict.iteritems():
    for val in v:
        vendor_url = 'http://admin.swisswatchintl.com/Z/'
        vendor_style = k + ".jpg"
        colorstyle = str(v[val]) + ".jpg"
        vendor_stripped = k
        vendor_file = vendor_url + vendor_stripped + ".jpg"

        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
        # 
        print vendor_file, colorstyle_file
        try:
            url_download_file(vendor_file,colorstyle_file)
            #os.rename(vendor_style, colorstyle_file)
            
            
            print "Renamed: " + vendor_file + " ---> " + colorstyle_file
        except:
            vendor_file = vendor_file.split('-')[1:]
            #try:
            #    url_download_file(vendor_file,colorstyle_file)
            #except:
            #    print "TOTAL FAILURE: " + vendor_file + " ---> " + colorstyle_file