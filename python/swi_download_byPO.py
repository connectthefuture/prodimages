#!/usr/bin/env python

def sqlQuery_GetStyleVendor_ByPO(ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is null and POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
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
        
        try:
            url = os.path.join(url_parent, url_split)
            error_check = urllib.urlopen(url)
            urlcode_value = error_check.getcode()
            #print urlcode_value
            
            if urlcode_value == 200:
                urllib.urlretrieve(url, filepath)
                print "On 2nd Attempt, Retrieved: " + url + " ---> " + filepath

            elif urlcode_value == 404: 
                print "Failed Downloading URL {0} on 2nd Attempt with Error Code {1}".format(url, urlcode_value)
            
            else:
                print "Totally Failed Downloading URL {0} on 2nd Attempt with Error Code {1}".format(url, urlcode_value)
        
        
        except:
            print "Failed {0} on 2nd Attempt".format(url)
            pass
    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)
        


#    import requests
#    r = requests.get(url)                    


#### Run ###

import os,sys

try:
    ponum = sys.argv[0]
    #ponum = '119071'
except:
    print "Enter a PO Number as 1st Arg or Nothing will Happen"

stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)


for k,v in stylesDict.iteritems():
    for val in v:
        vendor_url = 'http://admin.swisswatchintl.com/Z/'
        vendor_style = k + ".jpg"
        colorstyle = str(v[val]) + ".jpg"
        #vendor_stripped = k
        vendor_file = vendor_url + vendor_style

        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
        # 
        #print vendor_file, colorstyle_file
        #try:
        url_download_file(vendor_file,colorstyle_file)
            #os.rename(vendor_style, colorstyle_file)
            
            
        #    print "Renamed: " + vendor_file + " ---> " + colorstyle_file
        #except:
        #    vendor_file = vendor_file.split('-')[1:]
            #try:
            #    url_download_file(vendor_file,colorstyle_file)
            #except:
            #    print "TOTAL FAILURE: " + vendor_file + " ---> " + colorstyle_file
