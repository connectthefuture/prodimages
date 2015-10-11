
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:48:56 2013

@author: jb
"""
def sqlQueryConsigRename(vnum, ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    
    
    querymake_consig_stylefix="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE LIKE '" + vnum + "%' AND POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['COLORSTYLE'] = row['COLORSTYLE']
        #consigstyle['VENDOR_STYLE'] = row['VENDOR_STYLE']
        consigstyles[row['VENDOR_STYLE']] = consigstyle
        
    #print consigstyles
    connection.close()
    return consigstyles
    
    
    
#sqlQueryConsigRename(vnum, ponum)[vnum]    

import sys
import os
import glob
import sqlalchemy
#glbdir = sys.argv[1]   
glbdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117131'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')
globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*.jpg'))
#print globtoconvert
for f in globtoconvert:
    
    #print globtoconvert
    try:
        name = os.path.basename(f)
        vnumfile = os.path.splitext(name)
        pdirname = os.path.dirname(f)
        vnum = vnumfile[0]
        ext = vnumfile[1]
        ponum = pdirname.split('/')[-1]
        altnum = vnum.split('_')[-1]
        vnum = vnum.split('_')[0]
        bflyfile = sqlQueryConsigRename(vnum, ponum)
        #print bflyfile
        for key,value in bflyfile.iteritems():
            style = str(value.values())            
            #for kv in value:
            #    style = value.values()
            #print style            
            newname = os.path.join(pdirname, str(style) + "_" + altnum + ext)
                
            newname1 = newname.replace(vnum, '')
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
