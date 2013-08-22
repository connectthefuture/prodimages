#!/usr/bin/env python

def event_styles_by_categoryid(categoryid):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    
    if len(categoryid) != 4:
        ### Run Query using Category ID found at end of BC list pages
        querymake_event_styles_by_categoryid="SELECT Distinct POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS colorstyle, POMGR.EVENT.CATEGORY AS category, POMGR.EVENT_PRODUCT_COLOR.EVENT_ID AS event_id FROM POMGR.EVENT INNER JOIN POMGR.EVENT_PRODUCT_COLOR ON POMGR.EVENT.ID = POMGR.EVENT_PRODUCT_COLOR.EVENT_ID WHERE POMGR.EVENT.CATEGORY like '%" + categoryid + "'"
    elif len(categoryid) == 4:
        ### If 4 digit Event ID is given, Query using Event ID instead of Cat id
        eventid = categoryid
        querymake_event_styles_by_categoryid="SELECT Distinct POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS colorstyle, POMGR.EVENT.CATEGORY AS category, POMGR.EVENT_PRODUCT_COLOR.EVENT_ID AS event_id FROM POMGR.EVENT INNER JOIN POMGR.EVENT_PRODUCT_COLOR ON POMGR.EVENT.ID = POMGR.EVENT_PRODUCT_COLOR.EVENT_ID WHERE POMGR.EVENT_PRODUCT_COLOR.EVENT_ID = '" + eventid + "'"
        
    result = connection.execute(querymake_event_styles_by_categoryid)
    styles = {}
    for row in result:
        style = {}        
        style['event_id'] = row['event_id']
        style['category'] = row['category']
        styles[row['colorstyle']] = style
    connection.close()
    return styles

## Path to file below is from the mountpoint on FTP, ie /mnt/images..
## Download via FTP
def getbinary_ftp_netsrv101(remote_pathtofile, outfile=None):
    # fetch a binary file
    import ftplib
    ftpdown = ftplib.FTP("netsrv101.l3.bluefly.com")
    ftpdown.login("imagedrop", "imagedrop0")
    if outfile is None:
        outfile = sys.stdout
    destfile = open(outfile, "wb")
    ftpdown.retrbinary("RETR " + remote_pathtofile, destfile.write, 8*1024)
    destfile.close()

## Upload to imagedrop via FTP
def upload_to_imagedrop(file):
    import ftplib
    session = ftplib.FTP('file3.bluefly.corp', 'imagedrop', 'imagedrop0')
    fileread = open(file,'rb')
    filename = str(file.split('/')[-1])
    session.cwd("ImageDrop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit()
#    ftpup.storbinary("STOR " + file, open(file, "rb"), 8*1024)


## Create BG image to Composite Primary over inorder to pad BC cutoffs on List page
def pad_image_to_x480(file):
    from PythonMagick import Image, CompositeOperator
    fname = file.split(".")[0]
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + "_" + "l" + ".jpg")

    ## Make BG layer
    bgimg = Image('400x480', 'white')

    ## Open Primary image 
    img = Image(file)
    img.backgroundColor("white")
    img.sample('350x432')

    # Composite + Save Primary over bg, padding primary with white of bg
    type = img.type
    img.composite(bgimg, 0, 0, CompositeOperator.DstOverCompositeOp)
    img.magick('JPG')
    img.type = type
    img.quality(100)
    img.write(outfile)


def subproc_pad_to_x480(file,destdir):
    import subprocess, os
    
    fname = file.split(".")[0]
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + "_" + "l" + ".jpg")
    
    try:
            
        subprocess.call([
            "convert",
            file,
            "-format",
            "jpg",
            "-resize",
            "350x432",
            "-background",
            "white",
            "-gravity",
            "center",
            "-extent",
            "400x480",
            outfile,
        ])

    except:
        print "Failed: {0}".format(file)
    return outfile

################# RUN ###########################
################# RUN ###########################

import sys,os,re,ftplib
#import PythonMagick as Magick
categoryid = sys.argv[1]

## Get the Styles within this event
event_styles = event_styles_by_categoryid(categoryid)
count = 0

prodimages_share = '/home/johnb/Share/PRODIMAGES_OUTPUT'

### Iterate list and Download Files from Netsrv101
for k,v in event_styles.iteritems():
    event_id = v['event_id']
    colorstyle = str(k)
    hashdir = colorstyle[:4]
    colorstyle_file = colorstyle + ".png"
    remotedir = "/mnt/images/images"
    remotepath = os.path.join(remotedir, hashdir, colorstyle_file)
    destdir = os.path.join(prodimages_share, 'event_' + str(event_id))
    destpath = os.path.join(destdir, colorstyle_file)
    
    if os.path.isdir(destdir):
        pass
    else:
        try:
            os.makedirs(destdir, 16877)
        except OSError:
            pass

    try:
        getbinary_ftp_netsrv101(remotepath, outfile=destpath)
        print "Successfully Downloaded {0}".format(destpath)
        count += 1
        print "Files Downloaded: {0}".format(count)
    except:
        print "{0} Does Not Exist".format(remotepath)
        pass
    ## weddavLogin="https://imagedrop:imagedrop0@file3.bluefly.corp/ImageDrop/"


print "Total Files Downloaded: {0}".format(count)
#

### Now that Files have downloaded, change dirs to dload folder and pad images using subproc + ImageMagick Then load the _l
os.chdir(destdir)
for f in os.listdir(destdir):
    padded_file = subproc_pad_to_x480(f,destdir)
    ## Uncomment below to have padded file autoload after padding
    #upload_to_imagedrop(padded_file)
    

     