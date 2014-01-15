#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import os

##########################Vars
client_id='924881045523-kc7leju7role0too3k4itlo864eprl1u.apps.googleusercontent.com'
client_secret='rqZxYuy0Cht37rJ0GSZ05YoY'
user_agent='Python2.7'
BROWSERdeveloperKey='AIzaSyBHozNPRDnVkdPo_JlP_4TLbNrJIsd3bQ4'
SERVERdeveloperKey='AIzaSyDe68JsIJK5O5Cqd-tAVGqaSeHqcFCNPh8'

here = os.path.dirname(os.path.realpath(os.path.curdir))
storage_file = os.path.join('/usr/local', 'batchRunScripts', 'calendar.dat')

############################
FLAGS = gflags.FLAGS

# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id=client_id,
    client_secret=client_secret,
    scope='https://www.googleapis.com/auth/calendar',
    user_agent=user_agent)

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

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

prodnumberscal = 'k8oohvl27sq3u0odgafpbmdl6s@group.calendar.google.com'

# Build a service object for interacting with the API.
service = build(serviceName='calendar', version='v3', http=http)


## Getting Event Info
#page_token = None
#try:    
#    while True:
#        events = service.events().list(calendarId=prodnumscal, pageToken=page_token).execute()
#        for event in events['items']:
#            print event['summary']
#        page_token = events.get('nextPageToken')
#        if not page_token:
#            break
#except:
#    page_token = None
#    while True:
#        events = service.events().list(calendarId=prodnumscal, pageToken=page_token).execute()
#        for event in events['items']:
#            print event['summary']
#        page_token = events.get('nextPageToken')
#        if not page_token:
#            break

#calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
#cals = service.calendarList().get(calendarId='john.bragato@gmail.com').execute()

#############################Get Data to send to API###########################
from python.gcal_functions import sqlQueryEventsUpcoming


future_events, future_styles = sqlQueryEventsUpcoming()
#for key,value in future_styles.iteritems():
#    #for kv in [value]:
#    #d[value['event_id']].append(key)
#    print "Event {0} has {1} Styles".format(key,len(value))

#print d

count = 0
for k,v in future_events.iteritems():
    import datetime, time
    for value in [v]:
        titlekv = str(value['event_id'])
        desckv = str(value['event_title'])
        desckv = desckv.replace('&', 'And')
        desckv = desckv.replace('%', ' Percent')
        colorstyles = future_styles.get(value['event_id'])
        colorstyles = sorted(colorstyles)
        incomplete = []
        complete = []
        for colorstyle in colorstyles:
            if colorstyle[1] == 'Production Complete':
                complete.append(colorstyle)
            elif colorstyle[1] == 'Production Incomplete':
                incomplete.append(colorstyle)
        incomplete_styles = "{0} Incomplete Styles = {1}".format(len(incomplete),incomplete)
        complete_styles = "{0} Complete Styles = {1}".format(len(complete),complete)
        colorstyles_statuses = "{0}\n{1}".format(incomplete_styles,complete_styles)
        count_complete = len(complete)
        count_complete += .00
        count_incomplete = len(incomplete)
        count_incomplete += .00
        count_total = count_complete + count_incomplete
        progress = "{:.0%}".format(count_complete/count_total)
        if len(incomplete) == 0:
            event_complete_flag = True
        else:
            event_complete_flag = False

        status = value['production_status']
        prod_category = str(value['prod_category'])
        category_id = value['category_id']

        pmurl = "http://pm.bluefly.corp/manager/event/editevent.html?id="
        pmimgs = "http://pm.bluefly.corp/manager/event/viewproductimages.html?id="
        bcurl = "http://www.belleandclive.com/browse/sales/details.jsp?categoryId="

        pmurl = pmurl + titlekv
        pmimgs = pmimgs + titlekv
        bcurl = pmurl + titlekv

        try:
            if colorstyles == None:
                lockv = str(pmurl)
            else:
                lockv = str(pmimgs)
        except TypeError:
            lockv = str(bcurl)

        sdatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_start'])
        edatekvraw = '{:%Y,%m,%d,%H,%M,%S,00,00,00}'.format(value['ev_end'])
        sdatekvsplit = sdatekvraw.split(",")
        edatekvsplit = edatekvraw.split(",")
        sdatekv = map(int,sdatekvsplit)
        edatekv = map(int,edatekvsplit)
        titleid = 'Event {0} - {2} Complete - {1}'.format(titlekv,desckv,str(progress))
        descfull = '{0} {1} in Event {2}:\n {3}\n'.format(len(colorstyles), prod_category, titlekv, colorstyles_statuses)
        descfull = str(descfull)
        count += 1
        event_start = value['ev_start']
        event_end = value['ev_end']
        ## Choose Color of Event Based on Role
        
        teststatus = count_complete/count_total
        if teststatus > .98:
            colorId = '9'
        elif teststatus > .90:
            colorId = '8'
        elif teststatus > .70:
            colorId = '7'
        elif teststatus > .50:
            colorId = '4'
        elif teststatus > .30:
            colorId = '3'
        else:
            colorId = '2'
        
        lockv = pmurl
        event = {
          'summary': titleid,
          'description': descfull,
          'location': lockv,
          'colorId': colorId,
          'start': {
            'dateTime': event_start.isoformat(),
            'timeZone': 'America/New_York'
          },
          'end': {
            'dateTime': event_end.isoformat(),
            'timeZone': 'America/New_York'
          },
        #  'recurrence': [
        #    'RRULE:FREQ=WEEKLY;UNTIL=20110701T100000-07:00',
        #  ],
          # 'attendees': [
          #   {
          #     'email': 'james.hoetker@bluefly.com',
          #     # Other attendee's data...
          #   },
          #   # ...
          # ],
        }
        
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print created_event['id']
    except OSError:
        print 'ERROR {}'.format(event)
        pass
        