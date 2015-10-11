# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 19:33:19 2013

@author: jb
"""



def sqlQueryConsigRename(oldfilevendor):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like 'oldfilevendor%';"
    
    result = connection.execute(querymake_consig_stylefix)
#    result = connection.execute(querymake)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['vend_name'] = row['VENDOR_STYLE_NO']
        consigstyle['bfly_name'] = row['COLORSTYLE']
        
        consigstyles[row['vend_name']] = consigstyle
        
    print consigstyles
    connection.close()
    return consigstyles
    
    
## 
#querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like '%oldfile%"'



#consig_rename_list = sqlQueryConsigRename(oldfilename)
    
def sqlQueryConsigRename(vnum,ponum):
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where pomgr_snp.production_snapshot.po_hdr = 'ponum' AND vendor_style_no like 'vnum%';"
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['bfly_name'] = row['COLORSTYLE']
        consigstyle['vend_name'] = row['VENDOR_STYLE_NO']
        consigstyles[row['bfly_name']] = consigstyle
        
    print consigstyles
    connection.close()
    return consigstyles


dir_conv = ('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion')

globtoconvert = glob.glob(os.path.join(dir_conv, '*/*.*'))
#for f in globtoconvert:
#    name = os.path.basename(f)
#    
#    poname = os.path.dirname(f)
#    
#    '{0},{1},{2}'.format(name,)    
#    print name, "=", poname
    
for f in globtoconvert:
    name = os.path.basename(f)
    vnumfile = os.path.splitext(name)
    pdirname = os.path.dirname(f)
    f = venfile
    vnum = vnumfile[0]
    ext = vnumfile[1]
    ponum = pdirname.split('/')[-1]
    bflyfile = sqlQueryConsigRename(vnum,ponum)
    


#querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like '%oldfile%"'




#select prdsnp.colorstyle, prdsnp.vendor_style_no from pomgr_snp.production_snapshot prdsnp where