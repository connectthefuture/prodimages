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

EventEntry entry = ...

AtomLink link = new AtomLink("image/gif", "http://schemas.google.com/gCal/2005/webContent");
link.Title = "Test content";
link.HRef = "http://www.google.com/calendar/images/google-holiday.gif";
WebContent content = new WebContent();
content.Url = "http://www.google.com/logos/july4th06.gif";
content.Width = 270;
content.Height = 130;
link.ExtensionElements.Add(content);
entry.Links.Add(link);
entry.Update(


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
