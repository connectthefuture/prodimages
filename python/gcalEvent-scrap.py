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