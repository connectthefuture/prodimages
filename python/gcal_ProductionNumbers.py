#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 20:58:41 2013

@author: JCut
"""
#!/usr/bin/env python

def sql_query_production_numbers():
    import sqlalchemy
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
    connection = orcl_engine.connect()

    ### Get Production Complete Totals and Build Dict of key value pairs
    querymake_prodnumbers = '''SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as completion_total,
    POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as prod_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT >= TRUNC(SysDate - 25)
    GROUP BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT
    ORDER BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT DESC'''
    prodcomplete = connection.execute(querymake_prodnumbers)
    prodcomplete_dict = {}
    for row in prodcomplete:
            tmp_dict = {}
            tmp_dict['completion_total'] = row['completion_total']
            tmp_dict['role'] = 'Production'
            prodcomplete_dict[row['prod_complete_dt']] = tmp_dict

    ### Get Retouching Complete Totals and Build Dict of key value pairs
    querymake_retouchnumbers = '''SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as retouch_total,
    POMGR.PRODUCT_COLOR.IMAGE_READY_DT as retouch_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT >= TRUNC(SysDate - 25)
    GROUP BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC'''
    retouchcomplete = connection.execute(querymake_retouchnumbers)
    retouchcomplete_dict = {}
    for row in retouchcomplete:
            tmp_dict = {}
            tmp_dict['retouch_total'] = row['retouch_total']
            tmp_dict['role'] = 'Retouching'
            retouchcomplete_dict[row['retouch_complete_dt']] = tmp_dict

    ### Get Copy Complete Totals and Build Dict of key value pairs
    querymake_copynumbers = '''SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as copy_total,
    POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.COPY_READY_DT >= TRUNC(SysDate - 25)
    GROUP BY POMGR.PRODUCT_COLOR.COPY_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.COPY_READY_DT DESC'''
    copycomplete = connection.execute(querymake_copynumbers)
    copycomplete_dict = {}
    for row in copycomplete:
            tmp_dict = {}
            tmp_dict['copy_total'] = row['copy_total']
            tmp_dict['role'] = 'Copy'
            copycomplete_dict[row['copy_complete_dt']] = tmp_dict

    connection.close()
    return prodcomplete_dict, retouchcomplete_dict, copycomplete_dict


## Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    return walkedlist


###
## Extract All Metadata from Image File as Dict using PIL
def get_exif(file_path):
    from PIL import Image
    from PIL.ExifTags import TAGS
    exifdata = {}
    im = Image.open(file_path)
    info = im._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exifdata[decoded] = value
    return exifdata


###
## Convert Walked Dir List To Lines with path,photo_date,stylenum,alt. Depends on above "get_exif" function
def walkeddir_parse_stylestrings_out(walkeddir_list):
    import re,os
########  Regex only finds _1.jpg files
    regex = re.compile(r'.*?[0-9]{9}_1\.[jpgJPG]{3}$')
    regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    stylestrings = []
    stylestringsdict = {}
    for line in walkeddir_list:
        stylestringsdict_tmp = {}
        if re.findall(regex,line):
            try:
                file_path = line
                filename = file_path.split('/')[-1]
                colorstyle = filename.split('_')[0]
                alt_ext = file_path.split('_')[-1]
                alt = alt_ext.split('.')[0]
                ext = alt_ext.split('.')[-1]
                try:
                    path_date = file_path.split('/')[4][:6]
                    path_date = "20{2:.2}-{0:.2}-{1:.2}".format(path_date[:2], path_date[2:4], path_date[4:6])
                    if re.findall(regex_date, path_date):
                        photo_date = path_date
                    else:
                        try:
                            photo_date = get_exif(file_path)['DateTimeOriginal'][:10]
                        except KeyError:
                            try:
                                photo_date = get_exif(file_path)['DateTime'][:10]
                            except KeyError:
                                photo_date = '0000-00-00'
                except AttributeError:
                    photo_date = '0000-00-00'
                photo_date = str(photo_date)
                photo_date = photo_date.replace(':','-')
                stylestringsdict_tmp['colorstyle'] = colorstyle
                stylestringsdict_tmp['photo_date'] = photo_date
                stylestringsdict_tmp['file_path'] = file_path
                stylestringsdict_tmp['alt'] = alt
                stylestringsdict[file_path] = stylestringsdict_tmp
                file_path_reletive = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
                file_path_reletive = file_path.replace('JPG', 'jpg')
                ## Format CSV Rows
                row = "{0},{1},{2},{3}".format(colorstyle,photo_date,file_path_reletive,alt)
                #print row
                stylestrings.append(row)
            except IOError:
                print "IOError on {0}".format(line)
            #except AttributeError:
            #    print "AttributeError on {0}".format(line)
    return stylestringsdict



def gcal_insert_bc_event(titleid, descfull, lockv, sdatekv, edatekv):
    from GoogleCalendar import GoogleCalendarMng, newEvent
    import GoogleCalendar
    try:
        #from GoogleCalendar import *
        gCalMNG = GoogleCalendarMng()
        myname = "john bragato"
        myemail = "john.bragato@gmail.com"
        gCalMNG.connect (myemail, "yankee17")
        calendar = gCalMNG.getCalendar ("Default1")
        gcalevents = calendar.getEvents()
        print len(gcalevents)
        gcaleventslist = []
        for event in gcalevents:
            gcalevent = event.getTitle()
            if gcalevent == titleid:
                continue
            else:
                print event.getContent()
                #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
                #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
        ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
        print ev
        calendar.addEvent (ev)
    except xml.parsers.expat.ExpatError:
    #except:
        print "FAILED"

##
def gcal_login_jb(myemail='john.bragato@gmail.com', password='yankee17'):
    from GoogleCalendar import GoogleCalendarMng
    import xml
    gCalMNG = GoogleCalendarMng()
    myemail = myemail
    gCalMNG.connect(myemail, password)
    return gCalMNG
##
##
def get_google_event_data(event):
    eventid = event.getID()
    content = event.getContent()
    title = event.getTitle()
    editing_url = event.getEditURL()
    #print eventid, title, editing_url
    title_4digit = title.strip(r'')
    #title_4digit = bfly_eventnum[:4]
    #if title_4digit.isdigit():
    return editing_url, title_4digit, title, content

##
def delete_gcalendar_event(titleid, calendar_name='Default1', myemail='john.bragato@gmail.com', password='yankee17'):
    from GoogleCalendar import GoogleCalendarMng
    import xml
    gCalMNG = GoogleCalendarMng()
    myname = myemail.split('@')[0]
    myemail = myemail
    gCalMNG.connect(myemail, password)
    calendar = gCalMNG.getCalendar(calendar_name)
    events = calendar.getEvents()
    for event in events:
        if event.getTitle() == titleid:
            event.delete()
            return "Deleted {0}".format(titleid)


###
#
# First retrieve the event from the API.
#event = service.events().get(calendarId='primary', eventId='eventId').execute()

#event['summary'] = 'Appointment at Somewhere'

#updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

# Print the updated date.
#print updated_event['updated']


#
############## RUN ###########
import os,re,sys,csv
from collections import defaultdict

regex = re.compile(r'.*?[0-9]{9}_1\.[jpgJPG]{3}$')

### Query DB for Prod,Retouch and Copy counts by date
prodcomplete_dict, retouchcomplete_dict, copycomplete_dict = sql_query_production_numbers()

#print prodcomplete_dict
######  Recursively search Photo Folders and get counts of shots by date
rootdir_fashion = '/mnt/Post_Ready/Retouch_Fashion'
#####  Walk rootdir tree compile dict of Walked Directory
walkedout_fashion = recursive_dirlist(rootdir_fashion)
#### Parse Walked Directory Paths Output stylestringssdict
stylestringsdict_fashion = walkeddir_parse_stylestrings_out(walkedout_fashion)
### Get and Collect Counts of fashion and still sets by date
fashiond = defaultdict(list)
for row in stylestringsdict_fashion.itervalues():
    file_path = row['file_path']
    photo_date = row['photo_date']
    try:
        dt = photo_date
        dt = "{} 00:00:00".format(dt)
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        #### 5 digit date
        photo_date = dt
    except:
        pass
    fashiond[photo_date].append(file_path)
## Count the Grouped Files
# fashioncomplete_dict = defaultdict(int)
# for k in fashiond:
#     fashioncomplete_dict[k] +=1
fashioncomplete_dict = {}
for k,v in fashiond.iteritems():
    fashioncomplete_dict[k] = len(v)
#    fashioncomplete_dict['Role'] = 'Fashion_Photo'
#    fashioncomplete_dict['shot_count'] = len(v)
######
####
######  Recursively search Photo Folders and get counts of shots by date
rootdir_still = '/mnt/Post_Ready/Retouch_Still'
#####  Walk rootdir tree compile dict of Walked Directory
walkedout_still = recursive_dirlist(rootdir_still)
#### Parse Walked Still Directory Paths Output stylestringssdict
stylestringsdict_still = walkeddir_parse_stylestrings_out(walkedout_still)
### Now the still sets counts by date
stilld = defaultdict(list)
for row in stylestringsdict_still.itervalues():
    file_path = row['file_path']
    photo_date = row['photo_date']
    try:
        dt = photo_date
        dt = "{} 00:00:00".format(dt)
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        #### 5 digit date
        photo_date = dt
    except:
        pass
    stilld[photo_date].append(file_path)
## Count the Grouped Files
stillcomplete_dict = {}
for k,v in stilld.iteritems():
    stillcomplete_dict[k] = len(v)
#    stillcomplete_dict['Role'] = 'Still_Photo'
#    fashioncomplete_dict['shot_count'] = len(v)

#####  Consignment ######
rootdir_consig = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment'
walkedout_consig = recursive_dirlist(rootdir_consig)
#### Parse Walked Directory Paths Output stylestringssdict
stylestringsdict_consig= walkeddir_parse_stylestrings_out(walkedout_consig)
### Get and Collect Counts of fashion and still sets by date
consigd = defaultdict(list)
for row in stylestringsdict_consig.itervalues():
    file_path = row['file_path']
    photo_date = row['photo_date']
    try:
        dt = photo_date
        dt = "{} 00:00:00".format(dt)
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        #### 5 digit date
        photo_date = dt
    except:
        pass
    consigd[photo_date].append(file_path)
## Count the Grouped Files
consigcomplete_dict = {}
for k,v in consigd.iteritems():
    consigcomplete_dict[k] = len(v)
    consigcomplete_dict['Role'] = 'Consig_Photo'



for k,v in iter(prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, stillcomplete_dict, fashioncomplete_dict):


## First compile the Fields as key value pairs
fulldict = {}
for k,v in stylestringsdict.iteritems():
    dfill = {}
    dfill['colorstyle'] = v['colorstyle']
    dfill['photo_date'] = v['photo_date']
    file_path = k
    file_path = file_path.replace('/mnt/Post_Ready/zImages_1/', '/zImages/')
    file_path = file_path.replace('/mnt/Post_Ready/Retouch_', '/Retouch_')
    dfill['file_path'] = file_path
    dfill['alt'] = v['alt']
    fulldict[k] = dfill


#regex = re.compile(r'.+?\.[jpgJPG]{3}$')

## Write CSV List to dated file for Impor t to MySQL
#csv_write_datedOutfile(stylestrings)

#count = 0
#for k,v in future_events.iteritems():
#    import datetime, time
#    for value in [v]:
#        titlekv = str(value['event_id'])
#        desckv = str(value['event_title'])
#        desckv = desckv.replace('&', 'And')
#        desckv = desckv.replace('%', ' Percent')
#        colorstyles = future_styles.get(value['event_id'])
#        colorstyles = sorted(colorstyles)
#        still_complete = []
#        fashion_complete = []
#
#
#        for colorstyle in colorstyles:
#            if colorstyle[1] == 'Production Complete':
#                complete.append(colorstyle)
#            elif colorstyle[1] == 'Production Incomplete':
#                incomplete.append(colorstyle)
#        incomplete_styles = "{0} Incomplete Styles = {1}".format(len(incomplete),incomplete)
#        complete_styles = "{0} Complete Styles = {1}".format(len(complete),complete)
#        colorstyles_statuses = "{0}\n{1}".format(incomplete_styles,complete_styles)
#
#        count_complete = len(complete)
#        count_incomplete = len(incomplete)
#        count_total = count_complete + count_incomplete
#
#        progress = count_complete/count_total*100
#
#
#        sdatekvraw = '{:%Y,%m,%d,00,00,00,00,00,00}'.format(value['ev_start'])
#        edatekvraw = '{:%Y,%m,%d,00,00,00,00,00,00}'.format(value['ev_end'])
#        sdatekvsplit = sdatekvraw.split(",")
#        edatekvsplit = edatekvraw.split(",")
#        sdatekv = map(int,sdatekvsplit)
#        edatekv = map(int,edatekvsplit)
#        titleid = 'Event {0} -- {1}'.format(titlekv,desckv)
#        descfull = '{0} {1} in Event {2}:\n {3}\n'.format(len(colorstyles), prod_category, titlekv, colorstyles_statuses)
#        descfull = str(descfull)
#        #print titleid, descfull, edatekv, prod_category, lockv
#        count += 1
#        #print count
#
#        try:
#        #gcal_insert_bc_event(titleid, descfull, lockv, sdatekv, edatekv)
#            gCalMNG = gcal_login_jb()
#            #calendar = gCalMNG.getCalendar("Default1")
#            gcalevents = gCalMNG.getCalendar("ProductionNumbers").getEvents()
#            print len(gcalevents)
#            gcaleventslist = []
#            for event in gcalevents:
#                gcalevent = event.getTitle()
#                if gcalevent == titleid:
#                    continue
#                else:
#                    print event.getContent()
#                    #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getStartTime()))
#                    #print time.strftime("%Y-%m-%dT%H:%M:%S" , time.localtime(event.getEndTime()))
#            ev = newEvent(myname, myemail, titleid, descfull, lockv, time.mktime(sdatekv), time.mktime(edatekv))
#            print ev
#            calendar.addEvent (ev)
#        except xml.parsers.expat.ExpatError:
#        #except:
#            print "FAILED" #+ k,v
#        #    continue
