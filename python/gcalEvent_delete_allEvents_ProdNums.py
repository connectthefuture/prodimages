#!/usr/bin/env python

def gcal_login_jb(myemail='john.bragato@gmail.com', password='yankee17'):
    from GoogleCalendar import GoogleCalendarMng
    import xml
    gCalMNG = GoogleCalendarMng()
    myemail = myemail
    gCalMNG.connect(myemail, password)
    return gCalMNG



##### RUN ####
default_cal = gcal_login_jb().getCalendars()[2]
events = default_cal.getEvents()
# Delete all Calendar Events prior to Fresh insert
print len(events)
while len(events) >= 1:
    for event in events:
        event.delete()
        events = default_cal.getEvents()
    default_cal = gcal_login_jb().getCalendars()[1]
    events = default_cal.getEvents()
