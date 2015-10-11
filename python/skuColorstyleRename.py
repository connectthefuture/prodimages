#!/usr/bin/env python
"""
Created on Tue April 16 14:48:56 2013

@author: jb
"""
def sqlQuerySkuColorstyleConvert(sku):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    
    
    querymake_consig_stylefix="SELECT Distinct POMGR_SNP.SKU.PRODUCT_COLOR_ID AS colorstyle, POMGR_SNP.SKU.SKU_CODE AS sku FROM POMGR_SNP.SKU WHERE POMGR_SNP.SKU.SKU_CODE LIKE '" + sku + "' ORDER by POMGR_SNP.SKU.PRODUCT_COLOR_ID ASC"
    
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        consigstyles[row['sku']] = consigstyle
        
    #print consigstyles
    connection.close()
    return consigstyles
    
    
    
#sqlQueryConsigRename(vnum, ponum)[vnum]    

import sys
import os
import glob
import sqlalchemy
glbdir = sys.argv[1]   
#glbdir = '/Users/johnb/sss'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')
globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*.jpg'))
#print globtoconvert
for f in globtoconvert:
    
    #print globtoconvert
    try:
        name = os.path.basename(f)
        skunumfile = os.path.splitext(name)
        pdirname = os.path.dirname(f)
        sku = skunumfile[0]
        ext = skunumfile[1]
        #ponum = pdirname.split('/')[-1]
        altnum = sku.split('_')[-1]
        #altnum = '1'
        sku = sku.split('_')[0]
        bflyfile = sqlQuerySkuColorstyleConvert(sku)
        #print bflyfile
        for key,value in bflyfile.iteritems():
            style = str(value.values())            
            #for kv in value:
            #    style = value.values()
            print style            
            newname = os.path.join(pdirname, str(style) + "_" + altnum + ext)
                
            newname1 = newname.replace(sku, '')
            newname2 = newname1.replace('[', '')
            newname3 = newname2.replace(']_.', '.')
            newname4 = newname3.replace(']_', '_')
            finalnewname = newname4
            print finalnewname + '\t' + f
            os.rename(f, finalnewname)
            #print "HELPPLLLP"
            break
        
    
    except KeyError:
        continue
    except sqlalchemy.exc.DatabaseError:
        continue
        print "DBERR" + f
