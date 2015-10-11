#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 20:58:41 2013

@author: JCut
"""
#!/usr/bin/env python

def sql_query_production_numbers():
    import sqlalchemy
    import datetime
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    ### Get Production Complete Totals and Build Dict of key value pairs
    querymake_prodnumbers = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as completion_total,
    POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT as prod_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT >= TRUNC(SysDate - 30)
    GROUP BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT
    ORDER BY POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT DESC"""
    prodcomplete = connection.execute(querymake_prodnumbers)
    prodcomplete_dict = {}
    for row in prodcomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['completion_total']
        tmp_dict['role'] = 'Production'
        prodcomplete_dict[row['prod_complete_dt']] = tmp_dict

    ### Get Retouching Complete Totals and Build Dict of key value pairs
    querymake_retouchnumbers = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as retouch_total,
    POMGR.PRODUCT_COLOR.IMAGE_READY_DT as retouch_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT >= TRUNC(SysDate - 30)
    GROUP BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC"""
    retouchcomplete = connection.execute(querymake_retouchnumbers)
    retouchcomplete_dict = {}
    for row in retouchcomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['retouch_total']
        tmp_dict['role'] = 'Retouching'
        retouchcomplete_dict[row['retouch_complete_dt']] = tmp_dict

    ### Get Copy Complete Totals and Build Dict of key value pairs
    querymake_copynumbers = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as copy_total,
    to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') as copy_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.COPY_READY_DT >= TRUNC(SysDate - 30)
    GROUP BY to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD')
    ORDER BY to_date(POMGR.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') DESC"""
    copycomplete = connection.execute(querymake_copynumbers)
    copycomplete_tmpdict = {}
    for row in copycomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['copy_total']
        tmp_dict['role'] = 'Copy'
        copycomplete_tmpdict[row['copy_complete_dt']] = tmp_dict
## Super Coersion of nums and year due to time stamp occasionally on copy dates
    copycomplete_dict = {}
    for k,v in copycomplete_tmpdict.iteritems():
        tmp_dict = {}
        tmp_dict['total'] = v['total']
        tmp_dict['role'] = v['role']
        dt = str(datetime.datetime.strptime(str(k), "%Y-%m-%d %H:%M:%S"))
        dtsplit = dt.replace('00','', 2)
        dtsplit = "20{2:.2}-{1:.2}-{0:.2} 00:00:00".format(dtsplit[:2],dtsplit[3:5],dtsplit[6:8])
        dtsplit = datetime.datetime.strptime(dtsplit, "%Y-%m-%d %H:%M:%S")
        copycomplete_dict[dtsplit] = tmp_dict

    ### Get Sample Received Totals and Build Dict of key value pairs
    querymake_sample_received = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as sample_total,
    to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') AS sample_dt
    FROM POMGR.PRODUCT_COLOR
    LEFT JOIN POMGR.SAMPLE ON POMGR.PRODUCT_COLOR.ID = POMGR.SAMPLE.PRODUCT_COLOR_ID
    LEFT JOIN POMGR.SAMPLE_TRACKING ON POMGR.SAMPLE.ID = POMGR.SAMPLE_TRACKING.SAMPLE_ID
    LEFT JOIN POMGR.LK_SAMPLE_STATUS ON POMGR.SAMPLE_TRACKING.STATUS_ID = POMGR.LK_SAMPLE_STATUS.ID
    WHERE (POMGR.SAMPLE_TRACKING.CREATE_DT >= TRUNC(SysDate - 30)
    AND POMGR.LK_SAMPLE_STATUS.NAME = 'Scanned In at Bluefly')
    GROUP BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')
    ORDER BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') DESC"""
    samples_received = connection.execute(querymake_sample_received)
    samples_received_tmpdict = {}
    for row in samples_received:
        tmp_dict = {}
        tmp_dict['total'] = row['sample_total']
        tmp_dict['role'] = 'Samples_Received'
        samples_received_tmpdict[row['sample_dt']] = tmp_dict
## Super Coersion of nums and year due to time stamp occasionally on copy dates
    samples_received_dict = {}
    for k,v in samples_received_tmpdict.iteritems():
        tmp_dict = {}
        tmp_dict['total'] = v['total']
        tmp_dict['role'] = v['role']
        dt = str(datetime.datetime.strptime(str(k), "%Y-%m-%d %H:%M:%S"))
        dtsplit = dt.replace('00','', 2)
        dtsplit = "20{2:.2}-{1:.2}-{0:.2} 00:00:00".format(dtsplit[:2],dtsplit[3:5],dtsplit[6:8])
        dtsplit = datetime.datetime.strptime(dtsplit, "%Y-%m-%d %H:%M:%S")
        samples_received_dict[dtsplit] = tmp_dict

#    ### Get Sample InHouse Totals and Build Dict of key value pairs
#    querymake_samples_inhouse = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as sample_total,
#    to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') AS sample_dt,
#    POMGR.PRODUCT_COLOR.PRODUCTION_STATUS as production_status
#    FROM POMGR.PRODUCT_COLOR
#    LEFT JOIN POMGR.SAMPLE ON POMGR.PRODUCT_COLOR.ID = POMGR.SAMPLE.PRODUCT_COLOR_ID
#    LEFT JOIN POMGR.SAMPLE_TRACKING ON POMGR.SAMPLE.ID = POMGR.SAMPLE_TRACKING.SAMPLE_ID
#    LEFT JOIN POMGR.LK_SAMPLE_STATUS ON POMGR.SAMPLE_TRACKING.STATUS_ID = POMGR.LK_SAMPLE_STATUS.ID
#    WHERE (POMGR.SAMPLE_TRACKING.CREATE_DT > TRUNC(SysDate - 30)
#    AND POMGR.LK_SAMPLE_STATUS.NAME = 'Scanned In at Bluefly'
#    AND POMGR.PRODUCT_COLOR.PRODUCTION_STATUS = 'Production_Incomplete')
#    GROUP BY POMGR.PRODUCT_COLOR.PRODUCTION_STATUS,
#    to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')
#    ORDER BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') DESC"""
#    samples_inhouse = connection.execute(querymake_samples_inhouse)
#    samples_inhouse_tmpdict = {}
#    for row in samples_inhouse:
#        tmp_dict = {}
#        tmp_dict['total'] = row['sample_total']
#        tmp_dict['role'] = 'Samples_Inhouse'
#        samples_inhouse_tmpdict[row['sample_dt']] = tmp_dict
### Super Coersion of nums and year due to time stamp occasionally on copy dates
#    samples_inhouse_dict = {}
#    for k,v in samples_inhouse_tmpdict.iteritems():
#        tmp_dict = {}
#        tmp_dict['total'] = v['total']
#        tmp_dict['role'] = v['role']
#        dt = str(datetime.datetime.strptime(str(k), "%Y-%m-%d %H:%M:%S"))
#        dtsplit = dt.replace('00','', 2)
#        dtsplit = "20{2:.2}-{1:.2}-{0:.2} 00:00:00".format(dtsplit[:2],dtsplit[3:5],dtsplit[6:8])
#        dtsplit = datetime.datetime.strptime(dtsplit, "%Y-%m-%d %H:%M:%S")
#        samples_inhouse_dict[dtsplit] = tmp_dict


    connection.close()
    return prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict


def sqlQueryEventsUpcoming():
    import sqlalchemy
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    querymake_eventscal = '''SELECT DISTINCT
      POMGR.EVENT.ID                             AS event_id,
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID AS colorstyle,
      POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME       AS prod_category,
      POMGR.EVENT.EVENT_DESCRIPTION              AS event_title,
      POMGR.EVENT.START_DATE                     AS ev_start,
      POMGR.EVENT.END_DATE                       AS ev_end,
      POMGR.LK_PRODUCT_STATUS.NAME               AS production_status,
      POMGR.EVENT.CATEGORY                       AS category_id
    FROM
      POMGR.EVENT_PRODUCT_COLOR
    LEFT JOIN POMGR.EVENT
    ON
      POMGR.EVENT_PRODUCT_COLOR.EVENT_ID = POMGR.EVENT.ID
    INNER JOIN POMGR.LK_EVENT_PRODUCT_CATEGORY
    ON
      POMGR.EVENT.PRODUCT_CATEGORY_ID = POMGR.LK_EVENT_PRODUCT_CATEGORY.ID
    LEFT JOIN POMGR.PRODUCT_COLOR
    ON
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID
    LEFT JOIN POMGR.LK_PRODUCT_STATUS
    ON
      POMGR.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR.LK_PRODUCT_STATUS.ID
    WHERE
      POMGR.EVENT.START_DATE >= TRUNC(SysDate)
    GROUP BY
      POMGR.EVENT.ID,
      POMGR.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID,
      POMGR.LK_EVENT_PRODUCT_CATEGORY.NAME,
      POMGR.EVENT.EVENT_DESCRIPTION,
      POMGR.EVENT.START_DATE,
      POMGR.EVENT.END_DATE,
      POMGR.LK_PRODUCT_STATUS.NAME,
      POMGR.EVENT.CATEGORY'''
    result = connection.execute(querymake_eventscal)

    events = {}
    styles = defaultdict(list)
    for row in result:
        event = {}
        event['event_id'] = row['event_id']
        event['prod_category'] = row['prod_category']
        event['event_title'] = row['event_title']
        event['category_id'] = row['category_id']
        event['ev_start'] = row['ev_start']
        event['ev_end'] = row['ev_end']
        event['production_status'] = row['production_status']

        status = str(row['production_status'])
        colorstyle = str(row['colorstyle'])

        stylestatus = (colorstyle,status)
        styles[row['event_id']].append(stylestatus)
        events[row['event_id']] = event

    connection.close()
    return events, styles



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
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


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
def gcal_login_jb(myemail='john.bragato@gmail.com', password=''):
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
def delete_gcalendar_event(titleid, calendar_name='Default1', myemail='john.bragato@gmail.com', password=''):
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



def fashioncomplete():
    import datetime
    from collections import defaultdict
    ######  Recursively search Photo Folders and get counts of shots by date
    ## rootdir_fashion = '/mnt/Post_Ready/Retouch_Fashion'
    rootdir_fashion = '/mnt/Post_Ready/eFashionPush'
    #####  Walk rootdir tree compile dict of Walked Directory
    walkedout_fashion = recursive_dirlist(rootdir_fashion)
    #### Parse Walked Directory Paths Output stylestringssdict
    stylestringsdict_fashion = walkeddir_parse_stylestrings_out(walkedout_fashion)
    ### Get and Collect Counts of fashion and still sets by date
    fashiond = defaultdict(list)
    for row in stylestringsdict_fashion.itervalues():
        try:
            file_path = row['file_path']
            photo_date = row['photo_date']
            dt = photo_date
            dt = "{} 00:00:00".format(dt)
            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            #### 5 digit date
            if type(dt) == datetime.datetime:
                photo_date = dt
                fashiond[photo_date].append(file_path)
        except:
            pass
    ## Count the Grouped Files
    # fashioncomplete_dict = defaultdict(int)
    # for k in fashiond:
    #     fashioncomplete_dict[k] +=1
    fashioncomplete_dict = {}
    for k,v in fashiond.iteritems():
        tmp_dict = {}
        tmp_dict['role'] = 'Fashion'
        tmp_dict['total'] = len(v)
        fashioncomplete_dict[k] = tmp_dict
    #    fashioncomplete_dict['Role'] = 'Fashion_Photo'
    #    fashioncomplete_dict['shot_count'] = len(v)
    return fashioncomplete_dict



def stillcomplete():
    import datetime
    from collections import defaultdict
    ######  Recursively search Photo Folders and get counts of shots by date
    ## rootdir_still = '/mnt/Post_Ready/Retouch_Still'
    rootdir_still = '/mnt/Post_Ready/aPhotoPush'
    #####  Walk rootdir tree compile dict of Walked Directory
    walkedout_still = recursive_dirlist(rootdir_still)
    #### Parse Walked Still Directory Paths Output stylestringssdict
    stylestringsdict_still = walkeddir_parse_stylestrings_out(walkedout_still)
    ### Now the still sets counts by date
    stilld = defaultdict(list)
    for row in stylestringsdict_still.itervalues():
        try:
            file_path = row['file_path']
            photo_date = row['photo_date']
            dt = photo_date
            dt = "{} 00:00:00".format(dt)
            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            #### 5 digit date
            if type(dt) == datetime.datetime:
                photo_date = dt
                stilld[photo_date].append(file_path)
    #        else:
    #            dt = ''
    #            dt = "2000-01-01 00:00:00".format(dt)
    #            dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    #            photo_date = dt
    #            stilld[photo_date].append(file_path)
        except:
            pass

    ## Count the Grouped Files
    stillcomplete_dict = {}
    for k,v in stilld.iteritems():
        tmp_dict = {}
        tmp_dict['role'] = 'Still'
        tmp_dict['total'] = len(v)
        stillcomplete_dict[k] = tmp_dict
    #    stillcomplete_dict['Role'] = 'Still_Photo'
    #    fashioncomplete_dict['shot_count'] = len(v)
    return stillcomplete_dict





              # event = {
              #   "end": {
              #   },
              #   "start": {
              #   },
              #   "gadget": {
              #       "display": "",
              #       "preferences": {
              #           "": ""
              #           },
              #       "type": "",
              #       "title": "",
              #       "width": "",
              #       "iconLink": "",
              #       "link": "",
              #       "height": ""
              #       },
              #   "sequence": "",
              #   "description": "",
              #   "colorId": "",
              #   "htmlLink": "",
              #   "source": {
              #       "url": "",
              #       "title": ""
              #       },
              #   "id": "",
              #   "creator": {
              #       "displayName": "",
              #       "self": false,
              #       "email": "",
              #       "id": ""
              #   },
              #   "location": "",
              #   "summary": "",
              #   "status": "",
              #   "hangoutLink": "",
              #   "kind": "calendar#event",
              #   "organizer": {
              #       "displayName": "",
              #       "email": "",
              #       "id": "",
              #       "self": false
              #       },
              #   "updated": "",
              #   "reminders": {
              #       "overrides": [
              #           {
              #           "method": "",
              #           "minutes": ""
              #           }
              #       ],
              #       "useDefault": false
              #   },
              #   "created": "",
              #   "attendees": [
              #       {
              #       "email": "",
              #       "displayName": "",
              #       "id": "",
              #       "organizer": false,
              #       "resource": false,
              #       "responseStatus": "",
              #       "additionalGuests": "",
              #       "optional": false,
              #       "self": false,
              #       "comment": ""
              #       }
              #   ]
              #   }


