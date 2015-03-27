#!/usr/bin/env python
import os, sys, re, csv


def sqlQuery_GetStyleVendor_ByPO(ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    #orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
    # AND POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE like '%vendornum%'"

    result = connection.execute(querymake_StylesByPO)
    styles = {}
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
                        
                     
def url_download_file(url,filepath):
    import urllib
    #error_check = urllib.urlopen(url)
    #urlcode_value = error_check.getcode()
    #print urlcode_value
    
    #if urlcode_value == 200:
    urllib.urlretrieve(url, filepath)
    print "Retrieved: " + url + " ---> " + filepath
    #    return urlcode_value
    #elif urlcode_value == 404:
    #    return urlcode_value
        
        
#        url_split = url.split('/')[-1]
#        url_split = url_split.split('-')[1:]
#        url_split = '-'.join(url_split)       
#        url_parent = url.split('/')[:-1]
#        url_parent = '/'.join(url_parent)
        
#        try:
#            url = os.path.join(url_parent, url_split)
#            error_check = urllib.urlopen(url)
#            urlcode_value = error_check.getcode()
#            #print urlcode_value
#            
#            if urlcode_value == 200:
#                urllib.urlretrieve(url, filepath)
#                print "On 2nd Attempt, Retrieved: " + url + " ---> " + filepath
#
#            elif urlcode_value == 404: 
#                print "Failed Downloading URL {0} on 2nd Attempt with Error Code {1}".format(url, urlcode_value)
#            
#            else:
#                print "Totally Failed Downloading URL {0} on 2nd Attempt with Error Code {1}".format(url, urlcode_value)
#        
#        except:
#            print "Failed {0} on 2nd Attempt".format(url)
#    
#    else:
#        print "{0} Error:\v {1} is not a valid URL".format(urlcode_value,url)
        


#    import requests
#    r = requests.get(url)                    


#### Run ###

import os,sys, urllib

args = sys.argv[1:]

regex_r = re.compile(r'.*?\r.*?')
regex_n = re.compile(r'.*?\n.*?')



args1 = args[0].split('\n')   #(','.join(str(arg) for arg in args)).split('\n')
#args2 = args1.split('\n')
#if re.findall(regex_r, args):
#    print "REEEEEE"
#    args_split = [ arg.split('\r') for arg in args ][0]
#
#if re.findall(regex_n, args):
#re.findall(regex_n, args)    

#args_split = [ arg.replace('\n',' ') for arg in args ]
#    print "NNNNEEEEEE"
        



#args_split = [ arg.split('\n') for arg in args ][0]
 #.split('r')[1:]
#args = args[:]
#args.split('\n')[:]
#spl = str(args[:]).split('\n')

try:
    if len(args1) >= 2:
        styleslist = args1
        print "HELLO Greater 2"
        print len(styleslist)
        
    elif len(args1) == 1:
        ponum = args[0] #sys.argv[1]#ys.argv[1]#args_split #sys.argv[1]
        print ponum
        styleslist = sqlQuery_GetStyleVendor_ByPO(ponum)
        #print stylesDict
#        #ponum = '119071'
except OSError:
    print "Enter at least PO Number as 1st Arg or Nothing will Happen"
#
#if ponum:
#    stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)
#
#
#print len(args1)
#stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)
#
#if type(styles) == 'dict':



#for k,v in styles.iteritems():
for style in styleslist:

    netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
    colorstyle = str(style)
    ext_PNG     = '.png'
    ext_JPG     = '.jpg'

    #colorstyle = str(v[val]) + ".jpg"
    #vendor_stripped = k
    netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext_PNG)
#try:
    #error_check = urllib.urlopen(netsrv101_url_file)
    #urlcode_value = error_check.getcode()
    #print urlcode_value
    #try: #if urlcode_value == 200:
    colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle + ext_PNG)
    try:
        url_download_file(netsrv101_url_file, colorstyle_file)
    
        alt = 0   
        for x in range(1,6):
            try:
                alt = x   
                ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
                colorstylealt = colorstyle + ext_ALT
                colorstyle_filealt = os.path.join(os.path.abspath(os.curdir), colorstylealt)
                
                netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)
                
                #error_check = urllib.urlopen(netsrv101_url_filealt)
                #urlcode_value = error_check.getcode()
                #if urlcode_value == 200:
                if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                    url_download_file(netsrv101_url_filealt, colorstyle_filealt)
            except IOError:
                pass        
    except IOError:
        pass   
#    print netsrv101_url_filealt
#print netsrv101_url_file

            
        #, colorstyle_file
        # 
        #print vendor_file, colorstyle_file
        #try:
    #url_download_file(netsrv101_url_file,colorstyle_file)
            #os.rename(vendor_style, colorstyle_file)
            #    print "Renamed: " + vendor_file + " ---> " + colorstyle_file
    #except:
    #    vendor_file = vendor_file.split('-')[1:]
        #try:
        #    url_download_file(vendor_file,colorstyle_file)
        #except:
        #    print "TOTAL FAILURE: " + vendor_file + " ---> " + colorstyle_file
        
