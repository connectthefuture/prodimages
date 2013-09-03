## -*- coding: utf-8 -*-
#"""
#Created on Thu Mar  7 19:33:19 2013
#
#@author: jb
#"""
#
#
#
#def sqlQueryConsigRename(oldfilevendor):
#    import sqlalchemy
#    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
#    connection = orcl_engine.connect()
#    querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like 'oldfilevendor%';"
#    
#    result = connection.execute(querymake_consig_stylefix)
##    result = connection.execute(querymake)
#    consigstyles = {}
#    for row in result:
#        consigstyle = {}        
#        consigstyle['vend_name'] = row['VENDOR_STYLE_NO']
#        consigstyle['bfly_name'] = row['COLORSTYLE']
#        
#        consigstyles[row['vend_name']] = consigstyle
#        
#    print consigstyles
#    connection.close()
#    return consigstyles
#    
#    
### 
##querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like '%oldfile%"'
#
#

consig_rename_list = sqlQueryConsigRename(oldfilename)
    
def sqlQueryConsigRename(oldfilevendor):
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like 'oldfilevendor%';"
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['vend_name'] = row['VENDOR_STYLE_NO']
        consigstyle['bfly_name'] = row['COLORSTYLE']
        
        consigstyles[row['vend_name']] = consigstyle
        
    print consigstyles
    connection.close()
    return consigstyles


dir_conv = ('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion')

globtoconvert = glob.glob(os.path.join(dir_conv, '*/*.*'))
for f in globtoconvert:
    name = os.path.basename(f)
    
    ponum = os.path.dirname(f)
    
    '{0},{1},{2}'.format(name,newname,ponum)    
    print name, "=", poname
    

    


#querymake_consig_stylefix="select pomgr_snp.production_snapshot.colorstyle, pomgr_snp.production_snapshot.vendor_style_no from pomgr_snp.production_snapshot where vendor_style_no like '%oldfile%"'




#select prdsnp.colorstyle, prdsnp.vendor_style_no from pomgr_snp.production_snapshot prdsnp where