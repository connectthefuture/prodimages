#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import AccessTokenRefreshError
from oauth2client.tools import run
import os, sys

##########################Vars
client_id='924881045523-kc7leju7role0too3k4itlo864eprl1u.apps.googleusercontent.com'
client_secret='rqZxYuy0Cht37rJ0GSZ05YoY'
user_agent='Python2.7'
BROWSERdeveloperKey='AIzaSyBHozNPRDnVkdPo_JlP_4TLbNrJIsd3bQ4'
SERVERdeveloperKey='AIzaSyDe68JsIJK5O5Cqd-tAVGqaSeHqcFCNPh8'



batchRunScripts = os.path.join('/usr/local', 'batchRunScripts')
os.chdir(batchRunScripts)

#here = os.path.dirname(os.path.realpath(os.path.curdir))
storage_file = os.path.join(batchRunScripts, 'calendar.dat')

############################
# FLAGS = gflags.FLAGS

# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id=client_id,
    client_secret=client_secret,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent=user_agent)

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage(storage_file)
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

#prodnumberscal = 'k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com'
prodnumberscal = 'https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com/'
# k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com
# https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s%40group.calendar.google.com/
#prodnumberscal = 'https://www.google.com/calendar/feeds/k8oohvl27sq3u0odgafpbmdl6s%40group.calendar.google.com/private-cfbcfde94d17e48fbf1f824a8536e0ba/basic'
# Build a service object for interacting with the API.
service = build(serviceName='calendar', version='v3', http=http)

# Getting All Event Ids
page_token = None
events_list = []
try:    
    while True:
        events = service.events().list(calendarId=prodnumberscal, pageToken=page_token).execute()
        for event in events['items']:
            event_id = event['id']
            events_list.append(event_id)
            #print event_id
        page_token = events.get('nextPageToken')
        if not page_token:
            break

except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')
except:
    page_token = None
    while True:
        events = service.events().list(calendarId=prodnumberscal, pageToken=page_token).execute()
        for event in events['items']:
            event_id = event['id']
            events_list.append(event_id)
            #print event_id
        page_token = events.get('nextPageToken')
        if not page_token:
            break

###########################
####  END AUTH SECTION
###########################
#############################Get Data to send to API###########################
#from python.gcal_functions import stillcomplete, fashioncomplete, sql_query_production_numbers

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

    connection.close()
    return prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict



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

#############################END Funcx Section##########################

######RUN######


## Delete all Events by ID prior to reup
for event in events_list:
    service.events().delete(calendarId=prodnumberscal, eventId=event).execute()
    
print "Deleted all Events"    
#calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
#cals = service.calendarList().get(calendarId='john.bragato@gmail.com').execute()

#############################Get Data Functions to Query DB###########################


prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict = sql_query_production_numbers()

###########################################
stillcomplete_dict     = stillcomplete()
fashioncomplete_dict   = fashioncomplete()

lotsofdicts = [prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict, stillcomplete_dict, fashioncomplete_dict]
##############################################################################

for iterdict in lotsofdicts:
    count = 0
    for k,v in iterdict.iteritems():
        import datetime, time
        for value in [v]:
            try:
                titlekv = str(v['role'])
            except:
                titlekv = 'Studio_Shots'
            try:
                desckv = str(v['total'])
                desckv = desckv.replace('&', 'And')
                desckv = desckv.replace('%', ' Percent')
#                sdatekvraw = '{:%Y,%m,%d,12,30,00,00,00,00}'.format(k)
#                edatekvraw = '{:%Y,%m,%d,21,50,00,00,00,00}'.format(k)
#                sdatekvsplit = sdatekvraw.split(",")
#                edatekvsplit = edatekvraw.split(",")
#                sdatekv = map(int,sdatekvsplit)
#                edatekv = map(int,edatekvsplit)
                
                titleid = '{0} - {1}'.format(desckv,titlekv)
                #if v['total'] < 200:
                #    congrats = '<>'
                #elif v['total'] >= 200:
                #    if v['total'] <= 300:
                #        congrats = '<-->'
                #    else:
                #        congrats = '<-*->'
                descfull = '{0} Total for {1} is {2}\n'.format(titlekv, str(k)[:10], desckv)
                descfull = str(descfull)
                count += 1
                
                ##TODO: rework choose color process below with following 3 line of code 
                # keycode =  v['role']
                #functions = {9: 'Production', 8: 'Copy', 7: 'Retouching'}
                #functions.get(keycode, unknown_key_pressed)()

                ## Choose Color of Event Based on Role
                lockv = v['role']
                if lockv == 'Production':
                    colorId = '9'
                elif lockv == 'Copy':
                    colorId = '8'
                elif lockv == 'Retouching':
                    colorId = '7'
                elif lockv == 'Fashion':
                    colorId = '6'
                    print descfull
                    
                elif lockv == 'Still':
                    colorId = '5'
                elif lockv == 'Samples_Received':
                    colorId = '4'

                event = {
                  'summary': titleid,
                  'description': descfull,
                  'location': lockv,
                  'colorId': colorId,
                  'start': {
                    'date': "{0:%Y-%m-%d}".format(k.date()),
                    'timeZone': 'America/New_York'
                  },
                  'end': {
                    'date': "{0:%Y-%m-%d}".format(k.date()),
                    'timeZone': 'America/New_York'
                  },
                #  'recurrence': [
                #    'RRULE:FREQ=WEEKLY;UNTIL=20110701T100000-07:00',
                #  ],
#                  'attendees': [
#                    {
#                      'email': 'james.hoetker@bluefly.com',
#                      # Other attendee's data...
#                    },
#                    # ...
#                  ],
                }
                
                created_event = service.events().insert(calendarId=prodnumberscal, body=event).execute()
                print created_event['id']
            except OSError:
                print 'ERROR {}'.format(event)
                pass
                