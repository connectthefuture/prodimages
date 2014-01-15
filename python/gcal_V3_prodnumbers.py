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
from python.gcal_functions import stillcomplete, fashioncomplete, sql_query_production_numbers

prodcomplete_dict, retouchcomplete_dict, copycomplete_dict, samples_received_dict = sql_query_production_numbers()

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
                descfull = '{0} Total for {1} is {2}'.format(titlekv, str(k)[:10], desckv)
                descfull = str(descfull)
                count += 1
                
                ## Choose Color of Event Based on Role
                titlekv = v['role']
                if titlekv == 'Retouching':
                    colorId = '9'
                elif titlekv == 'Production':
                    colorId = '8'
                elif titlekv == 'Copy':
                    colorId = '7'
                elif titlekv == 'Fashion':
                    colorId = '6'
                elif titlekv == 'Still':
                    colorId = '5'
                elif titlekv == 'Samples_Received':
                    colorId = '4'
                
                lockv = titlekv
                event = {
                  'summary': titleid,
                  'description': descfull,
                  'location': lockv,
                  'colorId': colorId,
                  'start': {
                    'dateTime': k.isoformat(),
                    'timeZone': 'America/New_York'
                  },
                  'end': {
                    'dateTime': k.isoformat(),
                    'timeZone': 'America/New_York'
                  },
                #  'recurrence': [
                #    'RRULE:FREQ=WEEKLY;UNTIL=20110701T100000-07:00',
                #  ],
                  'attendees': [
                    {
                      'email': 'james.hoetker@bluefly.com',
                      # Other attendee's data...
                    },
                    # ...
                  ],
                }
                
                created_event = service.events().insert(calendarId=prodnumberscal, body=event).execute()
                print created_event['id']
            except OSError:
                print 'ERROR {}'.format(event)
                pass
                
