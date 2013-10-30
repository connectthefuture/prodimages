from string import Template
CompletionList_Template = Template('Incomplete Styles: $incompletecount\n$incomplete_styles\nCompleted Styles: $completecount\n$complete_styles')

CompletionList = CompletionList_Template.substitute(incompletecount=len(incomplete_styles),incomplete_styles=incomplete_styles,completecount=len(complete_styles),complete_styles=complete_styles)

print output


try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time
'''

<atom:link rel="http://schemas.google.com/gCal/2005/webContent"
           title="$titleid"
           href="$locv">
           type="text/html or image/*"
  <gCal:webContent url="a link to the content"
                   width="pixels"
                   height="pixels" />
</atom:link>
'''

event_entry = gdata.calendar.data.CalendarEventEntry()
link_type = 'application/x-google-gadgets+xml'
atomlink = atom.Link(link_type, "http://schemas.google.com/gCal/2005/webContent")
atomlink.Title = "SUPER TEST"
href = 'https://raw.github.com/relic7/prodimages/master/html_css_js/html/compiledPhotoReport.html'
#href = 'http://l.yimg.com/j/assets/i/us/sp/v/mlb/players_l/20130405/7054.1.jpg'
atomlink.HRef = href
web_content = gdata.calendar.WebContent()
web_content.url = 'https://raw.github.com/relic7/prodimages/master/html_css_js/html/compiledPhotoReport.html' #"http://www.google.com/logos/july4th06.gif"
web_content.width = 370
web_content.height = 530
web_content.gadget_pref.append(gdata.calendar.data.WebContentGadgetPref(name='color', value='green'))
atomlink.extension_elements.append(web_content)
event_entry.link.append(atomlink)
new_event = glogin_jb.cal_client.InsertEvent(event_entry)



def InsertCalendar(cal_client=gcal_connect, title=titleid, description=descfull, time_zone='America/New_York', hidden=False, location=locv, color=colorflag):
    import gdata, gevent
    """Creates a new calendar using the specified data."""
    print 'Creating new calendar with title "%s"' % title
    calendar_new = gdata.calendar.data.CalendarEntry()
    calendar_new.title = atom.data.Title(text=title)
    calendar_new.summary = atom.data.Summary(text=description)
    calendar_new.where.append(gdata.calendar.data.CalendarWhere(value=location))
    calendar_new.color = gdata.calendar.data.ColorProperty(value=color)
    calendar_new.timezone = gdata.calendar.data.TimeZoneProperty(value=time_zone)
    if hidden:
      calendar_new.hidden = gdata.calendar.dats = gdata.calendar.data.HiddenProperty(value='false')
    new_calendar = cal_client.InsertCalendar(new_calendar=calendar_new)
    return new_calendar


def UpdateCalendar(calendar_name=selected_calendar, cal_client=gcal_connection, title=titleid, description=descfull, color=colorflag):
    import gdata, gevent, atom
    """Updates the title and, optionally, the color of the supplied calendar"""
    print 'Updating the calendar titled "%s" with the title "%s"' % (calendar_name.title.text, title)
    calendar_name.title = atom.data.Title(text=title)
    if color is not None:
        calendar_name.color = gdata.calendar.data.ColorProperty(value=color)
        updated_calendar = cal_client.Update(calendar_name)
    return updated_calendar




import GCalendar_Class
import gdata
#gcal_client = GCalendar_Class.GCalendar(email='john.bragato@gmail.com', password='yankee17')
#https://www.google.com/calendar/feeds/khn4f4kmgcu19h7tgh8ejv8894%40group.calendar.google.com/private-8cd060685625899c147572bcfe26fc55/basic'
myemail = 'john.bragato@gmail.com'
password = 'yankee17'
#calendar_id = 'khn4f4kmgcu19h7tgh8ejv8894%40group.calendar.google.com'
#private_id = '/private-8cd060685625899c147572bcfe26fc55/basic'
ev_start = '2013-08-14'
ev_end = '2013-08-24'
#calendar_id = 'khn4f4kmgcu19h7tgh8ejv8894%40group.calendar.google.com/private-8cd060685625899c147572bcfe26fc55/basic/onusa2c5mbu26tpo710hljd1hc'
calendar_id = 'khn4f4kmgcu19h7tgh8ejv8894%40group.calendar.google.com/private-8cd060685625899c147572bcfe26fc55/basic'
default1_calid = 'http://www.google.com/calendar/feeds/khn4f4kmgcu19h7tgh8ejv8894%40group.calendar.google.com/private-8cd060685625899c147572bcfe26fc55/basic'

## Cal Ent FEED

gcal_client = gdata.calendar.client.CalendarClient(source=myemail)
gcal_client.ClientLogin(myemail, password, gcal_client.source)
feed_uri = gcal_client.get_calendar_event_feed(calendar=calendar_id)
event_uri = os.path.join(feed_uri)
calendar_entry = gcal_client.get_calendar_entry(event_uri, desired_class=gdata.calendar.data.CalendarEventEntry())

## EVENTS FEED
eventsfeed = gcal_client.get_calendar_event_feed()
event_entries = eventsfeed.entry[:]
for entry in event_entries:
    print entry
    #entry_color = entry.color.value


eventsfeed.title = atom.Title(text='1AMTitle')

event.title = atom.Title(text=titleid)
event.when.append(gdata.calendar.When(start_time=ev_start, end_time=ev_end))

## OwnCalFeed
## Get Entries from own cal
ownfeed = gcal_client.GetOwnCalendarsFeed()
own_etag = ownfeed.etag
ownfeed.title = atom.Title(text=titleid)

entries = ownfeed.entry[:]
for entry in entries:
    print entry
    entry_color = entry.color.value


wc = gdata.calendar.WebContent()
wc.url = 'http://www.thefreedictionary.com/_/WoD/wod-module.xml'
wc.width = '300'
wc.height = '136'
wc.gadget_pref.append(gdata.calendar.WebContentGadgetPref(name='Days', value='1'))
wc.gadget_pref.append(gdata.calendar.WebContentGadgetPref(name='Format', value='0'))

wcl = gdata.calendar.WebContentLink()
wcl.title = 'Word of the Day'
wcl.href = 'http://www.thefreedictionary.com/favicon.ico'
wcl.type = 'application/x-google-gadgets+xml'
wcl.web_content = wc

event.link.append(wcl)

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

import requests
from urllib import urlencode
import json
from subprocess import Popen

client_id='222573514309.apps.googleusercontent.com'
client_secret='r4BerSFPl7p6bHr2uYK4MHik'
user_agent='gcal_tests/v01'
developerKey='AIzaSyB101MP8UXS7I8jIgJ0IYEDhr3arua5mB0'
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
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

  r = requests.get(base_url + "auth?%s" % urlencode(authorization_code_req),
                   allow_redirects=False)
  print "Request Gotten"
  url = r.headers.get('location')
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
  r = requests.get("https://www.googleapis.com/oauth2/v2/userinfo",
                   headers=authorization_header)
  print r.text



def get_calendar_list():
  global authorization_code
  global access_token

  authorization_code = retrieve_authorization_code()
  tokens = retrieve_tokens(authorization_code)
  access_token = tokens['access_token']
  authorization_header = {"Authorization": "OAuth %s" % access_token}

  r = requests.get("https://www.googleapis.com/calendar/v3/users/me/calendarList",
                   headers=authorization_header)
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
    url = ("https://www.googleapis.com/calendar/v3/calendars/%s/events?key=%s" %
           (quote_plus(calendar_id), quote_plus(api_key)))
    r = requests.get(url, headers=authorization_header)

    events = json.loads(r.text)
    for event in events['items']:
      print event.get('summary', '(Event title not set)')
      if event['status'] != 'cancelled':
        start, end = _get_start_end_time(event)
        print "   start : ", start, "  end : ", end


def main():
  get_events_list()


if __name__ == '__main__':
  main()












def sql_query_production_numbers():
    import sqlalchemy
    from collections import defaultdict
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
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
            tmp_dict['total'] = row['completion_total']
            tmp_dict['role'] = 'Production'
            prodcomplete_dict[row['prod_complete_dt']] = tmp_dict


 ### Get Sample Received Totals and Build Dict of key value pairs
    querymake_sample_received = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as sample_total,
    MAX(to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')) AS sample_dt
    FROM POMGR.PRODUCT_COLOR
    LEFT JOIN POMGR.SAMPLE ON POMGR.PRODUCT_COLOR.ID = POMGR.SAMPLE.PRODUCT_COLOR_ID
    LEFT JOIN POMGR.SAMPLE_TRACKING ON POMGR.SAMPLE.ID = POMGR.SAMPLE_TRACKING.SAMPLE_ID
    LEFT JOIN POMGR.LK_SAMPLE_STATUS ON POMGR.SAMPLE_TRACKING.STATUS_ID = POMGR.LK_SAMPLE_STATUS.ID
    WHERE (POMGR.SAMPLE_TRACKING.CREATE_DT >= TRUNC(SysDate - 25)
    AND POMGR.LK_SAMPLE_STATUS.NAME = 'Scanned In at Bluefly')
    GROUP BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')
    ORDER BY to_date(POMGR.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD') DESC"""
    samples_received = connection.execute(querymake_sample_received)
    samples_received_dict = {}
    for row in samples_received:
            tmp_dict = {}
            tmp_dict['total'] = row['sample_total']
            tmp_dict['role'] = 'Samples_Received'
            samples_received_dict[row['sample_dt']] = tmp_dict

    querymake_copynumbers = """SELECT COUNT(DISTINCT POMGR.PRODUCT_COLOR.ID) as copy_total,
    POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_complete_dt
    FROM POMGR.PRODUCT_COLOR
    WHERE POMGR.PRODUCT_COLOR.COPY_READY_DT >= TRUNC(SysDate - 25)
    GROUP BY POMGR.PRODUCT_COLOR.COPY_READY_DT
    ORDER BY POMGR.PRODUCT_COLOR.COPY_READY_DT DESC"""
    copycomplete = connection.execute(querymake_copynumbers)
    copycomplete_dict = {}
    for row in copycomplete:
        tmp_dict = {}
        tmp_dict['total'] = row['copy_total']
        tmp_dict['role'] = 'Copy'
        copycomplete_dict[row['copy_complete_dt']] = tmp_dict

#
