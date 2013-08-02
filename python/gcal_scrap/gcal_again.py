#!/usr/bin/env python
calendarId = 'me36k96u55g9gts6fmu4tgq4ts@group.calendar.google.com'

#bfly-client_id='633559698772.apps.googleusercontent.com'
#bfly-client_secret='9iqW9BTnwTt8rWg4fQtJL3CG'
#bfly-user_agent='bragato-cal-2013/v1'
#bfly-developerKey='AIzaSyCjPID1d7hKLiRCjMTWYj6DjagF8viG8wM'

client_id='222573514309.apps.googleusercontent.com'
user_agent='gcaltests-2013/v1'
client_secret='r4BerSFPl7p6bHr2uYK4MHik'
developerKey='AIzaSyB101MP8UXS7I8jIgJ0IYEDhr3arua5mB0'

import os.path
here = os.path.dirname(os.path.realpath(__file__))
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
#FLAGS.auth_local_webserver = False

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
service = build(serviceName='calendar', version='v3', http=http,
       developerKey=developerKey)

    

from gdata import calendar
import pprint

def getEvents(calendarId=calendarId, pageToken=None):
    events = service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin='2012-11-01T00:00:00-08:00',
        timeMax='2013-11-30T00:00:00-08:00',
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

