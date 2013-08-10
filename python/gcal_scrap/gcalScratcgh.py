# -*- coding: utf-8 -*-
"""
This scripts reqire a third party module 'requests'.
You can get it from PyPI, i.e. you can install it using
easy_install or pip.

   http://docs.python-requests.org/en/v0.10.4/

Original source code is written by shin1ogawa, which is in Java.

   https://gist.github.com/1899391

Materials for this session are avaliable in following URLs:

  - Hands on material: http://goo.gl/oAhzI
  - Google APIs Console: https://code.google.com/apis/console/
  - Google APIs Explorer: http://code.google.com/apis/explorer/
  - OAuth 2.0 Playground: https://code.google.com/oauthplayground/
"""

__author__ = "@ymotongpoo"


from urllib import urlencode
import json
from subprocess import Popen

import time, sha, jwt, hashlib, requests, OpenSSL
from oauth2client import anyjson

client_email = "222573514309@developer.gserviceaccount.com"
client_id='222573514309.apps.googleusercontent.com'
client_secret='r4BerSFPl7p6bHr2uYK4MHik'
user_agent='gcal_tests/v01'
developerKey='AIzaSyB101MP8UXS7I8jIgJ0IYEDhr3arua5mB0'
api_key = developerKey
iat = int("{0}".format(time.time())[:10])
exp = iat + 3600

#redirect_uri = "urn:localhost" #"urn:ietf:wg:oauth:2.0:oob"
#redirect_uri = "urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob"
redirect_uri = r"http://localhost:8000"
base_url = r"https://accounts.google.com/o/oauth2/"
authorization_code = ""
access_token = ""


"""
Retrieving authorization_code from authorization API.
"""
def retrieve_authorization_code():
  authorization_code_req = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": (r"https://www.googleapis.com/auth/userinfo.profile" +
              r" https://www.googleapis.com/auth/userinfo.email" +
              r" https://www.googleapis.com/auth/calendar")
    }

  r = requests.get(base_url + "auth?%s" % urlencode(authorization_code_req), allow_redirects=False)
  print "Request Gotten"
  url = r.headers.get('location')
  print url
  Popen(["open", url])

  authorization_code = raw_input("\nAuthorization Code >>> ")
  return authorization_code


"""
Retrieving access_token and refresh_token from Token API.
"""
def retrieve_tokens(authorization_code):
  access_token_req = {
    "code" : authorization_code,
    "client_id" : client_id,
    "client_secret" : client_secret,
    "redirect_uri" : redirect_uri,
    "grant_type": "authorization_code",
    }
  content_length=len(urlencode(access_token_req))
  access_token_req['content-length'] = str(content_length)

  r = requests.post(base_url + "token", data=access_token_req)
  data = json.loads(r.text)
  return data



"""
Sample code of fetching user information from userinfo API.
"""
def get_userinfo():
  global authorization_code
  authorization_code = retrieve_authorization_code()
  tokens = retrieve_tokens(authorization_code)
  access_token = tokens['access_token']
  authorization_header = {"Authorization": "OAuth %s" % access_token}
  r = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=authorization_header)
  print r.text



def get_calendar_list():
  global authorization_code
  global access_token

  authorization_code = retrieve_authorization_code()
  tokens = retrieve_tokens(authorization_code)
  access_token = tokens['access_token']
  authorization_header = {"Authorization": "OAuth %s" % access_token}

  r = requests.get("https://www.googleapis.com/calendar/v3/users/me/calendarList", headers=authorization_header)
  return r.text


def _get_start_end_time(event):
  try:
    if event['start'].has_key('date'):
      start = event['start']['date']
    elif event['start'].has_key('dateTime'):
      start = event['start']['dateTime']
    else:
      start = 'N/A'

    if event['end'].has_key('date'):
      end = event['end']['date']
    elif event['end'].has_key('dateTime'):
      end = event['end']['dateTime']
    else:
      end = 'N/A'
    return start, end

  except:
    return event['etag'], event['status']


def get_events_list():
  global authorization_code
  global access_token

  data = json.loads(get_calendar_list())
  for calendar in data['items']:
    calendar_id = calendar['id']
    print calendar['summary']

    if authorization_code == "" or access_token == "":
      authorization_code = retrieve_authorization_code()
      tokens = retrieve_tokens(authorization_code)
      access_token = tokens['access_token']

    authorization_header = {"Authorization": "OAuth %s" % access_token}
    url = ("https://www.googleapis.com/calendar/v3/calendars/%s/events?key=%s" % ((calendar_id), (api_key)))
    r = requests.get(url, headers=authorization_header)

    events = json.loads(r.text)

    try:
        for event in events['items']:
            print event.get('summary', '(Event title not set)')
            if event['status'] != 'cancelled':
                start, end = _get_start_end_time(event)
                print "   start : ", start, "  end : ", end
    except:
        pass
    return events

def main():
  get_events_list()


if __name__ == '__main__':
  main()



import os.path
here = os.path.dirname(os.path.realpath(os.path.expanduser('~')))
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
service = build(serviceName='calendar', version='v3', http=http,
       developerKey=developerKey)
