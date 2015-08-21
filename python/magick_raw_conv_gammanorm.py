#!/usr/bin/env python

"""
Created on Fri Jun 28 14:48:56 2013

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
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        metatag['IPTC:Brand'] = row['brand']
        metatag['XMP:Genre'] = row['color_group']
        metatag['IPTC:ProductType'] = row['category_sub']
        metatag['EventID'] = row['event_id']
        try:
            metatag['XMP:Album'] = "EventID " + str(row['event_id'])
        except:
            pass
        metatag['IPTC:Credit'] = row['product_path']
        metatag['IPTC:CopyrightNotice'] = row['brand']
        metatag['IPTC:SpecialInstructions'] = row['production_status']
        metatag['Keywords'] = row['category_parent']
        metatag['IPTC:Source'] = row['shot_list_dt']
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


def get_dbinfo_for_metatags_singlefile(f):
    import os
    metafield_dict = {}
    listed = []
    stylefile = os.path.basename(f)
    style = stylefile.split('_')[0]
    #print style, f
    ### string = key/val as k=filepath, val=all metadata as k/v pairs
    exiftoolstring = sqlQueryMetatags(style,f)
    #pairs = zip(exiftoolstring.values(), exiftoolstring.keys())

    for k,v in exiftoolstring.iteritems():
        tmpd = {}
        for val in v:
            tmpd[val] = v[val]
            listed.append(tmpd)
        metafield_dict[k] = tmpd

    return metafield_dict
    #return listed

def embed_exif_metadata(image_filepath, exiftag=None, exifvalue=None):
    from PIL import Image
    import pyexiv2
    # Read EXIF data to initialize
    image_metadata = pyexiv2.ImageMetadata(image_filepath)
    image_metadata.read()
    # Add and Write new Tag to File
    image_metadata[exiftag] = exifvalue
    image_metadata.write()
    return image_filepath


def get_exif_metadata_value(image_filepath, exiftag=None, exifvalue=None):
    from PIL import Image
    import pyexiv2
    if exifvalue:
        pass
    else:
        
        # Read EXIF data to initialize
        image_metadata = pyexiv2.ImageMetadata(image_filepath)
        metadata = image_metadata.read()
        # Add and Write new Tag to File
        exifvalue = metadata[exiftag]
        # image_metadata[exiftag] = exifvalue
        # image_metadata.write()
#    else:
#        print "Not Yet Built"
    return image_filepath


def write_metadata_file(filename):
    import sys
    import os
    import glob
    import sqlalchemy


    metadict = get_dbinfo_for_metatags_singlefile(filename)
    exiftags = []
    exifdict = {}
    for k,v in metadict.items():
        metatags = []

        for val in v:
            #m = []
            filename = str(k)
            exiftag = val
            exifvalue = v[val]
            #exifpart = str(' -' + "'" + str(exiftag) + "=" + str(exifvalue) + "'" + ''),
            exifpart = "-'{exiftag}'='{exifvalue}'".format(exiftag=exiftag,exifvalue=exifvalue)
            metatags.append(exifpart)
            #print metatags
            #m.append(exifpart)
            #print val,v[val]
        #exifdict[filename] = [x for x in metatags]
        #metatags = (str(tag) for tag in metatags)
        exifdict[filename] = " ".join(metatags)

        execlist = []
        for key,value in exifdict.iteritems():
            execstring = "exiftool -m -overwrite_original_in_place -fast2 -q {0} {1}".format(value,key)
            execlist.append(execstring)

        for line in execlist:
            try:
                os.system(line)
                print line
            except:
                pass

def recursive_dirlist(rootdir):
    import os, re
    regex_raw = re.compile(r'.+?.CR2$')
    regex_jpg = re.compile(r'.+?.jpg$')
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                if re.findall(regex_raw, file_path):
                    walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


### Identify the FocalLength
def subproc_identify_focallength(filepath):
    import subprocess, os, re, sys
    focallength = subprocess.call([
    "identify",
    "-format",
    '%[EXIF:FocalLength]',
    filepath,
    ])
    print 
    return str(focallength)


### Better Gamma Output    
def subproc_convert_rawtojpgshort(filepath):
    import subprocess, os, re, sys
    dngcmd = str("dng:" + filepath)
    outfile = filepath.replace('.CR2','.jpg')
    
    
    subprocess.call([
    "convert",
    "-define",
    'dng:size=3744x',
    dngcmd,
    "-depth", 
    "16",
    "-density",
    "350x350",
    "-profile", 
    "/usr/local/color_profiles/AdobeRGB1998.icc",
    "-colorspace",
    "LAB",
    "-filter",
    "LanczosSharp",
    "-distort",
    'Barrel', 
    "0.0 0.0 -0.025",
##    "-level",
##    "0%,100%,1.5",
    "-colorspace",
    'sRGB',
    "-channel",
    "RGBA",
    "-gamma",
    "1.8/1.4/1.6",
    "-normalize",
    "-auto-level",
    "-unsharp", 
    "0x0.75+0.75+0.008",
    outfile,
    ])
    return outfile


##################### Begin CMDS ##############

import sys
import os
import glob
import sqlalchemy

if sys.argv[1]:
    rootdir = sys.argv[1]
else:
    rootdir = '.'

raw_to_convert = recursive_dirlist(rootdir)

for filename in raw_to_convert:
    try:
        subproc_convert_rawtojpgshort(filename)
    except:
        print "Failed to Convert {}".format(filename)
        
