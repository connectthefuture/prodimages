#!/usr/bin/env python

def sqlQuery_GetStyleVendor_ByPO(ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_StylesByPO="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
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
                        
                     
                    
                    
#### Run ###

import os,sys

try:
    ponum = sys.argv[1]
except:
    print "Enter a PO Number as 1st Arg or Nothing will Happen"

stylesDict = sqlQuery_GetStyleVendor_ByPO(ponum)


for k,v in stylesDict.iteritems():
    for val in v:
        vendor_url = 'http://admin.swisswatchintl.com/Z'
        vendor_style = k + ".jpg"
        colorstyle = str(v[val]) + ".jpg"
        vendor_file = vendor_url + "/" + vendor_style
        colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle)
        # 
        print vendor_file, colorstyle_file
        try:
            os.rename(vendor_file, colorstyle_file)
            print "Renamed: " + vendor_file + " ---> " + colorstyle_file
        except:
            print "Failed: " + vendor_file + " ---> " + colorstyle_file