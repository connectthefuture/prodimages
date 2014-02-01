#!/usr/bin/env python

def sqlQuery_GetStyleVendor_ByPO(ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
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
    
    else:
        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)
        


#    import requests
#    r = requests.get(url)                    


#### Run ###

import os,sys

#try:
#    ponum = sys.argv[1]
#    #ponum = '119071'
#except:
#    print "Enter a PO Number as 1st Arg or Nothing will Happen"
import csv
file = '/mnt/Post_Ready/Retouchers/JohnBragato/SQLDeveloper_Exports/swisswatchstyles.csv'

polist = []
with open(file, 'rbU') as f:
    reader = csv.reader(f, dialect=csv)    
    for ponumber in reader:
        polist.append(ponumber[1])
    
polist = set(polist)

stylesDictsDict = []
for ponum in polist:
    try:
        
        stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)
        stylesDictsDict.append(stylesDict)
    except:
        pass


for stylesDict in stylesDictsDict:
    for k,v in stylesDict.iteritems():
            
        vendor_url = "http://admin.swisswatchintl.com/Z/{0}.jpg".format(k)
        vendor_url_back = vendor_url.replace('.jpg', '-back.jpg')
        vendor_url_side = vendor_url.replace('.jpg', '-side.jpg')
        
        style = str(v['colorstyle'])
        colorstyle =  style + "_1.jpg"
        colorstyle_side = style  + "_2.jpg"
        colorstyle_back = style  + "_3.jpg"
        
        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
        colorstyle_back_file = os.path.join(os.path.abspath(os.curdir), colorstyle_back)
        colorstyle_side_file = os.path.join(os.path.abspath(os.curdir), colorstyle_side)
        #imagefalse = sqlQuery_GetStyleVendor_ByPO()
        #if imagefalse:
#        try:            
#        #print imagefalse,vendor_url, colorstyle_file
#            url_download_file(vendor_url,colorstyle_file)
#        except:
#            print "Failed {}{}".format(vendor_url,colorstyle_file)
#            #print swiurl
        try:            
        #print imagefalse,vendor_url, colorstyle_file
            url_download_file(vendor_url_back,colorstyle_back_file)
        except:
            print "Failed {}{}".format(vendor_url,colorstyle_back_file)


        try:            
        #print imagefalse,vendor_url, colorstyle_file
            url_download_file(vendor_url_side,colorstyle_side_file)
        except:
            print "Failed {}{}".format(vendor_url,colorstyle_side_file)

#
#for stylesDict in stylesDictsDict:
#    for k,v in stylesDict.iteritems():
#        for val in v:
#            vendor_url = 'http://admin.swisswatchintl.com/Z/'
#            vendor_style = k + ".jpg"
#            colorstyle = str(v[val]) + ".jpg"
#            #vendor_stripped = k
#            vendor_file = vendor_url + vendor_style
#
#            colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
#            # 
#            #print vendor_file, colorstyle_file
#            #try:
#            url_download_file(vendor_file,colorstyle_file)
#                #os.rename(vendor_style, colorstyle_file)
                
            
        #    print "Renamed: " + vendor_file + " ---> " + colorstyle_file
        #except:
        #    vendor_file = vendor_file.split('-')[1:]
            #try:
            #    url_download_file(vendor_file,colorstyle_file)
            #except:
            #    print "TOTAL FAILURE: " + vendor_file + " ---> " + colorstyle_file
