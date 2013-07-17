# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:53:20 2013

@author: johnb
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:23:55 2013

@author: jb
"""
def sqlQueryEventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = 'SELECT ATG_SNP.EVENT.ID AS "event_id", ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.NAME AS "category", ATG_SNP.EVENT.EVENT_DESCRIPTION AS "event_title", ATG_SNP.EVENT.START_DATE AS "ev_start", ATG_SNP.EVENT.END_DATE AS "ev_end", ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS "colorstyle", POMGR_SNP.LK_PRODUCT_STATUS.NAME AS "production_status" FROM ATG_SNP.EVENT INNER JOIN ATG_SNP.LK_EVENT_PRODUCT_CATEGORY ON ATG_SNP.EVENT.PRODUCT_CATEGORY_ID = ATG_SNP.LK_EVENT_PRODUCT_CATEGORY.ID RIGHT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON ATG_SNP.EVENT.ID = ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID INNER JOIN ATG_SNP.PRODUCT_COLOR ON ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = ATG_SNP.PRODUCT_COLOR.ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON ATG_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID WHERE ATG_SNP.EVENT.START_DATE >= TRUNC(SysDate) ORDER BY ATG_SNP.EVENT.ID DESC, ATG_SNP.EVENT.START_DATE DESC Nulls Last'
    result = connection.execute(querymake_eventscal)
    
    events = {}
    for row in result:
        event = {}        
        event['event_id'] = row['event_id']
        event['category'] = row['category']                
        event['event_title'] = row['event_title']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']        
        event['colorstyle'] = row['colorstyle']        
        event['production_status'] = row['production_status']  
        events[row['colorstyle']] = event
       
    print events
    connection.close()
    return events

# First retrieve the event from the API.
#event = service.events().get(calendarId='primary', eventId='eventId').execute()

#event['summary'] = 'Appointment at Somewhere'

#updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

# Print the updated date.
#print updated_event['updated']


future_events = sqlQueryEventsUpcoming()

for key,value in future_events.iteritems():
    import datetime, time    
    for kv in iter(value):
        titlekv = value['event_id']
        desckv = value['event_title']
        colorstyle = value['colorstyle']
        status = value['production_status']
        category = value['category']
                
        lockv = str(category)
        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
        sdatekvsplit = sdatekvraw.split(",")
        edatekvsplit = edatekvraw.split(",")
        sdatekv = map(int,sdatekvsplit)
        edatekv = map(int,edatekvsplit)
        titleid = '{0}_{1}'.format(titlekv,desckv)
        descfull = '{0}_{1}'.format(colorstyle,status)
        descfull = str(descfull)    
        try:
            
            from GoogleCalendar import *
            gCalMNG = GoogleCalendarMng()
            myname = "john bragato"
            myemail = "john.bragato@gmail.com"
            gCalMNG.connect (myemail, "yankee17")
            calendar = gCalMNG.getCalendar ("Default1")
            gcalevents = calendar.getEvents()
        
            
            for event in gcalevents:
                print event.getTitle()
                print event.getContent()
                print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
                print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
            ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
            print ev
            calendar.addEvent (ev)
        except TypeError:
            print "Type_Error"
        except xml.parsers.expat.ExpatError:
            print "FAILED" + key,value
            continue
    
    
    
    
########################################################### Alt Script Below  
    
#!/usr/bin/python

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
    
    querymake_metatags="SELECT DISTINCT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.BRAND.NAME AS brand, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') AS copy_dt, POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL AS category_parent, POMGR_SNP.PRODUCT_FOLDER.LABEL AS category_sub, MAX(ATG_SNP.EVENT.ID) AS event_id, POMGR_SNP.LK_PRODUCT_STATUS.NAME AS production_status, MAX(ATG_SNP.EVENT.EVENT_DESCRIPTION) AS event_title, MAX(to_date(POMGR_SNP.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')) AS sample_dt, MAX(POMGR_SNP.LK_SAMPLE_STATUS.NAME) AS sample_status, MAX(POMGR_SNP.PO_LINE.PO_HDR_ID) AS po_num, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style FROM POMGR_SNP.PRODUCT_COLOR LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON POMGR_SNP.PRODUCT_COLOR.ID = ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID LEFT JOIN ATG_SNP.EVENT ON ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID INNER JOIN POMGR_SNP.PRODUCT ON POMGR_SNP.PRODUCT_COLOR.PRODUCT_ID = POMGR_SNP.PRODUCT.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER ON POMGR_SNP.PRODUCT.PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER.ID INNER JOIN POMGR_SNP.BRAND ON POMGR_SNP.PRODUCT.BRAND_ID = POMGR_SNP.BRAND.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED ON POMGR_SNP.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.ID LEFT JOIN POMGR_SNP.SAMPLE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.SAMPLE.PRODUCT_COLOR_ID LEFT JOIN POMGR_SNP.SAMPLE_TRACKING ON POMGR_SNP.SAMPLE.ID = POMGR_SNP.SAMPLE_TRACKING.SAMPLE_ID LEFT JOIN POMGR_SNP.LK_SAMPLE_STATUS ON POMGR_SNP.SAMPLE_TRACKING.STATUS_ID = POMGR_SNP.LK_SAMPLE_STATUS.ID LEFT JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.ID = '" + style + "' GROUP BY POMGR_SNP.PRODUCT_COLOR.ID, POMGR_SNP.BRAND.NAME, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD'), POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL, POMGR_SNP.PRODUCT_FOLDER.LABEL, POMGR_SNP.LK_PRODUCT_STATUS.NAME, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE ORDER BY POMGR_SNP.PRODUCT_COLOR.ID DESC"
    
    result = connection.execute(querymake_metatags)
    metatags = {}
    for row in result:
        metatag = {}        
        metatag['colorstyle'] = row['colorstyle']
        metatag['Keywords'] = row['brand']
        metatag['IPTC:SpecialInstructions'] = row['copy_dt']
        metatag['XMP:Album'] = row['category_parent'] + "_" + row['category_sub']
        #metatag['category_sub'] = row['category_sub']
        metatag['XMP:Genre'] = row['event_id']
        metatag['IPTC:CopyrightNotice'] = row['production_status']
        metatag['IPTC:Credit'] = row['event_title']
        metatag['IPTC:Source'] = row['sample_dt']
        metatag['IPTC:SimilarityIndex'] = row['sample_status']
        metatag['IPTC:PONumber'] = row['po_num']
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        #metatag['SourceFile'] = str(f)
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag
        
    connection.close()
    return metatags
    
    
#def newDatedCsvWriter(lines):
#    import csv, string, datetime
#    dt = str(datetime.datetime.now())
#    today = dt.split(' ')[0]
#    f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
#    for line in lines:
#        with open(f, 'ab+') as csvwritefile:

#            writer = csv.writer(csvwritefile, delimiter=',')
#            writer.writerows([lines])
#
#def newCsvReader(f):
#    with open(f, 'rb') as csvreadfile:
#        reader = csv.reader(csvreadfile)
#        for rows in reader:
#            for row in rows:
#                return row

#def writeXmp(imgfile,xmpkey,xmpvalue):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[xmpkey] = xmpvalue
#    
#def writeIptc(imgfile,iptckey,iptcvalue):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[iptckey] = iptcvalue
#
#def writeExif(imgfile,exifkey,exifvalue):
#    import pyexiv2    
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[exifkey] = exifvalue
#
#def readIptc(imgfile):
#    import pyexiv2    
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    mdataprint = metadata.read()
#    print metadata

####### 
#####################
#######    
                                                

import sys
import os
import glob
import sqlalchemy
#glbdir = sys.argv[1]
glbdir='/mnt/Post_Ready/aPhotoPush'
#glbdir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117257'
#globtoconvert = os.path.join('/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/images_for_conversion/117147', '*.jpg')

globtoconvert = glob.glob(os.path.join(os.path.realpath(glbdir), '*/*/*.jpg'))
#print globtoconvert

for f in globtoconvert:
    stylefile = os.path.basename(f)
    style = stylefile.split('_')[0]
    exiftoolstring = sqlQueryMetatags(style,f)

    
    for key, values in exiftoolstring.iteritems():
        #exifcmds = {}
        for value in iter(values):
            #exifcmd = {}
            try:
                
                exifcmd = str('exiftool -' + "'" + value + "=" + str(values[value]) + "'" + '')
                lines = str(exifcmd + " " + f)

            ###    Now MAke csv file with each tag as line of exiftool shell script
                print lines
            #newDatedCsvWriter([lines])
            except TypeError:
                print "TypeError{0}".format(value)
    
    


