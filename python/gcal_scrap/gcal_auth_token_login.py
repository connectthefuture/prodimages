#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 21:33:00 2013

@author: JCut
"""

calendarId = 'john.bragato@gmail.com'

import google_calendar
import pprint

def getEvents(pageToken=None):
    events = google_calendar.service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin='2012-11-01T00:00:00-08:00',
        timeMax='2012-11-30T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
    return events

def main():
    events = getEvents()
    while True:
        for event in events['items']:
            pprint.pprint(event)
        page_token = events.get('nextPageToken')
        if page_token:
            events = getEvents(page_token)
        else:
            break

if __name__ == '__main__':
    main()

client_id='222573514309.apps.googleusercontent.com'
client_secret='r4BerSFPl7p6bHr2uYK4MHik'
user_agent='gcal_tests/v01'
developerKey='AIzaSyB101MP8UXS7I8jIgJ0IYEDhr3arua5mB0'

import os.path
here = os.path.dirname(os.path.realpath('/Users/JCut/Dropbox/Dropbox_sites/SpyderMac'))
storage_file = os.path.join(here, 'calendar.dat')

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
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

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http, developerKey=developerKey)
