#!/usr/bin/env python

# #!/bin/bash
# 
# . ~/.bash_profile
# . ~/.bashrc
# 
# DATE=`date "+%Y-%m-%d"`
# DAY=`date "+%Y-%m-%d-RetouchToDo"`
# 
# searchDir="$1"
# 
# stylePath=`find $searchDir -iname \*[^2-9][0-9,{8}]_[1-6].\*`
# 
# for f in $stylePath:
# do
# style=`basename $f | awk -F_ '{ print $1 }'`
# paired=`echo "$style,$f"`
# 
# echo $paired >> $LIMBO/$DATE_tagpairs.csv
# 
# done


"""
Created on Fri Mar  8 14:48:56 2013

@author: jb
"""
def sqlQueryMetatags(style,f):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_metatags="""SELECT DISTINCT
      POMGR_SNP.PRODUCT_COLOR.ID                  AS colorstyle,
      POMGR_SNP.BRAND.NAME                        AS brand,
      POMGR_SNP.COLOR_GROUP.DESCRIPTION           AS color_group,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL AS category_parent,
      POMGR_SNP.PRODUCT_FOLDER.LABEL              AS category_sub,
      MAX(ATG_SNP.EVENT.ID)                       AS event_id,
      ATG_SNP.EVENT.EVENT_DESCRIPTION             AS event_title,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.PATH  AS product_path,
      ATG_SNP.EVENT.SHOT_LIST_DATE                AS shot_list_dt,
      ATG_SNP.EVENT.BRAND_EDITORIAL               AS brand_editorial,
      ATG_SNP.EVENT.CATEGORY                      AS cat_id,
      POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE        AS vendor_style,
      POMGR_SNP.LK_PRODUCT_STATUS.NAME            AS production_status
    FROM
      POMGR_SNP.PRODUCT_COLOR
    LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR
    ON
      POMGR_SNP.PRODUCT_COLOR.ID = ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID
    LEFT JOIN POMGR_SNP.LK_PRODUCT_STATUS
    ON
      POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID
    LEFT JOIN ATG_SNP.EVENT
    ON
      ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID
    LEFT JOIN POMGR_SNP.PRODUCT
    ON
      POMGR_SNP.PRODUCT_COLOR.PRODUCT_ID = POMGR_SNP.PRODUCT.ID
    LEFT JOIN POMGR_SNP.PRODUCT_FOLDER
    ON
      POMGR_SNP.PRODUCT.PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER.ID
    LEFT JOIN POMGR_SNP.BRAND
    ON
      POMGR_SNP.PRODUCT.BRAND_ID = POMGR_SNP.BRAND.ID
    LEFT JOIN POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED
    ON
      POMGR_SNP.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID =
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.ID
    LEFT JOIN POMGR_SNP.COLOR_GROUP
    ON
      POMGR_SNP.PRODUCT_COLOR.COLOR_GROUP_ID = POMGR_SNP.COLOR_GROUP.ID
    WHERE
      POMGR_SNP.PRODUCT_COLOR.ID = COLORSTYLESEARCH
    GROUP BY
      POMGR_SNP.PRODUCT_COLOR.ID,
      POMGR_SNP.BRAND.NAME,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL,
      POMGR_SNP.PRODUCT_FOLDER.LABEL,
      ATG_SNP.EVENT.EVENT_DESCRIPTION,
      POMGR_SNP.COLOR_GROUP.DESCRIPTION,
      POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.PATH,
      POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE,
      ATG_SNP.EVENT.SHOT_LIST_DATE,
      ATG_SNP.EVENT.BRAND_EDITORIAL,
      ATG_SNP.EVENT.CATEGORY,
      POMGR_SNP.LK_PRODUCT_STATUS.NAME
    ORDER BY
      POMGR_SNP.PRODUCT_COLOR.ID DESC"""

##   --POMGR_SNP.PRODUCT_COLOR.MODIFIED_DATE >= TRUNC(SysDate - 365)

##   --RENAME INPUT VARIABLE PRIOR TO QUERY
    querymake_metatags = querymake_metatags.replace('COLORSTYLESEARCH', str(style))
    result = connection.execute(querymake_metatags)
    

    metatags = {}
    for row in result:
        metatag = {}
#        metatag['colorstyle'] = row['colorstyle']
#        metatag['IPTC:PONumber'] = row['po_num']
        #metatag['IPTC:VendorStyle'] = row['vendor_style']
        metatag['Xmp.xmpDM.artist'] = row['vendor_style']
        #metatag['IPTC:Brand'] = row['brand']
        metatag['Xmp.xmpDM.genre'] = row['color_group']
        #metatag['IPTC:ProductType'] = row['category_sub']
        metatag['Iptc.Application2.Source'] = row['category_sub']
        #metatag['EventID'] = row['event_id']
        try:
            metatag['Xmp.xmpDM.album'] = "EventID " + str(row['event_id'])
        except:
            pass
        metatag['Iptc.Application2.Credit'] = row['product_path']
        metatag['Iptc.Application2.Copyright'] = row['brand']
        metatag['Iptc.Application2.SpecialInstructions'] = row['production_status']
        metatag['Iptc.Application2.Keywords'] = row['category_parent']
        #metatag['Iptc.Application2.Source'] = row['shot_list_dt']
#        metatag['IPTC:SpecialInstructions'] = '{:%Y-%m-%d}'.format(metatag['brand_editorial'])
#        metatag['IPTC:SampleStatusDate'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:Source'] = '{:%Y-%m-%d}'.format(row['sample_dt'])
#        metatag['IPTC:Source'] = row['sample_dt']
#        metatag['SourceFile'] = f
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag

    connection.close()
    return metatags
    
    
def embed_exif_metadata(image_filepath, exiftag=None, exifvalue=None):
    import pyexiv2, os
    # Read EXIF data to initialize
    image_metadata = pyexiv2.ImageMetadata(image_filepath)
    image_metadata.read()
    # Add and Write new Tag to File
    image_metadata.modified = True
    image_metadata.writable = os.access(image_filepath, os.W_OK)
    image_metadata[exiftag] = [exifvalue]
    #image_metadata[exiftag] = pyexiv2.ExifTag(exiftag, exifvalue)
    
    print image_metadata[exiftag], image_metadata
    image_metadata.write()
    return image_filepath    

def get_exif_all_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_filepath)
        #['XMP:DateCreated'][:10].replace(':','-')
    return metadata
        

##############################
import sys
import os
import glob
import sqlalchemy
glbdir = sys.argv[1]
#glbdir='/mnt/Post_Ready/aPhotoPush'
#glbdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117257'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')
globtoconvert = glob.glob(os.path.join(os.path.abspath(glbdir), '*.??g'))
#print globtoconvert
import pyexiv2

for f in globtoconvert:
    stylefile = os.path.basename(f)
    try:
        style = stylefile.split('_')[0]
        if style.isdigit():
            pass
        else:
            style = stylefile.split('.')[0][:9]
    except:
        print "Error --> {}".format(f)
        pass
    #print style, f
    ### string = key/val as k=filepath, val=all metadata as k/v pairs
    exiftoolstring = sqlQueryMetatags(style,f)
    
    
    for key,values in exiftoolstring.iteritems():
        #full = str(value.values())
        for tag in values:
            image_filepath = f
            exiftag        = tag
            exifvalue      = values[tag]
            print values
            print image_filepath, exiftag, exifvalue
            try:
                embed_exif_metadata(image_filepath, exiftag=exiftag, exifvalue=exifvalue)
                print "Success Embedded {0} = {1} --> {2}".format(exiftag, exifvalue, image_filepath)
            except pyexiv2.xmp.XmpValueError:
                print "XMP ValueError {0}-{1}".format(exiftag, exifvalue, image_filepath)
                pass    
            except IndexError:
                print "Index ERROR WHILE EMBEDDING {0} = {1} --> {2}".format(exiftag, exifvalue, image_filepath)
            except IOError:
                print "Key ERROR WHILE EMBEDDING {0} = {1} --> {2}".format(exiftag, exifvalue, image_filepath)
            