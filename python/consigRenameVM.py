#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 01:20:40 2013

author: jb
"""

def sqlQueryConsigRename(vnum, ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    
#    querymake_consig_stylefix="select pomgr_snp.product_snapshot.colorstyle, pomgr_snp.product_snapshot.vendor_style_no from pomgr_snp.product_snapshot where pomgr_snp.product_snapshot.po_hdr = ponum AND vendor_style_no = vnum"    
# /mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/116912/AMH8500E.jpg
    
    #ponum = '116912'
    #vnum = 'AMH8500E'
    
    #querymake_consig_stylefix="select pomgr_snp.product_snapshot.colorstyle, pomgr_snp.product_snapshot.vendor_style_no from pomgr_snp.product_snapshot where pomgr_snp.product_snapshot.po_hdr = ponum AND vendor_style_no = vnum"    
    
    querymake_consig_stylefix="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE LIKE '" + vnum + "%' AND POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
    result = connection.execute(querymake_consig_stylefix)
    #print querymake_consig_stylefix 
    #print result 
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['bfly_name'] = row['COLORSTYLE']
        consigstyle['vend_name'] = row['VENDOR_STYLE']
        consigstyles[row['VENDOR_STYLE']] = consigstyle
        
    #print consigstyles
    connection.close()
    return consigstyles
    #return consigstyle['bfly_name']


######## RUN
import os,sys,re,glob

#dir_conv = ('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion')
dir_conv = ('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147')

globtoconvert = glob.glob(os.path.join(dir_conv, '*.jpg'))
#for f in globtoconvert:
#    name = os.path.basename(f)
#    
#    poname = os.path.dirname(f)
#    
#    '{0},{1},{2}'.format(name,)    
#    print name, "=", poname
    
for f in globtoconvert:
    try:
        name = os.path.basename(f)
        vnumfile = os.path.splitext(name)
        pdirname = os.path.dirname(f)
        print "HELPPLLLP"
        vnum = vnumfile[0]
        ext = vnumfile[1]
        ponum = pdirname.split('/')[-1]
        altnum = vnum.split('_')[-1]
        vnum = vnum.split('_')[0]
        bflyfile = sqlQueryConsigRename(vnum, ponum)[1]
#        for fn in bflyfile.iteritems():
#            bflystyle = f[0]
#            #print f[0]
#            newname = os.path.join(pdirname, bflystyle + "_" + altnum + ext)
#            print newname
        print "HELPPLLLP" + newname
        #break
        
    except KeyError:
        
        continue
        print "BadKey Request - " + f
    #finally:
    #    print "done"        
    except sqlalchemy.exc.DatabaseError:
        continue
  #      print "DBERR" + f
        
