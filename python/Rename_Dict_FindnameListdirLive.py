#!/usr/bin/env python
#from pythonstartup import *

def sqlQueryConsigRename(vnum, ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()    
    #$chiprint connection
    querymake_consig_stylefix="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.VENDOR_STYLE LIKE '" + vnum + "%' AND POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        consigstyles[row['vendor_style']] = consigstyle
        
    #print consigstyles
    connection.close()
    return consigstyles


def vendor_styles_from_filename(directory):
    sorted_dir_list = sorted(os.listdir(directory))
    #vendor_styles = []
    if sorted_dir_list:
            vendor_styles = []
            for line in sorted_dir_list:
                vendorstyle = '_'.join(line.split("_")[:-1])
                vendor_styles.append(vendorstyle)
                sorted(vendor_styles)
    return sorted(vendor_styles)


def keyvalue_dict_rename(keyvalue_dictlist,directory):
    renaming_basedir = directory
    sorted_dir_list = sorted(os.listdir(renaming_basedir))
    for alldicts in keyvalue_dictlist:
        for k,v in alldicts.iteritems():
            oldname = k
            oldpath = os.path.join(renaming_basedir,oldname)
            newname = v['colorstyle']
            newname = str(newname)
            newpath = os.path.join(renaming_basedir,newname)
            print sorted_dir_list
            for f in sorted_dir_list:
                vendnum = '_'.join(f.split("_")[:-1])
                extold = f.split("_")[-1]
                extnew = extold.lower()
                if oldname == vendnum:
                    oldfile = oldpath + "_" + extold
                    newfile = newpath + "_" + extnew
                    try:
                        #os.rename(oldfile,newfile)
                        print "Renamed: " + oldfile + " ---> " + newfile
                    except:
                        print "Failed: " + oldfile + " ---> " + newfile

## Execute Query Return K/V dict
def run_SQL_Query(vendor_styles_list,directory):
    import sqlalchemy
    ponum = directory.split('/')[-1]
    returnlist = []

        
    for vendor_style in vendor_styles_list:
            try:     
                result = sqlQueryConsigRename(vendor_style, ponum)
                returnlist.append(result)
    
            #except sqlalchemy.exc.DatabaseError:
            except OSError:
                print "Error on Vendor Style {0}".format(vendor_style)
                pass
    
    return returnlist
    
############################################    RUN  #################


import os,sys

try:
    directory = os.path.abspath(sys.argv[1])
    ponum = directory.split('/')[-1]
except IndexError:
    #directory = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/11789e4'
    #ponum = directory.split('/')[-1]
    print "Directory Arg Not Supplied"
    
    #break

## Get vendor style name from listing input Directory
vendor_styles_list = vendor_styles_from_filename(directory)

## Query Oracle DSSPRD1 using vendor_styles_list and directory where files reside Returning Vendorstyle as key and colorstyle as Value 
vendor_style_bfly_dictlist = run_SQL_Query(vendor_styles_list,directory)

#print vendor_styles_list
#### Using Dict of Vend/Colorstyles listdir loop through directory for match between filesnames and vendorstyles and rename as bfly colorstyle
keyvalue_dict_rename(vendor_style_bfly_dictlist,directory)

#print vendor_style_bfly_dictlist


