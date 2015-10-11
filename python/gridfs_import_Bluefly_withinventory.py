#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sqlQuery_StyleWithInventory():
    import sqlalchemy,sys
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    query_marketplace_inprog ="""select
              distinct POMGR.PRODUCT_COLOR.id as COLORSTYLE,
              POMGR.INVENTORY.CURR_ON_HAND
            FROM
              POMGR.PRODUCT_COLOR
            INNER JOIN POMGR.SKU
            ON
              POMGR.SKU.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
            LEFT JOIN POMGR.INVENTORY
            ON
              POMGR.SKU.PRODUCT_COLOR_ID = POMGR.INVENTORY.PRODUCT_COLOR_ID
            WHERE
              POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT >= TRUNC(sysdate - 30)
            --AND SUBSTR(POMGR.SKU.SKU_CODE, 1, 1)          = '8'
            group by
            POMGR.PRODUCT_COLOR.id ,
              POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT,
              POMGR.SKU.SKU_CODE,
              POMGR.INVENTORY.TOTAL_ON_HAND,
              POMGR.INVENTORY.AVAL_ON_HAND,
              POMGR.INVENTORY.CURR_ON_HAND
            having POMGR.INVENTORY.AVAL_ON_HAND > 0 
            or POMGR.INVENTORY.TOTAL_ON_HAND > 0 
            or POMGR.INVENTORY.CURR_ON_HAND > 0
            order by
              colorstyle DESC"""

    ## WHERE POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    ## AND POMGR.PRODUCT_COLOR.COPY_READY_DT IS NOT NULL
    ##
    
    result = connection.execute(query_marketplace_inprog)
    styles = {}
    filepaths = []
    for row in result:
        styledata = {}           
        styledata['colorstyle'] = row['colorstyle']
        fname = str(row['colorstyle']) + '.png'
        filepath = os.path.join('/mnt/netsrv101.l3.bluefly.com', fname[:4], fname)
        #consigstyle['vendor_style'] = row['vendor_style']
        filepaths.append(filepath)
        #styles[style_alt] = styledata
        
    #print consigstyles
    connection.close()
    return filepaths

## Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os,re
    regex_bflyfile = re.compile(r'^(.*?/?)?.*?([0-9]{9})((_[1-7xX])|(_alt0[1-6]))?(\.[jpngJPNG]{3,4})?$')
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path) and regex_bflyfile.findall(file_path):
                walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)#['XMP:DateCreated'][:10].replace(':','-')
    return metadata


## Returns False if file is Zero KB, True if file is valid - does not catch corrupt files greater than 1KB
def zero_byte_file_filter(image_filepath,error_dir=None):
    import os, shutil
    if not error_dir:
        imagedir  = os.path.dirname(image_filepath)
        rootdir   = os.path.dirname(imagedir)
        error_root = os.path.join(rootdir,'zero_byte_errors')
        error_details_drop_dir = os.path.join(error_root, 'originated_in_' + imagedir.split('/')[-1])
    mdata = get_exif_all_data(os.path.abspath(image_filepath))
    if mdata.get('File:FileSize') <= 1:
        try:
            os.makedirs(error_details_drop_dir, 16877)
        except:
            pass
        error_file_stored = os.path.join(error_details_drop_dir, os.path.basename(image_filepath))
        if os.path.isfile(error_file_stored):
            os.remove(error_file_stored)
            shutil.move(image_filepath, error_file_stored)
        else:
            shutil.move(image_filepath, error_file_stored)
        return False
    else:
        return True


def getparse_metadata_from_imagefile(image_filepath):
    import os, re
    from collections import defaultdict
    image_filepath = os.path.abspath(image_filepath)
    mdata = get_exif_all_data(image_filepath)
    mdatainsert = {} #defaultdict(list)
    groupdict = defaultdict(list)
    for k,v in mdata.iteritems():
        try:
            mgroup, mtag = k.split(':')
            mvalue = v
            metakvpairs = {mtag: mvalue}
            groupdict[mgroup].append(metakvpairs)
            #print mgroup, mtag, mvalue, '----_----', metagroupdict, '----\n----',groupdict
            #metagroupdict[mgroup].append(metatagval)
        except ValueError:
            pass
    #print groupdict  datagroupkey, datagroupvalues = groupdict.popitem()
    mdatainsert[image_filepath] = groupdict #.items()
    return mdatainsert

def insert_gridfs_extract_metadata(image_filepath):    
    from mongo_gridfs_insert_file import insert_file_gridfs_file7
    import os,sys
    try:
        db_name = sys.argv[2]
    except IndexError:
        db_name='gridfs_bfly'
    metadata = getparse_metadata_from_imagefile(image_filepath).items()[0][1]
    print image_filepath, metadata
    insert_record = insert_file_gridfs_file7(filepath=image_filepath, metadata=metadata, db_name=db_name)
    return #insert_record


def update_gridfs_extract_metadata(image_filepath):    
    from mongo_gridfs_insert_file import update_file_gridfs_file7
    import os,sys
    try:
         db_name = sys.argv[2]
    except IndexError:
        db_name='gridfs_file7'
    metadata = getparse_metadata_from_imagefile(image_filepath).items()[0][1]
    print image_filepath, metadata
    insert_record = insert_file_gridfs_file7(filepath=image_filepath, metadata=metadata, db_name=db_name)
    return #insert_record

if __name__ == '__main__':
    import sys,os
    try:
        #directory = sys.argv[1]
        dirfileslist = sqlQuery_StyleWithInventory() #recursive_dirlist(directory)
        for f in dirfileslist:
            insert_gridfs_extract_metadata(f)
        #print dirfileslist
    except IndexError:
        print 'FAILED INDEX ERROR'
        pass


