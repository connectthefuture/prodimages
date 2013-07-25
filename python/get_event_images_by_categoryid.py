#!/usr/bin/env python

def event_styles_by_categoryid(categoryid):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
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
    ftpdown = ftplib.FTP("netsrv101.l3.bluefly.com")
    ftpdown.login("imagedrop", "imagedrop0")
    if outfile is None:
        outfile = sys.stdout
        ftpdown.retrbinary("RETR " + remote_pathtofile, outfile.write)


## Upload to imagedrop via FTP
def upload(file):
    ftpup = ftplib.FTP("file3.bluefly.corp/ImageDrop/")
    ftpup.login("imagedrop", "imagedrop0")
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftpup.storlines("STOR " + file, open(file))
    else:
        ftpup.storbinary("STOR " + file, open(file, "rb"), 1024)


################# RUN ###########################
################# RUN ###########################

import sys,os,re,ftplib

categoryid = sys.argv[1]

## Get the Styles within this event
event_styles = event_styles_by_categoryid(categoryid)
count = 0

### Iterate list and Download Files from Netsrv101
for k,v in event_styles.iteritems():
    event_id = v['event_id']
    colorstyle = str(k)
    serverdir = colorstyle[:4]
    colorstyle_file = colorstyle + ".png"
    remotedir = "/mnt/images/images"
    remotepath = os.path.join(remotedir, serverdir, colorstyle_file)
    destdir = os.path.join(os.path.expanduser('~'), 'event_' + str(event_id))
    destpath = os.path.join(destdir, colorstyle_file)
    
    if os.path.isdir(destdir):
        pass
    else:
        try:
            os.makedirs(destdir, 16877)
        except:
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
    